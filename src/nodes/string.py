import io
import struct
import xml.etree.ElementTree as ET

from .uint import Uint


class String:
    def __init__(self, f):

        if isinstance(f, io.IOBase):
            # pascal-like. the first 4 bytes are string length. not null terminated.
            length = Uint(f).value
            self.value = struct.unpack(f"<{length}s", f.read(length))[0].decode("cp1251", "replace")
        elif isinstance(f, str):
            self.value = f
        else:
            raise TypeError(type(f))


    @classmethod
    def from_value(cls, value):
        self = cls()
        self.value = value
        return self

    def xml(self):
        element = ET.Element("String")
        element.text = self.value.replace('\0', '')
        return element
