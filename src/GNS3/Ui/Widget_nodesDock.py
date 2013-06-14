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

from PyQt4 import QtCore, QtGui
import GNS3.Globals as globals
from GNS3.Utils import translate
from GNS3.Globals.Symbols import SYMBOLS
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Node.AnyEmuDevice import QemuDevice, PIX, ASA, AWP, JunOS, IDS
from GNS3.Node.AnyVBoxEmuDevice import VBoxDevice

class nodesDock(QtGui.QTreeWidget):
    """ Class for managing the node types list
        Custom QTreeWidget
    """

    def __init__(self, parent):

        QtGui.QTreeWidget.__init__(self, parent)
        self.header().hide()

    def populateNodeDock(self, nodeType):
        """ Fill the node dock
        """

        self.clear()
        count = 0
        for symbol in SYMBOLS:
            if nodeType != 'All devices' and (not symbol.has_key('type') or symbol['type'] != nodeType):
                count += 1
                continue
            item = QtGui.QTreeWidgetItem(self, 1000 + count)
            if symbol['translated']:
                item.setText(0, translate("nodesDock", symbol['name']))
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(symbol['name']))
            else:
                item.setText(0, symbol['name'])
            item.setIcon(0, QtGui.QIcon(symbol['normal_svg_file']))
            count += 1
            
            self.checkImageAvailability(item, symbol)

    def checkImageAvailability(self, item, symbol):
        """ Checks if the image of the associated device is registered/configured,
             and if not disable it graphically so it can't be drag & drop'ed """

        node = symbol['object']
        item.setDisabled(symbol.has_key('checkForImage') and symbol['checkForImage'])

        # Check if an IOS image is registered
        if issubclass(node, IOSRouter):
            if len(globals.GApp.iosimages.keys()) == 0:
                return
            # Check availability of each Cisco platform's image individually
            for (image, conf) in globals.GApp.iosimages.iteritems():
                # Special check for EtherSwitch router
                if conf.platform in 'c3700' and symbol['name'] == 'EtherSwitch router':
                    item.setDisabled(False)
                    return
                if conf.platform in symbol['name']:
                    item.setDisabled(False)
                    return
        # Check if a JunOS image is registered
        elif issubclass(node, JunOS) and len(globals.GApp.junosimages) != 0:
            item.setDisabled(False)
        # Check availability for firewall and IDS images
        elif issubclass(node, ASA) and len(globals.GApp.asaimages) != 0:
            item.setDisabled(False)
        elif issubclass(node, AWP) and len(globals.GApp.awprouterimages) != 0:
            item.setDisabled(False)
        elif issubclass(node, PIX) and len(globals.GApp.piximages) != 0:
            item.setDisabled(False)
        elif issubclass(node, IDS) and len(globals.GApp.idsimages) != 0:
            item.setDisabled(False)
        # Check if an image for Qemu or VirtualBox is registered
        elif issubclass(node, QemuDevice) and len(globals.GApp.qemuimages) != 0:
            item.setDisabled(False)
        elif issubclass(node, VBoxDevice) and len(globals.GApp.vboximages) != 0:
            item.setDisabled(False)
        # No need to register an image for a "Host" so enable it
        elif symbol['name'] == 'Host':
            item.setDisabled(False)

    def mouseMoveEvent(self, event):
        """ Drag event
        """

        if ((event.buttons() & QtCore.Qt.LeftButton ) == None
            or self.currentItem() == None):
            return

        item = self.currentItem()
        if not item.type():
            return

        drag = QtGui.QDrag(self)
        mimedata = QtCore.QMimeData()

        # Deduce item name from its CustomType
        mimedata.setText(SYMBOLS[item.type()-1000]['name'])
        iconeSize = self.iconSize()
        icone = item.icon(0)
        drag.setMimeData(mimedata)
        drag.setHotSpot(QtCore.QPoint(iconeSize.width(), iconeSize.height()))
        drag.setPixmap(icone.pixmap(iconeSize))
        drag.start(QtCore.Qt.MoveAction)

    def retranslateItem(self, item):

        # Translate current item
        data = str(item.data(0, QtCore.Qt.UserRole).toString())
        if data:
            item.setText(0, translate('nodesDock', data))

            # Recurse for child-items translation
            childNum = 0
            childCount = item.childCount()
            while childNum < childCount:
                child_item = item.child(childNum)
                self.retranslateItem(child_item)
                childNum += 1

    def retranslateUi(self, MainWindow):

        self.populateNodeDock()
        return
