#!/usr/bin/env python
"""A window for selecting which file to open"""

__author__ = "Andrew Walla"
__date__ = "10 June, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import wx
import os
from utilities.Config import Config
import subprocess

def endswith(path, ext):
    '''Recurse the path to find all files ending with the extension'''
    file_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                file_list.append(os.path.join(root,file))
    return file_list

class AnyLanguageArduinoConfig(Config):

    def __init__(self, filename):
        self.__filename__ = filename
        super(AnyLanguageArduinoConfig, self).__init__(filename)

    @property
    def Brief(self):
        return self['BRIEF'] if 'BRIEF' in self else None

    @property
    def Extension(self):
        return '.' + self['SOURCE CODE'].split('.')[1] if 'SOURCE CODE' in self else None

    @property
    def Path(self):
        return self.__filename__

class MainMenu(wx.Frame):

    @property
    def RootDirectory(self):
        '''The (hardcoded) project root directory'''
        return os.path.abspath(os.path.join(self.Directory,'../..'))

    @property
    def Directory(self):
        '''The directory of this source code file'''
        return os.path.dirname(__file__)

    @property
    def Configs(self):
        '''Returns a list of all config files found in the project'''
        return [AnyLanguageArduinoConfig(item) for item in endswith(self.RootDirectory, '.cfg')]

    @property
    def ConfigStrings(self):
        '''The config file description fields'''
        return [item.Brief for item in self.Configs]

    def __init__(self, parent, title="Any Language Arduino"):
        super(MainMenu, self).__init__(parent, title=title, size=(450,150))
        self.SetLabel("Any Language Arduino")
        self.SetIcon(wx.Icon(os.path.join(self.Directory,'arduino_icon.ico')))
        sizer = wx.GridBagSizer(4, 4)
        label = wx.StaticText(self, label="Project Type:")
        sizer.Add(label, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        self.ProjectChoice = wx.Choice(self, -1, choices=self.ConfigStrings)
        self.ProjectChoice.Bind(wx.EVT_CHOICE, self.OnSelectionChanged)
        sizer.Add(self.ProjectChoice, pos=(1, 0), span=(1, 4), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        self.NewButton = wx.Button(self, wx.ID_OK, label="New")
        self.NewButton.Bind(wx.EVT_BUTTON, self.OnNew)
        self.NewButton.Enable(False)
        self.OpenButton = wx.Button(self, wx.ID_OK, label="Open")
        self.OpenButton.Bind(wx.EVT_BUTTON, self.OnOpen)
        self.OpenButton.Enable(False)
        cancelButton = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        sizer.Add(self.NewButton, pos=(3, 1))
        sizer.Add(self.OpenButton, pos=(3, 2))
        sizer.Add(cancelButton, pos=(3, 3), flag=wx.RIGHT|wx.BOTTOM, border=10)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def lookup(self, key):
        '''Get the config file matching a given brief'''
        if key in self.ConfigStrings:
            return self.Configs[self.ConfigStrings.index(key)]
        else:
            return None

    @property
    def SelectedItem(self):
        return self.lookup(self.ConfigStrings[self.ProjectChoice.GetSelection()])

    def OnSelectionChanged(self, e):
        isEnabled = self.ProjectChoice.GetSelection()>=0
        self.NewButton.Enable(isEnabled)
        self.OpenButton.Enable(isEnabled)

    def OnNew(self, e):
        newFileDialog = wx.FileDialog(self, "Create", "", "", 
              self.SelectedItem.Brief.replace('|',',') + "|*" + self.SelectedItem.Extension, 
               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if newFileDialog.ShowModal() == wx.ID_OK:
            subprocess.Popen(
                ['python', os.path.join(self.Directory, 'AnyLanguageArduino.py'), self.SelectedItem.Path, newFileDialog.GetPath()],
                cwd=os.path.dirname(self.SelectedItem.Path),
                shell=True)
        newFileDialog.Destroy()

    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
              self.SelectedItem.Brief.replace('|',',') + "|*" + self.SelectedItem.Extension, 
               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:
            subprocess.Popen(
                ['python', os.path.join(self.Directory, 'AnyLanguageArduino.py'), self.SelectedItem.Path, openFileDialog.GetPath()],
                cwd=os.path.dirname(self.SelectedItem.Path),
                shell=True)
        openFileDialog.Destroy()

    def OnCancel(self, e):
        self.Close()

def MainMenuApplication():
    """Main application that launches the main menu"""
    app = wx.App()
    demo_app = MainMenu(None)
    demo_app.Show()
    app.MainLoop()

if __name__ == "__main__":
    MainMenuApplication()
