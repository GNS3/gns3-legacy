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

import sys
from PyQt4 import QtCore, QtGui, QtSvg
from Ui_MainWindow import *
from Ui_Inspector import *
from NamFileSimulation import *
import layout
import svg_resources_rc
        
# emplacement temporaire de Edge pour les tests
class Edge(QtGui.QGraphicsLineItem):
    '''Edge for QGraphicsScene'''

    def __init__(self, sourceNode, destNode):
    
        QtGui.QGraphicsLineItem.__init__(self)
        #self.setFlag(self.ItemIsMovable)
        self.statussource = QtGui.QGraphicsEllipseItem(self)
        self.statusdest = QtGui.QGraphicsEllipseItem(self)
        #self.setZValue(2)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

    def adjust(self):

        # Line style
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)
        self.setPen(pen) 
        
        #TODO: Correct the bug when you throw the node

        rectsource = self.source.boundingRect()
        topmiddle = rectsource.topRight() / 2
        leftmiddle = rectsource.bottomLeft() / 2
        sourcecenter = QtCore.QPointF(topmiddle.x(), leftmiddle.y())

        rectdest= self.dest.boundingRect()
        topmiddle = rectdest.topRight() / 2
        leftmiddle = rectdest.bottomLeft() / 2
        destcenter = QtCore.QPointF(topmiddle.x(), leftmiddle.y())

        line = QtCore.QLineF(self.source.mapToScene(sourcecenter), self.dest.mapToScene(destcenter))        
        self.setLine(line)
        self.adjustStatusPoints(line)
        
    def adjustStatusPoints(self, line):
        
        #TODO: Finish to put a status point on the link
        pen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)
        self.statusdest.setPen(pen)
        self.statusdest.setBrush(QtGui.QBrush(QtCore.Qt.red))

##            self.statusdest.setRect(line.p2().x() - (line.dx() /  2), line.p2().y() - (line.dy() / 2), 10, 10)   
##    
##            test = line.pointAt(0.50)
##            self.statusdest.setRect(test.x() , test.y() , 10, 10)
    
# emplacement temporaire de Node pour les tests
class Node(QtSvg.QGraphicsSvgItem):
    '''Node for QGraphicsScene'''
   
    id = None
    edgeList = []
    
    def __init__(self, svgfile):
        
        QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)
        self.setZValue(1)

    def addEdge(self, edge):
    
        self.edgeList.append(edge)
        edge.adjust()
    
    def ajustAllEdges(self):
    
        for edge in self.edgeList:
            edge.adjust()
            
    def hasEdgeToNode(self, node_id):
    
        for edge in self.edgeList:
            if edge.dest.id == node_id:
                return 1
        return 0
        
    def itemChange(self, change, value):
    
        if change == self.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()
        return QtGui.QGraphicsItem.itemChange(self, change, value)
        
    def mouseDoubleClickEvent(self, event):
    
        inspector = QtGui.QDialog()
        ui = Ui_FormInspector()
        ui.setupUi(inspector)
        inspector.show()
        inspector.exec_()
        
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
        self.scene.setSceneRect(-500, -500, 1000, 1000)
        self.graphicsView.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graphicsView.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        # Example of use
        node1 = Node(":Switch")
        node2 = Node(":Route switch processor")
        node3 = Node(":Multilayer switch")
        node4 = Node(":Router firewall")
        node5 = Node(":Router")

##        text = QtGui.QGraphicsTextItem("10.10.1.45")
##        text.setFlag(text.ItemIsMovable)
##        text.setZValue(2)
##        self.scene.addItem(text)

        self.scene.addItem(node1)
        self.scene.addItem(node2)
        self.scene.addItem(node3)
        self.scene.addItem(node4)
        self.scene.addItem(node5)

        node1.setPos(0, 0)
        node2.setPos(150, 150)
        node3.setPos(-100, 150)
        node4.setPos(150, -150)
        node5.setPos(-150, -150)
        self.scene.addItem(Edge(node1, node2))
        self.scene.addItem(Edge(node2, node3))
        self.scene.addItem(Edge(node3, node1))
        self.scene.addItem(Edge(node1, node4))
        self.scene.addItem(Edge(node1, node5))
        # End of example


        # background test
        #background = QtGui.QBrush(QtGui.QPixmap("worldmap2.jpg"))
        #self.graphicsView.setBackgroundBrush(background)
        #self.graphicsView.scale(0.8, 0.8)

    def SaveToFile(self):
    
        filedialog = QtGui.QFileDialog(self)
        selected = QtCore.QString()
        exports = 'PNG File (*.png);;JPG File (*.jpeg *.jpg);;BMP File (*.bmp);;XPM File (*.xpm *.xbm)'
        path = QtGui.QFileDialog.getSaveFileName(filedialog, 'Export', '.', exports, selected)
        if not path:
            return
        path = unicode(path)
        if str(selected) == 'PNG File (*.png)' and path[-4:] != '.png':
            path = path + '.png'
        if str(selected) == 'JPG File (*.jpeg *.jpg)' and (path[-4:] != '.jpg' or  path[-5:] != '.jpeg'):
            path = path + '.jpeg'
        if str(selected) == 'BMP File (*.bmp)' and path[-4:] != '.bmp':
            path = path + '.bmp'
        if str(selected) == 'BMP File (*.bmp)' and (path[-4:] != '.xpm' or path[-4:] != '.xbm'):
            path = path + '.xpm'
        try:
            self.Export(path, str(str(selected)[:3]))
        except IOError, (errno, strerror):
            QtGui.QMessageBox.critical(self, 'Open',  u'Open: ' + strerror)
        
    def Export(self, name, format):
    
        rect = self.graphicsView.viewport().rect()
        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        #FIXME: We should set a white background on the scene, not on the pixmap
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #self.scene.render(painter)
        self.graphicsView.render(painter)
        painter.end()
        print pixmap.save(name, format)
        
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
                new_node = Node(":Router")
                new_node.id = event['id']
                nodes[new_node.id] = new_node
                self.scene.addItem(new_node)
                new_node.setPos(-100, -(new_node.id * 50))
            if event['type'] == 'link':
                self.scene.addItem(Edge(nodes[event['src']], nodes[event['dst']]))

        # test of a simple layout algorithm
        #pos = layout.circular_layout(nodes, 200)
        pos = layout.spring_layout(nodes)
        for id in pos:
            nodes[id].setPos(pos[id][0] * 1500, pos[id][1] * 1500) 
            nodes[id].ajustAllEdges()
