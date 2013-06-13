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

#print "WELCOME to Preferences.py"

from PyQt4 import QtGui, QtCore
from GNS3.Ui.Form_PreferencesDialog import Ui_PreferencesDialog
from GNS3.Utils import translate
import GNS3.Globals as globals

class PreferencesDialog(QtGui.QDialog, Ui_PreferencesDialog):

    def __init__(self):
        """ Initilize a preferences dialog
        """

        # force the translation of Capture
        translate('PreferencesDialog', 'Capture')

        self.__prefsList = [
                        'General',
                        'Dynamips',
                        'Capture',
                        'Qemu',
                        'VirtualBox',
                        #'DeployementWizard' #FIXME: TEMP DISABLED FOR GNS3 0.8.4 RC1.
                        ]

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.connect(self.listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.configItemChanged)
        self.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Apply), QtCore.SIGNAL('clicked()'), self.__applyChanges)
#         self.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Ok), QtCore.SIGNAL('clicked()'), self.__applyChanges)

        # Init dialog
        self.__initDialog()
        # Raise a element in list
        self.__raiseWidgetByNum(0)

    def retranslateUi(self, MainWindow):
        # Call parent retranslateUi
        Ui_PreferencesDialog.retranslateUi(self, self)

        # Update titleLabel
        currIdx = self.stackedWidget.currentIndex()
        if currIdx > -1 and len(self.__prefsList) > currIdx:
            self.titleLabel.setText(translate('PreferencesDialog', self.__prefsList[currIdx]))

        # For each widget retranslate too
        lnum = 0
        for itemName in self.__prefsList:
            try:
                widget = self.stackedWidget.widget(lnum)
                widget.retranslateUi(widget)
                self.listWidget.item(lnum).setText(translate('PreferencesDialog', self.__prefsList[lnum]))
            except Exception:
                # In case widgets don't have restranslateUi method
                pass
            lnum += 1

    def __applyChanges(self):
        """ Save change for all item present into the Dialog
        All widget need to implement a method `saveConf' for this to work.
        """

        lnum = 0
        for itemName in self.__prefsList:
            widget = self.stackedWidget.widget(lnum)
            if widget.saveConf() == False:
                return False
            lnum += 1
        return True

    def __loadWidget(self, widgetPrefix, widgetName):
        """ Load a config widget from GNS3.Ui.ConfigurationPages
        """
        widgetCompleteName = widgetPrefix + widgetName
        modName = "GNS3.Ui.ConfigurationPages.Page_%s" % (widgetCompleteName)
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
        except ImportError, err:
            print "Error while importing %s: %s" % (modName, err)
            return None

    def __initDialog(self):

        # Insert config pages...
        lnum = 0
        for itemName in self.__prefsList:
            cls = self.__loadWidget('Preferences', itemName)
            widget = cls()
            item = QtGui.QListWidgetItem(translate('PreferencesDialog', itemName),
                    self.listWidget)
            # Insert widget / item into the dialog
            self.listWidget.insertItem(lnum, item)
            self.stackedWidget.insertWidget(lnum, widget)
            # increment for next item / widget
            lnum += 1

    def __raiseWidgetByNum(self, num):
        self.titleLabel.setText(
            translate('PreferencesDialog', self.__prefsList[num]))
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

    def reject(self):
        """ Refresh devices list when closing the window
        """
   
        globals.GApp.mainWindow.nodesDock.populateNodeDock(globals.GApp.workspace.dockWidget_NodeTypes.windowTitle())
        QtGui.QDialog.reject(self)
   
    def accept(self):
        """ Refresh devices list when closing the window
        """
   
        globals.GApp.mainWindow.nodesDock.populateNodeDock(globals.GApp.workspace.dockWidget_NodeTypes.windowTitle())
        if self.__applyChanges():
            QtGui.QDialog.accept(self)
