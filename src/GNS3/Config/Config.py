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

import os
import GNS3.Globals as globals
from GNS3.Config.Objects import iosImageConf, hypervisorConf, libraryConf, qemuImageConf, pixImageConf, junosImageConf, asaImageConf, idsImageConf
from GNS3.Globals.Symbols import SYMBOLS, SYMBOL_TYPES
from GNS3.Node.DecorativeNode import DecorativeNode
from PyQt4 import QtCore
from GNS3.Utils import Singleton, translate

class ConfDB(Singleton, QtCore.QSettings):

    def __init__(self):

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
            if ConfigDefaults.has_key(key):
                return _ConfigDefaults[key]
            # or finally, return None
            return None
        # if conf exist, return it.
        return unicode(value)

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
            else:
                # convertion type not implemented
                pass

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

            img_filename = c.get(cgroup + "/filename", unicode(''))
            img_hypervisors = c.get(cgroup + "/hypervisors", unicode('')).split()

            if img_filename == '':
                continue

            if len(img_hypervisors) == 0:
                img_ref = globals.GApp.systconf['dynamips'].HypervisorManager_binding + ":" + img_filename
            else:
                if len(img_hypervisors) > 1:
                    img_ref = 'load-balanced-on-external-hypervisors:' +   img_filename
                else:
                    (host, port) = img_hypervisors[0].rsplit(':',  1)
                    img_ref = host + ":" + img_filename

            conf = iosImageConf()
            conf.id = int(img_num)
            conf.filename = img_filename
            conf.baseconfig = unicode(c.get(cgroup + "/baseconfig", 'baseconfig.txt'))
            conf.platform = str(c.get(cgroup + "/platform", ''))
            conf.chassis = str(c.get(cgroup + "/chassis", ''))
            conf.idlepc = str(c.get(cgroup + "/idlepc", ''))
            conf.default_ram = int(c.get(cgroup + "/default_ram", 0))
            conf.default =  c.value(cgroup + "/default", QtCore.QVariant(False)).toBool()
            conf.hypervisors = img_hypervisors

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

            hyp_port = c.get(cgroup + "/port",  '7200')
            hyp_host = c.get(cgroup + "/host", unicode(''))
            hyp_wdir = c.get(cgroup + "/working_directory", unicode(''))
            hyp_baseUDP = c.get(cgroup + "/base_udp", '10000')
            hyp_baseConsole = c.get(cgroup + "/base_console", '2000')
            hyp_baseAUX = c.get(cgroup + "/base_aux", '0')

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
            conf.baseConsole = int(hyp_baseConsole)
            conf.baseAUX = int(hyp_baseAUX)
            globals.GApp.hypervisors[img_ref] = conf

            if conf.id >= globals.GApp.hypervisors_ids:
                globals.GApp.hypervisors_ids = conf.id + 1

    def QEMU_images(self):
        """ Load Qemu images settings from config file
        """

        # Loading Qemu image conf
        basegroup = "QEMU.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            
            conf = qemuImageConf()
            conf.id = int(id)
            conf.name = c.get(cgroup + "/name", unicode(''))
            conf.filename = c.get(cgroup + "/filename", unicode(''))
            conf.memory = int(c.get(cgroup + "/memory", 256))
            conf.nic_nb = int(c.get(cgroup + "/nic_nb", 6))
            conf.nic = str(c.get(cgroup + "/nic", 'e1000'))
            conf.options = str(c.get(cgroup + "/options", ''))
            conf.kqemu = c.value(cgroup + "/kqemu", QtCore.QVariant(False)).toBool()
            conf.kvm = c.value(cgroup + "/kvm", QtCore.QVariant(False)).toBool()
            globals.GApp.qemuimages[conf.name] = conf
            
            if conf.id >= globals.GApp.qemuimages_ids:
                globals.GApp.qemuimages_ids = conf.id + 1
                
    def PIX_images(self):
        """ Load PIX images settings from config file
        """

        # Loading PIX image conf
        basegroup = "PIX.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            
            conf = pixImageConf()
            conf.id = int(id)
            conf.name = c.get(cgroup + "/name", unicode(''))
            conf.filename = c.get(cgroup + "/filename", unicode(''))
            conf.memory = int(c.get(cgroup + "/memory", 128))
            conf.nic_nb = int(c.get(cgroup + "/nic_nb", 6))
            conf.nic = str(c.get(cgroup + "/nic", 'e1000'))
            conf.options = str(c.get(cgroup + "/options", ''))
            conf.kqemu = c.value(cgroup + "/kqemu", QtCore.QVariant(False)).toBool()
            conf.key = str(c.get(cgroup + "/key", ''))
            conf.serial = str(c.get(cgroup + "/serial", ''))
            globals.GApp.piximages[conf.name] = conf
            
            if conf.id >= globals.GApp.piximages_ids:
                globals.GApp.piximages_ids = conf.id + 1
                
    def JUNOS_images(self):
        """ Load JunOS images settings from config file
        """

        # Loading JunOS image conf
        basegroup = "JUNOS.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            
            conf = junosImageConf()
            conf.id = int(id)
            conf.name = c.get(cgroup + "/name", unicode(''))
            conf.filename = c.get(cgroup + "/filename", unicode(''))
            conf.memory = int(c.get(cgroup + "/memory", 128))
            conf.nic_nb = int(c.get(cgroup + "/nic_nb", 6))
            conf.nic = str(c.get(cgroup + "/nic", 'e1000'))
            conf.options = str(c.get(cgroup + "/options", ''))
            conf.kqemu = c.value(cgroup + "/kqemu", QtCore.QVariant(False)).toBool()
            conf.kvm = c.value(cgroup + "/kvm", QtCore.QVariant(False)).toBool()
            globals.GApp.junosimages[conf.name] = conf

            if conf.id >= globals.GApp.junosimages_ids:
                globals.GApp.junosimages_ids = conf.id + 1
                
    def ASA_images(self):
        """ Load ASA images settings from config file
        """

        # Loading ASA image conf
        basegroup = "ASA.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            
            conf = asaImageConf()
            conf.id = int(id)
            conf.name = c.get(cgroup + "/name", unicode(''))
            conf.memory = int(c.get(cgroup + "/memory", 256))
            conf.nic_nb = int(c.get(cgroup + "/nic_nb", 6))
            conf.nic = str(c.get(cgroup + "/nic", 'e1000'))
            conf.options = str(c.get(cgroup + "/options", ''))
            conf.kqemu = c.value(cgroup + "/kqemu", QtCore.QVariant(False)).toBool()
            conf.kvm = c.value(cgroup + "/kvm", QtCore.QVariant(False)).toBool()
            conf.initrd = c.get(cgroup + "/initrd", unicode(''))
            conf.kernel = c.get(cgroup + "/kernel", unicode(''))
            conf.kernel_cmdline = c.get(cgroup + "/kernel_cmdline", unicode(''))
            globals.GApp.asaimages[conf.name] = conf

            if conf.id >= globals.GApp.asaimages_ids:
                globals.GApp.asaimages_ids = conf.id + 1
                
    def IDS_images(self):
        """ Load IDS images settings from config file
        """

        # Loading IDS image conf
        basegroup = "IDS.images"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            
            conf = idsImageConf()
            conf.id = int(id)
            conf.image1 = c.get(cgroup + "/image1", unicode(''))
            conf.image2 = c.get(cgroup + "/image2", unicode(''))
            conf.name = c.get(cgroup + "/name", unicode(''))
            conf.memory = int(c.get(cgroup + "/memory", 512))
            conf.nic_nb = int(c.get(cgroup + "/nic_nb", 3))
            conf.nic = str(c.get(cgroup + "/nic", 'e1000'))
            conf.options = str(c.get(cgroup + "/options", ''))
            conf.kqemu = c.value(cgroup + "/kqemu", QtCore.QVariant(False)).toBool()
            conf.kvm = c.value(cgroup + "/kvm", QtCore.QVariant(False)).toBool()
            globals.GApp.idsimages[conf.name] = conf

            if conf.id >= globals.GApp.idsimages_ids:
                globals.GApp.idsimages_ids = conf.id + 1

    def Libraries(self):
        """ Load libraries settings from config file
        """

        # Loading libraries conf
        basegroup = "Symbol.libraries"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        for id in childGroups:

            cgroup = basegroup + '/' + id
            path = c.get(cgroup + "/path", unicode(''))
            
            library_name = os.path.basename(unicode(path))
            if not QtCore.QResource.registerResource(path, ":/" + library_name):
                print unicode(translate("Config", "Can't open library: %s")) % path
                continue
    
            conf = libraryConf()
            conf.path = path
            globals.GApp.libraries[library_name] = conf
            
    def Symbols(self):
        """ Load symbols settings from config file
        """

        # Loading symbols conf
        basegroup = "Symbol.settings"
        c = ConfDB()
        c.beginGroup(basegroup)
        childGroups = c.childGroups()
        c.endGroup()

        loaded_symbols = []
        for id in childGroups:

            cgroup = basegroup + '/' + id
            name = str(c.get(cgroup + "/name", 'default'))
            type =  str(c.get(cgroup + "/type", 'DecorativeNode'))
            object = DecorativeNode
            for (object_class, type_name) in SYMBOL_TYPES.iteritems():
                if type_name == type:
                    object = object_class
                    break

            normal_svg_file = str(c.get(cgroup + "/normal_svg_file", ':/icons/default.svg'))
            selected_svg_file = str(c.get(cgroup + "/selected_svg_file", ':/icons/default.svg'))

            SYMBOLS.append(
                                {'name': name, 'object': object,
                                'normal_svg_file': normal_svg_file,
                                'select_svg_file': selected_svg_file, 
                                'translated': False})

    # Static Methods stuffs
    load_IOSimages = classmethod(IOS_images)
    load_IOShypervisors = classmethod(IOS_hypervisors)
    load_Libraries = classmethod(Libraries)
    load_Symbols = classmethod(Symbols)
