#!/usr/bin/python
"""
OpenEmbedded 'Event' implementation

Classes and functions for manipulating 'events' in the
OpenEmbedded (http://openembedded.org) build infrastructure.

Copyright: (c) 2003-2004 Chris Larson
"""

import os, re
class Event:
	"""Base class for events"""
	type = "Event"

NotHandled = 0
Handled = 1
handlers = []

def tmpHandler(event):
	"""Default handler for code events"""
	return NotHandled

def defaultTmpHandler():
	tmp = "def tmpHandler(e):\n\t\"\"\"heh\"\"\"\n\treturn 0"
	comp = compile(tmp, "tmpHandler(e)", "exec")
	return comp

def fire(event):
	"""Fire off an Event"""
	for h in handlers:
		if type(h).__name__ == "code":
			exec(h)
			if tmpHandler(event) == Handled:
				return Handled
		else:
			if h(event) == Handled:
				return Handled
	return NotHandled

def register(handler):
	"""Register an Event handler"""
	if handler is not None:
		# handle string containing python code
		if type(handler).__name__ == "str":
			return registerCode(handler)
		# prevent duplicate registration
		if not handler in handlers:
			handlers.append(handler)

def registerCode(handlerStr):
	"""Register a 'code' Event.
	   Deprecated interface; call register instead.

	   Expects to be passed python code as a string, which will
	   be passed in turn to compile() and then exec().  Note that
	   the code will be within a function, so should have had
	   appropriate tabbing put in place."""
	tmp = "def tmpHandler(e):\n%s" % handlerStr
	comp = compile(tmp, "tmpHandler(e)", "exec")
	# prevent duplicate registration
	if not comp in handlers:
		handlers.append(comp)

def remove(handler):
	"""Remove an Event handler"""
	for h in handlers:
		if type(handler).__name__ == "str":
			return removeCode(handler)

		if handler is h:
			handlers.remove(handler)

def removeCode(handlerStr):
	"""Remove a 'code' Event handler
	   Deprecated interface; call remove instead."""
	tmp = "def tmpHandler(e):\n%s" % handlerStr
	comp = compile(tmp, "tmpHandler(e)", "exec")
	handlers.remove(comp)

def getName(e):
	"""Returns the name of a class or class instance"""
	if getattr(e, "__name__", None) == None:
		return e.__class__.__name__
	else:
		return e.__name__


class PkgBase(Event):
        """Base class for package events"""

        def __init__(self, t, d = {}):
                self.pkg = t
                self.data = d

        def getPkg(self):
                return self._pkg

        def setPkg(self, pkg):
                self._pkg = pkg

        def getData(self):
                return self._data

        def setData(self, data):
                self._data = data

        pkg = property(getPkg, setPkg, None, "pkg property")
        data = property(getData, setData, None, "data property")


class BuildBase(Event):
        """Base class for oemake run events"""

        def __init__(self, n, p, c):
                self.name = n
                self.pkgs = p
                self.cfg = c

        def getPkgs(self):
                return self._pkgs

        def setPkgs(self, pkgs):
                self._pkgs = pkgs

        def getName(self):
                return self._name

        def setName(self, name):
                self._name = name

        def getCfg(self):
                return self._cfg

        def setCfg(self, cfg):
                self._cfg = cfg

        pkgs = property(getPkgs, setPkgs, None, "pkgs property")
        name = property(getName, setName, None, "name property")
        cfg = property(getCfg, setCfg, None, "cfg property")


class DepBase(PkgBase):
        """Base class for dependency events"""

        def __init__(self, t, data, d):
                self.dep = d
                PkgBase.__init__(self, t, data)

        def getDep(self):
                return self._dep

        def setDep(self, dep):
                self._dep = dep

        dep = property(getDep, setDep, None, "dep property")


class PkgStarted(PkgBase):
        """Package build started"""


class PkgFailed(PkgBase):
        """Package build failed"""


class PkgSucceeded(PkgBase):
        """Package build completed"""


class BuildStarted(BuildBase):
        """oemake build run started"""


class BuildCompleted(BuildBase):
        """oemake build run completed"""


class UnsatisfiedDep(DepBase):
        """Unsatisfied Dependency"""


class RecursiveDep(DepBase):
        """Recursive Dependency"""


class MultipleProviders(PkgBase):
        """Multiple Providers"""

