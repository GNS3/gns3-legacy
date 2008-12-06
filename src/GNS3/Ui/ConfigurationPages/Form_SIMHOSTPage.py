# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_SIMHOSTPage.ui'
#
# Created: Sat Dec  6 20:36:13 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SIMHOSTPage(object):
    def setupUi(self, SIMHOSTPage):
        SIMHOSTPage.setObjectName("SIMHOSTPage")
        SIMHOSTPage.resize(QtCore.QSize(QtCore.QRect(0,0,553,337).size()).expandedTo(SIMHOSTPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(SIMHOSTPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(SIMHOSTPage)

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

        self.spinBoxID = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxID.sizePolicy().hasHeightForWidth())
        self.spinBoxID.setSizePolicy(sizePolicy)
        self.spinBoxID.setMinimum(0)
        self.spinBoxID.setMaximum(255)
        self.spinBoxID.setProperty("value",QtCore.QVariant(0))
        self.spinBoxID.setObjectName("spinBoxID")
        self.gridlayout1.addWidget(self.spinBoxID,0,1,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,1,0,1,1)

        self.lineEdit_IP = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.gridlayout1.addWidget(self.lineEdit_IP,1,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,2,0,1,1)

        self.lineEdit_Mask = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Mask.setObjectName("lineEdit_Mask")
        self.gridlayout1.addWidget(self.lineEdit_Mask,2,1,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,3,0,1,1)

        self.lineEdit_Gateway = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Gateway.setObjectName("lineEdit_Gateway")
        self.gridlayout1.addWidget(self.lineEdit_Gateway,3,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(SIMHOSTPage)
        self.groupBox_2.setObjectName("groupBox_2")

        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout.setObjectName("vboxlayout")

        self.treeWidgetInterfaces = QtGui.QTreeWidget(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidgetInterfaces.sizePolicy().hasHeightForWidth())
        self.treeWidgetInterfaces.setSizePolicy(sizePolicy)
        self.treeWidgetInterfaces.setRootIsDecorated(False)
        self.treeWidgetInterfaces.setObjectName("treeWidgetInterfaces")
        self.vboxlayout.addWidget(self.treeWidgetInterfaces)
        self.gridlayout.addWidget(self.groupBox_2,0,2,3,1)

        self.pushButtonAdd = QtGui.QPushButton(SIMHOSTPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,1,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(SIMHOSTPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(20,101,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,2,1,1,1)

        self.retranslateUi(SIMHOSTPage)
        QtCore.QMetaObject.connectSlotsByName(SIMHOSTPage)
        SIMHOSTPage.setTabOrder(self.spinBoxID,self.pushButtonAdd)
        SIMHOSTPage.setTabOrder(self.pushButtonAdd,self.pushButtonDelete)
        SIMHOSTPage.setTabOrder(self.pushButtonDelete,self.treeWidgetInterfaces)

    def retranslateUi(self, SIMHOSTPage):
        SIMHOSTPage.setWindowTitle(QtGui.QApplication.translate("SIMHOSTPage", "Ethernet Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SIMHOSTPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SIMHOSTPage", "Interface ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SIMHOSTPage", "IP address:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_IP.setText(QtGui.QApplication.translate("SIMHOSTPage", "192.168.1.1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SIMHOSTPage", "Mask:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_Mask.setText(QtGui.QApplication.translate("SIMHOSTPage", "255.255.255.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SIMHOSTPage", "Gateway:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_Gateway.setText(QtGui.QApplication.translate("SIMHOSTPage", "192.168.1.254", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SIMHOSTPage", "Interfaces", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetInterfaces.headerItem().setText(0,QtGui.QApplication.translate("SIMHOSTPage", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetInterfaces.headerItem().setText(1,QtGui.QApplication.translate("SIMHOSTPage", "IP address", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetInterfaces.headerItem().setText(2,QtGui.QApplication.translate("SIMHOSTPage", "Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetInterfaces.headerItem().setText(3,QtGui.QApplication.translate("SIMHOSTPage", "Gateway", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("SIMHOSTPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("SIMHOSTPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

