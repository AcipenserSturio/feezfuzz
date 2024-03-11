import xml.etree.ElementTree as ET

from .command import Command
from ..db.nodes.string import String


class Script:
    def __init__(self, f):
        self.string = String(f).value
        self.commands = [Command(string) for string in self.string.split("\n")]

    def xml(self):
        element = ET.Element("Script")
        for item in self.commands:
            element.append(item.xml())
        return element

    def toml(self):
        return "\n".join([command.toml() for command in self.commands])
