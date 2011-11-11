from distutils.core import setup

try:
    import py2exe
except ImportError:
    raise RuntimeError, "Cannot import py2exe"

setup(console=['unpack.py'], zipfile=None, options={"py2exe": { "optimize": 2}})
