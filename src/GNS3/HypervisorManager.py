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

import time, os, socket
import GNS3.Globals as globals
import GNS3.Dynagen.dynamips_lib as lib
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug, killAll
from GNS3.Node.IOSRouter import IOSRouter
from distutils.version import LooseVersion

class HypervisorManager(object):
    """ HypervisorManager class
        Start one or more dynamips in hypervisor mode
    """

    def __init__(self):

        self.hypervisors = []
        self.setDefaults()

    def __del__(self):
        """ Shutdown all started hypervisors
        """

        for hypervisor in self.hypervisors:
            hypervisor['proc_instance'].kill()

    def setDefaults(self):
        """ Set the default values for the hypervisor manager
        """

        self.dynamips = globals.GApp.systconf['dynamips']
        self.hypervisor_path = self.dynamips.path
        self.hypervisor_wd = self.dynamips.workdir
        self.baseConsole = self.dynamips.baseConsole
        self.baseAUX = self.dynamips.baseAUX
        globals.hypervisor_baseport = self.dynamips.port
        globals.GApp.dynagen.globaludp = self.dynamips.baseUDP

    def startNewHypervisor(self, port, binding=None, processcheck=True):
        """ Create a new dynamips process and start it
        """

        if binding == None:
            if self.dynamips.HypervisorManager_binding and self.dynamips.HypervisorManager_binding != '0.0.0.0':
                binding = self.dynamips.HypervisorManager_binding
            else:
                binding = '127.0.0.1'

        proc = QtCore.QProcess(globals.GApp.mainWindow)

        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)

        if processcheck:
            # test if a hypervisor is already running on this port
            timeout = 60.0
            try:
                #FIXME: replace with bind() for faster process?
                s = socket.create_connection((binding, port), timeout)
                s.close()

                reply = QtGui.QMessageBox.question(globals.GApp.mainWindow, translate("HypervisorManager", "Hypervisor Manager"),
                                                   translate("HypervisorManager", "Apparently an hypervisor is already running on %s port %i, would you like to kill all Dynamips processes?") % (binding, port),
                                                   QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    killAll(os.path.basename(self.hypervisor_path))
                    time.sleep(1)
                else:
                    print "Incrementing +100 for base console port, base AUX port, base hypervisor port and +200 for base UDP port"
                    self.baseConsole += 100
                    if self.baseAUX:
                        self.baseAUX += 100
                    globals.hypervisor_baseport += 100
                    globals.GApp.dynagen.globaludp += 200
                    port = globals.hypervisor_baseport

                #FIXME: replace with bind() for faster process?
                s = socket.create_connection((binding, port), timeout)
                s.close()

                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("HypervisorManager", "Hypervisor Manager"),
                                           translate("HypervisorManager", "A program is still running on %s port %i, you will have to stop it manually or change port settings") % (binding, port))

                globals.hypervisor_baseport += 1
                return None
            except:
                pass

        try:
            # start dynamips in hypervisor mode (-H)
            # Dynamips version 0.2.8-RC3 and before cannot accept a specific port when binding on a chosen address with param -H <IP address:port> (bug is inside Dynamips).
            if self.dynamips.detected_version and LooseVersion(self.dynamips.detected_version) > '0.2.8-RC3' and self.dynamips.HypervisorManager_binding != '0.0.0.0':
                debug("Starting Dynamips with -H %s:%i" % (binding, port))
                proc.start(self.hypervisor_path,  ['-H', binding + ':' + str(port)])
            else:
                debug("Starting Dynamips with -H %i" % port)
                proc.start(self.hypervisor_path,  ['-H', str(port)])
        except:
            debug('Exception with LooseVersion()')
            proc.start(self.hypervisor_path,  ['-H', str(port)])

        if proc.waitForStarted() == False:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager', translate("HypervisorManager", "Can't start Dynamips on %s port %i") % (binding, port))
            return None

        hypervisor = {'host': binding,
                      'port': port,
                      'proc_instance': proc,
                      'load': 0,
                      'image_ref': ''}

        self.hypervisors.append(hypervisor)
        return hypervisor

    def waitHypervisor(self, hypervisor, binding=None):
        """ Wait the hypervisor until it accepts connections
        """
        
        if binding == None:
            if self.dynamips.HypervisorManager_binding and self.dynamips.HypervisorManager_binding != '0.0.0.0':
                binding = self.dynamips.HypervisorManager_binding
            else:
                debug("Hypervisor manager: warning: no default binding, defaulting to 127.0.0.1")
                binding = '127.0.0.1'

        last_exception = None
        # give 15 seconds to the hypervisor to accept connections
        count = 15
        progress = None
        timeout = 60.0
        connection_success = False
        debug("Hypervisor manager: connecting on %s:%i" % (binding, hypervisor['port']))
        for nb in range(count + 1):            
            if nb == 3:
                progress = QtGui.QProgressDialog(translate("HypervisorManager", "Connecting to an hypervisor on %s port %i ...") % (binding, hypervisor['port']),
                                                 translate("HypervisorManager", "Abort"), 0, count, globals.GApp.mainWindow)
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
                s = socket.create_connection((binding, hypervisor['port']), timeout)
            except Exception, ex:
                time.sleep(1)
                last_exception = ex
                continue
            debug("Hypervisor manager: connected to hypervisor on %s port %i" % (binding, hypervisor['port']))
            connection_success = True
            break

        if connection_success:
            s.close()
            globals.hypervisor_baseport += 1
            time.sleep(0.2)
        else:
            if not last_exception:
                last_exception = 'Unknown problem'
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',
                                       translate("HypervisorManager", "Can't connect to the hypervisor on %s port %i: %s") % (binding, hypervisor['port'], last_exception))
            hypervisor['proc_instance'].close()
            self.hypervisors.remove(hypervisor)
            return False
        if progress:
            progress.setValue(count)
            progress.deleteLater()
            progress = None
        return True

    def allocateHypervisor(self, node):
        """ Allocate a hypervisor for a given node
        """

        for hypervisor in self.hypervisors:
            if not isinstance(node, IOSRouter) or (isinstance(node, IOSRouter) and hypervisor['load'] + node.default_ram <= self.dynamips.memory_limit):
                if isinstance(node, IOSRouter):
                    if self.dynamips.allocateHypervisorPerIOS and hypervisor['image_ref'] != node.image_reference:
                        continue
                    hypervisor['load'] += node.default_ram
                debug("Hypervisor manager: allocates an already started hypervisor on %s port %i" % (hypervisor['host'], hypervisor['port']))
                if not globals.GApp.dynagen.dynamips.has_key(hypervisor['host'] + ':' + str(hypervisor['port'])):
                    globals.GApp.dynagen.create_dynamips_hypervisor(hypervisor['host'], hypervisor['port'])
                dynamips_hypervisor = globals.GApp.dynagen.dynamips[hypervisor['host'] + ':' + str(hypervisor['port'])]
                node.set_hypervisor(dynamips_hypervisor)
                return hypervisor

        hypervisor = self.startNewHypervisor(globals.hypervisor_baseport)
        if hypervisor == None:
            return None

        if not self.waitHypervisor(hypervisor):
            return None

        if isinstance(node, IOSRouter):
            hypervisor['load'] = node.default_ram
            hypervisor['image_ref'] = node.image_reference

        # use project workdir in priority
        if globals.GApp.workspace.projectWorkdir:
            if not os.access(globals.GApp.workspace.projectWorkdir, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'HypervisorManager',
                                          translate("HypervisorManager", "Working directory %s seems to not exist or be writable, please check") % globals.GApp.workspace.projectWorkdir)
            globals.GApp.dynagen.defaults_config['workingdir'] = globals.GApp.workspace.projectWorkdir
        elif self.hypervisor_wd:
            if not os.access(self.hypervisor_wd, os.F_OK | os.W_OK):
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'HypervisorManager',
                                          translate("HypervisorManager", "Working directory %s seems to not exist or be writable, please check") % self.hypervisor_wd)
            globals.GApp.dynagen.defaults_config['workingdir'] = self.hypervisor_wd
        try:
            dynamips_hypervisor = globals.GApp.dynagen.create_dynamips_hypervisor(hypervisor['host'], hypervisor['port'])
        except:
            dynamips_hypervisor = None
        if not dynamips_hypervisor:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',
                                       translate("HypervisorManager", "Can't set up hypervisor on %s port %i, please check the settings (writable working directory ...)") % (hypervisor['host'], hypervisor['port']))
            if globals.GApp.dynagen.dynamips.has_key(hypervisor['host'] + ':' + str(hypervisor['port'])):
                del globals.GApp.dynagen.dynamips[hypervisor['host'] + ':' + str(hypervisor['port'])]
            hypervisor['proc_instance'].close()
            hypervisor['proc_instance'] = None
            count = 0
            for hyp in self.hypervisors:
                if hyp['port'] == hypervisor['port']:
                    del self.hypervisors[count]
                    break
                count += 1
            return None
        debug("Hypervisor manager: create a new hypervisor on %s port %i" % (hypervisor['host'], hypervisor['port']))
        globals.GApp.dynagen.update_running_config()
        dynamips_hypervisor.configchange = True
        dynamips_hypervisor.udp = globals.GApp.dynagen.globaludp
        dynamips_hypervisor.starting_udp = globals.GApp.dynagen.globaludp
        dynamips_hypervisor.baseconsole = self.baseConsole
        dynamips_hypervisor.baseaux = self.baseAUX
        globals.GApp.dynagen.globaludp += self.dynamips.udp_incrementation
        debug("Hypervisor manager: hypervisor base UDP is %d " % dynamips_hypervisor.udp)
        node.set_hypervisor(dynamips_hypervisor)
        return hypervisor

    def unallocateHypervisor(self, node, host, port):
        """ Unallocate a hypervisor for a given node
        """

        for hypervisor in self.hypervisors:
            if hypervisor['host'] == host and hypervisor['port'] == int(port):
                debug("Hypervisor manager: unallocate hypervisor on %s port %i for node %s" % (host, port, node.hostname))
                hypervisor['load'] -= node.default_ram
                if hypervisor['load'] <= 0:
                    hypervisor['load'] = 0
                break

