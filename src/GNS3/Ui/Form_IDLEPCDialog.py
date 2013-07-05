# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_IDLEPCDialog.ui'
#
# Created: Fri Jul  5 13:39:29 2013
#      by: PyQt4 UI code generator 4.8.6
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
        IDLEPCDialog.resize(410, 108)
        IDLEPCDialog.setMinimumSize(QtCore.QSize(316, 108))
        IDLEPCDialog.setWindowTitle(QtGui.QApplication.translate("IDLEPCDialog", "IDLE PC values", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IDLEPCDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(IDLEPCDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(IDLEPCDialog)
        self.label.setText(QtGui.QApplication.translate("IDLEPCDialog", "Potentially better idlepc values are marked with \'*\'", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(IDLEPCDialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(IDLEPCDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(IDLEPCDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IDLEPCDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IDLEPCDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IDLEPCDialog)

    def retranslateUi(self, IDLEPCDialog):
        pass

import svg_resources_rc
