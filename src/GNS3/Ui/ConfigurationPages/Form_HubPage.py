# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Thu Dec 11 23:13:43 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(HubPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.spinBoxNbPorts = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxNbPorts.sizePolicy().hasHeightForWidth())
        self.spinBoxNbPorts.setSizePolicy(sizePolicy)
        self.spinBoxNbPorts.setMinimum(0)
        self.spinBoxNbPorts.setMaximum(32)
        self.spinBoxNbPorts.setSingleStep(8)
        self.spinBoxNbPorts.setProperty("value",QtCore.QVariant(8))
        self.spinBoxNbPorts.setObjectName("spinBoxNbPorts")
        self.gridlayout1.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

