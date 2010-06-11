# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.UndoFramework as undo
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Topology import Topology
from GNS3.Utils import translate, debug
from GNS3.Annotation import Annotation
from GNS3.ShapeItem import AbstractShapeItem, Rectangle, Ellipse
from GNS3.StyleDialog import StyleDialog
from GNS3.MACTableDialog import MACTableDialog
from GNS3.Pixmap import Pixmap
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMBR import ATMBR
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
        self.reloadRenderers()

    def reloadRenderers(self):
        """ Load all needed renderers
        """
            
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

        instances = map(lambda item: not isinstance(item, Annotation) and not isinstance(item, Pixmap) and not isinstance(item, AbstractShapeItem), items)
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

            menu.addAction(configAct)
            menu.addAction(showHostnameAct)
            menu.addAction(changeHostnameAct)

        instances = map(lambda item: isinstance(item, ETHSW) or isinstance(item, ATMSW) or isinstance(item, ATMBR) or isinstance(item, FRSW), items)
        if True in instances:
            
            # Action: ChangeHypervisor (Change the hypervisor)
            changeHypervisor = QtGui.QAction(translate('Scene', 'Set an hypervisor'), menu)
            changeHypervisor.setIcon(QtGui.QIcon(":/icons/applications.svg"))
            self.connect(changeHypervisor, QtCore.SIGNAL('triggered()'), self.slotChangeHypervisor)
            
            menu.addAction(changeHypervisor)
            
        instances = map(lambda item: isinstance(item, ETHSW), items)
        if True in instances:
            
            # Action: MAC Table
            MACTableAct = QtGui.QAction(translate('Scene', 'MAC Address Table'), menu)
            MACTableAct.setIcon(QtGui.QIcon(':/icons/inspect.svg'))
            self.connect(MACTableAct, QtCore.SIGNAL('triggered()'), self.slotMACTable)

            menu.addAction(MACTableAct)

        instances = map(lambda item: isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice), items)
        if True in instances:

            # Action: Change the console port
            consolePortAct = QtGui.QAction(translate('Scene', 'Change console port'), menu)
            consolePortAct.setIcon(QtGui.QIcon(':/icons/console_port.svg'))
            self.connect(consolePortAct, QtCore.SIGNAL('triggered()'), self.slotChangeConsolePort)

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

            menu.addAction(consolePortAct)
            menu.addAction(consoleAct)
            menu.addAction(startAct)
            menu.addAction(stopAct)

        instances = map(lambda item: isinstance(item, IOSRouter), items)
        if True in instances:

            # Action: Calculate IDLE PC
            idlepcAct = QtGui.QAction(translate('Scene', 'Idle PC'), menu)
            idlepcAct.setIcon(QtGui.QIcon(':/icons/calculate.svg'))
            self.connect(idlepcAct, QtCore.SIGNAL('triggered()'), self.slotIdlepc)
            
            # Action: Change the startup-config
            StartupConfigAct = QtGui.QAction(translate('Scene', 'Startup-config'), menu)
            StartupConfigAct.setIcon(QtGui.QIcon(':/icons/startup_config.svg'))
            self.connect(StartupConfigAct, QtCore.SIGNAL('triggered()'), self.slotStartupConfig)

            # Action: Suspend (Suspend IOS on hypervisor)
            suspendAct = QtGui.QAction(translate('Scene', 'Suspend'), menu)
            suspendAct.setIcon(QtGui.QIcon(':/icons/pause.svg'))
            self.connect(suspendAct, QtCore.SIGNAL('triggered()'), self.slotSuspendNode)
            
            # Action: Reload (stop and start IOS on hypervisor)
            reloadAct = QtGui.QAction(translate('Scene', 'Reload'), menu)
            reloadAct.setIcon(QtGui.QIcon(':/icons/reload.svg'))
            self.connect(reloadAct, QtCore.SIGNAL('triggered()'), self.slotReloadNode)

            menu.addAction(suspendAct)
            menu.addAction(reloadAct)
            menu.addAction(idlepcAct)
            menu.addAction(StartupConfigAct)

        instances = map(lambda item: isinstance(item, Annotation) or isinstance(item, AbstractShapeItem), items)
        if True in instances:
        
            # Action: Style
            styleAct = QtGui.QAction(translate('Scene', 'Style'), menu)
            styleAct.setIcon(QtGui.QIcon(':/icons/drawing.svg'))
            self.connect(styleAct, QtCore.SIGNAL('triggered()'), self.slotStyle)

            menu.addAction(styleAct)
            
        # Action: Delete (Delete the node)
        deleteAct = QtGui.QAction(translate('Scene', 'Delete'), menu)
        deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(deleteAct, QtCore.SIGNAL('triggered()'), self.slotDeleteNode)
        menu.addAction(deleteAct)
        
        # Action: Lower Z value
        lowerZvalueAct = QtGui.QAction(translate('Scene', 'Lower one step'), menu)
        lowerZvalueAct.setIcon(QtGui.QIcon(':/icons/lower_z_value.svg'))
        self.connect(lowerZvalueAct, QtCore.SIGNAL('triggered()'), self.slotlowerZValue)
            
        # Action: Raise Z value
        raiseZvalueAct = QtGui.QAction(translate('Scene', 'Raise one step'), menu)
        raiseZvalueAct.setIcon(QtGui.QIcon(':/icons/raise_z_value.svg'))
        self.connect(raiseZvalueAct, QtCore.SIGNAL('triggered()'), self.slotraiseZValue)

        menu.addAction(raiseZvalueAct)
        menu.addAction(lowerZvalueAct)

        menu.exec_(QtGui.QCursor.pos())

        # force the deletion of the children
        for child in menu.children():
            child.deleteLater()

    def addItem(self, node):
        """ Overloaded function that add the node into the topology
        """

        self.__topology.addNodeFromScene(node)

    def calculateIDLEPC(self, router):
        """ Show a splash screen
        """

        splash = QtGui.QSplashScreen(QtGui.QPixmap(":images/logo_gns3_splash.png"))
        splash.show()
        splash.showMessage(translate("Scene", "Please wait while calculating an IDLE PC"))
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        result = globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPGET)
        return result

    def slotMACTable(self):
        """ Show Ethernet Switch MAC Address Table
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, ETHSW):
                table = MACTableDialog(item)
                table.show()
                table.exec_()

    def slotStyle(self):
        """ Change the style of an annotation or a shape item
        """
        
        style = StyleDialog()
        style.setModal(True)
        if self.__topology.selectedItems():
            firstItem = self.__topology.selectedItems()[0]
            if isinstance(firstItem, Annotation):
                style.loadFontValues(firstItem.defaultTextColor(), firstItem.font(), firstItem.rotation)
            elif isinstance(firstItem, AbstractShapeItem):
                pen = firstItem.pen()
                brush = firstItem.brush()
                if brush.style() == QtCore.Qt.NoBrush:
                    color = QtCore.Qt.transparent
                else:
                    color = brush.color()
                style.loadShapeItemValues(color, pen.color(), pen.width(), pen.style(), firstItem.rotation)
        style.show()
        if style.exec_():
            for item in self.__topology.selectedItems():
                if isinstance(item, Annotation):
                    command = undo.NewAnnotationStyle(item, style.color, style.font, style.rotation)
                    item.autoGenerated = False
                    self.__topology.undoStack.push(command)
                elif isinstance(item, AbstractShapeItem):
                    pen = QtGui.QPen(style.borderColor, style.borderWidth, style.borderStyle, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                    brush = QtGui.QBrush(style.color)
                    command = undo.NewItemStyle(item, pen, brush, style.rotation)
                    self.__topology.undoStack.push(command)

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
                selection = str(selection).split(':')[0].strip('* ')
                index = int(selection)
                for node in globals.GApp.topology.nodes.values():
                    if isinstance(node, IOSRouter) and node.hostname == router.hostname:
                        dyn_router = node.get_dynagen_device()
                        if globals.GApp.iosimages.has_key(dyn_router.dynamips.host + ':' + dyn_router.image):
                            image = globals.GApp.iosimages[dyn_router.dynamips.host + ':' + dyn_router.image]
                            debug("Register IDLE PC " + idles[index] + " for image " + image.filename)
                            image.idlepc =  idles[index]
                            # Apply idle pc to devices with the same IOS image
                            for device in globals.GApp.topology.nodes.values():
                                if isinstance(device, IOSRouter) and device.config['image'] == image.filename:
                                    debug("Apply IDLE PC " + idles[index] + " to " + device.hostname)
                                    device.get_dynagen_device().idlepc = idles[index]
                                    config = device.get_config()
                                    config['idlepc'] = idles[index]
                                    device.set_config(config)
                                    device.setCustomToolTip()
                            break
                QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("Scene", "IDLE PC"),
                                              unicode(translate("Scene", "Applied idlepc value %s to %s")) % (idles[index], router.hostname))
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Scene", "Dynamips error"),  unicode(msg))
            return

    def slotConfigNode(self):
        """ Called to configure nodes
        """

        items = self.__topology.selectedItems()
        globals.nodeConfiguratorWindow = NodeConfigurator(items)
        globals.nodeConfiguratorWindow.setModal(True)
        globals.nodeConfiguratorWindow.show()
        globals.nodeConfiguratorWindow.exec_()
        globals.nodeConfiguratorWindow = None
        for item in items:
            item.setSelected(False)

    def slotChangeHostname(self):
        """ Slot called to change hostnames of selected items
        """

        for item in self.__topology.selectedItems():
            item.changeHostname()
            
    def slotChangeHypervisor(self):
        """ Slot called to change hypervisor of selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, ETHSW) or isinstance(item, ATMSW) or \
                isinstance(item, ATMBR) or isinstance(item, FRSW):
                item.changeHypervisor()

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
            if not isinstance(item, Annotation) and not isinstance(item, Pixmap) and not isinstance(item, AbstractShapeItem):
                for link in item.getEdgeList().copy():
                    if self.__topology.deleteLinkFromScene(link) == False:
                        if ok_to_delete_node:
                            ok_to_delete_node = False
                        continue
                if ok_to_delete_node:
                    self.__topology.deleteNodeFromScene(item.id)
            else:
                command = undo.DeleteItem(self.__topology, item)
                self.__topology.undoStack.push(command)

    def slotlowerZValue(self):
        """ Lower Z value
        """
 
        for item in self.__topology.selectedItems():
            zvalue = item.zValue()
            if zvalue > 0:
                command = undo.NewZValue(item, zvalue - 1)
                self.__topology.undoStack.push(command)
            elif isinstance(item, AbstractShapeItem):
                # shape items can have a z value lower than 0
                command = undo.NewZValue(item, zvalue - 1)
                self.__topology.undoStack.push(command)

    def slotraiseZValue(self):
        """ Raise Z value
        """
    
        for item in self.__topology.selectedItems():
            zvalue = item.zValue()
            command = undo.NewZValue(item, zvalue + 1)
            self.__topology.undoStack.push(command)

    def slotConsole(self):
        """ Slot called to launch a console on the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice):
                item.console()
                
    def slotChangeConsolePort(self):
        """ Slot called to change the console port
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice):
                item.changeConsolePort()

    def slotStartupConfig(self):
        """ Slot called to change the startup-config
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter):
                item.changeStartupConfig()

    def slotStartNode(self):
        """ Slot called to start the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice):
                item.startNode()

    def slotStopNode(self):
        """ Slot called to stop the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice):
                item.stopNode()

    def slotSuspendNode(self):
        """ Slot called to suspend the selected items
        """

        for item in self.__topology.selectedItems():
            if  isinstance(item, IOSRouter):
                item.suspendNode()
                
    def slotReloadNode(self):
        """ Slot called to reload the selected items
        """

        for item in self.__topology.selectedItems():
            if  isinstance(item, IOSRouter):
                item.reloadNode()
                
    def getSourceNode(self):
    
        return globals.GApp.topology.getNode(self.__sourceNodeID)
        
    def getDestNode(self):
    
        return globals.GApp.topology.getNode(self.__destNodeID)

    def __addLink(self):
        """ Add a new link between two nodes
        """

        if self.__sourceNodeID == self.__destNodeID:
            self.__isFirstClick = True
            return

        srcnode = self.getSourceNode()
        destnode = self.getDestNode()

        if srcnode == None or destnode == None:
            self.__isFirstClick = True
            return

        # add the link into the topology
        if self.__topology.addLinkFromScene(self.__sourceNodeID, self.__sourceInterface, self.__destNodeID, self.__destInterface) == False:
            self.__isFirstClick = True
        
        self.__sourceNodeID = None
        self.__destNodeID = None

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
                node = self.__topology.getNode(id)
                if (globals.currentLinkType == globals.Enum.LinkType.Serial or globals.currentLinkType == globals.Enum.LinkType.ATM) or \
                    (globals.currentLinkType == globals.Enum.LinkType.Manual and ((interface[0] == 's' or interface[0] == 'a') or (isinstance(node, ATMSW) or isinstance(node, FRSW)))):
                    # interface is serial or ATM
                    self.newedge = Serial(node, interface, self.mapToScene(QtGui.QCursor.pos()), 0, Fake = True)
                else:
                    # by default use an ethernet link
                    self.newedge = Ethernet(node, interface, self.mapToScene(QtGui.QCursor.pos()), 0, Fake = True)
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

        self.__topology.deleteLinkFromScene(edge)

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
        if key == QtCore.Qt.Key_Plus and event.modifiers() == QtCore.Qt.Key_Control:
            # Zoom in
            factor_in = pow(2.0, 120 / 240.0)
            self.scaleView(factor_in)
        elif key == QtCore.Qt.Key_Minus and event.modifiers() == QtCore.Qt.Key_Control:
            # Zoom out
            factor_out = pow(2.0, -120 / 240.0)
            self.scaleView(factor_out)
        elif key == QtCore.Qt.Key_Delete:
            # check if we are editing an Annotation object, then send the Delete event to it
            for item in self.__topology.selectedItems():
                if isinstance(item, Annotation) and item.hasFocus():
                    QtGui.QGraphicsView.keyPressEvent(self, event)
                    return
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
            # Get resource corresponding to node type
            object = None
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
            if SYMBOL_TYPES[item['object']] != item['name']:
                node.default_symbol = False
            node.setPos(self.mapToScene(event.pos()))

            if globals.GApp.workspace.flg_showHostname == True:
                node.showHostname()

            self.__topology.addNodeFromScene(node)

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
                
        if show and event.modifiers() & QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton and item and not globals.addingLinkFlag:
            item.setSelected(True)
        elif show and event.button() == QtCore.Qt.RightButton and not globals.addingLinkFlag:
            if item:
                if not event.modifiers() & QtCore.Qt.ShiftModifier:
                    for it in globals.GApp.topology.items():
                        it.setSelected(False)
                item.setSelected(True)
                self.showContextualMenu()
            elif len(self.__topology.selectedItems()) > 1:
                self.showContextualMenu()
        elif event.button() == QtCore.Qt.LeftButton and globals.addingNote:
            note = Annotation()
            note.setPos(self.mapToScene(event.pos()))
            pos_x = note.pos().x()
            pos_y = note.pos().y() - (note.boundingRect().height() / 2)
            note.setPos(pos_x, pos_y)      
            command = undo.AddItem(self.__topology, note, translate("Scene", "annotation"))
            self.__topology.undoStack.push(command)
            note.editText()
            globals.GApp.workspace.action_AddNote.setChecked(False)
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
            globals.addingNote = False
        elif event.button() == QtCore.Qt.LeftButton and globals.drawingRectangle:
            size = QtCore.QSizeF(200, 100)
            item = Rectangle(self.mapToScene(event.pos()),  size)
            command = undo.AddItem(self.__topology, item, translate("Scene", "rectangle"))
            self.__topology.undoStack.push(command)
            globals.GApp.workspace.action_DrawRectangle.setChecked(False)
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
            globals.drawingRectangle = False
        elif event.button() == QtCore.Qt.LeftButton and globals.drawingEllipse:
            size = QtCore.QSizeF(200, 200)
            item = Ellipse(self.mapToScene(event.pos()),  size)
            command = undo.AddItem(self.__topology, item, translate("Scene", "ellipse"))
            self.__topology.undoStack.push(command)
            globals.GApp.workspace.action_DrawEllipse.setChecked(False)
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
            globals.drawingEllipse = False
        else:
            QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        item = self.itemAt(event.pos())
        if not globals.addingLinkFlag and isinstance(item, AbstractNode):
            item.setSelected(True)
            self.slotConfigNode()
        else:
            QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):

        if (self.newedge):
            self.newedge.setMousePoint(self.mapToScene(event.pos()))
            event.ignore()
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)
