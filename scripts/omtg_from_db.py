#!/usr/bin/env python3
import sys
import math
import argparse
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET

from tqdm import tqdm

# ---- reuse your helpers / constants from getTables.py (same folder) ----
from getTables import (
    SCHEMA, TABLE_LIMIT, COLUMN_LIMIT, GEOM_UDT_NAMES,
    IGNORE_PREFIX,
    get_engine, connect,
    fetch_tables, fetch_columns_for_fallback, fetch_primary_key_cols
)

# ---------------- Defaults & Config ----------------
OUTPUT_XML = Path("omtg_generated.xml")
IGNORE_TABLES_DEFAULT = set(
    "votacao_partido_munzona_2022_sc",
    "br_ibge_censo_2022_setor_censitario_sc",
    "br_bd_diretorios_brasil_setor_censitario",
    "br_geobr_mapas_limite_vizinhanca"
)
ATTR_COL_CAP = 20
COMPACT_SINGLE_LINE = True

GRID_CELL_W = 380
GRID_COLS   = 5
GRID_START_X = 120
GRID_START_Y = 120

# default auto-height parameters
DEFAULT_BASE_H      = 140   # header ≈ 2.5 rows
DEFAULT_ROW_BLOCK_H = 80    # height per 4 attributes
DEFAULT_ROW_GAP     = 40    # vertical gap between rows
# ---------------------------------------------------

# ------------- Logging (configurable) --------------
class Logger:
    def __init__(self, level: str = "info"):
        self.level_map = {"quiet": 0, "info": 1, "debug": 2}
        self.level = self.level_map.get(level.lower(), 1)

    def debug(self, msg: str):  # noqa
        if self.level >= 2:
            print(msg)

    def info(self, msg: str):  # noqa
        if self.level >= 1:
            print(msg)

    def warn(self, msg: str):  # noqa
        print(msg)

    def error(self, msg: str):  # noqa
        print(msg, file=sys.stderr)

log = Logger("info")
# ---------------------------------------------------

def estimate_cell_height(attr_count: int, base_h: int, row_block_h: int) -> int:
    """
    With 4 attrs: base_h + row_block_h (e.g., 140 + 80 = 220).
    """
    blocks = max(1, math.ceil(max(0, attr_count) / 4))
    return int(base_h + blocks * row_block_h)

def detect_has_geometry(col_rows: List[Tuple]) -> bool:
    for row in col_rows:
        udt = (row[3] or "").lower()
        if udt in GEOM_UDT_NAMES:
            return True
    return False

def map_col_to_omtg_type(row: Tuple) -> str:
    data_type = (row[2] or "").lower()
    udt_name  = (row[3] or "").lower()
    num_scale = row[6]

    if data_type in ("boolean",) or udt_name in ("bool",):
        return "BOOLEAN"
    if data_type in ("date",):
        return "DATE"
    if data_type in ("time without time zone", "time with time zone") or udt_name in ("time", "timetz"):
        return "TIME"
    if data_type in ("smallint", "integer", "bigint") or udt_name in ("int2", "int4", "int8"):
        return "INTEGER"
    if data_type in ("real", "double precision") or udt_name in ("float4", "float8"):
        return "REAL"
    if data_type in ("numeric", "decimal") or udt_name in ("numeric", "decimal"):
        try:
            return "REAL" if (num_scale is not None and int(num_scale) > 0) else "INTEGER"
        except Exception:
            return "REAL"
    if data_type in ("character varying",) or udt_name in ("varchar",):
        return "VARCHAR"
    if data_type in ("character", "text") or udt_name in ("bpchar", "text"):
        return "TEXT"
    return "TEXT"

