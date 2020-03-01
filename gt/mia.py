import graph
import copy
from simulator import Simulator
from node import Node

def mia(start=0):
    '''Max-Improvement Algorithm or Best-Responding Algorithm
    
    make sure the value of utility function result is a positive  number
    '''
    
    M = Simulator.dis_to_power(Node.communicate_distance_max)  
    G_Mia = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes)
    
    flag = True  # is the power of node (game theory result) the NE?
    cnt = 0      # number of games
    while flag:
        cnt += 1
        flag = False       
        for i in range(start, Node.n):
            flag = mia_local(i, nodes, G_Mia, M)
        for i in range(0, start):
            flag = mia_local(i, nodes, G_Mia, M)                      
    print("Number of iterations of MIA:", cnt)
#    print(nodes[Node.n-1].power)
    return G_Mia, nodes

def mia_local(i, nodes, G_Mia, M):
    flag = False
    u = mia_utility(i, nodes, G_Mia, M)
    if u != nodes[i].power: # u is not NE, continue
        nodes[i].power = u
        flag = True
        nei = nodes[i].double_neighbor
        n = [x[0] for x in nei]  # id of node 
        d = [x[1] for x in nei]  # distance of node 
        for j in range(len(n)):  # according to the u, close the link
            if d[j] > u:
                G_Mia[  i ][n[j]] = 0
                G_Mia[n[j]][  i ] = 0
#            else:
#                G_Mia[  i ][n[j]] = 1
#                if G_Mia[n[j]][  i ] == 0:
#                    G_Mia[  i ][n[j]] = 0
    return flag
    
def mia_utility(cid, nodes, G_Mia, M):  # cid:current id
    '''return No.i node optimal power'''
    
    MG = copy.deepcopy(G_Mia)
    nei = nodes[cid].double_neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j      
    index = 0  # index of id of node that is NE
    utility_max = 0
    
    for i in range(len(n)):
        p = d[i]  # power
        for j in range(i):
            if d[j] > p:  # if d[j] > tp  close the connect
                MG[  cid ][n[j]] = 0
                MG[n[j]][  cid ] = 0
                
        k = graph.Connect(MG, Node.n, cid)  # judge the connect after close
#        k = graph.go_to_sink(MG, Node.n, cid)  # judge the connect after close
        u = M * k * Node.n - Simulator.dis_to_power(d[i]) # utility funciton
        
        if k > 0 and u > utility_max:
            utility_max = u
            index = i
            
    return d[index]
                       
