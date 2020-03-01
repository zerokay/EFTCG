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

def deba():
    ''' Distributed Energy Balance Algorithm-DEBA Topology Contorl '''
    
    G_deba = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes)
    
    ############################################################
    # better response
    ############################################################
    m = 0
    for i in range(Node.n):
        nei = nodes[i].neighbor
        n = [x[0] for x in nei]  # Neighbor Node id
        d = [x[1] for x in nei]  # the distance of i and j
        if len(d) > m:
            m = len(d)-1
#    print("MAX:", m)
    ############################################################        
    cnt = 0
    while True:
        if cnt > m: break
        for i in range(Node.n-1):
            u = deba_utility(nodes, i, G_deba, cnt)
            if u != nodes[i].power:
                nodes[i].power = u
                nei = nodes[i].neighbor
                n = [x[0] for x in nei]  # Neighbor Node id
                d = [x[1] for x in nei]  # the distance of i and j
                for j in range(len(d)):
                    if d[j] > u:
                        G_deba[i][ n[j] ] = 0
                        G_deba[ n[j] ][i] = 0
        cnt += 1
#    print("NE:", flag)                    
    print("Number of iterations of DEBA:", cnt)
#    print(nodes[Node.n-1].power)
    return G_deba, nodes


def deba_utility(nodes, cid, G_deba, cnt):  # cid:current id
    '''return No.i node optimal power and the index'''
    
    nei = nodes[cid].neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j   
    ########################################################
    a = 1
    b = 1
    ########################################################    
    kc = graph.Connect(G_deba, Node.n, cid)
    
    power = nodes[cid].power
    p = Simulator.dis_to_power(power)
    pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
    
    avg_e = average_energy(cid, nodes, G_deba, Node.n)
    ei_er = nodes[cid].energy_init / nodes[cid].energy_residual
    
    umax =  kc * (a * pmax * ei_er + b * avg_e) - a * p * ei_er
    
    MG = copy.deepcopy(G_deba)
    if cnt < len(d):
        for j in range(len(d)):
            if d[j] > d[cnt]:
                MG[cid][ n[j] ] = 0
                MG[ n[j] ][cid] = 0   
        ########################################################
        kc = graph.Connect(MG, Node.n, cid)
        
        p = Simulator.dis_to_power(d[cnt])
        pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
        
        avg_e = average_energy(cid, nodes, MG, Node.n)
        ei_er = nodes[cid].energy_init / nodes[cid].energy_residual 
        
        u = kc * (a * pmax * ei_er + b * avg_e) - a * p * ei_er
        #########################################################
        if (kc) == 1 and u > umax:
            power = d[cnt]
    return power

def degree(cid, G, n):
    kmin = 1
    k = len([i for i in range(n) if G[cid][i] == 1]) - 1
    if k >= kmin:
        return 1
    else:
        return 0
    
def average_energy(cid, nodes, G, n):
    e = 0
    nei = [i for i in range(n) if G[cid][i] == 1 and cid != i]
    for x in nei:
        e +=  nodes[ x ].energy_residual / nodes[ x ].energy_init
    if len(nei) != 0:    
        e = e / len(nei)
    return e