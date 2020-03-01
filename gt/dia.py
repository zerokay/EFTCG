import graph
import copy
from simulator import Simulator
from node import Node


def dia():
    '''d-Improvement Algorithm
    
    make sure the value of utility function result is a positive  numbers
    ''' 
    
    G_dia = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes)
    
    M = Simulator.dis_to_power(Node.communicate_distance_max) 
    
    flag = True  # is the power of node (game theory result) the NE?
    cnt = 0      # number of games  
    while flag:
        flag = False
        if cnt > (len(Node.power_list)-1): break  # power_list include all the power
        for i in range(Node.n-1):
            # Run length of power_list times
            u, index = dia_utility(i, nodes, G_dia, M, cnt)     
            if u == Node.communicate_distance_max:
                flag = True
                break
            if u != nodes[i].power: # u is not NE, continue
                flag = True
                nodes[i].power = u
                
                if index > nodes[i].power_select:                    
                    nei = nodes[i].double_neighbor
                    n = [x[0] for x in nei]  # id of beighbor of node-i 
                    G_dia[i][ n[nodes[i].power_select] ] = 0
                    G_dia[ n[nodes[i].power_select] ][i] = 0
                    
                    nodes[i].power_select = index
        cnt += 1
    print("Number of iterations of DIA:", cnt)
    return G_dia, nodes

def dia_utility(cid, nodes, G_dia, M, cnt):  # cid:current id
    '''return No.i node optimal power and the index'''
    
    MG = copy.deepcopy(G_dia)
    nei = nodes[cid].double_neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j
    
    pw_list = nodes[cid].power_list
    power = nodes[cid].power
    
    # The line where the neighbor ID currently needs to be disconnected 
    # It is initially 0.
    index = nodes[cid].power_select  # next selection of power
    k = graph.Connect(MG, Node.n)    # judge the connect after close
    
    umax = M * k - Simulator.dis_to_power(power)
    
    flag = False  # Whether the topology changes when power is reduced
    count_power = pw_list[cnt]
    
    if index < len(nei):  # Index points to the last link if temp > length of d
        if count_power < d[index]:
            MG[cid][(n[index])] = 0
            MG[(n[index])][cid] = 0           
            flag = True
            
        k = graph.Connect(MG, Node.n, cid)  # judge the connect after close
        u = M * k - Simulator.dis_to_power(count_power) # utility funciton
        
        if k > 0 and u > umax:
            power = count_power
            if flag:
                index += 1
            
    return power, index