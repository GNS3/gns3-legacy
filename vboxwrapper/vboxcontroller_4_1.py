#!/usr/bin/env python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (c) 2011 Alexey Eromenko "Technologov"
#
# Contributions by Pavel Skovajsa
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

#Written for GNS3.
#This module is used for actual control of the VirtualBox 4.1 hypervisor.
#vboxcontroller is controlled from "vboxwrapper"
#
#This module is separate from actual "vboxwrapper" code, because VirtualBox
#breaks API compatibility with every major release, so if we are to support
#several different major versions of VirtualBox, several controllers will need
#to be written.
#Essentially this module makes vboxwrapper future-proof.

#debuglevel: 0=disabled, 1=default, 2=debug, 3=deep debug
debuglevel = 0

import time
import sys
import os
import subprocess as sub

if debuglevel > 0:
    if sys.platform == 'win32':
        debugfilename = "C:\TEMP\gns3-vboxcontroller_4_1-log.txt"
    else:
        debugfilename = "/tmp/gns3-vboxcontroller_4_1-log.txt"
    try:
        dfile = open(debugfilename, 'wb')
    except:
        dfile = False
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

"""
# Basic VirtualBox initialization commands: (provided as example)

from vboxapi import VirtualBoxManager
mgr = VirtualBoxManager(None, None)
vbox = mgr.vbox
name = "my VM name"
mach = vbox.findMachine(name)
session = mgr.mgr.getSessionObject(vbox)

progress = mach.launchVMProcess(session, "gui", "")
progress.waitForCompletion(-1)

console=session.console
"""

