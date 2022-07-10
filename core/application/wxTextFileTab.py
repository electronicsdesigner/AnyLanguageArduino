#!/usr/bin/env python
"""A class implementing a wxPython Scintilla Text Box inside a Notebook tab"""

__author__ = "Andrew Walla"
__date__ = "06 February, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import wx
import wx.stc
import keyword
import os
import sys
import random
from utilities.LastCalled import LastCalled
import keyword

class wxTextFileTab(wx.Panel):
    @property
    def TextCtrl(self):
        """Access the text box object"""
        return self.__textctrl__

    @property
    def Text(self):
        """The text in the textbox"""
        return self.__textctrl__.GetValue()
    @Text.setter
    def Text(self, value):
        self.__textctrl__.SetValue(value.replace('\r',''))

    @property
    def Path(self):
        """File to be synchronised with textbox contents"""
        return self.__path__
    @Path.setter
    def Path(self, value):
        self.__path__ = None
        if value:
            if os.path.exists(value):
                with open(value, 'r') as f:
                    self.__textctrl__.SetValue(f.read())
        self.__path__ = value

    @property
    def Keywords(self):
        """A list of keywords to apply syntax highlighting to"""
        return self.__keywords__
    @Keywords.setter
    def Keywords(self, value):
        self.__keywords__ = value
        self.__textctrl__.SetKeyWords(0, " ".join(value))

    @property
    def Lexer(self):
        """A lexer from wx.stc.STC_LEX_[INSERT_LANGUAGE_HERE] to parse text syntax"""
        return self.__textctrl__.GetLexer()
    @Lexer.setter
    def Lexer(self, value):
        self.__textctrl__.SetLexer(value)

    def __init__(self, parent, *args, **kwargs):
        super(wxTextFileTab, self).__init__(parent, *args, **kwargs)
        parent = parent.GetParent()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.__textctrl__ = wx.stc.StyledTextCtrl(self, style=wx.TE_MULTILINE)
        self.__textctrl__.SetDropTarget(parent.DropTarget)
        sizer.Add(self.__textctrl__, wx.ID_ANY, wx.EXPAND) 
        self.SetSizer(sizer)
        self.__path__ = None
        self.Bind(wx.stc.EVT_STC_CHANGE, self.OnTextChanged)
        self.__keywords__ = list()
        self.__UpdateTextFile__ = LastCalled(self.UpdateTextFile)
        self.__readonly__ = False
        if sys.platform.startswith('win'):
            font = 'Courier New'
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            font = 'Monaco'
        else:
            font = 'Courier'
        random.seed(0)
        for i in range(1,100):
            r = lambda: random.randint(100,255)
            random_colour = '#%02X%02X%02X' % (r(),r(),r())
            self.__textctrl__.StyleSetSpec(i, "fore:"+random_colour+",face:"+font+",size:8")

    def OnTextChanged(self, e):
        self.__UpdateTextFile__()
        e.Skip()

    def UpdateTextFile(self):
        if self.__path__:
            text = self.Text.replace('\r','')
            if text:
                with open(self.__path__, 'w') as f:
                    f.write(text)
            elif os.path.exists(self.__path__):
                os.remove(self.__path__)

def wxTextFileTabDemo():
    """Using wxTextFileTab as Python text editor that autosaves"""
    app = wx.App()
    frame = wx.Frame(None, title="Type a Python filename to begin:")
    vbox = wx.BoxSizer(wx.VERTICAL)
    filenameTextBox = wx.TextCtrl(frame)
    vbox.Add(filenameTextBox, flag=wx.TOP | wx.EXPAND)
    nb = wx.Notebook(frame)
    textFileTab = wxTextFileTab(nb)
    textFileTab.Lexer = wx.stc.STC_LEX_PYTHON
    textFileTab.Keywords = keyword.kwlist
    nb.AddPage(textFileTab, "Source code")
    vbox.Add(nb, proportion=1, flag=wx.EXPAND)
    frame.SetSizer(vbox)
    def OnFilenameEnter(e):
        key = e.GetKeyCode()
        if key == wx.WXK_RETURN:
            textFileTab.Path = filenameTextBox.GetValue()
        e.Skip()
    filenameTextBox.Bind(wx.EVT_KEY_DOWN, OnFilenameEnter)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    wxTextFileTabDemo()