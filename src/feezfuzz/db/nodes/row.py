import xml.etree.ElementTree as ET

from .cell import Cell
from .uint import Uint
from .uuid import Uuid
from .string import String
from ...script.script import Script


class Row:
    def __init__(self, uid, cells):
        self.uid = uid
        self.cells = cells

    @classmethod
    def from_fbs(cls, f):
        uid = Uint(f)
        cells = [Cell.from_fbs(f) for index in range(Uint(f).value)]
        return cls(uid, cells)

    def xml(self):
        element = ET.Element("Row", attrib={"uid": f"{self.uid.hex()}"})
        for item in self.cells:
            element.append(item.xml())
        return element

    def fbs(self):
        return (
            self.uid.fbs()
            + Uint(len(self.cells)).fbs()
            + b"".join(item.fbs() for item in self.cells)
        )

    @classmethod
    def from_script_toml(
            cls,
            filename: str,
            data: dict,
            locale: "Table",
        ):
        return cls(
            Uuid(data["uid"]).uid,
            [
                Cell(Uint(3), Uint(3), Uuid(data["name"])),
                Cell(Uint(0), Uint(24), Script.from_toml(data["Script1"], locale, data["name"])),
                Cell(Uint(0), Uint(25), Script.from_toml(data["Script2"], locale, data["name"])),
                Cell(Uint(0), Uint(26), Script.from_toml(data["Script3"], locale, data["name"])),
                Cell(Uint(0), Uint(27), Script.from_toml(data["Script4"], locale, data["name"])),
                Cell(Uint(0), Uint(28), Script.from_toml(data["Script5"], locale, data["name"])),
                Cell(Uint(0), Uint(19), String(filename)),
            ],
        )

    @classmethod
    def new_text(
            cls,
            uid: Uint,
            text: str,
            npc_id: int,
        ):
        return cls(
            uid,
            [
                Cell(Uint(0), Uint(0), String(text)),
                Cell(Uint(1), Uint(29), Uint(npc_id)),
                Cell(Uint(0), Uint(30), String("")),
            ],
        )
