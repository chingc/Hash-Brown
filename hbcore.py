"""Core functions of Hash Brown."""

import sys
import threading

from hbdictionary import HASH, TEXT
from hbhelper import myprint


def calc(function, data):
    """Calculate a digest.

    function: A string giving the name of the hash function.
    data: Something that can be interpretable as a buffer of bytes.
    RETURN: The digest of data as a hexidecimal string, or an error message if
        an unsupported hash function is specified.

    NOTE: To get the digest of a string you must wrap it in a bytes buffer.
        e.g. io.BytesIO(bytes(string, "utf8"))
    """
    if function in HASH:
        f = HASH[function]()
        for x in data:
            f.update(x)
        return f.hexdigest()
    else:
        return TEXT["unsupported"]


def fcalc(function, infile, threshold=150*1024**2):
    """Calculate the digest of a file with optional progress monitor.

    function: A string giving the name of the hash function.
    infile: A string giving the name or path of the file to be hashed.
    threshold: Files larger than this value are monitored (default = 150 MBs).
    RETURN: A 2-tuple where the first element is a boolean indicating whether
        or not an error occurred; True on error, False on success.  The second
        element is either an error message or the digest.
    """
    try:
        with open(infile, "rb") as f:
            fsize = (f.seek(0, 2), f.seek(0))[0]
            if 0 <= threshold < fsize:
                def m(event):
                    while not event.is_set():
                        p = "{:.2%}".format(f.tell() / fsize)
                        length = myprint(function, f.name, p, "\r", True)
                        event.wait(0.25)
                        print(" " * length, end="\r", file=sys.stderr)
                e = threading.Event()
                t = threading.Thread(target=m, args=(e,))
                t.start()
                result = calc(function, f)
                e.set()
                t.join()
            else:
                result = calc(function, f)
            return (True if result == TEXT["unsupported"] else False, result)
    except IOError as err:
        return (True, err.strerror)
