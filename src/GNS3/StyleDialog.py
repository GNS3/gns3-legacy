# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# http://www.gns3.net/contact
#

from PyQt4 import QtCore, QtGui
from GNS3.Ui.Form_StyleDialog import Ui_StyleDialog
from GNS3.Utils import translate


class StyleDialog(QtGui.QDialog, Ui_StyleDialog):
    """ StyleDialog class
    """

    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.connect(self.pushButton_Color, QtCore.SIGNAL('clicked()'), self.__setColor)
        self.connect(self.pushButton_Font, QtCore.SIGNAL('clicked()'), self.__setFont)
        self.connect(self.pushButton_BorderColor, QtCore.SIGNAL('clicked()'), self.__setBorderColor)

        # default values
        self.color = QtCore.Qt.transparent
        self.borderColor = QtCore.Qt.black
        self.borderWidth = 2
        self.borderStyle = QtCore.Qt.SolidLine
        self.font = QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold)
        self.rotation = 0

        self.comboBox_borderStyle.addItem(translate("StyleDialog", "Solid"), QtCore.QVariant(QtCore.Qt.SolidLine))
        self.comboBox_borderStyle.addItem(translate("StyleDialog", "Dash"), QtCore.QVariant(QtCore.Qt.DashLine))
        self.comboBox_borderStyle.addItem(translate("StyleDialog", "Dot"), QtCore.QVariant(QtCore.Qt.DotLine))
        self.comboBox_borderStyle.addItem(translate("StyleDialog", "Dash Dot"), QtCore.QVariant(QtCore.Qt.DashDotLine))
        self.comboBox_borderStyle.addItem(translate("StyleDialog", "Dash Dot Dot"), QtCore.QVariant(QtCore.Qt.DashDotDotLine))
        self.comboBox_borderStyle.addItem(translate("StyleDialog", "No border"), QtCore.QVariant(QtCore.Qt.NoPen))

    def loadFontValues(self, color, font, rotation):

        self.color = color
        self.font = font
        self.spinBox_Rotation.setValue(rotation)

    def loadShapeItemValues(self, color, borderColor, borderWidth, borderStyle, rotation):

        self.color = color
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderStyle = borderStyle
        index = self.comboBox_borderStyle.findData(QtCore.QVariant(self.borderStyle), QtCore.Qt.UserRole)
        if (index != -1):
            self.comboBox_borderStyle.setCurrentIndex(index)
        self.spinBox_borderWidth.setValue(self.borderWidth)
        self.spinBox_Rotation.setValue(rotation)

    def __setFont(self):

        ok = None
        (selected_font, ok) = QtGui.QFontDialog.getFont(self.font)
        if ok:
            self.font = selected_font

    def __setColor(self):

        self.color = QtGui.QColorDialog.getColor(self.color)

    def __setBorderColor(self):

        self.borderColor = QtGui.QColorDialog.getColor(self.borderColor)

    def on_buttonBox_clicked(self, button):
        """ Private slot called by a button of the button box clicked.
            button: button that was clicked (QAbstractButton)
        """

        if button == self.buttonBox.button(QtGui.QDialogButtonBox.Cancel):
            QtGui.QDialog.reject(self)
        else:
            self.borderWidth = self.spinBox_borderWidth.value()
            self.rotation = self.spinBox_Rotation.value()
            self.borderStyle = QtCore.Qt.PenStyle(self.comboBox_borderStyle.itemData(self.comboBox_borderStyle.currentIndex(), QtCore.Qt.UserRole).toInt()[0])
            QtGui.QDialog.accept(self)
