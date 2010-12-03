"""Sanity checks."""

import os
import os.path


def path(path):
    """Perform existence, is-file, and is-readable checks on a given path.

    Arguments:
    path -- the path to check

    Returns:
    "No such file or directory" -- if the path doesn't exist
    "Not a file" -- if the path points to a directory or other such non-file
    "Read access denied" -- if permission is denied or for other reasons
    None -- no problems

    """
    if not os.path.exists(path):
        return "No such file or directory"
    if not os.path.isfile(path):
        return "Not a file"
    if not os.access(path, os.R_OK):
        return "Read access denied"
    return None
