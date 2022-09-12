import copy
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple
from zipfile import BadZipFile, ZipFile

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

app = typer.Typer()

FILE_RE = r"H_(?P<asdos>\w+)_(?P<npm>\d+)_(?P<name>.+)_[Ll]ab(?P<labnum>\d+)"
console = Console()


def filter_files(pattern: str):
    valid: List[Tuple[Path, re.Match[str]]] = []
    invalid: List[Path] = []

    for fpath in Path("submissions").glob(pattern):
        match = re.search(FILE_RE, fpath.name)
        if not match:
            console.print(f"[red]{fpath} has invalid scheme")
            invalid.append(fpath)
            continue

        valid.append((fpath, match))
    return (valid, invalid)


def extract_zip(zippath: Path):
    with ZipFile(zippath) as zfile:
        zfile.extractall(zippath.parent)


def get_submission():
    valid_zip, invalid_zip = filter_files("**/*.zip")
    for path, _ in valid_zip:
        try:
            extract_zip(path)
        except BadZipFile as e:
            console.print(f"[red]{path} -- Exception occured:", e)

    valid, invalid = filter_files("**/*.py")
    invalid.extend(invalid_zip)

    for curr in copy.copy(valid):
        fpath = curr[0]
        match = curr[1]
        if match.groupdict()["asdos"].lower() != "ren":
            console.print(f"[yellow]{fpath} has different TA")
            invalid.append(fpath)
            valid.remove(curr)
    return valid, invalid


@app.command(name="filter")
def filter_submissions():
    _, invalid = get_submission()
    for fpath in invalid:
        try:
            shutil.rmtree(fpath.parent)
        except:
            console.print("[yellow]Error occured on trying to remove", fpath.parent)


@app.command(name="run")
def run_submissions():
    valid, _ = get_submission()
    for submission in valid:
        console.clear()
        console.rule("[b]" + submission[0].name)
        params = submission[1].groupdict()

        syntaxed = Syntax.from_path(str(submission[0]))
        console.print(Panel(syntaxed, title=params["name"]))

        ans = console.input("Run? [Y/n] ")
        if ans.lower() == "n":
            continue

        console.print(f"Running for user [b]{params['name']}")
        subprocess.run(["DDPValidator", submission[0].parent, "-i"])

        console.input("Enter to continue...")


if __name__ == "__main__":
    app()