#FIXME: useless?
#    def changeHypervisorLoad(self, node, port, old_default_ram):
#        """ Change the hypervisor RAM load for a given node
#        """
#
#        for hypervisor in self.hypervisors:
#            if hypervisor['port'] == int(port):
#                debug("Hypervisor manager: change hypervisor load on %s port %i" % (self.dynamips.HypervisorManager_binding, port, node.hostname))
#                hypervisor['load'] -= old_default_ram
#                if hypervisor['load'] <= 0:
#                    hypervisor['load'] = 0
#                hypervisor['load'] += node.default_ram
#                break

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

        if globals.GApp != None and self.dynamips:
            self.setDefaults()
        hypervisors = globals.GApp.dynagen.dynamips.copy()
        for hypervisor in hypervisors.values():
            if isinstance(hypervisor, lib.Dynamips):
                try:
                    if globals.GApp.dynagen.dynamips.has_key(hypervisor.host + ':' + hypervisor.port):
                        debug("Hypervisor manager: reset and close hypervisor on %s port %i" % (hypervisor['host'], hypervisor['port']))
                        hypervisor.reset()
                        hypervisor.close()
                        del globals.GApp.dynagen.dynamips[hypervisor.host + ':' + hypervisor.port]
                except:
                    continue
        for hypervisor in self.hypervisors:
            debug("Hypervisor manager: close hypervisor on %s port %i" % (hypervisor['host'], hypervisor['port']))
            hypervisor['proc_instance'].terminate()
            time.sleep(0.5)
            hypervisor['proc_instance'].close()
            hypervisor['proc_instance'] = None
        self.hypervisors = []

    def preloadDynamips(self):
        """ Preload Dynamips
        """

        proc = QtCore.QProcess(globals.GApp.mainWindow)
        port = globals.hypervisor_baseport

        if self.hypervisor_wd:
            # set the working directory
            proc.setWorkingDirectory(self.hypervisor_wd)        
        try:
            # start dynamips in hypervisor mode (-H)
            # Dynamips version 0.2.8-RC3 and before cannot accept a specific port when binding on a chosen address with param -H <IP address:port> (bug is inside Dynamips).
            if self.dynamips.detected_version and LooseVersion(self.dynamips.detected_version) > '0.2.8-RC3' and self.dynamips.HypervisorManager_binding != '0.0.0.0':
                proc.start(self.hypervisor_path,  ['-H', self.dynamips.HypervisorManager_binding + ':' + str(port)])
            else:
                proc.start(self.hypervisor_path,  ['-H', str(port)])
        except:
            debug('Exception with LooseVersion')
            proc.start(self.hypervisor_path,  ['-H', str(port)])

        if proc.waitForStarted() == False:
            return False
        
        if self.dynamips.HypervisorManager_binding != '0.0.0.0':
            binding = self.dynamips.HypervisorManager_binding
        else:
            binding = '127.0.0.1'

        # give 5 seconds to the hypervisor to accept connections
        count = 5
        connection_success = False
        timeout = 60.0
        for nb in range(count + 1):
            try:
                s = socket.create_connection((binding, port), timeout)
            except:
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

    def showHypervisors(self):
        """ Show hypervisors port & load
        """

        print "Memory usage limit per hypervisor: %i MB" % self.dynamips.memory_limit
        print '%-10s %-10s %-10s' % ('Host/Binding','Port','Memory load')
        for hypervisor in self.hypervisors:
            print '%-10s %-10s %-10s' % (hypervisor['host'], hypervisor['port'], str(hypervisor['load']) + ' MB')

