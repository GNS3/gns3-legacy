#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

from PyQt4 import QtCore, QtGui

##class Prompt(QtGui.QLineEdit):
##    '''Custom QLine Edit'''
##
##    def __init__(self, *args):
##    
##        QtGui.QLineEdit.__init__(self, *args)
##        self.history = []
##        self.history_pos = 0
##        QtCore.QObject.connect(self, QtCore.SIGNAL('returnPressed()'), self.slotReturnPressed)
##
##    def slotReturnPressed(self):
##        '''Called if the return key is pressed'''
##
##        cmd = unicode(self.text())
##        self.setText('')
##        if len(cmd):
##            self.history.append(cmd)
##            self.history_pos = 0
##        self.emit(QtCore.SIGNAL('sigNewCmd'), cmd)
##
##    def keyPressEvent(self, key):
##        '''History handling'''
##
##        QtGui.QLineEdit.keyPressEvent(self, key)
##        code = key.key()
##
##        if code == QtCore.Qt.Key_Up:
##            self.history_pos += 1
##        elif code == QtCore.Qt.Key_Down:
##            self.history_pos -= 1
##        else:
##            return
##            
##        self.history_pos = max(self.history_pos, 0)
##        self.history_pos = min(self.history_pos, len(self.history))
##        text = ''
##        if self.history_pos > 0:
##            text = self.history[-self.history_pos]
##        self.setText(text)

class Console(QtGui.QTextEdit):
    '''Custom QText Edit'''

    def __init__(self, *args):
    
        QtGui.QTextEdit.__init__(self, *args)
        
        self.clear()
        self.history = []
        self.history_index = 0
        self.cursor = QtGui.QTextCursor(self.textCursor())
        self.begin_pos = 0
        
##        self.setTextFormat(QtCore.Qt.PlainText)
##        self.setCurrentFont(QtGui.QFont('Courier'))
        
        prog = '/home/grossmj/Dynamips/dynamips-0.2.7-RC1-x86.bin'
        self.proc = QtCore.QProcess(self)
        QtCore.QObject.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self.slotNewOutput)
        
        self.proc.start(prog,  ['-P', '3600', '--idle-pc', '0x60575b54', '/home/grossmj/Dynamips/c3640.bin'])


    def slotNewCmd(self, cmd):
    
        print cmd
        cmd += "\r\n"
        self.proc.write(str(cmd))

    def slotNewOutput(self):
        
        #self.append(QtCore.QString(self.proc.readAllStandardOutput()))
        self.insertPlainText(QtCore.QString(self.proc.readAllStandardOutput()))
        self.cursor.movePosition(QtGui.QTextCursor.End)#, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(self.cursor)
        self.begin_pos = self.cursor.position()
        
    def  mousePressEvent(self, event):
    
        event.ignore()
    
    def mouseDoubleClickEvent(self, event):
    
        event.ignore()
    
    def keyPressEvent(self, event):

        key = event.key()
        if key == QtCore.Qt.Key_Up:
##            self.cursor.clearSelection()
##            self.cursor.setPosition(self.begin_pos, QtGui.QTextCursor.KeepAnchor)
##            self.cursor.clearSelection()
            self.proc.write("\x1bOA")
        elif key == QtCore.Qt.Key_Down:
##            self.cursor.clearSelection()
##            self.cursor.setPosition(self.begin_pos, QtGui.QTextCursor.KeepAnchor)
##            self.cursor.clearSelection()
            self.proc.write("\x1bOB")
        elif key == QtCore.Qt.Key_Right:
            self.cursor.setPosition(self.cursor.position() + 1)
            self.proc.write("\x1bOC")
        elif key == QtCore.Qt.Key_Left:
            self.cursor.setPosition(self.cursor.position() - 1)
            self.proc.write("\x1bOD")
        else:
            self.proc.write(str(event.text()))
            #QtGui.QTextEdit.keyPressEvent(self, event)
