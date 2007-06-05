#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

from PyQt4 import QtCore, QtGui
from Config import ConfDB
from Utils import translate
import time
import __main__

class LocalHypervisor:
    """ LocalHypervisor class
        Start the local hypervisor program
    """
    
    # get access to globals
    main = __main__

    def __init__(self):
    
        self.proc = QtCore.QProcess(self.main.win)
        
        hypervisor_path = ConfDB().get("Dynamips/hypervisor_path", '')
        hypervisor_port = ConfDB().get("Dynamips/hypervisor_port", 7200)
        hypervisor_wd = ConfDB().get("Dynamips/hypervisor_working_directory", '')

        if (hypervisor_path and hypervisor_port):
            #QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotStandardOutput)
            
            if hypervisor_wd:
                self.proc.setWorkingDirectory(hypervisor_wd)
            self.proc.start(hypervisor_path,  ['-H', hypervisor_port])
        
            if self.proc.waitForStarted() == False:
                QtGui.QMessageBox.critical(self.main.win, 'Local hypervisor',  translate("LocalHypervisor", "Can't start the local hypervisor,\n check your configuration file or run gns3-config"))
                return
            
            self.main.integrated_hypervisor = {'port': int(hypervisor_port),
                                               'working_directory': hypervisor_wd,
                                               'dynamips_instance': None}

    def __del__(self):
    
        self.proc.close()

    def slotStandardOutput(self):
        """ Display the standard output of the process
        """

        print str(self.proc.readAllStandardOutput())
