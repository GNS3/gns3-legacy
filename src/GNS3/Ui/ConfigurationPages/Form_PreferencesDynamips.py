# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesDynamips.ui'
#
# Created: Sun Apr 28 17:24:47 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PreferencesDynamips(object):
    def setupUi(self, PreferencesDynamips):
        PreferencesDynamips.setObjectName(_fromUtf8("PreferencesDynamips"))
        PreferencesDynamips.resize(524, 449)
        PreferencesDynamips.setWindowTitle(QtGui.QApplication.translate("PreferencesDynamips", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.vboxlayout = QtGui.QVBoxLayout(PreferencesDynamips)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tabWidget = QtGui.QTabWidget(PreferencesDynamips)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesDynamips", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("PreferencesDynamips", "Executable path to Dynamips:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.dynamips_path = QtGui.QLineEdit(self.groupBox)
        self.dynamips_path.setObjectName(_fromUtf8("dynamips_path"))
        self.horizontalLayout_2.addWidget(self.dynamips_path)
        self.dynamips_path_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_path_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_path_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.dynamips_path_browser.setObjectName(_fromUtf8("dynamips_path_browser"))
        self.horizontalLayout_2.addWidget(self.dynamips_path_browser)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 4)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setText(QtGui.QApplication.translate("PreferencesDynamips", "Working directory for Dynamips:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dynamips_workdir = QtGui.QLineEdit(self.groupBox)
        self.dynamips_workdir.setObjectName(_fromUtf8("dynamips_workdir"))
        self.horizontalLayout.addWidget(self.dynamips_workdir)
        self.dynamips_workdir_browser = QtGui.QToolButton(self.groupBox)
        self.dynamips_workdir_browser.setText(QtGui.QApplication.translate("PreferencesDynamips", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.dynamips_workdir_browser.setObjectName(_fromUtf8("dynamips_workdir_browser"))
        self.horizontalLayout.addWidget(self.dynamips_workdir_browser)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 4)
        self.checkBoxClearWorkdir = QtGui.QCheckBox(self.groupBox)
        self.checkBoxClearWorkdir.setText(QtGui.QApplication.translate("PreferencesDynamips", "Automatically clean the working directory", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxClearWorkdir.setChecked(True)
        self.checkBoxClearWorkdir.setObjectName(_fromUtf8("checkBoxClearWorkdir"))
        self.gridLayout.addWidget(self.checkBoxClearWorkdir, 4, 0, 1, 3)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setText(QtGui.QApplication.translate("PreferencesDynamips", "Base port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setText(QtGui.QApplication.translate("PreferencesDynamips", " Base UDP:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setText(QtGui.QApplication.translate("PreferencesDynamips", "Base console:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setText(QtGui.QApplication.translate("PreferencesDynamips", "Base AUX port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 5, 3, 1, 1)
        self.dynamips_port = QtGui.QSpinBox(self.groupBox)
        self.dynamips_port.setSuffix(_fromUtf8(" TCP"))
        self.dynamips_port.setMaximum(65535)
        self.dynamips_port.setProperty("value", 7200)
        self.dynamips_port.setObjectName(_fromUtf8("dynamips_port"))
        self.gridLayout.addWidget(self.dynamips_port, 6, 0, 1, 1)
        self.dynamips_baseUDP = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseUDP.setSuffix(_fromUtf8(" UDP"))
        self.dynamips_baseUDP.setMaximum(65535)
        self.dynamips_baseUDP.setProperty("value", 10001)
        self.dynamips_baseUDP.setObjectName(_fromUtf8("dynamips_baseUDP"))
        self.gridLayout.addWidget(self.dynamips_baseUDP, 6, 1, 1, 1)
        self.dynamips_baseConsole = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseConsole.setSuffix(_fromUtf8(" TCP"))
        self.dynamips_baseConsole.setMaximum(65535)
        self.dynamips_baseConsole.setProperty("value", 2001)
        self.dynamips_baseConsole.setObjectName(_fromUtf8("dynamips_baseConsole"))
        self.gridLayout.addWidget(self.dynamips_baseConsole, 6, 2, 1, 1)
        self.dynamips_baseAUX = QtGui.QSpinBox(self.groupBox)
        self.dynamips_baseAUX.setSuffix(_fromUtf8(" TCP"))
        self.dynamips_baseAUX.setMaximum(65535)
        self.dynamips_baseAUX.setProperty("value", 2501)
        self.dynamips_baseAUX.setObjectName(_fromUtf8("dynamips_baseAUX"))
        self.gridLayout.addWidget(self.dynamips_baseAUX, 6, 3, 1, 1)
        self.checkBoxGhosting = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGhosting.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable ghost IOS support", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxGhosting.setChecked(True)
        self.checkBoxGhosting.setObjectName(_fromUtf8("checkBoxGhosting"))
        self.gridLayout.addWidget(self.checkBoxGhosting, 7, 0, 1, 2)
        self.checkBoxMmap = QtGui.QCheckBox(self.groupBox)
        self.checkBoxMmap.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable mmap support", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxMmap.setChecked(True)
        self.checkBoxMmap.setObjectName(_fromUtf8("checkBoxMmap"))
        self.gridLayout.addWidget(self.checkBoxMmap, 8, 0, 1, 2)
        self.checkBoxJITsharing = QtGui.QCheckBox(self.groupBox)
        self.checkBoxJITsharing.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable JIT sharing support (Dynamips > 0.2.8 RC2)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxJITsharing.setChecked(True)
        self.checkBoxJITsharing.setObjectName(_fromUtf8("checkBoxJITsharing"))
        self.gridLayout.addWidget(self.checkBoxJITsharing, 9, 0, 1, 4)
        self.checkBoxSparseMem = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSparseMem.setText(QtGui.QApplication.translate("PreferencesDynamips", "Enable sparse memory support", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSparseMem.setChecked(False)
        self.checkBoxSparseMem.setObjectName(_fromUtf8("checkBoxSparseMem"))
        self.gridLayout.addWidget(self.checkBoxSparseMem, 10, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.pushButtonTestDynamips = QtGui.QPushButton(self.tab_1)
        self.pushButtonTestDynamips.setText(QtGui.QApplication.translate("PreferencesDynamips", "&Test Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTestDynamips.setObjectName(_fromUtf8("pushButtonTestDynamips"))
        self.hboxlayout.addWidget(self.pushButtonTestDynamips)
        self.labelDynamipsStatus = QtGui.QLabel(self.tab_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDynamipsStatus.sizePolicy().hasHeightForWidth())
        self.labelDynamipsStatus.setSizePolicy(sizePolicy)
        self.labelDynamipsStatus.setText(_fromUtf8(""))
        self.labelDynamipsStatus.setObjectName(_fromUtf8("labelDynamipsStatus"))
        self.hboxlayout.addWidget(self.labelDynamipsStatus)
        self.verticalLayout.addLayout(self.hboxlayout)
        spacerItem = QtGui.QSpacerItem(390, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_2)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesDynamips", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setText(QtGui.QApplication.translate("PreferencesDynamips", "Memory usage limit per hypervisor:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinBoxMemoryLimit = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxMemoryLimit.setSuffix(QtGui.QApplication.translate("PreferencesDynamips", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxMemoryLimit.setMaximum(1000000)
        self.spinBoxMemoryLimit.setSingleStep(128)
        self.spinBoxMemoryLimit.setProperty("value", 512)
        self.spinBoxMemoryLimit.setObjectName(_fromUtf8("spinBoxMemoryLimit"))
        self.gridlayout.addWidget(self.spinBoxMemoryLimit, 1, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setText(QtGui.QApplication.translate("PreferencesDynamips", "UDP incrementation:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridlayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.spinBoxUDPIncrementation = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxUDPIncrementation.setMaximum(100000)
        self.spinBoxUDPIncrementation.setSingleStep(10)
        self.spinBoxUDPIncrementation.setProperty("value", 100)
        self.spinBoxUDPIncrementation.setObjectName(_fromUtf8("spinBoxUDPIncrementation"))
        self.gridlayout.addWidget(self.spinBoxUDPIncrementation, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setText(QtGui.QApplication.translate("PreferencesDynamips", "IP/host binding:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.comboBoxBinding = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxBinding.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.comboBoxBinding.setObjectName(_fromUtf8("comboBoxBinding"))
        self.gridlayout.addWidget(self.comboBoxBinding, 6, 0, 1, 1)
        self.checkBoxHypervisorManagerImport = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxHypervisorManagerImport.setText(QtGui.QApplication.translate("PreferencesDynamips", "Use Hypervisor Manager when importing", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxHypervisorManagerImport.setChecked(True)
        self.checkBoxHypervisorManagerImport.setObjectName(_fromUtf8("checkBoxHypervisorManagerImport"))
        self.gridlayout.addWidget(self.checkBoxHypervisorManagerImport, 7, 0, 1, 1)
        self.checkBoxAllocatePerIOS = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxAllocatePerIOS.setText(QtGui.QApplication.translate("PreferencesDynamips", "Allocate a new hypervisor per IOS image", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAllocatePerIOS.setChecked(True)
        self.checkBoxAllocatePerIOS.setObjectName(_fromUtf8("checkBoxAllocatePerIOS"))
        self.gridlayout.addWidget(self.checkBoxAllocatePerIOS, 2, 0, 1, 1)
        self.vboxlayout1.addWidget(self.groupBox_2)
        spacerItem1 = QtGui.QSpacerItem(390, 101, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(PreferencesDynamips)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDynamips)

    def retranslateUi(self, PreferencesDynamips):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtGui.QApplication.translate("PreferencesDynamips", "Dynamips", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PreferencesDynamips", "Hypervisor Manager", None, QtGui.QApplication.UnicodeUTF8))

