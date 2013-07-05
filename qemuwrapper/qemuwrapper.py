#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (c) 2007-2012 Thomas Pani & Jeremy Grossmann
#
# Contributions by Pavel Skovajsa & Alexey Eromenko "Technologov"
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

#This module is used for actual control of VMs, sending commands to the hypervisor.
#This is the server part, it can be started manually, or automatically from "QemuManager"
#Client part is named "qemu_lib". (dynagen component)

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

#qemuprotocol: 0=old, 1=experimental
qemuprotocol = 1

import csv
import cStringIO
import os
import re
import platform
import select
import socket
import subprocess
import sys
import threading
import SocketServer
import time
import random
import ctypes
import hashlib
import shutil

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    sys.stderr.write("Can't set default encoding to utf-8\n")

if debuglevel > 0:
    if platform.system() == 'Windows':
        debugfilename = "C:\TEMP\gns3-qemuwrapper-log.txt"
    else:
        debugfilename = "/tmp/gns3-qemuwrapper-log.txt"
    try:
        dfile = open(debugfilename, 'wb')
    except:
        dfile = 0
        print "WARNING: log file cannot be created !"
    if dfile:
        print "Log file = %s" % str(debugfilename)

def debugmsg(level, message):
    if debuglevel == 0:
        return
    if debuglevel >= level:
        print message
        if dfile:
            #In python 2.6, print with redirections always uses UNIX line-ending,
            # so I must add os-neutral line-endings.
            print >> dfile, message,
            dfile.write(os.linesep)
            dfile.flush()

msg = "WELCOME to qemuwrapper.py"
debugmsg(2, msg)

__author__ = 'Thomas Pani and Jeremy Grossmann'
__version__ = '0.8.4'

if platform.system() == 'Windows':
    if os.path.exists('Qemu\qemu-system-i386w.exe'):
        QEMU_PATH = "Qemu\qemu-system-i386w.exe"
        QEMU_IMG_PATH = "Qemu\qemu-img.exe"
    else:
        # For now we ship Qemu 0.11.0 in the all-in-one
        QEMU_PATH = "qemu.exe"
        QEMU_IMG_PATH = "qemu-img.exe"
else:
    QEMU_PATH = "qemu"
    QEMU_IMG_PATH = "qemu-img"

PORT = 10525
IP = ""
QEMU_INSTANCES = {}
FORCE_IPV6 = False
MONITOR_BASE_PORT = 5001

# set correctly the working directory for qemuwrapper
WORKDIR = os.getcwdu()
if os.environ.has_key("TEMP"):
    WORKDIR = unicode(os.environ["TEMP"], 'utf-8', errors='replace')
elif os.environ.has_key("TMP"):
    WORKDIR = unicode(os.environ["TMP"], 'utf-8', errors='replace')

# __file__ is not supported by py2exe and py2app
if hasattr(sys, "frozen"):
    PEMU_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    PEMU_DIR = os.path.dirname(os.path.abspath(__file__))

class UDPConnection:
    def __init__(self, saddr, sport, daddr, dport):
        self.saddr = saddr
        self.sport = sport
        self.daddr = daddr
        self.dport = dport

    def resolve_names(self):
        try:
            addr = socket.gethostbyname(self.daddr)
            self.daddr = addr
        except socket.error, e:
            print >> sys.stderr, "Unable to resolve hostname %s", self.daddr
            print >> sys.stderr, e
        except socket.herror, e:
            print >> sys.stderr, "Unable to resolve hostname %s", self.daddr
            print >> sys.stderr, e


