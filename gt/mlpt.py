#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:01:37 2018

@author: kay
"""

import graph
import copy
from simulator import Simulator
from node import Node

def mlpt():
    ''' Multi-power Topology Contorl Algorithm '''
    
    G_mlpt = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes)
     
    ##############################################################
    M = 0
    H = graph.flow(G_mlpt, Node.n)
    for i in range(Node.n):
        nei = nodes[i].double_neighbor
        n = [x[0] for x in nei]  # id of beighbor of node-i 
        d = [x[1] for x in nei]
        tempM = 0
        e = [None] * len(d)
        for j in range(len(d)):
            e[j] = H[i][ n[j] ] * Simulator.dis_to_power(d[j])
            tempM += e[j]           
        V = []
        for k in range(len(d)):
            V.append([ n[k], d[k], e[k] ])
        nodes[i].neighbor= V
        nodes[i].neighbor.sort(key=lambda x:x[2],reverse=True)
        
        if tempM > M:
            M = tempM      
    ################################################################        
    flag = True  # is the power of node (game theory result) the NE?
    cnt = 0      # number of games
    while flag:
        flag = False
        cnt += 1
        for i in range(Node.n):  # N->0
            (u, G_mlpt) = mlpt_utility(i, nodes, G_mlpt, M)
            if u != nodes[i].power:
                flag = True
                nodes[i].power = u                         
    print("Number of iterations of MLPT:", cnt)
#    print(nodes[0].neighbor)
#    print(nodes[0].power)  
#    print(nodes[1].power) 
#    print(nodes[Node.n-1].power) 
    return G_mlpt, nodes


def mlpt_utility(cid, nodes, G_mlpt, M):  # cid:current id
    '''return No.i node optimal power and the index'''
    nei = nodes[cid].neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j
    E = [x[2] for x in nei]  # energy by link
    
    utility_max = 0  
#    index = 0
    for i in range(len(E)):
        MG = copy.deepcopy(G_mlpt)
        if i != 0:
            MG[cid][ n[i-1] ] = 0
            MG[n[i-1]][ cid ] = 0 
        e = 0
        for j in range(len(E)):
            if MG[cid][ n[j] ] == 1:
                e += E[j]
        k = graph.Connect(MG, Node.n, cid)
        u = M * k - e
        
        if k > 0 and u > utility_max:
            utility_max = u
            G_mlpt = MG
#            index = i # maybe disconnect, so cannot use index
    ##################################################
    # Determine power
    ##################################################
#    power = d[index]
    power = 0
#    print("++++++++++++++++++++++++++++++++++++++++++++")
    for i in range(len(d)):
        if G_mlpt[cid][ n[i] ] == 1 and d[i] > power:
            power = d[i]
    return power, G_mlpt