#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, text

import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from tqdm import tqdm
import traceback

# ------------------ Config ------------------
DB_NAME = "gis"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5434

SCHEMA = "eleicoes22"
TABLE_LIMIT = 30
COLUMN_LIMIT = 30
SAMPLE_ROWS = 5
MAX_CELL_LEN = 120
NULL_STR = ""  # how to render NULLs in Markdown samples: "" / "NULL" / "—" / "(na)"
OUTPUT_PATH = Path("eleicoes22_introspection.md")
# --------------------------------------------

GEOM_UDT_NAMES = {"geometry", "geography"}  # render as WKT in samples


# ---------- Connections ----------
def get_engine():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)


def connect():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )


# ---------- Catalog helpers ----------
def fetch_tables(cur, schema):
    cur.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """,
        (schema,),
    )
    rows = cur.fetchall() or []
    return [r[0] for r in rows]


def fetch_views(cur, schema):
    cur.execute(
        """
        SELECT table_name
        FROM information_schema.views
        WHERE table_schema = %s
        ORDER BY table_name
        """,
        (schema,),
    )
    rows = cur.fetchall() or []
    return [r[0] for r in rows]


def fetch_matviews(cur, schema):
    cur.execute(
        """
        SELECT matviewname
        FROM pg_matviews
        WHERE schemaname = %s
        ORDER BY matviewname
        """,
        (schema,),
    )
    rows = cur.fetchall() or []
    return [r[0] for r in rows]


def count_columns(cur, schema, relname):
    cur.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        """,
        (schema, relname),
    )
    r = cur.fetchone()
    return int(r[0]) if r else 0


def get_first_n_columns_with_types(cur, schema, relname, n=COLUMN_LIMIT):
    """
    Works for tables, views, and materialized views.
    Returns [(column_name, udt_name)] limited to first N visible columns.
    """
    cur.execute(
        """
        SELECT a.attname AS column_name,
               t.typname AS udt_name
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_attribute a ON a.attrelid = c.oid
        JOIN pg_type t ON t.oid = a.atttypid
        WHERE n.nspname = %s
          AND c.relname = %s
          AND a.attnum > 0
          AND NOT a.attisdropped
        ORDER BY a.attnum
        LIMIT %s
        """,
        (schema, relname, n),
    )
    rows = cur.fetchall() or []
    return [(r[0], r[1]) for r in rows]



def estimate_row_count_pg18(cur, schema, relname):
    # Works for tables & matviews; views don't have rows
    cur.execute(
        """
        SELECT s.n_live_tup
        FROM pg_stat_all_tables s
        JOIN pg_class c ON c.oid = s.relid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = %s AND c.relname = %s
        """,
        (schema, relname),
    )
    r = cur.fetchone()
    if r and r[0] is not None:
        return int(r[0])

    cur.execute(
        """
        SELECT reltuples::bigint
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = %s AND c.relname = %s
        """,
        (schema, relname),
    )
    r = cur.fetchone()
    return int(r[0]) if r and r[0] is not None else None


def get_table_sizes(cur, schema, relname):
    """
    For tables & matviews. Views have no storage.
    Returns (heap_bytes, index_bytes, total_bytes).
    """
    fqn = f"{schema}.{relname}"
    cur.execute(
        """
        SELECT
          pg_table_size(to_regclass(%s))::bigint AS heap,
          pg_indexes_size(to_regclass(%s))::bigint AS indexes,
          pg_total_relation_size(to_regclass(%s))::bigint AS total
        """,
        (fqn, fqn, fqn),
    )
    r = cur.fetchone() or (0, 0, 0)
    heap_b = int(r[0] or 0)
    idx_b = int(r[1] or 0)
    tot_b = int(r[2] or 0)
    return heap_b, idx_b, tot_b


def _human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    v = float(n)
    idx = 0
    while v >= 1024 and idx < len(units) - 1:
        v /= 1024.0
        idx += 1
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return f"{s} {units[idx]}"


# ---------- DDL helpers ----------
def pg_has_tabledef(cur):
    cur.execute(
        """
        SELECT COUNT(*)
        FROM pg_proc
        WHERE proname = 'pg_get_tabledef'
          AND pg_catalog.pg_function_is_visible(oid)
        """
    )
    r = cur.fetchone()
    return bool(r and r[0])


def get_native_tabledef(cur, schema, table):
    cur.execute("SELECT pg_get_tabledef(%s::regclass)", (f"{schema}.{table}",))
    r = cur.fetchone()
    return r[0] if r and r[0] else None


