#!/bin/sh

# Please run Languages_UpdtProjFiles.sh before if you've added .py/.ui files or if you want to
# add a new language

# Set file names in gns3.pro
# ...

# internal
PATH=$PATH":/Library/Frameworks/Python.framework/Versions/2.7/bin/:/usr/local/Trolltech/Qt-4.7.1/bin/"

# create/update .ts files (for Qt Linguist)
pylupdate4 -noobsolete -verbose Languages.pro

# create .qm files from .ts files
lrelease -verbose Languages.pro
