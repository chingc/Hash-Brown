"""A hashlib-like user interface for zlib."""

import zlib


class Adapter:
    def __init__(self, name):
        self.checksum = 0
        if name == "adler32":
            self.name = zlib.adler32
        elif name == "crc32":
            self.name = zlib.crc32
        else:
            raise ValueError(f"Unsupported checksum type: '{name}'")

    def update(self, data):
        self.checksum = self.name(data, self.checksum)

    def hexdigest(self):
        return hex(self.checksum)[2:].zfill(8)
