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

import math, time, sys
import GNS3.Globals as globals
import subprocess as sub
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.FRSW import FRSW

class AbstractEdge(QtGui.QGraphicsPathItem, QtCore.QObject):
    """ AbstractEdge class
        Base class to create edges between nodes
    """

    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False):

        QtGui.QGraphicsItem.__init__(self)

        # status points size
        self.pointSize = 10
        # default pen size
        self.penWidth = 2.0

        self.source = sourceNode
        self.dest = destNode
        self.fake = Fake

        if not self.fake:

            self.srcIf = sourceIf
            self.destIf = destIf
            self.src_interface_status = 'down'
            self.dest_interface_status = 'down'

            # capture feature variables
            self.capturing = False
            self.capfile = None
            self.captureInfo = None

            # create a unique ID
            self.id = globals.GApp.topology.link_baseid
            globals.GApp.topology.link_baseid += 1

            # Set default tooltip
            self.setCustomToolTip()

            # record the edge into the nodes
            self.source.addEdge(self)
            self.dest.addEdge(self)

            # set item focusable
            self.setFlag(self.ItemIsFocusable)

            self.encapsulationTransform = {'ETH': 'EN10MB',
                                                            'FR': 'FRELAY',
                                                            'HDLC': 'C_HDLC',
                                                            'PPP': 'PPP_SERIAL'}

        else:
            src_rect = self.source.boundingRect()
            self.src = self.mapFromItem(self.source, src_rect.width() / 2.0, src_rect.height() / 2.0)
            self.dst = self.dest

    def adjust(self):
        """ Compute the source point and destination point
            Must be called when overloaded
        """

        self.prepareGeometryChange()
        src_rect = self.source.boundingRect()
        self.src = self.mapFromItem(self.source, src_rect.width() / 2.0, src_rect.height() / 2.0)

        # if source point is not a mouse point
        if not self.fake:
            dst_rect = self.dest.boundingRect()
            self.dst = self.mapFromItem(self.dest, dst_rect.width() / 2.0, dst_rect.height() / 2.0)

        # compute vectors
        self.dx = self.dst.x() - self.src.x()
        self.dy = self.dst.y() - self.src.y()

        # compute the length of the line
        self.length = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        self.draw = True

    def getLocalInterface(self, node):
        """ Returns the local interface of the node
        """

        if node == self.source:
            return self.srcIf
        else:
            return self.destIf

    def getConnectedNeighbor(self, node):
        """ Returns the connected neighbor's node and interface
        """

        if node == self.source:
            neighbor = (self.dest,  self.destIf)
        else:
            neighbor = (self.source,  self.srcIf)
        return neighbor

    def setCustomToolTip(self):
        """ Set a custom tool tip
        """

        self.setToolTip(unicode(translate("AbstractEdge", "Link: %s (%s) -> %s (%s)")) % (self.source.hostname, self.srcIf, self.dest.hostname, self.destIf))

    def keyReleaseEvent(self, event):
        """ Key release handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.__deleteAction()
        else:
            QtGui.QGraphicsPathItem.keyReleaseEvent(self, event)

    def mousePressEvent(self, event):
        """ Call when the edge is clicked
            event: QtGui.QGraphicsSceneMouseEvent instance
        """

        if (event.button() == QtCore.Qt.RightButton):
            if globals.addingLinkFlag:
                globals.GApp.scene.resetAddingLink()
                return
            menu = QtGui.QMenu()
            menu.addAction(QtGui.QIcon(':/icons/delete.svg'), translate("AbstractEdge", "Delete"))
            if self.capturing == True:
                menu.addAction(QtGui.QIcon(':/icons/inspect.svg'), translate("AbstractEdge", "Stop the capture"))
                menu.addAction(QtGui.QIcon(':/icons/wireshark.png'), translate("AbstractEdge", "Start Wireshark"))
            else:
                menu.addAction(QtGui.QIcon(':/icons/inspect.svg'), translate("AbstractEdge", "Capture"))
            menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.mousePressEvent_actions)
            menu.exec_(QtGui.QCursor.pos())

    def mousePressEvent_actions(self, action):
        """ Handle Menu actions
        """

        action = action.text()
        if action == translate("AbstractEdge", "Delete"):
            self.__deleteAction()
        elif action == translate("AbstractEdge", "Capture"):
            self.__captureAction()
        elif action == translate("AbstractEdge", "Stop the capture"):
            self.__stopCaptureAction()
        elif action == translate("AbstractEdge", "Start Wireshark"):
            self.__startWiresharkAction()

    def __returnCaptureOptions(self, options, hostname, dest, interface):
        """ Returns capture options (source hostname, encapsulation ...)
        """

        iftype = interface[0]
        if iftype == 'e' or iftype == 'f' or iftype == 'g':
            options.append(hostname + ' ' +  interface + ' (encapsulation:ETH)')
        elif iftype == 's' and isinstance(dest, FRSW):
            options.append(hostname + ' ' +  interface + ' (encapsulation:FR)')
        elif iftype == 's':
            options.append(hostname + ' ' +  interface + ' (encapsulation:HDLC)')
            options.append(hostname + ' ' +  interface + ' (encapsulation:PPP)')
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),
                                           translate("AbstractEdge", "Packet capture is not supported on this link type"))
            return False
        return True

    def __captureAction(self):
        """ Capture frames on the link
        """

        options = []
        if isinstance(self.source, IOSRouter):
            hostname = self.source.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname,  'utf-8')
            if not self.__returnCaptureOptions(options, hostname, self.dest, self.srcIf):
                return
        if isinstance(self.dest, IOSRouter):
            hostname = self.dest.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname,  'utf-8')
            if not self.__returnCaptureOptions(options, hostname, self.source, self.destIf):
                return

        if len(options):
            (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),
                                                          translate("AbstractEdge", "Please choose a source"), options, 0, False)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "No device available for traffic capture"))
            return

        if ok:

            (device, interface, encapsulation) = str(selection).split(' ')
            if globals.GApp.dynagen.devices[device].state != 'running':
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  unicode(translate("AbstractEdge", "Device %s is not running")) % device)
                return

            match_obj = dynagen_namespace.interface_re.search(interface)
            if match_obj:
                (inttype, slot, port) = match_obj.group(1, 2, 3)
                slot = int(slot)
                port = int(port)
            else:
                # Try checking for WIC interface specification (e.g. S1)
                match_obj = dynagen_namespace.interface_noport_re.search(interface)
                (inttype, port) = match_obj.group(1, 2)
                slot = 0

            try:
                encapsulation = encapsulation[1:-1].split(':')[1]
                encapsulation = self.encapsulationTransform[encapsulation]
                capture_conf = globals.GApp.systconf['capture']
                if capture_conf.workdir:
                    workdir = capture_conf.workdir
                else:
                    workdir = globals.GApp.dynagen.devices[device].dynamips.workingdir
                self.capfile = '"' + workdir + self.source.hostname + '_to_' + self.dest.hostname + '.cap' + '"'
                debug("Start capture in " + self.capfile)
                globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port,'capture','both', encapsulation + " " + self.capfile)
                self.captureInfo = (device, slot, inttype, port)
                self.capturing = True
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
                return
            self.__startWiresharkAction()

    def __stopCaptureAction(self):
        """ Stop capturing frames on the link
        """

        try:
            (device, slot, inttype, port) = self.captureInfo
            globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port,'none','both')
            QtGui.QMessageBox.information(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "Capture stopped"))
            self.capturing = False
            self.captureInfo = None
            self.capfile = None
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
            return

    def __startWiresharkAction(self):
        """ Start a Wireshark like tool
        """

        capture_conf = globals.GApp.systconf['capture']
        if capture_conf.auto_start:
            if capture_conf.cap_cmd == '':
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "Please configure capture options"))
                return
            try:
                path = capture_conf.cap_cmd.replace("%c", self.capfile)
                debug("Start Wireshark like application (wait 2 seconds): " + path)
                time.sleep(2)
                if sys.platform.startswith('win'):
                     sub.Popen(path)
                else:
                    sub.Popen(path, shell=True)
            except OSError, (errno, strerror):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), unicode(translate("AbstractEdge", "Cannot start %s : %s")) % (path, strerror))

    def __deleteAction(self):
        """ Delete the link
        """

        # delete one of the interface mean the edge is deleted
        self.source.deleteInterface(self.srcIf)

    def setLocalInterfaceStatus(self, node_id, status):
        """ Set the status to up/down for the node
            node_id: integer
            status: string 'up', 'down' or 'suspended'
        """

        if self.source.id == node_id:
            self.src_interface_status = status
        else:
            self.dest_interface_status = status
        self.update()

    def setMousePoint(self, scene_point):

        self.dst = scene_point
        self.adjust()
        self.update()
