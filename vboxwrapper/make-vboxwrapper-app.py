# vim: expandtab ts=4 sw=4 sts=4:
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
import setuptools

APP = ['vboxwrapper.py']
VERSION = '0.8.2.1'

OPTIONS = {'argv_emulation': False,
           'semi_standalone': True,
           'site_packages': True,
           'optimize':  1}

setuptools.setup(
    name='VBoxWrapper',
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
