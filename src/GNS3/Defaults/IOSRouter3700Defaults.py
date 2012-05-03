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

from GNS3.Defaults.IOSRouterDefaults import IOSRouterDefaults

class IOSRouter3700Defaults(IOSRouterDefaults):
    """ Class for managing the defaults of Cisco 3700 platform
    """

    def __init__(self):

        IOSRouterDefaults.__init__(self)

        #fill 3700 defaults
        self.default_ram = 128
        self.default_nvram = 55
        self.default_disk0 = 16
        self.default_disk1 = 0

    def set_image(self, image, model):
        """ Set a image path
            image: string
            model: string
        """

        IOSRouterDefaults.set_image(self, image, model)
        # 3745 has a different default nvram
        if model == '3745':
            self.default_nvram = 151
