if __name__ == "__main__":
    import sys

    from hb import hb

    for path in sys.argv[2:]:
        try:
            print(hb.compute(sys.argv[1], path))
        except hb.NotAFileError as e:
            print(e, file=sys.stderr)
