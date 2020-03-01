#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import copy
import random

import plot
import graph
import nx

from node import Node
from simulator import Simulator

from gt.mia import mia
from gt.dia import dia
from gt.mlpt import mlpt
from gt.deba import deba
from gt.myk import my as my

import time

def main():
    time_start = time.asctime( time.localtime(time.time()) )
    # 525 529 530 549
#    np.random.seed(549)
#    Node.n = 60
#    init()  
#    plot_all()
#    standard_all()    
    performance_k()
    fault()
#    f_plot()
    time_end = time.asctime( time.localtime(time.time()) )
    print(time_start, time_end)
    pass

def f_plot():
    Node.n = 60
    init()
    (G, N) = deba()
    plot.display_topology(G, N, "DEBA")
    
    (G, N) = my(1)
    plot.display_topology(G, N, "EFTCG-1")
    
    (G, N) = my(2)
    plot.display_topology(G, N, "EFTCG-2")
    
        
def symmetric_matrix(G):
    GG = np.transpose(G) 
    r = (G==GG).all()
    return r

def performance_k():
    x = range(40, 110, 10)
    num = 5 # number of evaluation-index
    times = 10 # number of iterations
    y_deba = [[] for x in range(num)]
    y_k1 = [[] for x in range(num)]
    y_k2 = [[] for x in range(num)]
    for i in x:
        print("The number of nodes:", i)
        Node.n = i
        y_deba_ = [[] for x in range(num)]
        y_k1_ = [[] for x in range(num)]
        y_k2_ = [[] for x in range(num)]
        for j in range(times):
            print("The count:", j)
            init()
            n = Node.n
            size_ = 10
            fault_node = random.sample(range(n-2), size_)
            
            G, N = deba()
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.survival_time(len(N), N, G)
            d, e = fault_k(len(N), G, fault_node)
            y_deba_[0].append(a)
            y_deba_[1].append(b)
            y_deba_[2].append(c)
            y_deba_[3].append(d)
            y_deba_[4].append(e)
        
            G, N = my(1)
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.survival_time(len(N), N, G)
            d, e = fault_k(len(N), G, fault_node)
            y_k1_[0].append(a)
            y_k1_[1].append(b)
            y_k1_[2].append(c)
            y_k1_[3].append(d)
            y_k1_[4].append(e)
            
            G, N = my(2)
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.survival_time(len(N), N, G)
            d, e = fault_k(len(N), G, fault_node)
            y_k2_[0].append(a)
            y_k2_[1].append(b)
            y_k2_[2].append(c)
            y_k2_[3].append(d)
            y_k2_[4].append(e)
        ###########################################
        # power
        ##########################################
        y_deba[0].append(np.mean(y_deba_[0]))
        y_k1[0].append(np.mean(y_k1_[0]))
        y_k2[0].append(np.mean(y_k2_[0]))
        ###########################################
        # degree
        ##########################################
        y_deba[1].append(np.mean(y_deba_[1]))
        y_k1[1].append(np.mean(y_k1_[1]))
        y_k2[1].append(np.mean(y_k2_[1]))
        ##########################################
        # survive time
        ##########################################
        y_deba[2].append(np.mean(y_deba_[2]))
        y_k1[2].append(np.mean(y_k1_[2]))
        y_k2[2].append(np.mean(y_k2_[2]))
        ###########################################
        # failure rate
        ##########################################
        y_deba[3].append(np.mean(y_deba_[3]))
        y_k1[3].append(np.mean(y_k1_[3]))
        y_k2[3].append(np.mean(y_k2_[3]))
        ###########################################
        # links rate
        ##########################################
        y_deba[4].append(np.mean(y_deba_[4]))
        y_k1[4].append(np.mean(y_k1_[4]))
        y_k2[4].append(np.mean(y_k2_[4]))
    ###############################################
    y0 = [
         [y_deba[0], "DEBA"],
         [y_k1[0], "EFTCG-1"],
         [y_k2[0], "EFTCG-2"],
        ]
    
    y1 = [
         [y_deba[1], "DEBA"],
         [y_k1[1], "EFTCG-1"],
         [y_k2[1], "EFTCG-2"],
        ]
    y2 = [
         [y_deba[2], "DEBA"],
         [y_k1[2], "EFTCG-1"],
         [y_k2[2], "EFTCG-2"],
        ]
    y3 = [
         [y_deba[3], "DEBA"],
         [y_k1[3], "EFTCG-1"],
         [y_k2[3], "EFTCG-2"],
        ]
    y4 = [
         [y_deba[4], "DEBA"],
         [y_k1[4], "EFTCG-1"],
         [y_k2[4], "EFTCG-2"],
        ]
    
    plot.plot_performance(x, y0, ylabel="Average Transmit Power")
    plot.plot_performance(x, y1, ylabel="Average Node Degree")
    plot.plot_performance(x, y2, ylabel="Network Lifetime")
    plot.plot_performance(x, y3, ylabel="Rate of Survival Nodes")
    plot.plot_performance(x, y4, ylabel="Rate of Connectable Node Pairs")
    
    
