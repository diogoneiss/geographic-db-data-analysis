#!/usr/bin/env python3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Any

import pandas as pd
import numpy as np
from sqlalchemy import text
from tqdm import tqdm

# ---- Reuse helpers from your existing script in the same folder ----
from getTables import (  # rename if your file has a different name/module
    DB_NAME, DB_HOST, DB_PORT, SCHEMA, TABLE_LIMIT, COLUMN_LIMIT,
    NULL_STR, GEOM_UDT_NAMES,
    get_engine, connect,
    fetch_tables,
    get_first_n_columns_with_types,
    _trim_cell, _format_number
)

# ---------- Output path ----------
OUTPUT_STATS = Path("eleicoes22_stats.md")

# ---------- Typing sets (aligned with your main script) ----------
NUMERIC_UDT  = {"int2","int4","int8","float4","float8","numeric","money"}
DATE_UDT     = {"date","timestamp","timestamptz","time","timetz"}
BOOL_UDT     = {"bool"}
TEXTLIKE_UDT = {"text","varchar","bpchar","uuid"}

# ---------- Ignore list (tables) ----------
IGNORE_TABLES = {
    #"votacao_secao_2022_sc",
    #"br_ibge_censo_2022_populacao_idade_sexo",
}

IGNORE_PREFIX = "ignore_"

# ---------- Fast iteration toggle ----------
FAST_MODE  = False   # set True to stop early
FAST_LIMIT = 5      # number of tables to process when FAST_MODE is True

# ---------- Helpers reused/extended ----------
def is_id_col(name: str) -> bool:
    n = name.lower()
    return n.startswith("id_") or n.endswith("_id")

def split_columns_for_stats(cur, schema: str, table: str, limit: int = COLUMN_LIMIT):
    cols = get_first_n_columns_with_types(cur, schema, table, limit)
    numeric, categorical, skipped_ids = [], [], []
    for name, udt in cols:
        if udt in GEOM_UDT_NAMES:
            continue
        if is_id_col(name):
            skipped_ids.append(name)
            continue
        if udt in NUMERIC_UDT:
            numeric.append((name, udt))
        elif udt in TEXTLIKE_UDT or udt in DATE_UDT or udt in BOOL_UDT:
            categorical.append((name, udt))
        # skip json/array/other exotic types for profiling
    return numeric, categorical, skipped_ids

def numeric_stats_sql(schema: str, table: str, num_cols: List[Tuple[str,str]]) -> str:
    fqn = f'"{schema}"."{table}"'
    sels = ['COUNT(*) AS "__n__"']
    for col, _ in num_cols:
        q = f'{fqn}."{col}"'
        sels += [
            f'COUNT({q}) AS "{col}__non_null"',
            f'(COUNT(*) - COUNT({q})) AS "{col}__nulls"',
            f'COUNT(DISTINCT {q}) AS "{col}__distinct"',
            f'AVG({q})::float AS "{col}__mean"',
            f'STDDEV_POP({q})::float AS "{col}__stddev"',
            f'MIN({q}) AS "{col}__min"',
            f'percentile_disc(0.25) WITHIN GROUP (ORDER BY {q}) AS "{col}__p25"',
            f'percentile_disc(0.50) WITHIN GROUP (ORDER BY {q}) AS "{col}__median"',
            f'percentile_disc(0.75) WITHIN GROUP (ORDER BY {q}) AS "{col}__p75"',
            f'MAX({q}) AS "{col}__max"',
        ]
    return "SELECT " + ", ".join(sels) + f" FROM {fqn};"

def numeric_outliers_query(schema: str, table: str, col: str, low: float, high: float) -> str:
    fqn = f'"{schema}"."{table}"'
    return (
        f'SELECT SUM(CASE WHEN "{col}" < {low} OR "{col}" > {high} '
        f'THEN 1 ELSE 0 END)::bigint AS outliers FROM {fqn};'
    )

def categorical_summary_sql(schema: str, table: str, col: str) -> str:
    fqn = f'"{schema}"."{table}"'
    return (
        f'SELECT COUNT(*) AS n, COUNT("{col}") AS non_null, '
        f'COUNT(*) - COUNT("{col}") AS nulls, COUNT(DISTINCT "{col}") AS distinct '
        f'FROM {fqn};'
    )

def categorical_topk_sql(schema: str, table: str, col: str, k: int = 5) -> str:
    fqn = f'"{schema}"."{table}"'
    return (
        f'SELECT "{col}" AS value, COUNT(*) AS cnt FROM {fqn} '
        f'GROUP BY 1 ORDER BY cnt DESC NULLS LAST, value ASC LIMIT {int(k)};'
    )

def markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    head = "| " + " | ".join(headers) + " |\n"
    sep  = "| " + " | ".join(["---"] * len(headers)) + " |\n"
    lines = []
    for r in rows:
        cells = []
        for v in r:
            if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool):
                if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
                    cells.append(NULL_STR)
                else:
                    cells.append(_format_number(v))
            else:
                cells.append(_trim_cell("" if v is None else v))
        lines.append("| " + " | ".join(cells) + " |")
    return head + sep + "\n".join(lines) + "\n"

def write_stats_header(out, schema: str, total_tables: int, ignored: List[str]):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out.write(f"# Statistical profile for `{schema}`\n\n")
    out.write(f"- Generated at: {ts}\n")
    out.write(f"- Database: {DB_NAME} @ {DB_HOST}:{DB_PORT}\n")
    out.write(f"- Tables discovered: {total_tables}\n")
    out.write(f"- Tables profiled: up to {TABLE_LIMIT} (cap)\n")
    out.write(f"- Ignored tables: {', '.join(sorted(ignored)) if ignored else '(none)'}\n")
    out.write(f"- Columns per table considered: up to {COLUMN_LIMIT} (geometry/geography skipped; id_* and *_id skipped)\n")
    out.write(f"- Outliers = Tukey fences (Q1−1.5·IQR, Q3+1.5·IQR)\n")
    out.write(f"- Fast mode: {FAST_MODE} (limit={FAST_LIMIT})\n")
    out.write("\n---\n\n")

