# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
# make-exe.py
from distutils.core import setup
import py2exe

setup(console=['vboxwrapper.py'], options = {"py2exe": {"dll_excludes": ["POWRPROF.dll", "MSWSOCK.dll"]}}, zipfile=None)
