# -*- coding: utf-8 -*-
'''dictionaries with attribute-style access.'''
#from stuf.iterable import (  #this is what it was
from iterable import (
    exhaustmap as exhaustitems, exhaustcall as exhaustmap, exhauststar)

from core import (
    defaultstuf, fixedstuf, frozenstuf, orderedstuf, stuf, chainstuf, countstuf)
#from stuf.core import (  #this is what it was
__version__ = (0, 9, 10)
__all__ = (
    'defaultstuf fixedstuf frozenstuf orderedstuf stuf chainstuf countstuf'
).split()
