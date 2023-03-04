from typing import TypedDict

from rich.console import Console

console = Console()
FILE_RE = (
    r"(?P<asdos>\w+)_(?P<kelas>\w)_(?P<npm>\d+)_(?P<name>.+)_[Ll]ab(?P<labnum>\d+)"
)


class ConfigType(TypedDict):
    kelas: str
    asdos: str
    editor: str


class Metadata(ConfigType):
    npm: str
    name: str
    labnum: str
