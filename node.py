import numpy as np
import copy
from simulator import Simulator

class Node(object):
    """Sensor Node"""
    
    # ======================================
    # WSN Simulation Environment Parameters. 
    # ======================================
    xm = 300
    ym = 300           # Target Area: x*y 
    n = 50             # total number of nodes
    communicate_distance_max = 100  # maximum communication distance
    energy_init = 50   # initial energy of a node
    
    # initial residual  energy of nodes
    # obey the Poisson distribution(the parameter 'lambda' is 25)
    # rvs: random varsiates.(mu: lambda, loc: bias, size: n)
    # Question: Why is Poisson distribution?
#    poisson_lambda = n/2
#    energy_poisson = poisson.rvs(mu = poisson_lambda, loc = 0, size = n)
    
    l_x = []
    l_y = []            # location list
    nodes = []          # all sensor nodes
#    power_list = []          # power list
    adjacency_matrix = []     # adjacency matrix: single link
    interconnect_matrix = []  # interconnect matrix: double link
    
#    np.random.seed(33)    
    def location_random(xm, ym, n):
        
#        return (np.linspace(30, xm, n+1),
#                np.linspace(30, xm, n+1))
        return (np.random.randint(xm, size=n), 
                np.random.randint(ym, size=n))

    def __init__(self):
        """sensor node default attribute """
        
        self.x = 0
        self.y = 0                       # 2D location
        self.c_d_max = Node.communicate_distance_max  # maximum communication distance
        self.power = self.c_d_max        # maximum communication distance 
        self.neighbor = []               # neighbors by single link
        self.double_neighbor = []        # neighbors by double link
        self.power_select = 0                    # power select by DIA in beiborhood
        self.energy_init = Node.energy_init      # initial energy
        self.energy_residual = 0                 # residual energy
        self.power_list = []        # list of powers for all node
        
    def init_nodes():
        """ initialize attribute of every node
        
        initialize node in order
        """
        
        Node.l_x, Node.l_y = Node.location_random(Node.xm, Node.ym, Node.n)
        Node.nodes = []
        
#        np.random.seed(33)
        poisson_lambda = 25 # 50/2
        energy_poisson = np.random.poisson(lam = poisson_lambda,size = Node.n)
#        print(energy_poisson)
        # initialize the ordinary node
        for i in range(Node.n-1):
            node = Node()
            node.id = i
            node.x = Node.l_x[i]
            node.y = Node.l_y[i]
            # node.power = Node.com_dis_max  # Node.e_p[i] + 50
            node.energy_residual = energy_poisson[i]
#            if node.energy_residual > 50:
#                node.energy_residual = 50
            Node.nodes.append(node)
        
        # initial sink
        sink = Node()
        sink.x = Node.xm / 2
        sink.y = Node.ym / 2
        sink.energy_residual =  Node.energy_init #energy_poisson[Node.n-1]#Node.energy_init
        sink.id = Node.n-1
        Node.nodes.append(sink)
        
    def find_neighbors():
        """ find all neighbors of each node """
        
        adjacency_matrix  =  np.eye(Node.n)  # create unit matrix
        power = []
        
        # create single link adjacency matrix
        for i in range(Node.n):
            for j in range(Node.n):
                if i == j: continue
                d = Simulator.distance(Node.nodes[i], Node.nodes[j])
                if d <= Node.nodes[i].power:
                    power.append(d)
                    adjacency_matrix[i][j] = 1
                    Node.nodes[i].neighbor.append([j, d])
            
            # descending sort by distance
            Node.nodes[i].neighbor.sort(key=lambda x:x[1],reverse=True)
            Node.nodes[i].double_neighbor = copy.deepcopy(Node.nodes[i].neighbor)
            
        Node.adjacency_matrix = adjacency_matrix
        Node.interconnect_matrix = Node.adjacency_matrix
#        print("no-set-power of links:", len(power))
        Node.power_list = sorted(list(set(power)), reverse = True)
        for i in range(Node.n):
            Node.nodes[i].power_list = copy.deepcopy(Node.power_list)
        
    def find_interconnect():
        """find neighbors by double link"""
        
        interconnect_m = copy.deepcopy(Node.adjacency_matrix)
        
        for i in range(Node.n):
            for j in range(i): # traversing the lower triangular matrix
                if interconnect_m[i][j] != interconnect_m[j][i]:
                    interconnect_m[i][j] = 0
                    interconnect_m[j][i] = 0
                    for x in Node.nodes[i].neighbor:
                        if x[0] == j:
                            Node.nodes[i].double_neighbor.remove(x)
                    for x in Node.nodes[j].neighbor:
                        if x[0] == i:
                            Node.nodes[j].double_neighbor.remove(x)
        Node.interconnect_matrix = interconnect_m             
        