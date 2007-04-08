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
import string

class Console(QtGui.QTextEdit):
    '''Custom QText Edit'''

    def __init__(self, *args):
    
        QtGui.QTextEdit.__init__(self, *args)
        
        self.clear()
        self.cursor = QtGui.QTextCursor(self.textCursor())
        self.write = None
        self.isConnected = False
        self.char_count = 0
        self.bell = False

        self.history_up_pressed = False
        self.history_down_pressed = False
        
    def filter(self, line_p):
       '''Remove non-printable characters'''

       self.bell = False
       line, i, imax = '', 0, len(line_p)
       while i < imax:
          ac = ord(line_p[i])
          # printable, \t, \n
          if ( 32 <= ac and ac < 127 ) or ac == 9 or ac == 10:       
             line = line + line_p[i]
          # remove coded sequences
          elif ac == 27:                                             
             i = i + 1
             while i < imax and string.lower( line_p[i] ) not in 'abcdhsujkm':
                i = i + 1
          # backspace or eol spacing
          elif ac == 7:
             self.bell = True
          elif ac == 8 or ( ac == 13 and line and line[-1] == ' ' ): 
             if line:
                line = line[:-1]
          i = i + 1
       return line

    def slotStandardOutput(self, output):
        
        output = self.filter(output)
        
        if self.history_up_pressed == True or self.history_down_pressed == True:
            print output
            print self.char_count
            if self.char_count > 0 and self.bell == False:
                self.cursor.setPosition(self.cursor.position() - self.char_count, QtGui.QTextCursor.KeepAnchor)
                self.cursor.removeSelectedText()
                self.cursor.clearSelection()
            self.char_count = len(output)
            self.history_up_pressed = False
            self.history_down_pressed = False

        self.insertPlainText(QtCore.QString(output))
        self.cursor.movePosition(QtGui.QTextCursor.End)
        self.setTextCursor(self.cursor)

    def backspace(self):
    
        if self.char_count > 0:
            self.cursor.setPosition(self.cursor.position() - 1, QtGui.QTextCursor.KeepAnchor)
            self.cursor.removeSelectedText()
            self.cursor.clearSelection()
            self.char_count -= 1
        
    def mousePressEvent(self, event):
    
        event.ignore()
    
    def mouseDoubleClickEvent(self, event):
    
        event.ignore()

    def keyPressEvent(self, event):

        '''
        Keystroke Effect for an IOS CLI

        Left and right arrow move the cursor left or right one
        character within the current line. => NOT FINISHED
        
        Up and down arrow display
        the previous or next lines from the command history buffer. => BUGS
        
        BACKSPACE Delete character before cursor
        DEL Same as backspace: delete character before cursor
        TAB Command completion
        ? Help

        Ctrl + A Move cursor to beginning of line (not implemented)
        Ctrl + B Back cursor up one character (not implemented)
        Ctrl + C
        Ctrl + D Delete the character the cursor is on (not implemented)
        Ctrl + E Move cursor to end of line (not implemented)
        Ctrl + G (not implemented)
        Ctrl + H Backspace (delete character before cursor) (not implemented)
        Ctrl + I Same as TAB
        Ctrl + J (not implemented)
        Ctrl + K Delete characters to end of line (characters go to cut buffer; see Ctrl + Y) (not implemented)
        Ctrl + L Redisplay line
        Ctrl + M (not implemented)
        Ctrl + N Bring up the next line from the command history buffer (not implemented)
        Ctrl + O (not implemented)
        Ctrl + P Bring up the previous line from the command history buffer (not implemented)
        Ctrl + Q (not implemented)
        Ctrl + R Retype line (useful when DEBUG output trashes the screen) (not implemented)
        Ctrl + S (not implemented)
        Ctrl + T Transpose characters (not implemented)
        Ctrl + U Delete characters to beginning of line (characters go to cut
        buffer; see Ctrl + Y) (not implemented)
        Ctrl + V Quoted insert (take the next character literally instead of
        as editor command, used to insert control character) (not implemented)
        Ctrl + W Delete previous word (not implemented)
        Ctrl + X Same as Ctrl + U: delete to beginning of line (characters go to cut buffer; see Ctrl + Y) (not implemented)
        Ctrl + Y Yank: restore cut characters from buffer after cursor (not implemented)
        Ctrl + Z (not implemented)
        Esc < Show first line from command history buffer (not implemented)
        Esc > Show last line from command history buffer (not implemented)
        Esc O Escape prefix sent by VT100 terminal prior to code for arrow key (not implemented)
        Esc Q Quoted insert (take the next character literally instead of
        as editor command, used to insert control character) (not implemented)
        Esc [ Escape prefix sent by VT100 terminal prior to code for arrow key (not implemented)
        Esc b Move cursor back one word (not implemented)
        Esc c Capitalize word after cursor (not implemented)
        Esc d Delete word (from cursor forward) (not implemented)
        Esc f Move cursor forward one word (not implemented)
        Esc i TAB (not implemented)
        Esc l Change word after cursor to lowercase (not implemented)
        Esc q Quoted insert (take the next character literally instead of
        as editor command, used to insert control character) (not implemented)
        Esc u Change word after cursor to uppercase (not implemented)
        Esc y Switch to previous cut buffer and yank (insert) it at cursor (not implemented)
        Esc DEL Delete word before cursor (not implemented)
        '''
    
        if self.isConnected == False:
            event.ignore()
            return
        assert(self.write != None)
        key = event.key()
        if key == QtCore.Qt.Key_Up:
            self.history_up_pressed = True
            self.write("\x1bOA")
        elif key == QtCore.Qt.Key_Down:
            self.history_down_pressed = True
            self.write("\x1bOB")
        elif key == QtCore.Qt.Key_Right:
            print 'right'
            #self.cursor.setPosition(self.cursor.position() + 1)
##            self.cursor.movePosition(QtGui.QTextCursor.Right)
##            self.setTextCursor(self.cursor)
            self.write("\x1bOC")
        elif key == QtCore.Qt.Key_Left:
            print 'left'
            #self.cursor.setPosition(self.cursor.position() - 1)
##            self.cursor.movePosition(QtGui.QTextCursor.Left)
##            self.setTextCursor(self.cursor)
            self.write("\x1bOD")
        elif key == QtCore.Qt.Key_Backspace or key == QtCore.Qt.Key_Delete:
            self.write(str(event.text()))
            self.backspace()
        else:
            if key == QtCore.Qt.Key_Return or (event.modifiers() == QtCore.Qt.ControlModifier and key == QtCore.Qt.Key_Z):
                self.char_count = 0
            elif (32 <= key and key < 127) and event.modifiers() == QtCore.Qt.NoModifier:
                if self.char_count > 0 and self.cursor.position() < self.char_count:
                    print 'insert'
##                    self.cursor.clearSelection()
##                    self.cursor.movePosition(self.cursor.position(), QtGui.QTextCursor.KeepAnchor)
                    self.cursor.insertText(str(event.text()))
                self.char_count += 1
            self.write(str(event.text()))
