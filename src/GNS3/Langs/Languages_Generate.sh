#!/bin/sh

# Please run Languages_UpdtProjFiles.sh before if you've added .py/.ui files or if you want to
# add a new language

# internal
PATH=$PATH":/Library/Frameworks/Python.framework/Versions/2.7/bin/:/usr/local/Trolltech/Qt-4.7.4/bin/:/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin:/opt/local/bin/"

# create/update .ts files (for Qt Linguist)
pylupdate4 -noobsolete -verbose Languages.pro

# create .qm files from .ts files
lrelease4 -verbose Languages.pro || lrelease -verbose Languages.pro
