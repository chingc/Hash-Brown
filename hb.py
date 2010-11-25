#!/usr/bin/env python3.1

"""Commandline interface."""

import getopt
import sys

import hbdictionary
import hbhelper
import hbsugar


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
    elif sys.argv[1].lower() in hbdictionary.HASH:
        function = sys.argv[1].lower()
    else:
        sys.exit(sys.argv[0] + ": Invalid option or unsupported hash type")

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
    for arg in args[:]:
        args.extend(hbhelper.expand(arg, recursive))
        args.pop(0)

    if mode is None:
        for arg in args:
            if arg == '-':
                hbsugar.standard_input(function, quiet)
            else:
                hbsugar.calculate(function, arg, quiet)
    elif mode == "dupe":
        if len(args) != 2:
            sys.exit(sys.argv[0] + ": option -d takes exactly two arguments")
        hbsugar.dupe(function, args[0], args[1], quiet)
    elif mode == "embedded":
        for arg in args:
            hbsugar.embedded(function, arg, quiet)
    elif mode == "inline":
        if len(args) % 2 != 0:
            sys.exit(sys.argv[0] + ": option -i missing file or digest")
        for i in range(0, len(args), 2):
            hbsugar.inline(function, args[i], args[i + 1], quiet)
    elif mode == "string":
        for arg in args:
            hbsugar.string(function, arg, quiet)
    elif mode == "check":
        for arg in args:
            hbsugar.check(arg, quiet)
    else:
        sys.exit(sys.argv[0] + ": you are in the fifth dimension")


try:
    exit(main())
except KeyboardInterrupt:
    print("^C", file=stderr)
