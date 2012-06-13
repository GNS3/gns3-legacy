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

import re, sys
import GNS3.Globals as globals
from GNS3.Utils import translate, getWindowsInterfaces
from PyQt4 import QtCore, QtGui, QtNetwork
from Form_CloudPage import Ui_CloudPage

class Page_Cloud(QtGui.QWidget, Ui_CloudPage):
    """ Class implementing the Cloud configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Cloud")
            
        # connect slots
        self.connect(self.pushButtonAddGenericEth, QtCore.SIGNAL('clicked()'), self.slotAddGenEth)
        self.connect(self.pushButtonDeleteGenericEth, QtCore.SIGNAL('clicked()'), self.slotDeleteGenEth)
        self.connect(self.listWidgetGenericEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotGenEthChanged)
        self.connect(self.pushButtonAddLinuxEth, QtCore.SIGNAL('clicked()'), self.slotAddLinuxEth)
        self.connect(self.pushButtonDeleteLinuxEth, QtCore.SIGNAL('clicked()'), self.slotDeleteLinuxEth)
        self.connect(self.listWidgetLinuxEth,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotLinuxEthChanged)
        self.connect(self.comboBoxGenEth, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedGenEth)
        self.connect(self.comboBoxLinuxEth, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedLinuxEth)
        self.connect(self.pushButtonAddUDP, QtCore.SIGNAL('clicked()'), self.slotAddUDP)
        self.connect(self.pushButtonDeleteUDP, QtCore.SIGNAL('clicked()'), self.slotDeleteUDP)
        self.connect(self.listWidgetUDP,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotUDPChanged)
        self.connect(self.listWidgetUDP,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotUDPselected)
        self.connect(self.pushButtonAddTAP, QtCore.SIGNAL('clicked()'), self.slotAddTAP)
        self.connect(self.pushButtonDeleteTAP, QtCore.SIGNAL('clicked()'), self.slotDeleteTAP)
        self.connect(self.listWidgetTAP,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotTAPChanged)
        self.connect(self.pushButtonAddUNIX, QtCore.SIGNAL('clicked()'), self.slotAddUNIX)
        self.connect(self.pushButtonDeleteUNIX, QtCore.SIGNAL('clicked()'), self.slotDeleteUNIX)
        self.connect(self.listWidgetUNIX,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotUNIXChanged)
        self.connect(self.listWidgetUNIX,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotUNIXselected)
        self.connect(self.pushButtonAddVDE, QtCore.SIGNAL('clicked()'), self.slotAddVDE)
        self.connect(self.pushButtonDeleteVDE, QtCore.SIGNAL('clicked()'), self.slotDeleteVDE)
        self.connect(self.listWidgetVDE,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotVDEChanged)
        self.connect(self.listWidgetVDE,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotVDEselected)
        self.connect(self.pushButtonAddNull, QtCore.SIGNAL('clicked()'), self.slotAddNull)
        self.connect(self.pushButtonDeleteNull, QtCore.SIGNAL('clicked()'), self.slotDeleteNull)
        self.connect(self.listWidgetNull,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotNullChanged)
        self.connect(self.listWidgetNull,  QtCore.SIGNAL('currentRowChanged(int)'),  self.slotNullselected)
        
        self.nios = []
        self.rpcap_mapping = {}

        if sys.platform.startswith('win'):
            interfaces = getWindowsInterfaces()
        else:
            interfaces = map(lambda interface: interface.name(), QtNetwork.QNetworkInterface.allInterfaces())
            self.comboBoxLinuxEth.addItems(interfaces)

        self.comboBoxGenEth.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBoxGenEth.addItems(interfaces)

    def slotSelectedGenEth(self,  index):
        """ Load the selected generic interface in lineEdit
        """

        self.lineEditGenEth.setText(self.comboBoxGenEth.currentText())
        
    def slotSelectedLinuxEth(self,  index):
        """ Load the selected linux interface in lineEdit
        """

        self.lineEditLinuxEth.setText(self.comboBoxLinuxEth.currentText())
        
    def slotGenEthChanged(self):
        """ Enable the use of the delete button
        """

        item = self.listWidgetGenericEth.currentItem()
        if item != None:
            self.pushButtonDeleteGenericEth.setEnabled(True)
        else:
            self.pushButtonDeleteGenericEth.setEnabled(False)

    def slotAddGenEth(self):
        """ Add a new generic Ethernet NIO
        """

        interface = unicode(self.lineEditGenEth.text(), 'utf-8', errors='replace')
        if interface:
            if sys.platform.startswith('win'):
                match = re.search(r"""^rpcap://(\\Device\\NPF_{[a-fA-F0-9\-]*})(.*)""", interface)
                interface = match.group(1)
            nio = 'nio_gen_eth:' + interface.lower()
            if not nio in self.nios:
                self.listWidgetGenericEth.addItem(nio)
                self.nios.append(nio)
                if sys.platform.startswith('win'):
                    name_match = re.search(r"""^\ :.*:\ (.+)""", match.group(2))
                    if name_match:
                        interface_name = name_match.group(1)
                    else:
                        # The interface name could not be found, let's use the interface model instead
                        model_match = re.search(r"""^\ :\ (.*)\ on local host:.*""", match.group(2))
                        if model_match:
                            interface_name = model_match.group(1)
                        else:
                            interface_name = translate("Page_Cloud", "Unknown name")
                    self.rpcap_mapping[nio] = interface_name

    def slotDeleteGenEth(self):
        """ Delete the selected generic Ethernet NIO
        """
    
        item = self.listWidgetGenericEth.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetGenericEth.takeItem(self.listWidgetGenericEth.currentRow())
            
    def slotLinuxEthChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetLinuxEth.currentItem()
        if item != None:
            self.pushButtonDeleteLinuxEth.setEnabled(True)
        else:
            self.pushButtonDeleteLinuxEth.setEnabled(False)
        
    def slotAddLinuxEth(self):
        """ Add a new Linux Ethernet NIO
        """
    
        interface = unicode(self.lineEditLinuxEth.text())
        if interface:
            nio = 'nio_linux_eth:' + interface.lower()
            if not nio in self.nios:
                self.listWidgetLinuxEth.addItem(nio)
                self.nios.append(nio)
        
    def slotDeleteLinuxEth(self):
        """ Enabled the use of the delete button
        """    
        item = self.listWidgetLinuxEth.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetLinuxEth.takeItem(self.listWidgetLinuxEth.currentRow())
        
    def slotAddUDP(self):
        """ Add a new UDP NIO
        """
    
        local_port = self.spinBoxLocalPort.value()
        remote_host = unicode(self.lineEditRemoteHost.text())
        remote_port = self.spinBoxRemotePort.value()
        if remote_host:
            nio = 'nio_udp:' + str(local_port) + ':' + remote_host + ':' + str(remote_port)
            if not nio in self.nios:
                self.listWidgetUDP.addItem(nio)
                self.nios.append(nio)
                self.spinBoxLocalPort.setValue(local_port + 1)
                self.spinBoxRemotePort.setValue(remote_port + 1)

    def slotDeleteUDP(self):
        """ Delete an UDP NIO
        """
        
        item = self.listWidgetUDP.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetUDP.takeItem(self.listWidgetUDP.currentRow())

    def slotUDPChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetUDP.currentItem()
        if item != None:
            self.pushButtonDeleteUDP.setEnabled(True)
        else:
            self.pushButtonDeleteUDP.setEnabled(False)
            
    def slotUDPselected(self,  index):
        """ Load a selected UDP NIO
        """
        
        item = self.listWidgetUDP.currentItem()
        if (item != None):
            nio = unicode(item.text())
            match = re.search(r"""^nio_udp:(\d+):(.+):(\d+)$""", nio)
            if match:
                self.spinBoxLocalPort.setValue(int(match.group(1)))
                self.lineEditRemoteHost.setText(unicode(match.group(2)))
                self.spinBoxRemotePort.setValue(int(match.group(3)))

    def slotAddTAP(self):
        """ Add a new UDP NIO
        """
    
        tap_interface = unicode(self.lineEditTAP.text())
        if tap_interface:
            nio = 'nio_tap:' + tap_interface.lower()
            if not nio in self.nios:
                self.listWidgetTAP.addItem(nio)
                self.nios.append(nio)

    def slotDeleteTAP(self):
        """ Delete a TAP NIO
        """
        
        item = self.listWidgetTAP.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetTAP.takeItem(self.listWidgetTAP.currentRow())

    def slotTAPChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetTAP.currentItem()
        if item != None:
            self.pushButtonDeleteTAP.setEnabled(True)
        else:
            self.pushButtonDeleteTAP.setEnabled(False)

    def slotAddUNIX(self):
        """ Add a new UNIX NIO
        """
    
        local_file = unicode(self.lineEditUNIXLocalFile.text())
        remote_file = unicode(self.lineEditUNIXRemoteFile.text())
        if local_file and remote_file:
            nio = 'nio_unix:' + local_file + ':' + remote_file
            if not nio in self.nios:
                self.listWidgetUNIX.addItem(nio)
                self.nios.append(nio)

    def slotDeleteUNIX(self):
        """ Delete an UNIX NIO
        """
        
        item = self.listWidgetUNIX.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetUNIX.takeItem(self.listWidgetUNIX.currentRow())

    def slotUNIXChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetUNIX.currentItem()
        if item != None:
            self.pushButtonDeleteUNIX.setEnabled(True)
        else:
            self.pushButtonDeleteUNIX.setEnabled(False)
            
    def slotUNIXselected(self,  index):
        """ Load a selected UNIX NIO
        """
        
        item = self.listWidgetUNIX.currentItem()
        if (item != None):
            nio = unicode(item.text())
            match = re.search(r"""^nio_unix:(.+):(.+)$""", nio)
            if match:
                self.lineEditUNIXLocalFile.setText(unicode(match.group(1)))
                self.lineEditUNIXRemoteFile.setText(unicode(match.group(2)))

    def slotAddVDE(self):
        """ Add a new VDE NIO
        """
    
        control_file = unicode(self.lineEditVDEControlFile.text())
        local_file = unicode(self.lineEditVDELocalFile.text())
        if local_file and control_file:
            nio = 'nio_vde:' + control_file + ':' + local_file
            if not nio in self.nios:
                self.listWidgetVDE.addItem(nio)
                self.nios.append(nio)

    def slotDeleteVDE(self):
        """ Delete a VDE NIO
        """
        
        item = self.listWidgetVDE.currentItem()
        if (item != None):
            nio = unicode(item.text())
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetVDE.takeItem(self.listWidgetVDE.currentRow())

    def slotVDEChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetVDE.currentItem()
        if item != None:
            self.pushButtonDeleteVDE.setEnabled(True)
        else:
            self.pushButtonDeleteVDE.setEnabled(False)
            
    def slotVDEselected(self,  index):
        """ Load a selected VDE NIO
        """
        
        item = self.listWidgetVDE.currentItem()
        if (item != None):
            nio = unicode(item.text())
            match = re.search(r"""^nio_vde:(.+):(.+)$""", nio)
            if match:
                self.lineEditVDEControlFile.setText(unicode(match.group(1)))
                self.lineEditVDELocalFile.setText(unicode(match.group(2)))

    def slotAddNull(self):
        """ Add a new NULL NIO
        """
    
        identifier = unicode(self.lineEditNullIdentifer.text())
        if identifier:
            nio = 'nio_null:' + identifier
            if not nio in self.nios:
                self.listWidgetNull.addItem(nio)
                self.nios.append(nio)

    def slotDeleteNull(self):
        """ Delete a NULL NIO
        """
        
        item = self.listWidgetNull.currentItem()
        if (item != None):
            nio = unicode(item.text())  
            connected_ports = self.node.getConnectedInterfaceList()
            if nio in connected_ports:
                QtGui.QMessageBox.critical(globals.nodeConfiguratorWindow, 'NIOs', translate("Page_Cloud", "A link is connected with NIO %s") % nio)
                return
            self.nios.remove(nio)
            self.listWidgetNull.takeItem(self.listWidgetNull.currentRow())

    def slotNullChanged(self):
        """ Enabled the use of the delete button
        """
        
        item = self.listWidgetNull.currentItem()
        if item != None:
            self.pushButtonDeleteNull.setEnabled(True)
        else:
            self.pushButtonDeleteNull.setEnabled(False)
            
    def slotNullselected(self,  index):
        """ Load a selected NULL NIO
        """
        
        item = self.listWidgetNull.currentItem()
        if (item != None):
            nio = unicode(item.text())
            match = re.search(r"""^nio_null:(.+)$""", nio)
            if match:
                self.lineEditNullIdentifer.setText(unicode(match.group(1)))

    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            Cloudconfig = config
        else:
            Cloudconfig = self.node.config

        self.nios = []
        self.listWidgetGenericEth.clear()
        self.listWidgetLinuxEth.clear()
        self.listWidgetUDP.clear()
        self.listWidgetTAP.clear()
        self.listWidgetUNIX.clear()
        self.listWidgetVDE.clear()
        self.listWidgetNull.clear()
        for nio in Cloudconfig['nios'] :
            (niotype, niostring) = nio.split(':',  1)
            self.nios.append(nio)
            if niotype.lower() == 'nio_gen_eth':
                self.listWidgetGenericEth.addItem(nio)
            elif niotype.lower() == 'nio_linux_eth':
                self.listWidgetLinuxEth.addItem(nio)
            elif niotype.lower() == 'nio_udp':
                self.listWidgetUDP.addItem(nio)
            elif niotype.lower() == 'nio_tap':
                self.listWidgetTAP.addItem(nio)
            elif niotype.lower() == 'nio_unix':
                self.listWidgetUNIX.addItem(nio)
            elif niotype.lower() == 'nio_vde':
                self.listWidgetVDE.addItem(nio)
            elif niotype.lower() == 'nio_null':
                self.listWidgetNull.addItem(nio)

    def saveConfig(self, id, config = None):
        """ Save the config
        """

        self.node = globals.GApp.topology.getNode(id)
        if config:
            Cloudconfig = config
        else:
            Cloudconfig  = self.node.duplicate_config()

        Cloudconfig['nios'] = self.nios
        Cloudconfig['rpcap_mapping'] = self.rpcap_mapping

        return Cloudconfig
            
def create(dlg):

    return  Page_Cloud()
