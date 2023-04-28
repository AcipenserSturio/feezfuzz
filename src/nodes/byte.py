import struct
import xml.etree.ElementTree as ET


class Byte:
    def __init__(self, f):
        self.value = struct.unpack("<B", f.read(1))[0]

    def xml(self):
        element = ET.Element("Byte")
        element.text = f"{self.value}"
        return element
