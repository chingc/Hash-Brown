"""Primary functions."""

import io
import os.path
import sys

import algorithm
import check
import track


def _to_stdout(a, b, c):
    """Print to standard output."""
    print("{} ({}) = {}".format(a.upper(), b, c))


def _to_stderr(a, b, c):
    """Print to standard error."""
    print("{} ({}) = {}".format(a.upper(), b, c), file=sys.stderr)


def _calc(name, path):
    """Calculate the digest or checksum of a file.

    Arguments:
    name -- the name of the algorithm
    path -- absolute or relative file path

    Returns:
    a digest or checksum in hexadecimal

    """
    with open(path, "rb") as data:
        if os.path.getsize(path) > track.threshold():
            track.progress(data)
        return algorithm.get(name)(data)


def _str(name, string):
    """Calculate the digest or checksum of a string.

    Arguments:
    name -- the name of the algorithm
    string -- a string

    Returns:
    a digest or checksum in hexadecimal

    Notes:
    All strings are treated as UTF-8.

    """
    return algorithm.get(name)(io.BytesIO(bytes(string, "utf_8")))


def checklist(infile):
    """Check a checklist.

    Arguments:
    infile -- the checklist

    Notes:
    Refer to the README for checklist format.

    """
    problem = check.path(infile)
    if problem is not None:
        _to_stderr("CHECK", infile, problem)
        return
    with open(infile, "rb") as infile:
        for line in infile:
            info = algorithm.pattern("checklist").search(line.decode("utf_8"))
            if info is not None:
                name = info.group(1).lower()
                path = info.group(2)
                given = info.group(3)
                if path.startswith('"') and path.endswith('"'):
                    _to_stdout(name, path, given == _str(name, path[1:-1]))
                else:
                    problem = check.path(path)
                    if problem is None:
                        _to_stdout(name, path, given == _calc(name, path))
                    else:
                        _to_stderr(name, path, problem)


def default(name, path):
    """Print the digest or checksum of a file.

    Arguments:
    name -- the name of the algorithm
    path -- absolute or relative file path

    """
    problem = check.path(path)
    if problem is None:
        _to_stdout(name, path, _calc(name, path))
    else:
        _to_stderr(name, path, problem)


def dupe(name, path1, path2):
    """Determine whether two files are identical.

    Arguments:
    name -- the name of the algorithm
    path1 -- absolute or relative file path
    path2 -- absolute or relative file path

    """
    problem1 = check.path(path1)
    problem2 = check.path(path2)
    if problem1 is None and problem2 is None:
        result1 = _calc(name, path1)
        _to_stdout(name, path1, result1)
        result2 = _calc(name, path2) if path1 != path2 else result1
        _to_stdout(name, path2, result2)
        print(result1 == result2)
    else:
        if problem1 is not None:
            _to_stderr(name, path1, problem1)
        if problem2 is not None:
            _to_stderr(name, path2, problem2)


def embedded(name, path):
    """Determine whether the digest or checksum in a filename is the actual.

    Arguments:
    name -- the name of the algorithm
    path -- absolute or relative file path

    """
    problem = check.path(path)
    if problem is None:
        given = algorithm.pattern(name).search(os.path.basename(path))
        if given is not None:
            _to_stdout(name, path, given.group(0).lower() == _calc(name, path))
        else:
            _to_stderr(name, path, "No digest or checksum found")
    else:
        _to_stderr(name, path, problem)


def inline(name, path, given):
    """Determine whether the given digest or checksum for a file is the actual.

    Arguments:
    name -- the name of the algorithm
    path -- absolute or relative file path
    given -- a digest or checksum

    """
    problem = check.path(path)
    if problem is None:
        _to_stdout(name, path, given.lower() == _calc(name, path))
    else:
        _to_stderr(name, path, problem)


def string(name, string):
    """Print the digest or checksum of a string.

    Arguments:
    name -- the name of the algorithm
    string -- a string

    Notes:
    All strings are treated as UTF-8.

    """
    _to_stdout(name, '"' + string + '"', _str(name, string))
