import xml.etree.ElementTree as ET

from .cell import Cell
from .uint import Uint


class Row:
    def __init__(self, f):
        self.uid = Uint(f)
        self.cells = [Cell(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("Row", attrib={"uid": f"{self.uid.value}"})
        for item in self.cells:
            element.append(item.xml())
        return element
