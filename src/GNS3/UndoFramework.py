# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
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
# code@gns3.net
#

from PyQt4 import QtGui

class UndoView(QtGui.QUndoView):

    def __init__(self, parent=None):
    
        QtGui.QUndoView.__init__(self, parent)

class AddItem(QtGui.QUndoCommand):
    
    def __init__(self, topology, item, text):

        QtGui.QUndoCommand.__init__(self)
        self.setText(text)
        self.topology = topology
        self.item = item

    def redo(self):

        if self.topology.addNode(self.item, fromScene=True) == False:
            self.undo()

    def undo(self):

        self.topology.deleteNode(self.item.id)
        self.item.__del__() 
        
class DeleteItem(QtGui.QUndoCommand):
    
    def __init__(self, topology, item, text):

        QtGui.QUndoCommand.__init__(self)
        self.setText(text)
        self.topology = topology
        self.item = item

    def redo(self):

        self.topology.deleteNode(self.item.id)
        self.item.__del__() 

    def undo(self):

        self.topology.addNode(self.item)

class AddLink(QtGui.QUndoCommand):
    
    def __init__(self, topology, srcid, srcif, dstid, dstif):

        QtGui.QUndoCommand.__init__(self)
        self.setText("New Link")
        self.topology = topology
        self.status = None
        self.link = None
        self.srcid = srcid
        self.srcif = srcif
        self.dstid = dstid
        self.dstif = dstif
        
    def redo(self):

        if self.link:
            self.status = self.topology.addLink(self.link.source.id, self.link.srcIf, self.link.dest.id, self.link.destIf, draw=False)
            self.topology.links.add(self.link)
            self.topology.addItem(self.link)
        else:
            self.status = self.topology.addLink(self.srcid, self.srcif, self.dstid, self.dstif)
            self.link = self.topology.lastAddedLink

    def undo(self):

        if self.status:
            if self.link in self.topology.links:
                self.topology.deleteLink(self.link)
                for link in self.topology.links:
                    link.adjust()

    def getStatus(self):
    
        return self.status
        
class DeleteLink(QtGui.QUndoCommand):
    
    def __init__(self, topology, link):

        QtGui.QUndoCommand.__init__(self)
        self.setText("Delete Link")
        self.topology = topology
        self.link = link
        
    def redo(self):

        if self.link in self.topology.links:
            self.status = self.topology.deleteLink(self.link)
            for link in self.topology.links:
                link.adjust()

    def undo(self):

        self.topology.addLink(self.link.source.id, self.link.srcIf, self.link.dest.id, self.link.destIf, draw=False)
        self.topology.links.add(self.link)
        self.topology.addItem(self.link)

class AddConfig(QtGui.QUndoCommand):
    
    def __init__(self, node, config, prevConfig):

        QtGui.QUndoCommand.__init__(self)
        self.setText("New configuration applied on %s" % node.hostname)
        self.node = node
        self.config = config
        self.previousConfig = prevConfig

    def redo(self):

        self.node.set_config(self.config)

    def undo(self):

        self.node.set_config(self.previousConfig)

