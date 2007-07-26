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

from PyQt4 import QtGui, QtCore
from GNS3.Ui.Form_PreferencesDialog import Ui_PreferencesDialog
from GNS3.Utils import translate

_systemPrefs = [
	'General',
	'Applications',
]

_projectPrefs = [
	'General',
]

class	PreferencesDialog(QtGui.QDialog, Ui_PreferencesDialog):

    def __init__(self, type = 'System'):
        """ Initilize a preferences dialog
        You can also choose the preferences type (used later for widget prefix)
        """

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.connect(self.listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.configItemChanged)
        self.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.SIGNAL('clicked()'), self.__applyChanges)
        self.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Ok),
            QtCore.SIGNAL('clicked()'), self.__applyChanges)

        # Init dialog
        self.__initDialog(type)
        # Raise the first element in list
        self.__raiseWidgetByNum(0)

    def __applyChanges(self):
        """ Save change for all item present into the Dialog
        All widget need to implement a method `saveConf' for this to work.
        """
        lnum = 0
        for itemName in self.__prefsList:
            widget = self.stackedWidget.widget(lnum)
            widget.saveConf()
            lnum += 1


    def __loadWidget(self, widgetPrefix, widgetName):
        """ Load a config widget from GNS3.Ui.ConfigurationPages
        """
        widgetCompleteName = widgetPrefix + widgetName
        modName = "GNS3.Ui.ConfigurationPages.%s" % (widgetCompleteName)
        try:
            # Import module
            mod = __import__(modName)
            # Walk into module tree
            components = modName.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            # Finally, get the class
            mod = getattr(mod, 'UiConfig_' + widgetPrefix + widgetName)
            return mod
        except ImportError:
            #FIXME: graphical error msg
            print 'no page !'
            return None

    def __initDialog(self, type):
        if type == 'System':
            dialogTitle = translate('Preferences', 'System preferences')
            self.__prefsList = _systemPrefs
        elif type == 'Project':
            dialogTitle = translate('Preferences', 'Project preferences')
            self.__prefsList = _projectPrefs
        else:
            raise 'Unknown dialog type'

        # Set dialog title
        self.setWindowTitle(dialogTitle)

        lnum = 0
        for itemName in self.__prefsList:
            cls = self.__loadWidget(type, itemName)
            widget = cls()
            item = QtGui.QListWidgetItem(translate('Preferences', itemName),
                    self.listWidget)
            # Insert widget / item into the dialog
            self.listWidget.insertItem(lnum, item)
            self.stackedWidget.insertWidget(lnum, widget)
            # increment for next item / widget
            lnum += 1

    def __raiseWidgetByNum(self, num):
        self.titleLabel.setText(
            translate('Preferences', self.__prefsList[num]))
        # Set stackedWidget minimum size
        widget = self.stackedWidget.widget(num)
        self.stackedWidget.setMinimumSize(widget.size())
        self.stackedWidget.resize(widget.size())
        # Raise the demanded widget
        self.stackedWidget.setCurrentIndex(num)

    def configItemChanged(self, widget_curr, widget_prev):
        if widget_curr is None:
            widget_curr = widget_prev
        self.__raiseWidgetByNum(self.listWidget.row(widget_curr))
