# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_TipsDialog.ui'
#
# Created: Fri Jun 14 21:09:35 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TipsDialog(object):
    def setupUi(self, TipsDialog):
        TipsDialog.setObjectName(_fromUtf8("TipsDialog"))
        TipsDialog.resize(424, 466)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TipsDialog.sizePolicy().hasHeightForWidth())
        TipsDialog.setSizePolicy(sizePolicy)
        TipsDialog.setWindowTitle(QtGui.QApplication.translate("TipsDialog", "GNS3 Tips", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(TipsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(TipsDialog)
        self.webView.setMinimumSize(QtCore.QSize(400, 400))
        self.webView.setMaximumSize(QtCore.QSize(400, 400))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBoxDontShowAgain = QtGui.QCheckBox(TipsDialog)
        self.checkBoxDontShowAgain.setText(QtGui.QApplication.translate("TipsDialog", "Don\'t show this again", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDontShowAgain.setObjectName(_fromUtf8("checkBoxDontShowAgain"))
        self.horizontalLayout.addWidget(self.checkBoxDontShowAgain)
        self.buttonBox = QtGui.QDialogButtonBox(TipsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TipsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TipsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TipsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TipsDialog)

    def retranslateUi(self, TipsDialog):
        pass

from PyQt4 import QtWebKit
