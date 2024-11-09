import numpy as np
from heapq import heappop, heappush

def dijkstra(grafo, inicio, fim, heuristica, dist_func, return_dists=False):
    dists = { no:np.inf for no in grafo.nodes}
    predecessor = { no:-1 for no in grafo.nodes}
    dists[inicio] = 0

    fila_prioridade = []
    heappush(fila_prioridade, (0, inicio))

    while fila_prioridade:
        _, atual = heappop(fila_prioridade)

        if atual == fim:
            break

        for vizinho in grafo.neighbors(atual):
            dist_g = dists[atual] + dist_func(grafo, atual, vizinho)
            
            if dist_g < dists[vizinho]:
                predecessor[vizinho] = atual
                dists[vizinho] = dist_g
                heappush(fila_prioridade, (dist_g, vizinho))

    if(predecessor[fim] == -1):
        if return_dists:
            return None, dists
        else:
            return None

    # Construir caminho a partir do dicionário de predecessores
    caminho = []
    x = fim
    while x != inicio:
        caminho.append(x)
        x = predecessor[x]
    caminho.append(inicio)

    if return_dists:
        return caminho[::-1], dists
    else:
        return caminho[::-1]