"""Sugary functions."""

import io
import sys

from hbcore import calc, fcalc
from hbdictionary import PATTERN, TEXT
from hbhelper import myprint


def calculate(function, infile, quiet=False):
    """Calculate the digest of a file.

    function: A string giving the name of the hash function.
    infile: A string giving the name or path of the file to be hashed.
    quiet: Output verbosity.

    Prints the digest of a given file in "HASH_TYPE (FILE) = DIGEST" format
    (excluding the quotes).  An error is printed if the file cannot be accessed.
    Quiet mode will output only the digest.
    """
    error, result = fcalc(function, infile)
    if error:
        myprint(function, infile, result, error=True)
    elif quiet:
        print(result)
    else:
        myprint(function, infile, result)


def dupe(function, infile1, infile2, quiet=False):
    """Check to see if two files are the same.

    function: A string giving the name of the hash function.
    infile1: A string giving the name or path of the file to be hashed.
    infile2: A string giving the name or path of the file to be hashed.
    quiet: Output verbosity.

    Prints the digest of the given files followed by a True or False, with True
    indicating the files are the same.  Quiet mode only outputs True or False.
    If either of the files cannot be accessed, an error is printed and no True
    or False answer is given.
    """
    error1, result1 = fcalc(function, infile1)
    error2, result2 = fcalc(function, infile2)
    if error1:
        myprint(function, infile1, result1, error=True)
    if error2:
        myprint(function, infile2, result2, error=True)
    if not error1 and not error2:
        if quiet:
            print(result1 == result2)
        else:
            myprint(function, infile1, result1)
            myprint(function, infile2, result2)
            print(result1 == result2)


def inline(function, infile, digest, quiet=False):
    """Compare the digest of a file against a given digest.

    function: A string giving the name of the hash function.
    infile: A string giving the name or path of the file to be hashed.
    digest: A string giving the file's digest.
    quiet: Output verbosity.

    Prints whether the file is good or bad by calculating its digest and
    comparing it to the given digest.  Quiet mode will only output errors and
    files with digests that do not match.
    """
    error, result = fcalc(function, infile)
    if error:
        myprint(function, infile, result, error=True)
    elif result.lower() != digest.lower():
        myprint(function, infile, TEXT["bad"])
    elif not quiet:
        myprint(function, infile, TEXT["good"])


def standard_input(function, quiet=False):
    """Calculate the digest of stdin.

    function: A string giving the name of the hash function.
    quiet: Output verbosity.

    Prints the digest of standard input in "HASH_TYPE (-) = DIGEST" format
    (excluding the quotes).  Quiet mode will output only the digest.
    """
    result = calc(function, io.BytesIO(bytes(sys.stdin.read(), "utf8")))
    if quiet:
        print(result)
    else:
        myprint(function, '-', result)


def string(function, string, quiet=False):
    """Calculate the digest of a string.

    function: A string giving the name of the hash function.
    string: The text to be hashed.
    quiet: Output verbosity.

    Prints the digest of the given string in "HASH_TYPE ("STRING") = DIGEST"
    format (excluding the outer quotes, and including the inner quotes).  Quiet
    mode will output only the digest.
    """
    result = calc(function, io.BytesIO(bytes(string, "utf8")))
    if quiet:
        print(result)
    else:
        myprint(function, '"' + string + '"', result)


def check(infile, quiet=False):
    """Compare the digest of a file against one found in a text file.

    infile: A string giving the name or path of the text file to be opened.
    quiet: Output verbosity.

    Prints whether the file is good or bad by comparing its digest with the
    digest found in the text file.  Quiet mode will only output errors and files
    with digests that do not match.

    The digest file should contain digests in the "HASH_TYPE (FILE) = DIGEST"
    format (excluding the quotes).  More than one HASH_TYPE can exist in the
    same file.

    Note: This function depends on the level-1 inline() function.

    Sample Digest File:
    CRC32 (file.txt) = 3F7B8CCE
    MD5 (file.txt) = b3e1ed9facbabeba3d7cb1a69167a529
    SHA1 (file.txt) = bbee0ae3860ab0f8fe99fdb87f3c8a4e9c5dc175
    """
    try:
        check_file = open(infile, "r")
    except IOError as err:
        myprint("CHECK", infile, err.strerror, error=True)
    else:
        for line in check_file:
            line = PATTERN["dfile"].search(line)
            if line is not None:
                function = line.group(1).lower()
                path = line.group(2)
                digest = line.group(3)
                if path[0] == '"' and path[len(path) - 1] == '"':
                    myprint(function, path,
                        TEXT["good"] if calc(function, path[1:-1]) == digest else TEXT["bad"])
                else:
                    inline(function, path, digest, quiet)
        check_file.close()


def embedded(function, infile, quiet=False):
    """Compare the digest of a file against the digest in its filename.

    function: A string giving the name of the hash function.
    infile: A string giving the name or path of the file to be hashed.
    quiet: Output verbosity.

    Prints whether the file is good or bad by calculating its digest and
    comparing it to the one found in its filename.  Quiet mode will only output
    errors and files with digests that do not match.

    Note: This function depends on the level-1 inline() function.
    """
    pattern = PATTERN[function]
    digest = pattern.search(infile)
    if digest:
        inline(function, infile, digest.group(0), quiet)
    else:
        myprint(function, infile, TEXT["missing"])
