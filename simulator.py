import numpy as np
import random
import nx

class Simulator(object):
    """Analog wireless sensor network environment"""
    
    receive_threshold = 7 * (10 ** -10)  # Minimum signal received power when receiver is operating
    system_loss = 1
    wave_length = 0.1224  # wavelength 2.45GHz
    trans_gain = 1    # Transmitting antenna gain
    receive_gain = 1            # Receiving antenna gain
        
    def dis_to_power(d):
        '''Distance to Power'''
        x = Simulator.receive_threshold * ((4*np.pi) **2) * (d**2) * Simulator.system_loss
        y = (Simulator.trans_gain * Simulator.receive_gain * (Simulator.wave_length**2))  
        power =  x / y
        return power
    
    def distance(n1, n2):
        d = np.sqrt( (n1.x - n2.x)**2 + (n1.y - n2.y)**2)
        return d

    def standards(n, nodes):
        energy = []
        for i in range(n-1):
            energy.append(nodes[i].energy_residual)           
        return np.std(energy)
    
    def send(n, nodes, G, times = 100):     
        std = []
        std.append(Simulator.standards(n, nodes))
        # minimum hop routing algorithm
        min_hop = nx.min_hop(G)
        #############################################################
        for t in range(times):
            for i in range(n-1):
                route = min_hop[i]
                for x in route:
                    if x == (n-1): continue
                    nodes[x].energy_residual -= Simulator.dis_to_power(nodes[x].power) * 0.1
            std.append(Simulator.standards(n, nodes))
        return std      
                    
    def survival_time(n, nodes, G):
        # minimum hop routing algorithm
        min_hop = nx.min_hop(G)
        #############################################################
        times = 0
        while True:
            times += 1
            tmp = list(range(n-1))
            random.shuffle(tmp)
            for i in tmp:
                route = min_hop[i]
                for x in route:
                    if x == (n-1): continue
                    nodes[x].energy_residual -= Simulator.dis_to_power(nodes[x].power) * 0.1
                    if nodes[x].energy_residual <= 0:
                        print("The First Dead node is :", x)
                        return times
        ##############################################################
######################################################################            
           
    def average_power(n, nodes):
        total = 0
        for i, x in enumerate(nodes):
            if i == n-1:
                continue
            total += Simulator.dis_to_power(x.power)
        average_power = total / (n-1)
        return average_power
    
    def average_degree(n, G):
        d = 0
        for i in range(n-1):
            neighbor = [x for x in G[i][:] if x ]
            d += len(neighbor)
        average_degree = d / n-1
        return average_degree
    
    def average_hop(n, G):
        # minimum hop routing algorithm
        min_hop = nx.min_hop(G)
        hophop = []
        for key, value in min_hop.items():
            if key == n-1:
                continue
            hophop.append(len(value) - 1)
        return np.mean(hophop)
                        
    def average_energy(n, nodes):
        total = 0
        for i, x in enumerate(nodes):
            if i == n-1:
                continue
            total += x.energy_residual
        average_energy = total / (n-1)
        return average_energy
    
    def topology_links(G):
        tp_links = 0
        l = len(G)
        for i in range(l):
            for j in range(i):
                if G[i][j] == 1:
                    tp_links += 1
        #####################################
#        print("Number of links:", tp_links)
        return tp_links
#####################################################################                
#     def send__(n, nodes, G, times = 200):
#        std = []
#        std.append(Simulator.standards(n, nodes))
#        ############################################################
#        a = list(range(n)) # a[i] => pre_node
#        visited = [0] * n
#        queue = []
#        queue.append(n-1)
#        visited[n-1] = 1
#        while(queue):
#            index = queue.pop(0)
#            neighbor = [j for j in range(n) if G[index][j]]
#            for k in neighbor:
#                if not visited[k]:
#                    visited[k] = 1
#                    a[k] = index
#                    queue.append(k)
##        print(a)
#        #############################################################
#        for t in range(times):
#            for i in range(n-1):
#                cid = i
##                print(cid, end="-->")
#                while a[cid] != cid:
#                    nodes[cid].energy_residual -= Simulator.dis_to_power(nodes[cid].power) * 0.1
##                    print(cid, end="-->")
#                    cid = a[cid]
##                print(a[cid])
#            ##########################################################
#            std.append(Simulator.standards(n, nodes))
#        return std
#    
#    def send_(n, nodes, G, times = 1):
#        std = []
#        std.append(Simulator.standards(n, nodes))
#        ############################################################
#        pre_node = []
#        for i in range(n-1):
#            a = list(range(n)) # a[i] => pre_node
#            visited = [0] * n
#            queue = []
#            queue.append(i)
#            visited[i] = 1
#            while(queue):
#                index = queue.pop(0)
#                neighbor = [j for j in range(n) if G[index][j]]
#                for k in neighbor:
#                    if not visited[k]:
#                        visited[k] = 1
#                        a[k] = index
#                        queue.append(k)
#            pre_node.append(a)
#        #############################################################
#        for t in range(times):
#            for i in range(n-1):
#                a = pre_node[i]
#                ####################################################
#                kay = n-1 # pre_node
##                print("Kay", end="<--")
#                while kay != i:
#                    kay = a[kay]
#                    nodes[kay].energy_residual -= Simulator.dis_to_power(nodes[kay].power) * 0.1
##                    print(kay+1, end="<--")
##                print("*")  
#            ########################################################
#            std.append(Simulator.standards(n, nodes))
#        return std           
                
