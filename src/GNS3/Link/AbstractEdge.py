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

import os, math, time, sys
import GNS3.Globals as globals
import subprocess as sub
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Dynagen.qemu_lib as qemu
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice
from GNS3.Node.FRSW import FRSW

class AbstractEdge(QtGui.QGraphicsPathItem, QtCore.QObject):
    """ AbstractEdge class
        Base class to create edges between nodes
    """

    def __init__(self, sourceNode, sourceIf, destNode, destIf, Fake = False, Multi = 0):

        QtGui.QGraphicsItem.__init__(self)

        # status points size
        self.pointSize = 10
        # default pen size
        self.penWidth = 2.0

        self.srcCollisionOffset = 0.0
        self.dstCollisionOffset = 0.0
                
        self.source = sourceNode
        self.dest = destNode
        self.fake = Fake
        self.multi = Multi

        self.setZValue(-1)

        if not self.fake:

            self.source.setCustomToolTip()
            self.dest.setCustomToolTip()
    
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

            self.encapsulationTransform = { 'ETH': 'EN10MB',
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
        
        # multi-links management
        if not self.fake and self.multi:
            angle = math.radians(90)
            self.dxrot = math.cos(angle) * self.dx - math.sin(angle) *  self.dy
            self.dyrot = math.sin(angle) * self.dx + math.cos(angle) * self.dy
            offset = QtCore.QPointF((self.dxrot * (self.multi * 5)) / self.length, (self.dyrot * (self.multi * 5)) / self.length)
            self.src = QtCore.QPointF(self.src + offset)
            self.dst = QtCore.QPointF(self.dst + offset)

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
            if self.fake:
                return
            menu = QtGui.QMenu()
            if self.capturing == True:
                menu.addAction(QtGui.QIcon(':/icons/inspect.svg'), translate("AbstractEdge", "Stop capturing"))
                menu.addAction(QtGui.QIcon(':/icons/wireshark.png'), translate("AbstractEdge", "Start Wireshark"))
            else:
                menu.addAction(QtGui.QIcon(':/icons/inspect.svg'), translate("AbstractEdge", "Capture"))
            menu.addAction(QtGui.QIcon(':/icons/delete.svg'), translate("AbstractEdge", "Delete"))
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
        elif action == translate("AbstractEdge", "Stop capturing"):
            self.__stopCaptureAction()
        elif action == translate("AbstractEdge", "Start Wireshark"):
            self.__startWiresharkAction()

    def __returnCaptureOptions(self, options, hostname, dest, interface):
        """ Returns capture options (source hostname, encapsulation ...)
        """

        iftype = interface[0]
        if iftype == 'e' or iftype == 'f' or iftype == 'g':
            options.append(hostname + ' ' +  interface + ' (encapsulation:ETH)')
        elif iftype == 's':
            options.append(hostname + ' ' +  interface + ' (encapsulation:HDLC)')
            options.append(hostname + ' ' +  interface + ' (encapsulation:PPP)')
            options.append(hostname + ' ' +  interface + ' (encapsulation:FR)')
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),
                                           translate("AbstractEdge", "Packet capture is not supported on this link type"))
            return False
        return True

    def __captureAction(self):
        """ Capture frames on the link
        """

        options = []
        if isinstance(self.source, IOSRouter) or isinstance(self.source, AnyEmuDevice):
            hostname = self.source.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname)
            if not self.__returnCaptureOptions(options, hostname, self.dest, self.srcIf):
                return
        if isinstance(self.dest, IOSRouter) or isinstance(self.dest, AnyEmuDevice):
            hostname = self.dest.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname)
            if not self.__returnCaptureOptions(options, hostname, self.source, self.destIf):
                return

        if len(options):
            (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),
                                                          translate("AbstractEdge", "Please choose a source"), options, 0, False)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "No device available for traffic capture"))
            return

        if ok:
            
            (device, interface, encapsulation) = unicode(selection).split(' ')
            if isinstance(globals.GApp.dynagen.devices[device], qemu.AnyEmuDevice):
                if globals.GApp.dynagen.devices[device].state == 'running':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  unicode(translate("AbstractEdge", "Device %s must be restarted to start capturing traffic")) % device)    
                self.__captureQemuDevice(device, interface)
            else:
                if globals.GApp.dynagen.devices[device].state != 'running':
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  unicode(translate("AbstractEdge", "Device %s is not running")) % device)
                    return
                self.__captureDynamipsDevice(device, interface, encapsulation)
        
        globals.GApp.mainWindow.capturesDock.refresh()

    def __captureQemuDevice(self, device, interface):
        """ Capture for Qemu based devices
        """

        host = globals.GApp.dynagen.devices[device].dynamips.host
        match_obj = dynagen_namespace. qemu_int_re.search(interface)
        if not match_obj:
            debug("Cannot parse interface " + interface)
            return
        port = match_obj.group(2)
        
        capture_conf = globals.GApp.systconf['capture']
        if capture_conf.workdir and (host == globals.GApp.systconf['qemu'].QemuManager_binding or host == 'localhost'):
            workdir = capture_conf.workdir
        else:
            workdir = globals.GApp.dynagen.devices[device].dynamips.workingdir
        if '/' in workdir:
            sep = '/'
        else:
            sep = '\\'
        self.capfile = unicode(workdir + sep + self.source.hostname + '_to_' + self.dest.hostname + '.cap')
        debug("Start capture to " + self.capfile)
        
        globals.GApp.dynagen.devices[device].capture(int(port), self.capfile)
        self.captureInfo = (device, port)
        self.capturing = True
        debug("Capturing to " + self.capfile)

    def __captureDynamipsDevice(self, device, interface, encapsulation):
        """ Capture for Dynamips based devices
        """
        
        host = globals.GApp.dynagen.devices[device].dynamips.host

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

            if capture_conf.workdir and (host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or host == 'localhost'):
                workdir = capture_conf.workdir
            else:
                workdir = globals.GApp.dynagen.devices[device].dynamips.workingdir
            if '/' in workdir:
                sep = '/'
            else:
                sep = '\\'
            self.capfile = unicode(workdir + sep + self.source.hostname + '_to_' + self.dest.hostname + '.cap')
            debug("Start capture to " + self.capfile)
            globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port,'capture','both', encapsulation + " " + '"' + self.capfile + '"')
            self.captureInfo = (device, slot, inttype, port)
            self.capturing = True
            debug("Capturing to " + self.capfile)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
            return
        capture_conf = globals.GApp.systconf['capture']
        if capture_conf.auto_start and (host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or host == 'localhost'):
            time.sleep(2)
            self.__startWiresharkAction()

    def stopCapturing(self, showMessage=True):

        if self.capturing:
            self.__stopCaptureAction(showMessage)

    def __stopCaptureAction(self, showMessage=True):
        """ Stop capturing frames on the link
        """

        try:
            if isinstance(globals.GApp.dynagen.devices[self.captureInfo[0]], qemu.AnyEmuDevice):
                (device, port) = self.captureInfo

                if showMessage and globals.GApp.dynagen.devices[device].state == 'running':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  unicode(translate("AbstractEdge", "Device %s must be stopped to stop capturing traffic")) % device) 

                # empty string means stop capturing traffic
                globals.GApp.dynagen.devices[device].capture(int(port), '')
    
            else:
                (device, slot, inttype, port) = self.captureInfo
                globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port, 'none', 'both')

            self.capturing = False
            self.captureInfo = None
            self.capfile = None
        except lib.DynamipsError, msg:
            if showMessage:
                QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
            return

        globals.GApp.mainWindow.capturesDock.refresh()

    def startWireshark(self):
        
        self.__startWiresharkAction()

    def __startWiresharkAction(self):
        """ Start a Wireshark like tool
        """

        capture_conf = globals.GApp.systconf['capture']
        if capture_conf.cap_cmd == '':
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "Please configure capture options"))
            return

        try:
            statinfo = os.stat(self.capfile)
            if not statinfo.st_size:
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  
                                            unicode(translate("AbstractEdge",  "%s is empty, no traffic captured on the link. Try again later")) % self.capfile)
                return
        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), unicode(translate("AbstractEdge", "Cannot find %s : %s")) % (self.capfile, e.strerror))
            return

        try:
            path = unicode(capture_conf.cap_cmd.replace("%c", '"%s"')) % self.capfile
            debug("Start Wireshark like application: " + path)
            if sys.platform.startswith('win'):
                sub.Popen(path)
            else:
                sub.Popen(path, shell=True)
        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), unicode(translate("AbstractEdge", "Cannot start %s : %s")) % (path, e.strerror))

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
