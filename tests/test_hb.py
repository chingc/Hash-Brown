"""test_hb.py"""

# mypy: ignore-errors

import hashlib
import zlib

from hb import hb
from hb.hb import HashBrown


def use_stdlib(algo, path) -> str:
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


def test_compute(subtests):
    """Compare with direct usage of hashlib and zlib."""
    for algo in hashlib.algorithms_guaranteed | {"adler32", "crc32"}:
        with subtests.test(algo=algo):
            using_hb = HashBrown(algo, "LICENSE").compute()
            using_stdlib = use_stdlib(algo, "LICENSE")
            assert using_hb == using_stdlib


def test_pprint(subtests):
    """Check pretty print output."""
    for algo in hashlib.algorithms_guaranteed | {"adler32", "crc32"}:
        with subtests.test(algo=algo):
            hexdigest = use_stdlib(algo, "LICENSE")
            assert hb.compute(algo, "LICENSE") == f"{hexdigest} {algo} LICENSE"
