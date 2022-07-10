#!/usr/bin/env python
"""Config class and unit tests"""

__author__ = "Andrew Walla"
__date__ = "06 June, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import os
import unittest

class Config(object):
    '''Read a configuration file according to the INI format'''

    def __init__(self, filename='config.ini'):
        self.__data__ = dict()
        with open(filename, 'r') as f:
            for line in f.readlines():
                kvp = line.split('=')
                if len(kvp)==2 and not any( c in kvp[0] for c in [';', '#']):
                    self.__data__[kvp[0].strip()] = kvp[1].strip()

    def __getitem__(self, key):
        return self.__data__[key] if key in self.__data__ else None

    def __iter__(self):
        return self.__data__.__iter__()

    def __next__(self):
        return self.__data__.__next__()

    def GetValue(self, key, default=''):
        '''Get item from configuration file or return default if not found'''
        return self[key] if key in self.__data__ else default

class ConfigTest(unittest.TestCase):
    """Unit tests for the Config class"""

    def test_always_pass(self):
        """Test always passes to validate unit test framework is working correctly"""
        self.assertEqual(True, True)

    def test_all(self):
        """Test everything - code is simple enough to do it in one"""
        with open('config.ini', 'w') as f:
            f.write('; This is a sample config file\n')
            f.write('\n')
            f.write('[Some Variables]\n')
            f.write('Foo=42\n')
            f.write('#Bar=43\n')
            f.write('Hello=world')
        config = Config('config.ini')
        self.assertEqual(config['Foo'], '42')
        self.assertEqual(config['Hello'], 'world')
        self.assertFalse('Bar' in config)
        self.assertEqual(config.GetValue('Bar',default='Goodbye'), 'Goodbye')
        os.remove('config.ini')

if __name__ == "__main__":
    unittest.main()