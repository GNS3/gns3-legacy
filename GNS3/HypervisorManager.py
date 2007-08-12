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

import time
import GNS3.Globals as globals
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate
from GNS3.Node.IOSRouter import IOSRouter

MEM_USAGE_LIMIT = 512
BASE_PORT_UDP = 10000

class HypervisorManager:
    """ LocalHypervisor class
        Start the local hypervisor program
    """

    def __init__(self):
    
        self.hypervisors = []
        
        dynamips = globals.GApp.systconf['dynamips']
        self.hypervisor_path = dynamips.path
        self.hypervisor_wd = dynamips.workdir
        self.hypervisor_baseport = dynamips.port
        self.baseUDP = BASE_PORT_UDP

    def __del__(self):
    
        self.stopProcHypervisors()
        
    def __startNewHypervisor(self):
    
        proc = QtCore.QProcess(globals.GApp.mainWindow)
        port = self.hypervisor_baseport
        self.hypervisor_baseport += 1
        #QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotStandardOutput)
        if self.hypervisor_wd:
            proc.setWorkingDirectory(self.hypervisor_wd)
        proc.start(self.hypervisor_path,  ['-H', str(port)])
        if proc.waitForStarted() == False:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor',  translate("HypervisorManager", "Can't start the local hypervisor"))
                return None
                
        hypervisor = {
                            'port': port,
                            'proc_instance': proc}

        self.hypervisors.append(hypervisor)
        return hypervisor
    
    def startProcHypervisors(self):

        node_list = []
        mem = 0
        for node in globals.GApp.topology.nodes.itervalues():
            if type(node) == IOSRouter:
                image = globals.GApp.iosimages[node.config.image]
                if not image.hypervisor_host:
                    node_list.append(node)
                    mem += node.config.RAM

        count = mem / MEM_USAGE_LIMIT
        count += 1
        if count > 1:
            progress = QtGui.QProgressDialog("Starting hypervisors ...", "Abort", 0, count, globals.GApp.mainWindow)
            progress.setMinimum(1)
            progress.setWindowModality(QtCore.Qt.WindowModal)

        mem = 0
        current_node = 0
        hypervisor = self.__startNewHypervisor()
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
            mem += node.config.RAM
            current_node += 1
            node.configHypervisor('localhost',  hypervisor['port'],  self.hypervisor_wd,  self.baseUDP)
            if mem >= MEM_USAGE_LIMIT and current_node != nb_node:
                hypervisor = self.__startNewHypervisor()
                time.sleep(1)
                self.baseUDP += 15
                mem = 0
        time.sleep(2)
        if count > 1:
            progress.setValue(count)
        return True
                
    def stopProcHypervisors(self):
    
        if globals.GApp != None:
            dynamips = globals.GApp.systconf['dynamips']
            self.hypervisor_baseport = dynamips.port
        self.baseUDP = BASE_PORT_UDP
        for hypervisor in self.hypervisors:
            hypervisor['proc_instance'].close()
        self.hypervisors = []

    def slotStandardOutput(self):
        """ Display the standard output of the process
        """

        print str(self.proc.readAllStandardOutput())
