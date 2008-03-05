#!/usr/bin/env python
# $Id: pemuwrapper.py 27 2008-03-04 17:17:46Z tpani $
#
# Copyright (c) 2007 Thomas Pani
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

import pemubin


__author__ = 'Thomas Pani'
__version__ = '0.2.3'   # TODO: remove RC when done

PORT = 10525
PEMU_INSTANCES = {}

PEMU_BIN = 'pemu'
if platform.system() == 'Windows':
    PEMU_BIN = 'pemu.exe'
else:
    PEMU_BIN = 'pemu'

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


class PEMUInstance:
    def __init__(self, name):
        self.name = name
        self.ram = '128'
        self.console = ''
        self.serial = '0x12345678'
        self.key = '0x00000000,0x00000000,0x00000000,0x00000000'
        self.image = ''
        self.nic = {}
        self.udp = {}
        self.process = None
        self.workdir = None


    def create(self):
        self.workdir = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        # Imbedded FLASH no longer needed with pemu 2008-03-03
        #flashfile = os.path.join(self.workdir, 'FLASH')
        #if not os.path.exists(flashfile):
        #    print "Unpacking FLASH..."
        #    f = cStringIO.StringIO(base64.decodestring(pemubin.flash))
        #    tar = tarfile.open('dummy', 'r:gz', f)
        #    for member in tar.getmembers():
        #        tar.extract(member, self.workdir)
        #    print "Done unpacking FLASH."

    def write_config(self):
        f = open(os.path.join(self.workdir, 'pemu.ini'), 'w')
        f.writelines(('serial=%s\n' % self.serial,
                'image=%s\n' % self.image,
                'key=%s\n' % self.key))
                # No longer needed, bios is integrated now
                #'bios1=%s\n' % os.path.join(PEMU_DIR, 'mybios_d8000'),
                #'bios2=%s\n' % os.path.join(PEMU_DIR, 'bios.bin'),
                #'bios_checksum=1\n'))
        f.close()

    def start(self):
        command = os.path.join(PEMU_DIR, PEMU_BIN)

        for vlan in range(6):
            if vlan in self.nic:
                command += ' -net nic,vlan=%d,macaddr=%s' % (vlan, self.nic[vlan])
            else:
                # add a default NIC for pemu (we always add 4 NICs)
                command += ' -net nic,vlan=%d,macaddr=00:00:ab:cd:ef:%02d' % (vlan, vlan)
            if vlan in self.udp:
                command += ' -net udp,vlan=%s,sport=%s,dport=%s,daddr=%s' % \
                        (vlan, self.udp[vlan].sport,
                         self.udp[vlan].dport,
                         self.udp[vlan].daddr)

        if self.console:
            command += ' -serial telnet::%s,server,nowait' % self.console
        command += ' -m %s FLASH' % self.ram
        print "    command:", command
        try:
            self.process = subprocess.Popen(command.split(),
                                            stdin=subprocess.PIPE,
                                            cwd=self.workdir)
        except OSError, e:
            print >> sys.stderr, "Unable to start PEMU instance", self.name
            print >> sys.stderr, e
            return False
        print "    pid:", self.process.pid

        if platform.system() == 'Windows':
            print "Setting priority class to BELOW_NORMAL"
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,
                    0, self.process.pid)
            returncode =  win32process.SetPriorityClass(handle,
                    win32process.BELOW_NORMAL_PRIORITY_CLASS)
            if returncode:
                print "   failed."

        else:
            print "Renicing to 19"
            returncode = subprocess.call(['renice', '+19', str(self.process.pid)])
            if returncode:
                print "    failed."

        return True

    def stop(self):
        if platform.system() == 'Windows':
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, self.process.pid)
            try:
                if win32api.TerminateProcess(handle, 0):
                    return False
            except pywintypes.error, e:
                print >> sys.stderr, "Unable to stop PEMU instance", self.name
                print >> sys.stderr, e[2]
                return False
        else:
            import signal
            try:
                os.kill(self.process.pid, signal.SIGINT)
            except OSError, e:
                print >> sys.stderr, "Unable to stop PEMU instance", self.name
                print >> sys.stderr, e
                return False
        self.process = None

        return True


