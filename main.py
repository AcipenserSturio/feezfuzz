from pathlib import Path
import xml.etree.ElementTree as ET

from src.nodes.indextable import IndexTable
from src.nodes.table import Table


if __name__ == "__main__":
    # DATA_PATH = Path("../Zanzarah/Data/")

    DATA_PATH = Path("../feezfuzz additions/unbended new/")
    BUILD_PATH = Path("./build")
    BUILD_PATH.mkdir(exist_ok=True)

    for filepath in DATA_PATH.glob("*.fbs"):
        with open(filepath, "rb") as f:
            if filepath.stem == "_fb0x00":
                tree = ET.ElementTree(IndexTable(f).xml())
            else:
                tree = ET.ElementTree(Table(f).xml())
            ET.indent(tree, space = "  ")
            tree.write(BUILD_PATH / (filepath.stem + ".xml"), encoding="utf8")
