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

import os, math, time, sys
import GNS3.Globals as globals
import subprocess as sub
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.dynagen as dynagen_namespace
import GNS3.Dynagen.qemu_lib as qemu
import GNS3.Dynagen.dynagen_vbox_lib as vboxlib
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import AnyEmuDevice, PIX
from GNS3.Node.AnyVBoxEmuDevice import AnyVBoxEmuDevice
from GNS3.Node.DecorativeNode import DecorativeNode
from GNS3.Node.FRSW import FRSW
from GNS3.Node.Cloud import Cloud
from PipeCapture import PipeCapture
from __main__ import GNS3_RUN_PATH

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

            # links must always be below nodes
            min_zvalue = min([sourceNode.zValue(), destNode.zValue()])
            self.setZValue(min_zvalue - 1)

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
            self.tailProcess = None
            self.capturePipeThread = None

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
        if not self.fake and self.multi and self.length:
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

        self.setToolTip(translate("AbstractEdge", "Link: %s (%s) -> %s (%s)") % (self.source.hostname, self.srcIf, self.dest.hostname, self.destIf))

    def keyReleaseEvent(self, event):
        """ Key release handler
        """

        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            self.__deleteAction()
        else:
            QtGui.QGraphicsPathItem.keyReleaseEvent(self, event)

    def addLinkActionsToMenu(self, menu):
        """ Populate contextual menu
        """

        if self.capturing == True:
            menu.addAction(QtGui.QIcon(':/icons/capture-stop.svg'), translate("AbstractEdge", "Stop capturing"))
            menu.addAction(QtGui.QIcon(':/icons/wireshark.png'), translate("AbstractEdge", "Start Wireshark"))
        else:
            menu.addAction(QtGui.QIcon(':/icons/capture-start.svg'), translate("AbstractEdge", "Start capturing"))
        menu.addAction(QtGui.QIcon(':/icons/delete.svg'), translate("AbstractEdge", "Delete"))
        menu.connect(menu, QtCore.SIGNAL("triggered(QAction *)"), self.mousePressEvent_actions)

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
            self.addLinkActionsToMenu(menu)
            menu.exec_(QtGui.QCursor.pos())

    def mousePressEvent_actions(self, action):
        """ Handle Menu actions
        """

        action = action.text()
        if action == translate("AbstractEdge", "Delete"):
            self.__deleteAction()
        elif action == translate("AbstractEdge", "Start capturing"):
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

    def startCapture(self):

        self.__captureAction()

    def __captureAction(self):
        """ Capture frames on the link
        """

        options = []
        if isinstance(self.source, IOSRouter) or (isinstance(self.source, AnyEmuDevice) and not isinstance(self.source, PIX)) or isinstance(self.source, AnyVBoxEmuDevice):
            hostname = self.source.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname)
            if not self.__returnCaptureOptions(options, hostname, self.dest, self.srcIf):
                return
        if isinstance(self.dest, IOSRouter) or (isinstance(self.dest, AnyEmuDevice) and not isinstance(self.dest, PIX)) or isinstance(self.dest, AnyVBoxEmuDevice):
            hostname = self.dest.hostname
            if type(hostname) != unicode:
                hostname = unicode(hostname)
            if not self.__returnCaptureOptions(options, hostname, self.source, self.destIf):
                return

        # don't capture if there is a connection to a decorative node
        if isinstance(self.source, DecorativeNode) or isinstance(self.dest, DecorativeNode):
            options = []

        if len(options):
            (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),
                                                          translate("AbstractEdge", "Please choose a source"), options, 0, False)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"),  translate("AbstractEdge", "No device available for traffic capture"))
            return

        if ok:

            (device, interface, encapsulation) = unicode(selection).split(' ')
            if isinstance(globals.GApp.dynagen.devices[device], qemu.AnyEmuDevice):
                if globals.GApp.dynagen.devices[device].state != 'stopped':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s must be restarted to start capturing traffic") % device)
                self.__captureQemuDevice(device, interface)
            elif isinstance(globals.GApp.dynagen.devices[device], vboxlib.AnyVBoxEmuDevice):
                if globals.GApp.dynagen.devices[device].state != 'stopped':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s must be restarted to start capturing traffic") % device)
                self.__captureVBoxDevice(device, interface)
            else:
                if globals.GApp.dynagen.devices[device].state != 'running':
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s is not running") % device)
                    return
                self.__captureDynamipsDevice(device, interface, encapsulation)

        globals.GApp.mainWindow.capturesDock.refresh()

    def isLocalhost(self, i_host):
        if i_host == 'localhost' or i_host == '127.0.0.1' or i_host == '::1' or i_host == "0:0:0:0:0:0:0:1":
            return True
        else:
            return False

    def startCapturing(self, device, interface, encapsulation):

        if not self.capturing:
            if isinstance(globals.GApp.dynagen.devices[device], qemu.AnyEmuDevice):
                if globals.GApp.dynagen.devices[device].state != 'stopped':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s must be restarted to start capturing traffic") % device)
                self.__captureQemuDevice(device, interface)
            elif isinstance(globals.GApp.dynagen.devices[device], vboxlib.AnyVBoxEmuDevice):
                if globals.GApp.dynagen.devices[device].state != 'stopped':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s must be restarted to start capturing traffic") % device)
                self.__captureVBoxDevice(device, interface)
            else:
                if globals.GApp.dynagen.devices[device].state != 'running':
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s is not running") % device)
                    return
                self.__captureDynamipsDevice(device, interface, encapsulation)

        globals.GApp.mainWindow.capturesDock.refresh()

    def __srcIfToPath(self):

        if sys.platform.startswith('win') and isinstance(self.source, Cloud):
            return self.srcIf.split(':', 1)[0]
        else:
            return self.srcIf.replace('/', '')

    def __destIfToPath(self):

        if sys.platform.startswith('win') and isinstance(self.dest, Cloud):
            return self.destIf.split(':', 1)[0]
        else:
            return self.destIf.replace('/', '')

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

        if capture_conf.workdir and (host == globals.GApp.systconf['qemu'].QemuManager_binding or self.isLocalhost(host)):
            # We only provide capture directory to locally running wrappers.
            if globals.GApp.workspace.saveCaptures and globals.GApp.workspace.projectFile:
                capture_dir = os.path.dirname(globals.GApp.workspace.projectFile) + os.sep + 'captures'
                self.capfile = unicode(capture_dir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '_' + time.strftime("%d%m%y_%H%M%S") + '.cap')
            else:
                self.capfile = unicode(capture_conf.workdir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')
        else:
            # Remote hypervisor should setup it's own work dir, when user is starting wrapper.
            self.capfile = unicode(self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')

        debug("Start capture to " + self.capfile)
        globals.GApp.dynagen.devices[device].capture(int(port), self.capfile)
        self.captureInfo = (device, port)
        self.capturing = True
        debug("Capturing to " + self.capfile)

    def __captureVBoxDevice(self, device, interface):
        """ Capture for VBox based devices
        """

        host = globals.GApp.dynagen.devices[device].dynamips.host
        match_obj = dynagen_namespace. vbox_int_re.search(interface)
        if not match_obj:
            debug("Cannot parse interface " + interface)
            return
        port = match_obj.group(2)

        capture_conf = globals.GApp.systconf['capture']

        if capture_conf.workdir and (host == globals.GApp.systconf['vbox'].VBoxManager_binding or self.isLocalhost(host)):
            # We only provide capture directory to locally running wrappers.
            if globals.GApp.workspace.saveCaptures and globals.GApp.workspace.projectFile:
                capture_dir = os.path.dirname(globals.GApp.workspace.projectFile) + os.sep + 'captures'
                self.capfile = unicode(capture_dir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '_' + time.strftime("%d%m%y_%H%M%S") + '.cap')
            else:
                self.capfile = unicode(capture_conf.workdir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')
        else:
            # Remote hypervisor should setup it's own work dir, when user is starting wrapper.
            self.capfile = unicode(self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')
        #"""
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
            original_encapsulation = encapsulation
            encapsulation = encapsulation[1:-1].split(':')[1]
            encapsulation = self.encapsulationTransform[encapsulation]
            capture_conf = globals.GApp.systconf['capture']

            if capture_conf.workdir and (host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or self.isLocalhost(host)):
                if globals.GApp.workspace.saveCaptures and globals.GApp.workspace.projectFile:
                    capture_dir = os.path.dirname(globals.GApp.workspace.projectFile) + os.sep + 'captures'
                    self.capfile = unicode(capture_dir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '_' + time.strftime("%d%m%y_%H%M%S") + '.cap')
                else:
                    self.capfile = unicode(capture_conf.workdir + os.sep + self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')
            else:
                # Remote hypervisor should setup it's own work dir, when user is starting wrapper.
                self.capfile = unicode(self.source.hostname + '_' + self.__srcIfToPath() + '_to_' + self.dest.hostname + '_' + self.__destIfToPath() + '.cap')

            debug("Start capture to " + self.capfile)
            globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port,'capture','both', encapsulation + " " + '"' + self.capfile + '"')
            self.captureInfo = (device, slot, inttype, port, original_encapsulation)
            self.capturing = True
            debug("Capturing to " + self.capfile)
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
            return
        capture_conf = globals.GApp.systconf['capture']
        if capture_conf.auto_start and (host == globals.GApp.systconf['dynamips'].HypervisorManager_binding or host == 'localhost'):
            self.__startWiresharkAction()

    def stopCapturing(self, showMessage=True, refresh=True):

        if self.capturing:
            self.__stopCaptureAction(showMessage, refresh)

    def __stopCaptureAction(self, showMessage=True, refresh=True):
        """ Stop capturing frames on the link
        """

        try:
            if isinstance(globals.GApp.dynagen.devices[self.captureInfo[0]], qemu.AnyEmuDevice) or isinstance(globals.GApp.dynagen.devices[self.captureInfo[0]], vboxlib.AnyVBoxEmuDevice):
                (device, port) = self.captureInfo

                if showMessage and globals.GApp.dynagen.devices[device].state != 'stopped':
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Device %s must be stopped to stop capturing traffic") % device)

                # empty string means stop capturing traffic
                globals.GApp.dynagen.devices[device].capture(int(port), '')

            else:
                (device, slot, inttype, port, encapsulation) = self.captureInfo
                globals.GApp.dynagen.devices[device].slot[slot].filter(inttype, port, 'none', 'both')

            self.capturing = False
            self.captureInfo = None
            self.capfile = None

            if self.capturePipeThread:
                self.capturePipeThread.quit()
                self.capturePipeThread = None

            if self.tailProcess:
                try:
                    debug("Killing tail %i" % self.tailProcess.pid)
                    self.tailProcess.kill()
                except:
                    pass
                self.tailProcess = None

        except lib.DynamipsError, msg:
            if showMessage:
                QtGui.QMessageBox.critical(self, translate("AbstractEdge", "Dynamips error"),  unicode(msg))
            return

        if refresh:
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
            if not capture_conf.cap_cmd.__contains__('tail'):
                # leave some time for packets to have a chance to be recorded into the capture file
                time.sleep(2)
                statinfo = os.stat(self.capfile)
                if not statinfo.st_size:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge",  "%s is empty, no traffic has been captured on the link yet. Please try again later") % self.capfile)
                    return
        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Cannot find %s : %s") % (self.capfile, e.strerror) + os.linesep + translate("AbstractEdge", "NOTE: This feature is only available for local hypervisors."))
            return

        try:
            if capture_conf.cap_cmd.__contains__("%c"):
                path = unicode(capture_conf.cap_cmd.replace("%c", '"%s"')) % self.capfile
            else:
                path = capture_conf.cap_cmd
            debug("Start Wireshark-like application: %s" % path)
            shell = False
            if not sys.platform.startswith('win'):
                # start commands using the shell on all platforms but Windows
                shell = True

            if path.__contains__('|'):
                # Live Traffic Capture
                commands = path.split('|', 1)
                env = None
                info = None
                if sys.platform.startswith('win') and sys.version_info >= (2, 7):
                    # hide tail.exe window (requires python 2.7)
                    info = sub.STARTUPINFO()
                    info.dwFlags |= sub.STARTF_USESHOWWINDOW
                    info.wShowWindow = sub.SW_HIDE
                    env = {"PATH": GNS3_RUN_PATH} # for Popen to find tail.exe
                self.tailProcess = sub.Popen(commands[0].strip(), startupinfo=info, stdout=sub.PIPE, env=env, shell=shell)
                sub.Popen(commands[1].strip(), stdin=self.tailProcess.stdout, stdout=sub.PIPE, shell=shell)
                self.tailProcess.stdout.close()
            elif path.__contains__('%p'):
                    if self.capturePipeThread and self.capturePipeThread.isRunning():
                        print QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Please close Wireshark"))
                        return
                    self.capturePipeThread = None
                    pipe = r"\\.\pipe\GNS3\%s_%s_to_%s_%s" % (self.source.hostname, self.__srcIfToPath(), self.dest.hostname, self.__destIfToPath())
                    path = path.replace("%p", "%s") % pipe
                    self.capturePipeThread = PipeCapture(self.capfile, path, pipe)
                    self.capturePipeThread.start()
            else:
                # Traditional Traffic Capture
                sub.Popen(path.strip(), shell=shell)

        except (OSError, IOError), e:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("AbstractEdge", "Capture"), translate("AbstractEdge", "Cannot start %s : %s") % (path, e.strerror))

    def __deleteAction(self):
        """ Delete the link
        """

        self.stopCapturing(showMessage=False, refresh=True)
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
