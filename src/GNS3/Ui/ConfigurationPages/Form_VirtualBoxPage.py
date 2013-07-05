# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_VirtualBoxPage.ui'
#
# Created: Fri Jul  5 13:39:31 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VirtualBoxPage(object):
    def setupUi(self, VirtualBoxPage):
        VirtualBoxPage.setObjectName(_fromUtf8("VirtualBoxPage"))
        VirtualBoxPage.resize(415, 446)
        VirtualBoxPage.setWindowTitle(QtGui.QApplication.translate("VirtualBoxPage", "VirtualBox configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(VirtualBoxPage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_17 = QtGui.QLabel(VirtualBoxPage)
        self.label_17.setText(QtGui.QApplication.translate("VirtualBoxPage", "VM Name / UUID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout.addWidget(self.label_17, 0, 0, 1, 1)
        self.lineEditImage = QtGui.QLineEdit(VirtualBoxPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditImage.sizePolicy().hasHeightForWidth())
        self.lineEditImage.setSizePolicy(sizePolicy)
        self.lineEditImage.setReadOnly(True)
        self.lineEditImage.setObjectName(_fromUtf8("lineEditImage"))
        self.gridLayout.addWidget(self.lineEditImage, 0, 1, 1, 1)
        self.label_37 = QtGui.QLabel(VirtualBoxPage)
        self.label_37.setEnabled(True)
        self.label_37.setText(QtGui.QApplication.translate("VirtualBoxPage", "Number of NICs:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout.addWidget(self.label_37, 1, 0, 1, 1)
        self.spinBoxNics = QtGui.QSpinBox(VirtualBoxPage)
        self.spinBoxNics.setEnabled(True)
        self.spinBoxNics.setToolTip(QtGui.QApplication.translate("VirtualBoxPage", "Maximum NICs with PIIX3 chipset is 8.\n"
"Maximum NICs with ICH9 chipset is 36.\n"
"Please, see VirtualBox settings to change the chipset.", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxNics.setMinimum(2)
        self.spinBoxNics.setMaximum(36)
        self.spinBoxNics.setSingleStep(1)
        self.spinBoxNics.setProperty("value", 6)
        self.spinBoxNics.setObjectName(_fromUtf8("spinBoxNics"))
        self.gridLayout.addWidget(self.spinBoxNics, 1, 1, 1, 1)
        self.label_26 = QtGui.QLabel(VirtualBoxPage)
        self.label_26.setEnabled(True)
        self.label_26.setText(QtGui.QApplication.translate("VirtualBoxPage", "NIC model:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout.addWidget(self.label_26, 2, 0, 1, 1)
        self.comboBoxNIC = QtGui.QComboBox(VirtualBoxPage)
        self.comboBoxNIC.setEnabled(True)
        self.comboBoxNIC.setObjectName(_fromUtf8("comboBoxNIC"))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(0, QtGui.QApplication.translate("VirtualBoxPage", "automatic", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(1, QtGui.QApplication.translate("VirtualBoxPage", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(2, QtGui.QApplication.translate("VirtualBoxPage", "pcnet2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(3, QtGui.QApplication.translate("VirtualBoxPage", "pcnet3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(4, QtGui.QApplication.translate("VirtualBoxPage", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.comboBoxNIC, 2, 1, 1, 1)
        self.checkBoxVBoxFirstInterfaceManaged = QtGui.QCheckBox(VirtualBoxPage)
        self.checkBoxVBoxFirstInterfaceManaged.setText(QtGui.QApplication.translate("VirtualBoxPage", "Reserve first NIC for VirtualBox NAT to host OS", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxVBoxFirstInterfaceManaged.setChecked(True)
        self.checkBoxVBoxFirstInterfaceManaged.setObjectName(_fromUtf8("checkBoxVBoxFirstInterfaceManaged"))
        self.gridLayout.addWidget(self.checkBoxVBoxFirstInterfaceManaged, 3, 0, 1, 2)
        self.checkBoxVboxConsoleSupport = QtGui.QCheckBox(VirtualBoxPage)
        self.checkBoxVboxConsoleSupport.setText(QtGui.QApplication.translate("VirtualBoxPage", "Enable console support", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxVboxConsoleSupport.setObjectName(_fromUtf8("checkBoxVboxConsoleSupport"))
        self.gridLayout.addWidget(self.checkBoxVboxConsoleSupport, 4, 0, 1, 2)
        self.checkBoxVboxConsoleServer = QtGui.QCheckBox(VirtualBoxPage)
        self.checkBoxVboxConsoleServer.setEnabled(False)
        self.checkBoxVboxConsoleServer.setText(QtGui.QApplication.translate("VirtualBoxPage", "Enable console server (for remote access)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxVboxConsoleServer.setObjectName(_fromUtf8("checkBoxVboxConsoleServer"))
        self.gridLayout.addWidget(self.checkBoxVboxConsoleServer, 5, 0, 1, 2)
        self.checkBoxVBoxHeadlessMode = QtGui.QCheckBox(VirtualBoxPage)
        self.checkBoxVBoxHeadlessMode.setText(QtGui.QApplication.translate("VirtualBoxPage", "Start in headless mode (without GUI)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxVBoxHeadlessMode.setObjectName(_fromUtf8("checkBoxVBoxHeadlessMode"))
        self.gridLayout.addWidget(self.checkBoxVBoxHeadlessMode, 6, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 281, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 1, 1, 1)

        self.retranslateUi(VirtualBoxPage)
        self.comboBoxNIC.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VirtualBoxPage)

    def retranslateUi(self, VirtualBoxPage):
        pass

