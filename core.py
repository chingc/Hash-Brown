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
pattern["checklist"] = r"(\w+) \((.+)\) = ([0-9A-Fa-f]+)"  # checklist file pattern
pattern["adler32"]   = r"[0-9A-Fa-f]{8}"    # 32 bit
pattern["crc32"]     = r"[0-9A-Fa-f]{8}"    # 32 bit
pattern["md5"]       = r"[0-9A-Fa-f]{32}"   # 128 bit
pattern["sha1"]      = r"[0-9A-Fa-f]{40}"   # 160 bit
pattern["sha224"]    = r"[0-9A-Fa-f]{56}"   # 224 bit
pattern["sha256"]    = r"[0-9A-Fa-f]{64}"   # 256 bit
pattern["sha384"]    = r"[0-9A-Fa-f]{96}"   # 384 bit
pattern["sha512"]    = r"[0-9A-Fa-f]{128}"  # 512 bit


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
    def extract(filename):
        return re.search(pattern[name], filename).group(0)

    def valid(digest):
        return True if re.match(r"^" + pattern[name] + r"$", digest) else False

    if not digest:
        filename = os.path.basename(data)
        try: digest = extract(filename)
        except: raise ValueError("Unable to find {}: '{}'".format(name.upper(), filename))
    if not isinstance(digest, str) or not valid(digest):
        raise ValueError("Invalid digest or checksum: '{}'".format(digest))
    return digest.lower() == calculate(name, data)


def parse(checklist):
    """Reads a checklist.

    Arguments:
    name -- A checklist.

    Returns:
    A list of tuples in the form (HASH_NAME, DATA, DIGEST).

    Notes:
    A checklist is a plain text file with lines like this:
    CRC32 (document.txt) = ad0c2001
    CRC32 (photo.png) = 1629491b
    MD5 (audio.flac) = 69afdf17b98ed394964f15ab497e12d2
    SHA1 (video.mkv) = 1f09d30c707d53f3d16c530dd73d70a6ce7596a9
    Comments can be on a line by itself, at the beginning, or the end.
    I am a string.  CRC32 ("hello, world!") = 58988d13  Double quote me!

    """
    parsed = []
    with open(checklist, "rb") as checklist:
        for line in checklist:
            found = re.search(pattern["checklist"], line.decode())
            if found:
                name, data, digest = found.groups()
                name = name.lower()
                if data.startswith('"') and data.endswith('"'):
                    data = data[1:-1].encode()
                digest = digest.lower()
                parsed.append((name, data, digest))
    return parsed
