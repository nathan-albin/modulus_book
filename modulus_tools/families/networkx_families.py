"""
Functor classes for various families of objects implemented
in NetworkX.
"""


import networkx as nx
import numpy as np

class ShortestConnectingPath:
    """
    Functor class for finding the shortest rho-length path between two sets of nodes.
    """

    # the dummy source and target node names
    src = '__source__'
    tgt = '__target__'
    
    def __init__(self, G, S, T):
                
        # remember the graph, source and target sets
        self.G = G
        self.S = S
        self.T = T
        
        # enumerate the edges so we can keep track of them
        # when processing a path
        for i, (u,v) in enumerate(G.edges()):
            G[u][v]['enum'] = i
        
        # make a copy of G to work on
        self.H = G.copy()
        
        # add dummy source and target nodes
        self.H.add_node(self.src)
        self.H.add_node(self.tgt)
        
        # link the dummy nodes
        for v in S:
            self.H.add_edge(self.src, v, rho=0)
        for v in T:
            self.H.add_edge(v, self.tgt, rho=0)
            
    def __call__(self, rho, tol):
        
        # assign rho to the graph edges
        for i, (u,v) in enumerate(self.G.edges()):
            self.H[u][v]['rho'] = rho[i]

        # find the shortest path
        p = nx.shortest_path(self.H, self.src, self.tgt, weight='rho')
        
        # the actual path omits the source and target dummy nodes
        p = p[1:-1]
        
        # form the row vector
        n = np.zeros(rho.shape)
        for i in range(len(p)-1):
            n[self.G[p[i]][p[i+1]]['enum']] = 1
            
        return p, n


class MinimumSpanningTree:
    """
    Functor class for finding the minimum rho-length spanning tree.
    """
    
    def __init__(self, G):
        
        # remember the graph
        self.G = G
        
        # enumerate the edges so we can keep track of them when
        # processing a spanning tree
        for i, (u,v) in enumerate(G.edges()):
            G[u][v]['enum'] = i
                
    def __call__(self, rho, tol):
        
        # assign rho to the graph edges
        for i, (u,v) in enumerate(self.G.edges()):
            self.G[u][v]['rho'] = rho[i]
            
        # find a minimum spanning tree
        T = list(nx.minimum_spanning_edges(self.G, weight='rho', data=False))
        
        # form the row vector
        n = np.zeros(rho.shape)
        for u,v in T:
            n[self.G[u][v]['enum']] = 1
            
        return T, n