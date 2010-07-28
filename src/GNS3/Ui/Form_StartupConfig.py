# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_StartupConfig.ui'
#
# Created: Wed Jul 28 11:54:24 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StartupConfigDialog(object):
    def setupUi(self, StartupConfigDialog):
        StartupConfigDialog.setObjectName("StartupConfigDialog")
        StartupConfigDialog.resize(660, 376)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartupConfigDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(StartupConfigDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(StartupConfigDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditStartupConfig = QtGui.QLineEdit(StartupConfigDialog)
        self.lineEditStartupConfig.setObjectName("lineEditStartupConfig")
        self.gridLayout.addWidget(self.lineEditStartupConfig, 0, 1, 1, 1)
        self.StartupConfigPath_browser = QtGui.QToolButton(StartupConfigDialog)
        self.StartupConfigPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.StartupConfigPath_browser.setObjectName("StartupConfigPath_browser")
        self.gridLayout.addWidget(self.StartupConfigPath_browser, 0, 2, 1, 1)
        self.LoadStartupConfig = QtGui.QToolButton(StartupConfigDialog)
        self.LoadStartupConfig.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/edit-redo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadStartupConfig.setIcon(icon1)
        self.LoadStartupConfig.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.LoadStartupConfig.setObjectName("LoadStartupConfig")
        self.gridLayout.addWidget(self.LoadStartupConfig, 0, 3, 1, 1)
        self.pushButtonConfigFromNvram = QtGui.QPushButton(StartupConfigDialog)
        self.pushButtonConfigFromNvram.setObjectName("pushButtonConfigFromNvram")
        self.gridLayout.addWidget(self.pushButtonConfigFromNvram, 0, 5, 1, 1)
        self.EditStartupConfig = QtGui.QPlainTextEdit(StartupConfigDialog)
        self.EditStartupConfig.setObjectName("EditStartupConfig")
        self.gridLayout.addWidget(self.EditStartupConfig, 1, 0, 1, 6)
        self.checkBoxSaveIntoConfigFile = QtGui.QCheckBox(StartupConfigDialog)
        self.checkBoxSaveIntoConfigFile.setChecked(True)
        self.checkBoxSaveIntoConfigFile.setObjectName("checkBoxSaveIntoConfigFile")
        self.gridLayout.addWidget(self.checkBoxSaveIntoConfigFile, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(StartupConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 6)

        self.retranslateUi(StartupConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), StartupConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), StartupConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StartupConfigDialog)

    def retranslateUi(self, StartupConfigDialog):
        StartupConfigDialog.setWindowTitle(QtGui.QApplication.translate("StartupConfigDialog", "Startup-config", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StartupConfigDialog", "Config file:", None, QtGui.QApplication.UnicodeUTF8))
        self.StartupConfigPath_browser.setText(QtGui.QApplication.translate("StartupConfigDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonConfigFromNvram.setText(QtGui.QApplication.translate("StartupConfigDialog", "Load config from nvram", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSaveIntoConfigFile.setText(QtGui.QApplication.translate("StartupConfigDialog", "Save changes into the config file", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
