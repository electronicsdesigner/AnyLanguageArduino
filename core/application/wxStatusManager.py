#!/usr/bin/env python
"""A class to enable property based getting and setting of a text label"""

__author__ = "Andrew Walla"
__date__ = "05 February, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

class wxStatusManager(object):
    """Get and set the value of a wx.StaticText label"""

    def __init__(self, wxStaticText):
        """
        Initialise a new status manager and provide a text label to contain the status

        Parameters
        ----------
        wxStaticText : str
            A wx.StaticText label to contain the status text
        """
        self.__statictext__ = wxStaticText

    @property
    def Status(self):
        """The value of the wx.StaticText label provided during initialisation"""
        return self.__statictext__.GetLabel()
    @Status.setter
    def Status(self, value):
        self.__statictext__.SetLabel(value)
