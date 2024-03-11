import xml.etree.ElementTree as ET

from .command import Command
from ..db.nodes.string import String
from ..db.nodes.table import Table


class Script:
    def __init__(self, script: str, locale: Table):
        self.script = script
        self.commands = [Command(string, locale) for string in self.script.split("\n")]

    def xml(self):
        element = ET.Element("Script")
        for item in self.commands:
            element.append(item.xml())
        return element

    def toml(self):
        return "\n".join([command.toml() for command in self.commands])
