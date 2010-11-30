"""A wrapper class to make zlib calls consistent with hashlib calls."""

import zlib


class _hbzlib:
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.checksum = self.function(b"", 0)

    def update(self, bytes):
        self.checksum = self.function(bytes, self.checksum)

    def digest(self):
        return self.checksum

    def hexdigest(self):
        return hex(self.checksum)[2:].zfill(8)

    def copy(self):
        clone = _ZLib(self.name, self.function)
        clone.checksum = self.checksum
        return clone


def adler32():
    """Instantiates a hashlib-like object that uses adler32."""
    return _hbzlib("adler32", zlib.adler32)


def crc32():
    """Instantiates a hashlib-like object that uses crc32."""
    return _hbzlib("crc32", zlib.crc32)
