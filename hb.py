"""Command-line interface for Hash Brown."""

import argparse
import sys
import textwrap

import core


def main():
    def rprint(name, data, result):
        """Prints hashing results."""
        if isinstance(data, bytes):
            data = '"' + data.decode() + '"'
        print("{} ({}) = {}".format(name.upper(), data, result))

    guaranteed = sorted(core.algorithm.keys())

    parser = argparse.ArgumentParser(
        usage="%(prog)s -h | %(prog)s [ALGORITHM] OPTION",
        description="A convenient command-line file hashing utility.",
        epilog=textwrap.dedent("""
            When using checklists, the argument specifying the hashing algorithm
            is ignored.  It will be determined by the checklist.

            A checklist is a plain text file with lines like this:
            CRC32 (document.txt) = ad0c2001
            CRC32 (photo.png) = 1629491b

            It can contain different algorithms.
            CRC32 (document.txt) = ad0c2001
            CRC32 (photo.png) = 1629491b
            MD5 (audio.flac) = 69afdf17b98ed394964f15ab497e12d2
            SHA1 (video.mkv) = 1f09d30c707d53f3d16c530dd73d70a6ce7596a9

            Comments can be on a line by itself, at the beginning, or the end.
            I am a string.  CRC32 ("hello, world!") = 58988d13  Double quote me!

            %(prog)s 4.0, Ching Chow
            http://chingc.tumblr.com
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    parser.add_argument("algorithm",
        nargs="?",
        default="sha1",
        choices=guaranteed,
        help="{} {}".format(", ".join(guaranteed), "(default: sha1)"),
        metavar="ALGORITHM"
        )

    mutex = parser.add_mutually_exclusive_group(required=True)

    mutex.add_argument("-c",
        help="verify a checklist",
        metavar="CHECKLIST"
        )
    mutex.add_argument("-d",
        nargs=2,
        help="see if one is a duplicate of the other",
        metavar=("FILE1", "FILE2")
        )
    mutex.add_argument("-e",
        nargs="+",
        help="see if the filename embedded digest matches",
        metavar="FILE"
        )
    mutex.add_argument("-i",
        nargs="+",
        help="get the digest of the given input files",
        metavar="FILE"
        )
    mutex.add_argument("-m",
        nargs=2,
        help="see if the given digest matches",
        metavar=("FILE", "DIGEST")
        )
    mutex.add_argument("-s",
        type=lambda s: s.encode(),
        help="get the digest of a string",
        metavar="STRING"
        )

    args = parser.parse_args()
    name = args.algorithm

    try:
        if args.c:
            for name, data, digest in core.parse(args.c):
                try: rprint(name, data, core.match(name, data, digest))
                except Exception as error: print(error, file=sys.stderr)
        elif args.d:
            result1 = core.calculate(name, args.d[0])
            rprint(name, args.d[0], result1)
            result2 = core.calculate(name, args.d[1])
            rprint(name, args.d[1], result2)
            print(result1 == result2)
        elif args.e:
            for e in args.e:
                try: rprint(name, e, core.match(name, e))
                except Exception as error: print(error, file=sys.stderr)
        elif args.i:
            for i in args.i:
                try: rprint(name, i, core.calculate(name, i))
                except Exception as error: print(error, file=sys.stderr)
        elif args.m:
            rprint(name, args.m[0], core.match(name, args.m[0], args.m[1]))
        elif args.s:
            rprint(name, '"' + args.s.decode() + '"', core.calculate(name, args.s))
        else:
            print("send me your input because you shouldn't be here!", file=sys.stderr)
    except Exception as error:
        print(error, file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("operation stopped by user", file=sys.stderr)
