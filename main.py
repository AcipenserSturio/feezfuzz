from pathlib import Path
import xml.etree.ElementTree as ET

import tomli_w

from src.db.nodes.indextable import IndexTable
from src.db.nodes.table import Table
from src.script.script import Script


def read_fbs(path: Path) -> IndexTable | Table:
        with open(filepath, "rb") as f:
            if filepath.stem == "_fb0x00":
                return IndexTable(f)
            return Table(f)


def write_xml(table: IndexTable | Table, path: Path):
    tree = ET.ElementTree(table.xml())
    ET.indent(tree, space = "  ")
    tree.write(path, encoding="utf8")

def write_fbs(table: IndexTable | Table, path: Path):
    with open(path, 'wb') as f:
        f.write(table.fbs())

def export_scripts_as_toml(tables):
    (BUILD_PATH / "scripts").mkdir(exist_ok=True)
    for row in tables[5].value:
        script = {
            "uid": row.uid.hex(),
            "name": row.cells[0].item.uid.hex(),
            "Script1": Script(row.cells[1].item.value[:-1], tables[6]).toml(),
            "Script2": Script(row.cells[2].item.value[:-1], tables[6]).toml(),
            "Script3": Script(row.cells[3].item.value[:-1], tables[6]).toml(),
            "Script4": Script(row.cells[4].item.value[:-1], tables[6]).toml(),
            "Script5": Script(row.cells[5].item.value[:-1], tables[6]).toml(),
        }
        filename = row.cells[-1].item.value.replace('\0', '')
        with open((BUILD_PATH / "scripts" / f"{filename}.toml"), "wb") as f:
            tomli_w.dump(script, f, multiline_strings=True)

if __name__ == "__main__":
    # DATA_PATH = Path("../Zanzarah/Data/")

    DATA_PATH = Path("../feezfuzz additions/unbended new/")
    BUILD_PATH = Path("./build")
    BUILD_PATH.mkdir(exist_ok=True)

    tables = {}
    for filepath in DATA_PATH.glob("*.fbs"):
        table_id = int(filepath.stem[-1])
        tables[table_id] = read_fbs(filepath)

    # for row in tables[6].value:
    #     for cell in row.cells:
    #         if cell.datatype.value == 0:
    #             cell.item.value = cell.item.value.upper()

    export_scripts_as_toml(tables)


    for table_id, table in tables.items():
        write_xml(table, BUILD_PATH / f"_fb0x0{table_id}.xml")
        write_fbs(table, BUILD_PATH / f"_fb0x0{table_id}.fbs")
