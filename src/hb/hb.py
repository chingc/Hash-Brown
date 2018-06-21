"""Hash Brown"""

import hashlib

from threading import Thread
from time import sleep
from typing import IO, Tuple, Any

from adapter import Adapter


HASHLIBS = sorted([h for h in hashlib.algorithms_guaranteed if "shake" not in h and "_" not in h])
ZLIBS = ["adler32", "crc32"]


def _progress(file: IO) -> None:
    """Display hashing progress.

    file -- an open file handle
    """
    fsize, _ = file.seek(0, 2), file.seek(0)
    while not file.closed:
        print(f"{round(file.tell() / fsize * 100)}%", end="\r")
        sleep(0.5)

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
            Thread(target=_progress, args=(file,)).start()
        for line in file:
            result.update(line)
    return str(result.hexdigest())

def parse(line: str) -> Tuple[str, str, str]:
    """Parse a line from the checklist file.

    line -- a line from the checklist file
    """
    algo, path, _, digest = line.strip().split(" ")
    return (algo, path[1:-1], digest)
