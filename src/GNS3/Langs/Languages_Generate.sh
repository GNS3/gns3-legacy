#!/bin/sh

# Set file names in gns-3.pro

# create .ts files (for Qt Linguist)
/opt/local/Library/Frameworks/Python.framework/Versions/2.6/bin/pylupdate4 -noobsolete -verbose Languages.pro

# create .qm files from .ts files
/usr/local/Trolltech/Qt-4.7.0/bin/lrelease Languages.pro || lrelease Languages.pro

# create ressource file (don't forget to add the .qm file to translations.qrc)
#pyrcc4 -compress 9 Languages.qrc -o ../Translations.py
