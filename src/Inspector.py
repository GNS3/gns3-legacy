#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

from PyQt4 import QtCore, QtGui
from Ui_Inspector import *
import __main__

class Inspector(QtGui.QDialog, Ui_FormInspector):
    ''' Inspector class
    
        Get access to an IOS console
        Settings of the IOS
    '''

    # Get access to globals
    main = __main__
    
    def __init__(self):

        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        # Node ID currently used
        self.nodeid = None
        
        # Connect IOS configuration buttons to slots
        self.connect(self.buttonBoxIOSConfig, QtCore.SIGNAL('clicked(QAbstractButton *)'), self.slotSaveIOSConfig)
        self.connect(self.buttonBoxIOSConfig, QtCore.SIGNAL('rejected()'), self.slotRestoreIOSConfig)
        
        # Connect console buttons to slots
        self.connect(self.pushButton_Start, QtCore.SIGNAL('clicked()'), self.slotStart)
        self.connect(self.pushButton_Shutdown, QtCore.SIGNAL('clicked()'), self.slotShutdown)


        # Connect IOS combobox to a slot
        self.connect(self.comboBoxIOS, QtCore.SIGNAL('currentIndexChanged(int)'), self.slotSelectedIOS)

        # Old code kept for future purposes
        #TODO: clean this code
##        # temporary emplacement for the hypervisor
##        self.proc = QtCore.QProcess(self)
##        self.proc.setWorkingDirectory(QtCore.QString('/home/grossmj/Dynamips/'))
##        QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotStandardOutput)
##        QtCore.QObject.connect(self.proc, QtCore.SIGNAL('error(QProcess::ProcessError)'), self.slotProcessError)
##        self.proc.start('/home/grossmj/Dynamips/dynamips-0.2.7-RC1-x86.bin',  ['-H', '7200'])
##        
##        if self.proc.waitForStarted() == False:
##            print 'Hypervisor not started !'
##            return
##        print 'Hypervisor started'

##    def __del__(self):
##    
##        self.proc.close()

##    def slotHypervisor(self):
##
##        self.telnet_hypervisor = telnetlib.Telnet('localhost', 7200)
##        
##        self.telnet_hypervisor.write("hypervisor version\r\n")
##        self.telnet_hypervisor.write("hypervisor reset\r\n")
##        self.telnet_hypervisor.write("hypervisor working_dir /tmp\r\n")
##        
##        self.telnet_hypervisor.write("c3600 create R1 0\r\n")
##        self.telnet_hypervisor.write("c3600 set_chassis R1 3640\r\n")
##        self.telnet_hypervisor.write("c3600 add_nm_binding R1 0 NM-1FE-TX\r\n")
##
##        self.telnet_hypervisor.write("vm set_con_tcp_port R1 2000\r\n")
##        self.telnet_hypervisor.write("vm set_ram R1 128\r\n")
##        self.telnet_hypervisor.write("vm set_disk0 R1 0\r\n")
##        self.telnet_hypervisor.write("vm set_disk1 R1 0\r\n")
##        self.telnet_hypervisor.write("vm set_idle_pc R1 0x60575b54\r\n")
##        self.telnet_hypervisor.write("vm set_ios R1 /home/grossmj/Dynamips/c3640.bin\r\n")
##        self.telnet_hypervisor.write("vm set_ram_mmap R1 1\r\n")
##
##        # "nio create_udp nio_udp0 10000 127.0.0.1 10001"
##        # "nio create_udp nio_udp1 10001 127.0.0.1 10000"
##        # "c3600 add_nio_binding R1 0 0 nio_udp0"
##        # "c3600 add_nio_binding R2 0 0 nio_udp1"
##
##        # start the instance
##        self.telnet_hypervisor.write("c3600 start R1\r\n")
##        self.pushButton_Hypervisor.setEnabled(False)
        
