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

import sys

try:
    import PyQt4
except ImportError:
    import tkMessageBox
    tkMessageBox.showwarning("PyQt", "PyQt is not installed, please see the README\n")
    sys.stderr.write('PyQt is not installed, please see the README')
    sys.exit(False)

sys.path.append("./src")
from Main import *
import traceback

print   '''Welcome to gns3 !
  _____ _   _  _____      ____  
 / ____| \ | |/ ____|    |___ \ 
| |  __|  \| | (___ ______ __) |
| | |_ | . ` |\___ \______|__ < 
| |__| | |\  |____) |     ___) |
 \_____|_| \_|_____/     |____/ 
'''

def exceptionHook(type, value, tb):
        
        if exceptionHook == None:
            return
        lines = traceback.format_exception(type, value, tb)
        print "---------------------Traceback lines-----------------------"
        print "\n" . join(lines)
        print "-----------------------------------------------------------"
        logfile = open('exception.log','a')
        logfile.write("\n" . join(lines))
        logfile.close()

sys.excepthook=exceptionHook
Main(sys.argv)

