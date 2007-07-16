#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
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
# Contact: contact@gns3.net
#

from GNS3.Globals import Mode

class Workspace:

    def __init__(self, mainWindow, projType=None, projFile=None):
        self.mainWindow = mainWindow
        self.projectType = projType 
        self.projectFile = projFile
        self.__states = {
            'design_mode': {
                'nodesDock': True,
            },
            'emulation_mode': {
                'summaryDock': True,
            },
            'simulation_mode': {
                'eventDock': True,
            }
        }

        self.loadProject(projFile)

        self.currentMode = None
        self.switchToMode(Mode.Design)

    def loadProject(self, projectFile):
        if projectFile is None:
            self.mainWindow.setWindowTitle("GNS3 - New Project")

    def saveProject(self, projectFile):
        pass

    def switchToMode(self, mode):
        modeFunction = {
            Mode.Design: self.switchToMode_Design,
            Mode.Emulation: self.switchToMode_Emulation,
            Mode.Simulation: self.switchToMode_Simulation
        }[mode]()
       
    def switchToMode_Design(self):
        print ">>> switchToMode: DESIGN"
        pass

    def switchToMode_Emulation(self):
        print ">>> switchToMode: EMULATION"
        pass

    def switchToMode_Simulation(self):
        print ">>> switchToMode: SIMULATION"
        pass

