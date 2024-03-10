import xml.etree.ElementTree as ET

from ..enums import INSTRUCTIONS

from ..nodes.uint import Uint as Int
from ..nodes.uuid import Uuid as Uid
from ..nodes.string import String

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
                self.arguments.extend(["0", "0", "0"])

            self.arguments = self.parse_args(self.instruction, self.arguments)

        else:
            self.arguments = []
            self.instruction = None

    def parse_args(self, instruction, args):
        match instruction:
            case "say":
                return [Uid(args.pop(0)), Int(args.pop(0))]
            case "setModel":
                return [String(args.pop(0))]
            case "choice":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "waitForUser":
                return []
            case "label":
                return []
            case "setCamera":
                return [Int(args.pop(0))]
            case "exit":
                return []
            case "wizform":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "spell":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "else":
                return []
            case "changeWaypoint":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "fight":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "lookAtPlayer":
                return [Int(args.pop(0)), Int(args.pop(0))]
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
                return [Int(args.pop(0))]
            case "removePlayerCards":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "moveSystem":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "movementSpeed":
                return [Int(args.pop(0))]
            case "modifyWizform":
                return
            case "lockUserInput":
                return [Int(args.pop(0))]
            case "modifyTrigger":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "playAnimation":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "ifIsWizform":
                return
            case "startPrelude":
                return []
            case "npcWizFormEscapes":
                return []
            # case "dance":
            #     return  # unclear
            case "setGlobal":
                return [Int(args.pop(0)), Int(args.pop(0))] # unclear
            case "beginIf_global":
                return [Int(args.pop(0)), Int(args.pop(0))] # unclear
            case "talk":
                return [Uid(args.pop(0))]
            case "goto":
                return [Int(args.pop(0))]
            case "gotoRandomLabel":
                return [Int(args.pop(0)), Int(args.pop(0))]
            # case "ask":
            #     return  # What even is ask?
            case "chafferWizForms":
                return [Uid(args.pop(0)), Uid(args.pop(0)), Uid(args.pop(0))]
            case "setNpcType":
                return [Int(args.pop(0))]
            case "deployNpcAtTrigger":
                if args[1] in ("0", "1"):
                    return [Int(args.pop(0)), Uid(args.pop(0))]
                else:
                    return [Uid(args.pop(0)), Uid(args.pop(0))]
            case "delay":
                return [Int(args.pop(0))]
            case "gotoLabelByRandom":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "ifCloseToWaypoint":
                return [Int(args.pop(0))]
            case "removeWizForms":
                return []
            case "ifNpcModifierHasValue":
                return [Int(args.pop(0))]
            case "setNpcModifier":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "defaultWizForm":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "idle":
                return []
            case "ifPlayerIsClose":
                return [Int(args.pop(0))]
            case "ifNumberOfNpcsIs":
                return [Int(args.pop(0)), Uid(args.pop(0))]
            case "startEffect":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "setTalkLabels":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "setCollision":
                return [Int(args.pop(0))]
            case "tradeWizform":
                return [Int(args.pop(0))]
            case "createDynamicItems":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "playVideo":
                return [Int(args.pop(0))]
            case "removeNpcAtTrigger":
                return [Int(args.pop(0))]
            case "revive":
                return []
            case "lookAtTrigger":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "ifTriggerIsEnabled":
                return [Int(args.pop(0))]
            case "playSound":
                return [Int(args.pop(0))]
            case "playInArena":
                return [Int(args.pop(0))]
            case "startActorEffect":
                return [Int(args.pop(0))]
            case "endActorEffect":
                return []
            case "createSceneObjects":
                return [Int(args.pop(0))]
            # case "evolveWizForm":
            #     return # unclear
            case "removeBehavior":
                return [Int(args.pop(0))]
            case "unlockDoor":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "endGame":
                return []
            case "defaultDeck":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "subGame":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "modifyEffect":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "playPlayerAnimation":
                return [Int(args.pop(0))]
            case "playAmyVoice":
                return [String(args.pop(0))]
            case "createDynamicModel":
                return [Int(args.pop(0)), Int(args.pop(0)), Int(args.pop(0))]
            case "deploySound":
                return [Int(args.pop(0)), Int(args.pop(0))]
            case "givePlayerPresent":
                return [Int(args.pop(0))]
            case "endIf":
                return []
            case _:
                print(f"Malformed script: {instruction}")


    def xml(self):
        element = ET.Element("Command")
        if not self.instruction:
            return element
        element.append(ET.Element("Instruction", text=f"{self.instruction}"))
        if self.arguments:
            for arg in self.arguments:
                element.append(arg.xml())
        return element
