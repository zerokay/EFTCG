#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:21:13 2019

@author: kay
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

Matrix = np.array([
        [1, 1, 1, 1, 1, 1, 0, 0],  # a
        [0, 1, 1, 0, 1, 0, 0, 0],  # b
        [0, 0, 1, 1, 0, 0, 0, 0],  # c
        [0, 0, 0, 1, 1, 0, 0, 0],  # d
        [0, 0, 0, 0, 1, 1, 0, 0],  # e
        [0, 0, 1, 0, 0, 1, 1, 1],  # f
        [0, 0, 0, 0, 0, 1, 1, 1],  # g
        [0, 0, 0, 0, 0, 1, 1, 1]]) # h

Matrix = np.array([
        [0,0,0],
        [0,0,0],
        [0,0,0]])


def min_hop(MG):
    n = len(MG)
    G = nx.Graph()
    G.add_nodes_from(list(range(n)))
    for i in range(n):
        for j in range(n):
            if MG[i][j]:
                G.add_edge(i, j)
    #####################################
    r = nx.shortest_path(G, target=n-1)    
    return r

def has_path(MG, s, t):
    n = len(MG)
    G = nx.Graph()
    G.add_nodes_from(list(range(n)))
    for i in range(n):
        for j in range(n):
            if MG[i][j]:
                G.add_edge(i, j)
    #####################################
    r = nx.has_path(G, s, t) 
#    nx.draw(G,with_labels=True)
#    plt.show()
    return r
if __name__ == "__main__":
    r = has_path(Matrix, 0, 1)
    print(r)
    
#def min_hop(MG, Nodes=None,flag=False):
#    n = len(MG)
#    G = nx.Graph()
#    for i in range(n):
#        for j in range(n):
#            if MG[i][j]:
#                G.add_edge(i, j) # weight=2/(Nodes[i].energy_residual + Nodes[j].energy_residual))
##    nx.draw(G,with_labels=True)
##    plt.show()
#    if flag:
#        r = nx.shortest_path(G, target=n-1, weight="weight")
#    else:
#        r = nx.shortest_path(G, target=n-1)
##    r = nx.dijkstra_path(G, target=n-1)    
##    print(r)
#    return r
