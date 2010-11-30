"""Output functions and message dictionary."""

import sys


def die(message):
    """Terminate program with an exit message."""
    sys.exit(message)


def to_stderr(algorithm_name, filename, result, end=None):
    """Print a result to stderr."""
    output = "{} ({}) = {}".format(algorithm_name.upper(), filename, result)
    print(output, end=end, file=sys.stderr)
    return len(output)


def to_stdout(algorithm_name, filename, result, end=None):
    """Print a result to stdout."""
    output = "{} ({}) = {}".format(algorithm_name.upper(), filename, result)
    print(output, end=end)
    return len(output)


def wipe(amount, end=None):
    """Print blank characters."""
    print(" " * amount, end=end, file=sys.stderr)


message_for = {}
message_for["match"] = "True"
message_for["mismatch"] = "False"
message_for["missing"] = "Digest not found in filename"
message_for["dupe_error"] = "hb: option -d takes exactly two arguments"
message_for["inline_error"] = "hb: option -i missing file or digest"
message_for["hash_count"] = "\n{} of {} file(s) hashed"
message_for["checklist_count"] = "\n{} of {} files(s) in {} line(s) checked"
message_for["mismatch_count"] = "Mismatches: {}"
