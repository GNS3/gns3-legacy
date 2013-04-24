#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

"""
portTracker_lib.py
Copyright (C) 2012 Jeremy Grossmann

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import socket, random, time

DEBUG = False

class portTracker:

    tcptrack = {}
    udptrack = {}

    tcptrack['localhost'] = []
    udptrack['localhost'] = []
    local_addresses = ['0.0.0.0', '127.0.0.1', 'localhost', '::1', '0:0:0:0:0:0:0:1']
    local_addresses.append(socket.gethostname())
    try:
        local_addresses.append(socket.gethostbyname(socket.gethostname()))
    except:
        # Dumb admin?
        print "WARNING: Your host file miss an entry for " + socket.gethostname()

    def addLocalAddress(self, addr):

        try:
            debug("registering additional local address %s" % addr)
            if addr not in self.local_addresses:
                self.local_addresses.append(addr)
        except:
            pass

    def getNotAvailableTcpPortRange(self, host, start_port, max_port=10):

        not_free_ports = []
        end = start_port + max_port
        try:
            for port in range(start_port, end + 1):
                try:
                    # timeout is 200 ms
                    s = socket.create_connection((host, port), 0.2)
                except socket.error:
                    continue
                else:
                    # Not available
                    debug("port %i is already in use by another program" % port)
                    not_free_ports.append(port)
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
        except:
            debug("unexpected exception with create_connection")
        return not_free_ports

    def getAvailableTcpPort(self, host, start_port, max_port=10):

        # not a local host, do not try to bind it
        if host not in self.local_addresses:
            return start_port
        end = start_port + max_port
        try:
            for port in range(start_port, end + 1):
                try:
                    if host.__contains__(':'):
                        # IPv6 address support
                        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                    else:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.bind((host, port))
                except socket.error, e:
                    # Not available
                    if (max_port != 0):
                        debug("port %i is already in use by another program (bind error on 0.0.0.0 -> %s)" % (port, e))
                    continue
                else:
                    # Available
                    s.close()
                    if port not in self.tcptrack['localhost']:
                        return port
                    else:
                        debug("port %i is not in use but already in the tracker" % port)
                        continue
        except:
            debug("unexpected exception with bind")
        if (max_port != 0):
            debug("couldn't find a non-listening port in range %i to %i" % (start_port, end))
        else:
            debug("port %s is not free to use" % start_port)
        return None

    def allocateTcpPort(self, host, port, max_tries=10):

        origin_port = port
        origin_host = host
        if host in self.local_addresses:
            host = 'localhost'
        if not self.tcptrack.has_key(host):
            self.tcptrack[host] = []
        i = 0
        while i <= max_tries:
            allocated_port = self.getAvailableTcpPort(origin_host, port, int(round(max_tries / 2)))
            if allocated_port and allocated_port not in self.tcptrack[host]:
                self.tcptrack[host].append(allocated_port)
                debug("allocate port %i" % allocated_port)
                return allocated_port
            else:
                # Could not find a port, try random ones ...
                port = random.randint(origin_port, origin_port + 100)
                debug("trying random port %i" % port)
                i += 1
                continue
        # could not find an available port, return port of origin and hope for the best
        debug("WARNING: couldn't find any available port!!!")
        return origin_port

    def tcpPortIsFree(self, host, port):

        if host in self.local_addresses:
            host = 'localhost'
        if self.tcptrack.has_key(host) and port in self.tcptrack[host]:
            # workaround, let's say the port is free to use
            debug("freeing port (already allocated) %i" % port)
            self.tcptrack[host].remove(port)
            #return False
        # forced to do this as sometimes the port of a (just) closed application is not considered free
        #if not self.getAvailableTcpPort(host, port, 0):
        #    return False
        return True

    def freeTcpPort(self, host, port):

        if host in self.local_addresses:
            host = 'localhost'
        if self.tcptrack.has_key(host) and port in self.tcptrack[host]:# and not self.tcpPortIsFree(host, port):
            debug("freeing port %i" % port)
            self.tcptrack[host].remove(port)
        else:
            debug("could not free port %i (not in tracker)" % port)

    def setTcpPort(self, host, port):

        if host in self.local_addresses:
            host = 'localhost'
        debug("adding port %i" % port)
        self.tcptrack[host].append(port)

    def clearAllTcpPort(self):

        debug("freeing all TCP ports")
        self.tcptrack.clear()
        self.tcptrack['localhost'] = []

    def showTcpPortAllocation(self):

        for (host, ports) in self.tcptrack.iteritems():
            print "%s is using the following TCP ports" % host
            print ports

def setdebug(flag):
    """ If true, print out debugs
    """

    global DEBUG
    DEBUG = flag

def debug(string):
    """ Print string if debugging is true
    """

    global DEBUG

    if DEBUG:
        curtime = time.strftime("%H:%M:%S")
        print "%s: DEBUG (1): PORT TRACKER: %s" % (curtime, unicode(string))

if __name__ == '__main__':

    track = portTracker()
    print track.allocateTcpPort('localhost', 7200, 4)
