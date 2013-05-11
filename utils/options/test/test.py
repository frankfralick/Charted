
from options import *
import sys
import six
    
def test_good_chainstuf():
    """Test options class for being faithful subclass of chainstuf"""
    
    # make some base dictsw
    d1 = Options(this=1, that=2, roger=None)
    d2 = dict(roger=99, that=100)
    
    # test simple attribute equivalence
    dd = d1.push(d2)
    assert dd.this == 1
    assert dd.roger == 99
    assert dd.this == dd['this']
    assert dd.that == dd['that']
    
    assert dd.roger == dd['roger']
    
    # set value, ensure properly set, in top dict
    dd.roger = 'wilco'
    assert dd.roger == 'wilco'

def test_unset():
    d1 = Options(this=1, that=2, roger=None)
    d2 = dict(roger=99, that=100)
    dd = d1.push(d2)
    d3 = dict(fish='wanda', that='fish')
    de = dd.push(d3)

    assert de.that == 'fish'
    de.set(that=Unset)
    assert de.that == 100
    de.set(that='fishy')
    assert de.that == 'fishy'
    de.set(that=Unset)
    assert de.that == 100

    assert dd.that == 100
    dd.set(that=Unset)
    assert dd.that == 2
    assert de.that == 2
    
def test_magic():
    
    o = Options(this=1, slick='slack', blik=99)
    o['_magic'] = { 'slick': lambda x: x.capitalize() }
    
    # test that magic doesnt effect everything
    o.blik = "wubber"
    assert o.blik == 'wubber'

    # test that it does effect the right things
    o.set(slick='mack')
    assert o.slick == 'Mack'  # note magical capitalization
    
    p = o.push(dict(this=2))
    assert p.this == 2
    assert p.slick == 'Mack'
    
   
def test_magic_designation():
    
    class T(object):
        options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )
        
        # technique 1: lambda expression or function
        options.magic(
            slick = lambda v: v.capitalize(),
        )
        
        def __init__(self, *args, **kwargs):
            self.options = T.options.push(kwargs)
            self.data = args
            
        def set(self, **kwargs):
            """
            Uplevel the set operation. A set() on this object is converted into
            a set on its options.
            """
            self.options.set(**kwargs)
            
        # technique 2 - a static method with after-the-fact inclusion
        
        @staticmethod
        def nick_magic(v, cur):
            return v.upper()
    
        options.magic(nick=nick_magic)

        # technique 3 - a decorated method
        
        @options.magical('man')
        def man_magic(self, v, cur):
            return v.upper()

    
    t = T()
    assert t.options.this == 1
    assert t.options.blik == 99
    assert t.options.nick == 'nack'
    assert t.options.slick == 'slack'
    t.set(slick='slack')
    assert t.options.slick == 'Slack'
    t.set(slick='wack')
    assert t.options.slick =='Wack'
    t.set(nick='flick')
    assert t.options.nick == 'FLICK'
    
    t.set(man='boy')
    assert t.options.man == 'BOY'
    t.set(man='girl')
    assert t.options.man == 'GIRL'
    

   
def test_push():
    
    class T2(object):
        options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )
        
        def __init__(self, *args, **kwargs):
            self.options = T2.options.push(kwargs)
            self.data = args
            
        def set(self, **kwargs):
            """
            Uplevel the set operation. A set() on this object is converted into
            a set on its options.
            """
            self.options.set(**kwargs)
        
        def write(self, **kwargs):
            opts = self.options.push(kwargs)
            six.print_(opts.nick)
            
        def push1(self, **kwargs):
            opts = self.options.push(kwargs)
            
            # persistent data test
            assert T2.options.nick == 'nack'
            assert T2.options.slick == 'slack'
            assert t.options.nick == 'N'
            assert t.options.slick == 'S'

            # transient data test
            assert opts.nick == 44
            assert opts.slick == 55
    
    t = T2(nick='N', slick='S')
    assert T2.options.nick == 'nack'
    assert T2.options.slick == 'slack'
    assert t.options.nick == 'N'
    assert t.options.slick == 'S'
    t.push1(nick=44, slick=55)
    
def test_files():
    # The underlying stuf container used to have (<0.9.9) a problem with files
    # being assigned in a stuf() constructor. This tests that we're over that
    # problem.
    
    # Get names of files that won't be munged by py.test's capturing mechanism
    # (sys.stdout and sys.stderr definitely will be overtaken by py.test, but
    # their primitive double-underscore names won't be). This doesn't seem to
    # be an issue with Python 2.x, but spuriously screws up the test otherwise
    # in Python 3.x (gives false negative, saying module not working when it is)
    
    f1 = sys.__stdout__
    f2 = sys.__stderr__
    f3 = sys.__stdin__
    
    o = Options(a=f1, b=f2, c=[f2, f3])

    assert o.a is f1
    assert o.b is f2
    assert len(o.c) == 2
    assert o.c[0] is f2
    assert o.c[1] is f3
    
    # first push
    oo = o.push(dict(b=f1, c=12))
    assert oo.a is f1
    assert oo.b is f1
    assert oo.c == 12
    
    # second push
    ooo = oo.push(dict(a=f2, b=f3))
    assert ooo.a is f2
    assert ooo.b is f3
    assert ooo.c == 12
    
    # partial unset
    ooo.set(a=Unset)
    assert ooo.a is f1
    assert ooo.b is f3
    assert ooo.c == 12
