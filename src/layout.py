#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright (C) 2004,2005 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html
#
#    Imported from NetworkX (https://networkx.lanl.gov) and modified for gns-3 
#    Contact: developers@gns3.net
#

from math import pi,sin,cos,sqrt
import sys
try:
    import Numeric as N
except ImportError:
    pass

def circular_layout(G, radius = 1.0, dim=2):
    """ Circular layout
        Crude version that doesn't try to minimize edge crossings.
    """
    vpos={}
    r=radius  # radius of circle
    t=0
    dt=2.0*pi/len(G)
    # should test for dim < 2 here
    for v in G:
        p=dim*[0.0]
        p[0]=r*cos(t)
        p[1]=r*sin(t)
        vpos[v]=N.array(p)
        t=t+dt
    return vpos        

def random_layout(G, dim=2):
    """ Random layout
    """
    import random
    vpos={}
    for v in G:
        vpos[v]=N.array([random.random() for i in range(dim)])
    return vpos        

def spring_layout(G, iterations=50, dim=2, node_pos=False):
    """ Spring force model layout
    """
    
    #  from Numeric import array,dot,sum,sqrt
    if not node_pos:
        # set the initial positions randomly in 1x1 box
        vpos=random_layout(G, dim=dim) 
    else:
        vpos=node_pos
    if iterations==0:
        return vpos
    if len(G)==0:
        k=1.0
    else:
        k=N.sqrt(1.0/len(G)) # optimal distance between nodes
    disp={}         # displacements

    # initial "temperature" (about .1 of domain area)
    # this is the largest step allowed in the dynamics
    # linearly step down by dt on each iteration so
    # on last iteration it is size dt.
    t=0.1
    dt=0.1/float(iterations+1)
    for i in range(0,iterations):
        for v in G:
            disp[v]=N.zeros(dim)
            for u in G:
                delta=vpos[v]-vpos[u]
                dn=max(sqrt(N.dot(delta,delta)),0.01)
                # repulsive force between all
                deltaf=delta*k**2/dn**2
                disp[v]=disp[v]+deltaf
                # attractive force between neighbors
                if G[v].hasEdgeToNode(u):
                    deltaf=-delta*dn**2/(k*dn)
                    disp[v]=disp[v]+deltaf

        # update positions
        for v in G:
            l=max(sqrt(N.dot(disp[v],disp[v])),0.01)
            vpos[v]=vpos[v]+ disp[v]*t/l
        t-=dt
    return vpos
