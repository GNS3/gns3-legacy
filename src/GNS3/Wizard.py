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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_Wizard import Ui_Wizard
from GNS3.IOSDialog import IOSDialog
from GNS3.Config.Preferences import PreferencesDialog


class Wizard(QtGui.QDialog, Ui_Wizard):
    """ Wizard class
    """

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        # connections to slots
        self.connect(self.pushButton_Step1, QtCore.SIGNAL('clicked()'), self.slotStep1)
        self.connect(self.pushButton_Step2, QtCore.SIGNAL('clicked()'), self.slotStep2)
        self.connect(self.pushButton_Step3, QtCore.SIGNAL('clicked()'), self.slotStep3)

    def slotStep1(self):

        globals.preferencesWindow = PreferencesDialog()
        globals.preferencesWindow.show()
        globals.preferencesWindow.exec_()
        globals.preferencesWindow = None

    def slotStep2(self):

        globals.preferencesWindow = PreferencesDialog()

        # show Dynamips pane when Preferences dialog opens.
        dynamips_pane = globals.preferencesWindow.listWidget.findItems("Dynamips", QtCore.Qt.MatchFixedString)[0]
        if dynamips_pane:
            globals.preferencesWindow.listWidget.setCurrentItem(dynamips_pane)

        globals.preferencesWindow.show()
        globals.preferencesWindow.exec_()
        globals.preferencesWindow = None

    def slotStep3(self):

        dialog = IOSDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()