class PEMUWrapperRequestHandler(SocketServer.StreamRequestHandler):

    modules = {
        'pemuwrapper' : {
            'version' : (0, 0),
            'parser_test' : (0, 10),
            'module_list' : (0, 0),
            'cmd_list' : (1, 1),
            'working_dir' : (1, 1),
            'reset' : (0, 0),
            'close' : (0, 0),
            'stop' : (0, 0),
            },
        'pemu' : {
            'version' : (0, 0),
            'create' : (1, 1),
            'delete' : (1, 1),
            'set_image' : (2, 2),
            'set_serial' : (2, 2),
            'set_key' : (2, 2),
            'create_nic' : (3, 3),
            'create_udp' : (5, 5),
            'set_ram' : (2, 2),
            'set_con_tcp' : (2, 2),
            'start' : (1, 1),
            'stop' : (1, 1),
            }
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

    def do_pemuwrapper_version(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, __version__)

    def do_pemuwrapper_parser_test(self, data):
        for i in range(len(data)):
            self.send_reply(self.HSC_INFO_MSG, 0,
                            "arg %d (len %u): \"%s\"" % \
                            (i, len(data[i]), data[i])
                            )
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemuwrapper_module_list(self, data):
        for module in self.modules.keys():
            self.send_reply(self.HSC_INFO_MSG, 0, module)
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemuwrapper_cmd_list(self, data):
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

    def do_pemuwrapper_working_dir(self, data):
        working_dir, = data
        try:
            os.chdir(working_dir)
            self.send_reply(self.HSC_INFO_OK, 1, "OK")
        except OSError, e:
            self.send_reply(self.HSC_ERR_INV_PARAM, 1,
                            "chdir: %s" % e.strerror)

    def do_pemuwrapper_reset(self, data):
        cleanup()
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemuwrapper_close(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1

    def do_pemuwrapper_stop(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, "OK")
        self.close_connection = 1
        self.server.stop()

    def do_pemu_version(self, data):
        self.send_reply(self.HSC_INFO_OK, 1, pemubin.__version__)

    def __pemu_create(self, name):
        if name in PEMU_INSTANCES.keys():
            print >> sys.stderr, "Unable to create PEMU instance", name
            print >> sys.stderr, "%s already exists" % name
            return 1
        pemu_instance = PEMUInstance(name)

        try:
            pemu_instance.create()
        except OSError, e:
            print >> sys.stderr, "Unable to create PEMU instance", name
            print >> sys.stderr, e
            return 1

        PEMU_INSTANCES[name] = pemu_instance
        return 0

    def do_pemu_create(self, data):
        name, = data
        if self.__pemu_create(name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "PEMU '%s' created" % name)
        else:
            self.send_reply(self.HSC_ERR_CREATE, 1,
                            "unable to create PEMU instance '%s'" % name)

    def __pemu_delete(self, name):
        if not name in PEMU_INSTANCES.keys():
            return 1
        if PEMU_INSTANCES[name].process and \
        not PEMU_INSTANCES[name].stop():
            return 1
        del PEMU_INSTANCES[name]
        return 0

    def do_pemu_delete(self, data):
        name, = data
        if self.__pemu_delete(name) == 0:
            self.send_reply(self.HSC_INFO_OK, 1, "PEMU '%s' deleted" % name)
        else:
            self.send_reply(self.HSC_ERR_DELETE, 1,
                            "unable to delete PEMU instance '%s'" % name)

    def do_pemu_set_image(self, data):
        name, image = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].image = image
        self.send_reply(self.HSC_INFO_OK, 1, "Image set for '%s'" % name)

    def do_pemu_set_serial(self, data):
        name, serial = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].serial = serial
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_set_key(self, data):
        name, key = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].key = key
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_create_nic(self, data):
        name, vlan, mac = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].nic[int(vlan)] = mac
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_create_udp(self, data):
        name, vlan, sport, daddr, dport = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        udp_connection = UDPConnection(sport, daddr, dport)
        udp_connection.resolve_names()
        PEMU_INSTANCES[name].udp[int(vlan)] = udp_connection
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_set_ram(self, data):
        name, ram = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].ram = ram
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_set_con_tcp(self, data):
        name, console = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].console = console
        self.send_reply(self.HSC_INFO_OK, 1, "OK")

    def do_pemu_start(self, data):
        name, = data
        if not name in PEMU_INSTANCES.keys():
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        PEMU_INSTANCES[name].write_config()
        if not PEMU_INSTANCES[name].start():
            self.send_reply(self.HSC_ERR_START, 1,
                            "unable to start instance '%s'" % name)
        else:
            self.send_reply(self.HSC_INFO_OK, 1, "PEMU '%s' started" % name)

    def do_pemu_stop(self, data):
        name, = data
        if not PEMU_INSTANCES[name].process:
            self.send_reply(self.HSC_ERR_UNK_OBJ, 1,
                            "unable to find PEMU '%s'" % name)
            return
        if not PEMU_INSTANCES[name].stop():
            self.send_reply(self.HSC_ERR_STOP, 1,
                            "unable to stop instance '%s'" % name)
        else:
            self.send_reply(self.HSC_INFO_OK, 1, "PEMU '%s' stopped" % name)


class DaemonThreadingMixIn(SocketServer.ThreadingMixIn):
    daemon_threads = True


class PEMUWrapperServer(DaemonThreadingMixIn, SocketServer.TCPServer):
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
    for name in PEMU_INSTANCES.keys():
        if PEMU_INSTANCES[name].process:
            PEMU_INSTANCES[name].stop()
        del PEMU_INSTANCES[name]
    print "Shutdown completed."


def main():
    if not os.path.exists(PEMU_DIR):
        print "Unpacking pemu binary."
        f = cStringIO.StringIO(base64.decodestring(pemubin.ascii))
        tar = tarfile.open('dummy', 'r:gz', f)
        for member in tar.getmembers():
            tar.extract(member)

    server = PEMUWrapperServer(("", PORT), PEMUWrapperRequestHandler)

    print "PEMU TCP control server started (port %d)." % PORT
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        cleanup()


if __name__ == '__main__':
    print "PIX Emulator Wrapper (version %s)" % __version__
    print "Copyright (c) 2007 Thomas Pani."
    print

    if platform.system() == 'Windows':
        try:
            import pywintypes, win32api, win32con, win32process
        except ImportError:
            print >> sys.stderr, "You need pywin32 installed to run pemuwrapper!"
            sys.exit(1)

    main()
