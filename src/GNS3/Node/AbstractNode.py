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

import re
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui, QtSvg
from GNS3.Utils import translate, debug
import GNS3.UndoFramework as undo

class AbstractNode(QtSvg.QGraphicsSvgItem):
    """ AbstractNode class
        Base class to create Dynamips nodes
    """

    def __init__(self, render_normal, render_select):
        """ renderer_normal: QtSvg.QSvgRenderer
            renderer_select: QtSvg.QSvgRenderer
        """

        QtSvg.QGraphicsSvgItem.__init__(self)
        self.__render_normal = render_normal
        self.__render_select = render_select
        self.__edgeList = set()
        self.__selectedInterface = None
        self.__flag_hostname = False

        self.dynagen = globals.GApp.dynagen
        self.default_symbol = True
        self.consoleProcesses = []

        # status used in the topology summary
        self.state = 'stopped'

        # create a unique ID
        self.id = globals.GApp.topology.node_baseid
        globals.GApp.topology.node_baseid += 1

        # default hostname
        self.hostname = 'Node' + str(self.id)

        # scene settings
        flags = self.ItemIsMovable | self.ItemIsSelectable | self.ItemIsFocusable
        # necessary to receive itemChange() notifications with Qt >= 4.6
        if QtCore.QT_VERSION >= 0x040600:
            try:
                flags = flags | self.ItemSendsGeometryChanges
            except AttributeError:
                # Forced to do this on CentOS, for an unknown reason, Qt doesn't support ItemSendsGeometryChanges even if version >= 4.6
                # This is very likely that the topology will break apart if not supported!
                pass
        self.setFlags(flags)
        self.setAcceptsHoverEvents(True)
        self.setSharedRenderer(self.__render_normal)

        # x&y position for hostname
        self.hostname_xpos = None
        self.hostname_ypos = None

        self.default_hostname_xpos = None
        self.default_hostname_ypos = None

        # Used by the undo process to prevent to ask again to choose an image
        self.image_reference = None

        self.setZValue(1)

    def __del__(self):

        if globals.GApp.systconf['general'].term_close_on_delete:
            self.closeAllConsoles()

    def closeAllConsoles(self):
        """ Close all opened terminal programs
        """

        # closing terminal programs
        for console in self.consoleProcesses:
            console.poll()
            if console.returncode == None:
                # the process hasn't returned yet (still active)
                debug("Sending terminate signal to terminal program (pid %i)" % console.pid)
                try:
                    console.terminate()
                except:
                    debug("Error while sending the signal to terminal program (pid %i)" % console.pid)
                    continue
        self.consoleProcesses = []

    def clearClosedConsoles(self):
        """ Refresh the list of opened terminal programs.
        """

        updated_list = []
        for console in self.consoleProcesses:
            console.poll()
            if console.returncode == None:
                # the process hasn't returned yet (still active)
                updated_list.append(console)
        self.consoleProcesses = updated_list
        debug("%s has %i terminal program(s) connected to itself" % (self.hostname, len(self.consoleProcesses)))

    def setRenderers(self, render_normal, render_select):
        """ renderer_normal: QtSvg.QSvgRenderer
            renderer_select: QtSvg.QSvgRenderer
        """

        self.__render_normal = render_normal
        self.__render_select = render_select
        self.setSharedRenderer(self.__render_normal)

    def getState(self):
        """ Returns the current node state
        """

        return (self.state)

    def updateToolTips(self):
        """ Update node and child links tooltip
        """

        self.setCustomToolTip()
        for edge in self.__edgeList:
            edge.setCustomToolTip()
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()

    def setUndoConfig(self, config, prevConfig):
        """ Set a new config to be put on the undo stack
        """

        command = undo.AddConfig(self, config, prevConfig)
        globals.GApp.topology.undoStack.push(command)

    def changeHostname(self):
        """ Called to change the hostname
        """

        (text, ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, translate("AbstractNode", "Change the hostname"),
                                          translate("AbstractNode", "Hostname:"), QtGui.QLineEdit.Normal,
                                          self.hostname)
        if ok and text:
            text = unicode(text)
            if not re.search(r"""^[\w,.\-\[\]]*$""", text, re.UNICODE):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"),
                                           translate("AbstractNode", "Please use only alphanumeric characters"))
                self.changeHostname()
                return
            
            if text.lower() == 'lan':
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"),
                                           translate("AbstractNode", "Please choose another hostname.\n%s is used by Dynagen to specify bridged networks.") % text)
                self.changeHostname()
                return

            for node in globals.GApp.topology.nodes.itervalues():
                if text == node.hostname:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hostname"),  translate("AbstractNode", "Hostname already used"))
                    return

            command = undo.NewHostname(self, text)
            globals.GApp.topology.undoStack.push(command)

    def changeHypervisor(self):
        """ Called to change an hypervisor
        """

        if len(self.__edgeList) > 0:
            QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractNode", "Hypervisor"),
                                      translate("AbstractNode", "The device must have no connection to other devices in order to change its hypervisor"))
            return

        if self.d:
            currentHypervisor = self.d
        else:
            currentHypervisor = "hostname:port"
        (text, ok) = QtGui.QInputDialog.getText(globals.GApp.mainWindow, translate("AbstractNode", "Set hypervisor"),
                                    translate("AbstractNode", "New hypervisor:"), QtGui.QLineEdit.Normal,
                                    currentHypervisor)

        if ok and text:
            hypervisor = unicode(text)
            if not re.search(r"""^.*:[0-9]*$""", text, re.UNICODE):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hypervisor"),
                                           translate("AbstractNode", "Invalid format for hypervisor (hostname:port is required)"))
                return
            (host, port) = hypervisor.rsplit(':',  1)

            if self.dynagen.dynamips.has_key(hypervisor):
                debug("Use an hypervisor: " + hypervisor)
                dynamips_hypervisor = self.dynagen.dynamips[hypervisor]
            else:
                debug("Connection to an hypervisor: " + hypervisor)

                # use project workdir
                if globals.GApp.workspace.projectWorkdir:
                    self.dynagen.defaults_config['workingdir'] = globals.GApp.workspace.projectWorkdir
                elif globals.GApp.systconf['dynamips'].workdir:
                    self.dynagen.defaults_config['workingdir'] = globals.GApp.systconf['dynamips'].workdir

                dynamips_hypervisor = self.dynagen.create_dynamips_hypervisor(host, int(port))
                if not dynamips_hypervisor:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Hypervisor"),
                                               translate("AbstractNode", "Can't connect to the hypervisor on %s") % hypervisor)
                    if self.dynagen.dynamips.has_key(hypervisor):
                        del self.dynagen.dynamips[hypervisor]
                    return

            self.dynagen.update_running_config()
            if self.d and self.dynagen.running_config[self.d].has_key(self.get_running_config_name()):
                config = self.dynagen.running_config[self.d][self.get_running_config_name()]
                self.dynagen.running_config[host + ':' + port][self.get_running_config_name()] = config
                del self.dynagen.running_config[self.d][self.get_running_config_name()]
            self.set_hypervisor(dynamips_hypervisor)
            self.reconfigNode(self.hostname)
            self.dynagen.update_running_config()
            QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("AbstractNode", "Hypervisor"),
                                          translate("AbstractNode", "New hypervisor %s has been set on device %s") % (hypervisor, self.hostname))

    def changeConsolePort(self):
        """ Called to change the console port
        """

        device = self.get_dynagen_device()
        (port, ok) = QtGui.QInputDialog.getInteger(globals.GApp.mainWindow, translate("AbstractNode", "Change the console port"),
                                                   translate("AbstractNode", "Console port for %s:") % self.hostname, device.console, 1, 65535, 1)
        if ok and device.console != port:

            command = undo.NewConsolePort(self, port)
            globals.GApp.topology.undoStack.push(command)
            if command.getStatus() != None:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Console port"), unicode(command.getStatus()))
                globals.GApp.topology.undoStack.undo()

    def changeAUXPort(self):
        """ Called to change the aux port
        """

        device = self.get_dynagen_device()
        if not device.aux:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "AUX port"),
                                       translate("AbstractNode", "AUX port not available for this router model or base AUX port is set to 0 in preferences"))
            return False

        current_aux = device.aux
        (port, ok) = QtGui.QInputDialog.getInteger(globals.GApp.mainWindow, translate("AbstractNode", "Change the aux port"),
                                                   translate("AbstractNode", "AUX port for %s:") % self.hostname, current_aux, 1, 65535, 1)
        if ok and device.aux != port:

            command = undo.NewAUXPort(self, port)
            globals.GApp.topology.undoStack.push(command)
            if command.getStatus() != None:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "AUX port"), unicode(command.getStatus()))
                globals.GApp.topology.undoStack.undo()

    def paint(self, painter, option, widget=None):
        """ Don't show the selection rectangle
        """

        _local_option = option
        if globals.GApp.systconf['general'].draw_selected_rectangle == False:
            _local_option.state = QtGui.QStyle.State_None

        QtSvg.QGraphicsSvgItem.paint(self, painter, _local_option, widget)

        # Don't draw if not activated
        if globals.GApp.workspace.flg_showLayerPos == False:
            return

        # Show layer level of this node
        brect = self.boundingRect()
        center = self.mapFromItem(self, brect.width() / 2.0, brect.height() / 2.0)

        painter.setBrush(QtCore.Qt.red)
        painter.setPen(QtCore.Qt.red)
        painter.drawRect((brect.width() / 2.0) - 10, (brect.height() / 2.0) - 10, 20,20)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("TypeWriter", 14, QtGui.QFont.Bold))
        zval = str(int(self.zValue()))
        painter.drawText(QtCore.QPointF(center.x() - 4, center.y() + 4), zval)

    def itemChange(self, change, value):
        """ do some action when item is changed...
        """

        # when the item is selected/unselected
        # dynamically change the renderer
        if change == self.ItemSelectedChange and self.__render_select:
            if value.toInt()[0] == 1:
                self.setSharedRenderer(self.__render_select)
            else:
                self.setSharedRenderer(self.__render_normal)

        if change == self.ItemPositionChange or change == self.ItemPositionHasChanged:
            for edge in self.__edgeList:
                edge.adjust()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def hoverEnterEvent(self, event):
        """ Called when the mouse is hover the node
        """

        # update tool tip
        try:
            self.setCustomToolTip()
        except:
            print translate("AbstractNode", "Cannot communicate with %s, the server running this node may have crashed!" % self.hostname)
        if not self.isSelected() and self.__render_select:
            self.setSharedRenderer(self.__render_select)
