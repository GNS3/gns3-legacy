# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_CalcIDLEPCDialog.ui'
#
# Created: Sat Dec 01 18:27:17 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CalcIDLEPCDialog(object):
    def setupUi(self, CalcIDLEPCDialog):
        CalcIDLEPCDialog.setObjectName(_fromUtf8("CalcIDLEPCDialog"))
        CalcIDLEPCDialog.setWindowModality(QtCore.Qt.WindowModal)
        CalcIDLEPCDialog.resize(400, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalcIDLEPCDialog.sizePolicy().hasHeightForWidth())
        CalcIDLEPCDialog.setSizePolicy(sizePolicy)
        CalcIDLEPCDialog.setMinimumSize(QtCore.QSize(400, 300))
        CalcIDLEPCDialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CalcIDLEPCDialog.setWindowIcon(icon)
        CalcIDLEPCDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(CalcIDLEPCDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(CalcIDLEPCDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.progressBar = QtGui.QProgressBar(CalcIDLEPCDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(CalcIDLEPCDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.retranslateUi(CalcIDLEPCDialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CalcIDLEPCDialog.cancel)
        QtCore.QMetaObject.connectSlotsByName(CalcIDLEPCDialog)

    def retranslateUi(self, CalcIDLEPCDialog):
        CalcIDLEPCDialog.setWindowTitle(QtGui.QApplication.translate("CalcIDLEPCDialog", "Idle Pc Calculation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("CalcIDLEPCDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
