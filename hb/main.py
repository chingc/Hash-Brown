"""Hash Brown"""

import hashlib
import re
import zlib
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Dict, IO, List, Tuple


class Checksum():
    """Compute various checksums.

    Digest, hash, and checksum are all referred to as checksum for simplicity.
    """
    SUPPORTED = ("blake2b", "blake2s", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "adler32", "crc32")
    VERSION = "1.2.0"

    @staticmethod
    def parse(path: str) -> List[Tuple[str, ...]]:
        """Parse lines from a checksum file."""
        parsed_lines = []
        with Path(path).open("r") as lines:
            for line in lines:
                line = line.strip()
                if not line or line[0] == "#":  # skip blank lines and comments
                    continue
                match = re.match(r"(\w+) \((.+)\) = (\w+)", line)
                if not match:
                    raise ValueError(f"Bad line in checksum file: '{line}'")
                parsed_lines.append(tuple(match.group(1, 2, 3)))
        return parsed_lines

    @staticmethod
    def print(algorithm: str, path: str, checksum: str) -> str:
        """BSD style checksum output."""
        return f"{algorithm} ({Path(path)}) = {checksum}"

    def __init__(self, path: str, threshold: int = 200) -> None:
        self._path = Path(path)
        self.checksums: Dict[str, str] = {}
        self.filesize = self._path.stat().st_size
        self.threshold = threshold

    def _progress(self, file: IO) -> None:
        def _p(file: IO) -> None:
            while not file.closed:
                print(f"{int(file.tell() / self.filesize * 100)}%", end="\r")
                sleep(0.2)
        if self.filesize > self.threshold * 1024 * 1024:
            Thread(target=_p, args=(file,)).start()

    def _hashlib_compute(self, name: str) -> str:
        result = hashlib.new(name)
        with self._path.open("rb") as lines:
            self._progress(lines)
            for line in lines:
                result.update(line)
        return result.hexdigest()

    def _zlib_compute(self, name: str) -> str:
        if name == "adler32":
            result = 1
            update = zlib.adler32
        elif name == "crc32":
            result = 0
            update = zlib.crc32
        with self._path.open("rb") as lines:
            self._progress(lines)
            for line in lines:
                result = update(line, result)
        return hex(result)[2:].zfill(8)

    def compute(self, algorithm: str) -> str:
        """Compute a checksum."""
        if algorithm not in Checksum.SUPPORTED:
            raise ValueError(f"Unsupported algorithm: '{algorithm}'")
        elif algorithm in ["adler32", "crc32"]:
            result = self._zlib_compute(algorithm)
        else:
            result = self._hashlib_compute(algorithm)
        self.checksums[algorithm] = result
        return result

    def get(self, algorithm: str) -> str:
        """Same as `compute` but does not recalculate the checksum if it is already known."""
        if algorithm in self.checksums:
            return self.checksums[algorithm]
        return self.compute(algorithm)

    @property
    def path(self) -> str:
        """The path to calculate."""
        return str(self._path)

    @path.setter
    def path(self, path: str) -> None:
        """Set new path and clear the checksums dictionary."""
        self._path = Path(path)
        self.checksums = {}

    @property
    def blake2b(self) -> str:
        """blake2b"""
        return self.get("blake2b")

    @property
    def blake2s(self) -> str:
        """blake2s"""
        return self.get("blake2s")

    @property
    def md5(self) -> str:
        """md5"""
        return self.get("md5")

    @property
    def sha1(self) -> str:
        """sha1"""
        return self.get("sha1")

    @property
    def sha224(self) -> str:
        """sha224"""
        return self.get("sha224")

    @property
    def sha256(self) -> str:
        """sha256"""
        return self.get("sha256")

    @property
    def sha384(self) -> str:
        """sha384"""
        return self.get("sha384")

    @property
    def sha512(self) -> str:
        """sha512"""
        return self.get("sha512")

    @property
    def adler32(self) -> str:
        """adler32"""
        return self.get("adler32")

    @property
    def crc32(self) -> str:
        """crc32"""
        return self.get("crc32")
