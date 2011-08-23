# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_VirtualBoxPage.ui'
#
# Created: Thu May  5 11:38:45 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VirtualBoxPage(object):
    def setupUi(self, VirtualBoxPage):
        VirtualBoxPage.setObjectName("VirtualBoxPage")
        VirtualBoxPage.resize(419, 453)
        self.gridLayout = QtGui.QGridLayout(VirtualBoxPage)
        self.gridLayout.setObjectName("gridLayout")
        self.label_17 = QtGui.QLabel(VirtualBoxPage)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 0, 1, 1)
        self.lineEditImage = QtGui.QLineEdit(VirtualBoxPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditImage.sizePolicy().hasHeightForWidth())
        self.lineEditImage.setSizePolicy(sizePolicy)
        self.lineEditImage.setObjectName("lineEditImage")
        self.gridLayout.addWidget(self.lineEditImage, 0, 1, 1, 1)
        self.label_37 = QtGui.QLabel(VirtualBoxPage)
        self.label_37.setEnabled(True)
        self.label_37.setObjectName("label_37")
        self.gridLayout.addWidget(self.label_37, 1, 0, 1, 1)
        self.spinBoxNics = QtGui.QSpinBox(VirtualBoxPage)
        self.spinBoxNics.setEnabled(True)
        self.spinBoxNics.setMinimum(0)
        self.spinBoxNics.setMaximum(7)
        self.spinBoxNics.setSingleStep(1)
        self.spinBoxNics.setProperty("value", 6)
        self.spinBoxNics.setObjectName("spinBoxNics")
        self.gridLayout.addWidget(self.spinBoxNics, 1, 1, 1, 1)
        self.label_26 = QtGui.QLabel(VirtualBoxPage)
        self.label_26.setEnabled(True)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 2, 0, 1, 1)
        self.comboBoxNIC = QtGui.QComboBox(VirtualBoxPage)
        self.comboBoxNIC.setEnabled(True)
        self.comboBoxNIC.setObjectName("comboBoxNIC")
        self.comboBoxNIC.addItem("")
        self.comboBoxNIC.addItem("")
        self.comboBoxNIC.addItem("")
        self.comboBoxNIC.addItem("")
        self.comboBoxNIC.addItem("")
        self.gridLayout.addWidget(self.comboBoxNIC, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 281, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)

        self.retranslateUi(VirtualBoxPage)
        self.comboBoxNIC.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(VirtualBoxPage)

    def retranslateUi(self, VirtualBoxPage):
        VirtualBoxPage.setWindowTitle(QtGui.QApplication.translate("VirtualBoxPage", "VirtualBox configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("VirtualBoxPage", "VM Name / UUID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setText(QtGui.QApplication.translate("VirtualBoxPage", "Number of NICs:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("VirtualBoxPage", "NIC model:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.setItemText(0, QtGui.QApplication.translate("VirtualBoxPage", "automatic", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.setItemText(1, QtGui.QApplication.translate("VirtualBoxPage", "e1000", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.setItemText(2, QtGui.QApplication.translate("VirtualBoxPage", "pcnet2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.setItemText(3, QtGui.QApplication.translate("VirtualBoxPage", "pcnet3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxNIC.setItemText(4, QtGui.QApplication.translate("VirtualBoxPage", "virtio", None, QtGui.QApplication.UnicodeUTF8))

