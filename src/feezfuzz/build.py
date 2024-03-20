from pathlib import Path
import xml.etree.ElementTree as ET

import tomli
import tomli_w

from .nodes.indextable import IndexTable
from .nodes.table import Table
from .nodes.row import Row
from .nodes.script import Script


def read_fbs(path: Path) -> IndexTable | Table:
        with open(path, "rb") as f:
            if path.stem == "_fb0x00":
                return IndexTable(f)
            return Table.from_fbs(f)


def write_xml(table: IndexTable | Table, path: Path):
    tree = ET.ElementTree(table.xml())
    ET.indent(tree, space = "  ")
    tree.write(path, encoding="utf8")

def write_fbs(table: IndexTable | Table, path: Path):
    with open(path, 'wb') as f:
        f.write(table.fbs())

def export_scripts_as_toml(build_path, tables):

    npcs = tables[5]
    locale = tables[6]

    for row in npcs.rows:
        script = {
            "UID": row.uid.hex(),
            "Name": row.cells[0].item.uid.hex(),
            "TriggerScript": row.cells[1].item.toml(locale),
            "InitScript": row.cells[2].item.toml(locale),
            "UpdateScript": row.cells[3].item.toml(locale),
            "DefeatedScript": row.cells[4].item.toml(locale),
            "VictoriousScript": row.cells[5].item.toml(locale),
        }
        script = {k: v for k, v in script.items() if v}
        filename = row.cells[-1].item.value.replace('\0', '')
        with open(build_path / f"{filename}.toml", "wb") as f:
            tomli_w.dump(script, f, multiline_strings=True)

def toml_to_fbs(build_path):
    locale = Table()
    npcs = Table()

    for filepath in build_path.glob("*.toml"):
        with open(filepath, "rb") as f:
            npcs.add(Row.from_script_toml(
                filepath.stem,
                tomli.load(f),
                locale,
            ))
    return npcs, locale

def build(data_path: Path):
    BUILD_PATH = data_path / "build"
    BUILD_PATH.mkdir(exist_ok=True)
    SCRIPT_PATH = BUILD_PATH / "scripts"
    SCRIPT_PATH.mkdir(exist_ok=True)

    tables = {}
    for filepath in data_path.glob("*.fbs"):
        table_id = int(filepath.stem[-1])
        tables[table_id] = read_fbs(filepath)

    for table_id, table in tables.items():
        write_xml(table, BUILD_PATH / f"_fb0x0{table_id}.xml")
        write_fbs(table, BUILD_PATH / f"_fb0x0{table_id}.fbs")

    # for row in tables[6].value:
    #     for cell in row.cells:
    #         if cell.datatype.value == 0:
    #             cell.item.value = cell.item.value.upper()

    export_scripts_as_toml(SCRIPT_PATH, tables)
    npcs, locale = toml_to_fbs(SCRIPT_PATH)

    write_fbs(npcs, BUILD_PATH / f"_fb0x05.fbs")
    write_xml(npcs, BUILD_PATH / f"_fb0x05.xml")

    write_fbs(locale, BUILD_PATH / f"_fb0x06.fbs")
    write_xml(locale, BUILD_PATH / f"_fb0x06.xml")

    # Test built fbs files:
    table = read_fbs(BUILD_PATH / f"_fb0x05.fbs")
    write_fbs(table, BUILD_PATH / f"_fb0x05.fbs")
    write_xml(table, BUILD_PATH / f"_fb0x05.xml")

    table = read_fbs(BUILD_PATH / f"_fb0x06.fbs")
    write_fbs(table, BUILD_PATH / f"_fb0x06.fbs")
    write_xml(table, BUILD_PATH / f"_fb0x06.xml")
