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

from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_MACTableDialog import Ui_MACTableDialog
from GNS3.Utils import translate
import GNS3.Dynagen.dynamips_lib as lib
import socket


class MACTableDialog(QtGui.QDialog, Ui_MACTableDialog):
    """ MACTableDialog class
    """

    def __init__(self, node, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.connect(self.pushButtonRefresh, QtCore.SIGNAL('clicked()'), self.__refreshTable)
        self.connect(self.pushButtonClear, QtCore.SIGNAL('clicked()'), self.__clearTable)
        self.setWindowTitle(translate('MACTableDialog', "%s MAC Address Table") % node.hostname)
        self.node = node
        self.__refreshTable()

    def __refreshTable(self):

        self.plainTextEditMACTable.clear()
        if self.node.ethsw:
            try:
                result = self.node.ethsw.show_mac()
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, translate("MACTableDialog", "Dynamips error"),  unicode(msg))
                return
            except (lib.DynamipsErrorHandled, socket.error):
                QtGui.QMessageBox.critical(self, translate("MACTableDialog", "Dynamips error"), translate("MACTableDialog", "Connection lost"))
                return
            table = ""
            for chunks in result:
                lines = chunks.strip().split('\r\n')
                for line in lines:
                    if line == '100-OK':
                        continue
                    infos = line.split()
                    connected_interfaces = map(int, self.node.getConnectedInterfaceList())
                    for port in connected_interfaces:
                        nio = self.node.ethsw.nio(port)
                        if nio and nio.name == infos[3]:
                            table = table + infos[1] + ' ' + translate("MACTableDialog", "learned from port") + ' ' + str(port) + "\n"
                            break
            self.plainTextEditMACTable.setPlainText(table)

    def __clearTable(self):

        if self.node.ethsw:
            try:
                self.node.ethsw.clear_mac()
                QtGui.QMessageBox.information(self, translate("MACTableDialog", "MAC Table"),  translate("MACTableDialog", "The MAC table has been cleared"))
                self.__refreshTable()
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, translate("MACTableDialog", "Dynamips error"),  unicode(msg))
                return
            except (lib.DynamipsErrorHandled, socket.error):
                QtGui.QMessageBox.critical(self, translate("MACTableDialog", "Dynamips error"), translate("MACTableDialog", "Connection lost"))
                return

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """

        QtGui.QDialog.accept(self)
