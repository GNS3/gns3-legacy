# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesQemu.ui'
#
# Created: Thu Feb 11 12:23:21 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesQemu(object):
    def setupUi(self, PreferencesQemu):
        PreferencesQemu.setObjectName("PreferencesQemu")
        PreferencesQemu.resize(476, 529)
        self.verticalLayout = QtGui.QVBoxLayout(PreferencesQemu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(PreferencesQemu)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 4)
        self.lineEditQemuwrapperPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditQemuwrapperPath.setObjectName("lineEditQemuwrapperPath")
        self.gridLayout_7.addWidget(self.lineEditQemuwrapperPath, 1, 0, 1, 3)
        self.QemuwrapperPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.QemuwrapperPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.QemuwrapperPath_browser.setObjectName("QemuwrapperPath_browser")
        self.gridLayout_7.addWidget(self.QemuwrapperPath_browser, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEditQemuwrapperWorkdir = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditQemuwrapperWorkdir.setObjectName("lineEditQemuwrapperWorkdir")
        self.gridLayout_7.addWidget(self.lineEditQemuwrapperWorkdir, 3, 0, 1, 3)
        self.QemuwrapperWorkdir_browser = QtGui.QToolButton(self.groupBox_2)
        self.QemuwrapperWorkdir_browser.setObjectName("QemuwrapperWorkdir_browser")
        self.gridLayout_7.addWidget(self.QemuwrapperWorkdir_browser, 3, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_7.addWidget(self.label_16, 4, 0, 1, 2)
        self.lineEditQemuPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditQemuPath.setObjectName("lineEditQemuPath")
        self.gridLayout_7.addWidget(self.lineEditQemuPath, 5, 0, 1, 3)
        self.QemuPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.QemuPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.QemuPath_browser.setObjectName("QemuPath_browser")
        self.gridLayout_7.addWidget(self.QemuPath_browser, 5, 3, 1, 1)
        self.label_17 = QtGui.QLabel(self.groupBox_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_7.addWidget(self.label_17, 6, 0, 1, 2)
        self.lineEditQemuImgPath = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditQemuImgPath.setObjectName("lineEditQemuImgPath")
        self.gridLayout_7.addWidget(self.lineEditQemuImgPath, 7, 0, 1, 3)
        self.QemuImgPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.QemuImgPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.QemuImgPath_browser.setObjectName("QemuImgPath_browser")
        self.gridLayout_7.addWidget(self.QemuImgPath_browser, 7, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 8, 0, 1, 1)
        self.comboBoxBinding = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxBinding.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.comboBoxBinding.setObjectName("comboBoxBinding")
        self.gridLayout_7.addWidget(self.comboBoxBinding, 8, 1, 1, 3)
        self.checkBoxEnableQemuManager = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxEnableQemuManager.setChecked(True)
        self.checkBoxEnableQemuManager.setObjectName("checkBoxEnableQemuManager")
        self.gridLayout_7.addWidget(self.checkBoxEnableQemuManager, 9, 0, 1, 1)
        self.checkBoxQemuManagerImport = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxQemuManagerImport.setChecked(True)
        self.checkBoxQemuManagerImport.setObjectName("checkBoxQemuManagerImport")
        self.gridLayout_7.addWidget(self.checkBoxQemuManagerImport, 10, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setEnabled(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 11, 0, 1, 2)
        self.lineEditHostExternalQemu = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditHostExternalQemu.setObjectName("lineEditHostExternalQemu")
        self.gridLayout_7.addWidget(self.lineEditHostExternalQemu, 11, 2, 1, 2)
        self.label_31 = QtGui.QLabel(self.groupBox_2)
        self.label_31.setObjectName("label_31")
        self.gridLayout_7.addWidget(self.label_31, 12, 0, 1, 1)
        self.baseUDP = QtGui.QSpinBox(self.groupBox_2)
        self.baseUDP.setEnabled(True)
        self.baseUDP.setMinimum(1)
        self.baseUDP.setMaximum(65535)
        self.baseUDP.setObjectName("baseUDP")
        self.gridLayout_7.addWidget(self.baseUDP, 12, 2, 1, 2)
        self.label_30 = QtGui.QLabel(self.groupBox_2)
        self.label_30.setObjectName("label_30")
        self.gridLayout_7.addWidget(self.label_30, 13, 0, 1, 1)
        self.baseConsole = QtGui.QSpinBox(self.groupBox_2)
        self.baseConsole.setEnabled(True)
        self.baseConsole.setMinimum(1)
        self.baseConsole.setMaximum(65535)
        self.baseConsole.setObjectName("baseConsole")
        self.gridLayout_7.addWidget(self.baseConsole, 13, 2, 1, 2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox = QtGui.QGroupBox(self.tab_4)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_14 = QtGui.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 1)
        self.NameQemuImage = QtGui.QLineEdit(self.groupBox)
        self.NameQemuImage.setObjectName("NameQemuImage")
        self.gridLayout.addWidget(self.NameQemuImage, 0, 1, 1, 3)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.QemuImage = QtGui.QLineEdit(self.groupBox)
        self.QemuImage.setObjectName("QemuImage")
        self.gridLayout.addWidget(self.QemuImage, 1, 1, 1, 2)
        self.QemuImage_Browser = QtGui.QToolButton(self.groupBox)
        self.QemuImage_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.QemuImage_Browser.setObjectName("QemuImage_Browser")
        self.gridLayout.addWidget(self.QemuImage_Browser, 1, 3, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 2, 0, 1, 1)
        self.QemuMemory = QtGui.QSpinBox(self.groupBox)
        self.QemuMemory.setMinimum(1)
        self.QemuMemory.setMaximum(100000)
        self.QemuMemory.setSingleStep(16)
        self.QemuMemory.setProperty("value", 128)
        self.QemuMemory.setObjectName("QemuMemory")
        self.gridLayout.addWidget(self.QemuMemory, 2, 1, 1, 3)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.QemuNIC = QtGui.QComboBox(self.groupBox)
        self.QemuNIC.setObjectName("QemuNIC")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.QemuNIC.addItem("")
        self.gridLayout.addWidget(self.QemuNIC, 3, 1, 1, 3)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.QemuOptions = QtGui.QLineEdit(self.groupBox)
        self.QemuOptions.setObjectName("QemuOptions")
        self.gridLayout.addWidget(self.QemuOptions, 4, 1, 1, 3)
        self.QemucheckBoxKqemu = QtGui.QCheckBox(self.groupBox)
        self.QemucheckBoxKqemu.setObjectName("QemucheckBoxKqemu")
        self.gridLayout.addWidget(self.QemucheckBoxKqemu, 5, 0, 1, 1)
        self.QemucheckBoxKVM = QtGui.QCheckBox(self.groupBox)
        self.QemucheckBoxKVM.setObjectName("QemucheckBoxKVM")
        self.gridLayout.addWidget(self.QemucheckBoxKVM, 5, 1, 1, 2)
        self.DeleteQemuImage = QtGui.QPushButton(self.groupBox)
        self.DeleteQemuImage.setObjectName("DeleteQemuImage")
        self.gridLayout.addWidget(self.DeleteQemuImage, 6, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(139, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 2, 1, 2)
        self.treeWidgetQemuImages = QtGui.QTreeWidget(self.groupBox)
        self.treeWidgetQemuImages.setObjectName("treeWidgetQemuImages")
        self.gridLayout.addWidget(self.treeWidgetQemuImages, 7, 0, 1, 4)
        self.SaveQemuImage = QtGui.QPushButton(self.groupBox)
        self.SaveQemuImage.setObjectName("SaveQemuImage")
        self.gridLayout.addWidget(self.SaveQemuImage, 6, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_6 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_23 = QtGui.QLabel(self.groupBox_6)
        self.label_23.setEnabled(True)
        self.label_23.setObjectName("label_23")
        self.gridLayout_6.addWidget(self.label_23, 0, 0, 1, 1)
        self.PIXImage = QtGui.QLineEdit(self.groupBox_6)
        self.PIXImage.setEnabled(True)
        self.PIXImage.setObjectName("PIXImage")
        self.gridLayout_6.addWidget(self.PIXImage, 0, 1, 1, 1)
        self.PIXImage_Browser = QtGui.QToolButton(self.groupBox_6)
        self.PIXImage_Browser.setEnabled(True)
        self.PIXImage_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.PIXImage_Browser.setObjectName("PIXImage_Browser")
        self.gridLayout_6.addWidget(self.PIXImage_Browser, 0, 2, 1, 1)
        self.label_29 = QtGui.QLabel(self.groupBox_6)
        self.label_29.setObjectName("label_29")
        self.gridLayout_6.addWidget(self.label_29, 1, 0, 1, 1)
        self.PIXMemory = QtGui.QSpinBox(self.groupBox_6)
        self.PIXMemory.setEnabled(True)
        self.PIXMemory.setMinimum(1)
        self.PIXMemory.setMaximum(100000)
        self.PIXMemory.setSingleStep(16)
        self.PIXMemory.setProperty("value", 128)
        self.PIXMemory.setObjectName("PIXMemory")
        self.gridLayout_6.addWidget(self.PIXMemory, 1, 1, 1, 2)
        self.label_26 = QtGui.QLabel(self.groupBox_6)
        self.label_26.setObjectName("label_26")
        self.gridLayout_6.addWidget(self.label_26, 2, 0, 1, 1)
        self.PIXNIC = QtGui.QComboBox(self.groupBox_6)
        self.PIXNIC.setEnabled(True)
        self.PIXNIC.setObjectName("PIXNIC")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.PIXNIC.addItem("")
        self.gridLayout_6.addWidget(self.PIXNIC, 2, 1, 1, 2)
        self.label_8 = QtGui.QLabel(self.groupBox_6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 3, 0, 1, 1)
        self.PIXOptions = QtGui.QLineEdit(self.groupBox_6)
        self.PIXOptions.setEnabled(True)
        self.PIXOptions.setObjectName("PIXOptions")
        self.gridLayout_6.addWidget(self.PIXOptions, 3, 1, 1, 2)
        self.PIXcheckBoxKqemu = QtGui.QCheckBox(self.groupBox_6)
        self.PIXcheckBoxKqemu.setEnabled(True)
        self.PIXcheckBoxKqemu.setObjectName("PIXcheckBoxKqemu")
        self.gridLayout_6.addWidget(self.PIXcheckBoxKqemu, 4, 0, 1, 3)
        self.verticalLayout_6.addWidget(self.groupBox_6)
        self.groupBox_7 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_24 = QtGui.QLabel(self.groupBox_7)
        self.label_24.setObjectName("label_24")
        self.gridLayout_5.addWidget(self.label_24, 0, 0, 1, 1)
        self.PIXKey = QtGui.QLineEdit(self.groupBox_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PIXKey.sizePolicy().hasHeightForWidth())
        self.PIXKey.setSizePolicy(sizePolicy)
        self.PIXKey.setObjectName("PIXKey")
        self.gridLayout_5.addWidget(self.PIXKey, 0, 1, 1, 1)
        self.label_25 = QtGui.QLabel(self.groupBox_7)
        self.label_25.setObjectName("label_25")
        self.gridLayout_5.addWidget(self.label_25, 1, 0, 1, 1)
        self.PIXSerial = QtGui.QLineEdit(self.groupBox_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PIXSerial.sizePolicy().hasHeightForWidth())
        self.PIXSerial.setSizePolicy(sizePolicy)
        self.PIXSerial.setObjectName("PIXSerial")
        self.gridLayout_5.addWidget(self.PIXSerial, 1, 1, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox_7)
        spacerItem1 = QtGui.QSpacerItem(20, 69, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_5 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.groupBox_5)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.JunOSImage = QtGui.QLineEdit(self.groupBox_5)
        self.JunOSImage.setEnabled(True)
        self.JunOSImage.setObjectName("JunOSImage")
        self.gridLayout_2.addWidget(self.JunOSImage, 0, 1, 1, 1)
        self.JunOSImage_Browser = QtGui.QToolButton(self.groupBox_5)
        self.JunOSImage_Browser.setEnabled(True)
        self.JunOSImage_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.JunOSImage_Browser.setObjectName("JunOSImage_Browser")
        self.gridLayout_2.addWidget(self.JunOSImage_Browser, 0, 2, 1, 1)
        self.label_21 = QtGui.QLabel(self.groupBox_5)
        self.label_21.setObjectName("label_21")
        self.gridLayout_2.addWidget(self.label_21, 1, 0, 1, 1)
        self.JunOSMemory = QtGui.QSpinBox(self.groupBox_5)
        self.JunOSMemory.setEnabled(True)
        self.JunOSMemory.setMinimum(1)
        self.JunOSMemory.setMaximum(100000)
        self.JunOSMemory.setSingleStep(16)
        self.JunOSMemory.setProperty("value", 96)
        self.JunOSMemory.setObjectName("JunOSMemory")
        self.gridLayout_2.addWidget(self.JunOSMemory, 1, 1, 1, 2)
        self.label_11 = QtGui.QLabel(self.groupBox_5)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)
        self.JunOSNIC = QtGui.QComboBox(self.groupBox_5)
        self.JunOSNIC.setEnabled(True)
        self.JunOSNIC.setObjectName("JunOSNIC")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.JunOSNIC.addItem("")
        self.gridLayout_2.addWidget(self.JunOSNIC, 2, 1, 1, 2)
        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 3, 0, 1, 1)
        self.JunOSOptions = QtGui.QLineEdit(self.groupBox_5)
        self.JunOSOptions.setEnabled(True)
        self.JunOSOptions.setObjectName("JunOSOptions")
        self.gridLayout_2.addWidget(self.JunOSOptions, 3, 1, 1, 2)
        self.JunOScheckBoxKqemu = QtGui.QCheckBox(self.groupBox_5)
        self.JunOScheckBoxKqemu.setEnabled(True)
        self.JunOScheckBoxKqemu.setObjectName("JunOScheckBoxKqemu")
        self.gridLayout_2.addWidget(self.JunOScheckBoxKqemu, 4, 0, 1, 1)
        self.JunOScheckBoxKVM = QtGui.QCheckBox(self.groupBox_5)
        self.JunOScheckBoxKVM.setEnabled(True)
        self.JunOScheckBoxKVM.setObjectName("JunOScheckBoxKVM")
        self.gridLayout_2.addWidget(self.JunOScheckBoxKVM, 5, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        spacerItem2 = QtGui.QSpacerItem(20, 130, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_22 = QtGui.QLabel(self.groupBox_3)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 0, 0, 1, 1)
        self.ASAMemory = QtGui.QSpinBox(self.groupBox_3)
        self.ASAMemory.setEnabled(True)
        self.ASAMemory.setMinimum(1)
        self.ASAMemory.setMaximum(100000)
        self.ASAMemory.setSingleStep(16)
        self.ASAMemory.setProperty("value", 256)
        self.ASAMemory.setObjectName("ASAMemory")
        self.gridLayout_3.addWidget(self.ASAMemory, 0, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 1, 0, 1, 1)
        self.ASANIC = QtGui.QComboBox(self.groupBox_3)
        self.ASANIC.setEnabled(True)
        self.ASANIC.setObjectName("ASANIC")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.ASANIC.addItem("")
        self.gridLayout_3.addWidget(self.ASANIC, 1, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 2, 0, 1, 1)
        self.ASAOptions = QtGui.QLineEdit(self.groupBox_3)
        self.ASAOptions.setEnabled(True)
        self.ASAOptions.setObjectName("ASAOptions")
        self.gridLayout_3.addWidget(self.ASAOptions, 2, 1, 1, 1)
        self.ASAcheckBoxKqemu = QtGui.QCheckBox(self.groupBox_3)
        self.ASAcheckBoxKqemu.setEnabled(True)
        self.ASAcheckBoxKqemu.setObjectName("ASAcheckBoxKqemu")
        self.gridLayout_3.addWidget(self.ASAcheckBoxKqemu, 3, 0, 1, 1)
        self.ASAcheckBoxKVM = QtGui.QCheckBox(self.groupBox_3)
        self.ASAcheckBoxKVM.setEnabled(True)
        self.ASAcheckBoxKVM.setObjectName("ASAcheckBoxKVM")
        self.gridLayout_3.addWidget(self.ASAcheckBoxKVM, 4, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.ASAInitrd_Browser = QtGui.QToolButton(self.groupBox_4)
        self.ASAInitrd_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ASAInitrd_Browser.setObjectName("ASAInitrd_Browser")
        self.gridLayout_4.addWidget(self.ASAInitrd_Browser, 0, 2, 1, 1)
        self.label_18 = QtGui.QLabel(self.groupBox_4)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 1, 0, 1, 1)
        self.ASAKernel = QtGui.QLineEdit(self.groupBox_4)
        self.ASAKernel.setObjectName("ASAKernel")
        self.gridLayout_4.addWidget(self.ASAKernel, 1, 1, 1, 1)
        self.ASAKernel_Browser = QtGui.QToolButton(self.groupBox_4)
        self.ASAKernel_Browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ASAKernel_Browser.setObjectName("ASAKernel_Browser")
        self.gridLayout_4.addWidget(self.ASAKernel_Browser, 1, 2, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.ASAKernelCmdLine = QtGui.QLineEdit(self.groupBox_4)
        self.ASAKernelCmdLine.setObjectName("ASAKernelCmdLine")
        self.gridLayout_4.addWidget(self.ASAKernelCmdLine, 2, 1, 1, 2)
        self.ASAInitrd = QtGui.QLineEdit(self.groupBox_4)
        self.ASAInitrd.setObjectName("ASAInitrd")
        self.gridLayout_4.addWidget(self.ASAInitrd, 0, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_4)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        spacerItem3 = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(PreferencesQemu)
        self.tabWidget.setCurrentIndex(0)
        self.QemuNIC.setCurrentIndex(5)
        self.PIXNIC.setCurrentIndex(5)
        self.JunOSNIC.setCurrentIndex(5)
        self.ASANIC.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(PreferencesQemu)

    def retranslateUi(self, PreferencesQemu):
        PreferencesQemu.setWindowTitle(QtGui.QApplication.translate("PreferencesQemu", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesQemu", "Qemuwrapper", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesQemu", "Path (qemuwrapper.exe on Windows else qemuwrapper.py):", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuwrapperPath_browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesQemu", "Working directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuwrapperWorkdir_browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("PreferencesQemu", "Path to qemu (not used for PIX):", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuPath_browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("PreferencesQemu", "Path to qemu-img (not used for PIX):", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuImgPath_browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PreferencesQemu", "Bind Qemu Manager with:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxEnableQemuManager.setText(QtGui.QApplication.translate("PreferencesQemu", "Enable Qemu Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxQemuManagerImport.setText(QtGui.QApplication.translate("PreferencesQemu", "Use Qemu Manager when importing", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PreferencesQemu", "Host for an external qemuwrapper:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_31.setText(QtGui.QApplication.translate("PreferencesQemu", "Base UDP port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_30.setText(QtGui.QApplication.translate("PreferencesQemu", "Base console port:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PreferencesQemu", "General Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesQemu", "Qemu Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("PreferencesQemu", "Identifier name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesQemu", "Binary image:", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuImage_Browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("PreferencesQemu", "Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("PreferencesQemu", "NIC:", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(0, QtGui.QApplication.translate("PreferencesQemu", "ne2k_pci", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(1, QtGui.QApplication.translate("PreferencesQemu", "i82551", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(2, QtGui.QApplication.translate("PreferencesQemu", "i82557b", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(3, QtGui.QApplication.translate("PreferencesQemu", "i82559er", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(4, QtGui.QApplication.translate("PreferencesQemu", "rtl8139", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(5, QtGui.QApplication.translate("PreferencesQemu", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(6, QtGui.QApplication.translate("PreferencesQemu", "pcnet", None, QtGui.QApplication.UnicodeUTF8))
        self.QemuNIC.setItemText(7, QtGui.QApplication.translate("PreferencesQemu", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesQemu", "Qemu Options:", None, QtGui.QApplication.UnicodeUTF8))
        self.QemucheckBoxKqemu.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KQemu", None, QtGui.QApplication.UnicodeUTF8))
        self.QemucheckBoxKVM.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KVM (Linux Only)", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteQemuImage.setText(QtGui.QApplication.translate("PreferencesQemu", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetQemuImages.headerItem().setText(0, QtGui.QApplication.translate("PreferencesQemu", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetQemuImages.headerItem().setText(1, QtGui.QApplication.translate("PreferencesQemu", "Image path", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveQemuImage.setText(QtGui.QApplication.translate("PreferencesQemu", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("PreferencesQemu", "Qemu", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("PreferencesQemu", "PIX Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("PreferencesQemu", "Binary image:", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXImage_Browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("PreferencesQemu", "Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("PreferencesQemu", "NIC:", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(0, QtGui.QApplication.translate("PreferencesQemu", "ne2k_pci", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(1, QtGui.QApplication.translate("PreferencesQemu", "i82551", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(2, QtGui.QApplication.translate("PreferencesQemu", "i82557b", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(3, QtGui.QApplication.translate("PreferencesQemu", "i82559er", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(4, QtGui.QApplication.translate("PreferencesQemu", "rtl8139", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(5, QtGui.QApplication.translate("PreferencesQemu", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(6, QtGui.QApplication.translate("PreferencesQemu", "pcnet", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXNIC.setItemText(7, QtGui.QApplication.translate("PreferencesQemu", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PreferencesQemu", "Qemu Options:", None, QtGui.QApplication.UnicodeUTF8))
        self.PIXcheckBoxKqemu.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KQemu", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_7.setTitle(QtGui.QApplication.translate("PreferencesQemu", "PIX Specific Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("PreferencesQemu", "Key:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("PreferencesQemu", "Serial:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("PreferencesQemu", "PIX", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("PreferencesQemu", "JunOS Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PreferencesQemu", "Binary image:", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSImage_Browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("PreferencesQemu", "Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("PreferencesQemu", "NIC:", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(0, QtGui.QApplication.translate("PreferencesQemu", "ne2k_pci", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(1, QtGui.QApplication.translate("PreferencesQemu", "i82551", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(2, QtGui.QApplication.translate("PreferencesQemu", "i82557b", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(3, QtGui.QApplication.translate("PreferencesQemu", "i82559er", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(4, QtGui.QApplication.translate("PreferencesQemu", "rtl8139", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(5, QtGui.QApplication.translate("PreferencesQemu", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(6, QtGui.QApplication.translate("PreferencesQemu", "pcnet", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOSNIC.setItemText(7, QtGui.QApplication.translate("PreferencesQemu", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("PreferencesQemu", "Qemu Options:", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOScheckBoxKqemu.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KQemu", None, QtGui.QApplication.UnicodeUTF8))
        self.JunOScheckBoxKVM.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KVM (Linux Only)", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("PreferencesQemu", "JunOS", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PreferencesQemu", "ASA Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("PreferencesQemu", "Memory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("PreferencesQemu", "NIC:", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(0, QtGui.QApplication.translate("PreferencesQemu", "ne2k_pci", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(1, QtGui.QApplication.translate("PreferencesQemu", "i82551", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(2, QtGui.QApplication.translate("PreferencesQemu", "i82557b", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(3, QtGui.QApplication.translate("PreferencesQemu", "i82559er", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(4, QtGui.QApplication.translate("PreferencesQemu", "rtl8139", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(5, QtGui.QApplication.translate("PreferencesQemu", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(6, QtGui.QApplication.translate("PreferencesQemu", "pcnet", None, QtGui.QApplication.UnicodeUTF8))
        self.ASANIC.setItemText(7, QtGui.QApplication.translate("PreferencesQemu", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("PreferencesQemu", "Qemu Options:", None, QtGui.QApplication.UnicodeUTF8))
        self.ASAcheckBoxKqemu.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KQemu", None, QtGui.QApplication.UnicodeUTF8))
        self.ASAcheckBoxKVM.setText(QtGui.QApplication.translate("PreferencesQemu", "Use KVM (Linux Only)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("PreferencesQemu", "ASA Specific Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.ASAInitrd_Browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("PreferencesQemu", "Kernel:", None, QtGui.QApplication.UnicodeUTF8))
        self.ASAKernel_Browser.setText(QtGui.QApplication.translate("PreferencesQemu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("PreferencesQemu", "Kernel cmd line:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("PreferencesQemu", "Initrd:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PreferencesQemu", "ASA", None, QtGui.QApplication.UnicodeUTF8))

