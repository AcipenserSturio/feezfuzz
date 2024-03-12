import xml.etree.ElementTree as ET

from .row import Row
from .uint import Uint


class Table:
    def __init__(self, value = list()):
        self.value = value

    @classmethod
    def from_fbs(cls, f):
        length = Uint(f)
        value = [Row.from_fbs(f) for index in range(length.value)]
        return cls(value)

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

    def get_text(self, uid):
        for row in self.value:
            if row.uid.value == int(uid, 16):
                return row.cells[0].item.value.replace("\0", "")
        print(f"Malformed DB: text uid {uid} missing")
        return self.value[0].cells[0].item.value.replace("\0", "")

    def add(self, row):
        self.value.append(row)
