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

conf_qemuImage_defaults = {
    'id': -1,
    'name': '',
    'filename': '',
    'memory': 128,
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
    'ghosting': True,
    'jitsharing': False,
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
    'jitsharing': bool,
    'sparsemem': bool,
    'mmap': bool,
    'memory_limit': int,
    'udp_incrementation': int,
    'import_use_HypervisorManager': bool,
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
    'default_qemu_image': '',
    'default_qemu_memory': 256,
    'default_qemu_nic': 'e1000',
    'default_qemu_options': '',
    'default_qemu_kqemu': False,
    'default_qemu_kvm': False,
    'default_pix_image': '',
    'default_pix_memory': 128,
    'default_pix_nic': 'e1000',
    'default_pix_options': '',
    'default_pix_kqemu': False,
    'default_pix_key': '',
    'default_pix_serial': '',
    'default_junos_image': '',
    'default_junos_memory': 96,
    'default_junos_nic': 'e1000',
    'default_junos_options': '',
    'default_junos_kqemu': False,
    'default_junos_kvm': False,
    'default_asa_memory': 256,
    'default_asa_nic': 'e1000',
    'default_asa_options': '',
    'default_asa_kqemu': False,
    'default_asa_kvm': False,
    'default_asa_kernel': '',
    'default_asa_initrd': '',
    'default_asa_kernel_cmdline': '',
    'default_ids_image1': '',
    'default_ids_image2': '',
    'default_ids_memory': 512,
    'default_ids_nic': 'e1000',
    'default_ids_options': '',
    'default_ids_kqemu': False,
    'default_ids_kvm': False,
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
    'default_qemu_image': unicode,
    'default_qemu_memory': int,
    'default_qemu_nic': str,
    'default_qemu_options': str,
    'default_qemu_kqemu': bool,
    'default_qemu_kvm': bool,
    'default_pix_image': unicode,
    'default_pix_memory': int,
    'default_pix_nic': str,
    'default_pix_options': str,
    'default_pix_kqemu': bool,
    'default_pix_key': str,
    'default_pix_serial': str,
    'default_junos_image': unicode,
    'default_junos_memory': int,
    'default_junos_nic': str,
    'default_junos_options': str,
    'default_junos_kqemu': bool,
    'default_junos_kvm': bool,
    'default_asa_memory': int,
    'default_asa_nic': str,
    'default_asa_options': str,
    'default_asa_kqemu': bool,
    'default_asa_kvm': bool,
    'default_asa_kernel': unicode,
    'default_asa_initrd': unicode,
    'default_asa_kernel_cmdline': unicode,
    'default_ids_image1': unicode,
    'default_ids_image2': unicode,
    'default_ids_memory': int,
    'default_ids_nic': str,
    'default_ids_options': str,
    'default_ids_kqemu': bool,
    'default_ids_kvm': bool,
}
