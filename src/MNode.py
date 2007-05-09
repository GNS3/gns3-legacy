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
from Inspector import Inspector
import Dynamips_lib as lib
import telnetlib
import socket
import __main__

class MNode(QtSvg.QGraphicsSvgItem, QtGui.QGraphicsScene):
    '''MNode for QGraphicsScene'''

    # Get access to globals
    id = None
    edgeList = []
    mNodeName = None
    InspectorInstance = None
    svg = None
    main = __main__
        
    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        
        QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
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
        QGraphicsScene.addItem(self)
        QGraphicsScene.update(self.sceneBoundingRect())
        
        self.InspectorInstance = Inspector()
        self.InspectorInstance.loadNodeInfos(self.id) 

        if self.main.hypervisor != None:
            self.configIOS()
        
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
        
        self.InspectorInstance.loadNodeInfos(self.id) 
        self.InspectorInstance.show()
                           
################### IOS stuff ###############################
    
    def configIOS(self):

        self.ios = lib.C3600(self.main.hypervisor, chassis = '3640', name = 'R' + str(self.id))
        self.ios.image = '/home/grossmj/c3640.bin'
        self.ios.slot[0] = lib.NM_1FE_TX(self.ios,0)
        self.ios.idlepc = '0x60575b54'
        
    def startIOS(self):
        
        # localport, remoteserver, remoteadapter, remoteport
        # self.ios.slot[0].connect(0, self.main.hypervisor, esw.slot[1], 0)
        #self.configIOS()
        
        for neighbor in self.neighborList:
            node = self.main.nodes[neighbor]
            if node.ios != None:
                try:
                    self.ios.slot[0].connect(0, self.main.hypervisor, node.ios.slot[0], 0)
                    node.ios.slot[0].connect(0, self.main.hypervisor, self.ios.slot[0], 0)
                except lib.DynamipsError, msg:
                    print msg

        print self.ios.start()
        
    def stopIOS(self):
    
        print self.ios.stop()
        self.ios.delete()
        self.ios = None
    
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

    def setName(self, name):
        self.mNodeName = name
    
    def getName(self):
        print self.mNodeName;
        return self.mNodeName
    
    def getIdSvg(self):
        return id(self.svg)
