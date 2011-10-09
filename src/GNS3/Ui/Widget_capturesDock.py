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
from PyQt4 import QtCore, QtGui
import GNS3.Dynagen.qemu_lib as qemu
from GNS3.Utils import translate

class capturesDock(QtGui.QTreeWidget):
    """ Class for showing the captures
        Custom QTreeWidget
    """

    def __init__(self, parent):

        QtGui.QTreeWidget.__init__(self, parent)
        self.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'),  self.slotItemClicked)

    def refresh(self):
        """ Refresh topology summary
        """

        self.clear()
        for link in globals.GApp.topology.links:

            #captureInfo
            if link.capturing:
                device = globals.GApp.dynagen.devices[link.captureInfo[0]]
                if isinstance(device, qemu.AnyEmuDevice):
                    (hostname, port) = link.captureInfo
                    port = 'e' + port
                else:
                    (hostname, slot, inttype, port) = link.captureInfo
                    if device.model_string in ['1710', '1720', '1721', '1750']:
                        port = inttype + str(port)
                    else:
                        port = inttype + str(slot) + '/' + str(port)

                item = QtGui.QTreeWidgetItem(self)
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant([hostname, port]))
                item.setText(0, hostname)
                
                if device.state == 'running':
                    item.setIcon(0, QtGui.QIcon(':/icons/led_green.svg'))
                else:
                    item.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
                    
                item.setText(1, port)
                self.insertTopLevelItem(0, item)
        
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

    def showContextualMenu(self):

        menu = QtGui.QMenu()
        stopCapture = QtGui.QAction(translate('Widget_capturesDock', 'Stop capturing'), menu)
        stopCapture.setIcon(QtGui.QIcon(':/icons/inspect.svg'))
        self.connect(stopCapture, QtCore.SIGNAL('triggered()'), self.slotStopCapture)
        startWireshark = QtGui.QAction(translate('Widget_capturesDock', 'Start Wireshark'), menu)
        startWireshark.setIcon(QtGui.QIcon(":/icons/wireshark.png"))
        self.connect(startWireshark, QtCore.SIGNAL('triggered()'), self.slotStartWireshark)
        menu.addAction(stopCapture)
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
    
    def stopAllCaptures(self):

        for link in globals.GApp.topology.links:
            link.stopCapturing()
        self.refresh()
            
    def slotStopCapture(self):

        link = self.getLink()
        if not link:
            print 'Cannot get link, please report'
            return
        link.stopCapturing()

    def slotStartWireshark(self):

        link = self.getLink()
        if not link:
            print 'Cannot get link, please report'
            return
        link.startWireshark()
     
    def slotItemClicked(self, item, column):
        
        if item:
            self.showContextualMenu()
