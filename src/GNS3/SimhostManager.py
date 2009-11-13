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
# code@gns3.net
#

import os, sys, time
import subprocess as sub
import GNS3.Globals as globals
import GNS3.Dynagen.simhost_lib as lwip
from socket import socket, timeout, AF_INET, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug

class SimhostManager(object):
    """ SimhostManager class
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

        simhost = globals.GApp.systconf['simhost']
        self.hypervisor_path = simhost.path
        self.hypervisor_wd = simhost.workdir
        globals.simhost_hypervisor_baseport = simhost.basePort
        globals.simhost_hypervisor_baseudp = simhost.baseUDP

    def startNewHypervisor(self, port):
        """ Create a new dynamips process and start it
        """

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)

        # test if a hypervisor is already running on this port
        s = socket(AF_INET, SOCK_STREAM)
        s.setblocking(0)
        s.settimeout(300)
        try:
            s.connect(('localhost', port))
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Simhost Manager',
                                      unicode(translate("SimhostManager", "A simhost hypervisor is already running on port %i, it will not be shutdown after you quit GNS3")) % port)
            s.close()
            globals.simhost_hypervisor_baseport += 1
            return None
        except:
            s.close()

        # start dynamips in hypervisor mode (-H)
        proc.start( self.hypervisor_path ,  ['-H', str(port)])

        if proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Simhost Manager',  unicode(translate("SimhostManager", "Can't start simhost hypervisor on port %i")) % port)
            return None

        hypervisor = {'port': port,
                            'proc_instance': proc}

        self.hypervisors.append(hypervisor)
        return hypervisor

    def waitHypervisor(self, hypervisor):
        """ Wait the hypervisor until it accepts connections
        """

        last_exception = None
        # give 15 seconds to the hypervisor to accept connections
        count = 15
        progress = None
        connection_success = False
        debug("Simhost manager: connect on " + str(hypervisor['port']))
        for nb in range(count + 1):
            s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            if nb == 3:
                progress = QtGui.QProgressDialog(unicode(translate("SimhostManager", "Connecting to a simhost hypervisor on port %i ...")) % hypervisor['port'],
                                                                                                                                        translate("SimhostManager", "Abort"), 0, count, globals.GApp.mainWindow)
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
            except Exception, ex:
                s.close()
                time.sleep(1)
                last_exception = ex
                continue
            debug("Simhost manager: hypervisor on port " +  str(hypervisor['port']) + " started")
            connection_success = True
            break

        if connection_success:
            s.close()
            globals.simhost_hypervisor_baseport += 1
            time.sleep(0.2)
        else:
            if last_exception:
                debug("Simhost manager: last exception raised by socket: " + unicode(last_exception))
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Simhost Manager',
                                       unicode(translate("SimhostManager", "Can't connect to the simhost hypervisor on port %i")) % hypervisor['port'])
            hypervisor['proc_instance'].close()
            self.hypervisors.remove(hypervisor)
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True

    def allocateHypervisor(self):
        """ Allocate a hypervisor for a given node
        """

        hypervisor = self.startNewHypervisor(globals.simhost_hypervisor_baseport)
        if hypervisor == None:
            return None

        if not self.waitHypervisor(hypervisor):
            return None

        globals.simhost_hypervisor_baseudp += globals.GApp.systconf['dynamips'].udp_incrementation
        return hypervisor

    def unallocateHypervisor(self, port):
        """ Unallocate a hypervisor for a given node
        """

        for hypervisor in self.hypervisors:
            if hypervisor['port'] == port:
                debug("Hypervisor manager: close lwip hypervisor on port " + str(hypervisor['port']))
                hypervisor['proc_instance'].close()
                hypervisor['proc_instance'] = None
        
    def getHypervisor(self, port):
        """ Get a hypervisor from the hypervisor manager
        """

        for hypervisor in self.hypervisors:
            if hypervisor['port'] == port:
                return hypervisor
        return None

    def stopProcHypervisors(self):
        """ Shutdown all started hypervisors
        """

        if globals.GApp != None and globals.GApp.systconf['simhost']:
            self.setDefaults()
        hypervisors = globals.GApp.dynagen.dynamips.copy()
        for hypervisor in hypervisors.values():
            if isinstance(hypervisor, lwip.LWIP):
                try:
                    if globals.GApp.dynagen.dynamips.has_key(hypervisor.host + ':' + hypervisor.port):
                        debug("Hypervisor manager: reset and close lwip hypervisor on port " + str(hypervisor['port']))
                        hypervisor.reset()
                        hypervisor.close()
                        del globals.GApp.dynagen.dynamips[hypervisor.host + ':' + hypervisor.port]
                except:
                    continue
        for hypervisor in self.hypervisors:
            debug("Hypervisor manager: close lwip hypervisor on port " + str(hypervisor['port']))
            hypervisor['proc_instance'].close()
            hypervisor['proc_instance'] = None
        self.hypervisors = []

    def preloadSimhost(self):
        """ Preload Simhost hypervisor
        """

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        port = globals.simhost_hypervisor_baseport

        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)
        # start simhost
        proc.start(self.hypervisor_path,  ['-H', str(port)])
        if proc.waitForStarted() == False:
            return False

        # give 5 seconds to the hypervisor to accept connections
        count = 5
        connection_success = False
        for nb in range(count + 1):
            s = socket(AF_INET, SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(300)
            try:
                s.connect(('localhost', port))
            except:
                s.close()
                time.sleep(1)
                continue
            connection_success = True
            break
        if connection_success:
            s.close()
            proc.close()
            return True
        if proc.state():
            proc.close()
        return False
