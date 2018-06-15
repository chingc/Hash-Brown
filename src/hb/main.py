"""Primary logic."""

import hashlib

from threading import Thread
from time import sleep

from adapter import Adapter


HASHLIB_NAMES = [name for name in hashlib.algorithms_guaranteed if "shake" not in name]
ZLIB_NAMES = ["adler32", "crc32"]

def _progress(f):
    """Display hashing progress.

    f: file -- an open file handle
    """
    fsize, _ = f.seek(0, 2), f.seek(0)
    while not f.closed:
        print(f"{round(f.tell() / fsize * 100)}%", end="\r")
        sleep(0.5)

def compute(name, path, show_progress=False):
    """Compute the file hash.

    name: str -- hashing algorithm name
    path: str -- file path
    show_progress: bool -- show progress meter (default: False)
    """
    name = name.lower()
    if name in HASHLIB_NAMES:
        result = hashlib.new(name)
    elif name in ZLIB_NAMES:
        result = Adapter(name)
    else:
        raise ValueError(f"Unsupported hash type: '{name}'")
    with open(path, "rb") as f:
        if show_progress:
            Thread(target=_progress, args=(f,)).start()
        for line in f:
            result.update(line)
    return result.hexdigest()

def parse(line):
    """Parse a line from the checklist file.

    line: str -- a line from the checklist file
    """
    name, path, _, digest = line.strip().split(" ")
    return (name, path[1:-1], digest)
