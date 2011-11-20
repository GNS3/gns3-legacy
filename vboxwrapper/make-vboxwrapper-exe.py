# make-exe.py
from distutils.core import setup
import py2exe

setup(console=['vboxwrapper.py'], options = {"py2exe": {"typelibs": [('{46137EEC-703B-4FE5-AFD4-7C9BBBBA0259}',0,1,3)]}}, zipfile=None)
