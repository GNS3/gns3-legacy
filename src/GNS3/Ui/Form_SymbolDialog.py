# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_SymbolDialog.ui'
#
# Created: Fri Dec 10 23:05:25 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SymbolDialog(object):
    def setupUi(self, SymbolDialog):
        SymbolDialog.setObjectName("SymbolDialog")
        SymbolDialog.resize(337, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SymbolDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(SymbolDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidgetSymbols = QtGui.QTreeWidget(SymbolDialog)
        self.treeWidgetSymbols.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidgetSymbols.setIconSize(QtCore.QSize(24, 24))
        self.treeWidgetSymbols.setObjectName("treeWidgetSymbols")
        self.verticalLayout.addWidget(self.treeWidgetSymbols)
        self.buttonBox = QtGui.QDialogButtonBox(SymbolDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SymbolDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SymbolDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SymbolDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SymbolDialog)

    def retranslateUi(self, SymbolDialog):
        SymbolDialog.setWindowTitle(QtGui.QApplication.translate("SymbolDialog", "Change symbol", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetSymbols.headerItem().setText(0, QtGui.QApplication.translate("SymbolDialog", "Symbols", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
