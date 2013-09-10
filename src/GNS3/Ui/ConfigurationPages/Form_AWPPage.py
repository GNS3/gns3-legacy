# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_AWPPage.ui'
#
# Created: Mon Sep  9 21:29:23 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AWPPage(object):
    def setupUi(self, AWPPage):
        AWPPage.setObjectName(_fromUtf8("AWPPage"))
        AWPPage.resize(383, 414)
        AWPPage.setWindowTitle(QtGui.QApplication.translate("AWPPage", "AWP Router configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(AWPPage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_24 = QtGui.QLabel(AWPPage)
        self.label_24.setText(QtGui.QApplication.translate("AWPPage", "RAM:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout.addWidget(self.label_24, 0, 0, 1, 1)
        self.spinBoxRamSize = QtGui.QSpinBox(AWPPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRamSize.sizePolicy().hasHeightForWidth())
        self.spinBoxRamSize.setSizePolicy(sizePolicy)
        self.spinBoxRamSize.setSuffix(QtGui.QApplication.translate("AWPPage", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRamSize.setMaximum(100000)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty("value", 256)
        self.spinBoxRamSize.setObjectName(_fromUtf8("spinBoxRamSize"))
        self.gridLayout.addWidget(self.spinBoxRamSize, 0, 1, 1, 2)
        self.label_37 = QtGui.QLabel(AWPPage)
        self.label_37.setText(QtGui.QApplication.translate("AWPPage", "Number of NICs:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout.addWidget(self.label_37, 1, 0, 1, 1)
        self.spinBoxNics = QtGui.QSpinBox(AWPPage)
        self.spinBoxNics.setMinimum(0)
        self.spinBoxNics.setMaximum(100000)
        self.spinBoxNics.setSingleStep(1)
        self.spinBoxNics.setProperty("value", 6)
        self.spinBoxNics.setObjectName(_fromUtf8("spinBoxNics"))
        self.gridLayout.addWidget(self.spinBoxNics, 1, 1, 1, 2)
        self.label_26 = QtGui.QLabel(AWPPage)
        self.label_26.setText(QtGui.QApplication.translate("AWPPage", "NIC model:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout.addWidget(self.label_26, 2, 0, 1, 1)
        self.comboBoxNIC = QtGui.QComboBox(AWPPage)
        self.comboBoxNIC.setEnabled(True)
        self.comboBoxNIC.setObjectName(_fromUtf8("comboBoxNIC"))
        self.comboBoxNIC.addItem(_fromUtf8(""))
        self.comboBoxNIC.setItemText(0, QtGui.QApplication.translate("AWPPage", "virtio", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.comboBoxNIC, 2, 1, 1, 2)
        self.label_8 = QtGui.QLabel(AWPPage)
        self.label_8.setText(QtGui.QApplication.translate("AWPPage", "Qemu Options:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.lineEditOptions = QtGui.QLineEdit(AWPPage)
        self.lineEditOptions.setEnabled(True)
        self.lineEditOptions.setObjectName(_fromUtf8("lineEditOptions"))
        self.gridLayout.addWidget(self.lineEditOptions, 3, 1, 1, 2)
        self.checkBoxKVM = QtGui.QCheckBox(AWPPage)
        self.checkBoxKVM.setEnabled(True)
        self.checkBoxKVM.setText(QtGui.QApplication.translate("AWPPage", "Use KVM (Linux hosts only)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxKVM.setObjectName(_fromUtf8("checkBoxKVM"))
        self.gridLayout.addWidget(self.checkBoxKVM, 4, 0, 1, 2)
        self.label_21 = QtGui.QLabel(AWPPage)
        self.label_21.setText(QtGui.QApplication.translate("AWPPage", "AWP Release File:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout.addWidget(self.label_21, 5, 0, 1, 1)
        self.lineEditRel = QtGui.QLineEdit(AWPPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRel.sizePolicy().hasHeightForWidth())
        self.lineEditRel.setSizePolicy(sizePolicy)
        self.lineEditRel.setObjectName(_fromUtf8("lineEditRel"))
        self.gridLayout.addWidget(self.lineEditRel, 5, 1, 1, 1)
        self.pushButtonRelBrowser = QtGui.QPushButton(AWPPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRelBrowser.sizePolicy().hasHeightForWidth())
        self.pushButtonRelBrowser.setSizePolicy(sizePolicy)
        self.pushButtonRelBrowser.setMaximumSize(QtCore.QSize(31, 27))
        self.pushButtonRelBrowser.setText(QtGui.QApplication.translate("AWPPage", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRelBrowser.setObjectName(_fromUtf8("pushButtonRelBrowser"))
        self.gridLayout.addWidget(self.pushButtonRelBrowser, 5, 2, 1, 1)
        self.label_13 = QtGui.QLabel(AWPPage)
        self.label_13.setText(QtGui.QApplication.translate("AWPPage", "Kernel cmd line:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 6, 0, 1, 1)
        self.lineEditKernelCmdLine = QtGui.QLineEdit(AWPPage)
        self.lineEditKernelCmdLine.setObjectName(_fromUtf8("lineEditKernelCmdLine"))
        self.gridLayout.addWidget(self.lineEditKernelCmdLine, 6, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 281, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 3)

        self.retranslateUi(AWPPage)
        self.comboBoxNIC.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(AWPPage)

    def retranslateUi(self, AWPPage):
        pass

