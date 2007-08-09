#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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

import GNS3.Ui.svg_resources_rc
import GNS3.Globals as globals 
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate

class topologySummaryDock(QtGui.QTreeWidget):
    """ Class for displaying the topology
        Custom QListWidget
    """

    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
        self.header().hide()

    def emulationMode(self):
        """ Create items for emulation mode
        """
        
        self.clear()
        self.setRootIsDecorated(True)
        for node in globals.GApp.topology.nodes.itervalues():
            rootitem = QtGui.QTreeWidgetItem(self)
            rootitem.setText(0, translate("MainWindow", node.hostname))
            #rootitem.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
    
            #TODO: finish to put the tree in emulation mode
            items = []
            for interface in node.getConnectedInterfaceList():
                item = QtGui.QTreeWidgetItem()
                neigbhor = node.getConnectedNeighbor(interface)
                item.setText(0, interface + ' is connected to ' + unicode(neigbhor[0].hostname) + ' in ' + neigbhor[1])
                items.append(item)
            rootitem.addChildren(items)
            
            #rootitem.addChild(QtGui.QTreeWidgetItem(['test']))
            self.insertTopLevelItem(0, rootitem)
