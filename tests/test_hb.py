"""Tests"""

from typing import Callable

import pytest

from hb.adapter import Adapter
from hb.main import compute, parse


def test_adapter(get_file: Callable[[str], str]) -> None:
    assert compute("adler32", get_file("0ada12d6.txt")) == "0ada12d6"
    assert compute("crc32", get_file("4a2e4fa3.txt")) == "4a2e4fa3"

    with pytest.raises(ValueError):
        Adapter("nonexistent")

def test_compute(get_file: Callable[[str], str]) -> None:
    assert compute("md5", get_file("a97e741e7b0a63dfb156fa8bf372736c.txt"), True) == "a97e741e7b0a63dfb156fa8bf372736c"

    with pytest.raises(ValueError):
        compute("nonexistent", "")

    with pytest.raises(FileNotFoundError):
        compute("md5", "")

def test_parse(get_file: Callable[[str], str]) -> None:
    for algo, path, digest in parse(get_file("checksum_good.txt")):
        assert algo == "md5"
        assert path == "test.txt"
        assert digest == "c08420f4c716f3814c268dd845356276"

    for bad in [1, 2, 3, 4]:
        with pytest.raises(ValueError):
            for algo, path, digest in parse(get_file(f"checksum_bad_0{bad}.txt")): pass
