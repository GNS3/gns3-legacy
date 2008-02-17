# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Wed Sep 26 18:58:45 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Oct 14 19:23:34 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Oct 14 19:33:17 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Oct 14 19:33:54 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Oct 14 19:43:27 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Thu Nov  1 11:59:21 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Thu Nov  1 14:59:10 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Fri Feb  1 15:12:45 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Fri Feb  1 15:14:58 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Fri Feb  1 15:59:49 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sat Feb  2 11:32:33 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sat Feb  2 11:38:25 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HubPage(object):
    def setupUi(self, HubPage):
        HubPage.setObjectName("HubPage")
        HubPage.resize(QtCore.QSize(QtCore.QRect(0,0,397,397).size()).expandedTo(HubPage.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(HubPage)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_4 = QtGui.QGroupBox(HubPage)
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
        self.gridlayout.addWidget(self.groupBox_4,0,0,1,1)

        self.groupBox = QtGui.QGroupBox(HubPage)

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
        self.gridlayout2.addWidget(self.spinBoxNbPorts,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.retranslateUi(HubPage)
        QtCore.QMetaObject.connectSlotsByName(HubPage)

    def retranslateUi(self, HubPage):
        HubPage.setWindowTitle(QtGui.QApplication.translate("HubPage", "Ethernet Hub", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("HubPage", "Hypervisor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIntegratedHypervisor.setText(QtGui.QApplication.translate("HubPage", "Use the hypervisor manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("HubPage", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HubPage", "Ports:", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Wed Feb  6 16:51:28 2008
#      by: PyQt4 UI code generator 4.3
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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Tue Feb 12 23:29:28 2008
#      by: PyQt4 UI code generator 4.3
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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Feb 17 15:25:00 2008
#      by: PyQt4 UI code generator 4.3
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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Feb 17 17:00:51 2008
#      by: PyQt4 UI code generator 4.3
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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_HubPage.ui'
#
# Created: Sun Feb 17 17:01:53 2008
#      by: PyQt4 UI code generator 4.3
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

