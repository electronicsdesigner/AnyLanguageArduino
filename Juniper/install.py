#!/usr/bin/env python
"""Configure Juniper configuration file for first-time users"""

__author__      = "Andrew Walla"
__date__        = "05 June, 2022"
__copyright__   = "Copyright 2022, Andrew Walla"
__credits__     = ["Andrew Walla"]
__license__     = "Beerware"
__version__     = "1.0.0"
__maintainer__  = "Andrew Walla"
__email__       = "andrew.walla@beta-mail.com"
__status__      = "development"

import os
from textwrap import dedent
from argparse import *
import sys

def __contains__(prefixes):
    """Helper function to infer operating system"""
    return any([sys.platform.startswith(pre) for pre in prefixes])

Windows = __contains__(['win'])
Linux = __contains__(['linux', 'cygwin'])

# Filenames
config    = 'Juniper.cfg'
programdir= os.path.abspath(os.path.join(os.getcwd(), '..'))
code      = os.path.join(os.getcwd(), 'template.jun')
scriptext = '.bat' if Windows else '.sh' if Linux else ''
script    = os.path.join(os.getcwd(), 'template'+scriptext)

# Command line parsing
parser = ArgumentParser(
    description = 'Generate default configuration files')
parser.add_argument(
    '--remove',
    action = 'store_true',
    help = 'Remove previously created configuration files')
args = parser.parse_args()

def install():
    '''Generate default configuration files'''
    if not os.path.exists(config):
        print('Creating file: ' + config)
        with open(config, 'w') as f:
            f.write('; Configuration file for AnyLanguageArduino\n')
            f.write('; Juniper Programming Language\n')
            f.write('\n')
            f.write('[User Interface Settings]\n')
            f.write('BRIEF=Juniper | Functional programming for Arduino\n')
            f.write('ICON=Juniper.ico\n')
            f.write('WELCOME MESSAGE=Drag a .jun file into the window to begin\n')
            f.write('\n')
            f.write('[Programming Language Settings]\n')
            f.write('STC LEXER=68\n')
            f.write('KEYWORDS=module,open,let,ref,fun,loop,setup,fn\n')
            f.write('\n')
            f.write('[Template Files]\n')
            f.write('PROGRAM DIRECTORY=' + programdir + '\n')
            f.write('SOURCE CODE=' + code + '\n')
            f.write('UPLOAD SCRIPT=' + script + '\n')

def remove():
    '''Delete any previously created configuration files'''
    if os.path.exists(config):
        print('Removing file: ' + config)
        os.remove(config)

if args.remove:
    remove()
else:
    install()