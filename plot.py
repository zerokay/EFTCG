import numpy as np
import matplotlib.pyplot as plt
from simulator import Simulator
t_line = 0.001
t_circle = 0.1

def display_topology(G, nodes, msg="No Topology Control"):
    plt.figure(figsize=(6,6))
    plt.xlim(0, 300)
    plt.ylim(0, 300)  
    plt.xlabel("X/m")
    plt.ylabel("Y/m")
    plot_nodes(nodes)
    plot_topology(G,nodes)
#    plt.title(msg)
    plt.show()
    print(msg)
    
def plot_topology(G,nodes):
    tp_links = 0
    l = len(G)
    for i in range(l):
        for j in range(i):
            if G[i][j] == 1:
                tp_links += 1
                plot_line(nodes[i], nodes[j])
#                plot_distance2(nodes[i], nodes[j])
    print("Number of links:", tp_links)
    
def plot_nodes(nodes):
    """plot all nodes, include information"""
    x = [node.x for node in nodes]
    y = [node.y for node in nodes]
    plt.plot(x, y, 'k.')
#    plot_nodes_id(nodes)
    plot_nodes_energy(nodes)
#    plot_nodes_power(nodes)

def plot_nodes_id(nodes):
    i = 1
    for node in nodes:
        plt.text(node.x+4, node.y-4, str(i)) #"ID:"+str(i))
        i += 1

def plot_nodes_energy(nodes):
    for node in nodes:
        plt.text(node.x+4, node.y-4, ""+str(int(node.energy_residual)))
        
def plot_nodes_power(nodes):
    for node in nodes:
        plt.text(node.x+2, node.y+8, "P:"+str(int(node.power)))


def plot_all_neighbors(nodes):
    for sink in nodes:
        plot_neighbors(sink, nodes)
        # plt.draw()
        # plt.pause(1)

def plot_neighbors(sink,nodes):
    nei = sink.double_neighbor
#    plot_circle(sink.x, sink.y, sink.power)
    for j, d in nei:
        plot_line(sink, nodes[j])
        plot_distance(sink, nodes[j], d)

def plot_distance(n1, n2, dis):
    msg = "the distance of "+str(n1.id) + "->" + str(n2.id) + ": " + str(int(dis))
    print(msg)
    plt.text((n1.x + n2.x)/2,
             (n1.y + n2.y)/2-3,
             msg)

def plot_distance2(n1, n2):
    d = Simulator.distance(n1, n2)
    msg = "d("+str(n1.id) + "," + str(n2.id) + ")=" + str(int(d))
#    print(msg)
    plt.text((n1.x + n2.x)/2-8,
             (n1.y + n2.y)/2,
             msg)
def plot_line(p1, p2):           # point1, point2
    x = [p1.x, p2.x]
    y = [p1.y, p2.y]
    plt.plot(x, y, 'k')
    #plt.pause(t_line)

def plot_circle(a=0, b=0, r=2):
    theta = np.arange(0, 2*np.pi, 0.01)
    x = a + r * np.cos(theta)
    y = b + r * np.sin(theta)
    plt.plot(x, y)
    plt.text(a+r/2, b+r/2, "radius:"+str(r))
    
    plt.pause(t_circle)
    
def plot_performance(x,y,xlabel="Number of Nodes",ylabel="None"):
    style = ["r:","g-.", "b--", "k-" , "m-"]
    style = ["rs:","g^-.", "bd--", "ko-" , "m*-"]
    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for i, yy in enumerate(y):
        plt.plot(x, yy[0], style[i], label = yy[1], )
    plt.legend()
    plt.grid()
    plt.show() 

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    