class xEMUInstance(object):

    def __init__(self, name):
        debugmsg(2, "xEMUInstance::__init__()")
        self.name = name
        self.ram = '256'
        self.console = ''
        self.image = ''
        self.nic = {}
        self.nics = '6'
        self.udp = {}
        self.usermod = False
        self.flavor = 'Default'
        self.capture = {}
        self.netcard = 'rtl8139'
        self.kvm = False
        self.options = ''
        self.process = None
        self.workdir = WORKDIR + os.sep + name
        self.valid_attr_names = ['image', 'ram', 'console', 'nics', 'netcard', 'kvm', 'options', 'usermod', 'flavor', 'monitor']
        # For Qemu monitor mode
        self.monitor = False
        self.monitor_conn = None
        self.monitor_sock = None
        global MONITOR_BASE_PORT
        self.monitor_port = MONITOR_BASE_PORT
        MONITOR_BASE_PORT = MONITOR_BASE_PORT + 1

    def create(self):
        debugmsg(2, "xEMUInstance::create()")
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def clean(self):
        pass

    def unbase_disk(self):
        pass

    def start(self):
        debugmsg(2, "xEMUInstance::start()")
        command = self._build_command()

        if bool(self.monitor):
            # Prepare the socket taking care of Qemu monitor mode
            for res in socket.getaddrinfo('localhost', self.monitor_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, cannonname, sa = res
                try:
                    self.monitor_sock = socket.socket(af, socktype, proto)
                except socket.error, msg:
                    self.monitor_sock = None
                    continue
                try:
                    self.monitor_sock.bind(sa)
                    self.monitor_sock.listen(1) # Allow only one connection
                except socket.error, msg:
                    self.monitor_sock.close()
                    self.monitor_sock = None
                    continue
                break
            if self.monitor_sock is None:
                print >> sys.stderr, 'Unable to open socket for monitor mode on localhost:' + self.monitor_port
                return False

        qemu_cmd = " ".join(command)
        print "Starting Qemu: ", qemu_cmd
        try:
            self.process = subprocess.Popen(command,
                                            stdin = subprocess.PIPE,
                                            stdout = subprocess.PIPE,
                                            #stderr = subprocess.PIPE,
                                            cwd=self.workdir,
                                            shell=False) # MUST STAY FALSE
        except OSError, e:
            print >> sys.stderr, "Unable to start instance", self.name, "of", self.__class__
            print >> sys.stderr, e
            print self.process.communicate()
            return False

        print "Qemu started with PID %i" % self.process.pid
        time.sleep(1)

        if bool(self.monitor):
            self.monitor_conn, addr = self.monitor_sock.accept()
            self.monitor_conn.setblocking(0)
            # consume the first lines of output of Qemu monitor mode
            output = ''
            while True:
                select.select([self.monitor_conn], [], [], 1)
                output += self.monitor_conn.recv(4096)
                if len(output) == 0 or 'monitor -'not in output:
                    continue
                else:
                    break

        if platform.system() == 'Windows':
            print "Setting priority class to BELOW_NORMAL"
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, self.process.pid)
            win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
        else:
            subprocess.call(['renice', '-n', '19', '-p', str(self.process.pid)])

        return True

    def stop(self):
        if platform.system() == 'Windows':
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, self.process.pid)
            try:
                if win32api.TerminateProcess(handle, 0):
                    return False
            except pywintypes.error, e:
                print >> sys.stderr, "Unable to stop Qemu instance", self.name
                print >> sys.stderr, e[2]
                # ignore and continue
                #return False
        else:
            import signal
            try:
                os.kill(self.process.pid, signal.SIGINT)
            except OSError, e:
                print >> sys.stderr, "Unable to stop Qemu instance", self.name
                print >> sys.stderr, e
        self.process = None

        return True

    def _net_options(self):
        global qemuprotocol
        options = []

        # compute new MAC address based on VM name + vlan number
        mac = hashlib.md5(self.name).hexdigest()
        local_qemuprotocol = qemuprotocol

        if platform.system() == 'Windows':
            # On Windows, Qemu binaries don't return anything when using -help. So pick up the protocol based on the filename.
            binary_name = os.path.basename(self.bin)
            print "Binary: %s" % binary_name
            if binary_name == 'qemu-system-i386w.exe':
                local_qemuprotocol = 1
                print "Using the new qemu syntax"
            else:
                local_qemuprotocol = 0
                print "Using the old qemu syntax"
        else:
            # fallback on another syntax if the current one is not supported
            if qemuprotocol == 0:
                try:
                    p = subprocess.Popen([self.bin, '-help'], stdout = subprocess.PIPE)
                    qemustdout = p.communicate()
                except:
                    print >> sys.stderr, "Unable to execute %s -help" % self.bin
                    return options
                if not qemustdout[0].__contains__('for dynamips/pemu/GNS3'):
                    print "Falling back to the new qemu syntax"
                    local_qemuprotocol = 1
            elif qemuprotocol == 1:
                try:
                    p = subprocess.Popen([self.bin, '-net', 'socket'], stderr = subprocess.PIPE)
                    qemustderr = p.communicate()
                except:
                    print >> sys.stderr, "Unable to execute %s -net socket" % self.bin
                    return options
                if not qemustderr[1].__contains__('udp='):
                    print "Falling back to the old qemu syntax"
                    local_qemuprotocol = 0

        for vlan in range(int(self.nics)):
            if local_qemuprotocol == 1:
                if vlan in self.nic and vlan in self.udp:
                    options.extend(['-device', '%s,mac=%s,netdev=gns3-%s' % (self.netcard, self.nic[vlan], vlan)])
                else:
                    options.extend(['-device', '%s,mac=00:00:ab:%02x:%02x:%02d' % (self.netcard, random.randint(0x00, 0xff), random.randint(0x00, 0xff), vlan)])
                if vlan in self.udp:
                    options.append('-netdev')
                    options.append('socket,id=gns3-%s,udp=%s:%s,localaddr=%s:%s' % (vlan, self.udp[vlan].daddr, self.udp[vlan].dport, self.udp[vlan].saddr, self.udp[vlan].sport))
                # FIXME: dump relies on vlans, incompatible with the new syntax: patch Qemu
                if vlan in self.capture:
                    print 'Dump option is not available with the netdev syntax'
                    #options.extend(['-net', 'dump,vlan=%s,file=%s' % (vlan, self.capture[vlan])])
            else:
                options.append('-net')
                if vlan in self.nic:
                    options.append('nic,vlan=%d,macaddr=%s,model=%s' % (vlan, self.nic[vlan], self.netcard))
                else:
                    # add a default NIC for Qemu
                    options.append('nic,vlan=%d,macaddr=00:00:ab:%02x:%02x:%02d,model=%s' % (vlan, random.randint(0x00, 0xff), random.randint(0x00, 0xff), vlan, self.netcard))
                if vlan in self.udp:
                    options.extend(['-net', 'udp,vlan=%s,sport=%s,dport=%s,daddr=%s' %
                            (vlan, self.udp[vlan].sport,
                             self.udp[vlan].dport,
                             self.udp[vlan].daddr)])
                if vlan in self.capture:
                    options.extend(['-net', 'dump,vlan=%s,file=%s' % (vlan, self.capture[vlan])])

        if bool(self.usermod):
            options.extend(['-device', '%s,mac=00:00:ab:%02x:%02x:%02x,netdev=gns3-usermod' % (self.netcard, random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff))])
            options.extend(['-netdev', 'user,id=gns3-usermod'])

        return options

    def _ser_options(self):
        if self.console:
            return ['-serial', 'telnet:' + IP + ':%s,server,nowait' % self.console]
        else:
            return []

