# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_ATMBRPage.ui'
#
# Created: Fri Feb 26 21:48:58 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ATMBRPage(object):
    def setupUi(self, ATMBRPage):
        ATMBRPage.setObjectName("ATMBRPage")
        ATMBRPage.resize(403, 383)
        self.gridlayout = QtGui.QGridLayout(ATMBRPage)
        self.gridlayout.setObjectName("gridlayout")
        self.groupBox = QtGui.QGroupBox(ATMBRPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.spinBoxSrcPort = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcPort.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcPort.setSizePolicy(sizePolicy)
        self.spinBoxSrcPort.setMinimum(0)
        self.spinBoxSrcPort.setMaximum(65535)
        self.spinBoxSrcPort.setProperty("value", 1)
        self.spinBoxSrcPort.setObjectName("spinBoxSrcPort")
        self.gridlayout1.addWidget(self.spinBoxSrcPort, 0, 1, 1, 1)
        self.gridlayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(ATMBRPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout.setObjectName("vboxlayout")
        self.treeWidgetMapping = QtGui.QTreeWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidgetMapping.sizePolicy().hasHeightForWidth())
        self.treeWidgetMapping.setSizePolicy(sizePolicy)
        self.treeWidgetMapping.setRootIsDecorated(False)
        self.treeWidgetMapping.setObjectName("treeWidgetMapping")
        self.vboxlayout.addWidget(self.treeWidgetMapping)
        self.gridlayout.addWidget(self.groupBox_2, 0, 2, 3, 1)
        self.groupBox_3 = QtGui.QGroupBox(ATMBRPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout2.setObjectName("gridlayout2")
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3, 0, 0, 1, 1)
        self.spinBoxDestPort = QtGui.QSpinBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestPort.sizePolicy().hasHeightForWidth())
        self.spinBoxDestPort.setSizePolicy(sizePolicy)
        self.spinBoxDestPort.setMinimum(0)
        self.spinBoxDestPort.setMaximum(65535)
        self.spinBoxDestPort.setProperty("value", 10)
        self.spinBoxDestPort.setObjectName("spinBoxDestPort")
        self.gridlayout2.addWidget(self.spinBoxDestPort, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout2.addWidget(self.label_6, 1, 0, 1, 1)
        self.spinBoxDestVCI = QtGui.QSpinBox(self.groupBox_3)
        self.spinBoxDestVCI.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestVCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestVCI.setSizePolicy(sizePolicy)
        self.spinBoxDestVCI.setMinimum(1)
        self.spinBoxDestVCI.setMaximum(65535)
        self.spinBoxDestVCI.setProperty("value", 1)
        self.spinBoxDestVCI.setObjectName("spinBoxDestVCI")
        self.gridlayout2.addWidget(self.spinBoxDestVCI, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4, 2, 0, 1, 1)
        self.spinBoxDestVPI = QtGui.QSpinBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestVPI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestVPI.setSizePolicy(sizePolicy)
        self.spinBoxDestVPI.setMaximum(65535)
        self.spinBoxDestVPI.setProperty("value", 202)
        self.spinBoxDestVPI.setObjectName("spinBoxDestVPI")
        self.gridlayout2.addWidget(self.spinBoxDestVPI, 2, 1, 1, 1)
        self.gridlayout.addWidget(self.groupBox_3, 1, 0, 1, 2)
        self.pushButtonAdd = QtGui.QPushButton(ATMBRPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd, 2, 0, 1, 1)
        self.pushButtonDelete = QtGui.QPushButton(ATMBRPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(371, 121, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 3)

        self.retranslateUi(ATMBRPage)
        QtCore.QMetaObject.connectSlotsByName(ATMBRPage)
        ATMBRPage.setTabOrder(self.spinBoxSrcPort, self.spinBoxDestPort)
        ATMBRPage.setTabOrder(self.spinBoxDestPort, self.spinBoxDestVCI)
        ATMBRPage.setTabOrder(self.spinBoxDestVCI, self.spinBoxDestVPI)
        ATMBRPage.setTabOrder(self.spinBoxDestVPI, self.pushButtonAdd)
        ATMBRPage.setTabOrder(self.pushButtonAdd, self.pushButtonDelete)
        ATMBRPage.setTabOrder(self.pushButtonDelete, self.treeWidgetMapping)

    def retranslateUi(self, ATMBRPage):
        ATMBRPage.setWindowTitle(QtGui.QApplication.translate("ATMBRPage", "ATM Bridge", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ATMBRPage", "Ethernet side", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ATMBRPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ATMBRPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetMapping.headerItem().setText(0, QtGui.QApplication.translate("ATMBRPage", "Ethernet Port", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetMapping.headerItem().setText(1, QtGui.QApplication.translate("ATMBRPage", "Port:VCI:VPI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("ATMBRPage", "ATM side", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ATMBRPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ATMBRPage", "VCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ATMBRPage", "VPI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("ATMBRPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("ATMBRPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

