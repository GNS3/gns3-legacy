# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_DragAndDropMultiDevices.ui'
#
# Created: Sun Dec 02 18:13:51 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DragDropMultipleDevices(object):
    def setupUi(self, DragDropMultipleDevices):
        DragDropMultipleDevices.setObjectName(_fromUtf8("DragDropMultipleDevices"))
        DragDropMultipleDevices.resize(382, 127)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DragDropMultipleDevices.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(DragDropMultipleDevices)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(DragDropMultipleDevices)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.nbOfDevices = QtGui.QSpinBox(self.groupBox)
        self.nbOfDevices.setMinimum(1)
        self.nbOfDevices.setMaximum(50)
        self.nbOfDevices.setProperty("value", 2)
        self.nbOfDevices.setObjectName(_fromUtf8("nbOfDevices"))
        self.gridLayout.addWidget(self.nbOfDevices, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 2, 1, 1)
        self.nbOfDevicesLabel = QtGui.QLabel(self.groupBox)
        self.nbOfDevicesLabel.setObjectName(_fromUtf8("nbOfDevicesLabel"))
        self.gridLayout.addWidget(self.nbOfDevicesLabel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.OKButton = QtGui.QPushButton(DragDropMultipleDevices)
        self.OKButton.setObjectName(_fromUtf8("OKButton"))
        self.horizontalLayout.addWidget(self.OKButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DragDropMultipleDevices)
        QtCore.QMetaObject.connectSlotsByName(DragDropMultipleDevices)

    def retranslateUi(self, DragDropMultipleDevices):
        DragDropMultipleDevices.setWindowTitle(QtGui.QApplication.translate("DragDropMultipleDevices", "Add multiple identical devices", None, QtGui.QApplication.UnicodeUTF8))
        DragDropMultipleDevices.setToolTip(QtGui.QApplication.translate("DragDropMultipleDevices", "Select multiple identical devices", None, QtGui.QApplication.UnicodeUTF8))
        DragDropMultipleDevices.setStatusTip(QtGui.QApplication.translate("DragDropMultipleDevices", "Select multiple identical devices", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DragDropMultipleDevices", "Select the number of identical devices you want to add to the topology:", None, QtGui.QApplication.UnicodeUTF8))
        self.nbOfDevicesLabel.setText(QtGui.QApplication.translate("DragDropMultipleDevices", "Number of devices:      ", None, QtGui.QApplication.UnicodeUTF8))
        self.OKButton.setText(QtGui.QApplication.translate("DragDropMultipleDevices", "OK", None, QtGui.QApplication.UnicodeUTF8))

import svg_resources_rc
