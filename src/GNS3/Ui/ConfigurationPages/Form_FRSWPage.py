# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FRSWPage.ui'
#
# Created: Wed Sep 26 18:58:45 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(FRSWPage)
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

        self.groupBox = QtGui.QGroupBox(FRSWPage)

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

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)

        self.spinBoxSrcDLCI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcDLCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcDLCI.setMaximum(65535)
        self.spinBoxSrcDLCI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcDLCI.setObjectName("spinBoxSrcDLCI")
        self.gridlayout2.addWidget(self.spinBoxSrcDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(FRSWPage)
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
        self.gridlayout.addWidget(self.groupBox_2,1,2,3,1)

        self.groupBox_3 = QtGui.QGroupBox(FRSWPage)

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

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,1,0,1,1)

        self.spinBoxDestDLCI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestDLCI.setSizePolicy(sizePolicy)
        self.spinBoxDestDLCI.setMaximum(65535)
        self.spinBoxDestDLCI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestDLCI.setObjectName("spinBoxDestDLCI")
        self.gridlayout3.addWidget(self.spinBoxDestDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,3,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,1,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("FRSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("FRSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("FRSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FRSWPage.ui'
#
# Created: Sun Oct 14 19:23:34 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(FRSWPage)
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

        self.groupBox = QtGui.QGroupBox(FRSWPage)

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

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)

        self.spinBoxSrcDLCI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcDLCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcDLCI.setMaximum(65535)
        self.spinBoxSrcDLCI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcDLCI.setObjectName("spinBoxSrcDLCI")
        self.gridlayout2.addWidget(self.spinBoxSrcDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(FRSWPage)
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
        self.gridlayout.addWidget(self.groupBox_2,1,2,3,1)

        self.groupBox_3 = QtGui.QGroupBox(FRSWPage)

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

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,1,0,1,1)

        self.spinBoxDestDLCI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestDLCI.setSizePolicy(sizePolicy)
        self.spinBoxDestDLCI.setMaximum(65535)
        self.spinBoxDestDLCI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestDLCI.setObjectName("spinBoxDestDLCI")
        self.gridlayout3.addWidget(self.spinBoxDestDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,3,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,1,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("FRSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("FRSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("FRSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FRSWPage.ui'
#
# Created: Sun Oct 14 19:33:17 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(FRSWPage)
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

        self.groupBox = QtGui.QGroupBox(FRSWPage)

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

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)

        self.spinBoxSrcDLCI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcDLCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcDLCI.setMaximum(65535)
        self.spinBoxSrcDLCI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcDLCI.setObjectName("spinBoxSrcDLCI")
        self.gridlayout2.addWidget(self.spinBoxSrcDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(FRSWPage)
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
        self.gridlayout.addWidget(self.groupBox_2,1,2,3,1)

        self.groupBox_3 = QtGui.QGroupBox(FRSWPage)

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

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,1,0,1,1)

        self.spinBoxDestDLCI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestDLCI.setSizePolicy(sizePolicy)
        self.spinBoxDestDLCI.setMaximum(65535)
        self.spinBoxDestDLCI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestDLCI.setObjectName("spinBoxDestDLCI")
        self.gridlayout3.addWidget(self.spinBoxDestDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,3,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,1,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("FRSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("FRSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("FRSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FRSWPage.ui'
#
# Created: Sun Oct 14 19:33:54 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(FRSWPage)
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

        self.groupBox = QtGui.QGroupBox(FRSWPage)

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

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)

        self.spinBoxSrcDLCI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcDLCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcDLCI.setMaximum(65535)
        self.spinBoxSrcDLCI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcDLCI.setObjectName("spinBoxSrcDLCI")
        self.gridlayout2.addWidget(self.spinBoxSrcDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(FRSWPage)
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
        self.gridlayout.addWidget(self.groupBox_2,1,2,3,1)

        self.groupBox_3 = QtGui.QGroupBox(FRSWPage)

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

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,1,0,1,1)

        self.spinBoxDestDLCI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestDLCI.setSizePolicy(sizePolicy)
        self.spinBoxDestDLCI.setMaximum(65535)
        self.spinBoxDestDLCI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestDLCI.setObjectName("spinBoxDestDLCI")
        self.gridlayout3.addWidget(self.spinBoxDestDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,3,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,1,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("FRSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("FRSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("FRSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_FRSWPage.ui'
#
# Created: Sun Oct 14 19:43:27 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FRSWPage(object):
    def setupUi(self, FRSWPage):
        FRSWPage.setObjectName("FRSWPage")
        FRSWPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(FRSWPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FRSWPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(FRSWPage)
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

        self.groupBox = QtGui.QGroupBox(FRSWPage)

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

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,1,0,1,1)

        self.spinBoxSrcDLCI = QtGui.QSpinBox(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSrcDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxSrcDLCI.setSizePolicy(sizePolicy)
        self.spinBoxSrcDLCI.setMaximum(65535)
        self.spinBoxSrcDLCI.setProperty("value",QtCore.QVariant(101))
        self.spinBoxSrcDLCI.setObjectName("spinBoxSrcDLCI")
        self.gridlayout2.addWidget(self.spinBoxSrcDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(FRSWPage)
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
        self.gridlayout.addWidget(self.groupBox_2,1,2,3,1)

        self.groupBox_3 = QtGui.QGroupBox(FRSWPage)

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

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,1,0,1,1)

        self.spinBoxDestDLCI = QtGui.QSpinBox(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxDestDLCI.sizePolicy().hasHeightForWidth())
        self.spinBoxDestDLCI.setSizePolicy(sizePolicy)
        self.spinBoxDestDLCI.setMaximum(65535)
        self.spinBoxDestDLCI.setProperty("value",QtCore.QVariant(202))
        self.spinBoxDestDLCI.setObjectName("spinBoxDestDLCI")
        self.gridlayout3.addWidget(self.spinBoxDestDLCI,1,1,1,1)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,2)

        self.pushButtonAdd = QtGui.QPushButton(FRSWPage)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridlayout.addWidget(self.pushButtonAdd,3,0,1,1)

        self.pushButtonDelete = QtGui.QPushButton(FRSWPage)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridlayout.addWidget(self.pushButtonDelete,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,1,1,2)

        self.retranslateUi(FRSWPage)
        QtCore.QMetaObject.connectSlotsByName(FRSWPage)

    def retranslateUi(self, FRSWPage):
        FRSWPage.setWindowTitle(QtGui.QApplication.translate("FRSWPage", "Frame Relay Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("FRSWPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("FRSWPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FRSWPage", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FRSWPage", "Mapping", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(0,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetVCmap.headerItem().setText(1,QtGui.QApplication.translate("FRSWPage", "Port:DLCI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("FRSWPage", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FRSWPage", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FRSWPage", "DLCI:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("FRSWPage", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("FRSWPage", "&Delete", None, QtGui.QApplication.UnicodeUTF8))

