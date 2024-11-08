import numpy as np
import networkx as nx

def dist(grafo, a, b):
    return np.linalg.norm(grafo.nodes[a]['pos'] - grafo.nodes[b]['pos'])

def gera_grafo(n, l):
    grafo = nx.Graph()
    np.random.seed(0)

    #Gera Nós
    vertices = np.random.rand(n, 2)*n
    grafo.add_nodes_from([ (i, dict(pos=vert)) for i, vert in enumerate(vertices) ])

    #Gera Arestas
    for i in range(len(vertices)):
        for j in range(i):
            if (dist(grafo, i, j)*l < np.random.rand()):
                grafo.add_edge(i, j)

    return grafo

# grafo = gera_grafo(500, 0.011)

# Plotar o grafo
# nx.draw(grafo, nx.get_node_attributes(grafo, 'pos'), node_size=10)
