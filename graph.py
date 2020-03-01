import numpy as np
import copy

def Connect(G, n, cid=0):
    '''use BFS, DFS, DSU(Disjoin Set Union)'''
    
    visited = [0] * n
    BFS(G, n, visited, cid)
    #print(visited)
    if 0 in  visited:
        return 0
    return 1

def go_to_sink(G, n, cid=0):
    '''use BFS, DFS, DSU(Disjoin Set Union)'''
    
    visited = [0] * n
    BFS(G, n, visited, cid)
    #print(visited)
    if not visited[n-1]:
        return 0
    return 1
  
def BFS(MG, n, visited, cid=0):
    """Breadth First Search by Using Adjacenty Matrix"""
    ####################################################
    # Delete unidirectional link
    ####################################################
    G = copy.deepcopy(MG)
#    for i in range(len(G)):
#        for j in range(len(G)):
#            if G[i][j] == 0:
#                G[j][i] = 0
    #####################################################
    queue = []
    visited[cid] = 1
    queue.append(cid)
    while(queue):
        i = queue.pop(0)
        neighbor = [j for j in range(n) if G[i][j]]
        for k in neighbor:
            if not visited[k]:
                visited[k] = 1
                queue.append(k)                
                                   
def flow(G, n):  
    """ the flow of every node """
    H = np.zeros([n, n])  # number of sij | H: hop
    for i in range(n):
        a = list(range(n)) # a[i] => pre_node
        visited = [0] * n
        queue = []
        queue.append(i)
        visited[i] = 1
        while(queue):
            index = queue.pop(0)
            neighbor = [j for j in range(n) if G[index][j]]
            for k in neighbor:
                if not visited[k]:
                    visited[k] = 1
                    a[k] = index
                    queue.append(k)
        ########################################            
        for j in range(n): # When the link passes through the node
            while a[j] != j:
                H[j][ a[j] ] += 1
                H[ a[j] ][j] += 1
                j = a[j]
    return H

#def BFS_by_neighbor(nodes, visited):
#    '''Breadth First Search By Using Neighbors'''
#    
#    queue = []
#    visited[0] = 1
#    queue.append(0)             # EnQueue
#    while(queue):
#        n = queue.pop(0)        # DeQueue
#        for (j,_)  in nodes[n].d_neighbor:
#            if not visited[j]:
#                visited[j] = 1
#                queue.append(j)
    
#def hop(G, i, n):
#    """ BFS max hop """
#    visited = [0] * n
#    queue = []
#    queue.append(i)
#    visited[i] = 1
#    hop = [0] * n
#    while(queue):
#        index = queue.pop(0)
#        neighbor = [j for j in range(n) if G[index][j]]
#        for k in neighbor:
#            if not visited[k]:
#                visited[k] = 1
#                hop[k] = hop[index] + 1   
#                queue.append(k)
#    m_h = max(hop)
#    a_h = np.mean(hop)
#    return (m_h, a_h)