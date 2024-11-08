import numpy as np
from heapq import heappop, heappush

def a_estrela(grafo, inicio, fim, heuristica, dist_func):
    dists = { no:np.inf for no in grafo.nodes}
    predecessor = { no:-1 for no in grafo.nodes}
    dists[inicio] = 0

    fila_prioridade = []
    heappush(fila_prioridade, (heuristica(grafo, inicio, fim), inicio))

    while fila_prioridade:
        _, atual = heappop(fila_prioridade)

        if atual == fim:
            break

        for vizinho in grafo.neighbors(atual):
            dist_g = dists[atual] + dist_func(grafo, atual, vizinho)
            
            if dist_g < dists[vizinho]:
                predecessor[vizinho] = atual
                dists[vizinho] = dist_g
                heuristica_f = dist_g + heuristica(grafo, atual, fim)
                heappush(fila_prioridade, (heuristica_f, vizinho))

    if(predecessor[fim] == -1):
        return None

    # Construir caminho a partir do dicionário de predecessores
    caminho = []
    x = fim
    while x != inicio:
        caminho.append(x)
        x = predecessor[x]
    caminho.append(inicio)

    return caminho[::-1]