#            if not globals.addingLinkFlag:
#                globals.GApp.scene.setCursor(QtCore.Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        """ Called when the mouse leaves the node
        """

        if not self.isSelected() and self.__render_select:
            self.setSharedRenderer(self.__render_normal)
#            if not globals.addingLinkFlag:
#                globals.GApp.scene.setCursor(QtCore.Qt.ArrowCursor)

    def addEdge(self, edge):
        """ Save the edge
            edge: Edge instance
        """

        self.__edgeList.add(edge)
        edge.adjust()

    def deleteEdge(self, edge):
        """ Delete the edge
            edge: Edge instance
        """

        if edge in self.__edgeList:
            edge.stopCapturing(showMessage=False)
            self.__edgeList.remove(edge)

    def getEdgeList(self):
        """ Returns the edge list
        """

        return self.__edgeList

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        self.setToolTip(translate("AbstractNode", "Hostname: %s") % self.hostname)

    def keyPressEvent(self, event):
        """ Key press handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.__deleteAction()
        else:
            QtGui.QGraphicsItem.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the node is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if globals.workaround_ManualLink == True:
            # We're not the right recipient of this event,
            # so acknowledge the workaround and return
            globals.workaround_ManualLink = False
            return

        if globals.addingLinkFlag and event.button() == QtCore.Qt.LeftButton:

            self.__selectedInterface = None
            self.showMenuInterface()
            if self.__selectedInterface:
                if self.__selectedInterface in self.getConnectedInterfaceList():
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"),  translate("AbstractNode", "Already connected interface") )
                    return
                self.emit(QtCore.SIGNAL("Add link"), self.id,  self.__selectedInterface)