def get_view_definition(cur, schema, view):
    # pretty format = true
    cur.execute("SELECT pg_get_viewdef(%s::regclass, true)", (f"{schema}.{view}",))
    r = cur.fetchone()
    return r[0] if r and r[0] else None


def fetch_columns_for_fallback(cur, schema, table, limit=COLUMN_LIMIT):
    cur.execute(
        """
        SELECT
            c.ordinal_position,
            c.column_name,
            c.data_type,
            c.udt_name,
            c.character_maximum_length,
            c.numeric_precision,
            c.numeric_scale,
            c.datetime_precision,
            c.is_nullable,
            c.column_default
        FROM information_schema.columns c
        WHERE c.table_schema = %s AND c.table_name = %s
        ORDER BY c.ordinal_position
        """,
        (schema, table),
    )
    rows = cur.fetchall() or []
    truncated = False
    if len(rows) > limit:
        rows = rows[:limit]
        truncated = True
    return rows, truncated


def fetch_primary_key_cols(cur, schema, table):
    cur.execute(
        """
        SELECT a.attname
        FROM pg_index i
        JOIN pg_class c ON c.oid = i.indrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
        WHERE n.nspname = %s AND c.relname = %s AND i.indisprimary
        ORDER BY array_position(i.indkey, a.attnum)
        """,
        (schema, table),
    )
    rows = cur.fetchall() or []
    return [r[0] for r in rows]


def render_type(row):
    (_ord, _name, data_type, udt_name, char_len, num_prec, num_scale, dt_prec,
     _nullable, _default) = row

    if data_type in ("character varying", "character"):
        return f"{data_type}({char_len})" if char_len is not None else data_type
    if data_type in ("numeric", "decimal"):
        if num_prec is not None and num_scale is not None:
            return f"{data_type}({num_prec},{num_scale})"
        if num_prec is not None:
            return f"{data_type}({num_prec})"
        return data_type
    if data_type in (
        "timestamp without time zone", "timestamp with time zone",
        "time without time zone", "time with time zone"
    ):
        return f"{data_type}({dt_prec})" if dt_prec is not None else data_type
    if data_type == "ARRAY" and udt_name:
        return udt_name
    if data_type == "USER-DEFINED" and udt_name:
        return udt_name
    return data_type


def build_fallback_tabledef(cur, schema, table, column_limit=COLUMN_LIMIT):
    cols, truncated = fetch_columns_for_fallback(cur, schema, table, column_limit)
    pk_cols = fetch_primary_key_cols(cur, schema, table)

    lines = []
    for row in cols:
        (_ord, name, _data_type, _udt, _cl, _np, _ns, _dp, is_nullable, col_default) = row
        t = render_type(row)
        parts = [sql.Identifier(name).as_string(cur), t]
        if col_default is not None:
            parts.append(f"DEFAULT {col_default}")
        if is_nullable == "NO":
            parts.append("NOT NULL")
        lines.append("  " + " ".join(parts))

    ddl = []
    ddl.append(f"CREATE TABLE {sql.Identifier(schema).as_string(cur)}.{sql.Identifier(table).as_string(cur)} (")
    if lines:
        ddl.append(",\n".join(lines))
    if pk_cols:
        pk = ", ".join(sql.Identifier(c).as_string(cur) for c in pk_cols)
        if lines:
            ddl.append(",\n  PRIMARY KEY (" + pk + ")")
        else:
            ddl.append("  PRIMARY KEY (" + pk + ")")
    ddl.append("\n);")

    if truncated:
        ddl.append(f"\n-- NOTE: Column list truncated to first {column_limit} columns.")
    return "\n".join(ddl)


# ---------- Sample formatting ----------
def _trim_cell(x, max_len=MAX_CELL_LEN):
    if pd.isna(x):
        return NULL_STR
    s = str(x)
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def _format_number(x):
    if pd.isna(x):
        return NULL_STR
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        if np.isfinite(x) and float(x).is_integer():
            return str(int(x))
        return np.format_float_positional(float(x), trim='-')
    return str(x)


