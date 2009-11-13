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

from GNS3.Defaults.AbstractDefaults import AbstractDefaults

class AnyEmuDefaults(AbstractDefaults):
    """Abstract class for managing the FW defaults"""

    def __init__(self):

        AbstractDefaults.__init__(self)

        self.default_image = 'None'
        self.default_ram = 128
        self.qemu = None
        self.d = None

    def set_hypervisor(self, qemu):
        """ Records an Qemu hypervisor
            qemu: Qemu object
        """

        self.qemu = qemu
        self.d = 'qemu ' + str(self.qemu.host)
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

class FWDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)
        self.default_serial = '0x12345678'
        self.default_key = '0x00000000,0x00000000,0x00000000,0x00000000'

class ASADefaults(AnyEmuDefaults):
    pass
    
class JunOSDefaults(AnyEmuDefaults):
    pass