class PEMUInstance(xEMUInstance):
    def __init__(self, name):
        debugmsg(2, "PEMUInstance::__init__()")
        super(PEMUInstance, self).__init__(name)
        if platform.system() == 'Windows':
            self.bin = 'pemu.exe'
        else:
            self.bin = 'pemu'
        self.serial = '0x12345678'
        self.key = '0x00000000,0x00000000,0x00000000,0x00000000'
        self.valid_attr_names += ['serial', 'key']
        self.pemu_bin_path = os.path.join(PEMU_DIR, self.bin)
        debugmsg(1, "self.pemu_bin_path = %s" % self.pemu_bin_path)

    def _net_options(self):

        options = []

        # compute new MAC address based on VM name + vlan number
        for vlan in range(int(self.nics)):
            options.append('-net')
            if vlan in self.nic:
                options.append('nic,vlan=%d,macaddr=%s,model=%s' % (vlan, self.nic[vlan], self.netcard))
            else:
                # add a default NIC for Qemu
                options.append('nic,vlan=%d,macaddr=00:00:ab:%02x:%02x:%02d,model=%s' % (vlan, random.randint(0x00, 0xff), random.randint(0x00, 0xff), vlan, self.netcard))
            if vlan in self.udp:
                options.extend(['-net', 'udp,vlan=%s,sport=%s,dport=%s,daddr=%s' %
                        (vlan, self.udp[vlan].sport,
                        self.udp[vlan].dport,
                        self.udp[vlan].daddr)])
            if vlan in self.capture:
                options.extend(['-net', 'dump,vlan=%s,file=%s' % (vlan, self.capture[vlan])])

        return options

    def _build_command(self):
        debugmsg(2, "PEMUInstance::_build_command()")
        "Builds the command as a list of shell arguments."
        command = [os.path.join(PEMU_DIR, self.bin)]
        command.extend(self._net_options())
        command.extend(['-m', str(self.ram), 'FLASH'])
        command.extend(self._ser_options())
        return command

    def _write_config(self):
        debugmsg(2, "PEMUInstance::_write_config()")
        f = open(os.path.join(self.workdir, 'pemu.ini'), 'w')
        f.writelines(''.join(['%s=%s\n' % (attr, getattr(self, attr))
            for attr in ('serial', 'key', 'image')]))
        f.close()

    def start(self):
        debugmsg(2, "PEMUInstance::start()")
        if not os.path.exists(self.pemu_bin_path):
            debugmsg(1, "ERROR: Cannot find PEMU !")
            print >> sys.stderr, "ERROR: Cannot find PEMU! (looking for %s)" % self.pemu_bin_path
            return False
        self._write_config()
        return super(PEMUInstance, self).start()

class PIXInstance(PEMUInstance):
    pass

class QEMUInstance(xEMUInstance):

    def __init__(self, name):
        debugmsg(3, "QEMUInstance::__init__()")
        super(QEMUInstance, self).__init__(name)
        self.bin = QEMU_PATH
        self.img_bin = QEMU_IMG_PATH
        self.valid_attr_names.extend(('flash_size', 'flash_name'))
        self.flash_size = '256M'
        self.flash_name = 'FLASH'

    def _build_command(self):
        debugmsg(3, "QEMUInstance::_build_command()")
        "Builds the command as a list of shell arguments."

        if 'qemu-system-' in self.bin and self.flavor != 'Default':
            self.bin = re.sub(r'qemu-system-.*', 'qemu-system' + self.flavor, self.bin)
            if sys.platform.startswith('win'):
                self.bin += 'w.exe' # We ship qemu-system-XXXw.exe on Windows
        command = [self.bin]

        # Qemu monitor mode through socket
        if bool(self.monitor):
            command.extend(['-monitor', 'stdio'])
            command.extend(['-chardev', 'socket,id=qemuwrapper-monitor,host=localhost,port=' + str(self.monitor_port)])
            command.extend(['-mon', 'qemuwrapper-monitor'])

        command.extend(['-name', self.name])
        command.extend(['-m', str(self.ram)])
        command.extend(self._disk_options())
        command.extend(self._image_options())
        command.extend(self._kernel_options())
        if bool(self.kvm) == True:
            command.extend(['-enable-kvm'])
        command.extend(self._net_options())
        command.extend(self._ser_options())
        self.options = self.options.strip()
        if self.options:
            #TODO: do not split inside double quotes => use re.split()
            command.extend(self.options.split())
        return command

    def _disk_options(self):
        debugmsg(3, "QEMUInstance::_disk_options()")
        return []

    def _kernel_options(self):
        debugmsg(3, "QEMUInstance::_kernel_options()")
        return []

    def _image_options(self):
        debugmsg(3, "QEMUInstance::_image_options()")
        return []


