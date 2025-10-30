#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import xml.etree.ElementTree as ET

from tqdm import tqdm

# ---- reuse your helpers / constants from getTables.py (same folder) ----
from getTables import (
    SCHEMA, COLUMN_LIMIT, GEOM_UDT_NAMES,
    IGNORE_PREFIX,                # e.g., "ignore_"
    get_engine, connect,
    fetch_tables, fetch_columns_for_fallback, fetch_primary_key_cols
)

# ---------------- Config ----------------
OUTPUT_XML = Path("omtg_generated.xml")

# Explicit “by name” ignore list (in addition to IGNORE_PREFIX)
IGNORE_TABLES = {
    # "some_table_to_skip",
}

# Rough auto layout when you don’t care about exact positions
GRID_CELL_W = 260
GRID_CELL_H = 160
GRID_COLS   = 4
GRID_START_X = 200
GRID_START_Y = 160
# ----------------------------------------


def autolayout(idx: int) -> Tuple[int, int]:
    r = idx // GRID_COLS
    c = idx % GRID_COLS
    top  = GRID_START_Y + r * GRID_CELL_H
    left = GRID_START_X + c * GRID_CELL_W
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


def map_col_to_omtg_type(data_type: str, udt_name: str) -> str:
    """
    Minimal attribute typing for the XML body (the example uses TEXT/INTEGER).
    We keep it simple: GEOMETRY -> 'GEOMETRY', numeric -> 'INTEGER'/'NUMERIC',
    boolean -> 'BOOLEAN', else 'TEXT'.
    """
    dt = (data_type or "").lower()
    udt = (udt_name or "").lower()

    if udt in GEOM_UDT_NAMES:
        return "GEOMETRY"
    if dt in ("smallint", "integer", "bigint"):
        return "INTEGER"
    if dt in ("numeric", "decimal", "real", "double precision", "money"):
        return "NUMERIC"
    if dt in ("boolean",):
        return "BOOLEAN"
    return "TEXT"


def build_omtg_xml(cur, schema: str, tables: List[str]) -> ET.ElementTree:
    """
    Build the OMT-G XML document like your example, based on DB catalog only.
    """
    print(f"[build] Creating XML document for schema '{schema}' with {len(tables)} tables…")
    root = ET.Element("omtg-conceptual-schema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "omtg-schema-template.xsd")

    classes_el = ET.SubElement(root, "classes")
    relationships_el = ET.SubElement(root, "relationships")  # left empty on purpose

    grid_idx = 0

    for tbl in tqdm(tables, desc="Emit classes", unit="cls"):
        print(f"  [table] {schema}.{tbl}: fetching columns…")
        col_rows, _ = fetch_columns_for_fallback(cur, schema, tbl, limit=10_000)  # take all cols
        print(f"    -> {len(col_rows)} columns found")

        has_geom = detect_has_geometry(col_rows)
        ctype = "polygon" if has_geom else "conventional"
        print(f"    -> geometry present: {has_geom}  => class <type> = {ctype}")

        pk_cols = fetch_primary_key_cols(cur, schema, tbl)
        pk_set = set(pk_cols)
        print(f"    -> primary keys detected: {list(pk_set) if pk_set else 'none'}")

        top, left = autolayout(grid_idx)
        grid_idx += 1
        print(f"    -> placement: top={top}, left={left}")

        # <class> node
        class_el = ET.SubElement(classes_el, "class")
        ET.SubElement(class_el, "name").text = tbl
        ET.SubElement(class_el, "top").text = str(top)
        ET.SubElement(class_el, "left").text = str(left)
        ET.SubElement(class_el, "type").text = ctype

        attrs_el = ET.SubElement(class_el, "attributes")

        # attributes from DB columns
        for row in col_rows:
            # row = (ord, name, data_type, udt_name, char_len, num_prec, num_scale, dt_prec, is_nullable, default)
            colname   = row[1]
            data_type = row[2]
            udt_name  = row[3]

            attr_el = ET.SubElement(attrs_el, "attribute")
            ET.SubElement(attr_el, "name").text = colname
            ET.SubElement(attr_el, "type").text = map_col_to_omtg_type(data_type, udt_name)
            if colname in pk_set:
                ET.SubElement(attr_el, "key").text = "true"

        print(f"    -> attributes emitted: {len(col_rows)}")
        # done one class

    print("[build] XML tree completed")
    return ET.ElementTree(root)


def main():
    try:
        print("[init] Connecting to database…")
        engine = get_engine()  # not strictly needed; keeps parity w/ your helpers
        with connect() as conn, conn.cursor() as cur:
            print(f"[init] Connected. Reading tables from schema '{SCHEMA}'…")
            all_tables = fetch_tables(cur, SCHEMA)
            print(f"[init] Found {len(all_tables)} base tables in '{SCHEMA}'")

            # apply ignores
            selected = []
            limit = 3
            count = 0
            for t in all_tables:
                if limit and count >= limit:
                    print(f"  [stop] reached limit of {limit} tables for demo purposes")
                    break
                if t.startswith(IGNORE_PREFIX):
                    print(f"  [skip] {t} (prefix {IGNORE_PREFIX})")
                    continue
                if t in IGNORE_TABLES:
                    print(f"  [skip] {t} (listed in IGNORE_TABLES)")
                    continue
                selected.append(t)
                count += 1

            print(f"[init] Will materialize {len(selected)} tables -> XML")
            tree = build_omtg_xml(cur, SCHEMA, selected)

        # pretty print
        print(f"[write] Writing XML to: {OUTPUT_XML}")
        # ElementTree doesn't pretty-print by default; do a minimal indent:
        pretty_print = False
        if pretty_print:
            try:
                ET.indent(tree, space="  ")  # Python 3.9+
            except Exception:
                pass
        tree.write(OUTPUT_XML, encoding="UTF-8", xml_declaration=True)
        print("[done] XML generated successfully.")

    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
