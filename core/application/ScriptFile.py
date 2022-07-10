#!/usr/bin/env python
"""Helper class to contain OS specific switches"""

__author__ = "Andrew Walla"
__date__ = "30 May, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import sys
import wx.stc

class __ScriptFile__(object):
    """Support for OS-specific script files (batch or shell)"""

    @property
    def Ext(self):
        if self.RunningWindows:
            return ".bat"
        if self.RunningLinux:
            return ".sh"
        raise Exception("Unsupported platform")       

    @property
    def Lexer(self):
        if self.RunningWindows:
            return wx.stc.STC_LEX_BATCH
        if self.RunningLinux:
            return wx.stc.STC_LEX_BASH
        raise Exception("Unsupported platform")       

    @property
    def Keywords(self):
        if self.RunningWindows:
            return [
                '%',    '/',    '\\',   "==",   '!==!', "|",    '@',
                '*',    '>',    '>>',   '<',    '%VAR%','REM',  'NUL',
                'NOT',  'ECHO', 'FOR',  'IN',   'DO',   'OFF',
                'GOTO', 'PAUSE','CHOICE','IF',  'EXIST','CALL'  'COMMAND',
                'SET',  'SHIFT','SGN',  'ERRORLEVEL',   'CON'   'PRN',
            ]
        if self.RunningLinux:
            return [
                '$',    '-',    '/',    "=",    '!=',   "|",    'set',
                '*',    '>',    '>>',   '<',    '$VAR', '#',    
                '!',    'echo', 'for',  'in',   'do',   'sleep','case',
                'select','if',  '-e',   '-z',   'source','.',   'export',
                'shift','-lt',  '-gt',  '$?',   'stdin'  'stdout',
                '/dev/null',
            ]
        raise Exception("Unsupported platform")       

    @property
    def RunningWindows(self):
        """Is this executing on a Windows PC?"""
        return self.__platform__(['win'])

    @property
    def RunningLinux(self):
        """Is this executing on a Linux PC?"""
        return self.__platform__(['linux', 'cygwin'])

    def __platform__(self, prefixes):
        """Helper function to infer operating system"""
        return any([sys.platform.startswith(pre) for pre in prefixes])

ScriptFile = __ScriptFile__()