#!/usr/bin/env python3
import sys
from textwrap import shorten

import psycopg2
from psycopg2 import sql

DB_NAME = "gis"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5434

SCHEMA = "eleicoes22"
SAMPLE_ROWS = 5
MAX_CELL_LEN = 120  # truncate wide cells for display

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
        ORDER BY table_name;
        """,
        (schema,),
    )
    return [r[0] for r in cur.fetchall()]

def fetch_columns(cur, schema, table):
    cur.execute(
        """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (schema, table),
    )
    return cur.fetchall()

def estimate_row_count(cur, schema, table):
    # fast estimate from pg_class; avoids expensive COUNT(*)
    cur.execute(
        """
        SELECT reltuples::bigint AS estimate
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = %s AND c.relname = %s;
        """,
        (schema, table),
    )
    row = cur.fetchone()
    return row[0] if row and row[0] is not None else None

def fetch_sample_rows(cur, schema, table, limit):
    # Use ORDER BY random() for a quick sample; change to ORDER BY 1 for deterministic
    qry = sql.SQL("SELECT * FROM {}.{} ORDER BY random() LIMIT {}").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.Literal(limit),
    )
    cur.execute(qry)
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    return colnames, rows

def print_divider(char="─", width=80):
    print(char * width)

def print_columns(columns):
    print("Columns:")
    print("  " + f"{'name':<34} {'type':<22} {'nullable'}")
    for name, dtype, nullable in columns:
        print(f"  {name:<34} {dtype:<22} {nullable}")

def print_rows(colnames, rows):
    if not rows:
        print("  (no rows)")
        return
    # header
    print("Sample rows:")
    print("  " + " | ".join(colnames))
    print("  " + "-" * (sum(len(c) for c in colnames) + 3 * (len(colnames)-1)))
    # data
    for r in rows:
        cells = [shorten(str(v), width=MAX_CELL_LEN, placeholder="…") if v is not None else "NULL" for v in r]
        print("  " + " | ".join(cells))

def main():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                print_divider()
                print(f"Schemas scanned: {SCHEMA}")
                print_divider()

                tables = fetch_tables(cur, SCHEMA)
                if not tables:
                    print(f"No tables found in schema '{SCHEMA}'.")
                    return

                for i, table in enumerate(tables, 1):
                    print(f"[{i}/{len(tables)}] {SCHEMA}.{table}")
                    print_divider("·", 80)

                    columns = fetch_columns(cur, SCHEMA, table)
                    print_columns(columns)

                    est = estimate_row_count(cur, SCHEMA, table)
                    print(f"\nEstimated row count: {est if est is not None else 'unknown'}\n")

                    colnames, rows = fetch_sample_rows(cur, SCHEMA, table, SAMPLE_ROWS)
                    print_rows(colnames, rows)
                    print_divider()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
