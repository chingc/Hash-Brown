"""Fixtures"""

from hashlib import algorithms_guaranteed
from pathlib import Path
from typing import List

from pytest import fixture

from hb.main import Checksum


CWD = Path(__file__).parent
FIXTURES = CWD / "fixtures"


@fixture
def supported() -> List[str]:
    """Guaranteed algorithms from hashlib minus ones with underscore plus adler32 and crc32."""
    return [x for x in sorted(algorithms_guaranteed) if "_" not in x] + ["adler32", "crc32"]

@fixture
def version() -> str:
    """Version from the pyproject.toml file."""
    ver = "Cannot find version!"
    with open(CWD.parent / "pyproject.toml", "r") as lines:
        for line in lines:
            if line.startswith("version = "):
                ver = line.strip().split(" = ")[1][1:-1]
    return ver

@fixture
def good_checklists() -> List[Path]:
    """All good checklists."""
    return [FIXTURES / f"checklist_good_0{i}.txt" for i in range(1, 2)]

@fixture
def bad_checklists() -> List[Path]:
    """All bad checklists."""
    return [FIXTURES / f"checklist_bad_0{i}.txt" for i in range(1, 4)]

@fixture
def fox() -> Checksum:
    """Checksum object."""
    return Checksum(FIXTURES / "fox.txt")

@fixture
def fox_progress() -> Checksum:
    """Checksum object with zero threshold."""
    return Checksum(FIXTURES / "fox.txt", threshold=0)
