# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Tue Sep 18 17:35:31 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,163).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(0,10,75,22))
        self.label.setObjectName("label")

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)
        self.langsBox.setGeometry(QtCore.QRect(80,10,321,22))
        self.langsBox.setObjectName("langsBox")

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))

