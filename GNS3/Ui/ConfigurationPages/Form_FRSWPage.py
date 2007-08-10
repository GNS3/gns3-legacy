# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_FRSWPage.ui'
#
# Created: Fri Aug 10 10:42:29 2007
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

        self.lineEditPort = QtGui.QLineEdit(self.groupBox)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridlayout1.addWidget(self.lineEditPort,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.lineEditDLCI = QtGui.QLineEdit(self.groupBox)
        self.lineEditDLCI.setObjectName("lineEditDLCI")
        self.gridlayout1.addWidget(self.lineEditDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,2)

        spacerItem = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,2,1,1)

        self.treeWidgetVCmap = QtGui.QTreeWidget(FRSWPage)
        self.treeWidgetVCmap.setObjectName("treeWidgetVCmap")
        self.gridlayout.addWidget(self.treeWidgetVCmap,0,3,3,1)

        self.pushButtonSave = QtGui.QPushButton(FRSWPage)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridlayout.addWidget(self.pushButtonSave,1,0,1,1)

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
        self.pushButtonSave.setText(QtGui.QApplication.translate("FRSWPage", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

