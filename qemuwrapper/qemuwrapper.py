#!/usr/bin/env python
#
# Copyright (c) 2007-2009 Thomas Pani & Jeremy Grossmann
#
# Contributions by Pavel Skovajsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# !!!
# !!! PLEASE NOTE: THIS LICENSE DOES NOT APPLY TO THE BINARIES ATTACHED TO
# !!! THIS SCRIPT IN UUENCODED FORM. THEY ARE THE EFFORT OF mmm123 ON
# !!! http://7200emu.hacki.at/.
# !!!
#


import base64
import csv
import cStringIO
import os
import platform
import select
import socket
import subprocess
import sys
import tarfile
import threading
import SocketServer
import time

import pemubin


__author__ = 'Thomas Pani and Jeremy Grossmann'
__version__ = '0.2.6'

QEMU_PATH = "qemu"
QEMU_IMG_PATH = "qemu-img"
PORT = 10525
QEMU_INSTANCES = {}

PEMU_DIR = os.getcwd()
if platform.system() == 'Windows':
    PEMU_DIR = os.path.join(PEMU_DIR, 'pemu_public_win_2008-03-03')
else:
    PEMU_DIR = os.path.join(PEMU_DIR, 'pemu_public_bin2008-03-04')


class UDPConnection:
    def __init__(self, sport, daddr, dport):
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
        self.name = name
        self.ram = '256'
        self.console = ''
        self.image = ''
        self.nic = {}
        self.udp = {}
        self.netcard = 'pcnet'
        self.kqemu = False
        self.kvm = False
        self.options = ''
        self.process = None
        self.workdir = None
        self.valid_attr_names = ['image', 'ram', 'console', 'netcard', 'kqemu', 'kvm', 'options']

    def create(self):
        self.workdir = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def start(self):
        command = self._build_command()

        print "    command:", command
        try:
            self.process = subprocess.Popen(command,
                                            stdin=subprocess.PIPE,
                                            cwd=self.workdir)
        except OSError, e:
            print >> sys.stderr, "Unable to start instance", self.name, "of", self.__class__
            print >> sys.stderr, e
            return False

        # give us some time to wait for Qemu to start
        time.sleep(1)
        
        print "    pid:", self.process.pid

        if platform.system() == 'Windows':
            print "Setting priority class to BELOW_NORMAL"
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,
                    0, self.process.pid)
            returncode =  win32process.SetPriorityClass(handle,
                    win32process.BELOW_NORMAL_PRIORITY_CLASS)
            if returncode:
                print "   failed."
                return False

        else:
            print "Renicing to 19"
            returncode = subprocess.call(['renice', '+19', str(self.process.pid)])
            if returncode:
                print "    failed."
                # ignore if renice didn't worked
                return True

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
                return False
        else:
            import signal
            try:
                os.kill(self.process.pid, signal.SIGINT)
            except OSError, e:
                print >> sys.stderr, "Unable to stop Qemu instance", self.name
                print >> sys.stderr, e
                return False
        self.process = None

        return True

    def _net_options(self):
        options = []
        for vlan in range(6):
            options.append('-net')
            if vlan in self.nic:
                options.append('nic,vlan=%d,macaddr=%s,model=%s' % (vlan, self.nic[vlan], self.netcard))
            else:
                # add a default NIC for Qemu (we always add 6 NICs)
                options.append('nic,vlan=%d,macaddr=00:00:ab:cd:ef:%02d,model=%s' % (vlan, vlan, self.netcard))
            if vlan in self.udp:
                options.extend(['-net', 'udp,vlan=%s,sport=%s,dport=%s,daddr=%s' %
                        (vlan, self.udp[vlan].sport,
                         self.udp[vlan].dport,
                         self.udp[vlan].daddr)])
        return options
        
    def _ser_options(self):
        if self.console:
            return ['-serial', 'telnet::%s,server,nowait' % self.console]
        else:
            return []

class PEMUInstance(xEMUInstance):
    def __init__(self, name):
        super(PEMUInstance, self).__init__(name)
        if platform.system() == 'Windows':
            self.bin = 'pemu.exe'
        else:
            self.bin = 'pemu'
        self.serial = '0x12345678'
        self.key = '0x00000000,0x00000000,0x00000000,0x00000000'
        self.valid_attr_names += ['serial', 'key']

    def _build_command(self):
        "Builds the command as a list of shell arguments."
        command = [os.path.join(PEMU_DIR, self.bin)]
        command.extend(self._net_options())
        command.extend(['-m', str(self.ram), 'FLASH'])
        command.extend(self._ser_options())
        return command

    def _write_config(self):
        f = open(os.path.join(self.workdir, 'pemu.ini'), 'w')
        f.writelines(''.join(['%s=%s\n' % (attr, getattr(self, attr))
            for attr in ('serial', 'key', 'image')]))
        f.close()
      
    def start(self):
        self._write_config()
        return super(PEMUInstance, self).start()

class PIXInstance(PEMUInstance):
    pass
    
