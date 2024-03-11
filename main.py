from pathlib import Path
import xml.etree.ElementTree as ET

from src.nodes.indextable import IndexTable
from src.nodes.table import Table


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
