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

class IOSRouter3600Defaults(IOSRouterDefaults):
    """ Class for managing the defaults of Cisco 3600 platform
    """

    def __init__(self):

        IOSRouterDefaults.__init__(self)

        #fill 3600 defaults
        self.default_ram = 128
        self.default_nvram = 128
        self.default_disk0 = 0
        self.default_disk1 = 0
        self.default_iomem = 'None'

