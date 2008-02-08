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

import time
import GNS3.Globals as globals
from socket import socket, timeout, AF_INET, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate,  debug
from GNS3.Node.IOSRouter import IOSRouter

class HypervisorManager:
    """ HypervisorManager class
        Start one or more dynamips in hypervisor mode
    """

    def __init__(self):
    
        self.hypervisors = []
        self.setDefaults()
        
    def __del__(self):
        """ Shutdown all started hypervisors 
        """

        self.stopProcHypervisors()
       
    def setDefaults(self):
        """ Set the default values for the hypervisor manager
        """
        
        dynamips = globals.GApp.systconf['dynamips']
        self.hypervisor_path = dynamips.path
        self.hypervisor_wd = dynamips.workdir
        self.hypervisor_baseport = dynamips.port
        self.baseUDP = dynamips.baseUDP
        self.baseConsole = dynamips.baseConsole
      
    def startNewHypervisor(self):
        """ Create a new dynamips process and start it
        """

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        port = self.hypervisor_baseport
        self.hypervisor_baseport += 1
        
        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)
        # start dynamips in hypervisor mode (-H)
        proc.start(self.hypervisor_path,  ['-H', str(port)])
        
        if proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',  translate("HypervisorManager", "Can't start Dynamips"))
            return None

        hypervisor = {'port': port,
                            'proc_instance': proc, 
                            'load': 0}

        self.hypervisors.append(hypervisor)
        return hypervisor
    
    def allocateHypervisor(self, node):
        """ Allocate an hypervisor for a given node
        """

        for hypervisor in self.hypervisors:
            if hypervisor['load'] + node.default_ram <= globals.HypervisorMemoryUsageLimit:
                hypervisor['load'] += node.default_ram
                print 'Already existing hypervisor port = ' + str(hypervisor['port'])
                dynamips_hypervisor = globals.GApp.dynagen.dynamips['localhost:' + str(hypervisor['port'])]
                node.set_hypervisor(dynamips_hypervisor)
                return hypervisor

        hypervisor = self.startNewHypervisor()
        if hypervisor == None:
            return None
        
        # give 15 seconds to the hypervisor to accept connections
        count = 15
        progress = None
        connection_success = False
        for nb in range(count + 1):
            s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            if nb == 3:
                progress = QtGui.QProgressDialog(translate("HypervisorManager", "Connecting to an hypervisor on port " + str(hypervisor['port']) + " ..."), translate("HypervisorManager", "Abort"), 0, count, globals.GApp.mainWindow)
                progress.setMinimum(1)
                progress.setWindowModality(QtCore.Qt.WindowModal)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
            if nb > 2:
                progress.setValue(nb)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
                if  progress.wasCanceled():
                    progress.reset()
                    break
            try:
                s.connect(('localhost', hypervisor['port']))
            except:
                s.close()
                time.sleep(1)
                continue
            debug("Hypervisor manager: hypervisor on port " +  str(hypervisor['port']) + " started")
            connection_success = True
            break

        if connection_success:
            s.close()
            time.sleep(0.2)
        else:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',  translate("HypervisorManager", "Can't connect to the hypervisor on port " + str(hypervisor['port'])))
            hypervisor['proc_instance'].close()
            self.hypervisors.remove(hypervisor)
            return None
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        hypervisor['load'] = node.default_ram

        dynamips_hypervisor = globals.GApp.dynagen.create_dynamips_hypervisor('localhost', hypervisor['port'])
        globals.GApp.dynagen.update_running_config()
        dynamips_hypervisor.configchange = True
        node.set_hypervisor(dynamips_hypervisor)
        dynamips_hypervisor.udp = self.baseUDP
        if self.hypervisor_wd:
            dynamips_hypervisor.workingdir = self.hypervisor_wd

        print 'New created hypervisor port = ' + str(hypervisor['port'])
        self.baseUDP += globals.HypervisorUDPIncrementation
        return hypervisor

    def unallocateHypervisor(self, node, port):
        """ Unallocate an hypervisor for a given node
        """

        for hypervisor in self.hypervisors:
            if hypervisor['port'] == int(port):
                hypervisor['load'] -= node.default_ram
                if hypervisor['load'] <= 0:
                    hypervisor['load'] = 0
                break
    
    def stopProcHypervisors(self):
        """ Shutdown all started hypervisors 
        """
    
        if globals.GApp != None and globals.GApp.systconf['dynamips']:
            self.setDefaults()
        for hypervisor in self.hypervisors:
            hypervisor['proc_instance'].close()
            hypervisor['proc_instance'] = None
        self.hypervisors = []

    def preloadDynamips(self):
        """ Preload Dynamips
        """

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        port = self.hypervisor_baseport
        
        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)
        # start dynamips in hypervisor mode (-H)
        proc.start(self.hypervisor_path,  ['-H', str(port)])
        if proc.waitForStarted() == False:
            return False
        proc.close()
        proc = None
        return True
