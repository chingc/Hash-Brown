"""test_hb.py"""

# mypy: ignore-errors
# pylint: disable=W

import hashlib
import os
import tempfile
import uuid
import zlib

import pytest

from hb import hb
from hb.hb import HashBrown


def use_stdlib(algo, path):
    """Compute the hexdigest using hashlib and zlib."""
    match algo:
        case "adler32":
            checksum = 1
            with open(path, mode="rb") as lines:
                for line in lines:
                    checksum = zlib.adler32(line, checksum)
            hexdigest = hex(checksum).removeprefix("0x").zfill(8)
        case "crc32":
            checksum = 0
            with open(path, mode="rb") as lines:
                for line in lines:
                    checksum = zlib.crc32(line, checksum)
            hexdigest = hex(checksum).removeprefix("0x").zfill(8)
        case _:
            digest = hashlib.new(algo)
            with open(path, mode="rb") as lines:
                for line in lines:
                    digest.update(line)
            if algo.startswith("shake_"):
                hexdigest = digest.hexdigest(64)
            else:
                hexdigest = digest.hexdigest()
    return hexdigest


@pytest.fixture
def randfile():
    """Generate a random ~1MB file."""
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    print("\n".join([str(uuid.uuid4()) for _ in range(30000)]), file=temp)
    temp.close()
    assert os.path.getsize(temp.name) > 1000000
    yield temp.name
    os.unlink(temp.name)
    assert not os.path.exists(temp.name)


def test_compute(subtests, randfile):
    """Compare with direct usage of hashlib and zlib."""
    for algo in hashlib.algorithms_guaranteed | {"adler32", "crc32"}:
        with subtests.test(algo=algo):
            using_hb = HashBrown(algo, randfile).compute()
            using_stdlib = use_stdlib(algo, randfile)
            assert using_hb == using_stdlib


def test_pprint(subtests, randfile):
    """Check pretty print output."""
    for algo in hashlib.algorithms_guaranteed | {"adler32", "crc32"}:
        with subtests.test(algo=algo):
            hexdigest = use_stdlib(algo, randfile)
            assert hb.compute(algo, randfile) == f"{hexdigest} {algo} {randfile}"
