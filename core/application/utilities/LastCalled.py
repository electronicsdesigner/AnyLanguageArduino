#!/usr/bin/env python
"""A class to handle threading to ensure only the latest event is called"""

__author__ = "Andrew Walla"
__date__ = "08 February, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import time
import threading
import unittest

class LastCalled(object):
    """Encases a long-running callable function; ensures only most recent call"""

    @property
    def PendingCount(self):
        """Number of unserviced underlying function calls since last execution"""
        return len(self.__pending__)

    def __init__(self, child_function):
        self.__child_function__ = child_function
        self.__pending__ = list()
        self.__is_running__ = False
        self.__lock__ = threading.Lock()

    def __del__(self):
        self.__lock__.acquire()
        self.__pending__.clear()
        self.__lock__.release()

    def __call__(self, *args, **kwargs):
        self.__lock__.acquire()
        self.__pending__.append((args, kwargs))
        if not self.__is_running__:
            thread = threading.Thread(target=self.__worker_thread__)
            if not self.__is_running__:
                self.__is_running__ = True
                thread.start()
        self.__lock__.release()

    def __worker_thread__(self):
        while self.__is_running__:
            args, kwargs = self.__pending__.pop(0)
            self.__child_function__(*args, **kwargs)
            self.__lock__.acquire()
            if self.PendingCount > 1:
                self.__pending__ = [self.__pending__.pop(-1)]
            if self.PendingCount == 0:
                self.__is_running__ = False
            self.__lock__.release()

class LastCalledTest(unittest.TestCase):
    """Unit test for LastCalled class"""

    def test_always_pass(self):
        self.assertEqual(True, True)

    def test_call(self):
        class Foo(object):
            """Class with a worker thread"""
            def __init__(self):
                self.__args__ = list()
                self.__kwargs__ = list()
                self.__running__ = list()
                self.__finished__ = list()
            def run(self, *args, **kwargs):
                index = len(self.__args__)
                self.__args__.append(args)
                self.__kwargs__.append(kwargs)
                self.__running__.append(True)
                self.__finished__.append(False)
                while self.__running__[index]:
                    time.sleep(0.001)
                self.__finished__[index] = True
            def rtn(self, index):
                if self.__finished__[index]:
                    return None
                self.__running__[index] = False
                while not self.__finished__[index]:
                    time.sleep(0.001)
                return self.__args__[index], self.__kwargs__[index]

        class Bar(object):
            """Class that fires (too many) callbacks"""
            def __init__(self):
                self.__count__ = 0
                self.__callbacks__ = list()
            def go(self):
                self.__count__ = self.__count__ + 1
                for callback in self.__callbacks__:
                    callback(-self.__count__, count=self.__count__)
            def add(self, callback):
                self.__callbacks__.append(callback)

        foo = Foo()
        bar = Bar()
        try:
            last_called_foo_run = LastCalled(foo.run)
            bar.add(last_called_foo_run)
            for i in range(10):
                bar.go()
            self.assertEqual(foo.rtn(0),((-1,),{'count':1}))
            self.assertEqual(foo.rtn(1),((-10,),{'count':10}))
        finally:
            del foo
            del bar

if __name__ == '__main__':
    unittest.main()