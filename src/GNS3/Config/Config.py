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

import sys, time
import GNS3.Globals as globals
import GNS3.Config.Defaults as Defaults
from GNS3.Config.Objects import iosImageConf, hypervisorConf
from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Link.Serial import Serial
from GNS3.Link.Ethernet import Ethernet
from PyQt4 import QtCore
from GNS3.Utils import Singleton
from GNS3.Config.Objects import hypervisorConf, iosImageConf

class ConfDB(Singleton, QtCore.QSettings):

    def __init__(self):
        #QtCore.QSettings.__init__(self, "./gns3.conf", QtCore.QSettings.IniFormat)
        QtCore.QSettings.__init__(self, QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "gns3")

    def __del__(self):
        self.sync()

    def delete(self, key):
        """ Delete a config key

        Same as QSettings.remove()
        """
        self.remove(key)

    def get(self, key, default_value = None):
        """ Get a config value for a specific key

        Get the config value for `key' key
        If no value exists:
          1) try to return default_value (if providen)
          2) try to find a default value into apps _ConfigDefaults dict.
          3) return None
        """
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
        return unicode(value,  'utf-8')

    def set(self, key, value):
        """ Set a value from a specific key
        """
        self.setValue(key, QtCore.QVariant(value))

    def getGroupNewNumChild(self, key):
        """ Get the maximum+1 numeric key from the specified config key group.

        Under config group `key', find the key with the max numeric value,
        then return max+1
        """
        self.beginGroup(key)
        childGroups = self.childGroups()
        self.endGroup()

        max = 0
        for i in childGroups:
            if int(i) + 1 > max:
                max = int(i) + 1
        return (key + '/' + str(max))

    def getGroupDict(self, key, fields_dict = None):
        """ Get all keys from a given `key' config group

        If fields_dict is providen, like { 'key': 'int' },
        only theses keys will be return. Moreover in this
        dictionnary, values represent the 'convertion' type
        that will be applied.
        """
        __values = {}
        self.beginGroup(key)

        childKeys = self.childKeys()
        for child in childKeys:
            # child key need to be a string
            child = str(child)
            # If fields_dict providen, check if the current
            # value is wanted or not
            if fields_dict != None and not fields_dict.has_key(child):
                continue

            child_value = self.value(child)
            # Try to find a suitable method for converting
            # conf value to desired type
            # default: provide a string
            conv_to = "string"
            if fields_dict != None \
                and fields_dict.has_key(child) and fields_dict[child] != '':
                conv_to = fields_dict[child]

            # Do the convertion, and assign the value
            if   conv_to == "string": __values[child] = str(child_value.toString())
            elif conv_to == "int":    __values[child] = int(child_value.toInt())
            else: raise "convertion type not implemented"

        self.endGroup()
        return __values

    def setGroupDict(self, key, dict_values):
        """ Set config keys/values under a specific config group

        All key/value pair present in `dict_values' will be saved
        in config under `key' group
        """

        self.beginGroup(key)
        for key in dict_values.keys():
            key_str = str(key)
            value_str = str(dict_values[key])
            if value_str == "None": value_str = ""
            self.set(key_str, value_str)
        self.endGroup()

class GNS_Conf(object):
    """ GNS_Conf provide static class method for loading user config
    """

    def IOS_images(self):
        """ Load IOS images settings from config file
        """

        # Loading IOS images conf
        basegroup = "IOS.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num

            img_filename = c.get(cgroup + "/filename", unicode('',  'utf-8'))
            img_hyp_host = c.get(cgroup + "/hypervisor_host", unicode('',  'utf-8'))
            
            if img_filename == '':
                continue

            if img_hyp_host == '':
                img_ref = "localhost:" + img_filename
            else:
                img_ref = img_hyp_host + ":" + img_filename

            conf = iosImageConf()
            conf.id = int(img_num)
            conf.filename = img_filename
            conf.platform = str(c.get(cgroup + "/platform", ''))
            conf.chassis = str(c.get(cgroup + "/chassis", ''))
            conf.idlepc = str(c.get(cgroup + "/idlepc", ''))
            conf.hypervisor_host = c.get(cgroup + "/hypervisor_host",  unicode('',  'utf-8'))
            conf.hypervisor_port = int(c.get(cgroup + "/hypervisor_port",  0))
            conf.default =  c.value(cgroup + "/default", QtCore.QVariant(False)).toBool()

            globals.GApp.iosimages[img_ref] = conf

            if conf.id >= globals.GApp.iosimages_ids:
                globals.GApp.iosimages_ids = conf.id + 1

    def IOS_hypervisors(self):
        """ Load IOS hypervisors settings from config file
        """

        # Loading IOS images conf
        basegroup = "IOS.hypervisors"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for img_num in childGroups:
            cgroup = basegroup + '/' + img_num

            hyp_port = c.get(cgroup + "/port", '')
            hyp_host = c.get(cgroup + "/host", unicode('',  'utf-8'))
            hyp_wdir = c.get(cgroup + "/working_directory", unicode('',  'utf-8'))
            hyp_baseUDP = c.get(cgroup + "/base_udp", '')

            # We need at least `hyp_host' and `hyp_port' to be set
            if hyp_host == '' or hyp_port == '':
                continue

            img_ref = hyp_host + ':' + hyp_port

            conf = hypervisorConf()
            conf.id = int(img_num)
            conf.host = hyp_host
            conf.port = int(hyp_port)
            conf.workdir = hyp_wdir
            conf.baseUDP = int(hyp_baseUDP)
            globals.GApp.hypervisors[img_ref] = conf

            if conf.id >= globals.GApp.hypervisors_ids:
                globals.GApp.hypervisors_ids = conf.id + 1

    # Static Methods stuffs
    load_IOSimages = classmethod(IOS_images)
    load_IOShypervisors = classmethod(IOS_hypervisors)
