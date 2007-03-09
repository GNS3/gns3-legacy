#!/bin/sh

pylupdate4 -verbose gns-3.pro
lrelease-qt4 gns-3.pro
pyrcc4 translations/translations.qrc -o src/translations.py
