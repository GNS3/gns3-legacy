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

import GNS3.Globals as globals 
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate

class topologySummaryDock(QtGui.QTreeWidget):
    """ Class for displaying the topology
        Custom QTreeWidget
    """

    def __init__(self, parent):
    
        QtGui.QTreeWidget.__init__(self, parent)
        self.header().hide()
        self.setRootIsDecorated(True)

    def emulationMode(self):
        """ Create items for emulation mode
        """
        
        self.clear()
        for node in globals.GApp.topology.nodes.itervalues():
            rootitem = QtGui.QTreeWidgetItem(self)
            rootitem.setText(0, node.hostname)
            rootitem.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
    
            items = []
            for interface in node.getConnectedInterfaceList():
                item = QtGui.QTreeWidgetItem()
                neighbor = node.getConnectedNeighbor(interface)
                list = QtCore.QStringList()
                list.append(interface)
                list.append(neighbor[0].hostname)
                list.append(neighbor[1])
                item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(list))
                newText = unicode(translate('topologySummaryDock', '%s is connected to %s %s')) \
                            % (interface, neighbor[0].hostname, neighbor[1])
                item.setText(0, newText)
                items.append(item)
            rootitem.addChildren(items)
            self.insertTopLevelItem(0, rootitem)

    def changeNodeStatus(self, hostname, status):
        """ Change the status of a node
            status: string 'running', 'stopped' or 'suspended'
        """    

        items = self.findItems (hostname, QtCore.Qt.MatchFixedString)
        if len(items):
            item = items[0]
            if status == 'running':
                item.setIcon(0, QtGui.QIcon(':/icons/led_green.svg'))
            elif status == 'suspended':
                item.setIcon(0, QtGui.QIcon(':/icons/led_yellow.svg'))
            else:
                item.setIcon(0, QtGui.QIcon(':/icons/led_red.svg'))
            
    def retranslateItem(self, item):
        # Translate current item
        data = item.data(0, QtCore.Qt.UserRole).toStringList()

        if data.count() == 3:
            newText = unicode(translate('topologySummaryDock', '%s is connected to %s %s')) \
                        % (unicode(data[0]), unicode(data[1]), unicode(data[2]))
            item.setText(0, newText)

        # Recurse for child-items translation
        childNum = 0
        childCount = item.childCount()
        while childNum < childCount:
            child_item = item.child(childNum)
            self.retranslateItem(child_item)
            childNum += 1

    def retranslateUi(self, MainWindow):
        topItemNum = 0
        topItemsCount = self.topLevelItemCount()
        while topItemNum < topItemsCount:
            topItem = self.topLevelItem(topItemNum)
            self.retranslateItem(topItem)
            topItemNum += 1
