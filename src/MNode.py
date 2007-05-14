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

from PyQt4 import QtCore, QtGui, QtSvg
from Edge import *
from Inspector import Inspector
import Dynamips_lib as lib
import telnetlib
import socket
import sys
import __main__



class MNode(QtSvg.QGraphicsSvgItem, QtGui.QGraphicsScene):
    '''MNode for QGraphicsScene'''

    # Get access to globals
    main = __main__
    id = None
    edgeList = []
    mNodeName = None
    InspectorInstance = None
    svg = None
    _QGraphicsScene = None
        
    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        
        svg = QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        self.edgeList = []
        self.iosConfig = {}

        
        self.neighborList = []
        self.__telnet = telnetlib.Telnet()
        self.console_host = None
        self.console_port = None
        self.ios = None


        # Create an ID
        self.id = self.main.baseid
        self.main.baseid += 1
        
        # Record the object
        print id(self)
        self.main.nodes[self.id] = self
        
        # MNode settings
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setZValue(1)
        
        # By default put the node to (0,0)
        if xPos is None : xPos = 0
        if yPos is None : yPos = 0 
        self.setPos(xPos, yPos)
        
        # MNode placement
        
        print type(self)
        self.setData(0, QtCore.QVariant(self.id))
        self._QGraphicsScene = QGraphicsScene
        self._QGraphicsScene.addItem(self)
        self._QGraphicsScene.update(self.sceneBoundingRect())
        
        self.InspectorInstance = Inspector()
        self.InspectorInstance.loadNodeInfos(self.id)

        #FIXME: don't need this later
#        if self.main.hypervisor != None:
#            self.configIOS()
        
    def move(self, xPos, yPos):
    
        self.setPos(xPos, yPos)

    def addEdge(self, edge):
    
        if edge.dest.id != self.id:
            self.neighborList.append(edge.dest.id)
        else:
            self.neighborList.append(edge.source.id)
        self.edgeList.append(edge)
        edge.adjust()
    
    def ajustAllEdges(self):
    
        for edge in self.edgeList:
            edge.adjust()
            
    def hasEdgeToNode(self, node_id):
    
        for edge in self.edgeList:
            if edge.dest.id == node_id or edge.source.id == node_id:
                return True
        return False
        
    def itemChange(self, change, value):
    
        if change == self.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
    def mouseDoubleClickEvent(self, event):

        if (event.button() == QtCore.Qt.LeftButton):
            self.InspectorInstance.loadNodeInfos(self.id) 
            self.InspectorInstance.show()
        
    def mousePressEvent(self, event):
        
        if (event.button() == QtCore.Qt.RightButton) and self.main.conception_mode == False:
            self.menu = QtGui.QMenu()
            self.menu.addAction('telnet')
            self.menu.addAction('start')
            self.menu.addAction('stop')
            self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.simAction) 
            self.menu.exec_(QtGui.QCursor.pos())
#        self.menu = QtGui.QMenu()
#        self.menu.addAction('f0/0')
#        self.menu.connect(self.menu, QtCore.SIGNAL("triggered(QAction *)"), self.selectedInterface) 
#        self.menu.exec_(QtGui.QCursor.pos())
        QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
#        
#    def selectedInterface(self, action):
#        
#        print action.text()

    def simAction(self, action):
        
        action = action.text()
        if action == 'start':
            self.startIOS()
        elif action == 'stop':
            self.stopIOS()

    def setName(self, name):
        self.mNodeName = name
    
    def getName(self):

        print self.mNodeName;
        return self.mNodeName

    def getIdSvg(self):
        
        #return id(self.svg)
        return self.id                   
