# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    print(
        """
        This homework requires Python 3.
        
        You may already have it in your path. Try using `python3` instead of `python`
        at the command line.
        
        You may already have Python 3 installed via PyCharm or a Python virtual env
        such as anaconda. (If you don’t think you’ve ever installed such a thing and
        what is that anyway?!? ... then you probably haven’t.) 
        
        If you don’t already have Python 3, then on a Mac:
        
            brew install python3
        
        On Windows:
        
            https://www.python.org/downloads/windows/
        """)
    exit(1)

from .types import *
from .expressions import *
