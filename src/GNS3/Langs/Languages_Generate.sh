#!/bin/sh

# Set file names in gns3.pro

# create .ts files (for Qt Linguist)
/Library/Frameworks/Python.framework/Versions/2.7/bin/pylupdate4 -noobsolete -verbose Languages.pro

# create .qm files from .ts files
/usr/local/Trolltech/Qt-4.7.1/bin/lrelease Languages.pro || lrelease Languages.pro

# create ressource file (don't forget to add the .qm file to translations.qrc)
#pyrcc4 -compress 9 Languages.qrc -o ../Translations.py
