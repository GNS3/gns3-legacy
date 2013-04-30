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

from GNS3.Node.IOSRouter import IOSRouter
from GNS3.Defaults.IOSRouter3700Defaults import IOSRouter3700Defaults

class IOSRouter3700(IOSRouter, IOSRouter3700Defaults):
    """ IOSRouter class implementing a IOS router c3700 platform
    """

    def __init__(self, renderer_normal, renderer_select):

        IOSRouter.__init__(self, renderer_normal, renderer_select)
        IOSRouter3700Defaults.__init__(self)
        self.platform = 'c3700'

    def get_chassis(self):
        """ Returns router model
        """

        assert(self.router)
        return ('')

    def create_router(self):

        IOSRouter.create_router(self)
        # EtherSwitch router special case: automatically assign NM-16ESW in slot 1
        if not self.default_symbol:
            config = self.create_config()
            config['slots'][1] = 'NM-16ESW'
            self.set_config(config)

            
