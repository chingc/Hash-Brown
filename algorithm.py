"""Hashing algorithms and digest patterns."""

import hashlib
import re

from hbzlib import adler32, crc32


# the dictionary values are basically constructor functions, they
# must be called in order to instantiate the desired hash object.
# e.g. algorithm_for["sha1"]() will create a sha1 hash object.

algorithm_for = {}
algorithm_for["md5"] = hashlib.md5
algorithm_for["sha1"] = hashlib.sha1
algorithm_for["sha224"] = hashlib.sha224
algorithm_for["sha256"] = hashlib.sha256
algorithm_for["sha384"] = hashlib.sha384
algorithm_for["sha512"] = hashlib.sha512
algorithm_for["adler32"] = adler32
algorithm_for["crc32"] = crc32


regex_for = {}
regex_for["md5"] = re.compile(r"[0-9A-Fa-f]{32}")      # 128 bit
regex_for["sha1"] = re.compile(r"[0-9A-Fa-f]{40}")     # 160 bit
regex_for["sha224"] = re.compile(r"[0-9A-Fa-f]{56}")   # 224 bit
regex_for["sha256"] = re.compile(r"[0-9A-Fa-f]{64}")   # 256 bit
regex_for["sha384"] = re.compile(r"[0-9A-Fa-f]{96}")   # 384 bit
regex_for["sha512"] = re.compile(r"[0-9A-Fa-f]{128}")  # 512 bit
regex_for["adler32"] = re.compile(r"[0-9A-Fa-f]{8}")   # 32 bit
regex_for["crc32"] = re.compile(r"[0-9A-Fa-f]{8}")     # 32 bit
regex_for["checklist"] = re.compile(r"^(\w+) \((.+)\) = ([0-9A-Fa-f]+)")