class ASAInstance(QEMUInstance):

    def __init__(self, *args, **kwargs):
        debugmsg(3, "ASAInstance::__init__()")
        super(ASAInstance, self).__init__(*args, **kwargs)
        self.netcard = 'e1000'
        self.initrd = ''
        self.kernel = ''
        self.kernel_cmdline = ''
        self.valid_attr_names += ['initrd', 'kernel', 'kernel_cmdline']

    def clean(self):
        debugmsg(3, "ASAInstance::clean()")

        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Deleting old flash file:", flash
                os.remove(flash)
            except (OSError, IOError), e:
                print >> sys.stderr, flash, "cannot be deleted:", e

    def _disk_options(self):
        debugmsg(3, "ASAInstance::_disk_options()")

        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-f', 'qcow2', flash, self.flash_size])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        return ('-hda', flash)

    def _image_options(self):
        debugmsg(3, "ASAInstance::_image_options()")
        return ('-kernel', self.kernel, '-initrd', self.initrd)

    def _kernel_options(self):
        debugmsg(3, "ASAInstance::_kernel_options()")
        
        return  ('-append', self.kernel_cmdline)

class AWPInstance(QEMUInstance):

    def __init__(self, *args, **kwargs):
        debugmsg(3, "AWPInstance::__init__()")
        super(AWPInstance, self).__init__(*args, **kwargs)
        self.netcard = 'virtio'
        self.initrd = ''
        self.kernel = ''
        self.kernel_cmdline = 'root=/dev/ram0 releasefile=0.0.0-test.rel console=ttyS0,0 no_autorestart loglevel=1'
        self.valid_attr_names += ['initrd', 'kernel', 'kernel_cmdline']

    def clean(self):
        debugmsg(3, "AWPInstance::clean()")

        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Deleting old flash file:", flash
                os.remove(flash)
            except (OSError, IOError), e:
                print >> sys.stderr, flash, "cannot be deleted:", e

    def _disk_options(self):
        debugmsg(3, "AWPInstance::_disk_options()")

        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-f', 'qcow2', flash, self.flash_size])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        return ('-hda', flash)

    def _image_options(self):
        debugmsg(3, "AWPInstance::_image_options()")
        return ('-kernel', self.kernel, '-initrd', self.initrd)

    def _kernel_options(self):
        debugmsg(3, "AWPInstance::_kernel_options()")
        return  ('-append', self.kernel_cmdline)

class JunOSInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        debugmsg(3, "JunOSInstance::__init__()")
        super(JunOSInstance, self).__init__(*args, **kwargs)
        self.swap_name= 'SWAP'
        self.swap_size = '1G'
        self.netcard = 'e1000'

    def clean(self):
        debugmsg(3, "JunOSInstance::clean()")
        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Deleting old flash file:", flash
                os.remove(flash)
            except (OSError, IOError), e:
                print >> sys.stderr, flash, "cannot be deleted:", e

        swap = os.path.join(self.workdir, self.swap_name)
        if os.path.exists(swap):
            try:
                print "Deleting old swap file:", swap
                os.remove(swap)
            except (OSError, IOError), e:
                print >> sys.stderr, swap, "cannot be deleted:", e

    def unbase_disk(self):
        debugmsg(3, "JunOSInstance::unbase_disk()")

        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Converting %s to have no base image" % flash
                retcode = subprocess.call([self.img_bin, 'convert', '-O', 'qcow2', flash, flash])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

    def _disk_options(self):
        debugmsg(3, "JunOSInstance::_disk_options()")

        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-o',
                                          'backing_file=' + self.image,
                                          '-f', 'qcow2', flash])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        swap = os.path.join(self.workdir, self.swap_name)
        if not os.path.exists(swap):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-f', 'qcow2', swap, self.swap_size])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        return (flash, '-hdb', swap)

class IDSInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        debugmsg(3, "IDSInstance::__init__()")
        super(IDSInstance, self).__init__(*args, **kwargs)
        self.netcard = 'e1000'
        self.image1 = ''
        self.image2 = ''
        self.valid_attr_names += ['image1', 'image2']
        self.img1_name = 'DISK1'
        self.img2_name = 'DISK2'

    def clean(self):
        debugmsg(3, "IDSInstance::clean()")

        img1 = os.path.join(self.workdir, self.img1_name)
        if os.path.exists(img1):
            try:
                print "Deleting old image file:", img1
                os.remove(img1)
            except (OSError, IOError), e:
                print >> sys.stderr, img1, "cannot be deleted:", e

        img2 = os.path.join(self.workdir, self.img2_name)
        if os.path.exists(img2):
            try:
                print "Deleting old image file:", img2
                os.remove(img2)
            except (OSError, IOError), e:
                print >> sys.stderr, img2, "cannot be deleted:", e

    def unbase_disk(self):
        debugmsg(3, "IDSInstance::unbase_disk()")

        img1 = os.path.join(self.workdir, self.img1_name)
        if os.path.exists(img1):
            try:
                print "Converting %s to have no base image" % img1
                retcode = subprocess.call([self.img_bin, 'convert', '-O', 'qcow2', img1, img1])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        img2 = os.path.join(self.workdir, self.img2_name)
        if os.path.exists(img2):
            try:
                print "Converting %s to have no base image" % img2
                retcode = subprocess.call([self.img_bin, 'convert', '-O', 'qcow2', img2, img2])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

    def _disk_options(self):
        debugmsg(3, "IDSInstance::_disk_options()")

        img1 = os.path.join(self.workdir, self.img1_name)
        if not os.path.exists(img1):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-o',
                                          'backing_file=' + self.image1,
                                          '-f', 'qcow2', img1])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        img2 = os.path.join(self.workdir, self.img2_name)
        if not os.path.exists(img2):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-o',
                                          'backing_file=' + self.image2,
                                          '-f', 'qcow2', img2])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        return ('-hda', img1, '-hdb', img2)

class QemuDeviceInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        debugmsg(3, "QemuDeviceInstance::__init__()")
        super(QemuDeviceInstance, self).__init__(*args, **kwargs)
        self.swap_name= 'SWAP'
        self.swap_size = '1G'
        self.netcard = 'rtl8139'

    def clean(self):
        debugmsg(3, "QemuDeviceInstance::clean()")

        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Deleting old flash file:", flash
                os.remove(flash)
            except (OSError, IOError), e:
                print >> sys.stderr, flash, "cannot be deleted:", e

        swap = os.path.join(self.workdir, self.swap_name)
        if os.path.exists(swap):
            try:
                print "Deleting old swap file:", swap
                os.remove(swap)
            except (OSError, IOError), e:
                print >> sys.stderr, swap, "cannot be deleted:", e

    def unbase_disk(self):
        debugmsg(3, "QemuDeviceInstance::unbase_disk()")

        flash = os.path.join(self.workdir, self.flash_name)
        if os.path.exists(flash):
            try:
                print "Converting %s to have no base image" % flash
                retcode = subprocess.call([self.img_bin, 'convert', '-O', 'qcow2', flash, flash])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

    def _disk_options(self):
        debugmsg(3, "QemuDeviceInstance::_disk_options()")
        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-o',
                                          'backing_file=' + self.image,
                                          '-f', 'qcow2', flash])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e

        swap = os.path.join(self.workdir, self.swap_name)
        if not os.path.exists(swap):
            try:
                retcode = subprocess.call([self.img_bin, 'create', '-f', 'qcow2', swap, self.swap_size])
                print self.img_bin + ' returned with ' + str(retcode)
            except OSError, e:
                print >> sys.stderr, self.img_bin, "execution failed:", e
        debugmsg(3, "flash = %s" % str(flash))
        debugmsg(3, "image = %s" % str(self.image))
        debugmsg(3, "swap = %s" % str(swap))

        return (flash, '-hdb', swap)