#        elif event.button() == QtCore.Qt.LeftButton:
#            globals.GApp.scene.setCursor(QtCore.Qt.ClosedHandCursor)
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

#        if not globals.addingLinkFlag:
#            globals.GApp.scene.setCursor(QtCore.Qt.OpenHandCursor)
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    def getConnectedInterfaceList(self):
        """ Returns a list of all the connected local interfaces
        """

        interface_list = set()
        for edge in self.__edgeList:
            interface = edge.getLocalInterface(self)
            interface_list.add(interface)
        return interface_list

    def getConnectedLinkByName(self, ifname):
        """ Returns the link object corresponding to an interface name
        """

        for edge in self.__edgeList:
            interface = edge.getLocalInterface(self)
            if interface == ifname:
                return edge
        return None

    def getConnectedNeighbor(self, ifname):
        """ Returns the connected neighbor's node and interface
        """

        for edge in self.__edgeList:
            interface = edge.getLocalInterface(self)
            if interface == ifname:
                return edge.getConnectedNeighbor(self)
        return None

    def showMenuInterface(self, unavailable_interfaces=[]):
        """ Show a contextual menu to choose an interface on a specific node
        """

        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)
        menu = QtGui.QMenu()
        self.connect(menu, QtCore.SIGNAL("hovered(QAction *)"), self._actionHovered)
        interfaces_list = self.getInterfaces()
        if len(interfaces_list) == 0:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractNode", "Connection"), translate("AbstractNode", "No interface available, please configure this device"))
            return
        connected_list = self.getConnectedInterfaceList()
        for interface in interfaces_list:
            if interface in unavailable_interfaces:
                # interface cannot be chosen by user (grayed out)
                action = menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), interface)
                action.setDisabled(True)
            elif interface in connected_list:
                # already connected interface
                menu.addAction(QtGui.QIcon(':/icons/led_green.svg'), interface)
            else:
                # disconnected interface
                menu.addAction(QtGui.QIcon(':/icons/led_red.svg'), interface)

        # connect the menu
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.slotSelectedInterface)
        menu.exec_(QtGui.QCursor.pos())
        globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 1000)

    # Overloaded in Cloud
    def _actionHovered(self, action):
        pass

    def showHostname(self):
        """ Show the hostname on the scene
        """

        # don't try to show hostname twice
        if self.__flag_hostname == True:
            return
        hostname = self.hostname
        if type(hostname) != unicode:
            hostname = unicode(hostname)
        self.textItem = QtGui.QGraphicsTextItem(hostname, self)
        self.textItem.setFont(QtGui.QFont("TypeWriter", 10, QtGui.QFont.Bold))
        self.textItem.setFlag(self.textItem.ItemIsMovable)
        if self.hostname_xpos == None and self.hostname_ypos == None:
            # use default positions
            textrect = self.textItem.boundingRect()
            textmiddle = textrect.topRight() / 2
            noderect = self.boundingRect()
            nodemiddle = noderect.topRight() / 2
            self.default_hostname_xpos = nodemiddle.x() - textmiddle.x()
            self.default_hostname_ypos = -25
            self.textItem.setPos(self.default_hostname_xpos, self.default_hostname_ypos)
        else:
            # use user defined positions
            self.textItem.setPos(self.hostname_xpos, self.hostname_ypos)
        self.__flag_hostname = True

    def removeHostname(self):
        """ Remove the hostname on the scene
        """

        if self.__flag_hostname == True:
            if self.textItem.x() != self.default_hostname_xpos or self.textItem.y() != self.default_hostname_ypos:
                # record user defined positions
                self.hostname_xpos = self.textItem.x()
                self.hostname_ypos = self.textItem.y()
            globals.GApp.topology.removeItem(self.textItem)
            self.__flag_hostname = False

    def hostnameDiplayed(self):
        """ Check if the hostname is displayed
        """

        return self.__flag_hostname

    def deleteInterface(self, ifname):
        """ Delete an interface and the link that is connected to it
            ifname: string
        """

        for edge in self.__edgeList.copy():
            interface = edge.getLocalInterface(self)
            if ifname == interface:
                self.emit(QtCore.SIGNAL("Delete link"), edge)

    def slotSelectedInterface(self, action):
        """ Called when an interface is selected from the contextual menu
            in design mode
            action: QtCore.QAction instance
        """

        interface = str(action.text())
        assert(interface)
        self.__selectedInterface = interface

    def startupInterfaces(self):
        """ Startup all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'up')

    def shutdownInterfaces(self):
        """ Shutdown all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'down')

    def suspendInterfaces(self):
        """ Suspend all interfaces
        """

        for edge in self.getEdgeList():
            edge.setLocalInterfaceStatus(self.id, 'suspended')
