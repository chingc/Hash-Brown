#!/usr/bin/env python3.1

"""Commandline interface."""

import getopt
import os.path
import sys

import algorithm
import hb
import message


class UsageError(Exception):
    """Commandline usage errors.

    Attributes:
    message -- an explanation of the error

    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def main():
    exit_status = 0

    try:
        argv = sys.argv
        progname = os.path.basename(argv[0]) + ":"

        if "-h" in argv:
            raise UsageError("help")
        if "-v" in argv:
            raise UsageError("version")

        if len(argv) <= 1:
            raise UsageError("help")
        elif argv[1] in ("-c"):
            opts, args = getopt.getopt(argv[2:], "")
            if len(args) == 0:
                raise UsageError("No files specified")
            mode = "checklist"
        elif argv[1].lower() in algorithm.names():
            opts, args = getopt.getopt(argv[2:], "deis")
            if len(args) == 0:
                raise UsageError("No files specified")
            algo = argv[1].lower()
            for o, a in opts:
                if o in ("-d"):
                    if len(args) % 2 != 0:
                        raise UsageError("Even number of arguments required")
                    mode = "dupe"
                elif o in ("-e"):
                    mode = "embedded"
                elif o in ("-i"):
                    if len(args) % 2 != 0:
                        raise UsageError("Even number of arguments required")
                    mode = "inline"
                elif o in ("-s"):
                    mode = "string"
                else:
                    raise UsageError("Twilight Zone")
            if len(opts) == 0:
                mode = "default"
        else:
            raise UsageError("Unrecognized algorithm or option")

        if mode == "default":
            for arg in args:
                hb.default(algo, arg)
        elif mode == "checklist":
            for arg in args:
                hb.checklist(arg)
        elif mode == "dupe":
            for i in range(0, len(args), 2):
                hb.dupe(algo, args[i], args[i + 1])
        elif mode == "embedded":
            for arg in args:
                hb.embedded(algo, arg)
        elif mode == "inline":
            for i in range(0, len(args), 2):
                hb.inline(algo, args[i], args[i + 1])
        elif mode == "string":
            for arg in args:
                hb.string(algo, arg)

    except UsageError as error:
        if error.message == "help":
            message.help()
        elif error.message == "version":
            message.version()
        else:
            exit_status = 1
            print(progname, error, file=sys.stderr)

    except (getopt.GetoptError, IOError, LookupError) as error:
        exit_status = 1
        print(progname, error, file=sys.stderr)

    finally:
        return exit_status


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
