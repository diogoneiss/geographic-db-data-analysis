#!/usr/bin/env python3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Any
import re
import pandas as pd
import numpy as np
from sqlalchemy import text
from tqdm import tqdm

# ---- Reuse helpers from your existing script in the same folder ----
from getTables import (  # rename if your file/module name differs
    DB_NAME, DB_HOST, DB_PORT, SCHEMA, TABLE_LIMIT, COLUMN_LIMIT,
    NULL_STR, GEOM_UDT_NAMES,
    IGNORE_PREFIX,
    get_engine, connect,
    fetch_tables,
    get_first_n_columns_with_types,
    _trim_cell, _format_number
)

# ---------- Optional ASCII histograms ----------
try:
    from ascii_graph import Pyasciigraph
    HAVE_ASCII_GRAPH = True
except Exception:
    HAVE_ASCII_GRAPH = False

# ---------- Python md-toc ----------
try:
    from md_toc.api import build_toc
    HAVE_MD_TOC = True
except Exception:
    HAVE_MD_TOC = False

# ---------- Output path ----------
OUTPUT_STATS = Path("eleicoes22_stats.md")

# ---------- Typing sets (aligned with your main script) ----------
NUMERIC_UDT  = {"int2","int4","int8","float4","float8","numeric","money"}
INT_UDT      = {"int2","int4","int8"}  # subset for categorical-numeric heuristic
DATE_UDT     = {"date","timestamp","timestamptz","time","timetz"}
BOOL_UDT     = {"bool"}
TEXTLIKE_UDT = {"text","varchar","bpchar","uuid"}

# ---------- Ignore list (tables) ----------
IGNORE_TABLES = {
    "votacao_partido_munzona_2022_sc",
    "br_ibge_censo_2022_setor_censitario_sc",
    "br_bd_diretorios_brasil_setor_censitario",
    "br_geobr_mapas_limite_vizinhanca"
}

# ---------- Fast iteration toggle ----------
FAST_MODE  = False
FAST_LIMIT = 13

# ---------- Feature toggles ----------
SHOW_SQL      = False
SHOW_HIST     = True
MAX_HIST_COLS = 10
HIST_BINS     = 10  # number of bins for both equal-frequency and fixed-width

# Treat ints with low cardinality as categorical
NUMERIC_CAT_MAX_DISTINCT = 20
NUMERIC_CAT_MAX_RATIO    = 0.01

# ---------- Helpers ----------
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

def numeric_histogram_sql(schema: str, table: str, col: str, bins: int = HIST_BINS) -> str:
    """Fixed-width histogram using width_bucket. Handles min==max."""
    fqn = f'"{schema}"."{table}"'
    return f"""
    WITH stats AS (
      SELECT MIN("{col}") AS minv, MAX("{col}") AS maxv, COUNT("{col}") AS nn
      FROM {fqn}
      WHERE "{col}" IS NOT NULL
    ),
    hist AS (
      SELECT
        CASE
          WHEN s.maxv = s.minv OR s.nn = 0 THEN 1
          ELSE width_bucket("{col}", s.minv, s.maxv, {bins})
        END AS b,
        COUNT(*)::bigint AS cnt
      FROM {fqn} t
      CROSS JOIN stats s
      WHERE "{col}" IS NOT NULL
      GROUP BY 1
    )
    SELECT b, cnt, (SELECT minv FROM stats) AS minv, (SELECT maxv FROM stats) AS maxv
    FROM hist
    ORDER BY b;
    """

def numeric_histogram_equalfreq_sql(schema: str, table: str, col: str, bins: int = HIST_BINS) -> str:
    """Equal-frequency (≈ same #rows per bin) via NTILE."""
    fqn = f'"{schema}"."{table}"'
    return f"""
    WITH base AS (
      SELECT "{col}" AS v
      FROM {fqn}
      WHERE "{col}" IS NOT NULL
    ),
    ranked AS (
      SELECT NTILE({bins}) OVER (ORDER BY v) AS b, v
      FROM base
    )
    SELECT b,
           COUNT(*)::bigint AS cnt,
           MIN(v) AS lo,
           MAX(v) AS hi
    FROM ranked
    GROUP BY b
    ORDER BY b;
    """

