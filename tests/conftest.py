"""Fixtures"""

from pathlib import Path
from typing import List

import pytest

from hb.main import Checksum


_TEST_FILES = Path(__file__).parent / "test_files"
_FOX = str(_TEST_FILES / "fox.txt")

@pytest.fixture  # type: ignore
def good_checklists() -> List[str]:
    return [str(_TEST_FILES / "checklist_good.txt")]

@pytest.fixture  # type: ignore
def bad_checklists() -> List[str]:
    return [str(_TEST_FILES / f"checklist_bad_0{i}.txt") for i in range(1, 4)]

@pytest.fixture  # type: ignore
def supported() -> str:
    return Checksum.supported  # type: ignore

@pytest.fixture  # type: ignore
def blake2b() -> str:
    return Checksum(_FOX).blake2b()  # type: ignore

@pytest.fixture  # type: ignore
def blake2s() -> str:
    return Checksum(_FOX).blake2s()  # type: ignore

@pytest.fixture  # type: ignore
def md5() -> str:
    return Checksum(_FOX).md5()  # type: ignore

@pytest.fixture  # type: ignore
def sha1() -> str:
    return Checksum(_FOX).sha1()  # type: ignore

@pytest.fixture  # type: ignore
def sha224() -> str:
    return Checksum(_FOX).sha224()  # type: ignore

@pytest.fixture  # type: ignore
def sha256() -> str:
    return Checksum(_FOX).sha256()  # type: ignore

@pytest.fixture  # type: ignore
def sha384() -> str:
    return Checksum(_FOX).sha384()  # type: ignore

@pytest.fixture  # type: ignore
def sha512() -> str:
    return Checksum(_FOX).sha512()  # type: ignore

@pytest.fixture  # type: ignore
def adler32() -> str:
    return Checksum(_FOX).adler32()  # type: ignore

@pytest.fixture  # type: ignore
def crc32() -> str:
    return Checksum(_FOX).crc32()  # type: ignore
