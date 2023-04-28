import struct
import xml.etree.ElementTree as ET

from .uint import Uint


class String:
    def __init__(self, f):
        # pascal-like. the first 4 bytes are string length. not null terminated.
        length = Uint(f).value
        self.value = struct.unpack(f"<{length}s", f.read(length))[0].decode("cp1252")

    def xml(self):
        element = ET.Element("String")
        element.text = f"{self.value}"
        return element
