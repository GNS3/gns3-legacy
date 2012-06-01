# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
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
# http://www.gns3.net/contact
#

import os, subprocess, time
from GNS3.Utils import debug
from PyQt4 import QtCore

try:
    import win32pipe, win32file
except:
    pass

class PipeCapture(QtCore.QThread):

    def __init__(self, input_capture_file_path, capture_cmd, wireshark_pipe):
        self.input_capture_file_path = input_capture_file_path
        self.capture_cmd = capture_cmd
        self.wireshark_pipe = wireshark_pipe
        self.process = None
        self.pipe = None
        QtCore.QThread.__init__(self)

    def __del__(self):

        debug("Deleting pipe thread ...")
        if self.pipe:
            win32file.CloseHandle(self.pipe)

    def run(self):

        try:
            in_file = open(self.input_capture_file_path, 'rb')
        except IOError, e:
            debug("Cannot open capture file: %s") % unicode(e)
            self.exit()
            return
        try:
            self.process = subprocess.Popen(self.capture_cmd.strip())
        except (OSError, IOError), e:
            debug("Cannot start Wireshark: %s") % unicode(e)
            self.exit()
            return
        try:
            self.pipe = win32pipe.CreateNamedPipe(self.wireshark_pipe, win32pipe.PIPE_ACCESS_OUTBOUND, win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT, 1, 65536, 65536, 300, None)
            win32pipe.ConnectNamedPipe(self.pipe, None)
        except win32pipe.error:
            debug("Error while creating and connecting the pipe ...")
            win32file.CloseHandle(self.pipe)
            self.exit()
            return

        while True:
            data = in_file.read()
            if not self.process or self.process.returncode != None:
                win32file.CloseHandle(self.pipe)
                debug("Wireshark is not running, deleting pipe ...")
                self.exit()
                return
            if data:
                try:
                    win32file.WriteFile(self.pipe, data)
                except:
                    win32file.CloseHandle(self.pipe)
                    debug("Wireshark has been closed, deleting pipe ...")
                    self.exit()
                    return
            else:
                time.sleep(0.5) #FIXME: find a better way to wake-up the thread only when there is data to read

if __name__ == '__main__':
    capture_cmd = "C:\Program Files (x86)\Wireshark\wireshark.exe -k -i %p"
    pipe = r'\\.\pipe\GNS3\R1_to_R2'
    capture_file = "capture.pcap"
    path = unicode(capture_cmd.replace("%p", "%s") % pipe)
    t = PipeCapture(capture_file, path, pipe)
    t.setDaemon(True)
    t.start()
    t.join(10) # let run the thread for 10 seconds and stop it