def fault_k(n, G, fault_node):
    in_num, links = robust(n, G, fault_node)
#    print(links)
    end = len(fault_node) - 1
#    print(in_num[end], n)
    return ((100 - (in_num[end] / n * 100)), 
            2 * (links[end] / (n * (n - 1))) * 100)
    pass
    
def fault():
    size_ = 10
    n = 60
    times = 1
    k1_in_num_ = []
    k1_links_ = []
    
    k2_in_num_ = []
    k2_links_ = []
    
    deba_in_num_ = []
    deba_links_ = []
    ###########################################################
    for i in range(times):
        Node.n = n
        init()
        n = Node.n
        size_ = 10
        fault_node = random.sample(range(n-2), size_)#= fault_node
        print("Fault Node is:", fault_node)
        #######################################################
        # EFTCG-1                                             #
        #######################################################
        G, N = my(1)
        in_num, links = robust(n, G, fault_node)
#        ad_1 = Simulator.average_degree(n, G)
#        st_1 = Simulator.survival_time(n, N, G)
        
        k1_in_num_.append(in_num)
        k1_links_.append(links)
        #######################################################
        # EFTCG-2                                             #
        #######################################################
        G, N = my(2)
        in_num, links = robust(n, G, fault_node)
#        ad_2 = Simulator.average_degree(n, G)
#        st_2 = Simulator.survival_time(n, N, G)
        
        k2_in_num_.append(in_num)
        k2_links_.append(links)
        #######################################################
        # DEBA                                                #
        #######################################################
        G, N = deba()
        in_num, links = robust(n, G, fault_node)
#        ad_3 = Simulator.average_degree(n, G)
#        st_3 = Simulator.survival_time(n, N, G)
        
        deba_in_num_.append(in_num)
        deba_links_.append(links)
    ##############################################################
    def avg(*lst):
#        global size_
        avg_ = 0
        for x in lst:
            avg_ += x / size_
        return avg_
    
    def fr(x):
#        global n
        return x / n * 100
    
    def rl(x):
#        global n
        return x / (n * (n-1)) * 100
    #############################################################      
    # failure rate
    #############################################################    
    k1_fr = list(map(fr, list(map(avg, *(k1_in_num_)))))
    k2_fr = list(map(fr, list(map(avg, *(k2_in_num_)))))
    deba_fr = list(map(fr, list(map(avg, *(deba_in_num_)))))
    
    #############################################################      
    # links
    ############################################################# 
    k1_rl = list(map(rl, list(map(avg, *(k1_links_)))))
    k2_rl = list(map(rl, list(map(avg, *(k2_links_)))))
    deba_rl = list(map(rl, list(map(avg, *(deba_links_)))))
            
            
    #############################################################    
    x = list(range(1, size_+1))
    y0 = [
         [deba_fr, "DEBA"],
         [k1_fr, "EFTCG-1"],
         [k2_fr, "EFTCG-2"],
         
        ]
    y1 = [
         [[100 - x for x in deba_fr], "DEBA"],
         [[100 - x for x in k1_fr], "EFTCG-1"],
         [[100 - x for x in k2_fr], "EFTCG-2"],
        ]
    y2 = [
         [deba_rl, "DEBA"],
         [k1_rl, "EFTCG-1"],
         [k2_rl, "EFTCG-2"],
        ]
