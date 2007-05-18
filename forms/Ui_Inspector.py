# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Inspector.ui'
#
# Created: Fri May 18 18:36:07 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_FormInspector(object):
    def setupUi(self, FormInspector):
        FormInspector.setObjectName("FormInspector")
        FormInspector.resize(QtCore.QSize(QtCore.QRect(0,0,625,386).size()).expandedTo(FormInspector.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(FormInspector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tabWidget = QtGui.QTabWidget(FormInspector)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,0,0,1,1)

        self.comboBoxIOS = QtGui.QComboBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxIOS.sizePolicy().hasHeightForWidth())
        self.comboBoxIOS.setSizePolicy(sizePolicy)
        self.comboBoxIOS.setObjectName("comboBoxIOS")
        self.gridlayout.addWidget(self.comboBoxIOS,0,1,1,1)

        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridlayout.addWidget(self.label_13,1,0,1,1)

        spacerItem = QtGui.QSpacerItem(32,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,2,2,1)

        self.lineEditConsolePort = QtGui.QLineEdit(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditConsolePort.sizePolicy().hasHeightForWidth())
        self.lineEditConsolePort.setSizePolicy(sizePolicy)
        self.lineEditConsolePort.setObjectName("lineEditConsolePort")
        self.gridlayout.addWidget(self.lineEditConsolePort,1,1,1,1)
        self.vboxlayout1.addLayout(self.gridlayout)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout1.addItem(spacerItem1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.pushButtonStartupConfig = QtGui.QPushButton(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStartupConfig.sizePolicy().hasHeightForWidth())
        self.pushButtonStartupConfig.setSizePolicy(sizePolicy)
        self.pushButtonStartupConfig.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonStartupConfig.setObjectName("pushButtonStartupConfig")
        self.gridlayout1.addWidget(self.pushButtonStartupConfig,0,2,1,1)

        self.label_18 = QtGui.QLabel(self.groupBox)
        self.label_18.setObjectName("label_18")
        self.gridlayout1.addWidget(self.label_18,0,0,1,1)

        self.lineEditStartupConfig = QtGui.QLineEdit(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditStartupConfig.sizePolicy().hasHeightForWidth())
        self.lineEditStartupConfig.setSizePolicy(sizePolicy)
        self.lineEditStartupConfig.setObjectName("lineEditStartupConfig")
        self.gridlayout1.addWidget(self.lineEditStartupConfig,0,1,1,1)
        self.vboxlayout1.addLayout(self.gridlayout1)

        spacerItem2 = QtGui.QSpacerItem(20,31,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout1.addItem(spacerItem2)
        self.hboxlayout.addWidget(self.groupBox)

        self.toolBox = QtGui.QToolBox(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setObjectName("toolBox")

        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0,0,309,221))
        self.page_3.setObjectName("page_3")

        self.gridlayout2 = QtGui.QGridLayout(self.page_3)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem3 = QtGui.QSpacerItem(51,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem3,0,3,5,1)

        self.label_7 = QtGui.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout2.addWidget(self.label_7,0,0,1,1)

        self.spinBoxPcmciaDisk1Size = QtGui.QSpinBox(self.page_3)
        self.spinBoxPcmciaDisk1Size.setSingleStep(4)
        self.spinBoxPcmciaDisk1Size.setObjectName("spinBoxPcmciaDisk1Size")
        self.gridlayout2.addWidget(self.spinBoxPcmciaDisk1Size,4,2,1,1)

        spacerItem4 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem4,1,1,1,1)

        self.spinBoxPcmciaDisk0Size = QtGui.QSpinBox(self.page_3)
        self.spinBoxPcmciaDisk0Size.setSingleStep(4)
        self.spinBoxPcmciaDisk0Size.setObjectName("spinBoxPcmciaDisk0Size")
        self.gridlayout2.addWidget(self.spinBoxPcmciaDisk0Size,3,2,1,1)

        self.spinBoxNvramSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxNvramSize.setMaximum(4096)
        self.spinBoxNvramSize.setSingleStep(4)
        self.spinBoxNvramSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxNvramSize.setObjectName("spinBoxNvramSize")
        self.gridlayout2.addWidget(self.spinBoxNvramSize,2,2,1,1)

        spacerItem5 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem5,2,1,1,1)

        self.spinBoxRomSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxRomSize.setMaximum(4096)
        self.spinBoxRomSize.setSingleStep(4)
        self.spinBoxRomSize.setProperty("value",QtCore.QVariant(4))
        self.spinBoxRomSize.setObjectName("spinBoxRomSize")
        self.gridlayout2.addWidget(self.spinBoxRomSize,1,2,1,1)

        self.label_11 = QtGui.QLabel(self.page_3)
        self.label_11.setObjectName("label_11")
        self.gridlayout2.addWidget(self.label_11,4,0,1,2)

        self.label_10 = QtGui.QLabel(self.page_3)
        self.label_10.setObjectName("label_10")
        self.gridlayout2.addWidget(self.label_10,3,0,1,2)

        self.spinBoxRamSize = QtGui.QSpinBox(self.page_3)
        self.spinBoxRamSize.setMaximum(4096)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxRamSize.setObjectName("spinBoxRamSize")
        self.gridlayout2.addWidget(self.spinBoxRamSize,0,2,1,1)

        self.label_9 = QtGui.QLabel(self.page_3)
        self.label_9.setObjectName("label_9")
        self.gridlayout2.addWidget(self.label_9,2,0,1,1)

        self.label_8 = QtGui.QLabel(self.page_3)
        self.label_8.setObjectName("label_8")
        self.gridlayout2.addWidget(self.label_8,1,0,1,1)

        spacerItem6 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem6,0,1,1,1)
        self.toolBox.addItem(self.page_3,"")

        self.page_5 = QtGui.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0,0,247,146))
        self.page_5.setObjectName("page_5")

        self.gridlayout3 = QtGui.QGridLayout(self.page_5)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_17 = QtGui.QLabel(self.page_5)
        self.label_17.setObjectName("label_17")
        self.gridlayout3.addWidget(self.label_17,2,0,1,2)

        spacerItem7 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem7,1,4,1,1)

        self.lineEditConfreg = QtGui.QLineEdit(self.page_5)
        self.lineEditConfreg.setObjectName("lineEditConfreg")
        self.gridlayout3.addWidget(self.lineEditConfreg,1,3,1,1)

        spacerItem8 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem8,1,1,1,2)

        self.label_16 = QtGui.QLabel(self.page_5)
        self.label_16.setObjectName("label_16")
        self.gridlayout3.addWidget(self.label_16,1,0,1,1)

        spacerItem9 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem9,0,4,1,1)

        self.checkBoxMapped = QtGui.QCheckBox(self.page_5)
        self.checkBoxMapped.setChecked(True)
        self.checkBoxMapped.setObjectName("checkBoxMapped")
        self.gridlayout3.addWidget(self.checkBoxMapped,0,0,1,4)

        spacerItem10 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem10,3,4,1,1)

        spacerItem11 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem11,2,4,1,1)

        self.spinBoxIomem = QtGui.QSpinBox(self.page_5)
        self.spinBoxIomem.setMaximum(100)
        self.spinBoxIomem.setProperty("value",QtCore.QVariant(5))
        self.spinBoxIomem.setObjectName("spinBoxIomem")
        self.gridlayout3.addWidget(self.spinBoxIomem,3,3,1,1)

        spacerItem12 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem12,3,1,1,2)

        self.label_14 = QtGui.QLabel(self.page_5)
        self.label_14.setObjectName("label_14")
        self.gridlayout3.addWidget(self.label_14,3,0,1,1)

        self.spinBoxExecArea = QtGui.QSpinBox(self.page_5)
        self.spinBoxExecArea.setMaximum(4096)
        self.spinBoxExecArea.setSingleStep(4)
        self.spinBoxExecArea.setProperty("value",QtCore.QVariant(64))
        self.spinBoxExecArea.setObjectName("spinBoxExecArea")
        self.gridlayout3.addWidget(self.spinBoxExecArea,2,3,1,1)

        spacerItem13 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem13,2,2,1,1)
        self.toolBox.addItem(self.page_5,"")
        self.hboxlayout.addWidget(self.toolBox)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        spacerItem14 = QtGui.QSpacerItem(301,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem14,1,1,1,1)

        spacerItem15 = QtGui.QSpacerItem(301,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem15,0,1,1,1)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setMargin(0)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.label_15 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName("label_15")
        self.gridlayout5.addWidget(self.label_15,2,0,1,1)

        self.label_19 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.gridlayout5.addWidget(self.label_19,3,0,1,1)

        self.comboBoxSlot0 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot0.setObjectName("comboBoxSlot0")
        self.gridlayout5.addWidget(self.comboBoxSlot0,0,2,1,1)

        spacerItem16 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem16,3,1,1,1)

        self.label_6 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridlayout5.addWidget(self.label_6,0,0,1,1)

        spacerItem17 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem17,0,1,1,1)

        self.comboBoxSlot2 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot2.setObjectName("comboBoxSlot2")
        self.gridlayout5.addWidget(self.comboBoxSlot2,2,2,1,1)

        self.label_12 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridlayout5.addWidget(self.label_12,1,0,1,1)

        spacerItem18 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem18,1,1,1,1)

        self.comboBoxSlot3 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot3.setObjectName("comboBoxSlot3")
        self.gridlayout5.addWidget(self.comboBoxSlot3,3,2,1,1)

        spacerItem19 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem19,2,1,1,1)

        self.comboBoxSlot1 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot1.setObjectName("comboBoxSlot1")
        self.gridlayout5.addWidget(self.comboBoxSlot1,1,2,1,1)
        self.gridlayout4.addLayout(self.gridlayout5,0,0,1,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setMargin(0)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.comboBoxSlot7 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot7.setObjectName("comboBoxSlot7")
        self.gridlayout6.addWidget(self.comboBoxSlot7,3,2,1,1)

        spacerItem20 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem20,2,1,1,1)

        spacerItem21 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem21,0,1,1,1)

        self.comboBoxSlot4 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot4.setObjectName("comboBoxSlot4")
        self.gridlayout6.addWidget(self.comboBoxSlot4,0,2,1,1)

        self.label_23 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridlayout6.addWidget(self.label_23,0,0,1,1)

        self.label_26 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName("label_26")
        self.gridlayout6.addWidget(self.label_26,1,0,1,1)

        self.label_29 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setObjectName("label_29")
        self.gridlayout6.addWidget(self.label_29,3,0,1,1)

        self.label_28 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setObjectName("label_28")
        self.gridlayout6.addWidget(self.label_28,2,0,1,1)

        self.comboBoxSlot6 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot6.setObjectName("comboBoxSlot6")
        self.gridlayout6.addWidget(self.comboBoxSlot6,2,2,1,1)

        self.comboBoxSlot5 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot5.setObjectName("comboBoxSlot5")
        self.gridlayout6.addWidget(self.comboBoxSlot5,1,2,1,1)

        spacerItem22 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem22,1,1,1,1)

        spacerItem23 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem23,3,1,1,1)
        self.gridlayout4.addLayout(self.gridlayout6,1,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem24 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem24)

        self.buttonBoxIOSConfig = QtGui.QDialogButtonBox(FormInspector)
        self.buttonBoxIOSConfig.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.buttonBoxIOSConfig.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxIOSConfig.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton)
        self.buttonBoxIOSConfig.setObjectName("buttonBoxIOSConfig")
        self.hboxlayout1.addWidget(self.buttonBoxIOSConfig)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(FormInspector)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormInspector)

    def retranslateUi(self, FormInspector):
        FormInspector.setWindowTitle(QtGui.QApplication.translate("FormInspector", "Node configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormInspector", "General settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FormInspector", "IOS image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("FormInspector", "Console port:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStartupConfig.setText(QtGui.QApplication.translate("FormInspector", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("FormInspector", "Startup-config:", None, QtGui.QApplication.UnicodeUTF8))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("FormInspector", "IOS configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("FormInspector", "slot2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("FormInspector", "slot3:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("FormInspector", "slot0:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("FormInspector", "slot1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("FormInspector", "slot4:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("FormInspector", "slot5:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("FormInspector", "slot7:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_28.setText(QtGui.QApplication.translate("FormInspector", "slot6:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("FormInspector", "Port adapters / Network modules", None, QtGui.QApplication.UnicodeUTF8))