def numeric_topk_values_sql(schema: str, table: str, col: str, k: int = 10) -> str:
    """Value frequency list for numeric-as-categorical hist (no buckets)."""
    fqn = f'"{schema}"."{table}"'
    return (
        f'SELECT "{col}" AS value, COUNT(*)::bigint AS cnt '
        f'FROM {fqn} '
        f'GROUP BY 1 '
        f'ORDER BY cnt DESC NULLS LAST, value ASC '
        f'LIMIT {int(k)};'
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
    out.write(f"- SHOW_SQL: {SHOW_SQL}\n")
    out.write(f"- SHOW_HIST: {SHOW_HIST} (bins={HIST_BINS}, max columns={MAX_HIST_COLS})\n")
    out.write(f"- Numeric low-cardinality heuristic: distinct ≤ {NUMERIC_CAT_MAX_DISTINCT} "
              f"or distinct/non_null ≤ {NUMERIC_CAT_MAX_RATIO:.2%}\n\n")
    # md-toc markers
    out.write("## Table of Contents\n\n")
    out.write("<!-- toc -->\n")
    out.write("<!-- tocstop -->\n\n")
    out.write("---\n\n")

def inject_toc(md_path: Path):
    raw = md_path.read_text(encoding="utf-8")
    if "<!-- toc -->" not in raw or "<!-- tocstop -->" not in raw:
        return
    toc = build_toc(
        str(md_path),
        ordered=False,
        no_links=False,
        no_indentation=False,
        no_list_coherence=False,
        keep_header_levels=6,
        parser="github",
        list_marker="-",
        skip_lines=0,
        constant_ordered_list=False,
        newline_string="\n",
    )
    pattern = r"(<!-- toc -->)(.*?)(<!-- tocstop -->)"
    repl = r"\1\n" + toc.strip() + r"\n\3"
    updated = re.sub(pattern, repl, raw, flags=re.DOTALL)
    md_path.write_text(updated, encoding="utf-8")

# ---------- Main CLI ----------
def main():
    try:
        engine = get_engine()
        with connect() as conn, conn.cursor() as cur, OUTPUT_STATS.open("w", encoding="utf-8") as out:
            database_tables = fetch_tables(cur, SCHEMA)
            all_tables = [t for t in database_tables if t not in IGNORE_TABLES and not t.startswith(IGNORE_PREFIX)]
            tables = all_tables[:TABLE_LIMIT]

            ignored_tables = sorted(set(database_tables) - set(tables))
            write_stats_header(out, SCHEMA, len(all_tables), ignored_tables)

            processed = 0
            for idx, table in enumerate(tqdm(tables, desc="Stats", unit="tbl"), start=1):
                if FAST_MODE and processed >= FAST_LIMIT:
                    break
                table_start = time.perf_counter()
                try:
                    # Heading WITHOUT schema
                    out.write(f"## {idx}. {table}\n\n")

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
                    agg_row: Dict[str, Any] = {}
                    if num_cols:
                        agg_sql = numeric_stats_sql(SCHEMA, table, num_cols)
                        numeric_sql_rendered = agg_sql

                        t0 = time.perf_counter()
                        df_agg = pd.read_sql_query(text(agg_sql), engine)
                        numeric_time = time.perf_counter() - t0

                        agg_row = df_agg.iloc[0].to_dict()
                        headers = ["column","non_null","nulls","nulls_%","distinct","mean","stddev","min","p25","median","p75","max"]
                        rows = []
                        outliers_time_total = 0.0

                        outlier_headers = ["column", "low", "high", "outliers", "time (s)"]
                        for col, udt in num_cols:
                            non_null = int(agg_row.get(f"{col}__non_null") or 0)
                            nulls    = int(agg_row.get(f"{col}__nulls") or 0)
                            total    = non_null + nulls
                            nulls_pct = (nulls / total * 100.0) if total > 0 else 0.0

                            distinct = agg_row.get(f"{col}__distinct")
                            mean     = agg_row.get(f"{col}__mean")
                            stddev   = agg_row.get(f"{col}__stddev")
                            vmin     = agg_row.get(f"{col}__min")
                            p25      = agg_row.get(f"{col}__p25")
                            med      = agg_row.get(f"{col}__median")
                            p75      = agg_row.get(f"{col}__p75")
                            vmax     = agg_row.get(f"{col}__max")

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
                        if SHOW_SQL:
                            out.write("**SQL (numeric aggregate)**\n\n```sql\n")
                            out.write(numeric_sql_rendered.strip() + "\n```\n\n")
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
                            if SHOW_SQL:
                                cat_sql_blocks.append(qsum.strip() + f"\n-- time: {dt:.6f}s")

                        out.write(markdown_table(head, cat_summary_rows) + "\n")

                        for col, _udt in cat_cols:
                            qtop = categorical_topk_sql(SCHEMA, table, col, k=5)
                            t0 = time.perf_counter()
                            df_top = pd.read_sql_query(text(qtop), engine)
                            dt = time.perf_counter() - t0
                            categorical_time += dt

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
                                if SHOW_SQL:
                                    out.write("**SQL (top-k)**\n\n```sql\n" + qtop.strip() + f"\n-- time: {dt:.6f}s\n```\n\n")

                        if SHOW_SQL and cat_sql_blocks:
                            out.write("**SQL (categorical summaries)**\n\n```sql\n")
                            out.write("\n\n".join(cat_sql_blocks) + "\n```\n\n")
                    else:
                        out.write("_No categorical columns considered._\n\n")

                    # ---------- Histograms (show BOTH styles) ----------
                    hist_time_total = 0.0
                    if SHOW_HIST and num_cols:
                        # choose up to MAX_HIST_COLS numeric columns (largest non-null counts)
                        ranked = []
                        for col, _ in num_cols:
                            non_null = int(agg_row.get(f"{col}__non_null") or 0)
                            ranked.append((non_null, col))
                        ranked.sort(reverse=True)
                        chosen_cols = [c for _, c in ranked[:MAX_HIST_COLS]]

                        out.write("### Histograms\n\n")

                        # 1) Equal-frequency (no ascii-graph; Markdown table)
                        out.write("#### Equal-frequency bins (NTILE)\n\n")
                        for col, udt in [nc for nc in num_cols if nc[0] in chosen_cols]:
                            qh_eq = numeric_histogram_equalfreq_sql(SCHEMA, table, col, bins=HIST_BINS)
                            t0 = time.perf_counter()
                            df_h_eq = pd.read_sql_query(text(qh_eq), engine)
                            dt = time.perf_counter() - t0
                            hist_time_total += dt

                            if df_h_eq.empty:
                                out.write(f"**{col}**: _no data to plot_\n\n")
                                continue

                            # Build rows regardless of cardinality; bins will collapse if few distincts
                            rows_eq = []
                            for _, r in df_h_eq.iterrows():
                                b   = int(r["b"])
                                lo  = r["lo"]; hi = r["hi"]
                                cnt = int(r["cnt"])
                                rows_eq.append([
                                    b,
                                    _format_number(lo) if pd.notna(lo) else "",
                                    _format_number(hi) if pd.notna(hi) else "",
                                    cnt
                                ])

                            out.write(f"**{col}** (bins={HIST_BINS}, time {dt:.6f}s)\n\n")
                            out.write(markdown_table(["bin","lo","hi","count"], rows_eq) + "\n")

                            if SHOW_SQL:
                                out.write("**SQL (equal-frequency)**\n\n```sql\n" + qh_eq.strip() + f"\n-- time: {dt:.6f}s\n```\n\n")

                        # 2) Fixed-width with ascii-graph
                        out.write("#### Fixed-width bins (width_bucket)\n\n")
                        for col, udt in [nc for nc in num_cols if nc[0] in chosen_cols]:
                            non_null = int(agg_row.get(f"{col}__non_null") or 0)
                            distinct = int(agg_row.get(f"{col}__distinct") or 0)

                            # Skip categorical-like ints/bools here; they’ll be shown as value counts (bars) below
                            treat_as_cat = (
                                udt in BOOL_UDT or
                                (udt in INT_UDT and non_null > 0 and (
                                    distinct <= NUMERIC_CAT_MAX_DISTINCT or
                                    (distinct / max(1, non_null)) <= NUMERIC_CAT_MAX_RATIO
                                ))
                            )
                            if treat_as_cat:
                                continue

                            qh = numeric_histogram_sql(SCHEMA, table, col, bins=HIST_BINS)
                            t0 = time.perf_counter()
                            df_h = pd.read_sql_query(text(qh), engine)
                            dt = time.perf_counter() - t0
                            hist_time_total += dt

                            if df_h.empty or df_h["minv"].isna().all() or df_h["maxv"].isna().all():
                                out.write(f"**{col}**: _no data to plot_\n\n")
                                continue

                            minv = float(df_h["minv"].iloc[0])
                            maxv = float(df_h["maxv"].iloc[0])
                            if not np.isfinite(minv) or not np.isfinite(maxv):
                                out.write(f"**{col}**: _unsupported range_\n\n")
                                continue

                            data = []
                            bins_present = df_h["b"].tolist()
                            counts = df_h["cnt"].tolist()
                            if maxv == minv:
                                edges = [(minv, maxv)]
                            else:
                                width = (maxv - minv) / HIST_BINS
                                edges = [(minv + (i-1)*width, minv + i*width) for i in range(1, HIST_BINS+1)]
                            for b, cnt in zip(bins_present, counts):
                                idx = int(b) - 1
                                if 0 <= idx < len(edges):
                                    lo, hi = edges[idx]
                                    label = f"[{np.format_float_positional(lo, trim='-')},{np.format_float_positional(hi, trim='-')})"
                                    data.append((label, int(cnt)))

                            if not data:
                                out.write(f"**{col}**: _no bins_\n\n")
                                continue

                            if not HAVE_ASCII_GRAPH:
                                out.write("_Install `ascii-graph` to render fixed-width bars: `pip install ascii-graph`._\n\n")
                                # Fallback: print as table
                                fw_rows = [[lab, c] for (lab, c) in data]
                                out.write(markdown_table(["range","count"], fw_rows) + "\n")
                            else:
                                graph = Pyasciigraph(titlebar='', separator_length=4, human_readable='si', float_format='{:,.2f}')
                                out.write(f"**{col}** (bins={HIST_BINS}, time {dt:.6f}s)\n\n")
                                lines = graph.graph('', data)
                                out.write("```\n" + "\n".join(lines) + "\n```\n\n")
                                if SHOW_SQL:
                                    out.write("**SQL (histogram fixed-width)**\n\n```sql\n" + qh.strip() + f"\n-- time: {dt:.6f}s\n```\n\n")

                        # 3) Categorical-like numeric (bool / low-cardinality ints): value-count bars
                        clike = [(c,u) for (c,u) in num_cols if c in chosen_cols]
                        any_clike = False
                        for col, udt in clike:
                            non_null = int(agg_row.get(f"{col}__non_null") or 0)
                            distinct = int(agg_row.get(f"{col}__distinct") or 0)
                            treat_as_cat = (
                                udt in BOOL_UDT or
                                (udt in INT_UDT and non_null > 0 and (
                                    distinct <= NUMERIC_CAT_MAX_DISTINCT or
                                    (distinct / max(1, non_null)) <= NUMERIC_CAT_MAX_RATIO
                                ))
                            )
                            if not treat_as_cat:
                                continue
                            any_clike = True
                            qv = numeric_topk_values_sql(SCHEMA, table, col, k=10)
                            t0 = time.perf_counter()
                            df_v = pd.read_sql_query(text(qv), engine)
                            dt = time.perf_counter() - t0
                            hist_time_total += dt

                            if df_v.empty:
                                out.write(f"**{col}** (categorical-like): _no values_\n\n")
                                continue

                            data = [(_trim_cell(r["value"]), int(r["cnt"])) for _, r in df_v.iterrows()]
                            if HAVE_ASCII_GRAPH:
                                graph = Pyasciigraph(titlebar='', separator_length=4, human_readable='si', float_format='{:,.2f}')
                                out.write(f"**{col}** (categorical-like, top-10) — time {dt:.6f}s\n\n")
                                lines = graph.graph('', data)
                                out.write("```\n" + "\n".join(lines) + "\n```\n\n")
                            else:
                                out.write(f"**{col}** (categorical-like, top-10) — time {dt:.6f}s\n\n")
                                out.write(markdown_table(["value","count"], [[lab, cnt] for (lab, cnt) in data]) + "\n")
                            if SHOW_SQL:
                                out.write("**SQL (value counts, top-10)**\n\n```sql\n" + qv.strip() + f"\n-- time: {dt:.6f}s\n```\n\n")
                        if any_clike:
                            out.write("\n")

                    total_time = time.perf_counter() - table_start

                    # Timings block
                    out.write("`Execution timings`\n\n")
                    trows = [
                        ["split_columns", round(split_time, 6)],
                        ["numeric_aggregates", round(numeric_time, 6)],
                        ["categoricals_total", round(categorical_time, 6)],
                        ["histograms_total", round(hist_time_total, 6)],
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

        # Build TOC in-place with Python md-toc
        if HAVE_MD_TOC:
            inject_toc(OUTPUT_STATS)
        else:
            print("md-toc not installed; run `pip install md-toc` to populate the TOC block.", file=sys.stderr)

        print(f"Wrote: {OUTPUT_STATS.resolve()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
