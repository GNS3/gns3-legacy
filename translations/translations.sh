#!/bin/sh

# Set file names in gns-3.pro

# create .ts files (for Qt Linguist)
pylupdate4 -verbose gns-3.pro

# create .qm files from .ts files
lrelease-qt4 gns-3.pro || lrelease gns-3.pro

# create ressource file (don't forget to add the .qm file to translations.qrc)
pyrcc4 -compress 9 translations.qrc -o ../src/Translations.py
