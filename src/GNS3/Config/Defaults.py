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

SysConfigDir = "/etc/gns3"
UsrConfigDir = "~/.gns3"

conf_iosImage_defaults = {
    'id': -1,
    'filename': '',
    'platform': '',
    'chassis': '',
    'idlepc': '',
    'default_ram': 0,
    'hypervisors': [], 
    'default': False
}

conf_iosImage_types = {
    'id': int,
    'filename': unicode,
    'platform': str,
    'chassis': str,
    'idlepc': str,
    'default_ram': int, 
    'hypervisors': list, 
    'default': bool
}

conf_hypervisor_defaults = {
    'id': -1,
    'host': '',
    'port': 7200,
    'workdir': '',
    'baseUDP': 10000,
    'baseConsole': 2000, 
    'used_ram':0, 
}

conf_hypervisor_types = {
    'id': int,
    'host': unicode,
    'port': int,
    'workdir': unicode,
    'baseUDP': int,
    'baseConsole': int, 
    'used_ram': int, 
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'clean_workdir': True, 
    'baseUDP': 10000,
    'baseConsole': 2000,
    'ghosting': True,
    'sparsemem': False,
    'mmap': True,
    'memory_limit': 512,
    'udp_incrementation': 100,
    'import_use_HypervisorManager': True,
    'HypervisorManager_binding': u'localhost', 
}

conf_systemDynamips_types = {
    'path': unicode,
    'port': int,
    'workdir': unicode,
    'clean_workdir': bool, 
    'baseUDP': int,
    'baseConsole': int,
    'ghosting': bool,
    'sparsemem': bool,
    'mmap': bool,
    'memory_limit': int,
    'udp_incrementation': int,
    'import_use_HypervisorManager': bool,
    'HypervisorManager_binding': unicode, 
}

conf_systemGeneral_defaults = {
    'lang': 'en',
    'term_cmd': '',
    'use_shell': True,
    'project_path': '.',
    'ios_path': '.',
    'status_points': True,
    'manual_connection': False
}

conf_systemGeneral_types = {
    'lang': unicode,
    'use_shell': bool,
    'term_cmd': unicode,
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
    'pemuwrapper_path':'',
    'pemuwrapper_workdir':'',
    'external_host':'',
    'enable_PemuManager': True,
    'import_use_PemuManager': True,
    'PemuManager_binding': u'localhost', 
    'default_pix_image': '',
    'default_pix_key':'',
    'default_pix_serial':'',
    'default_base_flash':'',
}

conf_systemPemu_types = {
    'pemuwrapper_path': unicode,
    'pemuwrapper_workdir': unicode,
    'external_host': unicode,
    'enable_PemuManager': bool,
    'import_use_PemuManager': bool,
    'PemuManager_binding': unicode,
    'default_pix_image': unicode,
    'default_pix_key': str,
    'default_pix_serial': str,
    'default_base_flash': unicode,
}