def pandas_sample_markdown_sqlalchemy(engine, schema, relname, cols_with_types, n=SAMPLE_ROWS):
    """
    Works for tables, views, matviews.
    Geometry/geography -> ST_AsText; numeric -> no sci notation; text -> trimmed.
    """
    select_parts = []
    for col, udt in cols_with_types:
        if udt in GEOM_UDT_NAMES:
            select_parts.append(f'ST_AsText("{schema}"."{relname}"."{col}") AS "{col}"')
        else:
            select_parts.append(f'"{schema}"."{relname}"."{col}"')
    select_list = ", ".join(select_parts)

    query = text(f'SELECT {select_list} FROM "{schema}"."{relname}" ORDER BY random() LIMIT :n;')
    df = pd.read_sql_query(query, engine, params={"n": n})

    colnames = [c for c, _ in cols_with_types]
    df = df[colnames]

    for c in colnames:
        s = df[c]
        if is_numeric_dtype(s.dtype):
            df[c] = s.map(_format_number)
        else:
            df[c] = s.map(_trim_cell)

    try:
        return df.to_markdown(index=False)
    except Exception:
        headers = "| " + " | ".join(colnames) + " |"
        sep = "| " + " | ".join(["---"] * len(colnames)) + " |"
        rows = ["| " + " | ".join("" if pd.isna(v) else str(v) for v in r.tolist()) + " |"
                for _, r in df.iterrows()]
        return "\n".join([headers, sep] + rows)


# ---------- Output header ----------
def write_header(out, schema, counts):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out.write(f"# Introspection of schema `{schema}`\n\n")
    out.write(f"- Generated at: {ts}\n")
    out.write(f"- Database: {DB_NAME} @ {DB_HOST}:{DB_PORT}\n")
    out.write(f"- Tables found: {counts.get('tables', 0)}\n")
    out.write(f"- Views found: {counts.get('views', 0)}\n")
    out.write(f"- Materialized views found: {counts.get('matviews', 0)}\n")
    if counts.get("tables", 0) > TABLE_LIMIT:
        out.write(f"- Processed first {TABLE_LIMIT} tables\n")
    out.write(f"- Columns per object shown: up to {COLUMN_LIMIT}\n")
    out.write(f"- Sample rows per object: {SAMPLE_ROWS} (random)\n")
    out.write("\n---\n\n")