class QemuWrapperRequestHandler(SocketServer.StreamRequestHandler):

    modules = {
        'qemuwrapper' : {
            'version' : (0, 0),
            'parser_test' : (0, 10),
            'module_list' : (0, 0),
            'cmd_list' : (1, 1),
            'qemu_path' : (1, 1),
            'qemu_img_path' : (1, 1),
            #'qemu_base_mac' : (1, 1),
            'working_dir' : (1, 1),
            'reset' : (0, 0),
            'close' : (0, 0),
            'stop' : (0, 0),
            },
        'qemu' : {
            'version' : (0, 0),
            'create' : (2, 2),
            'delete' : (1, 1),
            'setattr' : (3, 3),
            'create_nic' : (3, 3),
            'create_udp' : (6, 6),
            'delete_udp' : (2, 2),
            'create_capture' : (3, 3),
            'delete_capture' : (2, 2),
            'start' : (1, 1),
            'stop' : (1, 1),
            'clean': (1, 1),
            'unbase': (1, 1),
            'monitor': (2, 2),
            'rename' : (2, 2),
            }
        }

    qemu_classes = {
        'qemu': QemuDeviceInstance,
        'pix': PIXInstance,
        'asa': ASAInstance,
        'awprouter' : AWPInstance,
        'junos': JunOSInstance,
        'ids': IDSInstance,
        }

    # dynamips style status codes
    HSC_INFO_OK         = 100  #  ok
    HSC_INFO_MSG        = 101  #  informative message
    HSC_INFO_DEBUG      = 102  #  debugging message
    HSC_ERR_PARSING     = 200  #  parse error
    HSC_ERR_UNK_MODULE  = 201  #  unknown module
    HSC_ERR_UNK_CMD     = 202  #  unknown command
    HSC_ERR_BAD_PARAM   = 203  #  bad number of parameters
    HSC_ERR_INV_PARAM   = 204  #  invalid parameter
    HSC_ERR_BINDING     = 205  #  binding error
    HSC_ERR_CREATE      = 206  #  unable to create object
    HSC_ERR_DELETE      = 207  #  unable to delete object
    HSC_ERR_UNK_OBJ     = 208  #  unknown object
    HSC_ERR_START       = 209  #  unable to start object
    HSC_ERR_STOP        = 210  #  unable to stop object
    HSC_ERR_FILE        = 211  #  file error
    HSC_ERR_BAD_OBJ     = 212  #  bad object

    close_connection = 0

    def send_reply(self, code, done, msg):
        debugmsg(3, "QemuWrapperRequestHandler::send_reply(code=%s, done=%s, msg=%s)" % (str(code), str(done), str(msg)))
        sep = '-'
        if not done:
            sep = ' '
        self.wfile.write("%3d%s%s\r\n" % (code, sep, msg))

    def handle(self):
        debugmsg(2, "QemuWrapperRequestHandler::handle()")
        print "Connection from", self.client_address
        try:
            self.handle_one_request()
            while not self.close_connection:
                self.handle_one_request()
            print "Disconnection from", self.client_address
        except socket.error, e:
            print >> sys.stderr, e
            self.request.close()
            return

    def __get_tokens(self, request):
        debugmsg(3, "QemuWrapperRequestHandler::__get_tokens(%s)" % str(request))
        input_ = cStringIO.StringIO(request)
        tokens = []
        try:
            tokens = csv.reader(input_, delimiter=' ', escapechar='\\').next()
        except StopIteration:
            pass
        return tokens

    def finish(self):
        pass

    def handle_one_request(self):
        debugmsg(3, "QemuWrapperRequestHandler::handle_one_request()")
        request = self.rfile.readline()
        request = request.rstrip()      # Strip package delimiter.

        # Don't process empty strings (this creates Broken Pipe exceptions)
        #FIXME: this causes 100% cpu usage on Windows.
        #if request == "":
        #    return

        # Parse request.
        tokens = self.__get_tokens(request)
        if len(tokens) < 2:
            try:
                self.send_reply(self.HSC_ERR_PARSING, 1, "At least a module and a command must be specified")
            except socket.error:
                self.close_connection = 1
            return

        module, command = tokens[:2]
        data = tokens[2:]

        if not module in self.modules.keys():
            self.send_reply(self.HSC_ERR_UNK_MODULE, 1,
                            "Unknown module '%s'" % module)
            return

        # Prepare to call the do_<command> function.
        mname = 'do_%s_%s' % (module, command)
        if not hasattr(self, mname):
            self.send_reply(self.HSC_ERR_UNK_CMD, 1,
                            "Unknown command '%s'" % command)
            return
        try:
            if len(data) < self.modules[module][command][0] or \
                len(data) > self.modules[module][command][1]:
                self.send_reply(self.HSC_ERR_BAD_PARAM, 1,
                                "Bad number of parameters (%d with min/max=%d/%d)" %
                                    (len(data),
                                      self.modules[module][command][0],
                                      self.modules[module][command][1])
                                    )
                return
        except Exception, e:
            # This can happen, if you add send command, but forget to define it in class modules
            self.send_reply(self.HSC_ERR_INV_PARAM, 1, "Unknown Exception")
            debugmsg(1, ("handle_one_request(), ERROR: Unknown Exception: ", e))
            return

        # Call the function.
        method = getattr(self, mname)
        method(data)

    def do_qemuwrapper_version(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_version(%s)" % str(data))
        self.send_reply(self.HSC_INFO_OK, 1, __version__)

    def do_qemuwrapper_parser_test(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_parser_test(%s)" % str(data))
        for i in range(len(data)):
            self.send_reply(self.HSC_INFO_MSG, 0,
                            "arg %d (len %u): \"%s\"" % \
                            (i, len(data[i]), data[i])
                            )
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_module_list(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_module_list(%s)" % str(data))
        for module in self.modules.keys():
            self.send_reply(self.HSC_INFO_MSG, 0, module)
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_cmd_list(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_cmd_list(%s)" % str(data))
        module, = data

        if not module in self.modules.keys():
            self.send_reply(self.HSC_ERR_UNK_MODULE, 1,
                            "unknown module '%s'" % module)
            return

        for command in self.modules[module].keys():
            self.send_reply(self.HSC_INFO_MSG, 0,
                            "%s (min/max args: %d/%d)" % \
                            (command,
                             self.modules[module][command][0],
                             self.modules[module][command][1])
                            )

        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_qemu_path(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_qemu_path(%s)" % str(data))
        qemu_path, = data
        try:
            qemu_path = os.path.normpath(qemu_path)
            os.access(qemu_path, os.F_OK)
            global QEMU_PATH
            QEMU_PATH = qemu_path
            print "Qemu path is now %s" % QEMU_PATH
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].bin = os.path.join(os.getcwdu(), QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "access: %s" % e.strerror)

    def do_qemuwrapper_qemu_img_path(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_qemu_img_path(%s)" % str(data))
        qemu_img_path, = data
        try:
            qemu_img_path = os.path.normpath(qemu_img_path)
            os.access(qemu_img_path, os.F_OK)
            global QEMU_IMG_PATH
            QEMU_IMG_PATH = qemu_img_path
            print "Qemu-img path is now %s" % QEMU_IMG_PATH
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].img_bin = os.path.join(os.getcwdu(), QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "access: %s" % e.strerror)

    def do_qemuwrapper_working_dir(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_working_dir(%s)" % str(data))
        working_dir, = data
        try:
            working_dir = os.path.normpath(working_dir)
            os.chdir(working_dir)
            global WORKDIR
            WORKDIR = working_dir
            print "Working directory is now %s" % WORKDIR
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].workdir = os.path.join(working_dir, QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "chdir: %s" % e.strerror)

    def do_qemuwrapper_reset(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_reset(%s)" % str(data))
        cleanup()
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_close(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_close(%s)" % str(data))
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1

    def do_qemuwrapper_stop(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemuwrapper_stop(%s)" % str(data))
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1
        self.server.stop()

    def do_qemu_version(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_version(%s)" % str(data))
        self.send_reply(self.HSC_INFO_OK, 1, __version__)

    def __qemu_create(self, dev_type, name):
        debugmsg(2, "QemuWrapperRequestHandler::__qemu_create(dev_type=%s, name=%s)" % (str(dev_type), str(name)))
        try:
            devclass = self.qemu_classes[dev_type]
        except KeyError:
            print >> sys.stderr, "No device type %s" % dev_type
            return 1
        if name in QEMU_INSTANCES.keys():
            print >> sys.stderr, "Unable to create Qemu instance", name
            print >> sys.stderr, "%s already exists" % name
            return 1
        qemu_instance = devclass(name)

        try:
            qemu_instance.create()
        except OSError, e:
            print >> sys.stderr, "Unable to create Qemu instance", name
            print >> sys.stderr, e
            return 1

        QEMU_INSTANCES[name] = qemu_instance
        return 0

    def do_qemu_create(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_create(%s)" % str(data))
        dev_type, name = data
        if self.__qemu_create(dev_type, name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' created" % name)
        else:
            self.send_reply(self.HSC_ERR_CREATE, 1,
                            "unable to create Qemu instance '%s'" % name)

    def __qemu_delete(self, name):
        debugmsg(2, "QemuWrapperRequestHandler::__qemu_delete(%s)" % str(name))
        if not name in QEMU_INSTANCES.keys():
            return 1
        if QEMU_INSTANCES[name].process and not QEMU_INSTANCES[name].stop():
            return 1
        del QEMU_INSTANCES[name]
        return 0

    def do_qemu_delete(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_delete(%s)" % str(data))
        name, = data
        if self.__qemu_delete(name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' deleted" % name)
        else:
            self.send_reply(self.HSC_ERR_DELETE, 1,
                            "unable to delete Qemu instance '%s'" % name)

    def do_qemu_setattr(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_setattr(%s)" % str(data))
        name, attr, value = data
        try:
            instance = QEMU_INSTANCES[name]
        except KeyError:
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                             "unable to find Qemu '%s'" % name)
            return
        if not attr in instance.valid_attr_names:
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "Cannot set attribute '%s' for '%s" % (attr, name))
            return
        if attr in ("image", "initrd", "kernel", "image1", "image2"):
            value = os.path.normpath(value)
        print >> sys.stderr, '!! %s.%s = %s' % (name, attr, value)
        setattr(QEMU_INSTANCES[name], attr, value)
        self.send_reply(self.HSC_INFO_OK, 1, "%s set for '%s'" % (attr, name))

    def do_qemu_create_nic(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_create_nic(%s)" % str(data))
        name, vlan, mac = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        QEMU_INSTANCES[name].nic[int(vlan)] = mac
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_create_udp(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_create_udp(%s)" % str(data))
        name, vlan, saddr, sport, daddr, dport = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        udp_connection = UDPConnection(saddr, sport, daddr, dport)
        udp_connection.resolve_names()
        QEMU_INSTANCES[name].udp[int(vlan)] = udp_connection
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_delete_udp(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_delete_udp(%s)" % str(data))
        name, vlan = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        if QEMU_INSTANCES[name].udp.has_key(int(vlan)):
            del QEMU_INSTANCES[name].udp[int(vlan)]
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_create_capture(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_create_capture(%s)" % str(data))
        name, vlan, path = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return

        QEMU_INSTANCES[name].capture[int(vlan)] = os.path.normpath(path)
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_delete_capture(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_delete_capture(%s)" % str(data))
        name, vlan = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        if QEMU_INSTANCES[name].capture.has_key(int(vlan)):
            del QEMU_INSTANCES[name].capture[int(vlan)]
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_start(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_start(%s)" % str(data))
        name, = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        if not QEMU_INSTANCES[name].start():
            self.send_reply(self.HSC_ERR_START, 1,
                            "unable to start instance '%s'" % name)
        else:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' started" % name)

    def do_qemu_stop(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_stop(%s)" % str(data))
        name, = data
        if not QEMU_INSTANCES[name].process:
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        if not QEMU_INSTANCES[name].stop():
            self.send_reply(self.HSC_ERR_STOP, 1,
                            "unable to stop instance '%s'" % name)
        else:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' stopped" % name)

    def do_qemu_clean(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_clean(%s)" % str(data))
        name, = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        QEMU_INSTANCES[name].clean()
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_unbase(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_unbase(%s)" % str(data))
        name, = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        QEMU_INSTANCES[name].unbase_disk()
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    # QEMU MONITOR MODE
    def do_qemu_monitor(self, data):
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_monitor(%s)" % (str(data)))
        name, command = data
        command += "\n"
        if not QEMU_INSTANCES[name].process:
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s', is it started?" % name)
            return

        if bool(QEMU_INSTANCES[name].monitor) == False:
            self.send_reply(self.HSC_ERR_UNK_CMD, 1,
                            "Monitor mode is not activated for Qemu '%s'" % name)
            return

        # send the command to qemu monitor mode
        QEMU_INSTANCES[name].monitor_conn.send(command)

        output = ''
        while True:
            try:
                select.select([QEMU_INSTANCES[name].monitor_conn], [], [], 1)
                output += QEMU_INSTANCES[name].monitor_conn.recv(512)
            except:
                break
        output = output.replace("\r", "")
        # remove the first line (trash input and ESC sequence)
        output = output[output.find("\n") + 1:]
        # remove the qemu prompt
        output = output[:-9]
        # Serialize newlines: can only send a single line
        output = output.replace("\n", '\n')
        # Some commands don't generate any output, means it's OK
        if len(output) == 0:
            output = 'OK'
        self.send_reply(self.HSC_INFO_OK, 1, output)

    def do_qemu_rename(self, data):
        #FIXME: non-working code
        debugmsg(2, "QemuWrapperRequestHandler::do_qemu_rename(%s)" % str(data))
        oldname, newname = data
        if not oldname in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % oldname)
            return

        QEMU_INSTANCES[newname] = QEMU_INSTANCES[oldname]
        QEMU_INSTANCES[newname].name = newname
        global WORKDIR
        new_workdir = os.path.join(WORKDIR, newname)
        try:
            shutil.move(QEMU_INSTANCES[oldname].workdir, new_workdir)
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1, "rename: %s" % e.strerror)
        self.workdir = new_workdir
        del QEMU_INSTANCES[oldname]
        self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' renamed to '%s'" % (oldname, newname))

class DaemonThreadingMixIn(SocketServer.ThreadingMixIn):
    daemon_threads = True


class QemuWrapperServer(DaemonThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        debugmsg(2, "QemuWrapperServer::__init__()")
        global FORCE_IPV6
        if server_address[0].__contains__(':'):
            FORCE_IPV6 = True
        if FORCE_IPV6:
            # IPv6 address support
            self.address_family = socket.AF_INET6
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)
        self.stopping = threading.Event()
        self.pause = 0.1

    def serve_forever(self):
        while not self.stopping.isSet():
            if select.select([self.socket], [], [], self.pause)[0]:
                self.handle_request()
        cleanup()

    def stop(self):
        self.stopping.set()


def cleanup():
    print "Shutdown in progress..."
    for name in QEMU_INSTANCES.keys():
        if QEMU_INSTANCES[name].process:
            QEMU_INSTANCES[name].stop()
        del QEMU_INSTANCES[name]
    print "Shutdown completed."


def main():
    debugmsg(2, "qemuwrapper.py    main()")
    global IP
    from optparse import OptionParser

    usage = "usage: %prog [--listen <ip_address>] [--port <port_number>] [--forceipv6 false] [--no-path-check]"
    parser = OptionParser(usage, version="%prog " + __version__)
    parser.add_option("-l", "--listen", dest="host", help="IP address or hostname to listen on (default is to listen on all interfaces)")
    parser.add_option("-p", "--port", type="int", dest="port", help="Port number (default is 10525)")
    parser.add_option("-w", "--workdir", dest="wd", help="Working directory (default is current directory)")
    parser.add_option("-6", "--forceipv6", dest="force_ipv6", help="Force IPv6 usage (default is false; i.e. IPv4)")
    parser.add_option("-n", "--no-path-check", action="store_true", dest="no_path_check", default=False, help="No path check for Qemu and Qemu-img")

    try:
        (options, args) = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    if not options.no_path_check:
        try:
            p = subprocess.Popen([QEMU_PATH])
            p.terminate()
            print "Qemu path (%s) is valid" % QEMU_PATH

        except OSError, e:
            print >> sys.stderr, "Unable to start Qemu:", e
            if not os.path.exists(QEMU_PATH):
                print >> sys.stderr, "Path to Qemu seems to be invalid, please check. Current path is", QEMU_PATH
            sys.exit(1)

        try:
            p = subprocess.Popen([QEMU_IMG_PATH])
            p.terminate()
            print "Qemu-img path (%s) is valid" % QEMU_IMG_PATH
        except OSError, e:
            print >> sys.stderr, "Unable to start Qemu-img:", e
            if not os.path.exists(QEMU_IMG_PATH):
                print >> sys.stderr, "Path to Qemu seems invalid, please check. Current path is", QEMU_IMG_PATH
            sys.exit(1)

    if options.host and options.host != '0.0.0.0':
        host = options.host
        IP = host
    else:
        host = IP

    if options.port:
        port = options.port
        global PORT
        PORT = port
    else:
        port = PORT

    if options.wd:
        global WORKDIR
        WORKDIR = options.wd

    if options.force_ipv6 and not (options.force_ipv6.lower().__contains__("false") or options.force_ipv6.__contains__("0")):
        global FORCE_IPV6
        FORCE_IPV6 = options.force_ipv6

    server = QemuWrapperServer((host, port), QemuWrapperRequestHandler)

    print "Qemu TCP control server started (port %d)." % port

    if FORCE_IPV6:
        LISTENING_MODE = "Listening in IPv6 mode"
    else:
        LISTENING_MODE = "Listening"

    if IP:
        print "%s on %s" % (LISTENING_MODE, IP)
    else:
        print "%s on all network interfaces" % LISTENING_MODE
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        cleanup()


if __name__ == '__main__':
    print "Qemu Emulator Wrapper (version %s)" % __version__
    print "Copyright (c) 2007-2011 Thomas Pani & Jeremy Grossmann"
    print
    sys.stdout.flush()

    if platform.system() == 'Windows':
        try:
            import pywintypes, win32api, win32con, win32process
        except ImportError:
            print >> sys.stderr, "You need pywin32 installed to run qemuwrapper!"
            sys.exit(1)

    main()
