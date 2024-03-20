import argparse
import os.path
from pathlib import Path

from .build import build


def dir_path(path):
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"{path} is not a valid path")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Feezfuzz",
        description="A WIP build system for Zanzarah's Data files.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=dir_path,
        default=".",
    )
    args = parser.parse_args()
    build(Path(args.path))
