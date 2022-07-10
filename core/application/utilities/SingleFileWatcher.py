#!/usr/bin/env python
"""A class implementing a file system watcher for a single file"""

__author__ = "Andrew Walla"
__date__ = "07 February, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import unittest

class SingleFileWatcher(object):
    """Place an OS filesystem watch on a single file to fire event when changed"""

    @property
    def Filename(self):
        """The (single) file being watched for changes"""
        return self.__filename__
    @Filename.setter
    def Filename(self, value):
        self.__filename__ = value
        if self.__running__:
            self.__stop__()
            self.__start__()

    @property
    def IsRunning(self):
        """Whether the file watcher is currently enabled (watching for changes)"""
        return self.__running__

    def __init__(self):
        self.__filename__ = None
        self.__callbacks__ = list()
        self.__watchdog__ = None
        self.__running__ = False

    def __del__(self):
        self.stop()

    def start(self):
        """Start watching for changes"""
        self.__running__ = True
        if self.Filename is not None:
            self.__start__()

    def stop(self):
        """Stop watching for changes"""
        self.__running__ = False
        self.__stop__()

    def add(self, callback):
        """Register a callback to be called upon file changed event"""
        self.__callbacks__.append(callback)

    def remove(self, callback):
        """Unregister a callback that was previously registered"""
        self.__callbacks__.remove(callback)

    def __start__(self):
        class Handler(FileSystemEventHandler):
            def __init__(self, base):
                self.__base__ = base
            def on_modified(self, e):
                if e.src_path == self.__base__.Filename:
                    for callback in self.__base__.__callbacks__:
                        callback(e)
            def on_created(self, e):
                self.on_modified(e)
            def on_moved(self, e):
                self.on_modified(FileModifiedEvent(e.dest_path))
        self.__watchdog__ = Observer()
        self.__watchdog__.schedule(
            Handler(self),
            os.path.dirname(self.Filename),
            recursive=False)
        self.__watchdog__.start()

    def __stop__(self):
        if self.__watchdog__:
            self.__watchdog__.stop()        

class SingleFileWatcherTest(unittest.TestCase):

    def test_always_pass(self):
        self.assertEqual(True, True)

    def test_always_fail(self):
        raise Exception(NotImplemented)

if __name__ == '__main__':
    unittest.main()

