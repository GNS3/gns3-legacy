# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Mon Sep  9 21:29:22 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName(_fromUtf8("HubPage"))
        HubPage.resize(381, 270)
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet hub", None, QtGui.QApplication.UnicodeUTF8))
        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.groupBox = QtGui.QGroupBox(HubPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("HubPage", "Number of ports:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.spinBoxNumberOfPorts = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxNumberOfPorts.sizePolicy().hasHeightForWidth())
        self.spinBoxNumberOfPorts.setSizePolicy(sizePolicy)
        self.spinBoxNumberOfPorts.setMinimum(0)
        self.spinBoxNumberOfPorts.setMaximum(65535)
        self.spinBoxNumberOfPorts.setProperty("value", 1)
        self.spinBoxNumberOfPorts.setObjectName(_fromUtf8("spinBoxNumberOfPorts"))
        self.gridlayout1.addWidget(self.spinBoxNumberOfPorts, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 71, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem, 1, 1, 1, 1)
        self.gridlayout.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        pass

