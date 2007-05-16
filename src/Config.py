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

from PyQt4 import QtCore
from Utils import Singleton

_corpname = 'EPITECH'
_appname = 'GNS-3'
_ConfigDefaults = {
    'crash/1': 'boooum'
}

class ConfDB(Singleton, QtCore.QSettings):    

    def __init__(self):
        global _corpname, _appname
        QtCore.QSettings.__init__(self, _corpname, _appname)
    
    def __del__(self):
        self.sync()
        
    def get(self, key):
        value = self.value(key).toString()
        if value == "":
            if _ConfigDefaults.has_key(key):
                value = _ConfigDefaults[key]
            else:
                raise ">>(EE): No default value for config key ``" + key + "''"
        print ">> ConfDB[" + key + "] = " + str(value)
        
    def set(self, key, value):
        self.setValue(key, QtCore.QVariant(value))
        print ">> ConfDB[" + key + "] =<< " + str(value)
