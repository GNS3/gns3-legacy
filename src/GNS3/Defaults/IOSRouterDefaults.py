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

import sys, os
from GNS3.Defaults.AbstractDefaults import AbstractDefaults

class IOSRouterDefaults(AbstractDefaults):
    """Abstract class for managing the IOSRouter defaults"""

    def __init__(self):

        AbstractDefaults.__init__(self)

        self.chassis = 'None'
        self.default_image = 'None'
        self.default_ghostios = 'False'
        self.default_jitsharing = 'False'
        self.default_cnfg = 'None'
        self.default_conf = 'None'
        self.default_confreg = '0x2102'
        self.default_aux = 'None'
        self.default_idlepc = 'None'
        self.default_idlemax = 1500
        self.default_idlesleep = 30
        self.default_exec_area = 'None'
        self.default_mmap = True
        self.default_sparsemem = 'False'
        self.hypervisor = None
        self.d = None

    def set_hypervisor(self,  hypervisor):
        """ Records a hypervisor
            hypervisor: Dynamips object
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
            # basename doesn't work on Unix with Windows paths, so let's use this little trick
            if not sys.platform.startswith('win') and image[1] == ":":
                image = image[2:]
                image = image.replace("\\", "/")
            imagename = os.path.basename(image)
            #try to find idlepc value for this image in idlepc db
            if self.dynagen.useridledb:
                if imagename in self.dynagen.useridledb:
                    print imagename + ' found in user idlepc database\nSetting idlepc value to ' + self.dynagen.useridledb[imagename]
                    self.config['idlepc'] = self.dynagen.useridledb[imagename]

    def set_ghostios(self, ghostios):
        """ Enable or disable ghostios feature
        """

        if self.default_ghostios == ghostios:
            if self.config.has_key('ghostios'):
                del self.config['ghostios']
        else:
            self.config['ghostios'] = bool(ghostios)

    def set_jitsharing(self, jitsharing):
        """ Enable or disable JIT blocks sharing feature
        """

        if self.default_jitsharing == jitsharing:
            if self.config.has_key('jitsharing'):
                del self.config['jitsharing']
        else:
            self.config['jitsharing'] = bool(jitsharing)
