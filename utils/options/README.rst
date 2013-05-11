A module that helps encapsulate option and configuration data using a
multi-layer stacking model.

Classes, for example, set default values for all
instances. Instances can set new values. If an instance doesn't set a value, the
class-set default "shines through" and remains in effect. Individual method
calls can also set transient values that apply just for that call. If the call
doesn't set a value, the instance value applies. If the instance didn't set a
value, the class default applies.

This layered or stacked approach is particularly helpful when you have highly
functional classes that aim for "reasonable" or "intelligent" defaults and
behaviors, yet that allow users to override those defaults at any time, and that
aim for a simple, unobtrusive API.

This 
option-handling pattern is based on delegation rather than inheritance. It's
described in `this StackOverflow.com discussion of "configuration sprawl" 
<http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813>`_.

Unfortunately, it's a bit hard to demonstrate the virtues of this approach with
simple code. Python already has pretty flexible function arguments, inlcuding
variable number of arguments (``*args``), keyword arguments, and optional
keyword arguments (``**kwargs``). Combined with object inheritance, base Python
already covers a large number of use cases. But when you have a large number of
configuration and instance variables, and when you might want to temporarily
override either class or instance settings, things get dicey. This messy,
complicated space is where ``options`` truly begins to shine.

Usage
=====

::

    from options import Options, attrs
    
    class Shape(object):
    
        options = Options(
            name   = None,
            color  = 'white',
            height = 10,
            width  = 10,
        )
        
        def __init__(self, **kwargs):
            self.options = Shape.options.push(kwargs)
        
        def draw(self, **kwargs):
            opts = self.options.push(kwargs)
            print attrs(opts)

    one = Shape(name='one')
    one.draw()
    one.draw(color='red')
    one.draw(color='green', width=22)
    
yielding::

    color='white', width=10, name='one', height=10
    color='red', width=10, name='one', height=10
    color='green', width=22, name='one', height=10

So far we could do this with instance variables and standard arguments. It
might look a bit like this::

    class ClassicShape(object):

        def __init__(self, name=None, color='white', height=10, width=10):
            self.name   = name
            self.color  = color
            self.height = height
            self.width  = width

but when we got to the ``draw`` method, things would be quite a bit messier.::

        def draw(self, **kwargs):
            name   = kwargs.get('name',   self.name)
            color  = kwargs.get('color',  self.color)
            height = kwargs.get('height', self.height)
            width  = kwargs.get('width',  self.width)
            print "color='{}', width={}, name='{}', height={}".format(color, width, name, height)
        
One problem here is that we broke apart the values provided to ``__init__()`` into
separate instance variables, now we need to re-assemble them into something unified.
And we need to explicitly choose between the ``**kwargs`` and the instance variables.
This is pretty repetitive, and not very pretty. Another classic alternative, using
native keyword arguments, is not much
better::

        def draw2(self, name=None, color=None, height=None, width=None):
            name   = name   or self.name
            color  = color  or self.color
            height = height or self.height
            width  = width  or self.width
            print "color='{}', width={}, name='{}', height={}".format(color, width, name, height)

If we add just a few more instance variables, we have the `Mr. Creosote <http://en.wikipedia.org/wiki/Mr_Creosote>`_
of class design on our hands. Not good. Things get worse if we want to set
default values for all shapes in the class. We have to rework every method that
uses values, the ``__init__`` method, *et cetera*. We've entered
"just one more wafer-thin
mint..." territory.

But with ``options``, it's easy::

    Shape.options.set(color='blue')
    one.draw()
    one.draw(height=100)
    one.draw(height=44, color='yellow')
    
yields::

    color='blue', width=10, name='one', height=10
    color='blue', width=10, name='one', height=100
    color='yellow', width=10, name='one', height=44

In one line, we reset the default for all ``Shape`` objects.

The more options and settings a class has, the more unwieldy the class and
instance variable approach becomes, and the more desirable the delegation
alternative. Inheritance is a great software pattern for many kinds of data and
program structures, but it's a bad pattern for complex option and configuration
handling. For richly featured classes, the delegation pattern used by
``options`` is much simpler. Even a large number of options requires almost no
additional code and imposes no additional complexity or failure modes. By consolidating
options into one place, and by allowing neat attribute-style access, everything is
kept tidy. We can add new options or methods with confidence::

    def is_tall(self, **kwargs):
        opts = self.options.push(kwargs)
        return opts.height > 100

Under the covers, ``options`` uses a variation on the ``ChainMap``
data structure
(a multi-layer dictionary) to provide its option stacking. Every option set is
stacked on top of previously set option sets, with lower-level values shinging
through if they're not set at higher levels. This stacking or overlay model
resmebles how local and global variables are managed in many programming
languages.

Magic Parameters
================

