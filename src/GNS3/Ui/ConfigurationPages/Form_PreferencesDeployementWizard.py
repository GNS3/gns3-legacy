# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesDeployementWizard.ui'
#
# Created: Mon Sep  9 21:29:24 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PreferencesDeployementWizard(object):
    def setupUi(self, PreferencesDeployementWizard):
        PreferencesDeployementWizard.setObjectName(_fromUtf8("PreferencesDeployementWizard"))
        PreferencesDeployementWizard.resize(539, 581)
        PreferencesDeployementWizard.setWindowTitle(QtGui.QApplication.translate("PreferencesDeployementWizard", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_5 = QtGui.QGridLayout(PreferencesDeployementWizard)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tabWidget = QtGui.QTabWidget(PreferencesDeployementWizard)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesDeployementWizard", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "Output directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.ProjectPath = QtGui.QLineEdit(self.groupBox_2)
        self.ProjectPath.setText(_fromUtf8(""))
        self.ProjectPath.setObjectName(_fromUtf8("ProjectPath"))
        self.gridLayout_4.addWidget(self.ProjectPath, 2, 0, 1, 1)
        self.ProjectPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.ProjectPath_browser.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.ProjectPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ProjectPath_browser.setObjectName(_fromUtf8("ProjectPath_browser"))
        self.gridLayout_4.addWidget(self.ProjectPath_browser, 2, 1, 1, 1)
        self.ProjectName = QtGui.QLineEdit(self.groupBox_2)
        self.ProjectName.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "Topology.pdf", None, QtGui.QApplication.UnicodeUTF8))
        self.ProjectName.setObjectName(_fromUtf8("ProjectName"))
        self.gridLayout_4.addWidget(self.ProjectName, 4, 0, 1, 1)
        self.checkBoxRelativePaths = QtGui.QCheckBox(self.groupBox_2)
        self.checkBoxRelativePaths.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "Use relative path for the PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxRelativePaths.setChecked(True)
        self.checkBoxRelativePaths.setObjectName(_fromUtf8("checkBoxRelativePaths"))
        self.gridLayout_4.addWidget(self.checkBoxRelativePaths, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "Project Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.pushButtonTestDeployementWizard = QtGui.QPushButton(self.tab)
        self.pushButtonTestDeployementWizard.setText(QtGui.QApplication.translate("PreferencesDeployementWizard", "&Test Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTestDeployementWizard.setObjectName(_fromUtf8("pushButtonTestDeployementWizard"))
        self.hboxlayout.addWidget(self.pushButtonTestDeployementWizard)
        self.labelDeployementWizardStatus = QtGui.QLabel(self.tab)
        self.labelDeployementWizardStatus.setText(_fromUtf8(""))
        self.labelDeployementWizardStatus.setObjectName(_fromUtf8("labelDeployementWizardStatus"))
        self.hboxlayout.addWidget(self.labelDeployementWizardStatus)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridLayout_3.addLayout(self.hboxlayout, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(PreferencesDeployementWizard)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDeployementWizard)

    def retranslateUi(self, PreferencesDeployementWizard):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PreferencesDeployementWizard", "Export Settings", None, QtGui.QApplication.UnicodeUTF8))

