# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_Snapshots.ui'
#
# Created: Thu Feb 11 12:23:18 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Snapshots(object):
    def setupUi(self, Snapshots):
        Snapshots.setObjectName("Snapshots")
        Snapshots.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Snapshots)
        self.gridLayout.setObjectName("gridLayout")
        self.SnapshotList = QtGui.QListWidget(Snapshots)
        self.SnapshotList.setObjectName("SnapshotList")
        self.gridLayout.addWidget(self.SnapshotList, 0, 0, 1, 3)
        self.pushButtonCreate = QtGui.QPushButton(Snapshots)
        self.pushButtonCreate.setObjectName("pushButtonCreate")
        self.gridLayout.addWidget(self.pushButtonCreate, 1, 0, 1, 1)
        self.pushButtonLoad = QtGui.QPushButton(Snapshots)
        self.pushButtonLoad.setObjectName("pushButtonLoad")
        self.gridLayout.addWidget(self.pushButtonLoad, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Snapshots)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(Snapshots)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Snapshots.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Snapshots.reject)
        QtCore.QMetaObject.connectSlotsByName(Snapshots)

    def retranslateUi(self, Snapshots):
        Snapshots.setWindowTitle(QtGui.QApplication.translate("Snapshots", "Snapshots", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCreate.setText(QtGui.QApplication.translate("Snapshots", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLoad.setText(QtGui.QApplication.translate("Snapshots", "Load", None, QtGui.QApplication.UnicodeUTF8))

