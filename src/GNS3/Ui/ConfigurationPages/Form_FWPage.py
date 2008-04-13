# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FWPage.ui'
#
# Created: Sun Apr 13 03:51:41 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FWPage(object):
    def setupUi(self, FWPage):
        FWPage.setObjectName("FWPage")
        FWPage.resize(QtCore.QSize(QtCore.QRect(0,0,439,462).size()).expandedTo(FWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.label_17 = QtGui.QLabel(FWPage)
        self.label_17.setObjectName("label_17")
        self.gridlayout.addWidget(self.label_17,0,0,1,1)

        self.lineEditImage = QtGui.QLineEdit(FWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditImage.sizePolicy().hasHeightForWidth())
        self.lineEditImage.setSizePolicy(sizePolicy)
        self.lineEditImage.setObjectName("lineEditImage")
        self.gridlayout.addWidget(self.lineEditImage,0,1,1,1)

        self.pushButtonImageBrowser = QtGui.QPushButton(FWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonImageBrowser.sizePolicy().hasHeightForWidth())
        self.pushButtonImageBrowser.setSizePolicy(sizePolicy)
        self.pushButtonImageBrowser.setMaximumSize(QtCore.QSize(31,27))
        self.pushButtonImageBrowser.setObjectName("pushButtonImageBrowser")
        self.gridlayout.addWidget(self.pushButtonImageBrowser,0,2,1,1)

        self.label_24 = QtGui.QLabel(FWPage)
        self.label_24.setObjectName("label_24")
        self.gridlayout.addWidget(self.label_24,1,0,1,1)

        self.spinBoxRamSize = QtGui.QSpinBox(FWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRamSize.sizePolicy().hasHeightForWidth())
        self.spinBoxRamSize.setSizePolicy(sizePolicy)
        self.spinBoxRamSize.setMaximum(4096)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty("value",QtCore.QVariant(128))
        self.spinBoxRamSize.setObjectName("spinBoxRamSize")
        self.gridlayout.addWidget(self.spinBoxRamSize,1,1,1,2)

        self.label_20 = QtGui.QLabel(FWPage)
        self.label_20.setObjectName("label_20")
        self.gridlayout.addWidget(self.label_20,2,0,1,1)

        self.lineEditKey = QtGui.QLineEdit(FWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditKey.sizePolicy().hasHeightForWidth())
        self.lineEditKey.setSizePolicy(sizePolicy)
        self.lineEditKey.setObjectName("lineEditKey")
        self.gridlayout.addWidget(self.lineEditKey,2,1,1,2)

        self.label_21 = QtGui.QLabel(FWPage)
        self.label_21.setObjectName("label_21")
        self.gridlayout.addWidget(self.label_21,3,0,1,1)

        self.lineEditSerial = QtGui.QLineEdit(FWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSerial.sizePolicy().hasHeightForWidth())
        self.lineEditSerial.setSizePolicy(sizePolicy)
        self.lineEditSerial.setObjectName("lineEditSerial")
        self.gridlayout.addWidget(self.lineEditSerial,3,1,1,2)

        spacerItem = QtGui.QSpacerItem(20,281,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,4,1,1,1)

        self.retranslateUi(FWPage)
        QtCore.QMetaObject.connectSlotsByName(FWPage)

    def retranslateUi(self, FWPage):
        FWPage.setWindowTitle(QtGui.QApplication.translate("FWPage", "Firewall configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("FWPage", "PIX Image:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonImageBrowser.setText(QtGui.QApplication.translate("FWPage", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("FWPage", "RAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRamSize.setSuffix(QtGui.QApplication.translate("FWPage", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("FWPage", "Key:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("FWPage", "Serial:", None, QtGui.QApplication.UnicodeUTF8))

