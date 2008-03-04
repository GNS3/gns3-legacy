# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2008 GNS3 Dev Team
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

from GNS3.Config import Defaults

class ConfigObject(object):
    def __init__(self):
        self.conf = {}
        self.types = {}

    def __getPropertiesFunctions(cls, name):
        obj = dir(cls)


    def __getattr__(self, name):
        if self.__dict__['conf'].has_key(name):
            # Call the getter function, if there is one, else
            # return the value directly from the `conf' dictionnary.
            try:
                method_name = "get_" + name
                method = getattr(self, method_name)
                if callable(method):
                    return method()
            except:
                return self.__dict__['conf'][name]
        else:
            # In case the attribute is not part of the conf,
            # behave like the normal __getattr__
            super(ConfigObject, self).__getattr__(name)

    def __setattr__(self, name, value):
        # We must bypass `conf' and `types' attributes, because we use
        # it in this function !
        if name == 'conf' or not self.__dict__['conf'].has_key(name):
            return super(ConfigObject, self).__setattr__(name, value)

        if self.__dict__['conf'].has_key(name):
            # Check the `value' type
            if not type(value) == self.__dict__['types'][name]:
                raise AttributeError, "value of `%s' must be of type: %s" \
                    % (name, str(self.__dict__['types'][name]))

            # Call the setter function is one, else assign the value directly
            try:
                method_name = "set_" + name
                method = getattr(self, method_name)
                if callable(method):
                    return method(value)
            except:
                self.__dict__['conf'][name] = value
        else:
            # In case the attribute is not part of the conf,
            # behave like the normal __setattr__
            super(ConfigObject, self).__setattr__(name, value)

        # Post `set' function
        try:
            method_name = "postset_all"
            method = getattr(self, method_name)
            if callable(method):
                return method(name, value)
        except:
            # silently ignore errors
            pass

class iosImageConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_iosImage_defaults.copy()
        self.types = Defaults.conf_iosImage_types

class hypervisorConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_hypervisor_defaults.copy()
        self.types = Defaults.conf_hypervisor_types

class systemDynamipsConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_systemDynamips_defaults.copy()
        self.types = Defaults.conf_systemDynamips_types

class systemGeneralConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_systemGeneral_defaults.copy()
        self.types = Defaults.conf_systemGeneral_types

class systemCaptureConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_systemCapture_defaults.copy()
        self.types = Defaults.conf_systemCapture_types

class systemPemuConf(ConfigObject):
    def __init__(self):
        ConfigObject.__init__(self)
        self.conf = Defaults.conf_systemPemu_defaults.copy()
        self.types = Defaults.conf_systemPemu_types
