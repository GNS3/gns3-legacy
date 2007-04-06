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
from Ui_Inspector import *

class MNode(QtSvg.QGraphicsSvgItem, QtGui.QGraphicsScene):
    '''MNode for QGraphicsScene'''
   
    id = None
    edgeList = []
      
    def __init__(self, svgfile, QGraphicsScene, xPos=None, yPos=None):
        
        QtSvg.QGraphicsSvgItem.__init__(self, svgfile)
        
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
        
    def move(self, xPos, yPos):
    
        self.setPos(xPos, yPos)

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
