# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_SymbolDialog.ui'
#
# Created: Mon Sep  9 21:29:21 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SymbolDialog(object):
    def setupUi(self, SymbolDialog):
        SymbolDialog.setObjectName(_fromUtf8("SymbolDialog"))
        SymbolDialog.resize(337, 490)
        SymbolDialog.setWindowTitle(QtGui.QApplication.translate("SymbolDialog", "Change symbol", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SymbolDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(SymbolDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidgetSymbols = QtGui.QTreeWidget(SymbolDialog)
        self.treeWidgetSymbols.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidgetSymbols.setIconSize(QtCore.QSize(24, 24))
        self.treeWidgetSymbols.setObjectName(_fromUtf8("treeWidgetSymbols"))
        self.treeWidgetSymbols.headerItem().setText(0, QtGui.QApplication.translate("SymbolDialog", "Symbols", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout.addWidget(self.treeWidgetSymbols)
        self.buttonBox = QtGui.QDialogButtonBox(SymbolDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SymbolDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SymbolDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SymbolDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SymbolDialog)

    def retranslateUi(self, SymbolDialog):
        pass

import svg_resources_rc
