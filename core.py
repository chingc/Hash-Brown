"""Primary functions."""

import hashlib
import os.path
import re

import wrapper


algorithm = {}
algorithm["adler32"] = wrapper.adler32
algorithm["crc32"]   = wrapper.crc32
algorithm["md5"]     = hashlib.md5
algorithm["sha1"]    = hashlib.sha1
algorithm["sha224"]  = hashlib.sha224
algorithm["sha256"]  = hashlib.sha256
algorithm["sha384"]  = hashlib.sha384
algorithm["sha512"]  = hashlib.sha512

pattern = {}
pattern["adler32"] = r"[0-9A-Fa-f]{8}"    # 32 bit
pattern["crc32"]   = r"[0-9A-Fa-f]{8}"    # 32 bit
pattern["md5"]     = r"[0-9A-Fa-f]{32}"   # 128 bit
pattern["sha1"]    = r"[0-9A-Fa-f]{40}"   # 160 bit
pattern["sha224"]  = r"[0-9A-Fa-f]{56}"   # 224 bit
pattern["sha256"]  = r"[0-9A-Fa-f]{64}"   # 256 bit
pattern["sha384"]  = r"[0-9A-Fa-f]{96}"   # 384 bit
pattern["sha512"]  = r"[0-9A-Fa-f]{128}"  # 512 bit


def calculate(name, data):
    """Calculate a digest or checksum.

    Arguments:
    name -- The name of the hash function.
    data -- Bytes or a file path.

    Returns:
    A digest or checksum in hexadecimal.

    """
    result = algorithm[name]()
    if isinstance(data, bytes):
        result.update(data)
    elif isinstance(data, str):
        with open(data, "rb") as data:
            for piece in data: result.update(piece)
    else:
        raise ValueError("Argument must be of type bytes or str")
    return result.hexdigest()


def match(name, data, digest=None):
    """Determine whether a digest or checksum matches the data.

    Arguments:
    name -- The name of the hash function.
    data -- Bytes or a file path.
    digest -- A digest or checksum.

    Returns:
    True if the given digest or checksum matches the data, otherwise false.

    Notes:
    If no digest or checksum is given the filename will be checked for one.

    """
    def extract(data):
        return re.compile(pattern[name]).search(os.path.basename(data)).group(0)

    def valid(digest):
        return True if re.compile(r"^" + pattern[name] + r"$").match(digest) else False

    if not digest:
        try: digest = extract(data)
        except: raise ValueError("No digest or checksum found to match against")
    if not isinstance(digest, str) or not valid(digest):
        raise ValueError("Invalid digest or checksum")
    return digest.lower() == calculate(name, data)
