"""Hash Brown"""

import hashlib
import zlib
from dataclasses import dataclass, field
from threading import Thread
from time import sleep
from typing import Dict, IO, List


@dataclass
class Checksum():
    """Compute various secure message digests and checksums.

    Digests, hashes, and checksums will all be referred to as checksum for simplicity.
    """
    file: str = ""
    checksum: Dict[str, str] = field(default_factory=dict)
    show_progress: bool = False
    threshold: int = 1024 * 1024 * 200

    @staticmethod
    def supported() -> List[str]:
        """A list of supported algorithms."""
        return sorted([x for x in hashlib.algorithms_guaranteed if "_" not in x]) + ["adler32", "crc32"]

    def _progress(self, file: IO) -> None:
        def _p(file: IO, fsize: int) -> None:
            while not file.closed:
                print(f"{round(file.tell() / fsize * 100)}%", end="\r")
                sleep(0.2)
        fsize, _ = file.seek(0, 2), file.seek(0)
        if fsize > self.threshold:
            Thread(target=_p, args=(file, fsize)).start()

    def _hashlib_compute(self, name: str) -> str:
        if name in self.checksum:
            return self.checksum[name]
        result = hashlib.new(name)
        with open(self.file, "rb") as file:
            if self.show_progress:
                self._progress(file)
            for line in file:
                result.update(line)
        self.checksum[name] = result.hexdigest()
        return self.checksum[name]

    def _zlib_compute(self, name: str) -> str:
        if name in self.checksum:
            return self.checksum[name]
        if name == "adler32":
            result = 1
            update = zlib.adler32
        elif name == "crc32":
            result = 0
            update = zlib.crc32
        with open(self.file, "rb") as file:
            if self.show_progress:
                self._progress(file)
            for line in file:
                result = update(line, result)
        self.checksum[name] = hex(result)[2:].zfill(8)
        return self.checksum[name]

    def blake2b(self) -> str:
        """Compute a blake2b checksum."""
        return self._hashlib_compute("blake2b")

    def blake2s(self) -> str:
        """Compute a blake2s checksum."""
        return self._hashlib_compute("blake2s")

    def md5(self) -> str:
        """Compute an md5 checksum."""
        return self._hashlib_compute("md5")

    def sha1(self) -> str:
        """Compute a sha1 checksum."""
        return self._hashlib_compute("sha1")

    def sha224(self) -> str:
        """Compute a sha224 checksum."""
        return self._hashlib_compute("sha224")

    def sha256(self) -> str:
        """Compute a sha256 checksum."""
        return self._hashlib_compute("sha256")

    def sha384(self) -> str:
        """Compute a sha384 checksum."""
        return self._hashlib_compute("sha384")

    def sha512(self) -> str:
        """Compute a sha512 checksum."""
        return self._hashlib_compute("sha512")

    def adler32(self) -> str:
        """Compute an adler32 checksum."""
        return self._zlib_compute("adler32")

    def crc32(self) -> str:
        """Compute a crc32 checksum."""
        return self._zlib_compute("crc32")
