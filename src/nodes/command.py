import xml.etree.ElementTree as ET

from ..enums import INSTRUCTIONS


class Command:
    def __init__(self, string):
        if string.replace("\0", ""):
            self.arguments = string.split(".")
            self.instruction = INSTRUCTIONS[self.arguments.pop(0)]
        else:
            self.arguments = []
            self.instruction = None

    def xml(self):
        element = ET.Element("Command")
        if not self.instruction:
            return element
        element.append(ET.Element("Instruction", text=f"{self.instruction}"))
        for arg in self.arguments:
            element.append(ET.Element("Arg", text=f"{arg}"))
        return element
