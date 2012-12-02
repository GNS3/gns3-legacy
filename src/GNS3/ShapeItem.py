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

from PyQt4 import QtGui, QtCore
import GNS3.Globals as globals


class AbstractShapeItem(object):
    """ Abstract class to draw shapes on the scene
    """

    def __init__(self):

        self.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable | QtGui.QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents(True)
        self.border = 5
        self.rotation = 0
        #self.setZValue(-2)

    def keyPressEvent(self, event):

        key = event.key()
        modifiers = event.modifiers()
        if (key in (QtCore.Qt.Key_P, QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal) and modifiers & QtCore.Qt.AltModifier) \
            or (key == QtCore.Qt.Key_Plus and modifiers & QtCore.Qt.AltModifier and modifiers & QtCore.Qt.KeypadModifier) \
            and self.rotation > -360:
            if self.rotation:
                self.rotate(-self.rotation)
            self.rotation -= 1
            self.rotate(self.rotation)
        elif (key in (QtCore.Qt.Key_M, QtCore.Qt.Key_Minus) and modifiers & QtCore.Qt.AltModifier) \
            or (key == QtCore.Qt.Key_Minus and modifiers & QtCore.Qt.AltModifier and modifiers & QtCore.Qt.KeypadModifier) \
            and self.rotation < 360:
            if self.rotation:
                self.rotate(-self.rotation)
            self.rotation += 1
            self.rotate(self.rotation)
        else:
            QtGui.QGraphicsItem.keyPressEvent(self, event)

    def mousePressEvent(self, event):

        self.update()
        if event.pos().x() > (self.rect().right() - self.border):
            self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            self.edge = 'right'

        elif event.pos().x() < (self.rect().left() + self.border):
            self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            self.edge = 'left'

        elif event.pos().y() < (self.rect().top() + self.border):
            self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            self.edge = 'top'

        elif event.pos().y() > (self.rect().bottom() - self.border):
            self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            self.edge = 'bottom'

        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.update()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.edge = None
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):

        self.update()
        if hasattr(self, 'edge') and self.edge:
            r = self.rect()
            scenePos = event.scenePos()

            if self.edge == 'top':
                diff = self.y() - scenePos.y()
                if r.height() - diff > 0:
                    self.setPos(self.x(), scenePos.y())
                    self.setRect(0, 0, self.rect().width(), self.rect().height() + diff)
                else:
                    self.edge = 'bottom'
                    self.setPos(self.x(), self.y() + self.rect().height())
                    self.setRect(0, 0, self.rect().width(), diff - self.rect().height())

            elif self.edge == 'left':
                diff = self.x() - scenePos.x()
                if r.width() - diff > 0:
                    self.setPos(scenePos.x(), self.y())
                    self.setRect(0, 0, r.width() + diff, self.rect().height())
                else:
                    self.edge = "right"
                    self.setPos(self.x() + self.rect().width(), self.y())
                    self.setRect(0, 0, diff - self.rect().width(), self.rect().height())

            elif self.edge == 'bottom':
                if r.height() > 0:
                    pos = self.mapFromScene(scenePos)
                    self.setRect(0, 0, self.rect().width(), pos.y())
                else:
                    self.setRect(0, 0, self.rect().width(), abs(scenePos.y() - self.y()))
                    self.setPos(self.x(), scenePos.y())
                    self.edge = 'top'
            elif self.edge == 'right':
                if r.width() > 0:
                    pos = self.mapFromScene(scenePos)
                    self.setRect(0, 0, pos.x(), self.rect().height())
                else:
                    self.setRect(0, 0, abs(scenePos.x() - self.x()), self.rect().height())
                    self.setPos(scenePos.x(), self.y())
                    self.edge = 'left'

        QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def hoverMoveEvent(self, event):

        # objects on the background layer don't need cursors
        if self.zValue() >= 0:
            if event.pos().x() > (self.rect().right() - self.border):
                globals.GApp.scene.setCursor(QtCore.Qt.SizeHorCursor)
            elif event.pos().x() < (self.rect().left() + self.border):
                globals.GApp.scene.setCursor(QtCore.Qt.SizeHorCursor)
            elif event.pos().y() < (self.rect().top() + self.border):
                globals.GApp.scene.setCursor(QtCore.Qt.SizeVerCursor)
            elif event.pos().y() > (self.rect().bottom() - self.border):
                globals.GApp.scene.setCursor(QtCore.Qt.SizeVerCursor)
            else:
                globals.GApp.scene.setCursor(QtCore.Qt.SizeAllCursor)

    def hoverLeaveEvent(self, event):

        # objects on the background layer doesn't need cursors
        if self.zValue() >= 0:
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)

    def drawLayerInfo(self, painter):

        # Don't draw if not activated
        if globals.GApp.workspace.flg_showLayerPos == False:
            return

        # Show layer level of this node
        brect = self.boundingRect()

        # Don't draw if the object is too small ...
        if brect.width() < 20 or brect.height() < 20:
            return

        center = self.mapFromItem(self, brect.width() / 2.0, brect.height() / 2.0)

        painter.setBrush(QtCore.Qt.red)
        painter.setPen(QtCore.Qt.red)
        painter.drawRect((brect.width() / 2.0) - 10, (brect.height() / 2.0) - 10, 20, 20)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("TypeWriter", 14, QtGui.QFont.Bold))
        zval = str(int(self.zValue()))
        painter.drawText(QtCore.QPointF(center.x() - 4, center.y() + 4), zval)


class Rectangle(AbstractShapeItem, QtGui.QGraphicsRectItem):
    """ Class to draw a rectangle on the scene
    """

    def __init__(self, pos, size):

        QtGui.QGraphicsRectItem.__init__(self, 0, 0, size.width(), size.height())
        AbstractShapeItem.__init__(self)
        self.setPos(pos)
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.setPen(pen)

    def paint(self, painter, option, widget=None):

        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)
        self.drawLayerInfo(painter)


class Ellipse(AbstractShapeItem, QtGui.QGraphicsEllipseItem):
    """ Class to draw an ellipse on the scene
    """

    def __init__(self, pos, size):

        QtGui.QGraphicsEllipseItem.__init__(self, 0, 0, size.width(), size.height())
        AbstractShapeItem.__init__(self)
        self.setPos(pos)
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        self.setPen(pen)

    def paint(self, painter, option, widget=None):

        QtGui.QGraphicsEllipseItem.paint(self, painter, option, widget)
        self.drawLayerInfo(painter)
