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

import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
import GNS3.Dynagen.qemu_lib as qemu
import GNS3.Dynagen.dynagen_vbox_lib as vboxlib
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Utils import translate

class capturesDock(QtGui.QTreeWidget):
    """ Class for showing the captures
        Custom QTreeWidget
    """

    def __init__(self, parent):

        QtGui.QTreeWidget.__init__(self, parent)
        self.stoppedLinks = {}

    def refresh(self):
        """ Refresh topology summary
        """

        self.clear()
        refreshed_stoppedLinks = {}
        for link in globals.GApp.topology.links.copy():
            if link.capturing or self.stoppedLinks.has_key(link):
                
                if self.stoppedLinks.has_key(link):
                    captureInfo = self.stoppedLinks[link]
                    refreshed_stoppedLinks[link] = captureInfo
                else:
                    captureInfo = link.captureInfo

                device = globals.GApp.dynagen.devices[captureInfo[0]]

                if isinstance(device, qemu.AnyEmuDevice):
                    (hostname, port) = captureInfo
                    port = 'e' + port
                elif isinstance(device, vboxlib.AnyVBoxEmuDevice):
                    (hostname, port) = captureInfo
                    port = 'e' + port
                else:
                    (hostname, slot, inttype, port, encapsulation) = captureInfo
                    if device.model_string in ['1710', '1720', '1721', '1750']:
                        port = inttype + str(port)
                    else:
                        port = inttype + str(slot) + '/' + str(port)

                item = QtGui.QTreeWidgetItem(self)
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant([hostname, port]))
                item.setText(0, hostname)

                if self.stoppedLinks.has_key(link) or (isinstance(device, IOSRouter) and device.state != 'running'):
                    item.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
                    if link.capturing and not self.stoppedLinks.has_key(link):
                        link.stopCapturing(showMessage=False, refresh=False)
                        refreshed_stoppedLinks[link] = captureInfo
                elif device.state != 'running':
                    item.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
                else:
                    item.setIcon(0, QtGui.QIcon(':/icons/led_green.svg'))

                item.setText(1, port)
                self.insertTopLevelItem(0, item)
        
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.stoppedLinks = refreshed_stoppedLinks

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.RightButton:
            self.showContextualMenu()
        else:
            QtGui.QTreeWidget.mousePressEvent(self, event)

    def showContextualMenu(self):

        menu = QtGui.QMenu()
        startAllCaptures = QtGui.QAction(translate('Widget_capturesDock', 'Start all captures'), menu)
        startAllCaptures.setIcon(QtGui.QIcon(":/icons/capture-start.svg"))
        self.connect(startAllCaptures, QtCore.SIGNAL('triggered()'), self.startAllCaptures)
        stopAllCaptures = QtGui.QAction(translate('Widget_capturesDock', 'Stop all captures'), menu)
        stopAllCaptures.setIcon(QtGui.QIcon(":/icons/capture-stop.svg"))
        self.connect(stopAllCaptures, QtCore.SIGNAL('triggered()'), self.stopAllCaptures)
        clearStoppedCaptures = QtGui.QAction(translate('Widget_capturesDock', 'Clear stopped captures'), menu)
        clearStoppedCaptures.setIcon(QtGui.QIcon(":/icons/edit-clear.svg"))
        self.connect(clearStoppedCaptures, QtCore.SIGNAL('triggered()'), self.clearStoppedCaptures)
        menu.addAction(startAllCaptures)
        menu.addAction(stopAllCaptures)
        menu.addAction(clearStoppedCaptures)

        curitem = self.currentItem()
        if curitem:

            menu.addSeparator()
            link = self.getLink()

            if self.stoppedLinks.has_key(link) or not link.capturing:
                startCapture = QtGui.QAction(translate('Widget_capturesDock', 'Start capturing'), menu)
                startCapture.setIcon(QtGui.QIcon(':/icons/capture-start.svg'))
                self.connect(startCapture, QtCore.SIGNAL('triggered()'), self.slotStartCapture)
                menu.addAction(startCapture)
            else:
                stopCapture = QtGui.QAction(translate('Widget_capturesDock', 'Stop capturing'), menu)
                stopCapture.setIcon(QtGui.QIcon(':/icons/capture-stop.svg'))
                self.connect(stopCapture, QtCore.SIGNAL('triggered()'), self.slotStopCapture)
                menu.addAction(stopCapture)
                startWireshark = QtGui.QAction(translate('Widget_capturesDock', 'Start Wireshark'), menu)
                startWireshark.setIcon(QtGui.QIcon(":/icons/wireshark.png"))
                self.connect(startWireshark, QtCore.SIGNAL('triggered()'), self.slotStartWireshark)
                menu.addAction(startWireshark)

        menu.exec_(QtGui.QCursor.pos())
            
    def getLink(self):
        
        item = self.currentItem()
        data = item.data(0, QtCore.Qt.UserRole).toStringList()
        hostname = unicode(data[0])
        interface = str(data[1])
        for link in globals.GApp.topology.links:
            if link.source.hostname == hostname and link.srcIf == interface:
                return link
            elif link.dest.hostname == hostname and link.destIf == interface:
                return link
        return None

    def clearStoppedCaptures(self):

        self.stoppedLinks = {}
        self.refresh()

    def stopAllCaptures(self):

        for link in globals.GApp.topology.links:
            if link.capturing:
                self.stoppedLinks[link] = link.captureInfo
                link.stopCapturing()
        self.refresh()

    def startAllCaptures(self):

        refreshed_stoppedLinks = {}
        for (link, captureInfo) in self.stoppedLinks.iteritems():
            self.startCapturing(link, captureInfo)
            if not link.capturing:
                refreshed_stoppedLinks[link] = captureInfo

        self.stoppedLinks = refreshed_stoppedLinks
        self.refresh()

    def slotStopCapture(self):

        link = self.getLink()
        # this should never happen
        assert(link)

        self.stoppedLinks[link] = link.captureInfo
        link.stopCapturing()
        #self.refresh()

    def startCapturing(self, link, captureInfo):
        
        device = globals.GApp.dynagen.devices[captureInfo[0]]
        encapsulation = None

        if isinstance(device, qemu.AnyEmuDevice):
            (hostname, port) = captureInfo
            port = 'e' + port
        elif isinstance(device, vboxlib.AnyVBoxEmuDevice):
            (hostname, port) = captureInfo
            port = 'e' + port
        else:
            (hostname, slot, inttype, port, encapsulation) = captureInfo
            if device.model_string in ['1710', '1720', '1721', '1750']:
                port = inttype + str(port)
            else:
                port = inttype + str(slot) + '/' + str(port)

        link.startCapturing(hostname, port, encapsulation)

    def slotStartCapture(self):

        link = self.getLink()
        # this should never happen
        assert(link)

        if self.stoppedLinks.has_key(link):
            captureInfo = self.stoppedLinks[link]
            del self.stoppedLinks[link]
            self.startCapturing(link, captureInfo)
        #self.refresh()

    def slotStartWireshark(self):

        link = self.getLink()

        # this should never happen
        assert(link)
        link.startWireshark()
