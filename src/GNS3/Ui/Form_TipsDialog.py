# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_TipsDialog.ui'
#
# Created: Fri Jul  5 13:39:29 2013
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
        self.webView = QtWebKit.QWebView(TipsDialog)
        self.webView.setGeometry(QtCore.QRect(12, 12, 400, 400))
        self.webView.setMinimumSize(QtCore.QSize(400, 400))
        self.webView.setMaximumSize(QtCore.QSize(400, 400))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.widget = QtGui.QWidget(TipsDialog)
        self.widget.setGeometry(QtCore.QRect(12, 420, 401, 32))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBoxDontShowAgain = QtGui.QCheckBox(self.widget)
        self.checkBoxDontShowAgain.setText(QtGui.QApplication.translate("TipsDialog", "Don\'t show this again", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDontShowAgain.setObjectName(_fromUtf8("checkBoxDontShowAgain"))
        self.horizontalLayout.addWidget(self.checkBoxDontShowAgain)
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.widget)
        self.label.setText(QtGui.QApplication.translate("TipsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.gns3.net/why-this-ad/\"><span style=\" text-decoration: underline; color:#0000ff;\">Why this ad?</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TipsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TipsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TipsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TipsDialog)

    def retranslateUi(self, TipsDialog):
        pass

from PyQt4 import QtWebKit