Python's ``*args`` variable-number of arguments and ``**kwargs`` keyword
arguments are sometimes called "magic" arguments. ``options`` takes this up
a notch, allowing arguments to be interpreted on the fly. This is useful, for instance,
to provide relative rather than just absolute values. As an example, say that
we added this code after
``Shape.options``
was defined::

    options.magic(
        height = lambda v, cur: cur.height + int(v) if isinstance(v, str) else v,
        width  = lambda v, cur: cur.width  + int(v) if isinstance(v, str) else v
    )
    
Now, in addition to absolute ``height`` and ``width`` parameters which are provided
by specifying those values as ``int``, your module
auto-magically supports relative parameters.::

    one.draw(width='+200')
    
yields::

    color='blue', width=210, name='one', height=10
    
This can be as fancy as you like, defining an entire domain-specific expression language.
But even small functions can give you a great bump in expressive power. For example,
add this and you get full relative arithmetic capability (``+``, ``-``, ``*``, and ``/``)::

    def relmath(value, currently):
        if isinstance(value, str):
            if value.startswith('*'):
                return currently * int(value[1:])
            elif value.startswith('/'):
                return currently / int(value[1:])
            else:
                return currently + int(value)
        else:
            return value
    
    ...
    
    options.magic(
        height = lambda v, cur: relmath(v, cur.height),
        width  = lambda v, cur: relmath(v, cur.width)
    )

Then::

    one.draw(width='*4', height='/2')

yields::

    color='blue', width=40, name='one', height=5
    
Magically interpreted parameters are the sort of thing that one doesn't need
very often or for every parameter--but when 
it's useful, it's *enormously* useful and highly leveraged, leading
to much simpler, much higher function
APIs. We call them 'magical' here because of the "auto-magical" interpretation,
but they are really just analogs of Python object properties. The magic function
is basically a "setter" for a dictionary element.

Design Considerations
=====================

In general, classes will define a set of methods that are "outwards facing"--methods 
called by external code when consuming the class's functionality.
Those methods should generally expose their options through ``**kwargs``,
creating a local variable (say ``opts``) that represents the sum of all options
in use--the full stack of call, instance, and class options, including
any present magical interpretations.

Internal class methods--the sort that are not generally called by external code,
and that by Python convention are often prefixed by an underscore (``_``)--these
generally do not need ``**kwargs``. They should accept their options as a
single variable (say ``opts`` again) that the externally-facing methods will
provide.

For example, if ``options`` didn't provide the nice formatting function ``attrs``,
we might have designed our own::

    def _attrs(self, opts):
        nicekeys = [ k for k in opts.keys() if not k.startswith('_') ]
        return ', '.join([ "{}={}".format(k, repr(opts[k])) for k in nicekeys ])
   
    def draw(self, **kwargs):
        opts = self.options.push(kwargs)
        print self._attrs(opts)
        
``draw()``, being the outward-facing API, accepts general arguments and
manages their stacking (by ``push``ing ``kwargs`` onto the instance options).
When the internal ``_attrs()`` method is called, it is handed a pre-digested
``opts`` package of options.

A nice side-effect of making this distinction: Whenever you see a method with
``**kwargs``, you know it's outward-facing. When you see a method with just
``opts``, you know it's internal.

Objects defined with ``options`` make excellent "callables."
Define the ``__call__`` method, and you have a very nice analog of
function calls.

``options`` has broad utility, but it's not for every class or module. It best
suits high-level front-end APIs that multiplex lots of potential functionality, and
wish/need to do it in a clean/simple way. Classes for which the set of instance
variables is small, or methods for which the set of known/possible parameters is
limited--these work just fine with classic Python calling conventions. "Horses
for courses."

Setting and Unsetting
=====================

Using ``options``, objects often become "entry points" that represent both
a set of capabilities and a set of configurations for how that functionality
will be used. As a result, you may want to be able to set the object's
values directly, without referencing their underlying ``options``. It's
convenient to add a ``set()`` method, then use it, as follows::

    def set(self, **kwargs):
        self.options.set(**kwargs)
        
    one.set(width='*10', color='orange')
    one.draw()
    
yields::

    color='orange', width=100, name='one', height=10

``one.set()`` is now the equivalent of ``one.options.set()``. Or continue using
the ``options`` attribute explicitly, if you prefer that.

Values can also be unset.::

    from options import Unset

    one.set(color=Unset)
    one.draw()
    
yields::

    color='blue', width=100, name='one', height=10
    
Because ``'blue'`` was the color to which ``Shape`` had be most recently set.
With the color of the instance unset, the color of the class shines through.

**NOTA BENE** while options are ideally accessed with an attribute notion,
the preferred of setting options is through method calls: ``set()`` if
accessing directly, or ``push()`` if stacking values as part of a method call.
These perform the interpretation and unsetting magic;
straight assignment does not. In the future, ``options`` may provide an
equivalent ``__setattr__()`` method to allow assignment--but not yet.

