"""Dictionaries."""

import hashlib
import re

import hbzlib


HASH = {}
HASH["md5"] = hashlib.md5
HASH["sha1"] = hashlib.sha1
HASH["sha224"] = hashlib.sha224
HASH["sha256"] = hashlib.sha256
HASH["sha384"] = hashlib.sha384
HASH["sha512"] = hashlib.sha512
HASH["adler32"] = hbzlib.adler32
HASH["crc32"] = hbzlib.crc32

PATTERN = {}
PATTERN["md5"] = re.compile(r"[0-9A-Fa-f]{32}")        # 128 bit
PATTERN["sha1"] = re.compile(r"[0-9A-Fa-f]{40}")       # 160 bit
PATTERN["sha224"] = re.compile(r"[0-9A-Fa-f]{56}")     # 224 bit
PATTERN["sha256"] = re.compile(r"[0-9A-Fa-f]{64}")     # 256 bit
PATTERN["sha384"] = re.compile(r"[0-9A-Fa-f]{96}")     # 384 bit
PATTERN["sha512"] = re.compile(r"[0-9A-Fa-f]{128}")    # 512 bit
PATTERN["adler32"] = re.compile(r"[0-9A-Fa-f]{8}")     # 32 bit
PATTERN["crc32"] = re.compile(r"[0-9A-Fa-f]{8}")       # 32 bit
PATTERN["dfile"] = re.compile(r"^(\w+) \((.+)\) = ([0-9A-Fa-f]+)")    # digest file

TEXT = {}
TEXT["unsupported"] = "Unsupported hash type"
TEXT["missing"] = "Digest not found"
TEXT["good"] = "Good"
TEXT["bad"] = "Bad"
