#!/usr/bin/env python
"""Test whether platform is Windows or Linux"""

__author__ = "Andrew Walla"
__date__ = "05 June, 2022"
__copyright__ = "Copyright 2022, Andrew Walla"
__credits__ = ["Andrew Walla"]
__license__ = "Beerware"
__version__ = "1.0.0"
__maintainer__ = "Andrew Walla"
__email__ = "andrew.walla@beta-mail.com"
__status__ = "development"

import sys

def __contains__(prefixes):
    """Helper function to infer operating system"""
    return any([sys.platform.startswith(pre) for pre in prefixes])

IsWindows = __contains__(['win'])
IsLinux = __contains__(['linux', 'cygwin'])