class QEMUInstance(xEMUInstance):

    def __init__(self, name):
        super(QEMUInstance, self).__init__(name)
        self.bin = QEMU_PATH
        self.img_bin = QEMU_IMG_PATH
        self.valid_attr_names.extend(('flash_size', 'flash_name'))
        self.flash_size = '256M'
        self.flash_name = 'FLASH'
        
    def _build_command(self):
        "Builds the command as a list of shell arguments."
        command = [self.bin]
        command.extend(['-m', str(self.ram)])
        command.extend(self._disk_options())
        command.extend(self._image_options())
        command.extend(self._kernel_options())
        if bool(self.kqemu) == True:
            command.extend(['-kernel-kqemu'])
        if bool(self.kvm) == True:
            command.extend(['-enable-kvm'])
        command.extend(self._graphic_options())
        command.extend(self._net_options())
        command.extend(self._ser_options())
        if self.options:
            command.extend(self.options.split())
        return command

    def _disk_options(self):
        return []
        
    def _kernel_options(self):
        return []
        
    def _image_options(self):
        return []
    
    def _graphic_options(self):
        return []

class ASAInstance(QEMUInstance):

    def __init__(self, *args, **kwargs):
        super(ASAInstance, self).__init__(*args, **kwargs)
        self.netcard = 'e1000'
        self.initrd = ''
        self.kernel = ''
        self.kernel_cmdline = ''
        self.valid_attr_names += ['initrd', 'kernel', 'kernel_cmdline']
        
    def _disk_options(self):
        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-f', 'qcow2', flash, self.flash_size)
        return ('-hda', flash)
    
    def _image_options(self):
        return ('-kernel', self.kernel, '-initrd', self.initrd)
        
    def _kernel_options(self):
        return  ('-append', self.kernel_cmdline)
    
    def _graphic_options(self):
        return ['-nographic']

class JunOSInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        super(JunOSInstance, self).__init__(*args, **kwargs)
        self.flash_size = '3G'
        self.swap_name= 'SWAP'
        self.swap_size = '1G'
        self.netcard = 'e1000'
    
    def _disk_options(self):
        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-b', self.image, '-f', 'qcow2', flash, self.flash_size)
        swap = os.path.join(self.workdir, self.swap_name)
        if not os.path.exists(swap):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-f', 'qcow2', '-c', swap, self.swap_size)
        return (flash, '-hdb', swap)
    
    def _graphic_options(self):
        return ['-nographic']
    
class IDSInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        super(IDSInstance, self).__init__(*args, **kwargs)
        self.netcard = 'e1000'
        self.image1 = ''
        self.image2 = ''
        self.valid_attr_names += ['image1', 'image2']
        self.img1_name = 'DISK1'
        self.img2_name = 'DISK2'
        self.img1_size = '512M'
        self.img2_size = '4G'
    
    def _disk_options(self):
        img1 = os.path.join(self.workdir, self.img1_name)
        img2 = os.path.join(self.workdir, self.img2_name)
        if not os.path.exists(img1):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-b', self.image1, '-f', 'qcow2', img1, self.img1_size)
        if not os.path.exists(img2):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-b', self.image2, '-f', 'qcow2', img2, self.img2_size)
        return ('-hda', img1, '-hdb', img2)
    
