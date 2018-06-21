"""A hashlib-like user interface for zlib."""

import zlib


class Adapter:
    def __init__(self, algo: str) -> None:
        self.checksum = 0
        if algo == "adler32":
            self.algo = zlib.adler32
        elif algo == "crc32":
            self.algo = zlib.crc32
        else:
            raise ValueError(f"Unsupported type: '{algo}'")

    def update(self, data: bytes) -> None:
        self.checksum = self.algo(data, self.checksum)

    def hexdigest(self) -> str:
        return hex(self.checksum)[2:].zfill(8)
