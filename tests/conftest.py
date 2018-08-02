"""Fixtures"""

from hashlib import algorithms_guaranteed
from pathlib import Path
from typing import List

import pytest

from hb.main import Checksum


_HERE = Path(__file__).parent
_FOX = str(_HERE / "test_files" / "fox.txt")


@pytest.fixture
def supported() -> List[str]:
    return [x for x in sorted(algorithms_guaranteed) if "_" not in x] + ["adler32", "crc32"]

@pytest.fixture
def version() -> str:
    ver = "Cannot find version!"
    with open(_HERE.parent / "pyproject.toml", "r") as lines:
        for line in lines:
            if line.startswith("version = "):
                ver = line.strip().split(" = ")[1][1:-1]
    return ver

@pytest.fixture
def good_checklists() -> List[str]:
    return [str(_HERE / "test_files" / "checklist_good.txt")]

@pytest.fixture
def bad_checklists() -> List[str]:
    return [str(_HERE / "test_files" / f"checklist_bad_0{i}.txt") for i in range(1, 4)]

@pytest.fixture
def blake2b() -> str:
    return str(Checksum(_FOX).blake2b)

@pytest.fixture
def blake2s() -> str:
    return str(Checksum(_FOX).blake2s)

@pytest.fixture
def md5() -> str:
    return str(Checksum(_FOX).md5)

@pytest.fixture
def sha1() -> str:
    return str(Checksum(_FOX).sha1)

@pytest.fixture
def sha224() -> str:
    return str(Checksum(_FOX).sha224)

@pytest.fixture
def sha256() -> str:
    return str(Checksum(_FOX).sha256)

@pytest.fixture
def sha384() -> str:
    return str(Checksum(_FOX).sha384)

@pytest.fixture
def sha512() -> str:
    return str(Checksum(_FOX).sha512)

@pytest.fixture
def adler32() -> str:
    return str(Checksum(_FOX).adler32)

@pytest.fixture
def crc32() -> str:
    return str(Checksum(_FOX).crc32)

@pytest.fixture
def checksum_obj() -> Checksum:
    return Checksum(_FOX, threshold=0)
