# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_ATMSWPage.ui'
#
# Created: Tue Sep 18 10:20:33 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ATMSWPage(object):
    def setupUi(self, ATMSWPage):
        ATMSWPage.setObjectName("ATMSWPage")
        ATMSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,403,476).size()).expandedTo(ATMSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(ATMSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(ATMSWPage)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout1.setObjectName("gridlayout1")

        self.checkBoxIntegratedHypervisor = QtGui.QCheckBox(self.groupBox_4)
        self.checkBoxIntegratedHypervisor.setChecked(True)
        self.checkBoxIntegratedHypervisor.setObjectName("checkBoxIntegratedHypervisor")
        self.gridlayout1.addWidget(self.checkBoxIntegratedHypervisor,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,1,1,1)

        self.comboBoxHypervisors = QtGui.QComboBox(self.groupBox_4)
        self.comboBoxHypervisors.setEnabled(False)
        self.comboBoxHypervisors.setObjectName("comboBoxHypervisors")
        self.gridlayout1.addWidget(self.comboBoxHypervisors,1,0,1,2)
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,3)

        self.checkBoxVCI = QtGui.QCheckBox(ATMSWPage)
        self.checkBoxVCI.setObjectName("checkBoxVCI")
        self.gridlayout.addWidget(self.checkBoxVCI,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(ATMSWPage)
        self.groupBox_2.setObjectName("groupBox_2")

        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout.setObjectName("vboxlayout")

        self.treeWidgetVCmap = QtGui.QTreeWidget(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidgetVCmap.sizePolicy().hasHeightForWidth())
        self.treeWidgetVCmap.setSizePolicy(sizePolicy)
        self.treeWidgetVCmap.setRootIsDecorated(False)
        self.treeWidgetVCmap.setObjectName("treeWidgetVCmap")
        self.vboxlayout.addWidget(self.treeWidgetVCmap)
        self.gridlayout.addWidget(self.groupBox_2,1,2,4,1)

        self.groupBox = QtGui.QGroupBox(ATMSWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout2.addWidget(self.label,0,0,1,1)

        self.spinBoxSrcPort = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcPort.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcPort.setSizePolicy(sizePolicy)
        self.spinBoxSrcPort.setMinimum(0)
        self.spinBoxSrcPort.setMaximum(65535)
        self.spinBoxSrcPort.setProperty("value",QtCore.QVariant(1))
        self.spinBoxSrcPort.setObjectName("spinBoxSrcPort")
        self.gridlayout2.addWidget(self.spinBoxSrcPort,0,1,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,1,0,1,1)

        self.spinBoxSrcVCI = QtGui.QSpinBox(self.groupBox)
        self.spinBoxSrcVCI.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcVCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcVCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcVCI.setMaximum(65535)
        self.spinBoxSrcVCI.setProperty("value",QtCore.QVariant(0))
        self.spinBoxSrcVCI.setObjectName("spinBoxSrcVCI")
        self.gridlayout2.addWidget(self.spinBoxSrcVCI,1,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,2,0,1,1)

        self.spinBoxSrcVPI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcVPI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcVPI.setSizePolicy(sizePolicy)
        self.spinBoxSrcVPI.setMaximum(65535)
        self.spinBoxSrcVPI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcVPI.setObjectName("spinBoxSrcVPI")
        self.gridlayout2.addWidget(self.spinBoxSrcVPI,2,1,1,1)
        self.gridlayout.addWidget(self.groupBox,2,0,1,2)

        self.groupBox_3 = QtGui.QGroupBox(ATMSWPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout3.addWidget(self.label_3,0,0,1,1)

        self.spinBoxDestPort = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestPort.sizePolicy().hasHeightForWidth())
        self.spinBoxDestPort.setSizePolicy(sizePolicy)
        self.spinBoxDestPort.setMinimum(0)
        self.spinBoxDestPort.setMaximum(65535)
        self.spinBoxDestPort.setProperty("value",QtCore.QVariant(10))
        self.spinBoxDestPort.setObjectName("spinBoxDestPort")
        self.gridlayout3.addWidget(self.spinBoxDestPort,0,1,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,1,0,1,1)

        self.spinBoxDestVCI = QtGui.QSpinBox(self.groupBox_3)
        self.spinBoxDestVCI.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestVCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestVCI.setSizePolicy(sizePolicy)
        self.spinBoxDestVCI.setMaximum(65535)
        self.spinBoxDestVCI.setProperty("value",QtCore.QVariant(0))
        self.spinBoxDestVCI.setObjectName("spinBoxDestVCI")
        self.gridlayout3.addWidget(self.spinBoxDestVCI,1,1,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,2,0,1,1)

        self.spinBoxDestVPI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestVPI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestVPI.setSizePolicy(sizePolicy)
        self.spinBoxDestVPI.setMaximum(65535)
        self.spinBoxDestVPI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestVPI.setObjectName("spinBoxDestVPI")
        self.gridlayout3.addWidget(self.spinBoxDestVPI,2,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,3,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(ATMSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,4,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(ATMSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,4,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(213,31,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,5,2,1,1)

        self.retranslateUi(ATMSWPage)
        QtCore.QMetaObject.connectSlotsByName(ATMSWPage)

    def retranslateUi(self, ATMSWPage):
        ATMSWPage.setWindowTitle(QtGui.QApplication.translate("ATMSWPage", "ATM Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("ATMSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("ATMSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxVCI.setText(QtGui.QApplication.translate("ATMSWPage", "Use VCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ATMSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("ATMSWPage", "Port:VCI:VPI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("ATMSWPage", "Port:VCI:VPI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ATMSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ATMSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ATMSWPage", "VCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ATMSWPage", "VPI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("ATMSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ATMSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ATMSWPage", "VCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ATMSWPage", "VPI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("ATMSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("ATMSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

