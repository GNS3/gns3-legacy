#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Contact: contact@gns3.net
#

from PyQt4 import QtCore, QtGui
import GNS3.Globals as globals

class Translator():
    def __init__(self):
        self.__loadedLangs = {}
        self.__i18n_dir = "./Langs"
        self.__lastTranslator = None

    def listAvailables(self):
        local_translator = QtCore.QTranslator()
        lang_availables = []

        trans_dir = QtCore.QDir(self.__i18n_dir)
        fileNames = trans_dir.entryList(QtCore.QStringList("*.qm"), QtCore.QDir.Files, QtCore.QDir.Name)

        print str(trans_dir)
        for i in fileNames:
            # Remove file prefix (Lang_)
            lang = i[5:]
            # if extended notation used, take 5 chars an language code
            if lang[2] == '_':
                lang_code = lang[:5]
            # else only take 2 char (country code)
            else:
                lang_code = lang[:2]
            
            local_translator.load("Lang_" + lang, self.__i18n_dir)
            lang_name = local_translator.translate("MainWindow", "English")

            lang_availables.append([lang_code, lang_name])

        return (lang_availables)

    def switchLangTo(self, lang):
    
        if (len(lang) > 5):
            lang = lang[:5]

        if self.__loadedLangs.has_key(lang):
            pass    

        translator = QtCore.QTranslator()
        translator.load("Lang_" + lang, self.__i18n_dir)

        globals.GApp.installTranslator(translator)
        if self.__lastTranslator is not None:
            print "::> Removing previous translator"
            globals.GApp.removeTranslator(self.__lastTranslator)

        self.__lastTranslator = translator
        globals.GApp.mainWindow.retranslateUi(globals.GApp.mainWindow)

