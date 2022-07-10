#!/usr/bin/env python
"""A class implementing a wxPython file drop and example application"""

__author__ = "Andrew Walla"
__date__ = "06 July, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import wx

class wxFileDropTarget(wx.FileDropTarget):
    '''Class to handle file drop events'''

    def __init__(self, callback=None):
        wx.FileDropTarget.__init__(self)
        self.__callbacks__ = list()
        if callback:
            self.__callbacks__.append(callback)

    def add(self, callback):
        '''Register a callback(filenames) to process the file drop event'''
        self.__callbacks__.append(callback)

    def remove(self, callback):
        '''Remove a previously registered callback'''
        self.__callbacks__.remove(callback)

    def OnDropFiles(self, x, y, filenames):
        for callback in self.__callbacks__:
            callback(filenames)
        return True

def wxFileDropTargetDemo():
    """Example application using a wxFileDropTargetDemo"""
    app = wx.App()
    raise Exception(NotImplemented)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    wxFileDropTargetDemo()