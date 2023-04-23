from pathlib import Path
import struct
import json

def Byte(f):
    value = struct.unpack("<B", f.read(1))[0]
    # print(f"byte {value}")
    return value

def Uint(f):
    value = struct.unpack("<I", f.read(4))[0]
    # print(f"uint {value}")
    return value

def String(f):
    # pascal-like. the first 4 bytes are string length. not null terminated.
    length = Uint(f)
    value = struct.unpack(f"<{length}s", f.read(length))[0].decode("cp1252")
    # print(f"string {value}")
    return value


def Column(f):
    type = Uint(f)
    name = String(f)
    value = [type, name]
    # print(f"column {value}")
    return value

def Row(f):
    uid = Uint(f)
    column_data = [ColumnData(f) for index in range(Uint(f))]
    value = [uid, column_data]
    # print(f"row {value}")
    return value


def ColumnData(f):
    datatype = Uint(f)
    index = Uint(f)
    if datatype == 0:
        item = String(f)
    elif datatype == 1:
        assert Uint(f) == 4
        item = Uint(f)
    elif datatype == 3:
        assert Uint(f) == 8
        item = Uuid(f)
    elif datatype == 4:
        assert Uint(f) == 1
        item = Byte(f)
    elif datatype == 5:
        item = Buffer(f)
    value = [datatype, index, item]
    # print(f"columndata {value}")
    return value

def Uuid(f):
    # unused = Uint(f)
    uid = Uint(f)
    type = Uint(f)
    value = [uid, type]
    # print(f"uuid {value}")
    return value

def Buffer(f):
    value = [Byte(f) for index in range(Uint(f))]
    # print(f"buffer {value}")
    return value

def index_table(f):
    return [Column(f) for index in range(Uint(f))]

def table(f):
    return [Row(f) for index in range(Uint(f))]


if __name__ == "__main__":
    DATA_PATH = Path("../Zanzarah/Data/")
    for filepath in DATA_PATH.glob("*.fbs"):
        with open(filepath, "rb") as f:
            if filepath.stem == "_fb0x00":
                data = index_table(f)
            else:
                data = table(f)
            with open(filepath.stem + ".json", "w") as out:
                json.dump(data, out, indent=2)
