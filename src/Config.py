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
import __main__

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
        
    def get(self, key, default_value = None):
        value = self.value(key).toString()
        
        # if value not found is user/system config, or is empty
        if value == "":
            # return default_value if provided
            if default_value is not None:
                return default_value
            # or return the app default if it exist
            if _ConfigDefaults.has_key(key):
                return _ConfigDefaults[key]
            # or finally, return None
            return None
        # if conf exist, return it.
        return str(value)
    
    def set(self, key, value):
        self.setValue(key, QtCore.QVariant(value))

    def getGroupNewNumChild(self, key):
        self.beginGroup(key)
        childGroups = self.childGroups()
        self.endGroup()
        
        max = 0
        for i in childGroups:
            if int(i) + 1 > max:
                max = int(i) + 1
        return (key + '/' + str(max))
    
    
class GNS_Conf(object):
    """ GNS_Conf provide static class method for loading user config
    """
    
    main = __main__
    
    def IOSimages(self):
        """ Load IOSimages settings from config file
        """
        
        print ">> (II) LoadingConf: IOSimages"
        
        # Loading IOS images conf
        basegroup = "IOSimages/image"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()
        
        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num
            
            img_filename = c.get(cgroup + "/filename", '')
            img_hyp_host = c.get(cgroup + "/hypervisor_host", '')
            img_hyp_host_str = img_hyp_host
            if img_hyp_host_str == "localhost":
                img_hyp_host = None
            
            if img_filename == '' or img_hyp_host == '':
                continue
            
            img_ref = str(img_hyp_host_str + ":" + img_filename)
            self.main.ios_images[img_ref] = {
                    'confkey': cgroup,
                    'filename' : img_filename,
                    'platform' : c.get(cgroup + "/platform", ''),
                    'chassis': c.get(cgroup + "/chassis", ''),
                    'idlepc' : c.get(cgroup + "/idlepc", ''),
                    'hypervisor_host' : img_hyp_host,
                    'hypervisor_port' : c.get(cgroup + "/hypervisor_port", ''),
                    'working_directory' : c.get(cgroup + "/working_directory", '')                
            }


        # Loading IOS hypervisors conf
        # TODO: LoadingConfIOSHypervisors
  
    # Static Methods stuffs
    load_IOSimages = classmethod(IOSimages)