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
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from GNS3.Node.IOSRouter import IOSRouter

class HypervisorManager:
    """ HypervisorManager class
        Start one or more dynamips in hypervisor mode
    """

    def __init__(self):
    
        self.hypervisors = []
        self.preloaded_hypervisors = []
        self.used_preloaded_hypervisors = []
        self.setDefaults()
        
    def __del__(self):
        """ Shutdown all started hypervisors 
        """

        self.stopProcHypervisors()
        for hypervisor in self.preloaded_hypervisors:
            hypervisor['proc_instance'].close()
        self.preloaded_hypervisors = []
       
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

#        if len(self.preloaded_hypervisors):
#            for hypervisor in self.preloaded_hypervisors:
#                if hypervisor not in self.used_preloaded_hypervisors:
#                    self.used_preloaded_hypervisors.append(hypervisor)
#                    return hypervisor

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
                            'proc_instance': proc}

        self.hypervisors.append(hypervisor)
        return hypervisor
    
    def startProcHypervisors(self):
        """ Load-balance IOS instances on multiple hypervisors
        """

        node_list = []
        mem = 0
        for node in globals.GApp.topology.nodes.itervalues():
            if type(node) == IOSRouter:
                image = globals.GApp.iosimages[node.config.image]
                if not image.hypervisor_host:
                    # needs a local hypervisor
                    node_list.append(node)
                    mem += node.config.ram

        # compute the number of hypervisors to start
        count = mem / globals.HypervisorMemoryUsageLimit
        count += 1
        # show a progress dialog if multiple hypervisors to start
        if count > 1:
            
            progress = QtGui.QProgressDialog(translate("HypervisorManager", "Starting hypervisors ..."), translate("HypervisorManager", "Abort"), 0, count, globals.GApp.mainWindow)
            progress.setMinimum(1)
            progress.setWindowModality(QtCore.Qt.WindowModal)

        mem = 0
        current_node = 0
        hypervisor = self.startNewHypervisor()
        if hypervisor == None:
            return False
        nb_node = len(node_list)
        for node in node_list:
            if count > 1:
                progress.setValue(current_node)
                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
            if  count > 1 and progress.wasCanceled():
                progress.reset()
                break
            mem += node.config.ram
            current_node += 1
            node.configHypervisor('localhost',  hypervisor['port'],  self.hypervisor_wd,  self.baseUDP, self.baseConsole)
            if mem >= globals.HypervisorMemoryUsageLimit and current_node != nb_node:
                # start a new hypervisor
                hypervisor = self.startNewHypervisor()
                # wait for starting
                time.sleep(1)
                # change the base UDP
                self.baseUDP += globals.HypervisorUDPIncrementation
                mem = 0
        time.sleep(2)
        if count > 1:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True
                
    def stopProcHypervisors(self):
        """ Shutdown all started hypervisors 
        """
    
        if globals.GApp != None and globals.GApp.systconf['dynamips']:
            dynamips = globals.GApp.systconf['dynamips']
            self.hypervisor_baseport = dynamips.port
            self.baseUDP = dynamips.baseUDP
            self.baseConsole = dynamips.baseConsole
        for hypervisor in self.hypervisors:
            hypervisor['proc_instance'].close()
        self.hypervisors = []

    def slotStandardOutput(self):
        """ Display the standard output of the process
        """
        
        print 'received data stdout'
        for hypervisor in self.hypervisors:
            print hypervisor['proc_instance'].readAllStandardOutput()
        
        #print str(self.proc.readAllStandardOutput())
        
    def slotStandardErrorOutput(self):
        """ Display the error output of the process
        """

        print 'received data stderr'
        print str(self.proc.readAllStandardError)
        
    def preloadDynamips(self, showErrMessage=True):
        """ Preload Dynamips
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
            if showErrMessage:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',  translate("HypervisorManager", "Can't start Dynamips"))
            return False

        hypervisor = {'port': port,
                            'proc_instance': proc}

        self.preloaded_hypervisors.append(hypervisor)
        return True
