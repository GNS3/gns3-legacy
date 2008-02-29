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

import sys, threading, platform
import GNS3.Globals as globals
import GNS3.Dynagen.pemuwrapper
from socket import socket, timeout, AF_INET, SOCK_STREAM
from PyQt4 import QtCore, QtGui
from GNS3.Utils import translate, debug


import os
import string

if os.name in ("nt", "dos"):
    exefile = ".exe"
else:
    exefile = ""

def spawn():

#    try:
#        spawnv = os.spawnv
#    except AttributeError:
        # assume it's unix
    pid = os.fork()
    if not pid:

        os.setsid()
        sys.stdout=open("/dev/null", 'w')
        sys.stderr=open("/dev/null", 'w')
        sys.stdin=open("/dev/null", 'r')
        
        GNS3.Dynagen.pemuwrapper.main()
        
#            import os, base64, cStringIO, tarfile
#            import GNS3.Dynagen.pemubin
#    
#            if not os.path.exists(GNS3.Dynagen.pemuwrapper.PEMU_DIR):
#                print "Unpacking pemu binary."
#                f = cStringIO.StringIO(base64.decodestring(GNS3.Dynagen.pemubin.ascii))
#                tar = tarfile.open('dummy', 'r:gz', f)
#                for member in tar.getmembers():
#                    tar.extract(member)
    else:
        print 'Pemu started on ' + str(pid)
#    else:
#        # got spawnv but no spawnp: go look for an executable
#        for path in string.split(os.environ["PATH"], os.pathsep):
#            file = os.path.join(path, program) + exefile
#            try:
#                return spawnv(os.P_NOWAIT, file, (file,) + args)
#            except os.error:
#                pass
#        raise IOError, "cannot find executable"


class PemuThread(threading.Thread):

    def run(self):

        sys.stdout   = sys.__stdout__
        sys.stderr   = sys.__stderr__
        sys.stdin    = sys.__stdin__
        #GNS3.Dynagen.pemuwrapper.main()
        #execfile('/home/grossmj/workspace/gns3-devel/src/GNS3/Dynagen/pemuwrapper.py')
        server = GNS3.Dynagen.pemuwrapper.PEMUWrapperServer(("", 10525), GNS3.Dynagen.pemuwrapper.PEMUWrapperRequestHandler)
        server.serve_forever()

class PemuManager(object):
    """ Pemu class
    """

    def __init__(self):
    
        self.pemu = None
        
#    def __del__(self):
#        """ Shutdown pemu
#        """
#        
#        if self.pemu:
#            self.pemu._Thread__stop()
#       
#    def setDefaults(self):
#        """ Set the default values for the hypervisor manager
#        """
#        
#        dynamips = globals.GApp.systconf['dynamips']
#        self.hypervisor_path = dynamips.path
#        self.hypervisor_wd = dynamips.workdir
#        self.baseConsole = dynamips.baseConsole
#        globals.hypervisor_baseport = dynamips.port
#        globals.GApp.dynagen.globaludp = dynamips.baseUDP
#      
#    def startNewHypervisor(self, port):
#        """ Create a new dynamips process and start it
#        """
#
#        proc = QtCore.QProcess(globals.GApp.mainWindow)
#        if self.hypervisor_wd:
#            # set the working directory
#            proc.setWorkingDirectory(self.hypervisor_wd)
#            
#        # test if an hypervisor is already running on this port
#        s = socket(AF_INET, SOCK_STREAM)
#        s.setblocking(0)
#        s.settimeout(300)
#        try:
#            s.connect(('localhost', port))
#            QtGui.QMessageBox.warning(globals.GApp.mainWindow, 'Hypervisor Manager',  unicode(translate("HypervisorManager", "Hypervisor already running on port %i")) % port) 
#            s.close()
#            globals.hypervisor_baseport += 1
#            return None
#        except:
#            s.close()
#
#        # start dynamips in hypervisor mode (-H)
#        proc.start(self.hypervisor_path,  ['-H', str(port)])
#
#        if proc.waitForStarted() == False:
#            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',  unicode(translate("HypervisorManager", "Can't start Dynamips on port %i")) % port)
#            return None
#
#        hypervisor = {'port': port,
#                            'proc_instance': proc, 
#                            'load': 0}
#
#        self.hypervisors.append(hypervisor)
#        return hypervisor
#    
#    def waitHypervisor(self, hypervisor):
#        """ Wait the hypervisor until it accepts connections
#        """
#
#        # give 15 seconds to the hypervisor to accept connections
#        count = 15
#        progress = None
#        connection_success = False
#        debug("Hypervisor manager: connect on " + str(hypervisor['port']))
#        for nb in range(count + 1):
#            s = socket(AF_INET, SOCK_STREAM)
#            s.setblocking(0)
#            s.settimeout(300)
#            if nb == 3:
#                progress = QtGui.QProgressDialog(unicode(translate("HypervisorManager", "Connecting to an hypervisor on port %i ...")) % hypervisor['port'], 
#                                                                                                                                        translate("HypervisorManager", "Abort"), 0, count, globals.GApp.mainWindow)
#                progress.setMinimum(1)
#                progress.setWindowModality(QtCore.Qt.WindowModal)
#                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
#            if nb > 2:
#                progress.setValue(nb)
#                globals.GApp.processEvents(QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents, 2000)
#                if  progress.wasCanceled():
#                    progress.reset()
#                    break
#            try:
#                s.connect(('localhost', hypervisor['port']))
#            except:
#                s.close()
#                time.sleep(1)
#                continue
#            debug("Hypervisor manager: hypervisor on port " +  str(hypervisor['port']) + " started")
#            connection_success = True
#            break
#
#        if connection_success:
#            s.close()
#            globals.hypervisor_baseport += 1
#            time.sleep(0.2)
#        else:
#            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Hypervisor Manager',  
#                                       unicode(translate("HypervisorManager", "Can't connect to the hypervisor on port %i")) % hypervisor['port'])
#            hypervisor['proc_instance'].close()
#            self.hypervisors.remove(hypervisor)
#            return False
#        if progress:
#            progress.setValue(count)
#            progress.deleteLater()
#            progress = None
#        return True

    def startPemu(self):
        """ Start Pemu
        """

        if self.pemu:
            print 'Pemu is already started'
            return

        if platform.system() == 'Windows':
            try:
                import pywintypes, win32api, win32con, win32process
            except ImportError:
                print >> sys.stderr, "You need pywin32 installed to run pemuwrapper!"

        print 'Start pemu'
        spawn()
##        import os, base64, cStringIO, tarfile
##        import GNS3.Dynagen.pemubin
##
##        if not os.path.exists(GNS3.Dynagen.pemuwrapper.PEMU_DIR):
##            print "Unpacking pemu binary."
##            f = cStringIO.StringIO(base64.decodestring(GNS3.Dynagen.pemubin.ascii))
##            tar = tarfile.open('dummy', 'r:gz', f)
##            for member in tar.getmembers():
##                tar.extract(member)

#        self.pemu = PemuThread() #threading.Thread(None, GNS3.Dynagen.pemuwrapper.main)
#        self.pemu.start()
        print 'Pemu started'
