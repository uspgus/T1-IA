import numpy as np
import networkx as nx

def gera_grafo(n, l):
    grafo = nx.Graph()
    np.random.seed(0)

    # Gera nós com coordenadas aleatórias em um plano de tamanho n x n
    vertices = np.random.rand(n, 2) * n
    grafo.add_nodes_from([(i, {'pos': vert}) for i, vert in enumerate(vertices)])

    # Adiciona arestas
    for i in range(n):
        for j in range(i + 1, n):  # Evita repetir pares e autoconexões
            distancia = np.linalg.norm(grafo.nodes[i]['pos'] - grafo.nodes[j]['pos'])  # Distância geométrica entre i e j

            # Calcula a probabilidade p = e^(-λsij)
            # sij - distância do nó i ao nó j
            p = np.exp(-l * distancia)

            # Adiciona aresta com base na probabilidade p
            if np.random.rand() < p:
                grafo.add_edge(i, j, weight=distancia)
    
    return grafo
