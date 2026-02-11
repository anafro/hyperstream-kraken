from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CLIArgs:
    query: str
    output: Path
