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

import os
import GNS3.Globals as globals
from GNS3.Config.Objects import libraryConf
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from PyQt4 import QtCore, QtGui
from GNS3.Node.DecorativeNode import DecorativeNode
from GNS3.Ui.Form_SymbolManager import Ui_SymbolManager
from GNS3.Utils import translate, fileBrowser


class SymbolManager(QtGui.QDialog, Ui_SymbolManager):
    """ SymbolManager class
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # connections to slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAdd)
        self.connect(self.pushButtonRemove, QtCore.SIGNAL('clicked()'), self.slotRemove)
        self.connect(self.pushButtonApply, QtCore.SIGNAL('clicked()'), self.slotApply)
        self.connect(self.pushButtonAddLibrary, QtCore.SIGNAL('clicked()'), self.slotAddLibrary)
        self.connect(self.pushButtonRemoveLibrary, QtCore.SIGNAL('clicked()'), self.slotRemoveLibrary)
        self.connect(self.toolButtonLibrary, QtCore.SIGNAL('clicked()'), self.slotCallLibraryBrowser)
        self.connect(self.treeWidgetNodes,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotNodeSelectionChanged)
        self.connect(self.treeWidgetSymbols,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotSymbolSelectionChanged)
        self.connect(self.treeWidgetNodes,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'), self.slotNodeSelected)
        self.connect(self.treeWidgetSymbols,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'), self.slotLibrarySelected)

        # populate node type list
        for type in SYMBOL_TYPES.values():
            self.comboBoxNodeType.addItem(translate("nodesDock", type))

        # load current nodes
        self.treeWidgetNodes.clear()
        for symbol in SYMBOLS:
            if not symbol['translated']:
                item = QtGui.QTreeWidgetItem(self.treeWidgetNodes)
                item.setText(0, symbol['name'])
                item.setIcon(0,  QtGui.QIcon(symbol['normal_svg_file']))
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(translate("nodesDock", SYMBOL_TYPES[symbol['object']])))

        # load built-in symbols
        self.treeWidgetSymbols.clear()
        internal_symbols = QtGui.QTreeWidgetItem()
        internal_symbols.setText(0, 'Built-in symbols')
        internal_symbols.setIcon(0,  QtGui.QIcon(':/icons/package.svg'))
        internal_symbols.setFlags(QtCore.Qt.ItemIsEnabled)
        self.treeWidgetSymbols.addTopLevelItem(internal_symbols)
        self.treeWidgetSymbols.expandItem(internal_symbols)
        symbol_resources = QtCore.QResource(":/symbols")
        for symbol in symbol_resources.children():
            symbol = str(symbol)
            if symbol.endswith('.normal.svg'):
                name = symbol[:-11]
                item = QtGui.QTreeWidgetItem(internal_symbols)
                item.setText(0, name)
                item.setIcon(0,  QtGui.QIcon(':/symbols/' + symbol))
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(':/symbols/' + symbol))

        # load libraries
        for (library_name, conf) in globals.GApp.libraries.iteritems():
            self.addLibrarySymbols(library_name, conf.path)

        self.pushButtonAdd.setEnabled(False)
        self.pushButtonRemove.setEnabled(False)

    def slotAdd(self):
        """ Add a symbol to the node list
        """

        symbols = self.treeWidgetSymbols.selectedItems()
        for symbol in symbols:
            name = unicode(symbol.text(0))
            resource_symbol = unicode(symbol.data(0, QtCore.Qt.UserRole).toString())
            if resource_symbol.startswith(':/symbols/'):
                normal_svg_file = resource_symbol
                selected_svg_file = ':/symbols/' + name + '.selected.svg'
            else:
                normal_svg_file = selected_svg_file = resource_symbol

            SYMBOLS.append(
                           {'name': name, 'object': DecorativeNode,
                            'normal_svg_file': normal_svg_file,
                            'select_svg_file': selected_svg_file,
                            'translated': False})

            item = QtGui.QTreeWidgetItem(self.treeWidgetNodes)
            item.setText(0, name)
            item.setIcon(0, symbol.icon(0))
            item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(translate("nodesDock", "Decorative node")))
            item.setSelected(True)

            self.lineEditNodeName.setText(name)
            index = self.comboBoxNodeType.findText(translate("nodesDock", "Decorative node"))
            if index != -1:
                self.comboBoxNodeType.setCurrentIndex(index)
            self.treeWidgetNodes.setCurrentItem(item)

    def slotRemove(self):
        """ Remove a symbol from the node list
        """

        nodes = self.treeWidgetNodes.selectedItems()
        for node in nodes:
            name = unicode(node.text(0))
            self.treeWidgetNodes.takeTopLevelItem(self.treeWidgetNodes.indexOfTopLevelItem(node))
            symbols = list(SYMBOLS)
            index = 0
            for symbol in SYMBOLS:
                if (symbol['translated'] and name == translate("nodesDock", symbol['name'])) or symbol['name'] == name:
                    del SYMBOLS[index]
                index += 1

    def slotApply(self):
        """ Apply settings for a node
        """

        current = self.treeWidgetNodes.currentItem()
        if current and self.lineEditNodeName.text():
            name = unicode(self.lineEditNodeName.text())
            type = unicode(self.comboBoxNodeType.currentText())
            for symbol in SYMBOLS:
                if symbol['name'] == unicode(current.text(0)):
                    symbol['name'] = name
                    for (object, type_name) in SYMBOL_TYPES.iteritems():
                        if translate("nodesDock", type_name) == type:
                            symbol['object'] = object
                            break
                    break
            current.setText(0, name)
            current.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(type))

    def slotNodeSelectionChanged(self):
        """ Check if an entry is selected in the list of nodes
        """

        if len(self.treeWidgetNodes.selectedItems()):
            self.pushButtonAdd.setEnabled(False)
            self.pushButtonRemove.setEnabled(True)
            self.treeWidgetSymbols.clearSelection()

    def slotSymbolSelectionChanged(self):
        """ Check if an entry is selected in the list of symbols
        """

        if len(self.treeWidgetSymbols.selectedItems()):
            self.pushButtonAdd.setEnabled(True)
            self.pushButtonRemove.setEnabled(False)
            self.treeWidgetNodes.clearSelection()

    def slotNodeSelected(self, node):
        """ Load node settings
        """

        self.lineEditNodeName.setText(node.text(0))
        type_name = node.data(0, QtCore.Qt.UserRole).toString()
        index = self.comboBoxNodeType.findText(type_name)
        if index != -1:
            self.comboBoxNodeType.setCurrentIndex(index)
        else:
            print 'Warning: cannot find type ' + type_name

    def slotLibrarySelected(self, item):
        """ Load library settings
        """

        if item and not item.parent():
            path = item.data(0, QtCore.Qt.UserRole).toString()
            self.lineEditLibrary.setText(path)

    def addLibrarySymbols(self, library_name, path):
        """ Add library symbols in the list
        """

        library = QtGui.QTreeWidgetItem()
        library.setText(0, library_name)
        library.setIcon(0,  QtGui.QIcon(':/icons/package.svg'))
        library.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(path))
        self.treeWidgetSymbols.addTopLevelItem(library)
        resources = QtCore.QResource(":/" + library_name)
        for symbol in resources.children():
            item = QtGui.QTreeWidgetItem(library)
            item.setText(0, symbol)
            item.setIcon(0, QtGui.QIcon(':/' + library_name + '/' + symbol))
            item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(':/' + library_name + '/' + symbol))

    def slotAddLibrary(self):
        """ Add a library
        """

        path = unicode(self.lineEditLibrary.text())
        if not path:
            return
        library_name = os.path.basename(path)
        if len(self.treeWidgetSymbols.findItems(library_name, QtCore.Qt.MatchFixedString)):
            QtGui.QMessageBox.critical(self, translate("SymbolManager", "Library"), translate("SymbolManager", "This library is already loaded: %s") % library_name)
            return
        if not QtCore.QResource.registerResource(path, ":/" + library_name):
            QtGui.QMessageBox.critical(self, translate("SymbolManager", "Library"), translate("SymbolManager", "Can't open library: %s") % path)
            return

        self.addLibrarySymbols(library_name, path)
        conf = libraryConf()
        conf.path = path
        globals.GApp.libraries[library_name] = conf

    def slotRemoveLibrary(self):
        """ Remove a library
        """

        path = unicode(self.lineEditLibrary.text())
        if not path:
            return
        library_name = os.path.basename(path)
        if not QtCore.QResource.unregisterResource(path, ":/" + library_name):
            QtGui.QMessageBox.critical(self, translate("SymbolManagement", "Library"), translate("SymbolManager", "Can't remove library: %s") % path)
            return

        library = self.treeWidgetSymbols.findItems(library_name, QtCore.Qt.MatchFixedString)[0]
        self.treeWidgetSymbols.takeTopLevelItem(self.treeWidgetSymbols.indexOfTopLevelItem(library))
        del globals.GApp.libraries[library_name]

    def slotCallLibraryBrowser(self):
        """ Call a file system browser to select a library
        """
        fb = fileBrowser(translate('SymbolManagement', 'Library path'), directory=globals.GApp.systconf['general'].project_path, parent=self)
        (path, selected) = fb.getFile()

        if path is not None and path != '':
            self.lineEditLibrary.clear()
            self.lineEditLibrary.setText(os.path.normpath(path))
