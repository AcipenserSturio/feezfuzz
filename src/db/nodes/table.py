import xml.etree.ElementTree as ET

from .row import Row
from .uint import Uint


class Table:
    def __init__(self, f):
        self.value = [Row(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("Table")
        for item in self.value:
            element.append(item.xml())
        return element

    def fbs(self):
        return (
            Uint(len(self.value)).fbs()
            + b"".join(item.fbs() for item in self.value)
        )
