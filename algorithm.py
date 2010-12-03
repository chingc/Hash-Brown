"""Algorithms and regex patterns for various digests and checksums."""

import hashlib
import re
import zlib


def names():
    """A list of supported algorithms."""
    return ["md5", "sha1", "sha224", "sha256",
    "sha384", "sha512", "adler32", "crc32"]


def get(name):
    """Retrieve a function that calculates a digest or checksum.

    Arguments:
    name -- the name of the algorithm

    Raises:
    LookupError -- if the name given is unsupported

    Returns:
    a function

    """
    if name == "md5":
        return md5
    if name == "sha1":
        return sha1
    if name == "sha224":
        return sha224
    if name == "sha256":
        return sha256
    if name == "sha384":
        return sha384
    if name == "sha512":
        return sha512
    if name == "adler32":
        return adler32
    if name == "crc32":
        return crc32
    raise LookupError("Unsupported algorithm")


def pattern(name):
    """Retrieve a regex pattern for a digest or checksum.

    Arguments:
    name -- the name of the algorithm

    Raises:
    LookupError -- if the name given is unsupported

    Returns:
    a pattern

    """
    if name == "md5":
        return re.compile(r"[0-9A-Fa-f]{32}")   # 128 bit
    if name == "sha1":
        return re.compile(r"[0-9A-Fa-f]{40}")   # 160 bit
    if name == "sha224":
        return re.compile(r"[0-9A-Fa-f]{56}")   # 224 bit
    if name == "sha256":
        return re.compile(r"[0-9A-Fa-f]{64}")   # 256 bit
    if name == "sha384":
        return re.compile(r"[0-9A-Fa-f]{96}")   # 384 bit
    if name == "sha512":
        return re.compile(r"[0-9A-Fa-f]{128}")  # 512 bit
    if name == "adler32":
        return re.compile(r"[0-9A-Fa-f]{8}")    # 32 bit
    if name == "crc32":
        return re.compile(r"[0-9A-Fa-f]{8}")    # 32 bit
    if name == "checklist":
        return re.compile(r"(\w+) \((.+)\) = ([0-9A-Fa-f]+)")
    raise LookupError("Unsupported pattern")


def _hashlib(hashlib_object, data):
    """Calculate a digest using the hashlib module.

    Arguments:
    hashlib_object -- a hash object from the hashlib module
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    for info in data:
        hashlib_object.update(info)
    return hashlib_object.hexdigest()


def _zlib(zlib_function, data):
    """Calculate a checksum using the zlib module.

    Arguments:
    zlib_function -- the adler32 or crc32 function from the zlib module
    data -- an object conforming to the buffer interface

    Returns:
    the checksum in hexadecimal

    """
    checksum = 0
    for info in data:
        checksum = zlib_function(info, checksum)
    return hex(checksum)[2:].zfill(8)


def md5(data):
    """Calculate a digest using MD5.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.md5(), data)


def sha1(data):
    """Calculate a digest using SHA-1.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.sha1(), data)


def sha224(data):
    """Calculate a digest using SHA-224.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.sha224(), data)


def sha256(data):
    """Calculate a digest using SHA-256.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.sha256(), data)


def sha384(data):
    """Calculate a digest using SHA-384.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.sha384(), data)


def sha512(data):
    """Calculate a digest using SHA-512.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the digest in hexadecimal

    """
    return _hashlib(hashlib.sha512(), data)


def adler32(data):
    """Calculate a checksum using Adler-32.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the checksum in hexadecimal

    """
    return _zlib(zlib.adler32, data)


def crc32(data):
    """Calculate a checksum using CRC-32.

    Arguments:
    data -- an object conforming to the buffer interface

    Returns:
    the checksum in hexadecimal

    """
    return _zlib(zlib.crc32, data)
