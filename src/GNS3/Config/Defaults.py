# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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

conf_iosImage_defaults = {
    'id': -1,
    'filename': '',
    'platform': '',
    'chassis': '',
    'idlepc': '',
    'hypervisor_host': '',
    'hypervisor_port': 7200,
    'default': False
}

conf_iosImage_types = {
    'id': int,
    'filename': unicode,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'hypervisor_host': unicode,
    'hypervisor_port': int,
    'default': bool
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10000, 
    'baseConsole': 2000
}

conf_hypervisor_types = {
    'id': int,
    'host': unicode,
    'port': int,
    'workdir': unicode, 
    'baseUDP': int,
    'baseConsole': int
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'term_cmd': '',
    'baseUDP': 10000, 
    'baseConsole': 2000, 
    'ghosting': True,
    'sparsemem': False,
    'mmap': True, 
    'memory_limit': 512, 
    'udp_incrementation': 100, 
    'import_use_HypervisorManager': True,
}

conf_systemDynamips_types = {
    'path': unicode,
    'port': int,
    'workdir': unicode,
    'term_cmd': unicode,
    'baseUDP': int,
    'baseConsole': int, 
    'ghosting': bool, 
    'sparsemem': bool,
    'mmap': bool,
    'memory_limit': int, 
    'udp_incrementation': int,  
    'import_use_HypervisorManager': bool,
}

conf_systemGeneral_defaults = {
    'lang': 'en',
    'project_path': '.',
    'ios_path': '.',
    'status_points': True, 
    'manual_connection': False
}

conf_systemGeneral_types = {
    'lang': unicode,
    'project_path': unicode,
    'ios_path': unicode,
    'status_points': bool, 
    'manual_connection': bool
}

conf_systemCapture_defaults = {
    'workdir': '',
    'cap_cmd': '', 
    'auto_start': True,
}

conf_systemCapture_types = {
    'workdir': unicode,
    'cap_cmd': unicode,
    'auto_start': bool
}

conf_systemPemu_defaults = {
    'default_pix_image': '',
}

conf_systemPemu_types = {
    'default_pix_image': unicode,
}
