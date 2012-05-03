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

import GNS3.Globals as globals

class AbstractDefaults(object):
    """ Abstract class for managing the device defaults """

    model = None

    def __init__(self):

        self.dynagen = globals.GApp.dynagen
        self.config = None

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
