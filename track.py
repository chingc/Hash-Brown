"""Progress tracker."""

import os.path
import sys
import threading


def _progress(handle, event):
    """Print file progress until the file handle is closed.

    Arguments:
    handle -- an open file handle
    event -- a threading event object

    """
    interval = 0.25
    elapsed = 0.001  # using zero causes division by zero
    try:
        name = os.path.basename(handle.name)
        size = os.path.getsize(handle.name)
        while not handle.closed:
            position = handle.tell()
            ratio = position / size
            speed = "{:.2f} MB/s".format(position / elapsed / 1024 ** 2)
            output = "{} @ {:.2%} ({})".format(name, ratio, speed)
            print(output, end="\r", file=sys.stderr)
            event.wait(interval)
            elapsed += interval  # accuracy is not important here
    except:
        pass


def progress(handle):
    """Spawn a separate thread to track progress.

    Arguments:
    handle -- an open file handle

    """
    t = threading.Thread(target=_progress, args=(handle, threading.Event()))
    t.start()


def threshold(megabytes=150):
    """A size in bytes to determine whether or not files are tracked.

    Notes:
    Using an argument value of zero will track all files.  This is highly not
    recommended because the performance impact of creating and destroying the
    thread that does tracking will become painfully obvious if you're hashing
    many small files (any file that takes less a few seconds to hash).

    Any negative integer value will return one yottabyte, a value so large that
    it basically disables tracking for the foreseeable future.  1Y ought to be
    enough to disable tracking.

    """
    return megabytes * 1024 ** 2 if megabytes > -1 else 1024 ** 8
