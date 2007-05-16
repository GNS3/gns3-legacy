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
import time
import __main__

class LocalHypervisor():
    """ LocalHypervisor class
        Start the local hypervisor program
    """
    
    # get access to globals
    main = __main__

    def __init__(self):
    
        self.proc = QtCore.QProcess(self.main.win)
        #QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotStandardOutput)
        #QtCore.QObject.connect(self.proc, QtCore.SIGNAL('error(QProcess::ProcessError)'), self.slotProcessError)
        self.proc.start('/home/grossmj/workspace/gns3/dynamips/dynamips-0.2.7-RC3-x86.bin',  ['-H', '7200'])
        #time.sleep(0.5)
        
        if self.proc.waitForStarted() == False:
            print 'Local hypervisor not started !'
            return
        print 'Local hypervisor started'

    def __del__(self):
    
        self.proc.close()

    def slotStandardOutput(self):
        """ Display the standard output of the process
        """

        print str(self.proc.readAllStandardOutput())
    
    def slotProcessError(self):

        print 'HYPERVISOR ERROR !'
