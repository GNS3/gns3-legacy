# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# http://www.gns3.net/contact
#

import os, sys
import GNS3.Globals as globals
from PyQt4 import QtCore
from GNS3.Utils import debug
import GNS3.Langs
import __main__


class Translator(object):

    def __init__(self):

        self.__langs = {}
        self.__langs_code = []
        self.__lang_current = ""
        self.__lastTranslator = None
        self.__lastQtTranslator = None

        # Add i18n dirs depending on platform.
        if sys.platform.startswith('win'):

            # __file__ is not supported by py2exe
            if hasattr(sys, "frozen"):
                self.__i18n_dirs = [os.path.dirname(os.path.abspath(sys.executable)) + os.sep + "Langs"]
            else:
                self.__i18n_dirs = [os.path.dirname(os.path.abspath(GNS3.Langs.__file__))]

            if os.environ.has_key("APPDATA"):
                self.__i18n_dirs.append(os.environ["APPDATA"] + "\\gns3\\Langs")
            else:
                debug('Translation: unable to find APPDATA in environ')

        else:

            self.__i18n_dirs = [os.path.dirname(os.path.abspath(GNS3.Langs.__file__)), os.path.dirname(os.path.abspath(__main__.__file__))]
            if os.environ.has_key("HOME"):
                self.__i18n_dirs.append(os.environ["HOME"] + "/.gns3/Langs")
            else:
                debug('Translation: unable to find HOME in environ')

        # Now find all available languages...
        self.findAvailableLangs()

    def findAvailableLangs(self):
        local_translator = QtCore.QTranslator()

        # Get available languages
        for i18n_dir in self.__i18n_dirs:
            d = QtCore.QDir(i18n_dir)

            if not d.exists():
                continue

            fileNames = d.entryList(QtCore.QStringList("*.qm"),
                                    QtCore.QDir.Files, QtCore.QDir.Name)
            for file in fileNames:
                lang_filename = i18n_dir + str(d.separator().toAscii()) + file
                # Remove file prefix (Lang_)
                lang = str(file)[5:]
                # if extended notation used, take 5 chars an language code
                if lang[2] == '_':
                    lang_code = lang[:5]
                # else only take 2 char (country code)
                else:
                    lang_code = lang[:2]

                # Load the file to get the i18n language name
                r_code = local_translator.load("Lang_" + lang_code, i18n_dir)
                if r_code == False:
                    # got error?
                    continue
                lang_name = unicode(local_translator.translate("MainWindow", "English"))

                # Create/Update langs dictionnary
                if self.__langs.has_key(lang_code):
                    self.__langs[lang_code]['dirs'].append(i18n_dir)
                else:
                    self.__langs[lang_code] = {
                        'code': lang_code,
                        'name': lang_name,
                        'dirs': [i18n_dir ],
                    }

        # Do some cleanup, and sort langs code
        for (k, v) in self.__langs.iteritems():
            # reverse directory order,
            # so first dir = last found
            v['dirs'].reverse()
            self.__langs_code.append(k)
        self.__langs_code.sort()

    def getAvailables(self):
        lang_availables = []

        for l in self.__langs_code:
            d = self.__langs[l]
            lang_availables.append([d['code'], d['name']])
        return (lang_availables)

    def loadByLangEnv(self, lang_fallback):
        if not os.environ.has_key('LANG'):
            return self.switchLangTo(lang_fallback)

        # get user env['LANG'], truncate to 5 chars,
        # as we don't need lang charset
        lang = os.environ['LANG'][:5]
        lang_code = None
        lang_country = None

        # Setup lang code & country
        if lang == "":
            return self.switchLangTo(lang_fallback)
        if len(lang) == 5 and lang[2] == "_":
            lang_country = lang[-2:].upper()
        if len(lang) >= 2:
            lang_code = lang[:2]

        # If we have a full langcode (i.e `en_US'), try it first
        if lang_country is not None and lang_code is not None:
            r_code = self.switchLangTo(lang_code + "_" + lang_country)
            if r_code == True:
                return
        # Or just the language (i.e `en')
        if lang_code is not None:
            r_code = self.switchLangTo(lang_code)
            if r_code == True:
                return
        # In last resort, try lang_fallback
        return self.switchLangTo(lang_fallback)

    def switchLangTo(self, lang):

        if (len(lang) > 5):
            lang = lang[:5]

        if self.__lang_current == lang:
            return
        if not self.__langs.has_key(lang):
            return

        translator = QtCore.QTranslator()
        qt_translator = QtCore.QTranslator()

        r_code = False
        for lang_dir in self.__langs[lang]['dirs']:
            # load Qt translation (for button in QMessageBox, QFileDialog etc.)
            qt_translator.load("qt_" + lang, lang_dir)
            r_code = translator.load("Lang_" + lang, lang_dir)
            if r_code == True:
                break
        if r_code == False:
            # TODO: Show a ERROR MsgBox (Warning: switchLangTo
            #       are called more than once, so find a mechanism
            #       which are not to intrusive for the user
            return False

        globals.GApp.installTranslator(translator)
        globals.GApp.installTranslator(qt_translator)
        if self.__lastTranslator is not None:
            globals.GApp.removeTranslator(self.__lastTranslator)
            globals.GApp.removeTranslator(self.__lastQtTranslator)

        self.__lastTranslator = translator
        self.__lastQtTranslator = qt_translator
        self.__lang_current = lang

        for widget in globals.GApp.topLevelWidgets():
            try:
                widget.retranslateUi(widget)
            except Exception, e:
                # simply ignore topLevelWidgets which don't
                # have a retranslateUi method
                pass
        return True
