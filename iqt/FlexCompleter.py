"""Word completion for GNU readline 2.0.

---------------------------------------------------------------------------
NOTE: This version is a re-implementation of FlexCompleter with
readline support for PyQt&sip-3.6 and earlier.

Full readline support is present in PyQt&sip-snapshot-20030531 and later.
---------------------------------------------------------------------------
NOTE: This version is a re-implementation of rlcompleter with selectable
namespace.

The problem with rlcompleter is that it's hardwired to work with
__main__.__dict__, and in some cases one may have 'sandboxed' namespaces. So
this class is a ripoff of rlcompleter, with the namespace to work in as an
optional parameter.

This class can be used just like rlcompleter, but the Completer class now has
a constructor with the optional 'namespace' parameter.

A patch has been submitted to Python@sourceforge for these changes to go in
the standard Python distribution.
---------------------------------------------------------------------------

Original rlcompleter documentation:

This requires the latest extension to the readline module (the
completes keywords, built-ins and globals in __main__; when completing
NAME.NAME..., it evaluates (!) the expression up to the last dot and
completes its attributes.

It's very cool to do "import string" type "string.", hit the
completion key (twice), and see the list of names defined by the
string module!

Tip: to use the tab key as the completion key, call

    readline.parse_and_bind("tab: complete")

Notes:

- Exceptions raised by the completer function are *ignored* (and
generally cause the completion to fail).  This is a feature -- since
readline sets the tty device in raw (or cbreak) mode, printing a
traceback wouldn't work well without some complicated hoopla to save,
reset and restore the tty state.

- The evaluation of the NAME.NAME... form may cause arbitrary
application defined code to be executed if an object with a
__getattr__ hook is found.  Since it is the responsibility of the
application (or the user) to enable this feature, I consider this an
acceptable risk.  More complicated expressions (e.g. function calls or
indexing operations) are *not* evaluated.

- GNU readline is also used by the built-in functions input() and
raw_input(), and thus these also benefit/suffer from the completer
features.  Clearly an interactive application can benefit by
specifying its own completer function and using raw_input() for all
its input.

- When the original stdin is not a tty device, GNU readline is never
used, and this module (and the readline module) are silently inactive.

"""

#*****************************************************************************
#
# Since this file is essentially a minimally modified copy of the rlcompleter
# module which is part of the standard Python distribution, I assume that the
# proper procedure is to maintain its copyright as belonging to the Python
# Software Foundation:
#
#       Copyright (C) 2001 Python Software Foundation, www.python.org
#
#  Distributed under the terms of the Python Software Foundation license.
#
#  Full text available at:
#
#                  http://www.python.org/2.1/license.html
#
#*****************************************************************************

import readline
import __builtin__
import __main__

__all__ = ["Completer"]

class Completer:
    def __init__(self, namespace = None):
        """Create a new completer for the command line.

        Completer([namespace]) -> completer instance.

        If unspecified, the default namespace where completions are performed
        is __main__ (technically, __main__.__dict__). Namespaces should be
        given as dictionaries.

        Completer instances should be used as the completion mechanism of
        readline via the set_completer() call:

        readline.set_completer(Completer(my_namespace).complete)
        """
        
        if namespace and type(namespace) != type({}):
            raise TypeError,'namespace must be a dictionary'

        # Don't bind to namespace quite yet, but flag whether the user wants a
        # specific namespace or to use __main__.__dict__. This will allow us
        # to bind to __main__.__dict__ at completion time, not now.
        if namespace is None:
            self.use_main_ns = 1
        else:
            self.use_main_ns = 0
            self.namespace = namespace

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.

        """
        if self.use_main_ns:
            self.namespace = __main__.__dict__
            
        if state == 0:
            if "." in text:
                self.matches = self.attr_matches(text)
            else:
                self.matches = self.global_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def global_matches(self, text):
        """Compute matches when text is a simple name.

        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        """
        import keyword
        matches = []
        n = len(text)
        for list in [keyword.kwlist,
                     __builtin__.__dict__.keys(),
                     self.namespace.keys()]:
            for word in list:
                if word[:n] == text and word != "__builtins__":
                    matches.append(word)
        return matches

    def attr_matches(self, text):
        """Compute matches when text contains a dot.

        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluatable in self.namespace, it will be evaluated and its attributes
        (as revealed by dir()) are used as possible completions.  (For class
        instances, class members are are also considered.)

        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.

        """
        import re

	# Testing. This is the original code:
	#m = re.match(r"(\w+(\.\w+)*)\.(\w*)", text)

	# Modified to catch [] in expressions:
	#m = re.match(r"([\w\[\]]+(\.[\w\[\]]+)*)\.(\w*)", text)

        # Another option, seems to work great. Catches things like ''.<tab>
        m = re.match(r"(\S+(\.\w+)*)\.(\w*)", text)

        if not m:
            return
        expr, attr = m.group(1, 3)
        object = eval(expr, self.namespace)
        words = dir(object)
        if hasattr(object,'__class__'):
            words.append('__class__')
            words = words + get_class_members(object.__class__)
        matches = []
        n = len(attr)
        for word in words:
            if word[:n] == attr and word != "__builtins__":
                matches.append("%s.%s" % (expr, word))
        return matches

def get_class_members(klass):
    # PyQwt's hack for PyQt&sip-3.6 and earlier
    if hasattr(klass, 'getLazyNames'):
        return klass.getLazyNames()
    # vanilla Python stuff
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret

readline.set_completer(Completer().complete)
