"""Wraps zlib in a class to provide a hashlib-like usage interface."""

import zlib


class _Wrapper:
    def __init__(self, name):
        self.checksum = 0
        if name == "adler32":
            self.algorithm = zlib.adler32
        elif name == "crc32":
            self.algorithm = zlib.crc32
        else:
            raise ValueError("Unsupported checksum function: '{}'".format(name))

    def update(self, data):
        self.checksum = self.algorithm(data, self.checksum)

    def hexdigest(self):
        return hex(self.checksum)[2:].zfill(8)


def adler32():
    """Convenience function to construct a wrapper around adler32."""
    return _Wrapper("adler32")


def crc32():
    """Convenience function to construct a wrapper around crc32."""
    return _Wrapper("crc32")
