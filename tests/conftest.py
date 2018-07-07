"""Fixtures"""

from pathlib import Path
from typing import List

import pytest

from hb.main import Checksum


_FOX = str(Path(__file__).parent / "test_files" / "fox.txt")

@pytest.fixture  # type: ignore
def supported() -> List[str]:
    return Checksum.supported()

@pytest.fixture  # type: ignore
def blake2b() -> str:
    return Checksum(_FOX).blake2b()

@pytest.fixture  # type: ignore
def blake2s() -> str:
    return Checksum(_FOX).blake2s()

@pytest.fixture  # type: ignore
def md5() -> str:
    return Checksum(_FOX).md5()

@pytest.fixture  # type: ignore
def sha1() -> str:
    return Checksum(_FOX).sha1()

@pytest.fixture  # type: ignore
def sha224() -> str:
    return Checksum(_FOX).sha224()

@pytest.fixture  # type: ignore
def sha256() -> str:
    return Checksum(_FOX).sha256()

@pytest.fixture  # type: ignore
def sha384() -> str:
    return Checksum(_FOX).sha384()

@pytest.fixture  # type: ignore
def sha512() -> str:
    return Checksum(_FOX).sha512()

@pytest.fixture  # type: ignore
def adler32() -> str:
    return Checksum(_FOX).adler32()

@pytest.fixture  # type: ignore
def crc32() -> str:
    return Checksum(_FOX).crc32()