Leftovers
=========

``options`` expects you to define all feasible and legitimate options at the
class level, and to give them reasonable defaults.

None of the initial settings ever have magic applied. Much of the
expected interpretation "magic" will be relative settings, and relative settings
require a baseline value. The top level is expected and demanded to provide a
reasonable baseline.

Any options set "further down" such as when an instance is created or a method
called should set keys that were already-defined at the class level.

However, there are cases where "extra" ``**kwargs`` values may be provided and
make sense. Your object might be a very high level entry point, for example,
representing very large buckets of functionality, with many options. Some of
those options are relevant to the current instance, while others are intended as
pass-throughs for lower-level modules. This may seem a rarified case--and it is,
relatively speaking. But it does happen, and when you need that kind of
multi-level processing, it's really, really super amazingly handy to have.

``options`` supports this in its core ``push()`` method by taking the values
that are known to be part of the class's options, and deleting those from
``kwargs``. Any values left over in the ``kwargs`` ``dict`` are either errors,
or intended for other recipients.

As yet, there is no automatic check for leftovers.

The Magic APIs
==============

The callables (usually functions, lambda expressions, static methods, or methods) called
to preform magical interpretation can be called with 1, 2, or 3 parameters.
``options`` inquires as to how many parameters the callable accepts. If it
accepts only 1, it will be the value passed in. Cleanups like "convert to upper case"
can be done, but no relative interpretation. If it accepts 2 arguments,
it will be called with the value and the current option mapping, in that order.
(NB this order reverses the way you may think logical. Caution advised.) If the
callable requires 3 parameters, it will be ``None``, value, current mapping. This
supports method calls, though has the defect of not really
passing in the current instance.

A decorator form, ``magical()`` is also supported. It must be given the
name of the key exactly::

    @options.magical('name')
    def capitalize_name(self, v, cur):
        return ' '.join(w.capitalize() for w in v.split())

The net is that you can provide just about any kind of callable.
But the meta-programming of the magic interpretation API could use a little work.

Subclassing
===========

Subclasses may have a different set of options than the superclass. In this case,
the subclass should ``add()`` to the superclass's options. This creates a layered
effect, just like ``push()`` for an instance. The difference is, ``push()`` does
not allow new options (keys) to be defined; ``add()`` does. It is also possible to
assign the special null object ``Prohibited``, which will disallow instances of the
subclass from setting those values.::

    options = Superclass.options.add(
        func   = None,
        prefix = Prohibited,  # was available in superclass, but not here
        suffix = Prohibited,  # ditto
    )

An alternative is to copy (or restart) the superclass's options. That suits cases
where changes to the superclass's options should not effect the subclass's options.
With ``add()``, they remain linked in the same way as instances and classes are.

Flat Arguments
==============

Sometimes it's more elegant to provide some arguments as flat, sequential values
rather than by keyword. In this case, use the ``addflat()`` method::

    def __init__(self, *args, **kwargs):
        self.options = Quoter.options.push(kwargs)
        self.options.addflat(args, ['prefix', 'suffix'])
        
to consume optional ``prefix`` and ``suffix`` flat arguments.

Notes
=====

 * This is a work in progress. The underlying techniques have
   been successfully used in multiple projects, but it remains in an evolving
   state as a standalone module. The API may change over time.
   Swim at your own risk.
   
 * Open question: Could "magic" parameter processing be
   improved with a properties-based approach akin to that of `basicproperty <http://pypi.python.org/pypi/basicproperty>`_,
   `propertylib <http://pypi.python.org/pypi/propertylib>`_,
   `classproperty <http://pypi.python.org/pypi/classproperty>`_, and `realproperty <http://pypi.python.org/pypi/rwproperty>`_.
   
 * Open question: Should "magic" parameter setters be allow to change
   multiple options at once? Discovered use case for this: "Abbreviation"
   options that combine multiple changes into one compact option. These would
   probably not have stored values themselves. It would require setting the
   "dependent" option values via side-effect rather than functional return values.
   
 * Commenced automated multi-version testing with
   `pytest <http://pypi.python.org/pypi/pytest>`_
   and `tox <http://pypi.python.org/pypi/tox>`_. Now
   successfully packaged for, and tested against, Python 2.6, 2.7, 3.2, and 3.3.
   
 * Versions subsequent to 0.200 require a late-model version of ``stuf`` to
   avoid a problem its earlier iterations had with file objects.
 
 * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
   `@jeunice on Twitter <http://twitter.com/jeunice>`_
   welcomes your comments and suggestions.

Installation
============

::

    pip install options

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install options
    
(You may need to prefix these with "sudo " to authorize installation.)