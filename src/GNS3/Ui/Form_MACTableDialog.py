# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_MACTableDialog.ui'
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

class Ui_MACTableDialog(object):
    def setupUi(self, MACTableDialog):
        MACTableDialog.setObjectName(_fromUtf8("MACTableDialog"))
        MACTableDialog.resize(336, 252)
        MACTableDialog.setWindowTitle(QtGui.QApplication.translate("MACTableDialog", "MAC Address Table", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MACTableDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(MACTableDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plainTextEditMACTable = QtGui.QPlainTextEdit(MACTableDialog)
        self.plainTextEditMACTable.setObjectName(_fromUtf8("plainTextEditMACTable"))
        self.gridLayout.addWidget(self.plainTextEditMACTable, 0, 0, 1, 3)
        self.pushButtonRefresh = QtGui.QPushButton(MACTableDialog)
        self.pushButtonRefresh.setText(QtGui.QApplication.translate("MACTableDialog", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRefresh.setObjectName(_fromUtf8("pushButtonRefresh"))
        self.gridLayout.addWidget(self.pushButtonRefresh, 1, 0, 1, 1)
        self.pushButtonClear = QtGui.QPushButton(MACTableDialog)
        self.pushButtonClear.setText(QtGui.QApplication.translate("MACTableDialog", "Clear table", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonClear.setObjectName(_fromUtf8("pushButtonClear"))
        self.gridLayout.addWidget(self.pushButtonClear, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MACTableDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(MACTableDialog)
        QtCore.QMetaObject.connectSlotsByName(MACTableDialog)

    def retranslateUi(self, MACTableDialog):
        pass

import svg_resources_rc
