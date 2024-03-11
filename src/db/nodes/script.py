import xml.etree.ElementTree as ET

from .command import Command
from .string import String


class Script:
    def __init__(self, f):
        self.string = String(f).value
        self.commands = [Command(string) for string in self.string.split("\n")]

    def xml(self):
        element = ET.Element("Script")
        for item in self.commands:
            element.append(item.xml())
        return element
