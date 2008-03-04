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

import os
import GNS3.Globals as globals
from GNS3.Defaults.AbstractDefaults import AbstractDefaults

class FWDefaults(AbstractDefaults):
    """Abstract class for managing the FW defaults"""

    def __init__(self):

        AbstractDefaults.__init__(self)

        self.default_image = 'None'
        self.default_serial = '0x12345678'
        self.default_key = '0x00000000,0x00000000,0x00000000,0x00000000'
        self.default_ram = 128
        self.pemu = None
        self.d = None

    def set_hypervisor(self, pemu):
        """ Records an pemu hypervisor
            pemu: Pemu object
        """

        self.pemu = pemu
        self.d = 'pemu ' + str(self.pemu.host)
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
