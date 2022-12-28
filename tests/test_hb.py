# mypy: ignore-errors

import hashlib
import os
import re
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
def rand_file():
    """Generate a random ~1MB file."""
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    print("\n".join([str(uuid.uuid4()) for _ in range(30000)]), file=temp)
    temp.close()
    assert os.path.getsize(temp.name) > 1_000_000
    yield temp.name
    os.unlink(temp.name)
    assert not os.path.exists(temp.name)


@pytest.fixture
def rand_digestfile(rand_file):
    """Generate a file of digests."""
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    for algo in hb.algorithms_guaranteed:
        print(hb.compute(algo, rand_file), file=temp)
    temp.close()
    yield temp.name
    os.unlink(temp.name)
    assert not os.path.exists(temp.name)


def test_compute(subtests, rand_file):
    """Compare with direct usage of hashlib and zlib."""
    for algo in hb.algorithms_guaranteed:
        with subtests.test(algo=algo):
            with_hb = HashBrown(algo, rand_file).compute()
            with_stdlib = use_stdlib(algo, rand_file)
            assert with_hb == with_stdlib


def test_pprint(subtests, rand_file):
    """Check pretty print output."""
    for algo in hb.algorithms_guaranteed:
        with subtests.test(algo=algo):
            with_hb = hb.compute(algo, rand_file)
            with_stdlib = f"{use_stdlib(algo, rand_file)} {algo} {rand_file}"
            assert with_hb == with_stdlib


def test_scan(rand_digestfile):
    """Verify file scanner."""
    with_hb = hb.scan(rand_digestfile, stdout_only=False)
    with_stdlib = []

    with open(rand_digestfile, encoding="utf-8") as lines:
        for line in lines:
            if match := re.match(r"^([0-9A-Fa-f]+) (\w+) (.+)$", line):
                given, algo, path = match.group(1, 2, 3)
                if use_stdlib(algo, path) == given:
                    with_stdlib.append(f"OK {algo} {path}")
                else:
                    with_stdlib.append(f"BAD {algo} {path}")

    assert with_hb == with_stdlib
