# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Wed Sep 26 18:58:46 2007
#      by: PyQt4 UI code generator 4-snapshot-20070701
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sun Oct 14 19:23:34 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sun Oct 14 19:33:17 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sun Oct 14 19:33:55 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sun Oct 14 19:43:27 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Thu Nov  1 11:59:21 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Thu Nov  1 14:59:10 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Fri Feb  1 15:12:45 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Fri Feb  1 15:14:58 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Fri Feb  1 15:59:49 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sat Feb  2 11:32:33 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sat Feb  2 11:38:25 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Wed Feb  6 16:51:28 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(QtCore.QSize(QtCore.QRect(0,0,402,308).size()).expandedTo(PreferencesGeneral.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(PreferencesGeneral)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.langsBox = QtGui.QComboBox(PreferencesGeneral)
        self.langsBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.vboxlayout.addWidget(self.langsBox)

        self.groupBox = QtGui.QGroupBox(PreferencesGeneral)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.groupBox)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.vboxlayout1.addWidget(self.checkBoxShowStatusPoints)

        self.checkBoxManualConnections = QtGui.QCheckBox(self.groupBox)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.vboxlayout1.addWidget(self.checkBoxManualConnections)
        self.vboxlayout.addWidget(self.groupBox)

        spacerItem = QtGui.QSpacerItem(312,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(PreferencesGeneral)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "GUI settings", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use the manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))

