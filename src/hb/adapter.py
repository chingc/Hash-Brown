"""A hashlib-like user interface for zlib."""

import zlib


class Adapter:
    """Use zlib like hashlib."""

    def __init__(self, algo: str) -> None:
        if algo == "adler32":
            self.algo = zlib.adler32
            self.checksum = 1
        elif algo == "crc32":
            self.algo = zlib.crc32
            self.checksum = 0
        else:
            raise ValueError(f"Unsupported type: '{algo}'")

    def update(self, data: bytes) -> None:
        """Compute a running checksum."""
        self.checksum = self.algo(data, self.checksum)

    def hexdigest(self) -> str:
        """The checksum in hexadecimal."""
        return hex(self.checksum)[2:].zfill(8)
