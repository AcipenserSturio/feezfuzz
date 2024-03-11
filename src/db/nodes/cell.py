import xml.etree.ElementTree as ET

from .byte import Byte
from .cardid import CardId
from .level import Level
from .string import String
from .uint import Uint
from .uuid import Uuid
from ..enums import (
    COLUMN_NAMES,
    DATA_TYPES,
)


class Cell:
    def __init__(self, f):
        self.datatype = Uint(f)
        self.index = Uint(f)
        self.item = self.get_item(f)

    def get_item(self, f):
        match self.datatype.value:
            case 0:
                # if "Script" in COLUMN_NAMES[self.index.value]:
                #     return Script(f)
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
            "Cell",
            attrib = {
                "type": f"{DATA_TYPES[self.datatype.value]}",
                "index": f"{COLUMN_NAMES[self.index.value]}",
            }
        )
        element.append(self.item.xml())
        return element

    def item_fbs(self):
        match self.datatype.value:
            case 0:
                return self.item.fbs()
            case 1:
                return Uint(4).fbs() + self.item.fbs()
            case 3:
                return Uint(8).fbs() + self.item.fbs()
            case 4:
                return Uint(1).fbs() + self.item.fbs()
            case 5:
                raise Exception("Buffers exist in documentation, but not ingame. We don't support them")
            #     self.item.fbs()

    def fbs(self):
        return (
            self.datatype.fbs()
            + self.index.fbs()
            + self.item_fbs()
        )
