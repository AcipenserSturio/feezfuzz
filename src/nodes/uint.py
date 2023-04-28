import struct
import xml.etree.ElementTree as ET


class Uint:
    def __init__(self, f):
        self.value = struct.unpack("<I", f.read(4))[0]

    def xml(self):
        element = ET.Element("Uint")
        element.text = f"{self.value}"
        return element
