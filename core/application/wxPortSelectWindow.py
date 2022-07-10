#!/usr/bin/env python
"""A window for selecting the serial port"""

__author__ = "Andrew Walla"
__date__ = "29 May, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import wx
import os
from utilities.Serial import *

class wxPortSelectWindow(wx.Dialog):

    @property
    def Port(self):
        """The currently selected port"""
        return self.__port__
    @Port.setter
    def Port(self, value):
        self.__port__ = value

    def __init__(self, parent, title="Serial Port"):
        super(wxPortSelectWindow, self).__init__(parent, title=title, size=(300,150))
        self.SetLabel("Serial Port")
        self.__port__ = None
        sizer = wx.GridBagSizer(4, 4)
        label = wx.StaticText(self, label="Serial Port:")
        sizer.Add(label, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        ports = serial_ports()
        self.PortList = wx.Choice(self, -1, choices=ports)
        self.PortList.Bind(wx.EVT_CHOICE, self.OnPortChanged)
        sizer.Add(self.PortList, pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        okButton = wx.Button(self, wx.ID_OK, label="Okay")
        okButton.Bind(wx.EVT_BUTTON, self.OnOkay)
        cancelButton = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        sizer.Add(okButton, pos=(3, 3))
        sizer.Add(cancelButton, pos=(3, 4), flag=wx.RIGHT|wx.BOTTOM, border=10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def OnPortChanged(self, e):
        self.Port = self.PortList.GetString(self.PortList.GetSelection())

    def OnOkay(self, e):
        self.EndModal(wx.ID_OK)

    def OnCancel(self, e):
        self.Port = None
        self.EndModal(wx.ID_CANCEL)

def wxPortSelectWindowDemo():
    """Demo to be executed in __main__ for wxPortSelectWindowDemo features"""
    app = wx.App()
    demo_app = wxPortSelectWindow(None)
    demo_app.Show()
    app.MainLoop()

if __name__ == "__main__":
    wxPortSelectWindowDemo()