##    # check the hypervisor output
##    def slotStandardOutput(self):
##        
##        print str(self.proc.readAllStandardOutput())
##    
##    # check for any error
##    def slotProcessError(self):
##    
##        print 'HYPERVISOR ERROR !'
     
    def slotStart(self):
        '''Create a new IOS instance and connect a console to it'''

        # Is there a connection to a hypervisor ? (temporary code)
        if self.main.hypervisor == None:
            print 'No hypervisor !'
            return
        
        # Get the currently selected node
        node = self.main.nodes[self.nodeid]
        
        # Start a new IOS instance
        node.startIOS()
        
        self.textEditConsole.clear()
        # Tell the console how to write key events on the telnet connection
        self.textEditConsole.write = node.telnet.write
        
        # Get a telnet connection to the IOS
        if node.connect() == False:
            QtGui.QMessageBox.critical(self, 'Connection',  msg)
            return
            
        # Notify us when data are available to read on the console socket
        self.notifier = QtCore.QSocketNotifier(node.telnet.fileno(), QtCore.QSocketNotifier.Read)
        self.connect(self.notifier, QtCore.SIGNAL("activated(int)"), self.slotReadAllOutput)
        
        self.textEditConsole.isConnected = True
        self.pushButton_Start.setEnabled (False)
        self.pushButton_Shutdown.setEnabled (True)
        self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_green.svg'))
        
    def slotShutdown(self, close = True):
        '''Disconnect and shutdown a IOS instance'''
    
        # Is there a connection to a hypervisor ? (temporary code)
        if self.main.hypervisor == None:
            print 'No hypervisor !'
            return

        self.textEditConsole.isConnected = False
        
        # Get the currently selected node
        node = self.main.nodes[self.nodeid]
        
        # Disconnect the telnet console
        if close:
            node.disconnect()
            
        # Stop the IOS instance
        node.stopIOS()
        
        self.pushButton_Start.setEnabled (True)
        self.pushButton_Shutdown.setEnabled(False)
        self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_red.svg'))
        self.notifier.setEnabled(False)

    def slotReadAllOutput(self):
    
        try:
            # Get the currently selected node
            node = self.main.nodes[self.nodeid]
            
            # Read data on the socket and display them on the console
            self.textEditConsole.slotStandardOutput(node.telnet.read_very_eager())

        except EOFError, msg:
            QtGui.QMessageBox.critical(self, 'Disconnection',  unicode(msg))
            self.slotShutdown(close = False)
            
    def slotSelectedIOS(self, index):

        #FIXME: a bug adds more than once the network module list
        imagename = str(self.comboBoxIOS.currentText())
        if imagename != '':
            if self.main.ios_images[imagename]['platform'] == '3600':
                self.setDefaults3600Platform(imagename)

    def loadNodeInfos(self, id):
        '''Called when a node is selected'''

        # Prevent data being sent to the console from another node
        if self.nodeid != None and id != self.nodeid:
            self.textEditConsole.isConnected = False
            self.notifier.setEnabled(False)
        
        # Set the currently selected node ID
        self.nodeid = id
        self.textEditConsole.clear()
        node = self.main.nodes[self.nodeid]

        # Connect the node telnet socket (if connected) to the console
        if node.isConnected():
            self.textEditConsole.write = node.telnet.write
            self.textEditConsole.isConnected = True
            self.notifier = QtCore.QSocketNotifier(node.telnet.fileno(), QtCore.QSocketNotifier.Read)
            self.connect(self.notifier, QtCore.SIGNAL("activated(int)"), self.slotReadAllOutput)
            self.pushButton_Start.setEnabled (False)
            self.pushButton_Shutdown.setEnabled (True)
            self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_green.svg'))
        else:
            self.pushButton_Start.setEnabled (True)
            self.pushButton_Shutdown.setEnabled (False)
            self.labelStatus.setPixmap(QtGui.QPixmap('../svg/icons/led_red.svg'))

        # Show IOS recorded images
        self.comboBoxIOS.addItems(self.main.ios_images.keys())
        
        # If the IOS config is not empty, restore it
        if node.iosConfig != {}:
            'RESTORE !!!'
            self.slotRestoreIOSConfig()
        else:
            self.setDefaults()
            self.saveIOSConfig()

    def setDefaults(self):
    
        #FIXME: do we really need this ?
        node = self.main.nodes[self.nodeid]
        self.comboBoxIOS.clear()
        self.lineEditConsolePort.clear()
        self.lineEditStartupConfig.clear()
        self.spinBoxRamSize.setValue(128)
        self.spinBoxRomSize.setValue(4)
        self.spinBoxNvramSize.setValue(128)
        self.spinBoxPcmciaDisk0Size.setValue(0)
        self.spinBoxPcmciaDisk1Size.setValue(0)
        self.checkBoxMapped.setCheckState(QtCore.Qt.Checked)
        self.lineEditConfreg.setText('0x2102')
        self.spinBoxExecArea.setValue(64)
        self.spinBoxIomem.setValue(5)
        
    def setDefaults3600Platform(self, imagename):
        
        network_modules = ['', 'NM-1E', 'NM-4E', 'NM-1FE-TX', 'NM-4T']

        chassis = self.main.ios_images[imagename]['chassis']
        if chassis == '3620':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
        elif chassis == '3640':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
            self.comboBoxSlot2.addItems(network_modules)
            self.comboBoxSlot3.addItems(network_modules)
        elif chassis == '3660':
            self.comboBoxSlot0.addItems(network_modules)
            self.comboBoxSlot1.addItems(network_modules)
            self.comboBoxSlot2.addItems(network_modules)
            self.comboBoxSlot3.addItems(network_modules)
            self.comboBoxSlot4.addItems(network_modules)
            self.comboBoxSlot5.addItems(network_modules)
            self.comboBoxSlot6.addItems(network_modules)
                
    def saveIOSConfig(self):
    
        node = self.main.nodes[self.nodeid]
        node.iosConfig['iosimage'] = str(self.comboBoxIOS.currentText())
        node.iosConfig['consoleport'] = str(self.lineEditConsolePort.text())
        node.iosConfig['startup-config'] = str(self.lineEditStartupConfig.text())
        node.iosConfig['RAM'] = self.spinBoxRamSize.value()
        node.iosConfig['ROM'] = self.spinBoxRomSize.value()
        node.iosConfig['NVRAM'] = self.spinBoxNvramSize.value()
        node.iosConfig['pcmcia-disk0'] = self.spinBoxPcmciaDisk0Size.value()
        node.iosConfig['pcmcia-disk1'] = self.spinBoxPcmciaDisk1Size.value()
        if self.checkBoxMapped.checkState() == QtCore.Qt.Checked:
            node.iosConfig['mmap'] = True
        else:
            node.iosConfig['mmap'] = False
        node.iosConfig['confreg'] = str(self.lineEditConfreg.text())
        node.iosConfig['execarea'] = self.spinBoxExecArea.value()
        node.iosConfig['iomem'] = self.spinBoxIomem.value()
        
        node.iosConfig['slots'] = []
        node.iosConfig['slots'].append(str(self.comboBoxSlot0.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot1.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot2.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot3.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot4.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot5.currentText()))
        node.iosConfig['slots'].append(str(self.comboBoxSlot6.currentText()))

    def slotSaveIOSConfig(self, button):
    
        if self.buttonBoxIOSConfig.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.saveIOSConfig()

    def slotRestoreIOSConfig(self):
    
        node = self.main.nodes[self.nodeid]
        if node.iosConfig == {}:
            return
        #self.comboBoxIOS.addItem(node.iosConfig['iosimage'])
        self.lineEditConsolePort.setText(node.iosConfig['consoleport'])
        self.lineEditStartupConfig.setText(node.iosConfig['startup-config'])
        self.spinBoxRamSize.setValue(node.iosConfig['RAM'])
        self.spinBoxRomSize.setValue(node.iosConfig['ROM'])
        self.spinBoxNvramSize.setValue(node.iosConfig['NVRAM'])
        self.spinBoxPcmciaDisk0Size.setValue(node.iosConfig['pcmcia-disk0'])
        self.spinBoxPcmciaDisk1Size.setValue(node.iosConfig['pcmcia-disk1'])
        if node.iosConfig['mmap'] == True:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxMapped.setCheckState(QtCore.Qt.Unchecked)
        self.lineEditConfreg.setText(node.iosConfig['confreg'])
        self.spinBoxExecArea.setValue(node.iosConfig['execarea'])
        self.spinBoxIomem.setValue(node.iosConfig['iomem'])