#    plot.plot_performance(x,y0,xlabel="Number of fault nodes",ylabel="Rate of Failure Nodes")
    plot.plot_performance(x,y1,xlabel="Number of fault nodes",ylabel="Rate of Survival Nodes")
    plot.plot_performance(x,y2,xlabel="Number of fault nodes",ylabel="Rate of Connectable Node Pairs")   
    pass
        
    
def robust(n, MG, fault_node = [0]):
    G = copy.deepcopy(MG)
    invalid_node = set()
    in_num = []
    links = []
    for j in range(len(fault_node)):
#        print("The delete node is", fault_node[:j+1])
        e = fault_node[j]
        for i in range(n):
            if G[e][i] == 1:
                G[e][i] = 0
                G[i][e] = 0
        ########################################
        for i in range(n-1):
            if not graph.go_to_sink(G, n, i):
                invalid_node.add(i)
        ########################################
#        print("Invalid node is:", invalid_node)
        in_num.append(len(invalid_node))
        ########################################
#        for i in invalid_node:
#            for j in range(len(G)):
#                if G[i][j] == 1:
#                    G[i][j] = 0
#                    G[j][i] = 0
        ########################################
        tp_links = 0
        for i in range(len(G)):
            for j in range(i):
                if nx.has_path(G, i, j):
                    tp_links += 1
        #########################################
#        print("Number of links is :", tp_links)
        links.append(tp_links)
        #########################################
    return in_num, links
    
def links(G):
    tp_links = 0
    for i in range(len(G)):
            for j in range(i):
                if G[i][j] == 1:
                    tp_links += 1
    return tp_links
    
def standard_all():
    Node.n = 100
#    np.random.seed(521)
    init()
    a = dia()
    b = mlpt()
    c = deba()
    d = my(1)
    Node_G = [
              [a,"DIA"],
              [b, "MLPT"],
              [c,"DEBA"],
              [d, "EFTCG"]
             ]
    standard_algorithm(Node.n, Node_G)

def standard_algorithm(n, Node_MG, times = 100):
    x = list(range(times+1))
    std = []
    for ng in Node_MG:
        a = Simulator.send(n, ng[0][1], ng[0][0], times)
        b = [a, ng[1]]
        std.append(b)
    plot.plot_performance(x, std, xlabel="Number of network running round", ylabel = "Standard deviation of the residual energy")

