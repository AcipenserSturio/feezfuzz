import re
import xml.etree.ElementTree as ET

from .command import Command
from ..db.nodes.string import String
from ..db.nodes.uint import Uint
from ..db.nodes.uuid import Uuid
from .instructions import INSTRUCTIONS


class Script:
    def __init__(self, script: str):
        self.script = script
        self.commands = [Command(string) for string in self.script.strip().split("\n")]

    @classmethod
    def from_toml(cls, script: str, locale: "Table", npc_id: str):
        while text := re.search("<.*?>", script, flags=re.DOTALL):
            text = text.group(0)
            uuid = locale.register_text(format_text(text), Uuid(npc_id).uid.value)
            script = re.sub(re.escape(text), uuid.hex(), script)
        return cls(script)

    def xml(self):
        element = ET.Element("Script")
        for item in self.commands:
            element.append(item.xml())
        return element

    def toml(self, locale):
        return "\n".join([command.toml(locale) for command in self.commands])

    def fbs(self):
        return String("\n".join([command.string() for command in self.commands])).fbs()


def format_text(text: str) -> str:
    text = re.sub("\n *", " ", text)
    text = re.sub("[<>]", "", text)
    text = text.strip()
    return text
