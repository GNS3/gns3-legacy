# make-exe.py
from distutils.core import setup
import py2exe

setup(console=["qemuwrapper.py"],zipfile=None)