def performance():
    x = range(30, 110, 10)
    num = 4 # number of evaluation-index
    times = 10 # number of iterations
    y_dia = [[] for x in range(num)]
    y_mlpt = [[] for x in range(num)]
    y_deba = [[] for x in range(num)]
    y_eftcg = [[] for x in range(num)]
    for i in x:
        print("The number of nodes:", i)
        Node.n = i
        y_dia_ = [[] for x in range(num)]
        y_mlpt_ = [[] for x in range(num)]
        y_deba_ = [[] for x in range(num)]
        y_eftcg_ = [[] for x in range(num)]
        for j in range(times):
            print("The count:", j)
            init()
            
            G, N = dia()
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.average_hop(len(N), G)
            d = Simulator.survival_time(len(N), N, G)
            y_dia_[0].append(a)
            y_dia_[1].append(b)
            y_dia_[2].append(c)
            y_dia_[3].append(d)
        
            G, N = mlpt()
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.average_hop(len(N), G)
            d = Simulator.survival_time(len(N), N, G)
            y_mlpt_[0].append(a)
            y_mlpt_[1].append(b)
            y_mlpt_[2].append(c)
            y_mlpt_[3].append(d)
            
            G, N = deba()
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.average_hop(len(N), G)
            d = Simulator.survival_time(len(N), N, G)
            y_deba_[0].append(a)
            y_deba_[1].append(b)
            y_deba_[2].append(c)
            y_deba_[3].append(d)
            
            G, N = my(1)
            a = Simulator.average_power(len(N), N)
            b = Simulator.average_degree(len(N), G)
            c = Simulator.average_hop(len(N), G)
            d = Simulator.survival_time(len(N), N, G)
            y_eftcg_[0].append(a)
            y_eftcg_[1].append(b)
            y_eftcg_[2].append(c)
            y_eftcg_[3].append(d)
        ###########################################
        # power
        ##########################################
        y_dia[0].append(np.mean(y_dia_[0]))
        y_mlpt[0].append(np.mean(y_mlpt_[0]))
        y_deba[0].append(np.mean(y_deba_[0]))
        y_eftcg[0].append(np.mean(y_eftcg_[0]))
        ###########################################
        # degree
        ##########################################
        y_dia[1].append(np.mean(y_dia_[1]))
        y_mlpt[1].append(np.mean(y_mlpt_[1]))
        y_deba[1].append(np.mean(y_deba_[1]))
        y_eftcg[1].append(np.mean(y_eftcg_[1]))
        ###########################################
        # hop
        ##########################################
        y_dia[2].append(np.mean(y_dia_[2]))
        y_mlpt[2].append(np.mean(y_mlpt_[2]))
        y_deba[2].append(np.mean(y_deba_[2]))
        y_eftcg[2].append(np.mean(y_eftcg_[2]))
        ##########################################
        y_dia[3].append(np.mean(y_dia_[3]))
        y_mlpt[3].append(np.mean(y_mlpt_[3]))
        y_deba[3].append(np.mean(y_deba_[3]))
        y_eftcg[3].append(np.mean(y_eftcg_[3]))
    ###############################################
    y0 = [
         [y_dia[0], "DIA"],
         [y_mlpt[0], "MLPT"],
         [y_deba[0], "DEBA"],
         [y_eftcg[0], "EFTCG"]
        ]    
    y1 = [
         [y_dia[1], "DIA"],
         [y_mlpt[1], "MLPT"],
         [y_deba[1], "DEBA"],
         [y_eftcg[1], "EFTCG"]
        ]    
    y2 = [
         [y_dia[2], "DIA"],
         [y_mlpt[2], "MLPT"],
         [y_deba[2], "DEBA"],
         [y_eftcg[2], "EFTCG"]
        ]  
    y3 = [
         [y_dia[3], "DIA"],
         [y_mlpt[3], "MLPT"],
         [y_deba[3], "DEBA"],
         [y_eftcg[3], "EFTCG"]
        ]    
    plot.plot_performance(x, y0, ylabel="Average Transmit Power")
    plot.plot_performance(x, y1, ylabel="Average Node Degree")
    plot.plot_performance(x, y2, ylabel="Average Hop")
    plot.plot_performance(x, y3, ylabel="Network Lifetime")
    
def avg_degree():
    x = range(30, 110, 10)
    y = []
    y_dia = []
    y_mlpt = []
    y_deba = []
    y_eftcg = []
    for i in x:
        print("The number of nodes:", i)
        Node.n = i
        y_dia_ = []
        y_mlpt_ = []
        y_deba_ = []
        y_eftcg_ = []
        for j in range(3):
            print("The count:", j)
            np.random.seed(j)
            init()
            
            G, N = dia()
            a = Simulator.average_degree(len(N), G)
            y_dia_.append(a)
        
            G, N = mlpt()
            a = Simulator.average_degree(len(N), G)
            y_mlpt_.append(a)
            
            G, N = deba()
            a = Simulator.average_degree(len(N), G)
            y_deba_.append(a)
            
            G, N = my(1)
            a = Simulator.average_degree(len(N), G)
            y_eftcg_.append(a)
        ###########################################
        y_dia.append(np.mean(y_dia_))
        y_mlpt.append(np.mean(y_mlpt_))
        y_deba.append(np.mean(y_deba_))
        y_eftcg.append(np.mean(y_eftcg_))
    ###############################################
    y = [
         [y_dia, "DIA"],
         [y_mlpt, "MLPT"],
         [y_deba, "DEBA"],
         [y_eftcg, "EFTCG"]
        ]    
    plot.plot_performance(x, y, ylabel="Avarage Degree")
    
