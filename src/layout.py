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
#    by Jeremy Grossmann <jeremy.grossmann@gns3.net>

from math import pi,sin,cos,sqrt
import sys
try:
    import Numeric as N
except ImportError:
    raise

def circular_layout(G, radius = 1.0, dim=2):
    """
    Circular layout.

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
    """ Random layout."""
    import random
    vpos={}
    for v in G:
        vpos[v]=N.array([random.random() for i in range(dim)])
    return vpos        

def spring_layout(G, iterations=50, dim=2, node_pos=False):
    """Spring force model layout"""
#    from Numeric import array,dot,sum,sqrt
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
##                if G.has_edge(v,u):
                    deltaf=-delta*dn**2/(k*dn)
                    disp[v]=disp[v]+deltaf

        # update positions
        for v in G:
            l=max(sqrt(N.dot(disp[v],disp[v])),0.01)
            vpos[v]=vpos[v]+ disp[v]*t/l
        t-=dt
    return vpos
                   


##def uniform_sequence(n):
##    """
##    Return sample sequence of length n from a uniform distribution.
##    """
##    return [ random.uniform(0,n) for i in xrange(n)]

##def spectral_layout(G, dim=2, vpos=None, iterations=1000, eps=1.e-3):
##    """
##    Return the position vectors for drawing G using spectral layout.
##    """
##    # check silly cases
##    n=G.order()
##    if iterations==0 or n==0:
##        return vpos or {}
##    # create initial guesses for positions
##    if vpos is None:
##        # start with random positions
##        nodes=G.nodes()
##        uhat=[ ]
##        for p in range(dim):
##            rx=uniform_sequence(n)
##            uhat.append( dict( zip(nodes,rx) ) )
##    else:
##        # use given positions
##        uhat=[]
##        for p in range(dim):
##            rx=[(v,pos[p]) for (v,pos) in vpos.iteritems()]   
##            uhat.append( dict(rx) )
##    # Find lowest eigenvectors
##    vhat=graph_low_ev_pi(uhat,G,eps,iterations)
##    # form position dict
##    vpos={}
##    for n in nodes:
##        poslist=[ vhat[p].get(n,0) for p in range(dim) ]
##        vpos[n]=N.array( poslist )
##    return vpos
##
##def graph_low_ev_pi(uhat,G,eps=1.e-3,iterations=10000):
##    """ 
##    Power Iteration method to find smallest eigenvectors of Laplacian(G).
##    Note: constant eigenvector has eigenvalue=0 but is not included
##    in the count of smallest eigenvalues.
##
##    uhat -- list of p initial guesses (dicts) for the p eigenvectors.
##    G -- The Graph from which Laplacian is calculated.
##    eps -- tolerance for norm of change in eigenvalue estimate.
##    iterations -- maximum number of iterations to use.
##    """
##    # set up element value for constant eigenvector (squared)
##    constant=1.0/G.order()
##    # set up data for faster iteration
##    gg_data=_gershgorin_setup(G)
##    # 
##    v=[]  # setup v to hold eigenvectors
##    p=len(uhat)   # number of guesses is number of vectors to return 
##    for i in xrange(p):
##        vv=uhat[i]  # get initial guess
##        ##normalize(vv)
##        norm=sqrt(N.sum([vals**2 for vals in vv.itervalues()]))
##        nn=1.0/norm
##        for k in vv:
##            vv[k] *= nn
##        ##
##        v.append(vv)
##
##        difference=eps+1
##        iii=0
###        sys.stderr.write("drawing")
##        while difference>eps:
##            vhat=v[i]
##            ## Orthogonal to constant vector
##            dotprod=constant*sum(vhat.itervalues())
##            for (k,val) in vhat.iteritems():
##                vhat[k]-=dotprod
##            ## Orthogonal to other already found eigenvectors
##            for j in range(i):  
##                ##  vhat= vhat- <vhat,v[j]> * v[j]
##                s_d=sum([vhat.get(k,0)*val for (k,val) in v[j].iteritems()])
##                for (k,value) in v[j].iteritems():
##                    vhat[k]=vhat.get(k,0)-value*s_d
##                ##
##            vv=_graph_gershgorin_dot_v(gg_data,vhat)
##            ##normalize(vv)     vv=vv/|vv|
##            norm=sqrt(sum([vals**2 for vals in vv.itervalues()]))
##            if norm==0:
##                raise networkx.NetworkXError,"Eigenvector with zero eigenvalue given as input."
##            nn=1.0/norm
##            for k in vv:
##                vv[k] *= nn
##            ##
##            v[i]=vv
##            ##difference = |vhat-vv|
##            result=vhat.copy()
##            for (k,value) in vv.iteritems():
##                result[k]=result.get(k,0)-value
##            difference=sqrt(sum([vals**2 for vals in result.itervalues()]))
##            #print "difference on iteration %s is %s"%(iii,difference)
##            ##
##            iii += 1
##            if iii==iterations: 
##                #print "Maximum iterations achieved."
##                break
##                raise NetworkXError, "Maximum number of iterations exceeded." 
###            if iii%20==0: sys.stderr.write(".")
##    return v 
##    
##def _gershgorin_setup(G):
##    """
##    Return a list of matrix properties to be used 
##    to iteratively multiply B*v where v is a vector
##    and B=g*I-L and g is the Gershgorin estimate of 
##    the largest eigenvalue of L=Laplacian(G).
##
##    Used as input to graph_gershgorin_dot_v()
##    """
##    diag=G.degree(with_labels=True)
##    adj={}
##    g=max(diag.itervalues())
##    for (n,degree) in diag.iteritems():
##        diag[n]=g-degree
##        adj[n]=G.neighbors(n)
##    return [diag,adj]
##
##def _graph_gershgorin_dot_v(gg_data,v):
##    """
##    Returns B*v where B=g*I-L and g is the Gershgorin estimate of the 
##    largest eigenvalue of L.  (g=max( deg(n) + sum_u(\|w_(n,u)\|)
##
##    We use this to iterate and find the smallest eigenvectors of L.
##    """
##    (diag,adj)=gg_data
##    r={}
##    for (n,nbrs) in adj.iteritems():
##        rn=sum([ v.get(u,0) for u in nbrs ])
##        #rn=sum([ v.get(u,0)*w for (u,w) in nbrs.iteritems() ])#weighted adj matrix
##        r[n]=rn+v.get(n,0)*diag[n]
##    return r
##
##def _test_suite():
##    import doctest
##    suite = doctest.DocFileSuite('tests/layout.txt',package='networkx')
##    return suite
##
##if __name__ == "__main__":
##    import sys
##    import unittest
##    if sys.version_info[:2] < (2, 4):
##        print "Python version 2.4 or later required for tests (%d.%d detected)." %  sys.version_info[:2]
##        sys.exit(-1)
##    unittest.TextTestRunner().run(_test_suite())
##    
