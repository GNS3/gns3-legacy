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
# http://www.gns3.net/contact
#

#This module is responsible for all the buttons (and reactions) on the main topology.

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

def debugmsg(level, message):
    if debuglevel == 0:
        return
    if debuglevel >= level:
        print message

import sys, time, math, os
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.UndoFramework as undo
from PyQt4 import QtCore, QtGui, QtSvg, Qt
from GNS3.Topology import Topology
from GNS3.Utils import translate, debug
from GNS3.Annotation import Annotation
from GNS3.ShapeItem import AbstractShapeItem, Rectangle, Ellipse
from GNS3.StyleDialog import StyleDialog
from GNS3.MACTableDialog import MACTableDialog
from GNS3.SymbolDialog import SymbolDialog
from GNS3.IDLEPCDialog import IDLEPCDialog
from GNS3.Pixmap import Pixmap
from GNS3.NodeConfigurator import NodeConfigurator
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice
from GNS3.Node.AnyVBoxEmuDevice import AnyVBoxEmuDevice
from GNS3.Node.FRSW import FRSW
from GNS3.Node.ATMSW import ATMSW
from GNS3.Node.ETHSW import ETHSW
from GNS3.Node.ATMBR import ATMBR
from GNS3.Node.Hub import Hub
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial
from GNS3.DragDropMultipleDevicesDialog import DragDropMultipleDevicesDialog
#from GNS3.Ui.Form_DragAndDropMultiDevices import Ui_DragDropMultipleDevices

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
        #self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag) #FIXME

        self.newedge = None
        self.resetAddingLink()
        self.reloadRenderers()

        self.sceneDragging = False
        self.lastMousePos = None

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

    def makeContextualMenu(self, menu):

        items = self.__topology.selectedItems()
        if len(items) == 0:
            return

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

            # Action: AddLink (To add a link)
            addLinkAct = QtGui.QAction(translate('Scene', 'Add a link'), menu)
            addLinkAct.setIcon(QtGui.QIcon(":/icons/connection.svg"))
            self.connect(addLinkAct, QtCore.SIGNAL('triggered()'), self.addLink)

            menu.addAction(configAct)
            menu.addAction(showHostnameAct)
            menu.addAction(changeHostnameAct)
            menu.addAction(addLinkAct)

        instances = map(lambda item: isinstance(item, ETHSW) or isinstance(item, Hub) or isinstance(item, ATMSW) or isinstance(item, ATMBR) or isinstance(item, FRSW), items)
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

        instances = map(lambda item: isinstance(item, AbstractNode), items)
        if True in instances:

            # Action: Change symbol
            changeSymbol = QtGui.QAction(translate('Scene', 'Change Symbol'), menu)
            changeSymbol.setIcon(QtGui.QIcon(':/icons/node_conception.svg'))
            self.connect(changeSymbol, QtCore.SIGNAL('triggered()'), self.slotchangeSymbol)
            menu.addAction(changeSymbol)

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

            # Action: Capture traffic on an interface
            captureAct = QtGui.QAction(translate('Scene', 'Capture'), menu)
            captureAct.setIcon(QtGui.QIcon(':/icons/inspect.svg'))
            self.connect(captureAct, QtCore.SIGNAL('triggered()'), self.slotCapture)

            menu.addAction(consolePortAct)
            menu.addAction(consoleAct)
            menu.addAction(captureAct)

        instances = map(lambda item: isinstance(item, AnyVBoxEmuDevice), items)
        if True in instances:

            # Action: Bring window to front
            displayWindowFocusAct = QtGui.QAction(translate('Scene', 'Bring display to front'), menu)
            displayWindowFocusAct.setIcon(QtGui.QIcon(':/symbols/computer.normal.svg'))
            self.connect(displayWindowFocusAct, QtCore.SIGNAL('triggered()'), self.slotDisplayWindowFocus)
            menu.addAction(displayWindowFocusAct)

            if not sys.platform.startswith('darwin'):
                # Only if not OSX
                # Action: Hide window
                displayWindowHideAct = QtGui.QAction(translate('Scene', 'Hide display window'), menu)
                displayWindowHideAct.setIcon(QtGui.QIcon(':/symbols/computer.normal.svg'))
                self.connect(displayWindowHideAct, QtCore.SIGNAL('triggered()'), self.slotDisplayWindowHide)
                menu.addAction(displayWindowHideAct)

            # Action: Change the console port
            consolePortAct = QtGui.QAction(translate('Scene', 'Change console port'), menu)
            consolePortAct.setIcon(QtGui.QIcon(':/icons/console_port.svg'))
            self.connect(consolePortAct, QtCore.SIGNAL('triggered()'), self.slotChangeConsolePort)
            menu.addAction(consolePortAct)

            # Action: Console (Connect to the node console)
            consoleAct = QtGui.QAction(translate('Scene', 'Console'), menu)
            consoleAct.setIcon(QtGui.QIcon(':/icons/console.svg'))
            self.connect(consoleAct, QtCore.SIGNAL('triggered()'), self.slotConsole)
            menu.addAction(consoleAct)

            # Action: Capture traffic on an interface
            captureAct = QtGui.QAction(translate('Scene', 'Capture'), menu)
            captureAct.setIcon(QtGui.QIcon(':/icons/inspect.svg'))
            self.connect(captureAct, QtCore.SIGNAL('triggered()'), self.slotCapture)
            menu.addAction(captureAct)

        instances = map(lambda item: isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice), items)
        if True in instances:

            # Action: Start (Start IOS on hypervisor)
            startAct = QtGui.QAction(translate('Scene', 'Start'), menu)
            startAct.setIcon(QtGui.QIcon(':/icons/play.svg'))
            self.connect(startAct, QtCore.SIGNAL('triggered()'), self.slotStartNode)

            menu.addAction(startAct)

        instances = map(lambda item: isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice), items)
        if True in instances:

            # Action: Suspend / Pause (Suspend IOS on hypervisor/pause VM)
            suspendAct = QtGui.QAction(translate('Scene', 'Suspend'), menu)
            suspendAct.setIcon(QtGui.QIcon(':/icons/pause.svg'))
            self.connect(suspendAct, QtCore.SIGNAL('triggered()'), self.slotSuspendNode)

            menu.addAction(suspendAct)

        instances = map(lambda item: isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice), items)
        if True in instances:

            # Action: Stop (Stop IOS on hypervisor)
            stopAct = QtGui.QAction(translate('Scene', 'Stop'), menu)
            stopAct.setIcon(QtGui.QIcon(':/icons/stop.svg'))
            self.connect(stopAct, QtCore.SIGNAL('triggered()'), self.slotStopNode)

            # Action: Reload (stop and start IOS on hypervisor)
            reloadAct = QtGui.QAction(translate('Scene', 'Reload'), menu)
            reloadAct.setIcon(QtGui.QIcon(':/icons/reload.svg'))
            self.connect(reloadAct, QtCore.SIGNAL('triggered()'), self.slotReloadNode)

            menu.addAction(stopAct)
            menu.addAction(reloadAct)

        instances = map(lambda item: isinstance(item, IOSRouter), items)
        if True in instances:

            # Action: Change the aux port
            auxPortAct = QtGui.QAction(translate('Scene', 'Change AUX port'), menu)
            auxPortAct.setIcon(QtGui.QIcon(':/icons/console_port.svg'))
            self.connect(auxPortAct, QtCore.SIGNAL('triggered()'), self.slotChangeAUXPort)

            # Action: Console (Connect to the node console)
            AuxAct = QtGui.QAction(translate('Scene', 'Console via AUX port'), menu)
            AuxAct.setIcon(QtGui.QIcon(':/icons/aux-console.svg'))
            self.connect(AuxAct, QtCore.SIGNAL('triggered()'), self.slotAuxConsole)

            # Action: Calculate IDLE PC
            idlepcAct = QtGui.QAction(translate('Scene', 'Idle PC'), menu)
            idlepcAct.setIcon(QtGui.QIcon(':/icons/calculate.svg'))
            self.connect(idlepcAct, QtCore.SIGNAL('triggered()'), self.slotIdlepc)

            # Action: Change the startup-config
            StartupConfigAct = QtGui.QAction(translate('Scene', 'Startup-config'), menu)
            StartupConfigAct.setIcon(QtGui.QIcon(':/icons/startup_config.svg'))
            self.connect(StartupConfigAct, QtCore.SIGNAL('triggered()'), self.slotStartupConfig)

            menu.addAction(auxPortAct)
            menu.addAction(AuxAct)
            menu.addAction(idlepcAct)
            menu.addAction(StartupConfigAct)

        instances = map(lambda item: isinstance(item, Annotation) or isinstance(item, AbstractShapeItem), items)
        if True in instances:

            # Action: Style
            styleAct = QtGui.QAction(translate('Scene', 'Style'), menu)
            styleAct.setIcon(QtGui.QIcon(':/icons/drawing.svg'))
            self.connect(styleAct, QtCore.SIGNAL('triggered()'), self.slotStyle)

            menu.addAction(styleAct)

            # Action: Duplicate
            duplicateAct = QtGui.QAction(translate('Scene', 'Duplicate'), menu)
            duplicateAct.setIcon(QtGui.QIcon(':/icons/new.svg'))
            self.connect(duplicateAct, QtCore.SIGNAL('triggered()'), self.slotDuplicate)

            menu.addAction(duplicateAct)

        # Action: Delete (Delete the node)
        deleteAct = QtGui.QAction(translate('Scene', 'Delete'), menu)
        deleteAct.setIcon(QtGui.QIcon(':/icons/delete.svg'))
        self.connect(deleteAct, QtCore.SIGNAL('triggered()'), self.slotDeleteNode)
        menu.addAction(deleteAct)

        # Action: Lower Z value
        lowerZvalueAct = QtGui.QAction(translate('Scene', 'Lower one layer'), menu)
        lowerZvalueAct.setIcon(QtGui.QIcon(':/icons/lower_z_value.svg'))
        self.connect(lowerZvalueAct, QtCore.SIGNAL('triggered()'), self.slotlowerZValue)

        # Action: Raise Z value
        raiseZvalueAct = QtGui.QAction(translate('Scene', 'Raise one layer'), menu)
        raiseZvalueAct.setIcon(QtGui.QIcon(':/icons/raise_z_value.svg'))
        self.connect(raiseZvalueAct, QtCore.SIGNAL('triggered()'), self.slotraiseZValue)

        menu.addAction(raiseZvalueAct)
        menu.addAction(lowerZvalueAct)

        items = self.__topology.selectedItems()
        if len(items) > 1:

            # Action: Align horizontally
            hozAlignAct = QtGui.QAction(translate('Scene', 'Align horizontally'), menu)
            hozAlignAct.setIcon(QtGui.QIcon(':/icons/horizontally.svg'))
            self.connect(hozAlignAct, QtCore.SIGNAL('triggered()'), self.slotHozAlignment)
            menu.addAction(hozAlignAct)

            # Action: Align vertically
            vertAlignAct = QtGui.QAction(translate('Scene', 'Align vertically'), menu)
            vertAlignAct.setIcon(QtGui.QIcon(':/icons/vertically.svg'))
            self.connect(vertAlignAct, QtCore.SIGNAL('triggered()'), self.slotVertAlignment)
            menu.addAction(vertAlignAct)

    def showContextualMenu(self):
        """  Create and display a contextual menu when clicking on the view
        """

        menu = QtGui.QMenu()
        self.makeContextualMenu(menu)
        menu.exec_(QtGui.QCursor.pos())
        menu.clear()

        # force the deletion of the children
        # for child in menu.children():
        #    child.deleteLater()

    def addItem(self, node):
        """ Overloaded function that add the node into the topology
        """

        self.__topology.addNodeFromScene(node)
        
    def addLink(self):
        """ Call add a link action
        """
        
        globals.GApp.workspace.startAction_addLink()

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

    def slotHozAlignment(self):
        """ Horizontally align items
        """

        hozPos = self.__topology.selectedItems()[0].y()
        for item in self.__topology.selectedItems():
            item.setPos(item.x(), hozPos)

    def slotVertAlignment(self):
        """ Vertically align items
        """

        vertPos = self.__topology.selectedItems()[0].x()
        for item in self.__topology.selectedItems():
            item.setPos(vertPos, item.y())

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
                    #item.autoGenerated = False
                    self.__topology.undoStack.push(command)
                elif isinstance(item, AbstractShapeItem):
                    pen = QtGui.QPen(style.borderColor, style.borderWidth, style.borderStyle, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                    brush = QtGui.QBrush(style.color)
                    command = undo.NewItemStyle(item, pen, brush, style.rotation)
                    self.__topology.undoStack.push(command)

    def slotDuplicate(self):
        """ Duplicate an item
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, Annotation):
                dupnote = Annotation()
                dupnote.setPos(item.x(), item.y() - 20)
                dupnote.setPlainText(item.toPlainText())
                dupnote.setDefaultTextColor(item.defaultTextColor())
                dupnote.setFont(item.font())
                dupnote.rotate(item.rotation)
                dupnote.rotation = item.rotation
                dupnote.setZValue(item.zValue())
                command = undo.AddItem(self.__topology, dupnote, translate("Scene", "annotation"))
                self.__topology.undoStack.push(command)
            if isinstance(item, AbstractShapeItem):
                pos = QtCore.QPointF(item.x() - 20, item.y() - 20)
                rect = item.rect()
                if isinstance(item, Rectangle):
                    dupshape = Rectangle(pos, QtCore.QSizeF(rect.width(), rect.height()))
                else:
                    dupshape = Ellipse(pos, QtCore.QSizeF(rect.width(), rect.height()))
                dupshape.setPen(item.pen())
                dupshape.setBrush(item.brush())
                dupshape.rotate(item.rotation)
                dupshape.rotation = item.rotation
                dupshape.setZValue(item.zValue())
                if isinstance(dupshape, Rectangle):
                    command = undo.AddItem(self.__topology, dupshape, translate("Scene", "rectangle"))
                else:
                    command = undo.AddItem(self.__topology, dupshape, translate("Scene", "ellipse"))
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
                                                   translate("Scene", "%s already has an idlepc value applied, do you want to calculate a new one?") % router.hostname,
                                                   QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    # reset idlepc
                    lib.send(globals.GApp.dynagen.devices[router.hostname].dynamips, 'vm set_idle_pc_online %s 0 %s' % (router.hostname, '0x0'))
                    result = self.calculateIDLEPC(router)
                else:
                    result = globals.GApp.dynagen.devices[router.hostname].idleprop(lib.IDLEPROPSHOW)
            else:
                result = self.calculateIDLEPC(router)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("Scene", "Dynamips error"),  unicode(msg))
            return

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

        idlepcdiag = IDLEPCDialog(router, idles, options)
        idlepcdiag.show()
        idlepcdiag.raise_()
        idlepcdiag.exec_()

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
                isinstance(item, ATMBR) or isinstance(item, FRSW) or isinstance(item, Hub):
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

        count = 0
        for item in self.__topology.selectedItems():
            if not isinstance(item, Annotation) and not isinstance(item, Pixmap) and not isinstance(item, AbstractShapeItem):
                count += 1

        if count > 1:
            reply = QtGui.QMessageBox.question(self, translate("Scene", "Message"), translate("Scene", "Do you really want to delete these nodes?"),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return

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

        show_message = True
        for item in self.__topology.selectedItems():
            zvalue = item.zValue()
            if zvalue > 0:
                command = undo.NewZValue(item, zvalue - 1)
                self.__topology.undoStack.push(command)
            elif isinstance(item, AbstractShapeItem) or isinstance(item, Annotation) or isinstance(item, Pixmap):
                # shape items, annotations and pictures can have a z value lower than 0
                command = undo.NewZValue(item, zvalue - 1)
                self.__topology.undoStack.push(command)
                if zvalue == 0 and show_message:
                    QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("Scene", "Layer position"),  translate("Scene", "Object moved to a background layer. You will now have to use the right-click action to select this object in the future and raise it to layer 0 to be able to move it"))
                    show_message = False

    def slotraiseZValue(self):
        """ Raise Z value
        """

        for item in self.__topology.selectedItems():
            zvalue = item.zValue()
            command = undo.NewZValue(item, zvalue + 1)
            self.__topology.undoStack.push(command)

    def slotchangeSymbol(self):
        """ Change a device's symbol
        """

        item_list = []
        for item in self.__topology.selectedItems():
            if isinstance(item, AbstractNode):
                item_list.append(item)
        if len(item_list):
            dialog = SymbolDialog(item_list)
            dialog.show()
            dialog.exec_()

    def slotConsole(self):
        """ Slot called to launch a console on the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                time.sleep(globals.GApp.systconf['general'].console_delay)
                item.console()

    def slotCapture(self):
        """ Slot called to capture on the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                links = []
                for localif in item.getConnectedInterfaceList():
                    linkobj = item.getConnectedLinkByName(localif)
                    (neighbor, neighborif) = linkobj.getConnectedNeighbor(item)
                    links.append("%s connected to %s %s" % (localif, neighbor.hostname, neighborif))
                (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Scene", "Capture"), translate("Scene", "Please choose a link"), links, 0, False)
                if ok:
                    interface = unicode(selection).split(' ')[0]
                    linkobj = item.getConnectedLinkByName(interface)
                    linkobj.startCapture()

    def slotDisplayWindowFocus(self):
        """ Slot called to bring VM's display as foreground window and focus on it
        """
        for item in self.__topology.selectedItems():
            if isinstance(item, AnyVBoxEmuDevice):
                item.displayWindowFocus()
                return

    def slotDisplayWindowHide(self):
        """ Slot called to hide VM's display window
        """
        for item in self.__topology.selectedItems():
            if isinstance(item, AnyVBoxEmuDevice):
                item.displayWindowHide()
                return

    def slotAuxConsole(self):
        """ Slot called to launch a console to AUX on the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter):
                time.sleep(globals.GApp.systconf['general'].console_delay)
                item.aux()

    def slotChangeConsolePort(self):
        """ Slot called to change the console port
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.changeConsolePort()

    def slotChangeAUXPort(self):
        """ Slot called to change the aux port
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter):
                item.changeAUXPort()

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
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.startNode()

    def slotStopNode(self):
        """ Slot called to stop the selected items
        """

        count = 0
        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                count += 1

        if count > 1:
            reply = QtGui.QMessageBox.question(globals.GApp.mainWindow, translate("Scene", "Message"), translate("Scene", "Do you really want to stop these devices?"),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.stopNode()

    def slotSuspendNode(self):
        """ Slot called to suspend the selected items
        """

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                item.suspendNode()

    def slotReloadNode(self):
        """ Slot called to reload the selected items
        """

        count = 0
        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
                count += 1

        if count > 1:
            reply = QtGui.QMessageBox.question(globals.GApp.mainWindow, translate("Scene", "Message"), translate("Scene", "Do you really want to reload these devices?"),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return

        for item in self.__topology.selectedItems():
            if isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice) or isinstance(item, AnyVBoxEmuDevice):
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
        debugmsg(2, "Scene.py: id = %s" % str(id))
        debugmsg(2, "Scene.py: interface = %s" % str(interface))
        debugmsg(2, "Scene.py: node = %s" % str(self.__topology.getNode(id)))

        if id == None and interface == None:
            self.__isFirstClick = True
            return

        node = self.__topology.getNode(id)

        if globals.currentLinkType == globals.Enum.LinkType.Serial or globals.currentLinkType == globals.Enum.LinkType.ATM or globals.currentLinkType == globals.Enum.LinkType.POS:
            if isinstance(node, AnyEmuDevice) or isinstance(node, AnyVBoxEmuDevice) or isinstance(node, ETHSW) or isinstance(node, Hub):
                if isinstance(node, AnyEmuDevice):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "Qemu machines support only Ethernet links."))
                if isinstance(node, AnyVBoxEmuDevice):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "VirtualBox machines support only Ethernet links."))
                if isinstance(node, ETHSW):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "Ethernet switch supports only Ethernet links."))
                if isinstance(node, Hub):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "Ethernet hub supports only Ethernet links."))
                self.__isFirstClick = True
                return

        if not (globals.currentLinkType == globals.Enum.LinkType.ATM or \
                globals.currentLinkType == globals.Enum.LinkType.Manual) and isinstance(node, ATMSW):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "ATM switch supports only ATM links."))
            self.__isFirstClick = True
            return

        if not (globals.currentLinkType == globals.Enum.LinkType.Serial or \
                globals.currentLinkType == globals.Enum.LinkType.Manual) and isinstance(node, FRSW):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "Frame-Relay switch supports only serial links."))
            self.__isFirstClick = True
            return

        if (globals.currentLinkType == globals.Enum.LinkType.Serial or \
            globals.currentLinkType == globals.Enum.LinkType.POS) and isinstance(node, ATMBR):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "AddLink"),  translate("Scene", "ATM bridge supports only ATM and Ethernet links."))
            self.__isFirstClick = True
            return

        if globals.addingLinkFlag:
            # user is adding a link
            if self.__isFirstClick:
                # source node
                self.__sourceNodeID = id
                self.__sourceInterface = interface
                self.__isFirstClick = False
                #node = self.__topology.getNode(id)
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
        if (factor < 0.10 or factor > 10):
            return
        self.scale(scale_factor, scale_factor)

    def wheelEvent(self, event):
        """ Zoom or scroll with the mouse wheel
        """

        if globals.GApp.workspace.action_DisableMouseWheel.isChecked() == False and \
        (globals.GApp.workspace.action_ZoomUsingMouseWheel.isChecked() or event.modifiers() == QtCore.Qt.ControlModifier) and \
        event.orientation() == QtCore.Qt.Vertical:
            self.scaleView(pow(2.0, event.delta() / 240.0))

        elif globals.GApp.workspace.action_DisableMouseWheel.isChecked() == False:
            QtGui.QGraphicsView.wheelEvent(self, event)

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
            if self.__isFirstClick:
                # Escape has been pressed while we were not drawing a link
                globals.GApp.workspace.stopAction_addLink()
            self.resetAddingLink()
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

    def dragMoveEvent(self, event):
        """ Drag move event
        """

        #debug("Drop event %s" % str(list(event.mimeData().formats())))
        if event.mimeData().hasFormat("text/uri-list") or event.mimeData().hasFormat("application/x-qt-mime-type-name") :
            event.acceptProposedAction()

    def dropEvent(self, event):
        """ Drop event
        """

        if event.mimeData().hasFormat("text/uri-list") and event.mimeData().hasUrls():
            if len(event.mimeData().urls()) > 1:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Scene", "Topology file"),  translate("Scene", "Please select only one file!"))
                return
            for url in event.mimeData().urls():
                path = unicode(url.toLocalFile(), 'utf-8', errors='replace')
                if os.path.isfile(path):
                    path = os.path.normpath(path)
                    debug("Load file from drop event %s" % path)
                    globals.GApp.workspace.openFromDroppedFile(path)
                    break
            event.acceptProposedAction()
        elif event.mimeData().hasText():

            symbolname = str(event.mimeData().text())
            # Get resource corresponding to node type
            object = None
            for item in SYMBOLS:
                if item['name'] == symbolname:
                    renderer_normal = self.renders[symbolname]['normal']
                    renderer_select = self.renders[symbolname]['selected']
                    object = item['object']
                    break
                    
            # If SHIFT key is pressed, launch the multi-drop feature
            if event.keyboardModifiers () == QtCore.Qt.ShiftModifier:
                dialog = DragDropMultipleDevicesDialog()
                dialog.exec_()
            else:
                dialog = None

            if dialog is not None:
                nbOfDevices = DragDropMultipleDevicesDialog.getNbOfDevices(dialog)
                arrangement = DragDropMultipleDevicesDialog.getArrangement(dialog)
            else:
                nbOfDevices = 1
                arrangement = None
            
            # Define the radius of the circle to be drawn when multiple-dropping devices
            radius = nbOfDevices * 35
            # Max number of devices on a single line
            maxDevPerLine = 5
            # Spacing between elements
            offset = 100
            
            for i in range(nbOfDevices):
            
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

                # Compute circle or line(s) arrangement
                if arrangement is not None:
                    if arrangement == "Circle":
                        # Determine center of the node (or set of nodes)
                        x_center = node.pos().x() - (node.boundingRect().width() / 2)
                        y_center = node.pos().y() - (node.boundingRect().height() / 2)
                        period = math.pi + ((2 * math.pi / nbOfDevices) * i)
                        pos_x = radius * math.cos(period) + x_center
                        pos_y = radius * math.sin(period) + y_center
                    elif arrangement == "Line":
                        pos_x = node.pos().x() - (node.boundingRect().width() / 2) + (i % maxDevPerLine) * offset
                        pos_y = node.pos().y() - (node.boundingRect().height() / 2) + (i / maxDevPerLine) * offset
                else:
                    pos_x = node.pos().x() - (node.boundingRect().width() / 2)
                    pos_y = node.pos().y() - (node.boundingRect().height() / 2)
                
                # Set node position on the scene
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

        # This statement checks to see if either the middle mouse is pressed
        # or a combination of the right and left mouse buttons is pressed to start dragging the view
        if show and event.buttons() == (QtCore.Qt.LeftButton | QtCore.Qt.RightButton) or event.buttons() & QtCore.Qt.MidButton:
            self.lastMousePos = self.mapFromGlobal(event.globalPos())
            self.sceneDragging = True
            globals.GApp.scene.setCursor(QtCore.Qt.ClosedHandCursor)
            return

        if show and event.modifiers() & QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton and item and not globals.addingLinkFlag:
