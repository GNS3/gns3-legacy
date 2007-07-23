# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Widget_SystemGeneral.ui'
#
# Created: Mon Jul 23 22:12:01 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SystemGeneral(object):
    def setupUi(self, SystemGeneral):
        SystemGeneral.setObjectName("SystemGeneral")
        SystemGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,163).size()).expandedTo(SystemGeneral.minimumSizeHint()))

        self.label = QtGui.QLabel(SystemGeneral)
        self.label.setEnabled(False)
        self.label.setGeometry(QtCore.QRect(0,10,71,22))
        self.label.setObjectName("label")

        self.comboBox = QtGui.QComboBox(SystemGeneral)
        self.comboBox.setEnabled(False)
        self.comboBox.setGeometry(QtCore.QRect(80,10,321,22))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(SystemGeneral)
        QtCore.QMetaObject.connectSlotsByName(SystemGeneral)

    def retranslateUi(self, SystemGeneral):
        SystemGeneral.setWindowTitle(QtGui.QApplication.translate("SystemGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SystemGeneral", "Langage:", None, QtGui.QApplication.UnicodeUTF8))

