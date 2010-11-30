"""Hashing modes."""

from algorithm import regex_for
from hasher import Hasher
from output import die, to_stderr, to_stdout, message_for


def default(algorithm_name, filenames):
    """Compute the digest of a file."""
    files_hashed = 0
    for filename in filenames:
        h = Hasher(algorithm_name, filename, True)
        if h.error is None:
            files_hashed += 1
            to_stdout(algorithm_name, filename, h.digest())
        else:
            to_stderr(algorithm_name, filename, h.error)
    return message_for["hash_count"].format(files_hashed, len(filenames))


def dupe(algorithm_name, filenames):
    """See if two files are the same."""
    if len(filenames) != 2:
        die(message_for["dupe_error"])
    files_hashed = 0
    digests = []
    for filename in filenames:
        h = Hasher(algorithm_name, filename, True)
        if h.error is None:
            files_hashed += 1
            to_stdout(algorithm_name, filename, h.digest())
            digests.append(h.digest())
        else:
            to_stderr(algorithm_name, filename, h.error)
            # ensure the result is false if both files are non-existent
            digests.append("" if len(digests) == 0 else " ")
    print(digests[0] == digests[1])
    return message_for["hash_count"].format(files_hashed, len(filenames))


def inline(algorithm_name, args):
    """See if a given digest matches the actual digest."""
    if len(args) % 2 != 0:
        die(message_for["inline_error"])
    files_hashed = 0
    bad_hash = 0
    args = {args[index]: args[index + 1] for index in range(0, len(args), 2)}
    for filename, digest in args.items():
        h = Hasher(algorithm_name, filename, True)
        if h.error is None:
            files_hashed += 1
            if h.match(digest):
                to_stdout(algorithm_name, filename, message_for["match"])
            else:
                bad_hash += 1
                to_stdout(algorithm_name, filename, message_for["mismatch"])
        else:
            to_stderr(algorithm_name, filename, h.error)
    print(message_for["mismatch_count"].format(bad_hash))
    return message_for["hash_count"].format(files_hashed, len(args))


def check(checklist):
    """Check the digests of the files in a checklist."""
    files_hashed = 0
    bad_hash = 0
    files_checked = 0
    lines_checked = 0
    with open(checklist, "rb") as infile:
        for line in infile:
            lines_checked += 1
            split = regex_for["checklist"].search(line.decode("utf_8"))
            if not split:
                continue
            files_checked += 1
            algorithm_name = split.group(1)
            filename = split.group(2)
            digest = split.group(3)
            h = Hasher(algorithm_name, filename, True)
            if h.error is None:
                files_hashed += 1
                if h.match(digest):
                    to_stdout(algorithm_name, filename, message_for["match"])
                else:
                    bad_hash += 1
                    to_stdout(algorithm_name, filename, message_for["mismatch"])
            else:
                to_stderr(algorithm_name, filename, h.error)
    print(message_for["mismatch_count"].format(bad_hash))
    return message_for["checklist_count"].format(
        files_hashed, files_checked, lines_checked
        )


def embedded(algorithm_name, filenames):
    """See if the digest in the filename is the actual digest."""
    files_hashed = 0
    bad_hash = 0
    for filename in filenames:
        digest = regex_for[algorithm_name].search(filename)
        if digest:
            h = Hasher(algorithm_name, filename, True)
            if h.error is None:
                files_hashed += 1
                if h.match(digest.group(0)):
                    to_stdout(algorithm_name, filename, message_for["match"])
                else:
                    bad_hash += 1
                    to_stdout(algorithm_name, filename, message_for["mismatch"])
        else:
            to_stdout(algorithm_name, filename, message_for["missing"])
    print(message_for["mismatch_count"].format(bad_hash))
    return message_for["hash_count"].format(files_hashed, len(filenames))
