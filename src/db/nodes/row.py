import xml.etree.ElementTree as ET

from .cell import Cell
from .uint import Uint
from .uuid import Uuid
from .string import String


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
            Uuid(data["uid"]),
            [
                Cell(Uint(3), Uint(3), Uuid(data["name"])),
                Cell(Uint(0), Uint(24), String(data["Script1"])),
                Cell(Uint(0), Uint(25), String(data["Script2"])),
                Cell(Uint(0), Uint(26), String(data["Script3"])),
                Cell(Uint(0), Uint(27), String(data["Script4"])),
                Cell(Uint(0), Uint(28), String(data["Script5"])),
                Cell(Uint(0), Uint(19), String(filename)),
            ],
        )
