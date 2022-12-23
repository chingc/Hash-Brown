"""Hash Brown"""

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


class HashBrown():
    def __init__(self, algo, path) -> None:
        self.algo = algo.lower()
        self.filesize = os.path.getsize(path)
        self.hexdigest = None
        self.path = Path(path)
        self.tell = 0

    @contextmanager
    def open(self) -> Generator:
        """File open with progress tracker."""
        def _progress() -> None:
            while self.tell != self.filesize:
                print("{:.3%} {} {}".format(self.tell / self.filesize, self.algo, self.path), end="\r", file=sys.stderr)
                time.sleep(0.5)

        Thread(target=_progress).start()
        with open(self.path, "rb") as lines:
            yield lines

    def compute(self) -> str:
        """Compute the hexdigest."""
        if self.hexdigest:
            return self.hexdigest

        match self.algo:
            case "adler32":
                result = 1
                with self.open() as lines:
                    for line in lines:
                        result = zlib.adler32(line, result)
                        self.tell = lines.tell()
                self.hexdigest = hex(result).removeprefix('0x').zfill(8)
            case "crc32":
                result = 0
                with self.open() as lines:
                    for line in lines:
                        result = zlib.crc32(line, result)
                        self.tell = lines.tell()
                self.hexdigest = hex(result).removeprefix('0x').zfill(8)
            case _:
                result = hashlib.new(self.algo)
                with self.open() as lines:
                    for line in lines:
                        result.update(line)
                        self.tell = lines.tell()
                self.hexdigest = result.hexdigest()

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
    with open(Path(path)) as lines:
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):  # skip blank lines and comments
                continue
            if match := re.match(r"^([0-9A-Fa-f]+) (\w+) (.+)$", line):
                given_hexdigest, algo, path = match.group(1, 2, 3)
                computed_hexdigest = HashBrown(algo, path).compute()
                print(f"{'OK' if computed_hexdigest == given_hexdigest else 'BAD'} {algo} {path}")
            else:
                print(f"\nUnable to read line {i}: '{line}'\n")
