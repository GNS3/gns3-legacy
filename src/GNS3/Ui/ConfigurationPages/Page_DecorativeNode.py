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
from Form_DecorativeNodePage import Ui_DecorativeNodePage

class Page_DecorativeNode(QtGui.QWidget, Ui_DecorativeNodePage):
    """ Class implementing the DecorativeNode configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Decorative Node")
        
        # connect slots
        self.connect(self.pushButtonAddInterface, QtCore.SIGNAL('clicked()'), self.slotAddInterface)
        self.connect(self.pushButtonDeleteInterface, QtCore.SIGNAL('clicked()'), self.slotDeleteInterface)
        self.connect(self.listWidgetInterfaces,  QtCore.SIGNAL('itemSelectionChanged()'), self.slotInterfaceChanged)
        self.connect(self.listWidgetInterfaces,  QtCore.SIGNAL('currentRowChanged(int)'), self.slotInterfaceselected)
        
        self.interfaces = []

    def slotAddInterface(self):
        """ Add a new interface
        """
    
        interface = unicode(self.lineEditInterface.text(), 'utf-8', errors='replace')
        if interface and interface not in self.interfaces:
            self.listWidgetInterfaces.addItem(interface)
            self.interfaces.append(interface)

    def slotDeleteInterface(self):
        """ Delete a interface
        """
        
        item = self.listWidgetInterfaces.currentItem()
        if (item != None):
            interface = unicode(item.text(), 'utf-8', errors='replace')
            self.interfaces.remove(interface)
            self.listWidgetInterfaces.takeItem(self.listWidgetInterfaces.currentRow())

    def slotInterfaceChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetInterfaces.currentItem()
        if item != None:
            self.pushButtonDeleteInterface.setEnabled(True)
        else:
            self.pushButtonDeleteInterface.setEnabled(False)
            
    def slotInterfaceselected(self, index):
        """ Load a selected interface
        """
        
        item = self.listWidgetInterfaces.currentItem()
        if (item != None):
            interface = item.text()
            self.lineEditInterface.setText(interface)

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            DecorativeNodeconfig = config
        else:
            DecorativeNodeconfig  = node.config

        self.interfaces = []
        self.listWidgetInterfaces.clear()
        for interface in DecorativeNodeconfig['interfaces']:
            self.interfaces.append(interface)
            self.listWidgetInterfaces.addItem(interface)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            DecorativeNodeconfig = config
        else:
            DecorativeNodeconfig  = node.duplicate_config()

        DecorativeNodeconfig['interfaces'] = self.interfaces

        return DecorativeNodeconfig

def create(dlg):

    return  Page_DecorativeNode() 
