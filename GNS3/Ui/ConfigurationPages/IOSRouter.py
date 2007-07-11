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
# contact@gns3.net
#

from PyQt4 import QtGui
from Form_IOSRouterPage import Ui_IOSRouterPage

class IOSRouter(QtGui.QWidget, Ui_IOSRouterPage):
    """
    Class implementing the IOS router configuration page.
    """
    def __init__(self):

		QtGui.QWidget.__init__(self)
		self.setupUi(self)
		self.setObjectName("IOSRouter")
		
    def save(self):
        
        pass

def create(dlg):
	
    return  IOSRouter()