#    def survival_time__(n, nodes, G):     
#        a = list(range(n)) # a[i] => pre_node
#        visited = [0] * n
#        queue = []
#        queue.append(n-1)
#        visited[n-1] = 1
#        while(queue):
#            index = queue.pop(0)
#            neighbor = [j for j in range(n) if G[index][j]]
#            for k in neighbor:
#                if not visited[k]:
#                    visited[k] = 1
#                    a[k] = index
#                    queue.append(k)
#        #############################################################
#        times = 0
#        while True:
#            times += 1
#            tmp = list(range(n-1))
#            random.shuffle(tmp)
#            for i in tmp:
##                print(i, end="-->")
#                cid = i
#                while a[cid] != cid:
#                    nodes[cid].energy_residual -= Simulator.dis_to_power(nodes[cid].power) * 0.1
#                    if nodes[cid].energy_residual <= 0:
#                        print("The First Dead node is :", cid)
#                        return times
#                    cid = a[cid]
##                    print(i, end="-->")
##                print("kay")
#                    
#    def survival_time_(n, nodes, G):
#        ############################################################
#        pre_node = []
#        for i in range(n-1):
#            a = list(range(n)) # a[i] => pre_node
#            visited = [0] * n
#            queue = []
#            queue.append(i)
#            visited[i] = 1
#            while(queue):
#                index = queue.pop(0)
#                neighbor = [j for j in range(n) if G[index][j]]
#                for k in neighbor:
#                    if not visited[k]:
#                        visited[k] = 1
#                        a[k] = index
#                        queue.append(k)
#            pre_node.append(a)
#        #############################################################
#        times = 0
#        while True:
#            times += 1
#            for i in range(n-1):
#                a = pre_node[i]
#                ####################################################
#                kay = n-1 # pre_node
#                while kay != i:
#                    kay = a[kay]
#                    nodes[kay].energy_residual -= Simulator.dis_to_power(nodes[kay].power) * 0.1
#                    if nodes[kay].energy_residual <= 0:
#                            return times
#        ######################################################################################                
                
#    def avg_hop(n, G):
#        pre_node = []
#        for i in range(n-1):
#            a = list(range(n)) # a[i] => pre_node
#            visited = [0] * n
#            queue = []
#            queue.append(i)
#            visited[i] = 1
#            while(queue):
#                index = queue.pop(0)
#                neighbor = [j for j in range(n) if G[index][j]]
#                for k in neighbor:
#                    if not visited[k]:
#                        visited[k] = 1
#                        a[k] = index
#                        queue.append(k)
#            pre_node.append(a)
#        #############################################################
#        hophop = []
#        for i in range(n-1):
#            a = pre_node[i]
#            ####################################################
#            kay = n-1 # pre_node
#            hop = 0
##            print("Kay", end="<--")
#            while kay != i:
#                kay = a[kay]
#                hop += 1
##                print(kay+1, end="<--")
##            print("*")
#            hophop.append(hop)
#        return np.mean(hophop) 

#    def average_energy2(n, nodes, G):
#        total = 0
#        cnt = 0
#        for i in range(n):
#            for j in range(n):
#                if i != j and G[i][j] == 1:
#                    total += nodes[j].energy_residual
#                    cnt += 1
#        average_energy = total / cnt
#        return average_energy               
    
#    def max_average_hop(n, G):
#        max_hop = 0
#        t_hop = 0
#        for i in range(n):
#            (m_h, avg_h) = graph.hop(G, i, n)
#            if max_hop < m_h:
#                max_hop = m_h
#            t_hop +=  avg_h
#        average_hop = t_hop / n
#        return (max_hop, average_hop)