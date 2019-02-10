"""Tests"""

from typing import List

from pytest import raises

from hb.main import Checksum


def test_supported(supported: List[str]) -> None:
    assert Checksum.SUPPORTED == tuple(supported)

def test_unsupported() -> None:
    with raises(ValueError):
        Checksum(".").compute("unsupported")

# def test_version(version: str) -> None:
#     assert Checksum.VERSION == version

def test_parse_success(good_checklists: List[str]) -> None:
    for checklist in good_checklists:
        for algorithm, path, checksum in Checksum.parse(checklist):
            assert algorithm == "md5"
            assert path == "test.txt"
            assert checksum == "c08420f4c716f3814c268dd845356276"

def test_parse_failure(bad_checklists: List[str]) -> None:
    for checklist in bad_checklists:
        with raises(ValueError):
            Checksum.parse(checklist)

def test_print() -> None:
    assert Checksum.print("a", "b", "c") == "a (b) = c"

def test_path_property(fox: Checksum) -> None:
    assert fox.md5 == "0d7006cd055e94cf614587e1d2ae0c8e"
    assert fox.path != "abc"
    assert "md5" in fox.checksums

    fox.path = "abc"
    assert fox.path == "abc"
    assert not fox.checksums

def test_blake2b(fox: Checksum) -> None:
    assert fox.blake2b == "91b27f225ee86f26ef2103de210fd19e7e9f6cb3d10f204a6ad359d90abbd5f06425dc9dc801a035d86d6dff977a69b5922a2d22a143ed8d63f026bb875009ec"

def test_blake2s(fox: Checksum) -> None:
    assert fox.blake2s == "8c580d37bdb44575570c971f29b4e8fa25346a105b959880260cdb6946f4d983"

def test_md5(fox: Checksum) -> None:
    assert fox.md5 == "0d7006cd055e94cf614587e1d2ae0c8e"

def test_sha1(fox: Checksum) -> None:
    assert fox.sha1 == "9c04cd6372077e9b11f70ca111c9807dc7137e4b"

def test_sha224(fox: Checksum) -> None:
    assert fox.sha224 == "e88799b0d0d5becc6791837fa95388d4056f1250a511d14829766663"

def test_sha256(fox: Checksum) -> None:
    assert fox.sha256 == "b47cc0f104b62d4c7c30bcd68fd8e67613e287dc4ad8c310ef10cbadea9c4380"

def test_sha384(fox: Checksum) -> None:
    assert fox.sha384 == "d51d28d0141e56f692952ea14861898e2b417b922831e0f4bcdbc326a7fe1e9d9563182e83d3a8af66f68536e0d42b88"

def test_sha512(fox: Checksum) -> None:
    assert fox.sha512 == "020da0f4d8a4c8bfbc98274027740061d7df52ee07091ed6595a083e0f45327bbe59424312d86f218b74ed2e25507abaf5c7a5fcf4cafcf9538b705808fd55ec"

def test_adler32(fox: Checksum) -> None:
    assert fox.adler32 == "7bf61012"

def test_crc32(fox: Checksum) -> None:
    assert fox.crc32 == "eb50cc6a"

def test_memoization(mocker, fox: Checksum) -> None:
    mocker.spy(fox, 'get')
    mocker.spy(fox, 'compute')

    assert fox.md5 == "0d7006cd055e94cf614587e1d2ae0c8e"
    assert fox.md5 == "0d7006cd055e94cf614587e1d2ae0c8e"
    assert fox.get.call_count == 2
    assert fox.compute.call_count == 1

    assert fox.crc32 == "eb50cc6a"
    assert fox.crc32 == "eb50cc6a"
    assert fox.get.call_count == 4
    assert fox.compute.call_count == 2