# ---------- Main CLI ----------
def main():
    try:
        engine = get_engine()
        with connect() as conn, conn.cursor() as cur, OUTPUT_STATS.open("w", encoding="utf-8") as out:
            all_tables = [t for t in fetch_tables(cur, SCHEMA) if t not in IGNORE_TABLES]
            tables = all_tables[:TABLE_LIMIT]

            write_stats_header(out, SCHEMA, len(all_tables), list(IGNORE_TABLES))

            processed = 0
            for idx, table in enumerate(tqdm(tables, desc="Stats", unit="tbl"), start=1):
                if FAST_MODE and processed >= FAST_LIMIT:
                    break
                table_start = time.perf_counter()
                try:
                    out.write(f"## {idx}. {SCHEMA}.{table}\n\n")

                    # Column splits
                    split_start = time.perf_counter()
                    num_cols, cat_cols, skipped_ids = split_columns_for_stats(cur, SCHEMA, table, COLUMN_LIMIT)
                    split_time = time.perf_counter() - split_start

                    if skipped_ids:
                        out.write(f"_Skipped ID-like columns (id_*, *_id):_ `{', '.join(skipped_ids)}`\n\n")

                    # ---------- Numeric aggregate stats ----------
                    numeric_time = 0.0
                    outlier_rows: List[List[Any]] = []
                    numeric_sql_rendered = ""
                    if num_cols:
                        agg_sql = numeric_stats_sql(SCHEMA, table, num_cols)
                        numeric_sql_rendered = agg_sql

                        t0 = time.perf_counter()
                        df_agg = pd.read_sql_query(text(agg_sql), engine)
                        numeric_time = time.perf_counter() - t0

                        row = df_agg.iloc[0].to_dict()
                        headers = ["column","non_null","nulls","nulls_%","distinct","mean","stddev","min","p25","median","p75","max"]
                        rows = []
                        outliers_time_total = 0.0

                        outlier_headers = ["column", "low", "high", "outliers", "time (s)"]
                        for col, _ in num_cols:
                            non_null = int(row.get(f"{col}__non_null") or 0)
                            nulls    = int(row.get(f"{col}__nulls") or 0)
                            total    = non_null + nulls
                            nulls_pct = (nulls / total * 100.0) if total > 0 else 0.0

                            distinct = row.get(f"{col}__distinct")
                            mean     = row.get(f"{col}__mean")
                            stddev   = row.get(f"{col}__stddev")
                            vmin     = row.get(f"{col}__min")
                            p25      = row.get(f"{col}__p25")
                            med      = row.get(f"{col}__median")
                            p75      = row.get(f"{col}__p75")
                            vmax     = row.get(f"{col}__max")

                            rows.append([col, non_null, nulls, round(nulls_pct, 4), distinct, mean, stddev, vmin, p25, med, p75, vmax])

                            # outliers
                            if p25 is not None and p75 is not None:
                                iqr = float(p75) - float(p25)
                                low = float(p25) - 1.5 * iqr
                                high = float(p75) + 1.5 * iqr
                                oq = numeric_outliers_query(SCHEMA, table, col, low, high)
                                t1 = time.perf_counter()
                                df_o = pd.read_sql_query(text(oq), engine)
                                dt = time.perf_counter() - t1
                                outliers = int(df_o.iloc[0]["outliers"]) if not df_o.empty else 0
                                outlier_rows.append([col, low, high, outliers, round(dt, 6)])
                                outliers_time_total += dt
                            else:
                                outlier_rows.append([col, None, None, None, 0.0])

                        out.write("### Numeric columns\n\n")
                        out.write(markdown_table(headers, rows) + "\n")

                        # Outliers table
                        out.write("#### Outliers (Tukey fences)\n\n")
                        out.write(markdown_table(outlier_headers, outlier_rows) + "\n")

                        # SQL used (aggregate)
                        out.write("**SQL (numeric aggregate)**\n\n```sql\n")
                        out.write(numeric_sql_rendered.strip() + "\n```\n\n")

                        # Template for outlier SQL
                        out.write("**SQL template (numeric outliers per column)**\n\n```sql\n")
                        out.write('SELECT SUM(CASE WHEN "{col}" < {low} OR "{col}" > {high} THEN 1 ELSE 0 END)::bigint AS outliers\n'
                                  f'FROM "{SCHEMA}"."{table}";\n')
                        out.write("```\n\n")
                    else:
                        out.write("_No numeric columns considered._\n\n")

                    # ---------- Categorical summary + top-k ----------
                    categorical_time = 0.0
                    cat_summary_rows: List[List[Any]] = []
                    cat_sql_blocks: List[str] = []
                    if cat_cols:
                        out.write("### Categorical columns\n\n")

                        # summary table
                        head = ["column","non_null","nulls","nulls_%","distinct"]
                        for col, _udt in cat_cols:
                            qsum = categorical_summary_sql(SCHEMA, table, col)
                            t0 = time.perf_counter()
                            rsum = pd.read_sql_query(text(qsum), engine).iloc[0]
                            dt = time.perf_counter() - t0
                            categorical_time += dt

                            non_null = int(rsum["non_null"])
                            nulls    = int(rsum["nulls"])
                            total    = non_null + nulls
                            nulls_pct = (nulls / total * 100.0) if total > 0 else 0.0

                            cat_summary_rows.append([col, non_null, nulls, round(nulls_pct, 4), int(rsum["distinct"])])
                            cat_sql_blocks.append(qsum.strip() + f"\n-- time: {dt:.6f}s")

                        out.write(markdown_table(head, cat_summary_rows) + "\n")

                        # top-5 values per categorical column (skip if all distinct)
                        for col, _udt in cat_cols:
                            qtop = categorical_topk_sql(SCHEMA, table, col, k=5)
                            t0 = time.perf_counter()
                            df_top = pd.read_sql_query(text(qtop), engine)
                            dt = time.perf_counter() - t0
                            categorical_time += dt

                            # If every non-null value is unique, max count will be 1
                            if not df_top.empty and int(df_top["cnt"].max()) == 1:
                                out.write(f"**Top-5 values for `{col}`** — _All non-null values are distinct; omitting list._\n\n")
                            else:
                                out.write(f"**Top-5 values for `{col}`**\n\n")
                                if df_top.empty:
                                    out.write("_No values (all NULL or empty table)._ \n\n")
                                else:
                                    df_top["value"] = df_top["value"].map(lambda x: _trim_cell(x))
                                    df_top["cnt"] = df_top["cnt"].map(lambda x: _format_number(x))
                                    out.write(df_top.to_markdown(index=False) + "\n\n")
                                out.write("**SQL (top-k)**\n\n```sql\n" + qtop.strip() + f"\n-- time: {dt:.6f}s\n```\n\n")

                        # include the summary SQLs
                        out.write("**SQL (categorical summaries)**\n\n```sql\n")
                        out.write("\n\n".join(cat_sql_blocks) + "\n```\n\n")
                    else:
                        out.write("_No categorical columns considered._\n\n")

                    total_time = time.perf_counter() - table_start

                    # Timings block
                    out.write("### Timings\n\n")
                    trows = [
                        ["split_columns", round(split_time, 6)],
                        ["numeric_aggregates", round(numeric_time, 6)],
                        ["categoricals_total", round(categorical_time, 6)],
                        ["table_total", round(total_time, 6)],
                    ]
                    out.write(markdown_table(["step","time (s)"], trows) + "\n")
                    out.write("---\n\n")

                    processed += 1

                except Exception as ex:
                    out.write(f"⚠️ **Error profiling {SCHEMA}.{table}:** {ex}\n\n")
                    import traceback as _tb
                    out.write("```\n" + "".join(_tb.format_exc()) + "```\n\n---\n\n")
                    continue

        print(f"Wrote: {OUTPUT_STATS.resolve()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
