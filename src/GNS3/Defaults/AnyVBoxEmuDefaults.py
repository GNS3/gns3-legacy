# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2011 GNS3 Development Team (http://www.gns3.net/team).
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

class AnyVBoxEmuDefaults(AbstractDefaults):
    """Abstract class for managing the vitualized device defaults"""

    def __init__(self):

        AbstractDefaults.__init__(self)

        self.default_image = 'None'
        self.default_netcard = 'automatic'
        self.default_nics = 6
        #self.default_ram = 128
        self.default_guestcontrol_user = ''
        self.default_guestcontrol_password = ''
        self.vbox = None
        self.d = None

    def set_hypervisor(self, vbox):
        """ Records an VBox hypervisor
            vbox: VBox object
        """

        self.vbox = vbox
        self.d = 'vbox ' + unicode(self.vbox.host) + ':' + str(self.vbox.port)
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
            
    def set_nics(self, nb):
        """ Set the number of NIC for this device
            nb: int
        """

        self.default_nics = nb

class VBoxDefaults(AnyVBoxEmuDefaults):
    pass
