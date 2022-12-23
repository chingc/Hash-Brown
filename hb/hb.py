"""hb.py"""

from contextlib import contextmanager
from pathlib import Path
from threading import Thread
from typing import Generator
import hashlib
import os
import re
import sys
import time
import zlib


class HashBrown:
    """Hash Brown"""

    def __init__(self, algo, path) -> None:
        self.algo = algo.lower()
        self.filesize = os.path.getsize(path)
        self.hexdigest = ""
        self.path = Path(path)
        self.tell = 0

    @contextmanager
    def open(self) -> Generator:
        """File open with progress tracker."""

        def _progress() -> None:
            while self.tell != self.filesize:
                print(
                    f"{self.tell / self.filesize:.3%} {self.algo} {self.path}",
                    end="\r",
                    file=sys.stderr,
                )
                time.sleep(0.5)

        Thread(target=_progress).start()
        with open(self.path, mode="rb") as lines:
            yield lines

    def compute(self) -> str:
        """Compute the hexdigest."""
        if self.hexdigest:
            return self.hexdigest

        match self.algo:
            case "adler32":
                checksum = 1
                with self.open() as lines:
                    for line in lines:
                        checksum = zlib.adler32(line, checksum)
                        self.tell = lines.tell()
                self.hexdigest = hex(checksum).removeprefix("0x").zfill(8)
            case "crc32":
                checksum = 0
                with self.open() as lines:
                    for line in lines:
                        checksum = zlib.crc32(line, checksum)
                        self.tell = lines.tell()
                self.hexdigest = hex(checksum).removeprefix("0x").zfill(8)
            case _:
                digest = hashlib.new(self.algo)
                with self.open() as lines:
                    for line in lines:
                        digest.update(line)
                        self.tell = lines.tell()
                if self.algo.startswith("shake_"):
                    self.hexdigest = digest.hexdigest(64)  # type: ignore
                else:
                    self.hexdigest = digest.hexdigest()

        self.tell = self.filesize
        return self.hexdigest

    def pprint(self) -> str:
        """Pretty print the hexdigest."""
        return f"{self.compute()} {self.algo} {self.path}"


def compute(algo: str, path: str) -> str:
    """Convenience function to compute and pprint."""
    return HashBrown(algo, path).pprint()


def scan(path: str) -> None:
    """Scan a file of hexdigests to check if they match."""
    with open(Path(path), encoding="utf-8") as lines:
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):  # skip blank lines and comments
                continue
            if match := re.match(r"^([0-9A-Fa-f]+) (\w+) (.+)$", line):
                given, algo, path = match.group(1, 2, 3)
                computed = HashBrown(algo, path).compute()
                print(f"{'OK' if computed == given else 'BAD'} {algo} {path}")
            else:
                print(f"\nUnable to read line {i}: '{line}'\n")
