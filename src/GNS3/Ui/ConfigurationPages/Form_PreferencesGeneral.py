# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sun Aug 17 18:43:21 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,432,491).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.label_4 = QtGui.QLabel(PreferencesGeneral)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.lineEditTermCommand = QtGui.QLineEdit(PreferencesGeneral)
        self.lineEditTermCommand.setObjectName("lineEditTermCommand")
        self.vboxlayout.addWidget(self.lineEditTermCommand)

        self.checkBoxUseShell = QtGui.QCheckBox(PreferencesGeneral)
        self.checkBoxUseShell.setChecked(True)
        self.checkBoxUseShell.setObjectName("checkBoxUseShell")
        self.vboxlayout.addWidget(self.checkBoxUseShell)

        self.groupBox_2 = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        self.ProjectPath = QtGui.QLineEdit(self.groupBox_2)
        self.ProjectPath.setObjectName("ProjectPath")
        self.gridlayout.addWidget(self.ProjectPath,1,0,1,1)

        self.ProjectPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.ProjectPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ProjectPath_browser.setObjectName("ProjectPath_browser")
        self.gridlayout.addWidget(self.ProjectPath_browser,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.IOSPath = QtGui.QLineEdit(self.groupBox_2)
        self.IOSPath.setObjectName("IOSPath")
        self.gridlayout.addWidget(self.IOSPath,3,0,1,1)

        self.IOSPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.IOSPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.IOSPath_browser.setObjectName("IOSPath_browser")
        self.gridlayout.addWidget(self.IOSPath_browser,3,1,1,1)
        self.vboxlayout.addWidget(self.groupBox_2)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        self.groupBox_3 = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox_3.setObjectName("groupBox_3")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.hboxlayout.setObjectName("hboxlayout")

        self.labelConfigurationPath = QtGui.QLabel(self.groupBox_3)
        self.labelConfigurationPath.setObjectName("labelConfigurationPath")
        self.hboxlayout.addWidget(self.labelConfigurationPath)

        spacerItem = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_ClearConfiguration = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_ClearConfiguration.setObjectName("pushButton_ClearConfiguration")
        self.hboxlayout.addWidget(self.pushButton_ClearConfiguration)
        self.vboxlayout.addWidget(self.groupBox_3)

        spacerItem1 = QtGui.QSpacerItem(414,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesGeneral", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxUseShell.setText(QtGui.QApplication.translate("PreferencesGeneral", "Launch this command using the system default shell", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesGeneral", "Project directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProjectPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesGeneral", "IOS/PIX directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.IOSPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Configuration file", None, QtGui.QApplication.UnicodeUTF8))
        self.labelConfigurationPath.setText(QtGui.QApplication.translate("PreferencesGeneral", "Unknown location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ClearConfiguration.setText(QtGui.QApplication.translate("PreferencesGeneral", "&Clear it", None, QtGui.QApplication.UnicodeUTF8))

