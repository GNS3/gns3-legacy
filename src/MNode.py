#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 GNS-3 Dev Team
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
# Contact: developers@gns3.net
#

import sys, time
from PyQt4 import QtCore, QtGui, QtSvg
from Config import ConfDB
from Ethernet import *
from Serial import *
from Utils import translate
import Dynamips_lib as lib
import subprocess as sub
import __main__

class MNode(QtSvg.QGraphicsSvgItem):
    """ MNode class
        Node item for the scene
    """

    # get access to globals
    main = __main__
    mNodeName = None
    svg = None
    _QGraphicsScene = None
    _MNodeSelected = None

    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        """ svgfile: string
            QGraphicsScene: QtGui.QGraphicsScene instance
            xPos: integer
            yPos: integer
        """

        svg = QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        self.edgeList = []
        self.iosConfig = {}
        self.interfaces = {}
        self.tmpif = None
        self.abort = True
        self.neighborList = []
        self.ios = None
        self.active_timer = False

        # create an ID
        self.id = self.main.baseid
        self.main.baseid += 1

        # MNode settings
        #self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setFlag(self.ItemIsFocusable)
        self.setZValue(1)

        # Init action applicable to the node
        self.__initActions()

        # by default put the node to (0,0)
        if xPos is None : xPos = 0
        if yPos is None : yPos = 0
        self.setPos(xPos, yPos)

        # MNode placement
        self._QGraphicsScene = QGraphicsScene
        self._QGraphicsScene.addItem(self)
        self._QGraphicsScene.update(self.sceneBoundingRect())

        # Flags
        self.flg_hostname = False

        if self.main.flg_showhostname == True:
            self.showHostname()

    def __initActions(self):
        """ Initialize all menu actions who belongs to MNode
        """

        # Action: Configure (Configure the node)
        self.configAct = QtGui.QAction(translate('MNode', 'Configure'), self)
        self.configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
        #self.configAct.setText('Configure Node')
        #self.configAct.setStatusTip('Configure the node')
        self.connect(self.configAct, QtCore.SIGNAL('activated()'), self.__configAction)

        # Action: Delete (Delete the node)
        self.deleteAct = QtGui.QAction(translate('MNode', 'Delete'), self)
        self.deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        #self.deleteAct.setText('Delete Node')
        #self.deleteAct.setStatusTip('Delete the node')
        self.connect(self.deleteAct, QtCore.SIGNAL('activated()'), self.__deleteAction)

        # Action: Console (Connect to the node console (IOS))
        self.consoleAct = QtGui.QAction(translate('MNode', 'Console'), self)
        self.consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
        #self.consoleAct.setText('Open Console')
        #self.consoleAct.setStatusTip('Connect to the node console (IOS)')
        self.connect(self.consoleAct, QtCore.SIGNAL('activated()'), self.__consoleAction)

        # Action: Start (Start IOS on hypervisor)
        self.startAct = QtGui.QAction(translate('MNode', 'Start'), self)
        self.startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
        #self.startAct.setText('Start IOS')
        #self.startAct.setStatusTip('Start IOS on hypervisor')
        self.connect(self.startAct, QtCore.SIGNAL('activated()'), self.__startAction)

        # Action: Stop (Stop IOS on hypervisor)
        self.stopAct = QtGui.QAction(translate('MNode', 'Stop'), self)
        self.stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
        #self.stopAct.setText('Stop IOS')
        #self.stopAct.setStatusTip('Stop IOS on hypervisor')
        self.connect(self.stopAct, QtCore.SIGNAL('activated()'), self.__stopAction)

    def __configAction(self):
        """ Action called for node configuration
        """

        self.InspectorInstance.loadNodeInfos()
        self.InspectorInstance.show()

    def __deleteAction(self):
        """ Action called for node deletion
        """

        self.delete()

    def __consoleAction(self):
        """ Action called to start a node console
        """

        self.telnetToIOS()


    def __startAction(self):
        """ Action called to start the IOS hypervisor on the node
        """

        try:
            self.startIOS()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))

    def __stopAction(self):
        """ Action called to stop IOS hypervisor on the node
        """

        try:
            self.stopIOS()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self.main.win, 'Dynamips error',  str(msg))


    def move(self, xPos, yPos):
        """ Set the node position on the scene
            xPos: integer
            yPos: integer
        """

        self.setPos(xPos, yPos)

    def addEdge(self, edge):
        """ Save the edge
            edge: Edge instance
        """

        if edge.dest.id != self.id:
            self.neighborList.append(edge.dest.id)
        else:
            self.neighborList.append(edge.source.id)
        self.edgeList.append(edge)
        edge.adjust()

    def deleteEdge(self, edge):
        """ Delete the edge
            edge: Edge instance
        """

        if edge.dest.id != self.id:
            neighborid = edge.dest.id
        else:
            neighborid = edge.source.id
        self.neighborList.remove(neighborid)
        self.edgeList.remove(edge)

        tmp = self.interfaces
        delete_list = []
        for interface in tmp:
            if tmp[interface][0] == neighborid:
                delete_list.append(interface)
        for interface in delete_list:
            del self.interfaces[interface]

    def ajustAllEdges(self):
        """ Refresh edges drawing
        """

        for edge in self.edgeList:
            edge.adjust()

    def hasEdgeToNode(self, node_id):
        """ Tell if we are connected to node_id
            node_id: integer
        """

        for edge in self.edgeList:
            if edge.dest.id == node_id or edge.source.id == node_id:
                return True
        return False

    def itemChange(self, change, value):
        """ Notify custom items that some part of the item's state changes
            change: enum QtGui.QGraphicsItem.GraphicsItemChange
            value: QtCore.QVariant instance
        """

        if change == self.ItemPositionHasChanged or change == self.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()

        if self.active_timer == False:
            self.active_timer = True
            QtCore.QTimer.singleShot(500, self.refresh)

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def refresh(self):

        for edge in self.edgeList:
                edge.adjust()
        self.active_timer = False

    def menuInterface(self):
        """ Show a contextual menu to choose an interface
        """

        menu = QtGui.QMenu()
        interfaces_list = self.getInterfaces()
        for interface in interfaces_list:
            if self.interfaces.has_key(interface):
                # already connected interface
                menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), interface)
            else:
                # disconnected interface
                menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), interface)

        # connect the menu
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.selectedInterface)
        menu.exec_(QtGui.QCursor.pos())

    def keyReleaseEvent(self, event):
        """ key release handler for MNodes
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.delete()
        else:
            QtGui.QGraphicsItem.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton) and self.main.design_mode == False:
            self.menu = QtGui.QMenu()
            self.menu.addAction(self.consoleAct)
            self.menu.addAction(self.startAct)
            self.menu.addAction(self.stopAct)
            self.menu.exec_(QtGui.QCursor.pos())
            return

        if (event.button() == QtCore.Qt.RightButton) and self.main.design_mode == True:
            self.menu = QtGui.QMenu()
            self.menu.addAction(self.configAct)
            self.menu.addAction(self.deleteAct)
            self.menu.exec_(QtGui.QCursor.pos())
            return

        if self.main.linkEnabled == False :
           QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
           return

        if len(self.getInterfaces()) == 0:
            QtGui.QMessageBox.critical(self.main.win, 'Connection',  'No interface available')
            return

        if (self._MNodeSelected == True):
            # MNode is selected
            self._MNodeSelected = False
            self.resetList()
            QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
            return

        if self.main.countClick == 0:
            # source node is clicked
            self.menuInterface()
            if self.abort == False and self.tmpif:
                self.main.countClick = 1
                self.main.TabLinkMNode.append(self)
                self._MNodeSelected = True
                self._QGraphicsScene.update()

        elif (self.main.countClick == 1 and cmp(self.main.TabLinkMNode[0], self)):
            # destination node is clicked
           self.menuInterface()
           self._MNodeSelected = True
           self._QGraphicsScene.update()
           if self.abort == False:
               self.main.TabLinkMNode.append(self)
               self._addLinkToScene(self.main.TabLinkMNode[0], self.main.TabLinkMNode[1])
           self.resetList()
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)

    def _addLinkToScene(self, node_src, node_dst):

        if node_src.tmpif[0] == "s" and node_dst.tmpif[0] == "s":
            link = Serial(node_src, node_dst, self._QGraphicsScene)
        else:
            link = Ethernet(node_src, node_dst, self._QGraphicsScene)
        self._QGraphicsScene.update(link.boundingRect())

    def resetList(self):
        """ Reset
        """

        i = 0
        while (i < len(self.main.TabLinkMNode)):
           self.main.TabLinkMNode[i].setMNodeSelected(False)
           i = i + 1
        self.main.countClick = 0
        self.main.TabLinkMNode= []

    def selectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        if not interface:
            return
        self.abort = True
        if (self.main.countClick == 0):
            # source node
            self.tmpif = interface
            # check if already connected
            if self.interfaces.has_key(interface):
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                self.abort = True
                return
            self.abort = False

        elif (self.main.countClick == 1 and cmp(self.main.TabLinkMNode[0], self)):
            # destination node
            if self.interfaces.has_key(interface):
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Already connected interface')
                self.abort = True
                return
            self.tmpif = interface
            srcif = self.main.TabLinkMNode[0].tmpif
            srcid = self.main.TabLinkMNode[0].id
            assert(srcif != None)
            if srcif[0] != interface[0]:
                QtGui.QMessageBox.critical(self.main.win, 'Connection',  'Interfaces types mismatch !')
                self.abort = True
                return
            self.interfaces[interface] = [srcid, srcif]
            self.main.TabLinkMNode[0].interfaces[srcif] = [self.id, interface]
            self.abort = False

    def deleteInterface(self, ifname):
        """ Delete an interface and the link that is connected to it (if present)
            ifname: string
        """

        destid = self.interfaces[ifname][0]
        destif = self.interfaces[ifname][1]
        delete_list = []

        for edge in self.edgeList:
            if edge.dest.id != self.id:
                neighborid = edge.dest.id
            else:
                neighborid = edge.source.id
            if neighborid == destid:
                delete_list.append(edge)
        for edge in delete_list:
            edge.delete()

    def cleanInterfaceStatus(self):
        """ Clean the interface status points
        """

        for edge in self.edgeList:
            edge.setStatus(self.id, False)

    def delete(self):
        """ Delete the current node
        """

        delete_list = []
        for edge in self.edgeList:
            self._QGraphicsScene.removeItem(edge)
            delete_list.append(edge)
        for edge in delete_list:
            if edge.dest.id != self.id:
                neighborid = edge.dest.id
            else:
                neighborid = edge.source.id
            self.main.nodes[neighborid].deleteEdge(edge)
            self.deleteEdge(edge)
        del self.main.nodes[self.id]
        self._QGraphicsScene.removeItem(self)

    def showHostname(self):
        """ Show the hostname on the scene
        """

        if self.flg_hostname == True:
            # don't try to show hostname twice
            return

        self.textItem = QtGui.QGraphicsTextItem("R " + str(self.id), self)
        self.textItem.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.textItem.setFlag(self.textItem.ItemIsMovable)
        self.textItem.setZValue(2)
        self.textItem.setPos(20, -20)
        self._QGraphicsScene.addItem(self.textItem)
        self.flg_hostname = True

    def telnetToIOS(self):
        """ Start a telnet console and connect it to an IOS
        """

        hypervisor_host = self.main.ios_images[self.iosConfig['iosimage']]['hypervisor_host']
        if self.ios.console != None:
            try:
                console = ConfDB().get("Dynamips/console", '')
                if console:
                    console = console.replace('%h', hypervisor_host)
                    console = console.replace('%p', str(self.ios.console))
                    console = console.replace('%d', self.ios.name)
                    sub.Popen(console, shell=True)
                else:
                    if sys.platform.startswith('darwin'):
                        sub.Popen("/usr/bin/osascript -e 'tell application \"Terminal\" to do script with command \"telnet " + hypervisor_host + " " + str(self.ios.console) +"; exit\"' -e 'tell application \"Terminal\" to tell window 1  to set custom title to \"" + self.ios.name + "\"'", shell=True)
                    elif sys.platform.startswith('win32'):
                        sub.Popen("telnet " +  hypervisor_host + " " + str(self.ios.console), shell=True)
                    else:
                        sub.Popen("xterm -T " + self.ios.name + " -e telnet '" + hypervisor_host + " " + str(self.ios.console) + "' > /dev/null 2>&1 &", shell=True)
            except OSError, (errno, strerror):
                QtGui.QMessageBox.critical(self.main.win, 'Console error', strerror)
                return (False)
            return (True)

    def removeHostname(self):
        """ Remove the hostname on the scene
        """

        if self.flg_hostname == True:
            self._QGraphicsScene.removeItem(self.textItem)
            self.flg_hostname = False

    def setName(self, name):

        self.mNodeName = name

    def getName(self):

        return self.mNodeName

    def setMNodeSelected(self, b):

         self._MNodeSelected = b

    def getMNodeSelected(self):

        return self._MNodeSelected

    def paint(self, painter, option, widget):
        """ Draw a rectangle around the node
        """

        if self._MNodeSelected == True:
            rect = self.boundingRect()
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

            #                  1st line
            #        (x,y) ----------------- (x + w, y)
            #             |                |
            #  4th Line   |                | 2nd Line
            #             |                |
            #             |                |
            #    (x,y + h)|________________|(x + w, y + h)
            #                   3rd Line

            # first line
            painter.drawLine(x, y, x + w, y)
            # Second line
            painter.drawLine(x + w, y, x + w, y + h)
            # Third line
            painter.drawLine(x + w, y + h, x, y + h)
            # fourth line
            painter.drawLine(x, y + h, x, y)
        QtSvg.QGraphicsSvgItem.paint(self,painter, option, widget)

