# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_MACTableDialog.ui'
#
# Created: Sat Nov 27 17:51:44 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MACTableDialog(object):
    def setupUi(self, MACTableDialog):
        MACTableDialog.setObjectName("MACTableDialog")
        MACTableDialog.resize(336, 252)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MACTableDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(MACTableDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEditMACTable = QtGui.QPlainTextEdit(MACTableDialog)
        self.plainTextEditMACTable.setObjectName("plainTextEditMACTable")
        self.gridLayout.addWidget(self.plainTextEditMACTable, 0, 0, 1, 3)
        self.pushButtonRefresh = QtGui.QPushButton(MACTableDialog)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.gridLayout.addWidget(self.pushButtonRefresh, 1, 0, 1, 1)
        self.pushButtonClear = QtGui.QPushButton(MACTableDialog)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.gridLayout.addWidget(self.pushButtonClear, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MACTableDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(MACTableDialog)
        QtCore.QMetaObject.connectSlotsByName(MACTableDialog)

    def retranslateUi(self, MACTableDialog):
        MACTableDialog.setWindowTitle(QtGui.QApplication.translate("MACTableDialog", "MAC Address Table", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRefresh.setText(QtGui.QApplication.translate("MACTableDialog", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonClear.setText(QtGui.QApplication.translate("MACTableDialog", "Clear table", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
