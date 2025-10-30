#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET

from tqdm import tqdm

# ---- reuse your helpers / constants from getTables.py (same folder) ----
from getTables import (
    SCHEMA, TABLE_LIMIT, COLUMN_LIMIT, GEOM_UDT_NAMES,
    IGNORE_PREFIX,                # e.g., "ignore_"
    get_engine, connect,
    fetch_tables, fetch_columns_for_fallback, fetch_primary_key_cols
)

# ---------------- Defaults & Config ----------------
OUTPUT_XML = Path("omtg_generated.xml")

# Explicit “by name” ignore list (in addition to IGNORE_PREFIX).
# You can still pass more via CLI: --ignore t1,t2,t3
IGNORE_TABLES_DEFAULT = set()

# Hard cap for attributes in OMT-G (first N columns only).
# We use the stricter between this cap and your COLUMN_LIMIT.
ATTR_COL_CAP = 20

# Optional: some importers only accept a single-line XML (off by default).
COMPACT_SINGLE_LINE = True

# Rough auto layout — **spaced out** by default
GRID_CELL_W = 380
GRID_CELL_H = 220
GRID_COLS   = 3
GRID_START_X = 120
GRID_START_Y = 120
# ---------------------------------------------------


def autolayout(idx: int, cols: int, cell_w: int, cell_h: int, start_x: int, start_y: int) -> tuple[int, int]:
    r = idx // cols
    c = idx % cols
    top  = start_y + r * cell_h
    left = start_x + c * cell_w
    return top, left


def detect_has_geometry(col_rows: List[Tuple]) -> bool:
    """
    col_rows come from fetch_columns_for_fallback:
      (ordinal_position, column_name, data_type, udt_name, char_len, num_prec,
       num_scale, dt_prec, is_nullable, col_default)
    """
    for row in col_rows:
        udt = (row[3] or "").lower()
        if udt in GEOM_UDT_NAMES:
            return True
    return False


def map_col_to_omtg_type(row: Tuple) -> str:
    """
    Map to the constrained set:
      BOOLEAN, DATE, INTEGER, REAL, TEXT, TIME, VARCHAR
    Logic:
      - bool -> BOOLEAN
      - date -> DATE
      - time/timetz -> TIME
      - integer types -> INTEGER
      - real/double -> REAL
      - numeric/decimal -> REAL if scale>0 else INTEGER
      - varchar -> VARCHAR
      - text/bpchar -> TEXT
      - fallback -> TEXT
    """
    # row: (ord, name, data_type, udt_name, char_len, num_prec, num_scale, dt_prec, is_nullable, default)
    data_type = (row[2] or "").lower()
    udt_name  = (row[3] or "").lower()
    num_scale = row[6]

    # booleans
    if data_type in ("boolean",) or udt_name in ("bool",):
        return "BOOLEAN"

    # date / time
    if data_type in ("date",):
        return "DATE"
    if data_type in ("time without time zone", "time with time zone") or udt_name in ("time", "timetz"):
        return "TIME"

    # integers
    if data_type in ("smallint", "integer", "bigint") or udt_name in ("int2", "int4", "int8"):
        return "INTEGER"

    # floating-point
    if data_type in ("real", "double precision") or udt_name in ("float4", "float8"):
        return "REAL"

    # numeric/decimal -> use scale to decide integer vs real
    if data_type in ("numeric", "decimal") or udt_name in ("numeric", "decimal"):
        try:
            if num_scale is not None and int(num_scale) > 0:
                return "REAL"
            return "INTEGER"
        except Exception:
            return "REAL"

    # character types
    if data_type in ("character varying",) or udt_name in ("varchar",):
        return "VARCHAR"
    if data_type in ("character", "text") or udt_name in ("bpchar", "text"):
        return "TEXT"

    # everything else -> TEXT
    return "TEXT"


