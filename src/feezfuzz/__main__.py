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

def export_scripts_as_toml(tables):
    (BUILD_PATH / "scripts").mkdir(exist_ok=True)

    npcs = tables[5]
    locale = tables[6]

    for row in npcs.rows:
        script = {
            "uid": row.uid.hex(),
            "name": row.cells[0].item.uid.hex(),
            "Script1": row.cells[1].item.toml(locale),
            "Script2": row.cells[2].item.toml(locale),
            "Script3": row.cells[3].item.toml(locale),
            "Script4": row.cells[4].item.toml(locale),
            "Script5": row.cells[5].item.toml(locale),
        }
        filename = row.cells[-1].item.value.replace('\0', '')
        with open((BUILD_PATH / "scripts" / f"{filename}.toml"), "wb") as f:
            tomli_w.dump(script, f, multiline_strings=True)

def toml_to_fbs():
    locale = Table()
    npcs = Table()

    (BUILD_PATH / "scripts").mkdir(exist_ok=True)
    for filepath in (BUILD_PATH / "scripts").glob("*.toml"):
        with open(filepath, "rb") as f:
            npcs.add(Row.from_script_toml(
                filepath.stem,
                tomli.load(f),
                locale,
            ))
    return npcs, locale

if __name__ == "__main__":
    # DATA_PATH = Path("../Zanzarah/Data/")

    DATA_PATH = Path("../feezfuzz additions/unbended new/")
    BUILD_PATH = Path("./build")
    BUILD_PATH.mkdir(exist_ok=True)

    tables = {}
    for filepath in DATA_PATH.glob("*.fbs"):
        table_id = int(filepath.stem[-1])
        tables[table_id] = read_fbs(filepath)

    for table_id, table in tables.items():
        write_xml(table, BUILD_PATH / f"_fb0x0{table_id}.xml")
        write_fbs(table, BUILD_PATH / f"_fb0x0{table_id}.fbs")

    # for row in tables[6].value:
    #     for cell in row.cells:
    #         if cell.datatype.value == 0:
    #             cell.item.value = cell.item.value.upper()

    export_scripts_as_toml(tables)
    npcs, locale = toml_to_fbs()

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