# ---------- Main ----------
def main():
    try:
        engine = get_engine()
        with connect() as conn, conn.cursor() as cur, OUTPUT_PATH.open("w", encoding="utf-8") as out:
            tables_all = fetch_tables(cur, SCHEMA)
            views_all = fetch_views(cur, SCHEMA)
            matviews_all = fetch_matviews(cur, SCHEMA)

            tables = tables_all[:TABLE_LIMIT]
            write_header(out, SCHEMA, {"tables": len(tables_all), "views": len(views_all), "matviews": len(matviews_all)})

            has_native = pg_has_tabledef(cur)

            # ----- Tables (## then ### per table)
            out.write("## Tables\n\n")
            for table in tqdm(tables, desc="Tables", unit="tbl"):
                try:
                    est = estimate_row_count_pg18(cur, SCHEMA, table)
                    col_count = count_columns(cur, SCHEMA, table)
                    cols_with_types = get_first_n_columns_with_types(cur, SCHEMA, table, COLUMN_LIMIT)
                    first_cols = [c for c, _ in cols_with_types]
                    heap_b, idx_b, tot_b = get_table_sizes(cur, SCHEMA, table)

                    out.write(f"### {SCHEMA}.{table}\n\n")
                    out.write(f"- Estimated rows: {est if est is not None else 'unknown'}\n")
                    out.write(f"- Columns: {col_count} (showing first {len(first_cols)})\n")
                    out.write(f"- Size (heap): {_human_bytes(heap_b)}\n")
                    out.write(f"- Size (indexes): {_human_bytes(idx_b)}\n")
                    out.write(f"- Size (total): {_human_bytes(tot_b)}\n\n")

                    # DDL
                    out.write("```sql\n")
                    ddl = None
                    if has_native and col_count <= COLUMN_LIMIT:
                        try:
                            ddl = get_native_tabledef(cur, SCHEMA, table)
                        except Exception:
                            ddl = None
                    if ddl is None:
                        ddl = build_fallback_tabledef(cur, SCHEMA, table, COLUMN_LIMIT)
                    out.write(ddl.strip() + "\n")
                    out.write("```\n\n")

                    # Samples
                    out.write(f"**Sample ({SAMPLE_ROWS} rows, first {len(first_cols)} columns):**\n\n")
                    md_table = pandas_sample_markdown_sqlalchemy(engine, SCHEMA, table, cols_with_types, SAMPLE_ROWS)
                    out.write(md_table + "\n\n")
                except Exception as ex:
                    out.write(f"⚠️ **Error processing {SCHEMA}.{table}:** {ex}\n\n")
                    out.write("```\n" + "".join(traceback.format_exc()) + "```\n\n")

            out.write("---\n\n")

            # ----- Views
            if views_all:
                out.write("## Views\n\n")
                for view in tqdm(views_all, desc="Views", unit="view"):
                    try:
                        col_count = count_columns(cur, SCHEMA, view)
                        cols_with_types = get_first_n_columns_with_types(cur, SCHEMA, view, COLUMN_LIMIT)
                        first_cols = [c for c, _ in cols_with_types]
                        defn = get_view_definition(cur, SCHEMA, view)

                        out.write(f"### {SCHEMA}.{view}\n\n")
                        out.write(f"- Columns: {col_count} (showing first {len(first_cols)})\n\n")

                        # DDL (view)
                        out.write("```sql\n")
                        if defn:
                            out.write(f"CREATE VIEW {sql.Identifier(SCHEMA).as_string(cur)}.{sql.Identifier(view).as_string(cur)} AS\n{defn};\n")
                        else:
                            out.write("-- view definition not available\n")
                        out.write("```\n\n")

                        # Samples
                        out.write(f"**Sample ({SAMPLE_ROWS} rows, first {len(first_cols)} columns):**\n\n")
                        md_table = pandas_sample_markdown_sqlalchemy(engine, SCHEMA, view, cols_with_types, SAMPLE_ROWS)
                        out.write(md_table + "\n\n")
                    except Exception as ex:
                        out.write(f"⚠️ **Error processing {SCHEMA}.{view}:** {ex}\n\n")
                        out.write("```\n" + "".join(traceback.format_exc()) + "```\n\n")

                out.write("---\n\n")

            # ----- Materialized Views
            if matviews_all:
                out.write("## Materialized Views\n\n")
                for mv in tqdm(matviews_all, desc="MatViews", unit="mv"):
                    try:
                        est = estimate_row_count_pg18(cur, SCHEMA, mv)
                        col_count = count_columns(cur, SCHEMA, mv)
                        cols_with_types = get_first_n_columns_with_types(cur, SCHEMA, mv, COLUMN_LIMIT)
                        first_cols = [c for c, _ in cols_with_types]
                        heap_b, idx_b, tot_b = get_table_sizes(cur, SCHEMA, mv)
                        defn = get_view_definition(cur, SCHEMA, mv)  # viewdef works for matviews too

                        out.write(f"### {SCHEMA}.{mv}\n\n")
                        out.write(f"- Estimated rows: {est if est is not None else 'unknown'}\n")
                        out.write(f"- Columns: {col_count} (showing first {len(first_cols)})\n")
                        out.write(f"- Size (heap): {_human_bytes(heap_b)}\n")
                        out.write(f"- Size (indexes): {_human_bytes(idx_b)}\n")
                        out.write(f"- Size (total): {_human_bytes(tot_b)}\n\n")

                        # DDL (matview)
                        out.write("```sql\n")
                        if defn:
                            out.write(f"CREATE MATERIALIZED VIEW {sql.Identifier(SCHEMA).as_string(cur)}.{sql.Identifier(mv).as_string(cur)} AS\n{defn};\n")
                        else:
                            out.write("-- materialized view definition not available\n")
                        out.write("```\n\n")

                        out.write(f"**Sample ({SAMPLE_ROWS} rows, first {len(first_cols)} columns):**\n\n")
                        if not first_cols:
                            out.write("_No visible columns; skipping sample._\n\n")
                        else:
                            md_table = pandas_sample_markdown_sqlalchemy(engine, SCHEMA, mv, cols_with_types, SAMPLE_ROWS)
                            if md_table.strip() == "" or md_table.count("\n") <= 2:
                                # Probably WITH NO DATA or truly empty result
                                out.write("_No rows (materialized view may need REFRESH MATERIALIZED VIEW)._ \n\n")
                            else:
                                out.write(md_table + "\n\n")
                    except Exception as ex:
                        out.write(f"⚠️ **Error processing {SCHEMA}.{mv}:** {ex}\n\n")
                        out.write("```\n" + "".join(traceback.format_exc()) + "```\n\n")

            # Footer
            out.write("---\n")
        print(f"Wrote: {OUTPUT_PATH.resolve()}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
