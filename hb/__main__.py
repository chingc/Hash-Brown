if __name__ == "__main__":
    import sys

    from hb import hb

    match sys.argv[1]:
        case "-c":
            for path in sys.argv[3:]:
                try:
                    print(hb.compute(sys.argv[2], path))
                except hb.NotAFileError as e:
                    print(e, file=sys.stderr)
        case "-s":
            for path in sys.argv[2:]:
                hb.scan(path)
