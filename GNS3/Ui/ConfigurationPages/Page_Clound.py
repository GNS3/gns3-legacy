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
from PyQt4 import QtCore,  QtGui
from Form_CloundPage import Ui_CloundPage

class Page_Clound(QtGui.QWidget, Ui_CloundPage):
    """
    Class implementing the Clound configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Clound")
        
        self.connect(self.pushButtonAddGenericEth, QtCore.SIGNAL('clicked()'), self.slotAddGenEth)
        self.connect(self.pushButtonDeleteGenericEth, QtCore.SIGNAL('clicked()'), self.slotDeleteGenEth)
        self.connect(self.listWidgetGenericEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotGenEthChanged)
        self.connect(self.pushButtonAddLinuxEth, QtCore.SIGNAL('clicked()'), self.slotAddLinuxEth)
        self.connect(self.pushButtonDeleteLinuxEth, QtCore.SIGNAL('clicked()'), self.slotDeleteLinuxEth)
        self.connect(self.listWidgetLinuxEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotLinuxEthChanged)
        self.nios = []
        
        # to test ...
        self.comboBoxGenEth.addItems(['eth0',  'eth1',  'eth2'])
        self.comboBoxLinuxEth.addItems(['eth0',  'eth1',  'eth2'])

    def slotGenEthChanged(self):

        item = self.listWidgetGenericEth.currentItem()
        if item != None:
            self.pushButtonDeleteGenericEth.setEnabled(True)
        else:
            self.pushButtonDeleteGenericEth.setEnabled(False)
        
    def slotAddGenEth(self):
    
        interface = str(self.comboBoxGenEth.currentText())
        if interface:
            nio = 'NIO_gen_eth:' + interface
            if not nio in self.nios:
                self.listWidgetGenericEth.addItem(nio)
                self.nios.append(nio)
        
    def slotDeleteGenEth(self):
    
        item = self.listWidgetGenericEth.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetGenericEth.takeItem(self.listWidgetGenericEth.currentRow())
            
    def slotLinuxEthChanged(self):

        item = self.listWidgetLinuxEth.currentItem()
        if item != None:
            self.pushButtonDeleteLinuxEth.setEnabled(True)
        else:
            self.pushButtonDeleteLinuxEth.setEnabled(False)
        
    def slotAddLinuxEth(self):
    
        interface = str(self.comboBoxLinuxEth.currentText())
        if interface:
            nio = 'NIO_linux_eth:' + interface
            if not nio in self.nios:
                self.listWidgetLinuxEth.addItem(nio)
                self.nios.append(nio)
        
    def slotDeleteLinuxEth(self):
    
        item = self.listWidgetLinuxEth.currentItem()
        if (item != None):
            nio = str(item.text())
            self.nios.remove(nio)
            self.listWidgetLinuxEth.takeItem (self.listWidgetLinuxEth.currentRow())

    def loadConfig(self,  id,  config = None):

        node = globals.GApp.topology.getNode(id)
        if config:
            Cloundconfig = config
        else:
            Cloundconfig  = node.config
            
        self.nios = []
        self.listWidgetGenericEth.clear()
        self.listWidgetLinuxEth.clear()
        for nio in Cloundconfig.nios:
            (niotype,  niostring) = nio.split(':')
            if niotype == 'NIO_gen_eth':
                self.listWidgetGenericEth.addItem(nio)
                self.nios.append(nio)
            elif niotype == 'NIO_linux_eth':
                self.listWidgetLinuxEth.addItem(nio)
                self.nios.append(nio)
            
    def saveConfig(self, id, config = None):

        node = globals.GApp.topology.getNode(id)
        if config:
            Cloundconfig = config
        else:
            Cloundconfig  = node.config

        Cloundconfig.nios = self.nios
            
def create(dlg):

    return  Page_Clound()
