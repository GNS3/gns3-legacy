# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_NodeConfigurator.ui'
#
# Created: Mon Jul 16 13:33:16 2007
#      by: PyQt4 UI code generator 4-snapshot-20070710
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NodeConfigurator(object):
    def setupUi(self, NodeConfigurator):
        NodeConfigurator.setObjectName("NodeConfigurator")
        NodeConfigurator.resize(QtCore.QSize(QtCore.QRect(0,0,665,492).size()).expandedTo(NodeConfigurator.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(NodeConfigurator)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(NodeConfigurator)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.treeViewNodes = QtGui.QTreeWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeViewNodes.sizePolicy().hasHeightForWidth())
        self.treeViewNodes.setSizePolicy(sizePolicy)
        self.treeViewNodes.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeViewNodes.setObjectName("treeViewNodes")

        self.configStack = QtGui.QStackedWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configStack.sizePolicy().hasHeightForWidth())
        self.configStack.setSizePolicy(sizePolicy)
        self.configStack.setFrameShape(QtGui.QFrame.Box)
        self.configStack.setFrameShadow(QtGui.QFrame.Sunken)
        self.configStack.setObjectName("configStack")

        self.emptyPage = QtGui.QWidget()
        self.emptyPage.setObjectName("emptyPage")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.emptyPage)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        spacerItem = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)

        self.emptyPagePixmap = QtGui.QLabel(self.emptyPage)
        self.emptyPagePixmap.setAlignment(QtCore.Qt.AlignCenter)
        self.emptyPagePixmap.setObjectName("emptyPagePixmap")
        self.vboxlayout1.addWidget(self.emptyPagePixmap)

        self.textLabel1 = QtGui.QLabel(self.emptyPage)
        self.textLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1.setObjectName("textLabel1")
        self.vboxlayout1.addWidget(self.textLabel1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.configStack.addWidget(self.emptyPage)
        self.vboxlayout.addWidget(self.splitter)

        self.buttonBox = QtGui.QDialogButtonBox(NodeConfigurator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NodeConfigurator)
        self.configStack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NodeConfigurator)

    def retranslateUi(self, NodeConfigurator):
        NodeConfigurator.setWindowTitle(QtGui.QApplication.translate("NodeConfigurator", "Node configurator", None, QtGui.QApplication.UnicodeUTF8))
        self.treeViewNodes.headerItem().setText(0,QtGui.QApplication.translate("NodeConfigurator", "Nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("NodeConfigurator", "Please select a node in the list \n"
        "to display the configuration page.", None, QtGui.QApplication.UnicodeUTF8))