def build_omtg_xml(
    cur,
    schema: str,
    tables: List[str],
    grid_cols: int,
    grid_w: int,
    grid_h: int,
    start_x: int,
    start_y: int,
) -> ET.ElementTree:
    """
    Build the OMT-G XML document like your example, based on DB catalog only.
    Applies per-table column cap = min(ATTR_COL_CAP, COLUMN_LIMIT).
    """
    print(f"[build] Creating XML document for schema '{schema}' with {len(tables)} tables…")
    root = ET.Element("omtg-conceptual-schema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "omtg-schema-template.xsd")

    classes_el = ET.SubElement(root, "classes")
    ET.SubElement(root, "relationships")  # empty for now

    grid_idx = 0
    per_table_cap = min(ATTR_COL_CAP, max(1, COLUMN_LIMIT))
    print(f"[build] Attribute column cap: first {per_table_cap} columns per table (min of ATTR_COL_CAP={ATTR_COL_CAP} and COLUMN_LIMIT={COLUMN_LIMIT})")
    print(f"[layout] cols={grid_cols}, cell=({grid_w}x{grid_h}), origin=({start_x},{start_y})")

    for tbl in tqdm(tables, desc="Emit classes", unit="cls"):
        print(f"  [table] {schema}.{tbl}: fetching columns…")
        # pull all visible columns, then cap locally
        col_rows, _ = fetch_columns_for_fallback(cur, schema, tbl, limit=10_000)
        total_cols = len(col_rows)
        if total_cols > per_table_cap:
            print(f"    -> {total_cols} columns found; capping to first {per_table_cap}")
            col_rows = col_rows[:per_table_cap]
        else:
            print(f"    -> {total_cols} columns found; no cap applied")

        has_geom = detect_has_geometry(col_rows)
        ctype = "polygon" if has_geom else "conventional"
        print(f"    -> geometry present: {has_geom}  => class <type> = {ctype}")

        pk_cols = fetch_primary_key_cols(cur, schema, tbl)
        pk_set = set(pk_cols)
        print(f"    -> primary keys detected: {list(pk_set) if pk_set else 'none'}")

        top, left = autolayout(grid_idx, grid_cols, grid_w, grid_h, start_x, start_y)
        grid_idx += 1
        print(f"    -> placement: top={top}, left={left}")

        # <class> node
        class_el = ET.SubElement(classes_el, "class")
        ET.SubElement(class_el, "name").text = tbl
        ET.SubElement(class_el, "top").text = str(top)
        ET.SubElement(class_el, "left").text = str(left)
        ET.SubElement(class_el, "type").text = ctype

        attrs_el = ET.SubElement(class_el, "attributes")

        # attributes from DB columns (capped)
        last_colname = ''
        for row in col_rows:
            # row = (ord, name, data_type, udt_name, char_len, num_prec, num_scale, dt_prec, is_nullable, default)
            colname = row[1]

            if last_colname == 'id_concentracao_urbana':
                print("\n\n\n\nEncontrei a concentração urbana!!!!\n\n\n")
                print(f"Coluna atual: {colname}, row completo = {row}")

            last_colname = colname

            attr_el = ET.SubElement(attrs_el, "attribute")
            ET.SubElement(attr_el, "name").text = colname
            ET.SubElement(attr_el, "type").text = map_col_to_omtg_type(row)
            if colname in pk_set:
                ET.SubElement(attr_el, "key").text = "true"

        #if total_cols > per_table_cap:
        #    attrs_el.append(ET.Comment(f" NOTE: attributes truncated to first {per_table_cap} of {total_cols} "))

        print(f"    -> attributes emitted: {len(col_rows)} (of {total_cols})")

    print("[build] XML tree completed")
    return ET.ElementTree(root)


def parse_ignore_list(arg_val: str) -> set:
    """
    Parse --ignore 'a,b,c' into a set; handles empty string.
    """
    if not arg_val:
        return set()
    return {x.strip() for x in arg_val.split(",") if x.strip()}


def main():
    parser = argparse.ArgumentParser(description="Generate OMT-G XML from DB catalog (tables only).")
    parser.add_argument("--ignore", type=str, default="", help="Comma-separated list of table names to ignore (in addition to IGNORE_PREFIX)")
    parser.add_argument("--out", type=str, default=str(OUTPUT_XML), help="Output XML path")
    parser.add_argument("--cols", type=int, default=GRID_COLS, help="Grid columns")
    parser.add_argument("--cellw", type=int, default=GRID_CELL_W, help="Grid cell width")
    parser.add_argument("--cellh", type=int, default=GRID_CELL_H, help="Grid cell height")
    parser.add_argument("--startx", type=int, default=GRID_START_X, help="Grid origin X")
    parser.add_argument("--starty", type=int, default=GRID_START_Y, help="Grid origin Y")
    parser.add_argument("--singleline", action="store_true", help="Collapse XML into a single line after write")
    args = parser.parse_args()

    out_path = Path(args.out)
    ignore_cli = parse_ignore_list(args.ignore)
    ignore_all = set(IGNORE_TABLES_DEFAULT) | ignore_cli

    try:
        print("[init] Connecting to database…")
        _ = get_engine()  # keep parity with your helpers (not strictly required here)
        with connect() as conn, conn.cursor() as cur:
            print(f"[init] Connected. Reading tables from schema '{SCHEMA}'…")
            all_tables = fetch_tables(cur, SCHEMA)
            print(f"[init] Found {len(all_tables)} base tables in '{SCHEMA}'")

            # apply ignores
            filtered = []
            for t in all_tables:
                if t.startswith(IGNORE_PREFIX):
                    print(f"  [skip] {t} (prefix {IGNORE_PREFIX})")
                    continue
                if t in ignore_all:
                    print(f"  [skip] {t} (in ignore list)")
                    continue
                filtered.append(t)

            # apply your table limit (0 or None = no cap)
            if TABLE_LIMIT and TABLE_LIMIT > 0:
                selected = filtered[:TABLE_LIMIT]
                print(f"[limit] TABLE_LIMIT={TABLE_LIMIT}: selected {len(selected)} / {len(filtered)} tables")
            else:
                selected = filtered
                print(f"[limit] No TABLE_LIMIT cap: selected all {len(selected)} tables")

            print(f"[init] Will materialize {len(selected)} tables -> XML")
            tree = build_omtg_xml(
                cur,
                SCHEMA,
                selected,
                grid_cols=args.cols,
                grid_w=args.cellw,
                grid_h=args.cellh,
                start_x=args.startx,
                start_y=args.starty,
            )

        # write XML (pretty whitespace off by default)
        print(f"[write] Writing XML to: {out_path}")
        tree.write(out_path, encoding="UTF-8", xml_declaration=True)

        # Optionally collapse to single line (some tools only accept a one-line file)
        if args.singleline or COMPACT_SINGLE_LINE:
            print("[write] Collapsing XML to a single line for importer compatibility")
            content = out_path.read_text(encoding="UTF-8")
            single_line = "".join(line.strip() for line in content.splitlines())
            out_path.write_text(single_line, encoding="UTF-8")

        print("[done] XML generated successfully.")
    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
