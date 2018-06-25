"""Hash Brown"""

import hashlib

from threading import Thread
from time import sleep
from typing import IO, Tuple, Any

from adapter import Adapter


HASHLIBS = sorted([x for x in hashlib.algorithms_guaranteed if "shake" not in x and "_" not in x])
ZLIBS = ["adler32", "crc32"]


def _progress(file: IO, fsize: int) -> None:
    """Display hashing progress.

    file -- an open file handle
    fsize -- the filesize
    """
    while not file.closed:
        print(f"{round(file.tell() / fsize * 100)}%", end="\r")
        sleep(0.2)

def compute(algo: str, path: str, show_progress: bool = False) -> str:
    """Compute the file hash.

    algo -- hash algorithm name
    path -- file path
    show_progress -- show progress meter (default: False)
    """
    algo = algo.lower()
    result: Any
    if algo in HASHLIBS:
        result = hashlib.new(algo)
    elif algo in ZLIBS:
        result = Adapter(algo)
    else:
        raise ValueError(f"Unsupported type: '{algo}'")
    with open(path, "rb") as file:
        if show_progress:
            fsize, _ = file.seek(0, 2), file.seek(0)
            Thread(target=_progress, args=(file, fsize)).start()
        for line in file:
            result.update(line)
    return str(result.hexdigest())

def parse(line: str) -> Tuple[str, str, str]:
    """Parse a line from the checklist file.

    line -- a line from the checklist file
    """
    algo, path, _, digest = line.strip().split(" ")
    return (algo, path[1:-1], digest)