class QemuDeviceInstance(QEMUInstance):


    def __init__(self, *args, **kwargs):
        super(QemuDeviceInstance, self).__init__(*args, **kwargs)
        self.flash_size = '4G'
        self.swap_name= 'SWAP'
        self.swap_size = '1G'
        self.netcard = 'e1000'
    
    def _disk_options(self):
        flash = os.path.join(self.workdir, self.flash_name)
        if not os.path.exists(flash):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-b', self.image, '-f', 'qcow2', flash, self.flash_size)
        swap = os.path.join(self.workdir, self.swap_name)
        if not os.path.exists(swap):
            os.spawnlp(os.P_WAIT, self.img_bin, self.img_bin, 'create',
                '-f', 'qcow2', '-c', swap, self.swap_size)
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
            'create_udp' : (5, 5),
            'delete_udp' : (2, 2),
            'start' : (1, 1),
            'stop' : (1, 1),
            }
        }

    qemu_classes = {
        'qemu': QemuDeviceInstance,
        'pix': PIXInstance,
        'asa': ASAInstance,
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
        sep = '-'
        if not done:
            sep = ' '
        self.wfile.write("%3d%s%s\r\n" % (code, sep, msg))

    def handle(self):
        print "Connection from", self.client_address
        try:
            self.handle_one_request()
            while not self.close_connection:
                self.handle_one_request()
        except socket.error:
            pass

    def __get_tokens(self, request):
        input_ = cStringIO.StringIO(request)
        tokens = []
        try:
            tokens = csv.reader(input_, delimiter=' ').next()
        except StopIteration:
            pass
        return tokens

    def handle_one_request(self):
        request = self.rfile.readline()
        request = request.rstrip()      # Strip package delimiter.

        # Parse request.
        tokens = self.__get_tokens(request)
        if len(tokens) < 2:
            self.send_reply(self.HSC_ERR_PARSING, 1,
                            "At least a module and a command must be specified")
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
        if len(data) < self.modules[module][command][0] or \
           len(data) > self.modules[module][command][1]:
            self.send_reply(self.HSC_ERR_BAD_PARAM, 1,
                            "Bad number of parameters (%d with min/max=%d/%d)" %
                                (len(data),
                                 self.modules[module][command][0],
                                 self.modules[module][command][1])
                                )
            return

        # Call the function.
        method = getattr(self, mname)
        method(data)

    def do_qemuwrapper_version(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, __version__)

    def do_qemuwrapper_parser_test(self, data):
        for i in range(len(data)):
            self.send_reply(self.HSC_INFO_MSG, 0,
                            "arg %d (len %u): \"%s\"" % \
                            (i, len(data[i]), data[i])
                            )
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_module_list(self, data):
        for module in self.modules.keys():
            self.send_reply(self.HSC_INFO_MSG, 0, module)
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_cmd_list(self, data):
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
        qemu_path, = data
        try:
            os.access(qemu_path, os.F_OK)
            global QEMU_PATH
            QEMU_PATH = qemu_path
            print "Qemu path is now %s" % QEMU_PATH
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].bin = os.path.join(os.getcwd(), QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "access: %s" % e.strerror)

    def do_qemuwrapper_qemu_img_path(self, data):
        qemu_img_path, = data
        try:
            os.access(qemu_img_path, os.F_OK)
            global QEMU_IMG_PATH
            QEMU_IMG_PATH = qemu_img_path
            print "Qemu-img path is now %s" % QEMU_IMG_PATH
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].img_bin = os.path.join(os.getcwd(), QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "access: %s" % e.strerror)

    def do_qemuwrapper_working_dir(self, data):
        working_dir, = data
        try:
            os.chdir(working_dir)
            for qemu_name in QEMU_INSTANCES.keys():
                QEMU_INSTANCES[qemu_name].workdir = os.path.join(os.getcwd(), QEMU_INSTANCES[qemu_name].name)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "chdir: %s" % e.strerror)

    def do_qemuwrapper_reset(self, data):
        cleanup()
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemuwrapper_close(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1

    def do_qemuwrapper_stop(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1
        self.server.stop()

    def do_qemu_version(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, __version__)

    def __qemu_create(self, dev_type, name):
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
        dev_type, name = data
        if self.__qemu_create(dev_type, name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' created" % name)
        else:
            self.send_reply(self.HSC_ERR_CREATE, 1,
                            "unable to create Qemu instance '%s'" % name)

    def __qemu_delete(self, name):
        if not name in QEMU_INSTANCES.keys():
            return 1
        if QEMU_INSTANCES[name].process and \
        not QEMU_INSTANCES[name].stop():
            return 1
        del QEMU_INSTANCES[name]
        return 0

    def do_qemu_delete(self, data):
        name, = data
        if self.__qemu_delete(name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "Qemu '%s' deleted" % name)
        else:
            self.send_reply(self.HSC_ERR_DELETE, 1,
                            "unable to delete Qemu instance '%s'" % name)

    def do_qemu_setattr(self, data):
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
        print >> sys.stderr, '!! %s.%s = %s' % (name, attr, value)
        setattr(QEMU_INSTANCES[name], attr, value)
        self.send_reply(self.HSC_INFO_OK, 1, "%s set for '%s'" % (attr, name))

    def do_qemu_create_nic(self, data):
        name, vlan, mac = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        QEMU_INSTANCES[name].nic[int(vlan)] = mac
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_create_udp(self, data):
        name, vlan, sport, daddr, dport = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        udp_connection = UDPConnection(sport, daddr, dport)
        udp_connection.resolve_names()
        QEMU_INSTANCES[name].udp[int(vlan)] = udp_connection
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        
    def do_qemu_delete_udp(self, data):
        name, vlan = data
        if not name in QEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find Qemu '%s'" % name)
            return
        del QEMU_INSTANCES[name].udp[int(vlan)]
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_qemu_start(self, data):
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


class DaemonThreadingMixIn(SocketServer.ThreadingMixIn):
    daemon_threads = True


class QemuWrapperServer(DaemonThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
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
    if not os.path.exists(PEMU_DIR):
        print "Unpacking pemu binary."
        f = cStringIO.StringIO(base64.decodestring(pemubin.ascii))
        tar = tarfile.open('dummy', 'r:gz', f)
        for member in tar.getmembers():
            tar.extract(member)

    server = QemuWrapperServer(("", PORT), QemuWrapperRequestHandler)

    print "Qemu TCP control server started (port %d)." % PORT
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        cleanup()


if __name__ == '__main__':
    print "Qemu Emulator Wrapper (version %s)" % __version__
    print "Copyright (c) 2007-2009 Thomas Pani & Jeremy Grossmann"
    print

    if platform.system() == 'Windows':
        try:
            import pywintypes, win32api, win32con, win32process
        except ImportError:
            print >> sys.stderr, "You need pywin32 installed to run qemuwrapper!"
            sys.exit(1)

    main()