################### IOS stuff ###############################
    
    def configIOS(self):

        self.InspectorInstance.comboBoxIOS.addItems(self.main.ios_images.keys())
        self.InspectorInstance.saveIOSConfig()

        print 'Set IOS config for node ' + str(self.id)
        if self.main.hypervisor == None:
            sys.stderr.write("No hypervisor !\n")
            return
        self.ios = lib.C3600(self.main.hypervisor, chassis = '3640', name = 'R' + str(self.id))

        if self.iosConfig['iosimage'] == '':
            sys.stderr.write("Node " + str(self.id) + ": no selected IOS image\n")
            self.ios.delete()
            return
        
        print self.iosConfig['iosimage']
        self.ios.image = self.iosConfig['iosimage']

        if self.iosConfig['startup-config'] != '':
            self.ios.cnfg = self.iosConfig['startup-config']
   
        self.ios.ram = self.iosConfig['RAM']
        self.ios.rom = self.iosConfig['ROM']
        self.ios.nvram = self.iosConfig['NVRAM']
        if self.iosConfig['pcmcia-disk0'] != 0:
            self.ios.disk0 = self.iosConfig['pcmcia-disk0']
        if self.iosConfig['pcmcia-disk1'] != 0:
            self.ios.disk1 = self.iosConfig['pcmcia-disk1']
        
        self.ios.mmap = self.iosConfig['mmap']
        if self.iosConfig['confreg'] != '':
            self.ios.conf = self.iosConfig['confreg']

        self.ios.exec_area = self.iosConfig['execarea']
        
        # Only for 3600 platform
        #self.iosConfig['iomem']

        self.configSlot(0, self.iosConfig['slot0'])
        self.configSlot(1, self.iosConfig['slot1'])
        self.configSlot(2, self.iosConfig['slot2'])
        self.configSlot(3, self.iosConfig['slot3'])
        self.configSlot(4, self.iosConfig['slot4'])
        self.configSlot(5, self.iosConfig['slot5'])
        self.configSlot(6, self.iosConfig['slot6'])

        self.ios.idlepc = '0x60483ae4'
        
    def configSlot(self, nb, module):
        
        if (module == ''):
            return
        elif (module == 'NM-1E'):
            self.ios.slot[nb] = lib.NM_1E(self.ios, nb)
        elif (module == 'NM-4E'):
            self.ios.slot[nb] = lib.NM_4E(self.ios, nb)
        elif (module == 'NM-1FE-TX'):
            self.ios.slot[nb] = lib.NM_1FE_TX(self.ios, nb)
        elif (module == 'NM-4T'):
            self.ios.slot[nb] = lib.NM_4T(self.ios, nb)
      
    def startIOS(self):
        
        # localport, remoteserver, remoteadapter, remoteport
        # self.ios.slot[0].connect(0, self.main.hypervisor, esw.slot[1], 0)

        for neighbor in self.neighborList:
            node = self.main.nodes[neighbor]
            if node.ios != None:
                try:
                    if self.ios.slot[0] != None and self.ios.slot[0].connected(0) == False:
                        self.ios.slot[0].connect(0, self.main.hypervisor, node.ios.slot[0], 0)
                except lib.DynamipsError, msg:
                    print msg

        print self.ios.start()
        
    def stopIOS(self):
    
        if self.ios != None:
            print self.ios.stop()
        
    def resetIOSConfig(self):
    
        if self.ios != None:
            self.ios.delete()
    
    def __settelnet(self, telnet):
        """ Set telnet object
            telnet: telnet object
        """

        self.__console = console
    
    def __gettelnet(self):
        """ Returns telnet object
        """
        return self.__telnet
        
    telnet = property(__gettelnet, __settelnet, doc = 'The telnet connection')
    
    def connect(self):

        try:
            self.__telnet.open('localhost', self.ios.console)
        except socket.error, (value, msg):
            return False
        self.console_host = 'localhost'
        self.console_port = self.ios.console
        return True
        
    def disconnect(self):

        self.__telnet.close()
        self.console_host = None
        self.console_port = None
        
    def isConnected(self):
    
        if self.console_host and self.console_port:
            return True
        return False
    
    def mousePressEvent(self, event):
       '''We recover all items of the QGraphicsView'''
       global countClick
       global TabLinkMNode
       
       print "------------------- START -----------------------"    
       
       print "countClick", self.main.countClick  
#       ''' Callback of original QGraphicsView object. So we can move the MNode on the scene'''
       if (self.main.countClick == 0):
           self.main.countClick = self.main.countClick + 1
           self.main.TabLinkMNode.append(self)
       elif (self.main.countClick == 1 and self.main.linkEnabled == True):
           self.main.TabLinkMNode.append(self)
           self.main.countClick = 0
           ed = Edge(self.main.TabLinkMNode[0], self.main.TabLinkMNode[1], self._QGraphicsScene)
           self.main.TabLinkMNode= []
           self._QGraphicsScene.update(ed.boundingRect())
       QtSvg.QGraphicsSvgItem.mousePressEvent(self, event)
       print "------------------- STOP -----------------------"
