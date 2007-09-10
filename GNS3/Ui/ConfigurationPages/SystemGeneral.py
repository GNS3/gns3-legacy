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

from PyQt4 import QtGui
from GNS3.Ui.ConfigurationPages.Widget_SystemGeneral import Ui_SystemGeneral
import GNS3.Globals as globals

class UiConfig_SystemGeneral(QtGui.QWidget, Ui_SystemGeneral):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        Ui_SystemGeneral.setupUi(self, self)

        self.langs = globals.GApp.translator.getAvailables()
        for lang in self.langs:
            lang_code = lang[0]
            lang_name = lang[1]
            lang_displayText = "%s (%s)" % (lang_name, lang_code)
            self.langsBox.addItem(lang_displayText)

        self.loadConf()

    def loadConf(self):
        curr_lang_code = globals.GApp.systconf['general'].lang

        # Set the languages comboBox the the right value.
        idx = 0
        for i in self.langs:
            if i[0] == curr_lang_code:
                self.langsBox.setCurrentIndex(idx)
            idx += 1

    def saveConf(self):

        new_idx = self.langsBox.currentIndex()
        print type(new_idx)
        new_lang_code = self.langs[new_idx][0]

        print "new language: %s" % (self.langs[new_idx][1])
        globals.GApp.systconf['general'].lang = unicode(new_lang_code, 'utf-8')
        globals.GApp.translator.switchLangTo(new_lang_code)
        pass


