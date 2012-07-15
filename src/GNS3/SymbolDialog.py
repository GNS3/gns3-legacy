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

from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Ui.Form_SymbolDialog import Ui_SymbolDialog


class SymbolDialog(QtGui.QDialog, Ui_SymbolDialog):
    """ SymbolManager class
    """

    def __init__(self, items):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.items = items

        symbol_resources = QtCore.QResource(":/symbols")
        for symbol in symbol_resources.children():
            symbol = str(symbol)
            if symbol.endswith('.normal.svg'):
                name = symbol[:-11]
                item = QtGui.QTreeWidgetItem()
                item.setText(0, name)
                item.setIcon(0, QtGui.QIcon(':/symbols/' + symbol))
                self.treeWidgetSymbols.addTopLevelItem(item)

    def on_applyButton_clicked(self):
        """ Apply settings for a node
        """

        current = self.treeWidgetSymbols.currentItem()
        if current:
            name = current.text(0)
            normal_renderer = QtSvg.QSvgRenderer(':/symbols/' + name + '.normal.svg')
            select_renderer = QtSvg.QSvgRenderer(':/symbols/' + name + '.selected.svg')
            for item in self.items:
                item.setRenderers(normal_renderer, select_renderer)
                item.default_symbol = False
                item.type = name

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """

        if button == self.buttonBox.button(QtGui.QDialogButtonBox.Apply):
            self.on_applyButton_clicked()
        elif button == self.buttonBox.button(QtGui.QDialogButtonBox.Cancel):
            QtGui.QDialog.reject(self)
        else:
            self.on_applyButton_clicked()
            QtGui.QDialog.accept(self)