#            if isinstance(item, AbstractShapeItem) or isinstance(item, Annotation) or isinstance(item, Pixmap):
#                item.setFlag(item.ItemIsSelectable, True)
            if item.isSelected():
                item.setSelected(False)
            else:
                item.setSelected(True)
        elif show and event.button() == QtCore.Qt.RightButton and not globals.addingLinkFlag:
            if item:
                #Prevent right clicking on a selected item from de-selecting all other items
                if not item.isSelected():
                    if not event.modifiers() & QtCore.Qt.ShiftModifier:
                        for it in self.__topology.items():
                            it.setSelected(False)
                    if item.zValue() < 0:
                        item.setFlag(item.ItemIsSelectable, True)
                    item.setSelected(True)
                    self.showContextualMenu()
                    if item.zValue() < 0:
                        item.setFlag(item.ItemIsSelectable, False)

                else:
                    self.showContextualMenu()
            # When more than one item is selected display the contextual menu even if mouse is not above an item
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

    def mouseReleaseEvent(self, event):
        """ If The Left and Right mouse buttons are not still pressed TOGETHER and neither is the middle button
            this means the user is no longer trying to drag the scene
        """

        item = self.itemAt(event.pos())
        
        if self.sceneDragging and not event.buttons() == (QtCore.Qt.LeftButton | QtCore.Qt.RightButton) and not event.buttons() & QtCore.Qt.MidButton:
            self.sceneDragging = False
            globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)
        else:
            if item is not None and not event.modifiers() & QtCore.Qt.ShiftModifier:
                item.setSelected(True)
                #for other_item in self.__topology.selectedItems():
                #    other_item.setSelected(False)
            QtGui.QGraphicsView.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        item = self.itemAt(event.pos())
        #print "ADEBUG: Scene.py: globals.addingLinkFlag = ", globals.addingLinkFlag
        if not globals.addingLinkFlag and isinstance(item, AbstractNode):
            item.setSelected(True)
            if (isinstance(item, IOSRouter) or isinstance(item, AnyEmuDevice)) and item.isStarted():
                self.slotConsole()
            elif isinstance(item, AnyVBoxEmuDevice) and (item.isStarted() or item.isSuspended()) and not globals.addingLinkFlag:
                self.slotDisplayWindowFocus()
            else:
                self.slotConfigNode()
        else:
            QtGui.QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        """ This if statement event checks to see if the user is dragging the scene
            if so it sets the value of the scene scroll bars based on the change between
            the previous and current mouse position
        """

        if self.sceneDragging:
            mappedGlobalPos = self.mapFromGlobal(event.globalPos())
            hBar = self.horizontalScrollBar()
            vBar = self.verticalScrollBar()
            delta = mappedGlobalPos - self.lastMousePos;
            hBar.setValue(hBar.value() + (delta.x() if globals.GApp.isRightToLeft() else -delta.x()))
            vBar.setValue(vBar.value() - delta.y())
            self.lastMousePos = mappedGlobalPos
        elif (self.newedge):
            self.newedge.setMousePoint(self.mapToScene(event.pos()))
            event.ignore()
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)
