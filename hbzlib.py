"""A wrapper to make zlib calls consistent with hashlib calls."""

import zlib


class _hbzlib():
    def __init__(self, function):
        self.function = function
        self.value = self.function(b"", 0)

    def update(self, arg):
        self.value = self.function(arg, self.value) & 0xffffffff

    def digest(self):
        return self.value

    def hexdigest(self):
        return hex(self.value)[2:].zfill(8)


def adler32():
    return _hbzlib(zlib.adler32)


def crc32():
    return _hbzlib(zlib.crc32)
