# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
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
# http://www.gns3.net/contact
#

from GNS3.Defaults.AbstractDefaults import AbstractDefaults

class AnyEmuDefaults(AbstractDefaults):
    """Abstract class for managing the emulated device defaults"""

    def __init__(self):

        AbstractDefaults.__init__(self)

        self.default_image = 'None'
        self.default_netcard = 'rtl8139'
        self.default_flavor = 'Default'
        self.default_nics = 6
        self.default_usermod = False
        self.default_kvm = False
        self.default_monitor = False
        self.default_options = ''
        self.default_ram = 256
        self.qemu = None
        self.d = None

    def set_hypervisor(self, qemu):
        """ Records an Qemu hypervisor
            qemu: Qemu object
        """

        self.qemu = qemu
        self.d = 'qemu ' + unicode(self.qemu.host) + ':' + str(self.qemu.port)
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

class QemuDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)

class PIXDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)
        self.default_serial = '0x12345678'
        self.default_key = '0x00000000,0x00000000,0x00000000,0x00000000'

class ASADefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)
        self.default_initrd = 'None'
        self.default_kernel = 'None'
        self.default_kernel_cmdline = 'None'

class JunOSDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)

class AWPDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)
        self.default_initrd = 'None'
        self.default_kernel = 'None'
        self.default_rel = 'None'
        self.default_kernel_cmdline = 'None'

class IDSDefaults(AnyEmuDefaults):
    def __init__(self):
        AnyEmuDefaults.__init__(self)
        self.default_image1 = 'None'
        self.default_image2 = 'None'

