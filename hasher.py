"""This class facilitates the hashing of files."""

import os.path
import threading

from algorithm import algorithm_for
from output import to_stderr, wipe


class Hasher:
    def __init__(self, algorithm_name, filename, calculate_now=False):
        self._hasher = algorithm_for[algorithm_name.lower()]()
        self._watch_event = None
        self._watch_thread = None
        self._file_object = None
        self._file_size = 0
        self._output_length = 0
        self.algorithm_name = self._hasher.name
        self.filename = filename
        self.error = None
        if calculate_now:
            self.calculate()

    def calculate(self, observe_size=250):
        """Computes the digest."""
        try:
            with open(self.filename, "rb") as self._file_object:
                self._file_size = os.path.getsize(self.filename)
                if self._file_size > observe_size * 1024 ** 2:
                    self._observe()
                for data in self._file_object:
                    self._hasher.update(data)
                if self._file_size > observe_size * 1024 ** 2:
                    self._unobserve()
        except (IOError, OSError) as err:
            self.error = err.strerror

    def digest(self):
        """Returns the digest or an error message."""
        if self.error is None:
            return self._hasher.hexdigest()
        else:
            return self.error

    def match(self, digest):
        """Compares the digest with a given digest."""
        if digest.lower() == self.digest():
            return True
        else:
            return False

    def _observe(self):
        if self._watch_thread is not None:
            return  # thread already running
        if self._file_object is None:
            return  # no file to observe
        if self._file_size == 0:
            return  # avoid division by 0
        self._watch_event = threading.Event()
        self._watch_thread = threading.Thread(target=self._watcher)
        self._watch_thread.start()

    def _unobserve(self):
        if self._watch_thread is None:
            return  # thread does not exist
        if self._watch_thread.is_alive():
            self._watch_event.set()
            self._watch_thread.join()
        self._watch_event = None
        self._watch_thread = None
        self._output_length = 0

    def _watcher(self):
        while not self._watch_event.is_set():
            self._output_length = to_stderr(
                self.algorithm_name,
                self.filename,
                "{:.2%}".format(self._file_object.tell() / self._file_size),
                end="\r",
                )
            self._watch_event.wait(0.25)
        wipe(self._output_length, end="\r")
