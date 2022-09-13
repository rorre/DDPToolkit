import json
from pathlib import Path
import re
from typing import Optional, Tuple, cast
from zipfile import ZipFile

from constants import FILE_RE, ConfigType, Metadata, console


def extract_zip(zippath: Path):
    with ZipFile(zippath) as zfile:
        zfile.extractall(zippath.parent)


def check_folder(
    config: ConfigType, path: Path
) -> Tuple[bool, str, Optional[Metadata]]:
    valid_path: Optional[Path] = None
    metadata: Optional[Metadata] = None
    for zip_path in path.glob("**/*.zip"):
        match = re.search(FILE_RE, zip_path.name)
        if not match:
            return False, "invalid filename", None

        if match.groupdict()["kelas"].lower() != config["kelas"].lower():
            return False, "unmatch class", None

        if match.groupdict()["asdos"].lower() != config["asdos"].lower():
            return False, "unmatch asdos", None

        valid_path = zip_path
        metadata = cast(Metadata, match.groupdict())
        break

    if not valid_path or not metadata:
        return False, "no such zip", None

    return True, "", metadata


def load_metadata(path: Path) -> Metadata:
    with open(path / "metadata.json", "r") as f:
        return json.load(f)


def select_main(path: Path) -> Path:
    py_paths = list(path.glob("**/*.py"))
    num = 0
    if len(py_paths) > 1:
        console.print("[yellow]There are more than one script file, select one:")
        for i, pypath in enumerate(py_paths):
            console.print(f"  [{i}] {pypath.relative_to(path)}")

        while True:
            num = int(console.input("Select number:"))
            if num < len(py_paths):
                break

    return py_paths[num]
