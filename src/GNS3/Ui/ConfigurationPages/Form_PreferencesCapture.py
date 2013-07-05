# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesCapture.ui'
#
# Created: Fri Jul  5 13:39:32 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PreferencesCapture(object):
    def setupUi(self, PreferencesCapture):
        PreferencesCapture.setObjectName(_fromUtf8("PreferencesCapture"))
        PreferencesCapture.resize(550, 373)
        PreferencesCapture.setWindowTitle(QtGui.QApplication.translate("PreferencesCapture", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.vboxlayout = QtGui.QVBoxLayout(PreferencesCapture)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(PreferencesCapture)
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesCapture", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridlayout = QtGui.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setEnabled(True)
        self.label.setText(QtGui.QApplication.translate("PreferencesCapture", "Working directory for capture files:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 2, 0, 1, 2)
        self.CaptureWorkingDirectory = QtGui.QLineEdit(self.groupBox)
        self.CaptureWorkingDirectory.setObjectName(_fromUtf8("CaptureWorkingDirectory"))
        self.gridlayout.addWidget(self.CaptureWorkingDirectory, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setEnabled(True)
        self.label_2.setText(QtGui.QApplication.translate("PreferencesCapture", "Command to launch Wireshark or a capture file reader:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 4, 0, 1, 2)
        self.CaptureCommand = QtGui.QLineEdit(self.groupBox)
        self.CaptureCommand.setObjectName(_fromUtf8("CaptureCommand"))
        self.gridlayout.addWidget(self.CaptureCommand, 5, 0, 1, 2)
        self.checkBoxStartCaptureCommand = QtGui.QCheckBox(self.groupBox)
        self.checkBoxStartCaptureCommand.setEnabled(True)
        self.checkBoxStartCaptureCommand.setText(QtGui.QApplication.translate("PreferencesCapture", "Automatically start the command when capturing", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxStartCaptureCommand.setChecked(False)
        self.checkBoxStartCaptureCommand.setObjectName(_fromUtf8("checkBoxStartCaptureCommand"))
        self.gridlayout.addWidget(self.checkBoxStartCaptureCommand, 6, 0, 1, 2)
        self.comboBoxPresets = QtGui.QComboBox(self.groupBox)
        self.comboBoxPresets.setObjectName(_fromUtf8("comboBoxPresets"))
        self.gridlayout.addWidget(self.comboBoxPresets, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("PreferencesCapture", "Default Presets:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.pushButtonUsePresets = QtGui.QPushButton(self.groupBox)
        self.pushButtonUsePresets.setText(QtGui.QApplication.translate("PreferencesCapture", "Use", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUsePresets.setObjectName(_fromUtf8("pushButtonUsePresets"))
        self.gridlayout.addWidget(self.pushButtonUsePresets, 1, 1, 1, 1)
        self.CaptureWorkingDirectory_Browser = QtGui.QToolButton(self.groupBox)
        self.CaptureWorkingDirectory_Browser.setText(QtGui.QApplication.translate("PreferencesCapture", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.CaptureWorkingDirectory_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.CaptureWorkingDirectory_Browser.setObjectName(_fromUtf8("CaptureWorkingDirectory_Browser"))
        self.gridlayout.addWidget(self.CaptureWorkingDirectory_Browser, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setToolTip(QtGui.QApplication.translate("PreferencesCapture", "Hint: To actually start capturing traffic, right click on link\'s small colored circle.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesCapture", "Hint: To actually start capturing traffic, right click on link\'s small colored circle\n"
"or the link itself.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 8, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setText(QtGui.QApplication.translate("PreferencesCapture", "%c = capture file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.vboxlayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 101, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesCapture)
        QtCore.QMetaObject.connectSlotsByName(PreferencesCapture)

    def retranslateUi(self, PreferencesCapture):
        pass

