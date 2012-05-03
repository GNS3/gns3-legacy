#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

# This test-case shows a reproducible lockup of VirtualBox VBoxSVC component on Windows XP hosts.

import time, os
from vboxapi import VirtualBoxManager

import vboxcontroller_4_1

class VBoxTestCase():

    def __init__(self):
        #debugmsg(2, "class xVBOXInstance::__init__(%s)" % str(name))
        self.nic = {}
        self.nics = '6'
        self.udp = {}
        self.capture = {}
        self.netcard = 'automatic'
        self.guestcontrol_user = ''
        self.guestcontrol_password = ''
        self.process = None
        self.mgr = VirtualBoxManager(None, None)
        self.vbox = self.mgr.vbox
        self.vmname = ""
        self.vbc = vboxcontroller_4_1.VBoxController_4_1(self.mgr)

    def startvm(self):
        return self.vbc.start(self.vmname, self.nics, self.udp, self.capture, self.netcard)

    def reset(self):
        return self.vbc.reset()

    def stop(self):
        return self.vbc.stop()

    def suspend(self):
        return self.vbc.suspend()

    def resume(self):
        return self.vbc.resume()

vmobj1 = VBoxTestCase()
vmobj1.vmname = "Windows XP immu 14"
for x in range(100):
    print os.linesep + "TEST iteration = %d" % (x+1) + os.linesep
    vmobj1.startvm()
    time.sleep(5)
    vmobj1.stop()
