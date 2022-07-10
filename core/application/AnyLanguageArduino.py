#!/usr/bin/env python
"""Application to act as an IDE for the Arduino in any programming language"""

__author__ = "Andrew Walla"
__date__ = "29 May, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import os
import re
import sys
import subprocess
import time
import wx
import datetime
from argparse import *
from serial import *
from wxTextFileTab import wxTextFileTab
from wxPortSelectWindow import wxPortSelectWindow
from wxStatusManager import wxStatusManager
from wxFileDropTarget import wxFileDropTarget
from ScriptFile import ScriptFile
from utilities.LastCalled import LastCalled
from utilities.Config import Config
from utilities.Serial import *

class AnyLanguageArduino(wx.Frame):
    """Application that watches for changes to source code and then uploads"""

    @property
    def Status(self):
        """The status text on the lower left of the window"""
        return self.StatusManager.Status
    @Status.setter
    def Status(self, value):
        self.StatusManager.Status = value

    @property
    def SourceCode(self):
        """The file being edited"""
        if self.__filename__ is None:
            return None
        if not os.path.exists(self.__filename__):
            self.__new_file__(self.__filename__, 'SOURCE CODE')
        return self.__filename__
    @SourceCode.setter
    def SourceCode(self, value):
        self.__filename__ = value
        self.FileNameTextBox.SetValue(value)
        self.CodeTab.Path = self.SourceCode
        self.ScriptTab.Path = self.UploadScript

    @property
    def SourceCodeExt(self):
        """Filename extension for the source code"""
        filename, ext = os.path.splitext(self.config['SOURCE CODE'])
        return ext

    @property
    def UploadScript(self):
        """The file that defines the compilation / upload steps"""
        if self.__filename__ is None:
            return None
        filename = os.path.splitext(self.__filename__)[0] + ScriptFile.Ext
        if not os.path.exists(filename):
            self.__new_file__(filename, 'UPLOAD SCRIPT')
        return filename

    @property
    def Port(self):
        """The serial port to communicate with the Arduino"""
        return self.__port__
    @Port.setter
    def Port(self, value):
        if self.__port__ != value:
            self.__port__ = value
            self.PortButton.SetLabel(value if value else "Serial")
            self.OnSerialChanged()

    @property
    def Baud(self):
        """The serial port baud to communicate with the Arduino"""
        return self.__baud__
    @Baud.setter
    def Baud(self, value):
        if self.__baud__ != value:
            self.__baud__ = value
            self.BaudList.SetSelection(Serial.BAUDRATES.index(value))
            self.OnSerialChanged()

    def __init__(self, config_file, source_code=None, parent=None, *args, **kwargs):
        super(AnyLanguageArduino, self).__init__(parent, *args, **kwargs)
        self.__filename__ = None
        self.__serial_callback__ = list()
        self.__port__ = -1
        self.__baud__ = 9600
        self.config = Config(config_file)
        self.SetDropTarget(wxFileDropTarget(self.OnFileDrop))
        nb = wx.Notebook(self)
        self.FileNameTextBox = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.CodeTab = wxTextFileTab(nb)
        if self.config['STC LEXER']:
            self.CodeTab.Lexer = int(self.config['STC LEXER'])
        if self.config['KEYWORDS']:
            self.CodeTab.Keywords = [k.strip() for k in self.config['KEYWORDS'].split(',')]
        self.ConsoleTab = wxTextFileTab(nb)
        self.ScriptTab = wxTextFileTab(nb)
        self.ScriptTab.Lexer = ScriptFile.Lexer
        self.ScriptTab.Keywords = ScriptFile.Keywords
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.FileNameTextBox, flag=wx.TOP | wx.EXPAND)
        nb.AddPage(self.CodeTab, "Code")
        nb.AddPage(self.ScriptTab, "Script")
        nb.AddPage(self.ConsoleTab, "Console")
        vbox.Add(nb, proportion=1, flag=wx.EXPAND)
        statusBar = wx.Panel(self)
        statusBox = wx.BoxSizer(wx.HORIZONTAL)
        self.StatusText = wx.StaticText(statusBar, -1)
        self.PortButton = wx.Button(statusBar, -1, "Serial")
        self.Port = default_serial_port()
        self.PortButton.Bind(wx.EVT_BUTTON, self.OnPortButtonClicked)
        bauds = [str(baud) for baud in Serial.BAUDRATES]
        self.BaudList = wx.Choice(statusBar, -1, choices=bauds)
        self.BaudList.Bind(wx.EVT_CHOICE, self.OnBaudChanged)
        self.BaudList.SetSelection(Serial.BAUDRATES.index(self.__baud__))
        self.UploadButton = wx.Button(statusBar, label="Upload")
        statusBox.Add(self.StatusText, proportion=1, flag=wx.LEFT | wx.ALIGN_CENTER, border=4)
        statusBox.Add(self.PortButton, proportion=0, flag=wx.RIGHT | wx.ALIGN_CENTER)
        statusBox.Add(self.BaudList, proportion=0, flag=wx.RIGHT | wx.ALIGN_CENTER)        
        statusBox.Add(self.UploadButton, proportion=0, flag=wx.RIGHT)
        statusBar.SetSizer(statusBox)
        vbox.Add(statusBar, flag=wx.BOTTOM | wx.EXPAND)
        self.SetSizer(vbox)
        self.StatusManager = wxStatusManager(self.StatusText)
        self.Status = "Version = " + __version__
        if self.config['WELCOME MESSAGE']:
            self.Status = self.config['WELCOME MESSAGE']
        self.UploadButton.Bind(wx.EVT_BUTTON, self.OnUpload)
        self.upload = LastCalled(self.__upload__)
        if source_code:
            self.SourceCode = source_code
        if self.config['BRIEF']:
            self.SetTitle(self.config['BRIEF'])
        else:
            self.SetTitle('Any Language Arduino')
        if self.config['ICON'] and os.path.exists(self.config['ICON']):
            self.SetIcon(wx.Icon(self.config['ICON']))

    def __upload__(self):
        """Compile the source code (programmatic equivalent to clicking the button)"""
        if self.SourceCode is not None and os.path.isfile(self.SourceCode):
            self.ConsoleTab.Text = "Upload in progress\n"
            result = subprocess.run([self.UploadScript], capture_output=True)
            text = result.stdout.decode() + result.stderr.decode()
            text = text.replace("\r","").replace("\n\n","\n")
            self.ConsoleTab.Text = text

    def add_serial_listener(self, listener):
        """Add a listener to subscribe to changes in serial settings"""
        self.__serial_callback__.append(listener)

    def remove_serial_listener(self, listener):
        """Remove a listener subscribed to changes in serial settings"""
        self.__serial_callback__.remove(listener)

    def OnFileDrop(self, filenames):
        for file in filenames:
            if file.endswith(self.SourceCodeExt):
                self.SourceCode = file
                self.Status = 'Opened file: ' + os.path.basename(file)
                return
        for file in filenames:
            if os.path.isdir(file):
                dialog = wx.TextEntryDialog(
                    self, 
                    'Enter a name for your source code',
                    'New File')
                if dialog.ShowModal() == wx.ID_OK:
                    filename = dialog.GetValue().split('.')[0]
                    filename += self.SourceCodeExt
                    self.SourceCode = os.path.join(file, filename)
                    self.Status = 'Created file: ' + filename
                return
        self.Status = 'ERROR: Valid source code file not provided'

    def OnPortButtonClicked(self, e):
        dialog = wxPortSelectWindow(None)
        dialog.ShowModal()
        if dialog.Port:
            self.Port = dialog.Port
        dialog.Destroy()

    def OnUpload(self, e):
        self.upload()

    def OnSerialChanged(self):
        for callback in self.__serial_callback__:
            callback(SerialChangedEventArgs(self.Port, self.Baud))

    def OnBaudChanged(self, e):
        self.Baud = int(self.BaudList.GetString(self.BaudList.GetSelection()))

    def __new_file__(self, filename, template_index):
        """Create a new file from a template"""
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        text = ''
        template = self.config[template_index]
        if template and os.path.exists(template):
            with open(template, 'r') as f:
                text = f.read()
        with open(filename, 'w') as f:
            f.write(self.__apply_substitutions__(text))

    def __apply_substitutions__(self, text):
        """Apply substitutions to template"""
        text = text.replace('[AUTHOUR]', os.getlogin())
        port = re.search(r'\[PORT=(.*?)\]', text)
        if port:
            portno = port.groups()[0]
            text = text.replace(portno, self.Port if self.Port else portno)
        wd = self.config['PROGRAM DIRECTORY']
        text = text.replace('[PROGRAM DIRECTORY]', wd if wd else '.')
        filename, ext = os.path.splitext(os.path.basename(self.SourceCode))
        text = text.replace('[FILENAME]', filename)
        text = text.replace('[EXTENSION]', ext[1:])
        text = text.replace('[DIRECTORY]', os.path.dirname(self.SourceCode))
        now = datetime.datetime.now()
        text = text.replace('[DAY]', now.strftime("%d"))
        text = text.replace('[MONTH]', now.strftime("%b"))
        text = text.replace('[YEAR]', now.strftime("%Y"))
        return text

def main():
    parser = ArgumentParser(description = 'Multiple language Arduino IDE')
    parser.add_argument('config', help='INI file specifying language settings')
    parser.add_argument('filename', nargs='?', help='Source code to edit')
    args = parser.parse_args()
    app = wx.App()
    frame = AnyLanguageArduino(args.config, args.filename)
    frame.AutoCompile = True
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
