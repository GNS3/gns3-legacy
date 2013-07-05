# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_NodeConfigurator.ui'
#
# Created: Fri Jul  5 13:39:28 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NodeConfigurator(object):
    def setupUi(self, NodeConfigurator):
        NodeConfigurator.setObjectName(_fromUtf8("NodeConfigurator"))
        NodeConfigurator.resize(689, 475)
        NodeConfigurator.setWindowTitle(QtGui.QApplication.translate("NodeConfigurator", "Node configurator", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/logo_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NodeConfigurator.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(NodeConfigurator)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.splitter = QtGui.QSplitter(NodeConfigurator)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeViewNodes = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeViewNodes.sizePolicy().hasHeightForWidth())
        self.treeViewNodes.setSizePolicy(sizePolicy)
        self.treeViewNodes.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeViewNodes.setObjectName(_fromUtf8("treeViewNodes"))
        self.treeViewNodes.headerItem().setText(0, QtGui.QApplication.translate("NodeConfigurator", "Nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QWidget(self.splitter)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.vboxlayout = QtGui.QVBoxLayout(self.verticalLayout)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.titleLabel = QtGui.QLabel(self.verticalLayout)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.titleLabel.setFont(font)
        self.titleLabel.setFrameShape(QtGui.QFrame.Box)
        self.titleLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.titleLabel.setText(QtGui.QApplication.translate("NodeConfigurator", "Node Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.titleLabel.setTextFormat(QtCore.Qt.PlainText)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.vboxlayout.addWidget(self.titleLabel)
        self.configStack = QtGui.QStackedWidget(self.verticalLayout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configStack.sizePolicy().hasHeightForWidth())
        self.configStack.setSizePolicy(sizePolicy)
        self.configStack.setFrameShape(QtGui.QFrame.Box)
        self.configStack.setFrameShadow(QtGui.QFrame.Sunken)
        self.configStack.setObjectName(_fromUtf8("configStack"))
        self.emptyPage = QtGui.QWidget()
        self.emptyPage.setObjectName(_fromUtf8("emptyPage"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.emptyPage)
        self.vboxlayout1.setSpacing(0)
        self.vboxlayout1.setContentsMargins(0, 4, 0, 0)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.textLabel1 = QtGui.QLabel(self.emptyPage)
        self.textLabel1.setText(QtGui.QApplication.translate("NodeConfigurator", "Please select a node in the list \n"
"to display the configuration page.", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.vboxlayout1.addWidget(self.textLabel1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.configStack.addWidget(self.emptyPage)
        self.vboxlayout.addWidget(self.configStack)
        self.gridlayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NodeConfigurator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NodeConfigurator)
        self.configStack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NodeConfigurator)

    def retranslateUi(self, NodeConfigurator):
        pass

import svg_resources_rc
