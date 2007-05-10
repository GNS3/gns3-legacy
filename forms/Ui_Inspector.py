# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Inspector.ui'
#
# Created: Thu May 10 10:26:41 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_FormInspector(object):
    def setupUi(self, FormInspector):
        FormInspector.setObjectName("FormInspector")
        FormInspector.resize(QtCore.QSize(QtCore.QRect(0,0,696,368).size()).expandedTo(FormInspector.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(FormInspector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(FormInspector)
        self.tabWidget.setObjectName("tabWidget")

        self.Console = QtGui.QWidget()
        self.Console.setObjectName("Console")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.Console)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.labelStatus = QtGui.QLabel(self.Console)
        self.labelStatus.setPixmap(QtGui.QPixmap("../svg/icons/led_red.svg"))
        self.labelStatus.setScaledContents(False)
        self.labelStatus.setObjectName("labelStatus")
        self.hboxlayout.addWidget(self.labelStatus)

        spacerItem = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton_Start = QtGui.QPushButton(self.Console)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.hboxlayout.addWidget(self.pushButton_Start)

        self.pushButton_Shutdown = QtGui.QPushButton(self.Console)
        self.pushButton_Shutdown.setEnabled(False)
        self.pushButton_Shutdown.setObjectName("pushButton_Shutdown")
        self.hboxlayout.addWidget(self.pushButton_Shutdown)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.textEditConsole = Console(self.Console)

        font = QtGui.QFont(self.textEditConsole.font())
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(10)
        self.textEditConsole.setFont(font)
        self.textEditConsole.setObjectName("textEditConsole")
        self.vboxlayout1.addWidget(self.textEditConsole)
        self.tabWidget.addTab(self.Console,"")

        self.General = QtGui.QWidget()
        self.General.setObjectName("General")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.General)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.General)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.label_3 = QtGui.QLabel(self.General)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.lineEditMask = QtGui.QLineEdit(self.General)
        self.lineEditMask.setObjectName("lineEditMask")
        self.gridlayout.addWidget(self.lineEditMask,2,1,1,1)

        self.lineEditIP = QtGui.QLineEdit(self.General)
        self.lineEditIP.setObjectName("lineEditIP")
        self.gridlayout.addWidget(self.lineEditIP,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,2,1,1)

        self.label_4 = QtGui.QLabel(self.General)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.lineEditGateway = QtGui.QLineEdit(self.General)
        self.lineEditGateway.setObjectName("lineEditGateway")
        self.gridlayout.addWidget(self.lineEditGateway,3,1,1,1)

        self.lineEditHostname = QtGui.QLineEdit(self.General)
        self.lineEditHostname.setObjectName("lineEditHostname")
        self.gridlayout.addWidget(self.lineEditHostname,0,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,0,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,3,2,1,1)

        self.label_2 = QtGui.QLabel(self.General)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(291,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,2,2,1,1)
        self.vboxlayout2.addLayout(self.gridlayout)

        spacerItem5 = QtGui.QSpacerItem(20,101,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem5)
        self.tabWidget.addTab(self.General,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.toolBox = QtGui.QToolBox(self.tab)
        self.toolBox.setGeometry(QtCore.QRect(370,10,301,251))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setObjectName("toolBox")

        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0,0,301,189))
        self.page_3.setObjectName("page_3")

        self.gridlayout1 = QtGui.QGridLayout(self.page_3)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem6 = QtGui.QSpacerItem(51,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem6,0,3,5,1)

        self.label_7 = QtGui.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,0,0,1,1)

        self.spinBoxPcmciaDisk1Size = QtGui.QSpinBox(self.page_3)
        self.spinBoxPcmciaDisk1Size.setSingleStep(4)
        self.spinBoxPcmciaDisk1Size.setObjectName("spinBoxPcmciaDisk1Size")
        self.gridlayout1.addWidget(self.spinBoxPcmciaDisk1Size,4,2,1,1)

        spacerItem7 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem7,1,1,1,1)

        self.spinBoxPcmciaDisk0Size = QtGui.QSpinBox(self.page_3)
        self.spinBoxPcmciaDisk0Size.setSingleStep(4)
        self.spinBoxPcmciaDisk0Size.setObjectName("spinBoxPcmciaDisk0Size")
        self.gridlayout1.addWidget(self.spinBoxPcmciaDisk0Size,3,2,1,1)

        self.spinBoxNvramSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxNvramSize.setMaximum(4096)
        self.spinBoxNvramSize.setSingleStep(4)
        self.spinBoxNvramSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxNvramSize.setObjectName("spinBoxNvramSize")
        self.gridlayout1.addWidget(self.spinBoxNvramSize,2,2,1,1)

        spacerItem8 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem8,2,1,1,1)

        self.spinBoxRomSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxRomSize.setMaximum(4096)
        self.spinBoxRomSize.setSingleStep(4)
        self.spinBoxRomSize.setProperty("value",QtCore.QVariant(4))
        self.spinBoxRomSize.setObjectName("spinBoxRomSize")
        self.gridlayout1.addWidget(self.spinBoxRomSize,1,2,1,1)

        self.label_11 = QtGui.QLabel(self.page_3)
        self.label_11.setObjectName("label_11")
        self.gridlayout1.addWidget(self.label_11,4,0,1,2)

        self.label_10 = QtGui.QLabel(self.page_3)
        self.label_10.setObjectName("label_10")
        self.gridlayout1.addWidget(self.label_10,3,0,1,2)

        self.spinBoxRamSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxRamSize.setMaximum(4096)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxRamSize.setObjectName("spinBoxRamSize")
        self.gridlayout1.addWidget(self.spinBoxRamSize,0,2,1,1)

        self.label_9 = QtGui.QLabel(self.page_3)
        self.label_9.setObjectName("label_9")
        self.gridlayout1.addWidget(self.label_9,2,0,1,1)

        self.label_8 = QtGui.QLabel(self.page_3)
        self.label_8.setObjectName("label_8")
        self.gridlayout1.addWidget(self.label_8,1,0,1,1)

        spacerItem9 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem9,0,1,1,1)
        self.toolBox.addItem(self.page_3,"")

        self.page_5 = QtGui.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0,0,301,189))
        self.page_5.setObjectName("page_5")

        self.gridlayout2 = QtGui.QGridLayout(self.page_5)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_17 = QtGui.QLabel(self.page_5)
        self.label_17.setObjectName("label_17")
        self.gridlayout2.addWidget(self.label_17,2,0,1,2)

        spacerItem10 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem10,1,4,1,1)

        self.lineEditConfreg = QtGui.QLineEdit(self.page_5)
        self.lineEditConfreg.setObjectName("lineEditConfreg")
        self.gridlayout2.addWidget(self.lineEditConfreg,1,3,1,1)

        spacerItem11 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem11,1,1,1,2)

        self.label_16 = QtGui.QLabel(self.page_5)
        self.label_16.setObjectName("label_16")
        self.gridlayout2.addWidget(self.label_16,1,0,1,1)

        spacerItem12 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem12,0,4,1,1)

        self.checkBoxMapped = QtGui.QCheckBox(self.page_5)
        self.checkBoxMapped.setChecked(True)
        self.checkBoxMapped.setObjectName("checkBoxMapped")
        self.gridlayout2.addWidget(self.checkBoxMapped,0,0,1,4)

        spacerItem13 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem13,3,4,1,1)

        spacerItem14 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem14,2,4,1,1)

        self.spinBoxIomem = QtGui.QSpinBox(self.page_5)
        self.spinBoxIomem.setMaximum(100)
        self.spinBoxIomem.setProperty("value",QtCore.QVariant(5))
        self.spinBoxIomem.setObjectName("spinBoxIomem")
        self.gridlayout2.addWidget(self.spinBoxIomem,3,3,1,1)

        spacerItem15 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem15,3,1,1,2)

        self.label_14 = QtGui.QLabel(self.page_5)
        self.label_14.setObjectName("label_14")
        self.gridlayout2.addWidget(self.label_14,3,0,1,1)

        self.spinBoxExecArea = QtGui.QSpinBox(self.page_5)
        self.spinBoxExecArea.setMaximum(4096)
        self.spinBoxExecArea.setSingleStep(4)
        self.spinBoxExecArea.setProperty("value",QtCore.QVariant(64))
        self.spinBoxExecArea.setObjectName("spinBoxExecArea")
        self.gridlayout2.addWidget(self.spinBoxExecArea,2,3,1,1)

        spacerItem16 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem16,2,2,1,1)
        self.toolBox.addItem(self.page_5,"")

        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10,10,341,251))
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout3.addWidget(self.label_5,0,0,1,1)

        self.comboBoxIOS = QtGui.QComboBox(self.groupBox)
        self.comboBoxIOS.setObjectName("comboBoxIOS")
        self.gridlayout3.addWidget(self.comboBoxIOS,0,1,1,1)

        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridlayout3.addWidget(self.label_13,1,0,1,1)

        spacerItem17 = QtGui.QSpacerItem(32,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem17,0,2,2,1)

        self.lineEditConsolePort = QtGui.QLineEdit(self.groupBox)
        self.lineEditConsolePort.setObjectName("lineEditConsolePort")
        self.gridlayout3.addWidget(self.lineEditConsolePort,1,1,1,1)
        self.vboxlayout3.addLayout(self.gridlayout3)

        spacerItem18 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout3.addItem(spacerItem18)

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.pushButtonStartupConfig = QtGui.QPushButton(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStartupConfig.sizePolicy().hasHeightForWidth())
        self.pushButtonStartupConfig.setSizePolicy(sizePolicy)
        self.pushButtonStartupConfig.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonStartupConfig.setObjectName("pushButtonStartupConfig")
        self.gridlayout4.addWidget(self.pushButtonStartupConfig,0,2,1,1)

        self.lineEditWorkingDirectory = QtGui.QLineEdit(self.groupBox)
        self.lineEditWorkingDirectory.setObjectName("lineEditWorkingDirectory")
        self.gridlayout4.addWidget(self.lineEditWorkingDirectory,1,1,1,1)

        self.label_18 = QtGui.QLabel(self.groupBox)
        self.label_18.setObjectName("label_18")
        self.gridlayout4.addWidget(self.label_18,0,0,1,1)

        self.label_19 = QtGui.QLabel(self.groupBox)
        self.label_19.setObjectName("label_19")
        self.gridlayout4.addWidget(self.label_19,1,0,1,1)

        self.lineEditStartupConfig = QtGui.QLineEdit(self.groupBox)
        self.lineEditStartupConfig.setObjectName("lineEditStartupConfig")
        self.gridlayout4.addWidget(self.lineEditStartupConfig,0,1,1,1)

        self.pushButtonWorkingDirectory = QtGui.QPushButton(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonWorkingDirectory.sizePolicy().hasHeightForWidth())
        self.pushButtonWorkingDirectory.setSizePolicy(sizePolicy)
        self.pushButtonWorkingDirectory.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonWorkingDirectory.setObjectName("pushButtonWorkingDirectory")
        self.gridlayout4.addWidget(self.pushButtonWorkingDirectory,1,2,1,1)
        self.vboxlayout3.addLayout(self.gridlayout4)

        spacerItem19 = QtGui.QSpacerItem(20,31,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout3.addItem(spacerItem19)

        self.widget = QtGui.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(18,270,641,34))
        self.widget.setObjectName("widget")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem20 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem20)

        self.buttonBoxIOSConfig = QtGui.QDialogButtonBox(self.widget)
        self.buttonBoxIOSConfig.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.buttonBoxIOSConfig.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxIOSConfig.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton)
        self.buttonBoxIOSConfig.setObjectName("buttonBoxIOSConfig")
        self.hboxlayout1.addWidget(self.buttonBoxIOSConfig)
        self.tabWidget.addTab(self.tab,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(FormInspector)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormInspector)
        FormInspector.setTabOrder(self.textEditConsole,self.pushButton_Start)
        FormInspector.setTabOrder(self.pushButton_Start,self.pushButton_Shutdown)
        FormInspector.setTabOrder(self.pushButton_Shutdown,self.tabWidget)
        FormInspector.setTabOrder(self.tabWidget,self.lineEditGateway)
        FormInspector.setTabOrder(self.lineEditGateway,self.lineEditIP)
        FormInspector.setTabOrder(self.lineEditIP,self.lineEditMask)
        FormInspector.setTabOrder(self.lineEditMask,self.lineEditHostname)

    def retranslateUi(self, FormInspector):
        FormInspector.setWindowTitle(QtGui.QApplication.translate("FormInspector", "Node configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Start.setText(QtGui.QApplication.translate("FormInspector", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Shutdown.setText(QtGui.QApplication.translate("FormInspector", "Shutdown", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Console), QtGui.QApplication.translate("FormInspector", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormInspector", "IP address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FormInspector", "Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FormInspector", "Gateway", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormInspector", "Hostname", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General), QtGui.QApplication.translate("FormInspector", "Quick configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("FormInspector", "RAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk1Size.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk0Size.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxNvramSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRomSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("FormInspector", "PCMCIA disk1 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("FormInspector", "PCMCIA disk0 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRamSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("FormInspector", "NVRAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("FormInspector", "ROM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QtGui.QApplication.translate("FormInspector", "Memories and disks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("FormInspector", "exec area:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditConfreg.setText(QtGui.QApplication.translate("FormInspector", "0x2102", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("FormInspector", "confreg:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxMapped.setText(QtGui.QApplication.translate("FormInspector", "Use mapped file for the memory", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxIomem.setSuffix(QtGui.QApplication.translate("FormInspector", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("FormInspector", "iomem :", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxExecArea.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), QtGui.QApplication.translate("FormInspector", "Advanced settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormInspector", "General settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FormInspector", "IOS image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("FormInspector", "Console port:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStartupConfig.setText(QtGui.QApplication.translate("FormInspector", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("FormInspector", "Startup-config:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("FormInspector", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonWorkingDirectory.setText(QtGui.QApplication.translate("FormInspector", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("FormInspector", "IOS configuration", None, QtGui.QApplication.UnicodeUTF8))

from Console import Console
