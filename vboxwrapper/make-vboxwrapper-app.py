# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

from distutils.core import setup, Extension
import setuptools

setuptools.setup(name='VBoxWrapper', app=['vboxwrapper.py'], options={'py2app': {'semi_standalone': True, 'site_packages': True, 'optimize':  1}}, setup_requires=['py2app'])