class VBoxController_4_1():

    def __init__(self, io_vboxManager):
        debugmsg(2, "class VBoxController_4_1::__init__()")
        self.mgr = io_vboxManager
        self.vbox = self.mgr.vbox
        self.maxNics = 8
        self.constants = self.mgr.constants
        self.statBytesReceived = 0
        self.statBytesSent = 0
        self.stats = ""
        self.guestIP = ""
        self.VBoxBug9239Workaround = True # VBoxSVC crash on Windows hosts.

    def start(self, vmname, nics, udp, capture, netcard, first_nic_managed='True', headless_mode='False', pipe_name=None):
        debugmsg(2, "VBoxController_4_1::start()")
        # note: If you want to improve 'vboxwrapper' code, take a look at
        #   'vboxshell', the official VirtualBox frontend writen in python.
        self.vmname = vmname
        self.nics = nics
        self.udp = udp
        self.capture = capture
        self.netcard = netcard
        self.first_nic_managed = first_nic_managed
        self.headless_mode = headless_mode
        self.pipe_name = pipe_name
        debugmsg(3, "vmname = %s, nics = %s, capture = %s, netcard = %s, 1st NIC managed = %s" % (vmname, nics, capture, netcard, first_nic_managed))

        debugmsg(2, "findMachine() is starting vmname = %s" % unicode(self.vmname))
        try:
            self.mach = self.vbox.findMachine(self.vmname)
        except Exception, e:
            #This usually happens if you try to start non-existent or unregistered VM
            debugmsg(1, "findMachine() FAILED")
            debugmsg(1, e)
            return False
        # Maximum support network cards depends on the Chipset (PIIX3 or ICH9)
        self.maxNics = self.vbox.systemProperties.getMaxNetworkAdapters(self.mach.chipsetType)
        if not self._safeGetSessionObject():
            return False
        if not self._safeNetOptions():
            return False
        if not self._safeConsoleOptions():
            return False
        if not self._safeLaunchVMProcess():
            return False
        debugmsg(3, "progress.percent = %s" % str(self.progress.percent))
        if self.progress.percent != 100:
            #This will happen if you attemp to start VirtualBox with unloaded "vboxdrv" module.
            #  or have too little RAM or damaged vHDD, or connected to non-existent network.
            # We must unlock machine, otherwise it locks the VirtualBox Manager GUI. (on Linux hosts)
            self._safeUnlockMachine()
            return False
        try:
            self.console = self.session.console
        except:
            debugmsg(2, "get session.console FAILED")
        return True

    def reset(self):
        debugmsg(2, "VBoxController_4_1::reset()")
        try:
            self.progress = self.console.reset()
            self.progress.waitForCompletion(-1)
        except:
            #Do not crash "vboxwrapper", if stopping VM fails.
            #But return True anyway, so VM state in GNS3 can become "stopped"
            #This can happen, if user manually kills VBox VM.
            debugmsg(3, "VBoxController_4_1::reset() FAILED !")
            return True

    def stop(self):
        debugmsg(2, "VBoxController_4_1::stop()")
        if self.VBoxBug9239Workaround and sys.platform == 'win32':
            debugmsg(1, "doing VM stop with workaround...")
            p = sub.Popen('cd /D "%%VBOX_INSTALL_PATH%%" && VBoxManage.exe controlvm "%s" poweroff' % self.vmname, shell=True)
            p.communicate()
        else:
            try:
                self.progress = self.console.powerDown()
                #Wait for VM to actually go down:
                self.progress.waitForCompletion(-1)
                debugmsg(3, "self.progress.percent = %s" % str(self.progress.percent))
                #self._safeUnlockMachine()
            except:
                #Do not crash "vboxwrapper", if stopping VM fails.
                #But return True anyway, so VM state in GNS3 can become "stopped"
                #This can happen, if user manually kills VBox VM.
                return True

        #Shutdown all managed interfaces:
        if not self._safeLockMachine():
            return True
        try:
            mach2=self.session.machine
        except:
            debugmsg(3, "mach2=self.session.machine FAILED ! Skipping shutdown of interfaces...")
            return True

        #time.sleep(1)
        if self.first_nic_managed == 'False':
            # first nic is managed by GNS3
            start_nic = 0
        else:
            # We leave vNIC #1 (vnic = 0) for VirtualBox management purposes
            start_nic = 1

        for vnic in range(start_nic, int(self.nics)):
            debugmsg(3, "Disabling managed netadp %s" % str(vnic))
            if not self._safeDisableNetAdpFromMachine(mach2, vnic, disableAdapter=True):
                debugmsg(3, "Disabling managed netadp %s FAILED, skipped." % str(vnic))
                #Return True anyway, so VM state in GNS3 can become "stopped"
                return True
        self._safeSaveSettings(mach2)  #Doesn't matter if command returns True or False...
        self._safeUnlockMachine()  #Doesn't matter if command returns True or False...
        return True

    def suspend(self):
        debugmsg(2, "VBoxController_4_1::suspend()")
        try:
          self.console.pause()
        except:
          return False
        return True

    def resume(self):
        debugmsg(2, "VBoxController_4_1::resume()")
        try:
          self.console.resume()
        except:
          return False
        return True
    
    def setName(self, name):
        debugmsg(2, "VBoxController_4_1::setName()")
        try:
            self.mach.setGuestPropertyValue("NameInGNS3",name)
        except E_ACCESSDENIED:
            debugmsg(2, "setName FAILED : E_ACCESSDENIED")
            return False
        except VBOX_E_INVALID_VM_STATE:
            debugmsg(2, "setName FAILED : VBOX_E_INVALID_VM_STATE")
            return False
        except VBOX_E_INVALID_OBJECT_STATE:
            debugmsg(2, "setName FAILED : VBOX_E_INVALID_OBJECT_STATE")
            return False
        return True

    def displayWindowFocus(self):
        debugmsg(2, "VBoxController_4_1::displayWindowFocus()")
        # For example, look at "VBoxGlobal.cpp"
        self.hwnd = 0
        try:
            self.hwnd = self.mach.showConsoleWindow()
        except Exception, e:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, e)
        return True

    def create_udp(self, i_vnic, sport, daddr, dport):
        debugmsg(2, "VBoxController_4_1::create_udp(%s, %s, %s, %s)" % (str(i_vnic), str(sport), str(daddr), str(dport)))
        # FlexiNetwork: Link hot-add
        #if machine == 'stopped': return True
        try:
            if self.mach: pass
        except:
            # If machine not yet created (or is stopped), just skip...
            return True
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "delete_udp() FAILED, no retries left, giving up...")
                return False
            try:
                mach2=self.session.machine
                netadp = mach2.getNetworkAdapter(int(i_vnic))
                netadp.cableConnected=True
                netadp.attachmentType=self.constants.NetworkAttachmentType_Null
                mach2.saveSettings()
                netadp.attachmentType=self.constants.NetworkAttachmentType_Generic
                netadp.genericDriver="UDPTunnel"
                netadp.setProperty("sport", str(sport))
                netadp.setProperty("dest", daddr)
                netadp.setProperty("dport", str(dport))
                mach2.saveSettings()
                break
            except Exception, e:
                #Usually due to COM Error: "The object is not ready"
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "delete_udp() FAILED, retrying #%d" % (retry+1))
                time.sleep(0.75)
                continue
        return True

    def delete_udp(self, i_vnic):
        debugmsg(2, "VBoxController_4_1::delete_udp(%s)" % str(i_vnic))
        # FlexiNetwork: Link hot-remove
        try:
            if self.mach: pass
        except:
            # If machine not yet created (or is stopped), just skip...
            return True
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "delete_udp() FAILED, no retries left, giving up...")
                return False
            try:
                mach2=self.session.machine
                netadp = mach2.getNetworkAdapter(int(i_vnic))
                netadp.attachmentType=self.constants.NetworkAttachmentType_Null
                netadp.cableConnected=False
                mach2.saveSettings()
                break
            except Exception, e:
                #Usually due to COM Error: "The object is not ready"
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "delete_udp() FAILED, retrying #%d" % (retry+1))
                time.sleep(0.75)
                continue
        return True

    def _console_options(self):
        """
        # Example to manually set serial parameters with Python

        from vboxapi import VirtualBoxManager
        mgr = VirtualBoxManager(None, None)
        mach = mgr.vbox.findMachine("My VM")
        session = mgr.mgr.getSessionObject(mgr.vbox)
        mach.lockMachine(session, 1)
        mach2=session.machine
        serial_port = mach2.getSerialPort(0)
        serial_port.enabled = True
        serial_port.path = "/tmp/test_pipe"
        serial_port.hostMode = 1
        serial_port.server = True
        session.unlockMachine()
        
        """
        debugmsg(2, "VBoxController_4_1::_console_options()")
        #This code looks really ulgy due to constant 'try' and 'except' pairs.
        #But this is because VirtualBox COM interfaces constantly fails
        #  on slow or loaded hosts. (on both Windows and Linux hosts)
        #Without 'try/except' pairs it results in vboxwrapper crashes.
        #
        #To reproduce: Try to configure several VMs, and restart them all in
        #  loop on heavily loaded hosts.

        if not self._safeLockMachine():
            return False
        try:
            mach2=self.session.machine
        except:
            debugmsg(1, "_console_options() -> self.session.machine FAILED !")
            return False

        try:
            serial_port = mach2.getSerialPort(0)
        except:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, "_console_options() -> getSerialPort() FAILED !")
            return False

        try:
            if self.pipe_name:
                serial_port.enabled = True
                serial_port.path = self.pipe_name
                serial_port.hostMode = 1
                serial_port.server = True
            else:
                serial_port.enabled = False
        except:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, "_console_options() -> serial port settings FAILED !")
            return False

        if not self._safeSaveSettings(mach2):
            return False
        if not self._safeUnlockMachine():
            return False
        return True

    def _net_options(self):
        debugmsg(2, "VBoxController_4_1::_net_options()")
        #This code looks really ulgy due to constant 'try' and 'except' pairs.
        #But this is because VirtualBox COM interfaces constantly fails
        #  on slow or loaded hosts. (on both Windows and Linux hosts)
        #Without 'try/except' pairs it results in vboxwrapper crashes.
        #
        #To reproduce: Try to configure several VMs, and restart them all in
        #  loop on heavily loaded hosts.

        if not self._safeLockMachine():
            return False
        try:
            mach2=self.session.machine
        except:
            debugmsg(1, "_net_options() -> self.session.machine FAILED !")
            return False
        debugmsg(3, "self.nics = %s" % str(self.nics))
        debugmsg(3, "self.maxNics = %s" % str(self.maxNics))

        try:
            netadp_mgmt = mach2.getNetworkAdapter(0)
            adaptertype_mgmt = netadp_mgmt.adapterType
        except:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, "_net_options() -> getNetworkAdapter() FAILED !")
            return False

        if self.first_nic_managed == 'False':
            # first nic is managed by GNS3
            start_nic = 0
        else:
            # We leave vNIC #1 (vnic = 0) for VirtualBox management purposes
            start_nic = 1

        for vnic in range(start_nic, int(self.nics)):
            try:
                # Vbox API starts counting from 0
                netadp = mach2.getNetworkAdapter(vnic)
                #netadp = mach2.getNetworkAdapter(0)
            except:
                #Usually due to COM Error on loaded hosts: "The object is not ready"
                debugmsg(1, "_net_options() -> getNetworkAdapter() FAILED !")
                return False

            try:
                adaptertype = netadp.adapterType
            except:
                #Usually due to COM Error: "The object is not ready"
                debugmsg(1, "_net_options() -> netadp.adapterType FAILED !")
                return False
            debugmsg(3, "Changing netadp %s type to %s" % (str(vnic), str(self.netcard)))
            if self.netcard == "pcnet2": # "AMD PCnet-II"
                adaptertype = 1
            if self.netcard == "pcnet3": # "AMD PCnet-III"
                adaptertype = 2
            if self.netcard == "e1000": # "Intel PRO/1000 MT Desktop"
                adaptertype = 3
            if self.netcard == "virtio": # "Red Hat VirtIO para-virtual adapter"
                adaptertype = 6
            if self.netcard == "automatic": # "Auto-guess, based on management NIC"
                adaptertype = adaptertype_mgmt
            try:
                netadp.adapterType = adaptertype
            except:
                #Usually due to COM Error: "The object is not ready"
                debugmsg(1, "_net_options() -> netadp.adapterType FAILED !")
                return False

            if vnic in self.udp:
                debugmsg(3, "Changing netadp %s mode" % str(vnic))
                try:
                    netadp.enabled=True
                    netadp.cableConnected=True
                    # Temporary hack around VBox-UDP patch limitation: inability to use DNS
                    if str(self.udp[vnic].daddr) == 'localhost':
                        daddr = '127.0.0.1'
                    else:
                        daddr = str(self.udp[vnic].daddr)
                    netadp.attachmentType=self.constants.NetworkAttachmentType_Generic
                    netadp.genericDriver="UDPTunnel"
                    netadp.setProperty("sport", str(self.udp[vnic].sport))
                    netadp.setProperty("dest", daddr)
                    netadp.setProperty("dport", str(self.udp[vnic].dport))
                except:
                    #Usually due to COM Error: "The object is not ready"
                    debugmsg(1, "_net_options() -> netadp.attach..() FAILED !")
                    return False
            else:
                #Shutting down unused interfaces... vNICs <2-N>
                debugmsg(3, "Detaching managed netadp %s" % str(vnic)) #It could be re-attached at run-time.
                if not self._safeDetachNetAdp(netadp):
                   return False

            if vnic in self.capture:
                if not self._safeEnableCapture(netadp, self.capture[vnic]):
                    return False

        for vnic in range(int(self.nics), self.maxNics):
            debugmsg(3, "Disabling remaining netadp %s" % str(vnic))
            if not self._safeDisableNetAdpFromMachine(mach2, vnic):
                return False
        if not self._safeSaveSettings(mach2):
            return False
        if not self._safeUnlockMachine():
            return False
        return True

    def get_nio_stats(self, vnic):
        # This function retrieves sent/received bytes from VMs.
        debugmsg(3, "VBoxController_4_1::get_nio_stats(%s)" % str(vnic))
        # In VirtualBox, Packets counters are implemented only for kernel-space
        # network backends, such as 'intnet'. Not for NAT / UDP.
        # Therefore we are limited to byte counters.
        self.statBytesReceived = self.statBytesSent = 0
        self.stats = "0 0 guestip|"
        # If machine is not yet created (or is stopped), just skip...
        try:
            if self.mach: pass
        except:
            return True
        try:
            # We skip first vNIC, as this is not managed by GNS3.
            # note: This code won't handle > 10 vNICs.
            # Parsing XML output...
            self.statBytesReceived = self.console.debugger.getStats("*%s/ReceiveBytes"  % str(int(vnic)-1), False).splitlines()[2].split("=")[1].split('"')[1]
            self.statBytesSent     = self.console.debugger.getStats("*%s/TransmitBytes" % str(int(vnic)-1), False).splitlines()[2].split("=")[1].split('"')[1]
            debugmsg(3, "self.statBytesReceived = %s" % str(self.statBytesReceived))
            debugmsg(3, "self.statBytesSent = %s" % str(self.statBytesSent))
        except Exception, e:
            debugmsg(3, e)
            #Can happen due to COM failure, or because machine is not running.
        if not self.get_nio_guestip(vnic-1):
            return False
        self.stats = str(self.statBytesReceived) + " " + str(self.statBytesSent) + " guestip|" + self.guestIP
        debugmsg(3, "self.stats = %s" % str(self.stats))
        return True

    def get_nio_guestip(self, vnic):
        # This function retrieves IP addresses from running virtual machines,
        # provided that "GuestAdditions" are installed.
        debugmsg(3, "VBoxController_4_1::get_nio_guestip(%s)" % str(vnic))
        self.guestIP = ""
        # If machine is not yet created (or is stopped), just skip...
        try:
            if self.mach: pass
        except:
            return True
        # note: There is no way to automatically map between multiple IPs and
        # multiple vNICs, so we use MAC addresses for this.
        if not self._safeGetMACaddr(vnic): # We skip first vNIC, as this is not managed by GNS3.
            return True
        debugmsg(3, "MACAddress = %s" % str(self.MACAddress))
        # Here I need to count all possible logical networks in Guest
        try:
            guest_networks = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/Count")
        except Exception, e:
            debugmsg(1, e)
            return True
        debugmsg(3, "guest_networks = %s" % str(guest_networks))
        # Two loops are needed, because I want to sort all IPv4 addresses first, and only then all IPv6 addresses.
        try:
            # Retrieve matching IPv4 addresses
            for x in range(int(guest_networks)):
                guestMAC = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/%s/MAC" % str(x))
                debugmsg(3, "guestMAC = %s" % str(guestMAC))
                # Comparing MAC address from VirtualBox host side vs. GuestAdditions report:
                if self.MACAddress == guestMAC:
                    try:
                        guestIPv4 = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/%s/V4/IP" % str(x))
                        netmask_long = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/%s/V4/Netmask" % str(x))
                        debugmsg(3, "guestIP = %s" % str(guestIPv4))
                        self.guestIP += guestIPv4 + "/" + str(self._subnetcalc(netmask_long)) + " "
                    except Exception, e:
                        debugmsg(2, e)
                        #pass
            # Retrieve matching IPv6 addresses
            for x in range(int(guest_networks)):
                guestMAC = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/%s/MAC" % str(x))
                debugmsg(3, "guestMAC = %s" % str(guestMAC))
                # Comparing MAC address from VirtualBox host side vs. GuestAdditions report:
                if self.MACAddress == guestMAC:
                    try:
                        guestIPv6 = self.mach.getGuestPropertyValue("/VirtualBox/GuestInfo/Net/%s/V6/IP" % str(x))
                        debugmsg(3, "guestIPv6 = %s" % str(guestIPv6))
                        self.guestIP += guestIPv6 + " "
                    except Exception, e:
                        debugmsg(2, e)
                        #pass
        except Exception, e:
            debugmsg(1, e)
            return True
        return True

    def _subnetcalc(self, netmask_long):
        #This function calculates short IP subnet mask, from long one, so for "255.255.255.0", it will return "24"
        debugmsg(3, "VBoxController_4_1::_subnetcalc(%s)" % str(netmask_long))
        sm=""
        for ni_octet in range(4):
            octet_long = int(netmask_long.split('.')[ni_octet])
            if octet_long == 255:
                sm += "1" * 8
                continue

            for bit in range(8):
                #Total 8 bits per octet. <0...7>
                if octet_long >= 2**(7-bit):
                    octet_long -= 2**(7-bit)
                    sm += "1"
        return len(sm)

    def vboxexec(self, command, guestcontrol_user, guestcontrol_password):
        # This function executes arbitary commands on VMs, and gets STDOUT results.
        # Technologov: to improve upon my work, please look at vboxshell's gexec command.
        debugmsg(3, "VBoxController_4_1::vboxexec(%s, %s, %s)" % (unicode(command), unicode(guestcontrol_user), unicode(guestcontrol_password)))
        self.result = ""
        self.guestcontrol_user = guestcontrol_user
        self.guestcontrol_password = guestcontrol_password
        timeout = 10 # in seconds
        flags = 0
        env = ""
        # VirtualBox GuestControl execute doesn't simulate shell properly,
        #so many things must be workarounded in our code.
        # In particular, it cannot auto-guess file extensions, and cannot execute shell commands.
        #windows_shell_commands = ['dir', 'type', 'copy', 'move', 'start', 'echo']
        #return
        # If machine is not yet created (or is stopped), just skip...
        try:
            if self.mach: pass
        except:
            #self.result = "The VM is not Running"
            return
        if len(command) is 0:
            self.result = "No command received"
            return True
        try:
            #self.OSTypeID = self.console.guest.OSTypeID
            # In some versions of VBox, "args" parameter shall contain program name as argv[0]
            #if command.split()[0] in windows_shell_commands:
            #    #mycommand = "cmd.exe"+" /c "+command.split()+" >1"
            #    mycommand = " /c "+command.split()+" >1"
            #    (progress, pid) = self.console.guest.executeProcess("cmd.exe", flags, mycommand, env, self.guestcontrol_user, self.guestcontrol_password, timeout*1000)
            #else:
            #    (progress, pid) = self.console.guest.executeProcess(command.split()[0], flags, command.split()[1:], env, self.guestcontrol_user, self.guestcontrol_password, timeout*1000)
            #    #(progress, pid) = self.console.guest.executeProcess(command.split()[0], flags, command.split(), env, self.guestcontrol_user, self.guestcontrol_password, timeout*1000)
            (progress, pid) = self.console.guest.executeProcess(command.split()[0], flags, command.split()[1:], env, self.guestcontrol_user, self.guestcontrol_password, timeout*1000)
            debugmsg(1, "executed with pid %d" %(pid))
            while True:
                data = self.console.guest.getProcessOutput(pid, 0, 10000, 4096)
                if data and len(data) > 0:
                    sys.stdout.write(data)
                    self.result += data
                    continue
                debugmsg(3, "progress.percent = %s" % str(progress.percent))
                progress.waitForCompletion(60)
                debugmsg(3, "progress.percent = %s" % str(progress.percent))
                data = self.console.guest.getProcessOutput(pid, 0, 0, 4096)
                if data and len(data) > 0:
                    sys.stdout.write(data)
                    self.result += data
                    continue
                if progress.completed:
                    break
        except Exception, e:
            debugmsg(3, e)
            #Can happen due to COM failure, or because GuestAdditions not running.
            try:
                self.result = "VirtualBox Exception: "+e.__str__()
            except Exception, e2:
                debugmsg(3, e2)

        # Our TCP client, dynagen_vbox_lib, apparently dies when receives the
        #output of GuestControl exec as-is, so I do some pre-formatting here,
        #before sending the result back.
        rebuilt_stream = ""
        for x in range(len(self.result.splitlines())):
            rebuilt_stream += self.result.splitlines()[x]+"\n"
            #debugmsg(3, "self.result.splitlines()[%d] = %s" % (x, str(self.result.splitlines()[x])))
        self.result = rebuilt_stream
        debugmsg(3, "self.result = %s" % unicode(self.result))
        return True

    def _safeGetMACaddr(self, i_vnic):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeGetMACaddr()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "_safeGetMACaddr() FAILED, no retries left, giving up...")
                return False
            try:
                netadp = self.mach.getNetworkAdapter(i_vnic)
                self.MACAddress = netadp.MACAddress
                break
            except Exception, e:
                #Usually due to COM Error: "The object is not ready"
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "_safeGetMACaddr() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True

    def _safeEnableCapture(self, i_netadp, i_filename):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeEnableCapture()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "_safeEnableCapture() FAILED, no retries left, giving up...")
                return False
            try:
                i_netadp.traceEnabled=True
                i_netadp.traceFile=i_filename
                break
            except:
                debugmsg(3, "_safeEnableCapture() FAILED, retrying #%d" % (retry+1))
                time.sleep(0.75)
                continue
        return True

    def _safeLaunchVMProcess(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeLaunchVMProcess()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "launchVMProcess() FAILED, no retries left, giving up...")
                return False
            try:
                if self.headless_mode == 'True':
                    mode = "headless"
                else:
                    mode = "gui"
                print "Starting %s in %s mode" % (self.vmname, mode)
                self.progress = self.mach.launchVMProcess(self.session, mode, "")
                break
            except Exception, e:
                #This will usually happen if you try to start the same VM twice,
                #  but may happen on loaded hosts too...
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "launchVMProcess() FAILED, retrying #%d" % (retry+1))
                time.sleep(0.6)
                continue
        debugmsg(3, "waitForCompletion()")
        try:
            self.progress.waitForCompletion(-1)
        except Exception, e:
            debugmsg(1, e)
            return False
        return True

    def _safeDisableNetAdpFromMachine(self, i_mach, i_vnic, disableAdapter=True):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeDisableNetAdpFromMachine()")
        #This command is retried several times, because it fails more often...
        retries=6
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "_safeDisableNetAdpFromMachine() FAILED, no retries left, giving up...")
                return False
            try:
                netadp = i_mach.getNetworkAdapter(i_vnic)
                debugmsg(3, "_safeDisableNetAdpFromMachine() disabling trace...")
                netadp.traceEnabled=False
                debugmsg(3, "_safeDisableNetAdpFromMachine() trace disabled.")
                netadp.attachmentType=self.constants.NetworkAttachmentType_Null
                if disableAdapter:
                    netadp.enabled=False
                break
            except Exception, e:
                #Usually due to COM Error: "The object is not ready"
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "_safeDisableNetAdpFromMachine() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True

    def _safeDetachNetAdp(self, i_netadp):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeDetachNetAdp()")
        try:
            i_netadp.enabled=True
            i_netadp.attachmentType=self.constants.NetworkAttachmentType_Null
            i_netadp.cableConnected=False
        except:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, "_safeDetachNetAdp() FAILED !")
            return False
        return True

    def _safeSaveSettings(self, i_mach):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeSaveSettings()")
        try:
            i_mach.saveSettings()
        except:
            #Usually due to COM Error: "The object is not ready"
            debugmsg(1, "_safeSaveSettings() FAILED !")
            return False
        return True

    def _safeGetSessionObject(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeGetSessionObject()")
        try:
            self.session = self.mgr.mgr.getSessionObject(self.vbox)
        except:
            #FAILs on heavily loaded hosts...
            debugmsg(1, "getSessionObject() FAILED")
            return False
        return True

    def _safeNetOptions(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeNetOptions()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "_net_options() FAILED, no retries left, giving up...")
                return False
            if self._net_options():
                break
            else:
                #fails on heavily loaded hosts...
                debugmsg(1, "_net_options() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True

    def _safeConsoleOptions(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeConsoleOptions()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "_console_options() FAILED, no retries left, giving up...")
                return False
            if self._console_options():
                break
            else:
                #fails on heavily loaded hosts...
                debugmsg(1, "_console_options() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True

    def _safeLockMachine(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeLockMachine()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "lockMachine() FAILED, no retries left, giving up...")
                return False
            try:
                self.mach.lockMachine(self.session, 1)
                break
            except Exception, e:
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "lockMachine() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True

    def _safeUnlockMachine(self):
        #_safe*() functions exist as a protection against COM failure on loaded hosts.
        debugmsg(3, "VBoxController_4_1::_safeUnlockMachine()")
        #This command is retried several times, because it fails more often...
        retries=4
        for retry in range(retries):
            if retry == (retries-1):
                debugmsg(1, "unlockMachine() FAILED, no retries left, giving up...")
                return False
            try:
                self.session.unlockMachine()
                break
            except Exception, e:
                if retry == (retries-2):
                    debugmsg(1, e)
                debugmsg(3, "unlockMachine() FAILED, retrying #%d" % (retry+1))
                time.sleep(1)
                continue
        return True
