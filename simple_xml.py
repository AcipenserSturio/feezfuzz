from pathlib import Path
import struct
import json
import xml.etree.ElementTree as ET

class Byte:
    def __init__(self, f):
        self.value = struct.unpack("<B", f.read(1))[0]

    def xml(self):
        element = ET.Element("Byte")
        element.text = f"{self.value}"
        return element


class Uint:
    def __init__(self, f):
        self.value = struct.unpack("<I", f.read(4))[0]

    def xml(self):
        element = ET.Element("Uint")
        element.text = f"{self.value}"
        return element


class String:
    def __init__(self, f):
        # pascal-like. the first 4 bytes are string length. not null terminated.
        length = Uint(f).value
        self.value = struct.unpack(f"<{length}s", f.read(length))[0].decode("cp1252")

    def xml(self):
        element = ET.Element("String")
        element.text = f"{self.value}"
        return element


class Column:
    def __init__(self, f):
        self.type = Uint(f)
        self.name = String(f)

    def xml(self):
        element = ET.Element("Column", attrib={"type": f"{self.type.value}"})
        element.append(self.name.xml())
        return element


class Row:
    def __init__(self, f):
        self.uid = Uint(f)
        self.column_data = [ColumnData(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("Column", attrib={"uid": f"{self.uid.value}"})
        for item in self.column_data:
            element.append(item.xml())
        return element


class ColumnData:
    def __init__(self, f):
        self.datatype = Uint(f)
        self.index = Uint(f)
        self.item = self.get_item(f)

    def get_item(self, f):
        match self.datatype.value:
            case 0:
                return String(f)
            case 1:
                assert Uint(f).value == 4
                return Uint(f)
            case 3:
                assert Uint(f).value == 8
                return Uuid(f)
            case 4:
                assert Uint(f).value == 1
                return Byte(f)
            case 5:
                return Buffer(f)

    def xml(self):
        element = ET.Element("ColumnData", attrib={"type": f"{self.datatype.value}", "index": f"{self.index.value}"})
        element.append(self.item.xml())
        return element


class Uuid:
    def __init__(self, f):
        self.uid = Uint(f)
        self.type = Uint(f)

    def xml(self):
        element = ET.Element("Uuid", attrib={"uid": f"{self.uid.value}"})
        element.append(self.type.xml())
        return element


class Buffer:
    def __init__(self, f):
        self.value = [Byte(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("Buffer")
        for item in self.value:
            element.append(item.xml())
        return element


class IndexTable:
    def __init__(self, f):
        self.value = [Column(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("IndexTable")
        for item in self.value:
            element.append(item.xml())
        return element


class Table:
    def __init__(self, f):
        self.value = [Row(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("Table")
        for item in self.value:
            element.append(item.xml())
        return element


if __name__ == "__main__":
    DATA_PATH = Path("../Zanzarah/Data/")
    for filepath in DATA_PATH.glob("*.fbs"):
        with open(filepath, "rb") as f:
            if filepath.stem == "_fb0x00":
                tree = ET.ElementTree(IndexTable(f).xml())
            else:
                tree = ET.ElementTree(Table(f).xml())
            ET.indent(tree, space = "  ")
            tree.write(filepath.stem + ".xml", encoding="utf8")
