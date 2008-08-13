# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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
# Contact: contact@gns3.net
#

from PyQt4 import QtGui, QtCore

class Annotation(QtGui.QGraphicsTextItem):
    """ Text annotation for the topology
    """

    def __init__(self):

        QtGui.QGraphicsTextItem.__init__(self)
        self.setFont(QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold))
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.rotation = 0

    def editText(self):

        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setSelected(True)
        self.setFocus()
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)

    def mouseDoubleClickEvent(self, event):

        self.editText()

    def focusOutEvent(self, event):

        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, False)

        # unselect text
        cursor = self.textCursor()
        if(cursor.hasSelection()):
            cursor.clearSelection()
            self.setTextCursor(cursor)
        return QtGui.QGraphicsTextItem.focusOutEvent(self, event)
