# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Inspector.ui'
#
# Created: Tue May 29 17:15:07 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FormInspector(object):
    def setupUi(self, FormInspector):
        FormInspector.setObjectName("FormInspector")
        FormInspector.resize(QtCore.QSize(QtCore.QRect(0,0,528,316).size()).expandedTo(FormInspector.minimumSizeHint()))

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
        self.gridlayout.addWidget(self.label_5,0,0,1,2)

        self.comboBoxMidplane = QtGui.QComboBox(self.groupBox)
        self.comboBoxMidplane.setEnabled(False)
        self.comboBoxMidplane.setObjectName("comboBoxMidplane")
        self.gridlayout.addWidget(self.comboBoxMidplane,3,4,1,2)

        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridlayout.addWidget(self.label_13,2,0,1,3)

        self.label_18 = QtGui.QLabel(self.groupBox)
        self.label_18.setObjectName("label_18")
        self.gridlayout.addWidget(self.label_18,1,0,1,4)

        self.comboBoxNPE = QtGui.QComboBox(self.groupBox)
        self.comboBoxNPE.setEnabled(False)
        self.comboBoxNPE.setObjectName("comboBoxNPE")
        self.gridlayout.addWidget(self.comboBoxNPE,4,4,1,2)

        self.pushButtonStartupConfig = QtGui.QPushButton(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStartupConfig.sizePolicy().hasHeightForWidth())
        self.pushButtonStartupConfig.setSizePolicy(sizePolicy)
        self.pushButtonStartupConfig.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonStartupConfig.setObjectName("pushButtonStartupConfig")
        self.gridlayout.addWidget(self.pushButtonStartupConfig,1,5,1,1)

        self.comboBoxIOS = QtGui.QComboBox(self.groupBox)
        self.comboBoxIOS.setObjectName("comboBoxIOS")
        self.gridlayout.addWidget(self.comboBoxIOS,0,4,1,2)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,3,0,1,1)

        spacerItem = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,4,1,1,3)

        self.lineEditStartupConfig = QtGui.QLineEdit(self.groupBox)
        self.lineEditStartupConfig.setObjectName("lineEditStartupConfig")
        self.gridlayout.addWidget(self.lineEditStartupConfig,1,4,1,1)

        spacerItem1 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,2,3,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,4,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,0,2,1,2)

        spacerItem3 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3,3,1,1,3)

        self.lineEditConsolePort = QtGui.QLineEdit(self.groupBox)
        self.lineEditConsolePort.setObjectName("lineEditConsolePort")
        self.gridlayout.addWidget(self.lineEditConsolePort,2,4,1,2)
        self.vboxlayout1.addLayout(self.gridlayout)
        self.hboxlayout.addWidget(self.groupBox)

        self.groupBox_5 = QtGui.QGroupBox(self.tab)
        self.groupBox_5.setObjectName("groupBox_5")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_5)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.checkBoxMapped = QtGui.QCheckBox(self.groupBox_5)
        self.checkBoxMapped.setChecked(True)
        self.checkBoxMapped.setObjectName("checkBoxMapped")
        self.vboxlayout2.addWidget(self.checkBoxMapped)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.spinBoxIomem = QtGui.QSpinBox(self.groupBox_5)
        self.spinBoxIomem.setEnabled(False)
        self.spinBoxIomem.setMaximum(100)
        self.spinBoxIomem.setProperty("value",QtCore.QVariant(5))
        self.spinBoxIomem.setObjectName("spinBoxIomem")
        self.gridlayout1.addWidget(self.spinBoxIomem,2,3,1,1)

        spacerItem4 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem4,0,1,1,2)

        self.spinBoxExecArea = QtGui.QSpinBox(self.groupBox_5)
        self.spinBoxExecArea.setMaximum(4096)
        self.spinBoxExecArea.setSingleStep(4)
        self.spinBoxExecArea.setProperty("value",QtCore.QVariant(64))
        self.spinBoxExecArea.setObjectName("spinBoxExecArea")
        self.gridlayout1.addWidget(self.spinBoxExecArea,1,3,1,1)

        self.label_22 = QtGui.QLabel(self.groupBox_5)
        self.label_22.setObjectName("label_22")
        self.gridlayout1.addWidget(self.label_22,2,0,1,1)

        spacerItem5 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem5,1,2,1,1)

        self.label_25 = QtGui.QLabel(self.groupBox_5)
        self.label_25.setObjectName("label_25")
        self.gridlayout1.addWidget(self.label_25,0,0,1,1)

        spacerItem6 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem6,2,1,1,2)

        self.label_31 = QtGui.QLabel(self.groupBox_5)
        self.label_31.setObjectName("label_31")
        self.gridlayout1.addWidget(self.label_31,1,0,1,2)

        self.lineEditConfreg = QtGui.QLineEdit(self.groupBox_5)
        self.lineEditConfreg.setObjectName("lineEditConfreg")
        self.gridlayout1.addWidget(self.lineEditConfreg,0,3,1,1)
        self.vboxlayout2.addLayout(self.gridlayout1)
        self.hboxlayout.addWidget(self.groupBox_5)
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.groupBox_2 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem7,0,1,1,1)

        spacerItem8 = QtGui.QSpacerItem(20,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem8,1,0,1,1)

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        spacerItem9 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem9,2,1,1,1)

        spacerItem10 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem10,1,1,1,1)

        spacerItem11 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem11,0,1,1,1)

        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridlayout3.addWidget(self.label_8,1,0,1,1)

        self.spinBoxNvramSize = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxNvramSize.setMaximum(4096)
        self.spinBoxNvramSize.setSingleStep(4)
        self.spinBoxNvramSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxNvramSize.setObjectName("spinBoxNvramSize")
        self.gridlayout3.addWidget(self.spinBoxNvramSize,2,2,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridlayout3.addWidget(self.label_7,0,0,1,1)

        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridlayout3.addWidget(self.label_9,2,0,1,1)

        self.spinBoxRomSize = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxRomSize.setMaximum(4096)
        self.spinBoxRomSize.setSingleStep(4)
        self.spinBoxRomSize.setProperty("value",QtCore.QVariant(4))
        self.spinBoxRomSize.setObjectName("spinBoxRomSize")
        self.gridlayout3.addWidget(self.spinBoxRomSize,1,2,1,1)

        self.spinBoxRamSize = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxRamSize.setMaximum(4096)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxRamSize.setObjectName("spinBoxRamSize")
        self.gridlayout3.addWidget(self.spinBoxRamSize,0,2,1,1)
        self.gridlayout2.addLayout(self.gridlayout3,0,0,1,1)
        self.hboxlayout1.addWidget(self.groupBox_2)

        self.groupBox_6 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_6.setObjectName("groupBox_6")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox_6)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_10 = QtGui.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.gridlayout4.addWidget(self.label_10,0,0,1,1)

        self.spinBoxPcmciaDisk0Size = QtGui.QSpinBox(self.groupBox_6)
        self.spinBoxPcmciaDisk0Size.setSingleStep(4)
        self.spinBoxPcmciaDisk0Size.setObjectName("spinBoxPcmciaDisk0Size")
        self.gridlayout4.addWidget(self.spinBoxPcmciaDisk0Size,0,1,1,1)

        self.spinBoxPcmciaDisk1Size = QtGui.QSpinBox(self.groupBox_6)
        self.spinBoxPcmciaDisk1Size.setSingleStep(4)
        self.spinBoxPcmciaDisk1Size.setObjectName("spinBoxPcmciaDisk1Size")
        self.gridlayout4.addWidget(self.spinBoxPcmciaDisk1Size,1,1,1,1)

        self.label_11 = QtGui.QLabel(self.groupBox_6)
        self.label_11.setObjectName("label_11")
        self.gridlayout4.addWidget(self.label_11,1,0,1,1)
        self.vboxlayout3.addLayout(self.gridlayout4)

        spacerItem12 = QtGui.QSpacerItem(20,81,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout3.addItem(spacerItem12)
        self.hboxlayout1.addWidget(self.groupBox_6)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.tab_2)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

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

        spacerItem13 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem13,3,1,1,1)

        self.label_6 = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.gridlayout5.addWidget(self.label_6,0,0,1,1)

        spacerItem14 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem14,0,1,1,1)

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

        spacerItem15 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem15,1,1,1,1)

        self.comboBoxSlot3 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot3.setObjectName("comboBoxSlot3")
        self.gridlayout5.addWidget(self.comboBoxSlot3,3,2,1,1)

        spacerItem16 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem16,2,1,1,1)

        self.comboBoxSlot1 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot1.setObjectName("comboBoxSlot1")
        self.gridlayout5.addWidget(self.comboBoxSlot1,1,2,1,1)
        self.hboxlayout2.addLayout(self.gridlayout5)

        spacerItem17 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem17)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setMargin(0)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.comboBoxSlot7 = QtGui.QComboBox(self.tab_2)
        self.comboBoxSlot7.setObjectName("comboBoxSlot7")
        self.gridlayout6.addWidget(self.comboBoxSlot7,3,2,1,1)

        spacerItem18 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem18,2,1,1,1)

        spacerItem19 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem19,0,1,1,1)

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

        spacerItem20 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem20,1,1,1,1)

        spacerItem21 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem21,3,1,1,1)
        self.hboxlayout2.addLayout(self.gridlayout6)
        self.tabWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem22 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem22)

        self.buttonBoxIOSConfig = QtGui.QDialogButtonBox(FormInspector)
        self.buttonBoxIOSConfig.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.buttonBoxIOSConfig.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxIOSConfig.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBoxIOSConfig.setObjectName("buttonBoxIOSConfig")
        self.hboxlayout3.addWidget(self.buttonBoxIOSConfig)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.retranslateUi(FormInspector)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormInspector)

    def retranslateUi(self, FormInspector):
        FormInspector.setWindowTitle(QtGui.QApplication.translate("FormInspector", "Node configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FormInspector", "General settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FormInspector", "IOS image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("FormInspector", "Console port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("FormInspector", "Startup-config:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStartupConfig.setText(QtGui.QApplication.translate("FormInspector", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FormInspector", "Midplane:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FormInspector", "NPE:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("FormInspector", "Advanced settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxMapped.setText(QtGui.QApplication.translate("FormInspector", "Use mmap", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxIomem.setSuffix(QtGui.QApplication.translate("FormInspector", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxExecArea.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("FormInspector", "iomem :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("FormInspector", "confreg:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_31.setText(QtGui.QApplication.translate("FormInspector", "exec area:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditConfreg.setText(QtGui.QApplication.translate("FormInspector", "0x2102", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("FormInspector", "General and advanced settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FormInspector", "Memories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("FormInspector", "ROM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxNvramSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("FormInspector", "RAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("FormInspector", "NVRAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRomSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRamSize.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("FormInspector", "Disks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("FormInspector", "PCMCIA disk0 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk0Size.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk1Size.setSuffix(QtGui.QApplication.translate("FormInspector", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("FormInspector", "PCMCIA disk1 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("FormInspector", "Memories and disks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("FormInspector", "slot2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("FormInspector", "slot3:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("FormInspector", "slot0:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("FormInspector", "slot1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("FormInspector", "slot4:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("FormInspector", "slot5:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("FormInspector", "slot7:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_28.setText(QtGui.QApplication.translate("FormInspector", "slot6:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("FormInspector", "Slots", None, QtGui.QApplication.UnicodeUTF8))

