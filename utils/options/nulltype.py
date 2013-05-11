"""Options"""
import sys
sys.path.append("C:\\Python27\\Lib\\site-packages\\")
sys.path.append("C:\\Python27\\Lib\\site-packages\\PyBuilding\\utils\\")
from stuf import six
#this was "import six"

class NullType(object):
    """
    A 'null' type different from, but parallel to, None. Core function
    is representing emptyness in a way that doesn't overload None.
    
    Instantiate to create desired Null values.
    """
    def __init__(self, name=None):
        self.name = name
        
    def __repr__(self):
        if self.name is not None:
            return self.name
        else:
            return repr(self)
        
    if six.PY3:
        def bool(self):
            """I am always False."""
            return False
    else:
        def __nonzero__(self):
            """I am always False."""
            return False
