import json
import shutil
import subprocess
from pathlib import Path

import typer

from constants import ConfigType, console
from utils import check_folder, extract_zip, load_metadata, select_main

app = typer.Typer()

submissions_dir = Path("submissions")
invalid_dir = Path("invalid")

submissions_dir.mkdir(exist_ok=True)
invalid_dir.mkdir(exist_ok=True)

with open("config.json", "r") as f:
    config: ConfigType = json.load(f)


@app.command(name="filter")
def filter_submissions():
    for path in submissions_dir.iterdir():
        is_valid, reason, meta = check_folder(config, path)
        if not is_valid:
            console.print(f"[yellow]{path.name} is invalid due to {reason}")
            Path(invalid_dir / reason).mkdir(exist_ok=True)
            shutil.move(path, invalid_dir / reason / path.name)
            continue

        with open(path / "metadata.json", "w") as f:
            json.dump(meta, f)


@app.command(name="extract")
def extract_submissions():
    for path in submissions_dir.iterdir():
        for zip_path in path.glob("*.zip"):
            extract_zip(zip_path)


@app.command(name="run")
def run_submissions():
    for path in submissions_dir.iterdir():
        metadata = load_metadata(path)
        py_path = select_main(path)

        console.clear()

        console.rule("[b]" + metadata["name"])
        console.print(f"Opening file in code editor ({config['editor']})")
        subprocess.run([config["editor"], py_path], shell=True)

        ans = console.input("Run? [Y/n] ")
        if ans.lower() == "n":
            continue

        console.print(f"Running for user [b]{metadata['name']}")
        subprocess.run(["ddpvalidator", py_path.parent, "-i"])

        # console.input("Enter to continue...")


if __name__ == "__main__":
    app()
