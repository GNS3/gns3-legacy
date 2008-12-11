# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Thu Dec 11 23:13:44 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,511,480).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(PreferencesGeneral)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout = QtGui.QGridLayout(self.tab)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.tab)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.langsBox = QtGui.QComboBox(self.tab)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.gridlayout.addWidget(self.langsBox,1,0,1,1)

        self.checkBoxProjectDialog = QtGui.QCheckBox(self.tab)
        self.checkBoxProjectDialog.setChecked(True)
        self.checkBoxProjectDialog.setObjectName("checkBoxProjectDialog")
        self.gridlayout.addWidget(self.checkBoxProjectDialog,2,0,1,1)

        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.lineEditTermCommand = QtGui.QLineEdit(self.tab)
        self.lineEditTermCommand.setObjectName("lineEditTermCommand")
        self.gridlayout.addWidget(self.lineEditTermCommand,4,0,1,1)

        self.checkBoxUseShell = QtGui.QCheckBox(self.tab)
        self.checkBoxUseShell.setChecked(True)
        self.checkBoxUseShell.setObjectName("checkBoxUseShell")
        self.gridlayout.addWidget(self.checkBoxUseShell,5,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,0,0,1,1)

        self.ProjectPath = QtGui.QLineEdit(self.groupBox_2)
        self.ProjectPath.setObjectName("ProjectPath")
        self.gridlayout1.addWidget(self.ProjectPath,1,0,1,1)

        self.ProjectPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.ProjectPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ProjectPath_browser.setObjectName("ProjectPath_browser")
        self.gridlayout1.addWidget(self.ProjectPath_browser,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,2,0,1,1)

        self.IOSPath = QtGui.QLineEdit(self.groupBox_2)
        self.IOSPath.setObjectName("IOSPath")
        self.gridlayout1.addWidget(self.IOSPath,3,0,1,1)

        self.IOSPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.IOSPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.IOSPath_browser.setObjectName("IOSPath_browser")
        self.gridlayout1.addWidget(self.IOSPath_browser,3,1,1,1)
        self.gridlayout.addWidget(self.groupBox_2,6,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.tab)
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
        self.gridlayout.addWidget(self.groupBox_3,7,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(471,21,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,8,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,0,0,1,1)

        self.workspaceWidth = QtGui.QSpinBox(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workspaceWidth.sizePolicy().hasHeightForWidth())
        self.workspaceWidth.setSizePolicy(sizePolicy)
        self.workspaceWidth.setMinimum(500)
        self.workspaceWidth.setMaximum(1000000)
        self.workspaceWidth.setSingleStep(100)
        self.workspaceWidth.setProperty("value",QtCore.QVariant(2000))
        self.workspaceWidth.setObjectName("workspaceWidth")
        self.gridlayout2.addWidget(self.workspaceWidth,0,1,1,1)

        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout2.addWidget(self.label_6,1,0,1,1)

        self.workspaceHeight = QtGui.QSpinBox(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workspaceHeight.sizePolicy().hasHeightForWidth())
        self.workspaceHeight.setSizePolicy(sizePolicy)
        self.workspaceHeight.setMinimum(500)
        self.workspaceHeight.setMaximum(1000000)
        self.workspaceHeight.setSingleStep(100)
        self.workspaceHeight.setProperty("value",QtCore.QVariant(1000))
        self.workspaceHeight.setObjectName("workspaceHeight")
        self.gridlayout2.addWidget(self.workspaceHeight,1,1,1,1)

        self.checkBoxDrawRectangle = QtGui.QCheckBox(self.tab_2)
        self.checkBoxDrawRectangle.setChecked(True)
        self.checkBoxDrawRectangle.setObjectName("checkBoxDrawRectangle")
        self.gridlayout2.addWidget(self.checkBoxDrawRectangle,2,0,1,2)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.tab_2)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.gridlayout2.addWidget(self.checkBoxManualConnections,3,0,1,2)

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.tab_2)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.gridlayout2.addWidget(self.checkBoxShowStatusPoints,4,0,1,2)

        spacerItem2 = QtGui.QSpacerItem(20,251,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem2,5,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(PreferencesGeneral)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxProjectDialog.setText(QtGui.QApplication.translate("PreferencesGeneral", "Launch the project dialog at startup", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesGeneral", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxUseShell.setText(QtGui.QApplication.translate("PreferencesGeneral", "Launch this command using the system default shell", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesGeneral", "Project directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProjectPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesGeneral", "IOS/PIX directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.IOSPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Configuration file", None, QtGui.QApplication.UnicodeUTF8))
        self.labelConfigurationPath.setText(QtGui.QApplication.translate("PreferencesGeneral", "Unknown location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ClearConfiguration.setText(QtGui.QApplication.translate("PreferencesGeneral", "&Clear it", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PreferencesGeneral", "General Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PreferencesGeneral", "Workspace width:", None, QtGui.QApplication.UnicodeUTF8))
        self.workspaceWidth.setSuffix(QtGui.QApplication.translate("PreferencesGeneral", " px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PreferencesGeneral", "Workspace height:", None, QtGui.QApplication.UnicodeUTF8))
        self.workspaceHeight.setSuffix(QtGui.QApplication.translate("PreferencesGeneral", " px", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDrawRectangle.setText(QtGui.QApplication.translate("PreferencesGeneral", "Draw a rectangle when an item is selected", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PreferencesGeneral", "GUI Settings", None, QtGui.QApplication.UnicodeUTF8))

