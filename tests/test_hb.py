"""Tests"""

from typing import Tuple

# def test_parse(get_file: Callable[[str], str]) -> None:
#     for algo, path, digest in parse(get_file("checksum_good.txt")):
#         assert algo == "md5"
#         assert path == "test.txt"
#         assert digest == "c08420f4c716f3814c268dd845356276"

#     for bad in [1, 2, 3, 4]:
#         with pytest.raises(ValueError):
#             for algo, path, digest in parse(get_file(f"checksum_bad_0{bad}.txt")): pass

def test_supported(supported: Tuple[str]) -> None:
    assert supported == ("blake2b", "blake2s", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "adler32", "crc32")

def test_blake2b(blake2b: str) -> None:
    assert blake2b == "1e5bbd57cc8fcdea22e4155f43672f3f3e655295c21a15405d1844b4be90cced030064a57e231b989b85db4a8a9e47accbd60be95608e52203da27b7cb18c85e"

def test_blake2s(blake2s: str) -> None:
    assert blake2s == "462b84b6ed0c29b302c4f0207f2b344a8c1ade6b5d5ff8a326fc681681a35899"

def test_md5(md5: str) -> None:
    assert md5 == "f2789658fd0737100f4dd1fac58c08e9"

def test_sha1(sha1: str) -> None:
    assert sha1 == "5aaf0a05ace3134ac1dc48004c0eacd9003eff5d"

def test_sha224(sha224: str) -> None:
    assert sha224 == "6338d3bc74dbbb5048cc2511db3bb639d4666d431574ca1c47ba021d"

def test_sha256(sha256: str) -> None:
    assert sha256 == "22f54567ed79dcf2423e7202a02482ce1406e42152e158ba8e0f44c6bbc6eaf9"

def test_sha384(sha384: str) -> None:
    assert sha384 == "de3c836b44e17e878ee3461a6d3d86abd037b6b9cc806e66ca30b5a14302bce48668dc2b68bc3a2f2b0fdb52d91a7483"

def test_sha512(sha512: str) -> None:
    assert sha512 == "b62a16f71f55b7baf52a4074238f85dc9543eb11a04b8d568fac299a9aec36f3b63b9b03b2101a5988ed51f8080d17f55726a1a06b5330040c94f4fa455f13a7"

def test_adler32(adler32: str) -> None:
    assert adler32 == "7bb40ff1"

def test_crc32(crc32: str) -> None:
    assert crc32 == "55f9bb0b"
