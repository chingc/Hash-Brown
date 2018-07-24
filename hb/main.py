"""Hash Brown"""

import hashlib
import re
import zlib
from dataclasses import dataclass, field
from threading import Thread
from time import sleep
from typing import Dict, IO, List, Sequence, Tuple


@dataclass
class Checksum():
    """Compute various checksums.

    Digest, hash, and checksum are all referred to as checksum for simplicity.
    """
    path: str
    checksums: Dict[str, str] = field(default_factory=dict, init=False)
    supported: Tuple = field(default=("blake2b", "blake2s", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "adler32", "crc32"), repr=False, init=False)
    threshold: int = field(default=200, repr=False)

    @staticmethod
    def parse(file: str) -> List[Sequence[str]]:
        """Parse lines from a checksum file."""
        parsed_lines = []
        with open(file, "r") as lines:
            for line in lines:
                line = line.strip()
                if not line or line[0] == "#":  # skip blank lines and comments
                    continue
                match = re.match(r"(\w+)\s?\((.+)\)\s?=\s?(\w+)", line)
                if not match:
                    raise ValueError(f"Bad line in checksum file: '{line}'")
                parsed_lines.append(match.group(1, 2, 3))
        return parsed_lines

    @staticmethod
    def print(algorithm: str, file: str, checksum: str) -> str:
        """BSD style checksum output."""
        return f"{algorithm} ({file}) = {checksum}"

    def _progress(self, file: IO) -> None:
        def _p(file: IO, fsize: int) -> None:
            while not file.closed:
                print(f"{round(file.tell() / fsize * 100)}%", end="\r")
                sleep(0.2)
        fsize, _ = file.seek(0, 2), file.seek(0)
        if fsize > self.threshold * 1024 * 1024:
            Thread(target=_p, args=(file, fsize)).start()

    def _hashlib_compute(self, name: str) -> str:
        result = hashlib.new(name)
        with open(self.path, "rb") as file:
            self._progress(file)
            for line in file:
                result.update(line)
        return result.hexdigest()

    def _zlib_compute(self, name: str) -> str:
        if name == "adler32":
            result = 1
            update = zlib.adler32
        elif name == "crc32":
            result = 0
            update = zlib.crc32
        with open(self.path, "rb") as file:
            self._progress(file)
            for line in file:
                result = update(line, result)
        return hex(result)[2:].zfill(8)

    def compute(self, algorithm: str) -> str:
        """Compute a checksum."""
        if algorithm not in self.supported:
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
