#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path

import psycopg2
from psycopg2 import sql

DB_NAME = "gis"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5434

SCHEMA = "eleicoes22"
TABLE_LIMIT = 30        # limit number of tables processed
COLUMN_LIMIT = 30       # limit number of columns shown per table
OUTPUT_PATH = Path("eleicoes22_introspection.md")


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


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
    return [r[0] for r in cur.fetchall()]


def estimate_row_count(cur, schema, table):
    cur.execute(
        """
        SELECT reltuples::bigint AS estimate
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = %s AND c.relname = %s
        """,
        (schema, table),
    )
    row = cur.fetchone()
    return int(row[0]) if row and row[0] is not None else None


def count_columns(cur, schema, table):
    cur.execute(
        """
        SELECT COUNT(*) 
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        """,
        (schema, table),
    )
    return cur.fetchone()[0]


def pg_has_tabledef(cur):
    # Postgres 16+: pg_get_tabledef(regclass)
    cur.execute(
        """
        SELECT COUNT(*) 
        FROM pg_proc 
        WHERE proname = 'pg_get_tabledef'
          AND pg_catalog.pg_function_is_visible(oid)
        """
    )
    return cur.fetchone()[0] > 0


def get_native_tabledef(cur, schema, table):
    # When available, returns full DDL (no column cap)
    cur.execute("SELECT pg_get_tabledef(%s::regclass)", (f"{schema}.{table}",))
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
    rows = cur.fetchall()
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
    return [r[0] for r in cur.fetchall()]


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


def write_header(f, schema, total_tables, limited_tables):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"# Introspection of schema `{schema}`\n\n")
    f.write(f"- Generated at: {ts}\n")
    f.write(f"- Database: {DB_NAME} @ {DB_HOST}:{DB_PORT}\n")
    f.write(f"- Tables found: {total_tables}\n")
    if limited_tables < total_tables:
        f.write(f"- Processed first {limited_tables} tables (limit={TABLE_LIMIT})\n")
    f.write(f"- Columns per table shown: up to {COLUMN_LIMIT}\n")
    f.write("\n---\n\n")


def main():
    try:
        with connect() as conn, conn.cursor() as cur, OUTPUT_PATH.open("w", encoding="utf-8") as out:
            all_tables = fetch_tables(cur, SCHEMA)
            tables = all_tables[:TABLE_LIMIT]
            write_header(out, SCHEMA, total_tables=len(all_tables), limited_tables=len(tables))

            has_native = pg_has_tabledef(cur)

            for idx, table in enumerate(tables, 1):
                est = estimate_row_count(cur, SCHEMA, table)
                col_count = count_columns(cur, SCHEMA, table)

                out.write(f"## {idx}. {SCHEMA}.{table}\n\n")
                out.write(f"- Estimated rows: {est if est is not None else 'unknown'}\n")
                out.write(f"- Columns: {col_count}\n\n")

                out.write("```sql\n")
                ddl = None
                # Use native DDL only if present AND column count fits our cap; otherwise fallback
                if has_native and col_count <= COLUMN_LIMIT:
                    try:
                        ddl = get_native_tabledef(cur, SCHEMA, table)
                    except Exception:
                        ddl = None
                if ddl is None:
                    ddl = build_fallback_tabledef(cur, SCHEMA, table, COLUMN_LIMIT)
                out.write(ddl.strip() + "\n")
                out.write("```\n\n")

        print(f"Wrote: {OUTPUT_PATH.resolve()}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
