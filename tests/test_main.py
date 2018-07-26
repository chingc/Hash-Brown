"""Tests"""

from typing import List

import pytest

from hb.main import Checksum


def test_version() -> None:
    assert Checksum.version() == "1.1.2"

    with pytest.raises(LookupError):
        Checksum.version("LICENSE")

def test_parse(good_checklists: List[str], bad_checklists: List[str]) -> None:
    for checklist in good_checklists:
        for algorithm, path, checksum in Checksum.parse(checklist):
            assert algorithm == "md5"
            assert path == "test.txt"
            assert checksum == "c08420f4c716f3814c268dd845356276"

    for checklist in bad_checklists:
        with pytest.raises(ValueError):
            for algorithm, path, checksum in Checksum.parse(checklist): pass

def test_print() -> None:
    assert Checksum.print("a", "b", "c") == "a (b) = c"

def test_supported(supported: str) -> None:
    assert supported == "blake2b blake2s md5 sha1 sha224 sha256 sha384 sha512 adler32 crc32"

def test_unsupported() -> None:
    with pytest.raises(ValueError):
        Checksum(".").compute("unsupported")

def test_blake2b(blake2b: str) -> None:
    assert blake2b == "20a9ed5b422c04cf7328b36c0d4ad235408d034bee5a15d77a4185c1bf2c30202d340c212e872d1074f3556f428357e2503b749f3e198b59a74313ad2975a951"

def test_blake2s(blake2s: str) -> None:
    assert blake2s == "668e0a8671f032f313c8a12d24f5c8669259ba6d9a9f6f62451ea33fda9f2f79"

def test_md5(md5: str) -> None:
    assert md5 == "37c4b87edffc5d198ff5a185cee7ee09"

def test_sha1(sha1: str) -> None:
    assert sha1 == "be417768b5c3c5c1d9bcb2e7c119196dd76b5570"

def test_sha224(sha224: str) -> None:
    assert sha224 == "62e514e536e4ed4633eeec99d60f97b4d95889227975d975b2ad0de3"

def test_sha256(sha256: str) -> None:
    assert sha256 == "c03905fcdab297513a620ec81ed46ca44ddb62d41cbbd83eb4a5a3592be26a69"

def test_sha384(sha384: str) -> None:
    assert sha384 == "f565ad8f9c76cf8c4a2e145e712df740702e066a5908f6285eafa1a83a623e882207643ce5ec29628ff0186150275ef3"

def test_sha512(sha512: str) -> None:
    assert sha512 == "a12ac6bdd854ac30c5cc5b576e1ee2c060c0d8c2bec8797423d7119aa2b962f7f30ce2e39879cbff0109c8f0a3fd9389a369daae45df7d7b286d7d98272dc5b1"

def test_adler32(adler32: str) -> None:
    assert adler32 == "6bc00fe4"

def test_crc32(crc32: str) -> None:
    assert crc32 == "6d93c138"

def test_via_get(checksum_obj: Checksum) -> None:
    assert checksum_obj.get("md5") == "37c4b87edffc5d198ff5a185cee7ee09"
    assert checksum_obj.get("crc32") == "6d93c138"

    # should not actually go through full compute again
    # this covers some lines for code coverage
    assert checksum_obj.md5 == "37c4b87edffc5d198ff5a185cee7ee09"
    assert checksum_obj.crc32 == "6d93c138"
