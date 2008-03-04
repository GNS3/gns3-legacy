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
