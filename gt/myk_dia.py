import graph
import copy
from simulator import Simulator
from node import Node
import mytarjan

def my(k_c):
    M = Simulator.dis_to_power(Node.communicate_distance_max) 
    G_dia = copy.deepcopy(Node.interconnect_matrix)  # innerconnect matrix of mia
    nodes = copy.deepcopy(Node.nodes) 
    
    flag = True  # is the power of node (game theory result) the NE?
    cnt = 0      # number of games   
    while flag:
        flag = False
        cnt += 1  
        for i in range(Node.n):
            # Run length of power_list times
            if cnt >= len(Node.power_list): 
                break  # power_list include all the power            
            u, index = dia_utility(i, nodes, G_dia, M, cnt, k_c)            
            if u != nodes[i].power: # u is not NE, continue
                flag = True
                nodes[i].power = u
                if index > nodes[i].power_select:                    
                    nei = nodes[i].double_neighbor
                    n = [x[0] for x in nei]  # id of beighbor of node-i 
                    G_dia[i][ n[nodes[i].power_select] ] = 0
                    G_dia[ n[nodes[i].power_select] ][i] = 0
                    
                    nodes[i].power_select = index
    print("Number of iterations of my:", cnt)
    return G_dia, nodes


def dia_utility(cid, nodes, G_Mia, M, cnt, k_c):  # cid:current id
    '''return No.i node optimal power and the index'''
    
    MG = copy.deepcopy(G_Mia)
    nei = nodes[cid].double_neighbor
    n = [x[0] for x in nei]  # Neighbor Node id
    d = [x[1] for x in nei]  # the distance of i and j
    
    pw_list = nodes[cid].power_list   
    ####################################################
    a = 1
    b = 1    
    ####################################################
    #k = graph.Connect(MG, Node.n)    # judge the connect after close
    mytarjan.g = MG
    mytarjan.init()
    kcon = mytarjan.k_tarjan(k_c, Node.n, cid)
    ####################################################
    power = nodes[cid].power
    p = Simulator.dis_to_power(power)
    pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
    avg_e = average_energy(cid, nodes, MG, Node.n )
    er_ei = nodes[cid].energy_residual / nodes[cid].energy_init 
 
    umax = kcon * (a + b * avg_e) - (p / pmax) * (1-er_ei)
    ####################################################    
    index = nodes[cid].power_select  # next selection of power
    count_power = pw_list[cnt]
    flag = False  # Whether the topology changes when power is reduced
    ####################################################      
    if index < len(nei):  # Index points to the last link if temp > length of d
        if count_power < d[index]:
            MG[cid][(n[index])] = 0
            MG[(n[index])][cid] = 0           
            flag = True
        ###############################################################   
        #k = graph.Connect(MG, Node.n)  # judge the connect after close
        mytarjan.g = MG
        mytarjan.init()
        kcon = mytarjan.k_tarjan(k_c, Node.n, cid)
        ###############################################################
        avg_e = average_energy(cid, nodes, MG, Node.n)
        p = Simulator.dis_to_power(count_power)
        pmax = Simulator.dis_to_power(nodes[cid].c_d_max)
        er_ei = nodes[cid].energy_residual / nodes[cid].energy_init 
        u = kcon * (a + b * avg_e) - (p / pmax) * (1-er_ei)

        if kcon > 0 and u > umax: 
            power = count_power
            if flag:
                index += 1
            
    return power, index

def average_energy(cid, nodes, G, n):
    e = 0
    nei = [i for i in range(n) if G[cid][i] == 1]
    for x in nei:
        e +=  nodes[ x ].energy_residual / nodes[ x ].energy_init        
    avg_e = e / len(nei)
    return avg_e