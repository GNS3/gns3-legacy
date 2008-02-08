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

import os
import GNS3.Globals as globals

class AbstractDefaults:
    """Abstract class for managing the device Defaults"""

    def __init__(self):
    
        self.dynagen = globals.GApp.dynagen
        self.chassis = 'None'
        self.default_image = 'None'
        self.default_ghostios = 'False'
        self.default_cnfg = 'None'
        self.default_conf = 'None'
        self.default_confreg = '0x2102'
        self.default_aux = 'None'
        self.default_image = 'None'
        self.default_idlepc = 'None'
        self.default_exec_area = 'None'
        self.default_mmap = True
        self.default_sparsemem = 'False'
        self.config = None
        self.d = None
        self.hypervisor = None
        self.model = None

    def set_hypervisor(self,  hypervisor):
        """ Records an hypervisor
            hypervisor: object
        """
    
        self.hypervisor = hypervisor
        self.d = self.hypervisor.host + ':' + str(self.hypervisor.port)
        self.config = self.dynagen.defaults_config[self.d]

    def set_image(self, image, model):
        """ Set a image path
            image: string
            model: string
        """

        self.model = model
        if model in self.config:
            self.config = self.config[model]
        else:
            self.config[model] = {}
            self.config = self.config[model]

        if self.default_image == image:
            if self.config.has_key('image'):
                del self.config['image']
        else:
            self.config['image'] = image
            #try to find idlepc value for this image in idlepc db
            imagename = os.path.basename(image)
            if self.dynagen.useridledb:
                if imagename in self.dynagen.useridledb:
                    print imagename + ' found in user idlepc database\nSetting idlepc value to ' + self.dynagen.useridledb[imagename]
                    self.config['idlepc'] = self.dynagen.useridledb[imagename]

    def set_int_option(self, option, argument):
        """ Set integer type option in config
        """

        option_value = int(argument)
        if getattr(self, 'default_' + option) == option_value:
            if self.config.has_key(option):
                del self.config[option]
        else:
            self.config[option] = option_value

    def set_string_option(self, option, argument):
        """ Set string type option in config
        """

        option_value = argument
        if getattr(self, 'default_' + option) == option_value:
            if self.config.has_key(option):
                del self.config[option]
        else:
            self.config[option] = option_value

    def set_ghostios(self, ghostios):
        """ghostios = {True|False}
\tenable or disable IOS ghosting"""

        if self.default_ghostios == ghostios:
            if self.config.has_key('ghostios'):
                del self.config['ghostios']
        else:
            self.config['ghostios'] = bool(ghostios)
