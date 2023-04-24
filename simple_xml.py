from pathlib import Path
import struct
import json
import xml.etree.ElementTree as ET

from defines import (
    DATA_TYPES,
    UUID_TYPES,
    COLUMN_NAMES,
    SPELL_CLASSES,
    SLOT_NAMES,
    CARD_TYPES,
)

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

class Ushort:
    def __init__(self, f):
        self.value = struct.unpack("<H", f.read(2))[0]

    def xml(self):
        element = ET.Element("Ushort")
        element.text = f"{self.value}"
        return element

class Level:
    def __init__(self, uint):
        byte = Byte(f).value
        self.first = byte & 0x0F
        self.second = byte >> 4
        byte = Byte(f).value
        self.third = byte & 0x0F
        self.slot = byte >> 4
        self.level = Ushort(f)

    def xml(self):
        element = ET.Element("Level")
        if self.level.value == 65535:
            return element
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.first]}"))
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.second]}"))
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.third]}"))
        element.append(ET.Element("Nibble", text=f"{SLOT_NAMES[self.slot]}"))
        element.append(self.level.xml())
        return element


class CardId:
    def __init__(self, f):
        Byte(f) # always 0xff
        self.type = Byte(f)
        self.id = Ushort(f)

    def xml(self):
        element = ET.Element("CardId", attrib={"type": f"{CARD_TYPES[self.type.value]}"})
        element.append(self.id.xml())
        return element


class Script:
    def __init__(self, f):
        self.string = String(f).value
        self.commands = [Command(string) for string in self.string.split("\n")]

    def xml(self):
        element = ET.Element("Script")
        for item in self.commands:
            element.append(item.xml())
        return element


class Command:
    def __init__(self, string):
        self.arguments = string.split(".")
        self.instruction = self.arguments.pop(0)

    def xml(self):
        element = ET.Element("Command")
        element.append(ET.Element("Instruction", text=f"{self.instruction}"))
        for arg in self.arguments:
            element.append(ET.Element("Arg", text=f"{arg}"))
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
        element = ET.Element("Row", attrib={"uid": f"{self.uid.value}"})
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
                if "Script" in COLUMN_NAMES[self.index.value]:
                    return Script(f)
                return String(f)
            case 1:
                assert Uint(f).value == 4
                if "Level" in COLUMN_NAMES[self.index.value]:
                    return Level(f)
                if "CardId" == COLUMN_NAMES[self.index.value]:
                    return CardId(f)
                return Uint(f)
            case 3:
                assert Uint(f).value == 8
                return Uuid(f)
            case 4:
                assert Uint(f).value == 1
                return Byte(f)
            case 5:
                raise Exception("Buffers exist in documentation, but not ingame. We don't support them")
            #     return Buffer(f)

    def xml(self):
        element = ET.Element(
            "ColumnData",
            attrib = {
                "type": f"{DATA_TYPES[self.datatype.value]}",
                "index": f"{COLUMN_NAMES[self.index.value]}",
            }
        )
        element.append(self.item.xml())
        return element


class Uuid:
    def __init__(self, f):
        self.uid = Uint(f)
        self.type = Uint(f)

    def xml(self):
        element = ET.Element("Uuid", attrib={"type": f"{UUID_TYPES[self.type.value]}"})
        element.text = f"{self.uid.value}"
        return element


# class Buffer:
#     def __init__(self, f):
#         self.value = [Byte(f) for index in range(Uint(f).value)]
#
#     def xml(self):
#         element = ET.Element("Buffer")
#         for item in self.value:
#             element.append(item.xml())
#         return element


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
