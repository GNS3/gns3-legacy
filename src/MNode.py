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
        self.setData(0, QtCore.QVariant(self.id))
        QGraphicsScene.addItem(self)
        QGraphicsScene.update(self.sceneBoundingRect())
        
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
        
        self.InspectorInstance.loadNodeInfos(self.id) 
        self.InspectorInstance.show()

    def setName(self, name):
        self.mNodeName = name
    
    def getName(self):

        print self.mNodeName;
        return self.mNodeName

    def getIdSvg(self):
        
        return id(self.svg)
                           
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
        
        #TODO: slots/adapters
        self.ios.slot[0] = lib.NM_1FE_TX(self.ios, 0)
 
        self.ios.idlepc = '0x60483ae4'
      
    def startIOS(self):
        
        # localport, remoteserver, remoteadapter, remoteport
        # self.ios.slot[0].connect(0, self.main.hypervisor, esw.slot[1], 0)

        for neighbor in self.neighborList:
            node = self.main.nodes[neighbor]
            if node.ios != None:
                try:
                    self.ios.slot[0].connect(0, self.main.hypervisor, node.ios.slot[0], 0)
                except lib.DynamipsError, msg:
                    print msg

        print self.ios.start()
        
    def stopIOS(self):
    
        print self.ios.stop()
    
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
