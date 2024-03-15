import re
import xml.etree.ElementTree as ET

from .row import Row
from .uint import Uint
from .uuid import Uuid


class Table:
    def __init__(self, value=None):
        if value == None:
            value = []
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

    def get_toml_text(self, uid):
        text = self.get_text(uid)
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
        if not len(re.findall(r"[\.\?\!] ", text)):
            return f"<{' '.join(sentences)}>"
        sentences = "\n    ".join(sentences)
        return f"<\n    {sentences}\n>"

    def add(self, row):
        self.value.append(row)

    def register_text(self, text: str, npc_id: int) -> Uuid:
        uuid = self.new_uid()
        self.add(Row.new_text(uuid.uid, text, npc_id))
        return uuid

    def new_uid(self) -> Uuid:
        table_suffix = "5"
        hex_len = Uint(len(self.value)).hex()
        if hex_len[0] != "0":
            raise IndexError("Too many uids in table")
        uid_str = hex_len[1:] + table_suffix
        return Uuid(uid_str)
