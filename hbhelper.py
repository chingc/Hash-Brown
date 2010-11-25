"""Contains miscellaneous helper functions."""

import glob
import os.path
import sys


def expand(path, recursive=False):
    """Expansion of the "*" and "?" globs, with optional recursion.

    path: A string giving the path to expand.
    NOTE: The range glob is disabled.
    """
    path_list = [path]
    if ("*" in path) or ("?" in path) or os.path.isdir(path):
        path = path.replace("[", "?")
        path = path.replace("]", "?")
        for x in glob.iglob(path):
            if recursive and os.path.isdir(x):
                path_list.extend(expand(x + "/*"))
            else:
                path_list.append(x)
        path_list.pop(0)
    return path_list


def myprint(x, y, z, end="\n", error=False):
    """Print helper.

    Outputs in the following format: x (y) = z
    """
    outfile = sys.stderr if error else sys.stdout
    output = "{} ({}) = {}".format(x.upper(), y, z)
    print(output, end=end, file=outfile)
    return len(output)
