import xml.etree.ElementTree as ET

from ..enums import INSTRUCTIONS

from ..nodes.uint import Uint as Int
from ..nodes.uuid import Uuid as Uid

class Command:
    def __init__(self, string):
        if string.replace("\0", ""):
            self.arguments = string.split(".")
            command_name = self.arguments.pop(0)
            if len(command_name) != 1:
                print(f"Warning: malformed command {string}: command {command_name.encode()} not a single char  ")
            arglen, self.instruction = INSTRUCTIONS[command_name[0]]

            if len(self.arguments) != arglen:
                # Suppress warnings for commands of format "J.textid":
                # they are used extensively by vanilla
                if (command_name != "J" and len(self.arguments) != 1):
                    print(f"Warning: malformed command {string}: {len(self.arguments)} args given, {arglen} expected")
                self.arguments.extend([0, 0, 0])
                self.arguments = self.arguments[:arglen]

        else:
            self.arguments = []
            self.instruction = None

    def parse_args(instruction, args):
        match instruction:
            case "say":
                return [Uid(args.pop(0)), Int(args.pop(0))]
            case "setModel":
                return
            case "choice":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "waitForUser":
                return []
            case "label":
                return
            case "setCamera":
                return [Int(args.pop(0))]
            case "exit":
                return
            case "wizform":
                return
            case "spell":
                return
            case "else":
                return
            case "changeWaypoint":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "fight":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "lookAtPlayer":
                return
            case "changeDatabase":
                return [Uid(args.pop(0))]
            case "removeNpc":
                return []
            case "catchWizform":
                return []
            case "killPlayer":
                return []
            case "tradingCurrency":
                return [Uid(args.pop(0))]
            case "tradingItem":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "tradingSpell":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "tradingWizform":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "givePlayerCards":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "setupGambling":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "ifPlayerHasCards":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "ifPlayerHasSpecials":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "ifTriggerIsActive":
                return
            case "removePlayerCards":
                return
            case "moveSystem":
                return
            case "movementSpeed":
                return
            case "modifyWizform":
                return
            case "lockUserInput":
                return
            case "modifyTrigger":
                return
            case "playAnimation":
                return
            case "ifIsWizform":
                return
            case "startPrelude":
                return
            case "npcWizFormEscapes":
                return
            case "dance":
                return
            case "setGlobal":
                return
            case "beginIf_global":
                return
            case "talk":
                return
            case "goto":
                return
            case "gotoRandomLabel":
                return
            case "ask":
                return
            case "chafferWizForms":
                return
            case "setNpcType":
                return
            case "deployNpcAtTrigger":
                return
            case "delay":
                return
            case "gotoLabelByRandom":
                return
            case "ifCloseToWaypoint":
                return
            case "removeWizForms":
                return
            case "ifNpcModifierHasValue":
                return
            case "setNpcModifier":
                return
            case "defaultWizForm":
                return
            case "idle":
                return
            case "ifPlayerIsClose":
                return
            case "ifNumberOfNpcsIs":
                return
            case "startEffect":
                return
            case "setTalkLabels":
                return
            case "setCollision":
                return
            case "tradeWizform":
                return
            case "createDynamicItems":
                return
            case "playVideo":
                return
            case "removeNpcAtTrigger":
                return
            case "revive":
                return
            case "lookAtTrigger":
                return
            case "ifTriggerIsEnabled":
                return
            case "playSound":
                return
            case "playInArena":
                return
            case "startActorEffect":
                return
            case "endActorEffect":
                return
            case "createSceneObjects":
                return
            case "evolveWizForm":
                return
            case "removeBehavior":
                return
            case "unlockDoor":
                return
            case "endGame":
                return
            case "defaultDeck":
                return
            case "subGame":
                return
            case "modifyEffect":
                return
            case "playPlayerAnimation":
                return
            case "playAmyVoice":
                return
            case "createDynamicModel":
                return
            case "deploySound":
                return
            case "givePlayerPresent":
                return
            case "endIf":
                return


    def xml(self):
        element = ET.Element("Command")
        if not self.instruction:
            return element
        element.append(ET.Element("Instruction", text=f"{self.instruction}"))
        for arg in self.arguments:
            element.append(ET.Element("Arg", text=f"{arg}"))
        return element
