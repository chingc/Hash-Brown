#!/usr/bin/env python3.1

"""Hash Brown commandline interface."""

import getopt
import sys

from expand import expand
from mode import default, dupe, inline, check, embedded


def help():
    print("help")


def usage():
    print("""Valid commandline usage:
        hb [-h | -v | -c FILE(S)]
        hb HASH_TYPE [OPTIONS] FILE(S)
        """)


def version():
    print("version info")


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        sys.exit(help())
    if "-v" in sys.argv or "--version" in sys.argv:
        sys.exit(version())
    if len(sys.argv) <= 2:
        sys.exit(usage())

    function = None
    mode = None
    quiet = False
    recursive = False

    index = 2
    options = "hvdeisqR"
    long_options = ["help", "version",
        "dupe", "embedded", "inline", "string",
        "quiet", "recursive"]

    if sys.argv[1] in ("-c", "--check"):
        index = 1
        options += "c"
        long_options.append("check")
    else:
        function = sys.argv[1]

    try:
        opts, args = getopt.getopt(sys.argv[index:], options, long_options)
    except getopt.GetoptError as msg:
        sys.exit(sys.argv[0] + ": " + str(msg))

    for o, a in opts:
        if o in ("-d", "--dupe"):
            mode = "dupe"
        if o in ("-e", "--embedded"):
            mode = "embedded"
        if o in ("-i", "--inline"):
            mode = "inline"
        if o in ("-s", "--string"):
            mode = "string"
        if o in ("-q", "--quiet"):
            quiet = True
        if o in ("-R", "--recursive"):
            recursive = True
        if o in ("-c", "--check"):
            mode = "check"

    # expand globs
    args = expand(args, recursive)

    output = ""
    if mode is None:
        output = default(function, args)
    elif mode == "dupe":
        output = dupe(function, args)
    elif mode == "embedded":
        output = embedded(function, args)
    elif mode == "inline":
        output = inline(function, args)
    elif mode == "string":
        pass
    elif mode == "check":
        for arg in args:
            output = check(arg)
    else:
        sys.exit(sys.argv[0] + ": you are in the fifth dimension")


try:
    exit(main())
except KeyboardInterrupt:
    print("^C", file=stderr)
