# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

SysConfigDir = "/etc/gns3"
UsrConfigDir = "~/.gns3"

conf_library_defaults = {
    'path': '',
}

conf_library_types = {
    'path': unicode,
}

conf_iosImage_defaults = {
    'id': -1,
    'filename': '',
    'baseconfig': '',
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
    'baseconfig': unicode,
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
    'baseAUX': 2100,
    'used_ram':0, 
}

conf_hypervisor_types = {
    'id': int,
    'host': unicode,
    'port': int,
    'workdir': unicode,
    'baseUDP': int,
    'baseConsole': int,
    'baseAUX': int,
    'used_ram': int, 
}

conf_qemuImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 256,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kqemu': False,
    'kvm': False
}

conf_qemuImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kqemu': bool,
    'kvm': bool
}

conf_pixImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 128,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kqemu': False,
    'key': '',
    'serial': ''
}

conf_pixImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kqemu': bool,
    'key': str,
    'serial': str
}

conf_junosImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 96,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kqemu': False,
    'kvm': False
}

conf_junosImage_types = {
    'id': int,
    'name': unicode,
    'filename': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kqemu': bool,
    'kvm': bool
}

conf_asaImage_defaults = {
    'id': -1,
    'name': '',
    'memory': 256,
    'nib_nb': 6,
    'nic': 'e1000',
    'options': '',
    'kqemu': False,
    'kvm': False,
    'kernel': '',
    'initrd': '',
    'kernel_cmdline': ''
}

conf_asaImage_types = {
    'id': int,
    'name': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kqemu': bool,
    'kvm': bool,
    'kernel': unicode,
    'initrd': unicode,
    'kernel_cmdline': unicode,
}

conf_idsImage_defaults = {
    'id': -1,
    'name': '',
    'image1': '',
    'image2': '',
    'memory': 512,
    'nib_nb': 3,
    'nic': 'e1000',
    'options': '',
    'kqemu': False,
    'kvm': False
}

conf_idsImage_types = {
    'id': int,
    'name': unicode,
    'image1': unicode,
    'image2': unicode,
    'memory': int,
    'nic_nb': int,
    'nic': str,
    'options': str,
    'kqemu': bool,
    'kvm': bool
}

conf_systemDynamips_defaults = {
    'path': '',
    'port': 7200,
    'workdir': '',
    'clean_workdir': True, 
    'baseUDP': 10000,
    'baseConsole': 2000,
    'baseAUX': 2100,
    'ghosting': True,
    'jitsharing': False,
    'sparsemem': False,
    'mmap': True,
    'memory_limit': 512,
    'udp_incrementation': 100,
    'import_use_HypervisorManager': True,
    'allocateHypervisorPerIOS': True,
    'HypervisorManager_binding': u'localhost', 
}

conf_systemDynamips_types = {
    'path': unicode,
    'port': int,
    'workdir': unicode,
    'clean_workdir': bool, 
    'baseUDP': int,
    'baseConsole': int,
    'baseAUX': int,
    'ghosting': bool,
    'jitsharing': bool,
    'sparsemem': bool,
    'mmap': bool,
    'memory_limit': int,
    'udp_incrementation': int,
    'import_use_HypervisorManager': bool,
    'allocateHypervisorPerIOS': bool,
    'HypervisorManager_binding': unicode, 
}

conf_systemGeneral_defaults = {
    'lang': 'en',
    'project_startup': True,
    'relative_paths': True,
    'slow_start': 0,
    'autosave': 60,
    'term_cmd': '',
    'use_shell': True,
    'project_path': '.',
    'ios_path': '.',
    'status_points': True,
    'manual_connection': False, 
    'scene_width': 2000, 
    'scene_height': 1000, 
}

conf_systemGeneral_types = {
    'lang': unicode,
    'project_startup': bool,
    'relative_paths': bool,
    'slow_start': int,
    'autosave': int,
    'use_shell': bool,
    'term_cmd': unicode,
    'project_path': unicode,
    'ios_path': unicode,
    'status_points': bool,
    'manual_connection': bool, 
    'scene_width': int, 
    'scene_height': int, 
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

conf_systemQemu_defaults = {
    'qemuwrapper_path':'',
    'qemuwrapper_workdir':'',
    'qemu_path':'qemu',
    'qemu_img_path':'qemu-img',
    'external_hosts':[],
    'enable_QemuManager': True,
    'import_use_QemuManager': True,
    'QemuManager_binding': u'localhost',
    'qemuwrapper_port': 10525,
    'qemuwrapper_baseUDP': 20000,
    'qemuwrapper_baseConsole': 3000,
}

conf_systemQemu_types = {
    'qemuwrapper_path': unicode,
    'qemuwrapper_workdir': unicode,
    'qemu_path': unicode,
    'qemu_img_path': unicode,
    'external_hosts': list,
    'enable_QemuManager': bool,
    'import_use_QemuManager': bool,
    'QemuManager_binding': unicode,
    'qemuwrapper_port': int,
    'qemuwrapper_baseUDP': int,
    'qemuwrapper_baseConsole': int,
}
