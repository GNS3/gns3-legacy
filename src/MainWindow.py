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
# Author: Jeremy Grossmann <jeremy.grossmann@gns3.net>
#

import sys
from PyQt4 import QtCore, QtGui, QtSvg
from Ui_MainWindow import *
from NamFileSimulation import *

# emplacement temporaire de Edge pour les tests
class Edge(QtGui.QGraphicsLineItem):
    '''Edge for QGraphicsScene'''

    def __init__(self, sourceNode, destNode):
    
        QtGui.QGraphicsLineItem.__init__(self)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

    def adjust(self):

        #TODO: A better links management
        line = QtCore.QLineF(self.mapFromItem(self.source, 30, 25), self.mapFromItem(self.dest, 30, 25))
        length = line.length()
        edgeoffset = QtCore.QPointF((line.dx() * 5) / length, (line.dy() * 5) / length)
        self.prepareGeometryChange()
        self.sourcepoint = line.p1() + edgeoffset
        self.destpoint = line.p2() - edgeoffset
        line = QtCore.QLineF(self.sourcepoint, self.destpoint)
        self.setLine(line)

# emplacement temporaire de Node pour les tests
class Node(QtSvg.QGraphicsSvgItem):
    '''Node for QGraphicsScene'''
   
    id = None
    edgeList = []
    
    def __init__(self, svgfile):
        
        QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setZValue(1)

    def addEdge(self, edge):
    
        self.edgeList.append(edge)
        edge.adjust()
        
    def itemChange(self, change, value):
    
        if change == self.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    ''' Main window '''
    
    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.createScene()
    
    def createScene(self):
    
        self.scene = QtGui.QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #TODO: A better management of the scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        
        # Example of use
        node1 = Node("router.svg")
        node2 = Node("router.svg")
        node3 = Node("router.svg")
        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)
        node1.setPos(0, 0)
        node2.setPos(150, 150)
        node3.setPos(0, 150)
        self.scene.addItem(Edge(node1, node2))
        self.scene.addItem(Edge(node2, node3))
        self.scene.addItem(Edge(node3, node1))
        # End of example


        # background test
        #background = QtGui.QBrush(QtGui.QPixmap("worldmap2.jpg"))
        #self.graphicsView.setBackgroundBrush(background)
        #self.graphicsView.scale(0.8, 0.8)

    def OpenNewFile(self):
        
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        path = QtGui.QFileDialog.getOpenFileName(filedialog, 'Choose a File', '.', \
                    'NAM File (*.nam)', selected)
        if not path:
            return
        path = unicode(path)
        try:
            if str(selected) == 'NAM File (*.nam)':
                self.NamSimulation(path)
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
            
    def NamSimulation(self, path):
        
        # Temporary example
        nam = NamFileSimulation(path)
        nodes = {}
        while (1):
            event = nam.next()
            if (event == None):
                break
            if (event == {}):
                continue
            if event['type'] == 'node':
                new_node = Node("router.svg")
                new_node.id = event['id']
                nodes[new_node.id] = new_node
                self.scene.addItem(new_node)
                new_node.setPos(-100, -(new_node.id * 50))
            if event['type'] == 'link':
                self.scene.addItem(Edge(nodes[event['src']], nodes[event['dst']]))