def avg_power():
    x = range(30, 110, 10)
    y = []
    y_dia = []
    y_mlpt = []
    y_deba = []
    y_eftcg = []
    for i in x:
        print("The number of nodes:", i)
        Node.n = i
        y_dia_ = []
        y_mlpt_ = []
        y_deba_ = []
        y_eftcg_ = []
        for j in range(3):
            print("The count:", j)
            np.random.seed(j)
            init()
            
            G, N = dia()
            a = Simulator.average_power(len(N), N)
            y_dia_.append(a)
        
            G, N = mlpt()
            a = Simulator.average_power(len(N), N)
            y_mlpt_.append(a)
            
            G, N = deba()
            a = Simulator.average_power(len(N), N)
            y_deba_.append(a)
            
            G, N = my(1)
            a = Simulator.average_power(len(N), N)
            y_eftcg_.append(a)
        ###########################################
        y_dia.append(np.mean(y_dia_))
        y_mlpt.append(np.mean(y_mlpt_))
        y_deba.append(np.mean(y_deba_))
        y_eftcg.append(np.mean(y_eftcg_))
    ###############################################
    y = [
         [y_dia, "DIA"],
         [y_mlpt, "MLPT"],
         [y_deba, "DEBA"],
         [y_eftcg, "EFTCG"]
        ]    
    plot.plot_performance(x, y, ylabel="Avarage Power")
    
def plot_all():
    # 100
    Node.n = 100
    np.random.seed(521)
    init()  
    plot_no_topology()
#    plot_mia()
    plot_dia()
    plot_mlpt()
    plot_deba()
    plot_my()
#    plot_my(2)
#    plot_my(3)
    
def plot_my(k=1):
    (Gmy, Nmy) = my(k)
    plot.display_topology(Gmy, Nmy, "EFTCG-"+str(k))
#    return Gmy, Nmy
   
def plot_deba():
    (Gdeba, Ndeba) = deba()
    plot.display_topology(Gdeba, Ndeba, "DEBA")
#    return Gdeba, Ndeba
    
def plot_mlpt():
    (Gmtc, Nmtc) = mlpt()
    plot.display_topology(Gmtc, Nmtc, "MLPT")
#    return Gmtc, Nmtc
    
def plot_dia():
    (Gdia, Ndia) = dia()
    plot.display_topology(Gdia, Ndia, "DIA")
#    return Gdia, Ndia
    
def plot_mia(n = 1):
    for i in range(n):      
        (Gmia, nodes) = mia(i)
        plot.display_topology(Gmia, nodes, "MIA-"+str(i))
#    return Gmia, nodes

def plot_no_topology():
     plot.display_topology(Node.interconnect_matrix, Node.nodes)
     
def init():  
    connect = False
    cnt = 0 
    while not connect:
        Node.init_nodes()
        Node.find_neighbors()
        #Node.find_interconnect()
        connect = graph.Connect(Node.interconnect_matrix, Node.n)
        cnt += 1
    print("Initialization times:",cnt)
    
    
def judge_connect():
    Node.init_nodes()
    Node.find_neighbors()
    Node.find_interconnect()
    if graph.Connect(Node.interconnect_matrix, Node.n):
        print("connect")
    else:
        print("No connect")
       
if __name__ == '__main__':
    main()
