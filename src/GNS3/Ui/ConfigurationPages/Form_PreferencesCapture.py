# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesCapture.ui'
#
# Created: Sat Feb 20 17:32:35 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesCapture(object):
    def setupUi(self, PreferencesCapture):
        PreferencesCapture.setObjectName("PreferencesCapture")
        PreferencesCapture.resize(398, 308)
        self.vboxlayout = QtGui.QVBoxLayout(PreferencesCapture)
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox = QtGui.QGroupBox(PreferencesCapture)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 2)
        self.CaptureWorkingDirectory = QtGui.QLineEdit(self.groupBox)
        self.CaptureWorkingDirectory.setObjectName("CaptureWorkingDirectory")
        self.gridlayout.addWidget(self.CaptureWorkingDirectory, 1, 0, 1, 1)
        self.CaptureWorkingDirectory_Browser = QtGui.QToolButton(self.groupBox)
        self.CaptureWorkingDirectory_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.CaptureWorkingDirectory_Browser.setObjectName("CaptureWorkingDirectory_Browser")
        self.gridlayout.addWidget(self.CaptureWorkingDirectory_Browser, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setEnabled(True)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.CaptureCommand = QtGui.QLineEdit(self.groupBox)
        self.CaptureCommand.setObjectName("CaptureCommand")
        self.gridlayout.addWidget(self.CaptureCommand, 3, 0, 1, 2)
        self.checkBoxStartCaptureCommand = QtGui.QCheckBox(self.groupBox)
        self.checkBoxStartCaptureCommand.setChecked(True)
        self.checkBoxStartCaptureCommand.setObjectName("checkBoxStartCaptureCommand")
        self.gridlayout.addWidget(self.checkBoxStartCaptureCommand, 4, 0, 1, 2)
        self.vboxlayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 101, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesCapture)
        QtCore.QMetaObject.connectSlotsByName(PreferencesCapture)

    def retranslateUi(self, PreferencesCapture):
        PreferencesCapture.setWindowTitle(QtGui.QApplication.translate("PreferencesCapture", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesCapture", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesCapture", "Working directory for capture files:", None, QtGui.QApplication.UnicodeUTF8))
        self.CaptureWorkingDirectory_Browser.setText(QtGui.QApplication.translate("PreferencesCapture", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesCapture", "Command to launch Wireshark or a capture file reader:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxStartCaptureCommand.setText(QtGui.QApplication.translate("PreferencesCapture", "Automatically start the command when capturing", None, QtGui.QApplication.UnicodeUTF8))

