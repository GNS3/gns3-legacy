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

import re
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Topology import Topology
from GNS3.Utils import translate
from Annotation import Annotation
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.FW import FW
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.Hub import Hub
from GNS3.Link.AbstractEdge import AbstractEdge
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial

class Scene(QtGui.QGraphicsView):
    """ Scene class
    """

    def __init__(self, parent = None):

        QtGui.QGraphicsView.__init__(self, parent)

        # Create topology and register it on GApp
        self.__topology = Topology()
        self.setScene(self.__topology)
        globals.GApp.topology = self.__topology

        # Set custom flags for the view
        self.setDragMode(self.RubberBandDrag)
        self.setCacheMode(self.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorViewCenter)

        self.newedge = None
        self.resetAddingLink()

        # Load all renders
        self.renders = {}
        for item in SYMBOLS:
            name = item['name']
            self.renders[name] = {}
            self.renders[name]['normal'] = QtSvg.QSvgRenderer(item['normal_svg_file'])
            self.renders[name]['selected'] = QtSvg.QSvgRenderer(item['select_svg_file'])

    def resetAddingLink(self):
        """ Reset when drawing a link
        """

        self.__isFirstClick = True
        self.__sourceNodeID = None
        self.__destNodeID = None
        self.__sourceInterface = None
        self.__destInterface = None
        if self.newedge:
            self.__topology.removeItem(self.newedge)
            self.newedge = None

    def showContextualMenu(self):
        """  Create and display a contextual menu when clicking on the view
        """

        items = self.__topology.selectedItems()
        if len(items) == 0:
            return

        menu = QtGui.QMenu()

        instances = map(lambda item: not isinstance(item, Annotation), items)
        if True in instances:

            # Action: Configure (Configure the node)
            configAct = QtGui.QAction(translate('Scene', 'Configure'), menu)
            configAct.setIcon(QtGui.QIcon(":/icons/configuration.svg"))
            self.connect(configAct, QtCore.SIGNAL('triggered()'), self.slotConfigNode)

            # Action: ChangeHostname (Change the hostname)
            changeHostnameAct = QtGui.QAction(translate('Scene', 'Change the hostname'), menu)
            changeHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
            self.connect(changeHostnameAct, QtCore.SIGNAL('triggered()'), self.slotChangeHostname)

            # Action: ShowHostname (Display the hostname)
            showHostnameAct = QtGui.QAction(translate('Scene', 'Show/Hide the hostname'), menu)
            showHostnameAct.setIcon(QtGui.QIcon(":/icons/show-hostname.svg"))
            self.connect(showHostnameAct, QtCore.SIGNAL('triggered()'), self.slotShowHostname)

            # actions for design mode
            menu.addAction(configAct)
            menu.addAction(showHostnameAct)
            menu.addAction(changeHostnameAct)

        instances = map(lambda item: isinstance(item, IOSRouter) or isinstance(item, FW), items)
        if True in instances:

            # Action: Console (Connect to the node console)
            consoleAct = QtGui.QAction(translate('Scene', 'Console'), menu)
            consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
            self.connect(consoleAct, QtCore.SIGNAL('triggered()'), self.slotConsole)

            # Action: Start (Start IOS on hypervisor)
            startAct = QtGui.QAction(translate('Scene', 'Start'), menu)
            startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
            self.connect(startAct, QtCore.SIGNAL('triggered()'), self.slotStartNode)

            # Action: Stop (Stop IOS on hypervisor)
            stopAct = QtGui.QAction(translate('Scene', 'Stop'), menu)
            stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
            self.connect(stopAct, QtCore.SIGNAL('triggered()'), self.slotStopNode)

            menu.addAction(consoleAct)
            menu.addAction(startAct)
            menu.addAction(stopAct)

        instances = map(lambda item: isinstance(item, IOSRouter), items)
        if True in instances:

            # Action: Calculate IDLE PC
            idlepcAct = QtGui.QAction(translate('Scene', 'Idle PC'), menu)
            idlepcAct.setIcon(QtGui.QIcon(':/icons/calculate.svg'))
            self.connect(idlepcAct, QtCore.SIGNAL('triggered()'), self.slotIdlepc)

            # Action: Suspend (Suspend IOS on hypervisor)
            suspendAct = QtGui.QAction(translate('Scene', 'Suspend'), menu)
            suspendAct.setIcon(QtGui.QIcon(':/icons/pause.svg'))
            self.connect(suspendAct, QtCore.SIGNAL('triggered()'), self.slotSuspendNode)

            menu.addAction(suspendAct)
            menu.addAction(idlepcAct)

        # Action: Delete (Delete the node)
        deleteAct = QtGui.QAction(translate('Scene', 'Delete'), menu)
        deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(deleteAct, QtCore.SIGNAL('triggered()'), self.slotDeleteNode)
        menu.addAction(deleteAct)

        menu.exec_(QtGui.QCursor.pos())

        # force the deletion of the children
        for child in menu.children():
            child.deleteLater()

    def addItem(self, node):
        """ Overloaded function that add the node into the topology
        """

        self.__topology.addNode(node)

    def calculateIDLEPC(self, router):
        """ Show a splash screen
        """

        splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
        splash.show()
        splash.showMessage(translate("Scene", "Please wait while calculating an IDLE PC"))
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        result = globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPGET)
        return result

    def slotIdlepc(self):
        """ Compute an IDLE PC
        """

        items = self.__topology.selectedItems()
        if len(items) != 1:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "IDLE PC"),  translate("Scene", "Please select only one router"))
            return
        router = items[0]
        assert(isinstance(router, IOSRouter))

        try:
            if globals.GApp.dynagen.devices[router.hostname].idlepc != None:
                reply = QtGui.QMessageBox.question(globals.GApp.mainWindow,translate("Scene", "IDLE PC"),
                                                   unicode(translate("Scene", "%s already has an idlepc value applied, do you want to calculate a new one?")) % router.hostname,
                                                   QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    # reset idlepc
                    lib.send(globals.GApp.dynagen.devices[router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (router.hostname, '0x0'))
                    result = self.calculateIDLEPC(router)
                else:
                    result = globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPSHOW)
            else:
                result = self.calculateIDLEPC(router)

            # remove the '100-OK' line
            result.pop()

            idles = {}
            options = []
            i = 1
            for line in result:
                (value, count) = line.split()[1:]

                # Flag potentially "best" idlepc values (between 50 and 60)
                iCount = int(count[1:-1])
                if 50 < iCount < 60:
                    flag = '*'
                else:
                    flag = ' '

                option = "%s %i: %s %s" % (flag, i, value, count)
                options.append(option)
                idles[i] = value
                i += 1

            if len(idles) == 0:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "IDLE PC"),  translate("Scene", "No idlepc values found"))
                return
            (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Scene", "IDLE PC"),
                                                        translate("Scene", "Potentially better idlepc values marked with '*'"), options, 0, False)
            if ok:
                index = int(selection[2:].split(':')[0])
                globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPSET, idles[index])
                QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("Scene", "IDLE PC"),
                                              unicode(translate("Scene", "Applied idlepc value %s to %s")) % (idles[index], router.hostname))
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, IOSRouter) and node.hostname == router.hostname:
                        dyn_router = node.get_dynagen_device()
                        if globals.GApp.iosimages.has_key(dyn_router.dynamips.host + ':' + dyn_router.image):
                            image = globals.GApp.iosimages[dyn_router.dynamips.host + ':' + dyn_router.image]
                            image.idlepc =  idles[index]
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Scene", "Dynamips error"),  str(msg))
            return

    def slotConfigNode(self):
        """ Called to configure nodes
        """

        items = self.__topology.selectedItems()
        configurator = NodeConfigurator(items)
        configurator.setModal(True)
        configurator.show()
        configurator.exec_()
        for item in items:
            item.setSelected(False)

    def slotChangeHostname(self):
        """ Slot called to change hostnames of selected items
        """

        for item in self.__topology.selectedItems():
            item.changeHostname()

    def slotShowHostname(self):
        """ Slot called to show hostnames of selected items
        """

        for item in self.__topology.selectedItems():
            if not item.hostnameDiplayed():
                item.showHostname()
            else:
                item.removeHostname()

    def slotDeleteNode(self):
        """ Called to delete nodes
        """

        ok_to_delete_node = True
        for item in self.__topology.selectedItems():
            if not isinstance(item, Annotation):
                for link in item.getEdgeList().copy():
                    if self.__topology.deleteLink(link) == False:
                        if ok_to_delete_node:
                            ok_to_delete_node = False
                        continue
                if ok_to_delete_node:
                    self.__topology.deleteNode(item.id)
            else:
                self.__topology.removeItem(item)

    def slotConsole(self):
        """ Slot called to launch a console on the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, FW):
                item.console()

    def slotStartNode(self):
        """ Slot called to start the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, FW):
                item.startNode()

    def slotStopNode(self):
        """ Slot called to stop the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, FW):
                item.stopNode()

    def slotSuspendNode(self):
        """ Slot called to suspend the selected items
        """

        for item in self.__topology.selectedItems():
            if  isinstance(item, IOSRouter):
                item.suspendNode()

    def __addLink(self):
        """ Add a new link between two nodes
        """

        if self.__sourceNodeID == self.__destNodeID:
            self.__isFirstClick = True
            return

        srcnode = globals.GApp.topology.getNode(self.__sourceNodeID)
        destnode = globals.GApp.topology.getNode(self.__destNodeID)

        if srcnode == None or destnode == None:
            self.__isFirstClick = True
            return

        # add the link into the topology
        if self.__topology.addLink(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface) == False:
            self.__isFirstClick = True

    def slotAddLink(self, id, interface):
        """ Called when a node wants to add a link
            id: integer
            interface: string
        """

        if id == None and interface == None:
            self.__isFirstClick = True
            return

        if globals.addingLinkFlag:
            # user is adding a link
            if self.__isFirstClick:
                # source node
                self.__sourceNodeID = id
                self.__sourceInterface = interface
                self.__isFirstClick = False
                if interface[0] == 's' or interface[0] == 'a':
                    # interface is serial or ATM
                    self.newedge = Serial(self.__topology.getNode(id), interface, self.mapToScene(QtGui.QCursor.pos()), 0, Fake = True)
                else:
                    # by default use an ethernet link
                    self.newedge = Ethernet(self.__topology.getNode(id), interface, self.mapToScene(QtGui.QCursor.pos()), 0, Fake = True)
                self.__topology.addItem(self.newedge)
            else:
                # destination node
                self.__destNodeID = id
                self.__destInterface = interface
                self.__topology.removeItem(self.newedge)
                self.newedge = None
                self.__addLink()
                self.__isFirstClick = True

    def slotDeleteLink(self,  edge):
        """ Delete an edge from the topology
        """

        self.__topology.deleteLink(edge)

    def scaleView(self, scale_factor):
        """ Zoom in and out
        """

        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if (factor < 0.20 or factor > 5):
            return
        self.scale(scale_factor, scale_factor)

    def wheelEvent(self, event):
        """ Zoom with the mouse wheel
        """
        self.scaleView(pow(2.0, -event.delta() / 240.0))

    def keyPressEvent(self, event):
        """ key press handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            # Zoom in
            factor_in = pow(2.0, 120 / 240.0)
            self.scaleView(factor_in)
        elif key == QtCore.Qt.Key_Minus:
            # Zoom out
            factor_out = pow(2.0, -120 / 240.0)
            self.scaleView(factor_out)
        elif key == QtCore.Qt.Key_Delete:
            self.slotDeleteNode()
        elif globals.addingLinkFlag and key == QtCore.Qt.Key_Escape:
            self.resetAddingLink()
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

    def dragMoveEvent(self, event):
        """ Drag move event
        """

        event.accept()

    def dropEvent(self, event):
        """ Drop event
        """

        if event.mimeData().hasText():

            symbolname = str(event.mimeData().text())
            x = event.pos().x()  / self.matrix().m11()
            y = event.pos().y()  / self.matrix().m22()
            repx = (self.width() /2) /  self.matrix().m11()
            repy = (self.height()/2) / self.matrix().m22()
            xPos =  x - repx
            yPos = y - repy

            # Get resource corresponding to node type
            object = None
            svgrc = ":/icons/default.svg"
            for item in SYMBOLS:
                if item['name'] == symbolname:
                    renderer_normal = self.renders[symbolname]['normal']
                    renderer_select = self.renders[symbolname]['selected']
                    object = item['object']
                    break

            if object == None:
                return
            node = object(renderer_normal, renderer_select)
            node.type = item['name']
            node.setPos(xPos, yPos)

            if globals.GApp.workspace.flg_showHostname == True:
                node.showHostname()

            self.__topology.addNode(node)

            # Center the node
            pos_x = node.pos().x() - (node.boundingRect().width() / 2)
            pos_y = node.pos().y() - (node.boundingRect().height() / 2)
            node.setPos(pos_x, pos_y)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        show = True
        item = self.itemAt(event.pos())
        if item:
            item_type = type(item)
            if item_type == Ethernet or item_type == Serial:
                show = False
        if show and event.button() == QtCore.Qt.RightButton and not globals.addingLinkFlag:
            if item:
                item.setSelected(True)
            self.showContextualMenu()
        elif event.button() == QtCore.Qt.LeftButton and globals.addingNote:
            note = Annotation()
            note.setPos(self.mapToScene(event.pos()))
            pos_x = note.pos().x()
            pos_y = note.pos().y() - (note.boundingRect().height() / 2)
            note.setPos(pos_x, pos_y)
            globals.GApp.topology.addItem(note)
            note.editText()
            globals.GApp.workspace.action_AddNote.setChecked(False)
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
            globals.addingNote = False
        else:
            QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        if not globals.addingLinkFlag:
            item = self.itemAt(event.pos())
            if isinstance(item, Annotation):
                QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)
            elif item and not isinstance(item, AbstractEdge):
                item.setSelected(True)
                self.slotConfigNode()
        else:
            QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):

        # update new edge position
        if(self.newedge):
            self.newedge.setMousePoint(self.mapToScene(event.pos()))
            event.ignore()
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)
