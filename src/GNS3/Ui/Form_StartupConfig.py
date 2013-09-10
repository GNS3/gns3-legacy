# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_StartupConfig.ui'
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

class Ui_StartupConfigDialog(object):
    def setupUi(self, StartupConfigDialog):
        StartupConfigDialog.setObjectName(_fromUtf8("StartupConfigDialog"))
        StartupConfigDialog.resize(660, 376)
        StartupConfigDialog.setWindowTitle(QtGui.QApplication.translate("StartupConfigDialog", "Startup-config", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartupConfigDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(StartupConfigDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(StartupConfigDialog)
        self.label.setText(QtGui.QApplication.translate("StartupConfigDialog", "Config file:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditStartupConfig = QtGui.QLineEdit(StartupConfigDialog)
        self.lineEditStartupConfig.setObjectName(_fromUtf8("lineEditStartupConfig"))
        self.gridLayout.addWidget(self.lineEditStartupConfig, 0, 1, 1, 1)
        self.StartupConfigPath_browser = QtGui.QToolButton(StartupConfigDialog)
        self.StartupConfigPath_browser.setText(QtGui.QApplication.translate("StartupConfigDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.StartupConfigPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.StartupConfigPath_browser.setObjectName(_fromUtf8("StartupConfigPath_browser"))
        self.gridLayout.addWidget(self.StartupConfigPath_browser, 0, 2, 1, 1)
        self.LoadStartupConfig = QtGui.QToolButton(StartupConfigDialog)
        self.LoadStartupConfig.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-redo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadStartupConfig.setIcon(icon1)
        self.LoadStartupConfig.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.LoadStartupConfig.setObjectName(_fromUtf8("LoadStartupConfig"))
        self.gridLayout.addWidget(self.LoadStartupConfig, 0, 3, 1, 1)
        self.pushButtonConfigFromNvram = QtGui.QPushButton(StartupConfigDialog)
        self.pushButtonConfigFromNvram.setText(QtGui.QApplication.translate("StartupConfigDialog", "Load config from nvram", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonConfigFromNvram.setObjectName(_fromUtf8("pushButtonConfigFromNvram"))
        self.gridLayout.addWidget(self.pushButtonConfigFromNvram, 0, 5, 1, 1)
        self.EditStartupConfig = QtGui.QPlainTextEdit(StartupConfigDialog)
        self.EditStartupConfig.setObjectName(_fromUtf8("EditStartupConfig"))
        self.gridLayout.addWidget(self.EditStartupConfig, 1, 0, 1, 6)
        self.checkBoxSaveIntoConfigFile = QtGui.QCheckBox(StartupConfigDialog)
        self.checkBoxSaveIntoConfigFile.setText(QtGui.QApplication.translate("StartupConfigDialog", "Save changes into the config file", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSaveIntoConfigFile.setChecked(True)
        self.checkBoxSaveIntoConfigFile.setObjectName(_fromUtf8("checkBoxSaveIntoConfigFile"))
        self.gridLayout.addWidget(self.checkBoxSaveIntoConfigFile, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(StartupConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 6)

        self.retranslateUi(StartupConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StartupConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StartupConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StartupConfigDialog)

    def retranslateUi(self, StartupConfigDialog):
        pass

import svg_resources_rc
