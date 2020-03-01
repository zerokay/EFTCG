#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:01:37 2018

@author: kay
"""

import copy
from simulator import Simulator
from node import Node
import mytarjan

def my(k_c):    
    G_my = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes)
    
    # better response
    m = 0
    for i in range(Node.n):
        nei = nodes[i].neighbor
        n = [x[0] for x in nei]  # Neighbor Node id
        d = [x[1] for x in nei]  # the distance of i and j
        if len(d) > m:
            m = len(d) - 1
    ############################################################
    cnt = 0
    while True:
        if cnt > m:break
        for i in range(Node.n-1):
            u = my_utility(nodes, i, G_my, cnt, k_c)
            if u != nodes[i].power:
                nodes[i].power = u
                nei = nodes[i].neighbor
                n = [x[0] for x in nei]  # Neighbor Node id
                d = [x[1] for x in nei]  # the distance of i and j
                for j in range(len(d)):
                    if d[j] > u:
                        G_my[i][ n[j] ] = 0
                        G_my[ n[j] ][i] = 0
        cnt += 1
    print("Number of iterations of EFTCG:", cnt)
    return G_my, nodes


def my_utility(nodes, cid, G_my, cnt, k_c):  # cid:current id
    '''return No.i node optimal power and the index'''
    
    nei = nodes[cid].neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j  
    #######################################################
    mytarjan.g = G_my
    mytarjan.init()
    kcon = mytarjan.k_tarjan(k_c, Node.n, cid)
    #######################################################
    power = nodes[cid].power
    p = Simulator.dis_to_power(power)
    pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
    avg_e = average_energy(cid, nodes, G_my, Node.n )
    er_ei = nodes[cid].energy_residual / nodes[cid].energy_init       
    ########################################################
    a = 1 - er_ei
    b = er_ei
    #######################################################
    
    MG = copy.deepcopy(G_my)
    if cnt < len(d):
        #################################################################  
        umax = kcon * (a * ((pmax - p) / pmax) + b * avg_e)
        #################################################################
        for j in range(len(d)):
            if d[j] > d[cnt]:
                MG[cid][ n[j] ] = 0
                MG[ n[j] ][cid] = 0
        #################################################
#        kc = graph.Connect(MG, Node.n)    # judge the connect after close
        #################################################
        mytarjan.g = MG
        mytarjan.init()
        kcon = mytarjan.k_tarjan(k_c, Node.n, cid)
        #################################################
        p = Simulator.dis_to_power(d[cnt])
        pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
        avg_e = average_energy(cid, nodes, MG, Node.n)
        ##############################################################
        u = kcon * (a * ((pmax - p) / pmax) + b * avg_e)
        ##############################################################
        if kcon == 1 and u > umax:
            power = d[cnt]
    return power

def average_energy(cid, nodes, G, n):
    e = 0
    nei = [i for i in range(n) if G[cid][i] == 1 and cid != i]
    for x in nei:
        e +=  nodes[ x ].energy_residual / nodes[ x ].energy_init
    if len(nei) != 0:    
        e = e / len(nei)
    return e