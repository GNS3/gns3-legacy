# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_FRSWPage.ui'
#
# Created: Fri Aug 10 14:00:12 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,379,289).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(FRSWPage)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.spinBoxPort = QtGui.QSpinBox(self.groupBox)
        self.spinBoxPort.setMinimum(0)
        self.spinBoxPort.setMaximum(65535)
        self.spinBoxPort.setProperty("value",QtCore.QVariant(1))
        self.spinBoxPort.setObjectName("spinBoxPort")
        self.gridlayout1.addWidget(self.spinBoxPort,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.spinBoxDLCI = QtGui.QSpinBox(self.groupBox)
        self.spinBoxDLCI.setMaximum(65535)
        self.spinBoxDLCI.setProperty("value",QtCore.QVariant(100))
        self.spinBoxDLCI.setObjectName("spinBoxDLCI")
        self.gridlayout1.addWidget(self.spinBoxDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,2)

        spacerItem = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,2,1,1)

        self.treeWidgetVCmap = QtGui.QTreeWidget(FRSWPage)
        self.treeWidgetVCmap.setObjectName("treeWidgetVCmap")
        self.gridlayout.addWidget(self.treeWidgetVCmap,0,3,3,1)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,1,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(168,121,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

