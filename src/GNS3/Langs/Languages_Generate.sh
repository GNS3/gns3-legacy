#!/bin/sh

# Set file names in gns-3.pro

# create .ts files (for Qt Linguist)
pylupdate4 -noobsolete -verbose Languages.pro

# create .qm files from .ts files
lrelease-qt4 Languages.pro || lrelease Languages.pro

# create ressource file (don't forget to add the .qm file to translations.qrc)
#pyrcc4 -compress 9 Languages.qrc -o ../Translations.py
