#!/usr/bin/env python
"""
Utilities for managing serial communications

References:
    https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
"""

__author__ = "tfeldmann"
__date__ = "11 November, 2015"
__credits__ = ["tfeldmann"]
__status__ = "production"

import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def default_serial_port():
    """First listed port (if any ports found)"""
    ports = serial_ports()
    return ports[0] if ports else None

class SerialChangedEventArgs(object):
    @property
    def Port(self):
        return self.__port__
    @property
    def Baud(self):
        return self.__baud__
    def __init__(self, port, baud):
        self.__port__ = port
        self.__baud__ = baud
