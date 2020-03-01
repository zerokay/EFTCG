#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 09:02:05 2019

@author: kay
"""

import copy
import numpy as np
import graph
import itertools

visited = {}
dfn = {}
low = {}
parent = {}
count = 0
ap = set()

g = [[1,1,0,0],
     [1,1,1,0],
     [0,1,1,1],
     [0,0,1,1]]

def init():
    global visited, count, dfn, low, parent, ap
    visited = {}
    dfn = {}
    low = {}
    parent = {}
    count = 0
    ap = set()

def neighbours(cid):  
    nei = []  
    tmp = g[cid]  
    for i in range(len(tmp)):  
        if i != cid and tmp[i] == 1:  
            nei.append(i)  
    return nei  

def dfs(u):
    global visited, count, dfn, low, parent, ap
    children = 0
    count += 1
    dfn[u] = low[u] = count
    visited[u] = True
    for v in neighbours(u):
        if not visited.get(v, False):
            children += 1
            parent[v] = u
            dfs(v)
            low[u] = min(low[u], low[v])
            if parent.get(u, -1) == -1 and children >= 2:
#                print("Articulation point:", u)
                ap.add(u)
            elif parent.get(u, -1) != -1 and low[v] >= dfn[u]:
#                print("Articulation point:", u)
                ap.add(u)
        elif v != parent.get(u, -1):
            low[u] = min(low[u], dfn[v])

def tarjan(start=0):
    dfs(start)
#    print("Articulation point:", ap) 
    if len(ap):
        return 0
    else:
        return 1

def k_tarjan(k, length, cid):
    global g
    if k == 1:
        return graph.Connect(g, length, cid)
    elif k == 2:
        init()
        return graph.Connect(g, length, cid) and tarjan(cid) 
    else:
        l = list(range(length-1))
        lst = itertools.combinations(l, k-2)
        g_ = copy.deepcopy(g)
        num = 0
        for x in lst:
            num += 1
#            print("The count of enum is: ", num)
            gg = copy.deepcopy(g_)
            combin = list(x)
#            print("Delete Point:", combin)
            gg = np.delete(g_, combin, 0)  # 删除行
            gg = np.delete(gg, combin, 1)  # 删除列
            g = gg
            init()
            if not graph.Connect(g, length-(k-2), cid) or not tarjan():
#                print("----------------------No k-connect!------------------------")
                return 0
        else:
#            print("--------------------------Yes k-connect!-----------------------")
            return 1
    
if __name__ == "__main__":
    init()
    print(k_tarjan(3, 4, 0))





































