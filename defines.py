
SPELL_CLASSES = {
    0: "None",
    1: "Nature",
    2: "Air",
    3: "Water",
    4: "Light",
    5: "Energy",
    6: "Psi",
    7: "Rock",
    8: "Ice",
    9: "Fire",
    10: "Night",
    11: "Chaos",
    12: "Metal",
    13: "Joker",
    14: "Invalid1",
    15: "Invalid2",
}


SLOT_NAMES = {
    0: "Slot 1",
    1: "Slot 2",
    2: "Slot 3",
    3: "Slot 4",
}


CARD_TYPES = {
    0: "Item",
    1: "Spell",
    2: "Fairy",
}


DATA_TYPES = {
    0: "string",
    1: "integer",
    3: "uuid",
    4: "byte",
    5: "buffer",
}


UUID_TYPES = {
    1227272: "fairy-name-info", # 158
    1242004: "npc-name",        # 148
    1240728: "spell-desc",      # 142
    1239960: "unk-1",           # 98
    1241024: "unk-2",           # 98
    8057384: "npc-name-2",      # 54
    1241796: "unk-4",           # 34
    1242428: "unk-5",           # 8
    1241028: "unk-6",           # 4
    1242300: "unk-7",           # 2
    1242368: "unk-8",           # 2
    1241920: "unk-9",           # 2
    1243164: "unk-10",          # 2
    1243080: "unk-11",          # 2
    7926312: "unk-12",          # 1
    1242416: "unk-13",          # 1
    1242636: "unk-14",          # 1
}


UUID_GROUPS = {
    0: "WizForm - Names",
    1: "Spell - Names",
    2: "Items - Names",
    3: "Credits",
    4: "Menus",
    5: "Npc - Names",
    6: "unused",
    7: "Scene Names",
    8: "Signs",
    9: "Item - Descriptions",
    10: "Spell Descriptions",
    11: "WizForm - Descriptions",
    12: "Help",
    13: "Dance Descriptions",
    14: "Start Dialog",
    15: "Class Group",
}


# We could read these dynamically. But I just don't
COLUMN_NAMES = [
    "Text",
    "Group",
    "Define",
    "Name",
    "CardId",
    "Info",
    "Mesh",
    "Class1",
    "Class2",
    "Level0",
    "Level1",
    "Level2",
    "Level3",
    "Level4",
    "Level5",
    "Level6",
    "Level7",
    "Level8",
    "Level9",
    "unknown",
    "SpellDesc",
    "PriceA",
    "PriceB",
    "PriceC",
    "Script1",
    "Script2",
    "Script3",
    "Script4",
    "Script5",
    "Npc",
    "Voice",
    "Special",
    "Script",
    "MHP",
    "EvolCId",
    "EvolVar",
    "MovSpeed",
    "Class0",
    "Mana",
    "Loadup",
    "Trajectory",
    "MissileEffect",
    "ImpactEffect",
    "Damage",
    "Type",
    "Behaviour",
    "JumpPower",
    "CriticalHit",
    "Glow",
    "Sphere",
    "LevelUp",
]


INSTRUCTIONS = {
    "!": "say",
    "C": "setModel",
    "\"": "choice",
    "#": "waitForUser",
    "$": "label",
    "&": "setCamera",
    "%": "exit",
    "'": "wizform",
    "(": "spell",
    "8": "else",
    ")": "changeWaypoint",
    "*": "fight",
    "+": "lookAtPlayer",
    ",": "changeDatabase",
    "-": "removeNpc",
    ".": "catchWizform",
    "0": "killPlayer",
    "5": "tradingCurrency",
    "2": "tradingItem",
    "3": "tradingSpell",
    "4": "tradingWizform",
    "1": "givePlayerCards",
    "B": "setupGambling",
    "6": "ifPlayerHasCards",
    "@": "ifPlayerHasSpecials",
    "=": "ifTriggerIsActive",
    "9": "removePlayerCards",
    ":": "moveSystem",
    "?": "movementSpeed",
    ";": "modifyWizform",
    "<": "lockUserInput",
    ">": "modifyTrigger",
    "A": "playAnimation",
    "D": "ifIsWizform",
    "E": "startPrelude",
    "F": "npcWizFormEscapes",
    "G": "dance",
    "H": "setGlobal",
    "I": "beginIf_global",
    "J": "talk",
    "K": "goto",
    "L": "gotoRandomLabel",
    "M": "ask",
    "N": "chafferWizForms",
    "O": "setNpcType",
    "P": "deployNpcAtTrigger",
    "Q": "delay",
    "R": "gotoLabelByRandom",
    "S": "ifCloseToWaypoint",
    "T": "removeWizForms",
    "U": "ifNpcModifierHasValue",
    "V": "setNpcModifier",
    "W": "defaultWizForm",
    "X": "idle",
    "Y": "ifPlayerIsClose",
    "Z": "ifNumberOfNpcsIs",
    "[": "startEffect",
    "\\": "setTalkLabels",
    "]": "setCollision",
    "^": "tradeWizform",
    "_": "createDynamicItems",
    "`": "playVideo",
    "a": "removeNpcAtTrigger",
    "b": "revive",
    "c": "lookAtTrigger",
    "d": "ifTriggerIsEnabled",
    "e": "playSound",
    "f": "playInArena",
    "g": "startActorEffect",
    "h": "endActorEffect",
    "i": "createSceneObjects",
    "j": "evolveWizForm",
    "k": "removeBehavior",
    "l": "unlockDoor",
    "m": "endGame",
    "n": "defaultDeck",
    "o": "subGame",
    "p": "modifyEffect",
    "q": "playPlayerAnimation",
    "s": "playAmyVoice",
    "r": "createDynamicModel",
    "t": "deploySound",
    "u": "givePlayerPresent",
    "7": "endIf",
}
