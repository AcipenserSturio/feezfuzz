import xml.etree.ElementTree as ET

from .uint import Uint
from ..enums import UUID_TYPES


class Uuid:
    def __init__(self, f):
        self.uid = Uint(f)
        self.type = Uint(f)

    def xml(self):
        element = ET.Element("Uuid", attrib={"type": f"{UUID_TYPES[self.type.value]}"})
        element.text = f"{self.uid.value}"
        return element
