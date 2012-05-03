#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
# make-exe.py
from distutils.core import setup
import py2exe

setup(console=["qemuwrapper.py"],zipfile=None)