def build_omtg_xml(
    cur,
    schema: str,
    tables: List[str],
    grid_cols: int,
    cell_w: int,
    start_x: int,
    start_y: int,
    base_h: int,
    row_block_h: int,
    row_gap: int,
) -> ET.ElementTree:
    """
    Columns capped at min(ATTR_COL_CAP, COLUMN_LIMIT).
    Auto-height: next row starts at previous row's max cell bottom + row_gap.
    """
    log.info(f"[build] Creating XML for schema '{schema}' with {len(tables)} tables…")
    root = ET.Element("omtg-conceptual-schema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "omtg-schema-template.xsd")

    classes_el = ET.SubElement(root, "classes")
    ET.SubElement(root, "relationships")  # empty

    per_table_cap = min(ATTR_COL_CAP, max(1, COLUMN_LIMIT))
    log.debug(f"[build] Attribute cap: first {per_table_cap} columns (min of {ATTR_COL_CAP} and COLUMN_LIMIT={COLUMN_LIMIT})")
    log.debug(f"[layout] cols={grid_cols}, cell_w={cell_w}, origin=({start_x},{start_y}); base_h={base_h}, row_block_h={row_block_h}, row_gap={row_gap}")

    current_y = start_y
    row_max_h = 0
    col_idx_in_row = 0

    for idx, tbl in enumerate(tqdm(tables, desc="Emit classes", unit="cls"), start=1):
        log.debug(f"[table] {schema}.{tbl}")

        col_rows, _ = fetch_columns_for_fallback(cur, schema, tbl, limit=10_000)
        total_cols = len(col_rows)
        if total_cols > per_table_cap:
            log.debug(f"  -> {total_cols} columns; capping to first {per_table_cap}")
            col_rows = col_rows[:per_table_cap]
        else:
            log.debug(f"  -> {total_cols} columns; no cap")

        has_geom = detect_has_geometry(col_rows)
        ctype = "polygon" if has_geom else "conventional"
        pk_set = set(fetch_primary_key_cols(cur, schema, tbl))
        log.debug(f"  -> geometry={has_geom} => type={ctype}; PKs={list(pk_set) if pk_set else 'none'}")

        this_h = estimate_cell_height(len(col_rows), base_h, row_block_h)
        row_max_h = max(row_max_h, this_h)

        c = col_idx_in_row
        left = start_x + c * cell_w
        top  = current_y

        class_el = ET.SubElement(classes_el, "class")
        ET.SubElement(class_el, "name").text = tbl
        ET.SubElement(class_el, "top").text = str(top)
        ET.SubElement(class_el, "left").text = str(left)
        ET.SubElement(class_el, "type").text = ctype

        attrs_el = ET.SubElement(class_el, "attributes")
        for row in col_rows:
            colname = row[1]
            attr_el = ET.SubElement(attrs_el, "attribute")
            ET.SubElement(attr_el, "name").text = colname
            ET.SubElement(attr_el, "type").text = map_col_to_omtg_type(row)
            if colname in pk_set:
                ET.SubElement(attr_el, "key").text = "true"

        log.debug(f"  -> placed at (left={left}, top={top}), height≈{this_h}, emitted {len(col_rows)} of {total_cols}")

        col_idx_in_row += 1
        if col_idx_in_row >= grid_cols or idx == len(tables):
            current_y += row_max_h + row_gap
            row_max_h = 0
            col_idx_in_row = 0

    log.info("[build] XML tree completed")
    return ET.ElementTree(root)

def parse_ignore_list(arg_val: str) -> set:
    if not arg_val:
        return set()
    return {x.strip() for x in arg_val.split(",") if x.strip()}

def main():
    global log
    parser = argparse.ArgumentParser(description="Generate OMT-G XML from DB catalog (tables only).")
    parser.add_argument("--ignore", type=str, default="", help="Comma-separated list of table names to ignore (in addition to IGNORE_PREFIX)")
    parser.add_argument("--out", type=str, default=str(OUTPUT_XML), help="Output XML path")
    parser.add_argument("--cols", type=int, default=GRID_COLS, help="Grid columns")
    parser.add_argument("--cellw", type=int, default=GRID_CELL_W, help="Grid cell width")
    parser.add_argument("--startx", type=int, default=GRID_START_X, help="Grid origin X")
    parser.add_argument("--starty", type=int, default=GRID_START_Y, help="Grid origin Y")
    parser.add_argument("--baseh", type=int, default=DEFAULT_BASE_H, help="Base header height (px)")
    parser.add_argument("--rowh", type=int, default=DEFAULT_ROW_BLOCK_H, help="Height per 4 attributes (px)")
    parser.add_argument("--rowgap", type=int, default=DEFAULT_ROW_GAP, help="Gap between rows (px)")
    parser.add_argument("--singleline", action="store_true", help="Collapse XML into a single line after write")
    parser.add_argument("--log", type=str, default="info", choices=["quiet","info","debug"], help="Log level")
    args = parser.parse_args()

    log = Logger(args.log)

    out_path = Path(args.out)
    ignore_all = set(IGNORE_TABLES_DEFAULT) | parse_ignore_list(args.ignore)

    try:
        log.info("[init] Connecting to database…")
        _ = get_engine()
        with connect() as conn, conn.cursor() as cur:
            log.info(f"[init] Connected. Reading tables from schema '{SCHEMA}'…")
            all_tables = fetch_tables(cur, SCHEMA)
            log.info(f"[init] Found {len(all_tables)} base tables in '{SCHEMA}'")

            filtered = []
            for t in all_tables:
                if t.startswith(IGNORE_PREFIX):
                    log.debug(f"  [skip] {t} (prefix {IGNORE_PREFIX})")
                    continue
                if t in ignore_all:
                    log.debug(f"  [skip] {t} (in ignore list)")
                    continue
                filtered.append(t)

            if TABLE_LIMIT and TABLE_LIMIT > 0:
                selected = filtered[:TABLE_LIMIT]
                log.info(f"[limit] TABLE_LIMIT={TABLE_LIMIT}: selected {len(selected)} / {len(filtered)} tables")
            else:
                selected = filtered
                log.info(f"[limit] No TABLE_LIMIT cap: selected all {len(selected)} tables")

            log.info(f"[init] Will materialize {len(selected)} tables -> XML")
            tree = build_omtg_xml(
                cur,
                SCHEMA,
                selected,
                grid_cols=args.cols,
                cell_w=args.cellw,
                start_x=args.startx,
                start_y=args.starty,
                base_h=args.baseh,
                row_block_h=args.rowh,
                row_gap=args.rowgap,
            )

        log.info(f"[write] Writing XML to: {out_path}")
        tree.write(out_path, encoding="UTF-8", xml_declaration=True)

        if args.singleline or COMPACT_SINGLE_LINE:
            log.info("[write] Collapsing XML to a single line for importer compatibility")
            content = out_path.read_text(encoding="UTF-8")
            single_line = "".join(line.strip() for line in content.splitlines())
            out_path.write_text(single_line, encoding="UTF-8")

        log.info("[done] XML generated successfully.")
    except Exception as e:
        log.error(f"[error] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
