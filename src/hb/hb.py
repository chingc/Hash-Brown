"""Hash Brown"""

import hashlib

from threading import Thread
from time import sleep
from typing import IO, Tuple, Any

from hb.adapter import Adapter


HASHLIB_ALGOS = [algo for algo in hashlib.algorithms_guaranteed if "shake" not in algo]
ZLIB_ALGOS = ["adler32", "crc32"]


def _progress(file_: IO) -> None:
    """Display hashing progress.

    f -- an open file handle
    """
    fsize, _ = file_.seek(0, 2), file_.seek(0)
    while not file_.closed:
        print(f"{round(file_.tell() / fsize * 100)}%", end="\r")
        sleep(0.5)

def compute(algo: str, path: str, show_progress: bool = False) -> str:
    """Compute the file hash.

    algo -- hash algorithm name
    path -- file path
    show_progress -- show progress meter (default: False)
    """
    algo = algo.lower()
    result: Any
    if algo in HASHLIB_ALGOS:
        result = hashlib.new(algo)
    elif algo in ZLIB_ALGOS:
        result = Adapter(algo)
    else:
        raise ValueError(f"Unsupported type: '{algo}'")
    with open(path, "rb") as file_:
        if show_progress:
            Thread(target=_progress, args=(file_,)).start()
        for line in file_:
            result.update(line)
    return str(result.hexdigest())

def parse(line: str) -> Tuple[str, str, str]:
    """Parse a line from the checklist file.

    line -- a line from the checklist file
    """
    name, path, _, digest = line.strip().split(" ")
    return (name, path[1:-1], digest)
