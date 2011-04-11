# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_IDLEPCDialog.ui'
#
# Created: Mon Apr 11 15:55:32 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IDLEPCDialog(object):
    def setupUi(self, IDLEPCDialog):
        IDLEPCDialog.setObjectName(_fromUtf8("IDLEPCDialog"))
        IDLEPCDialog.resize(316, 108)
        IDLEPCDialog.setMinimumSize(QtCore.QSize(316, 108))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IDLEPCDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(IDLEPCDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(IDLEPCDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(IDLEPCDialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(IDLEPCDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(IDLEPCDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IDLEPCDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IDLEPCDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IDLEPCDialog)

    def retranslateUi(self, IDLEPCDialog):
        IDLEPCDialog.setWindowTitle(QtGui.QApplication.translate("IDLEPCDialog", "IDLE PC values", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IDLEPCDialog", "Potentially better idlepc values marked with \'*\'", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
