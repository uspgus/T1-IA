import numpy as np
from heapq import heappop, heappush

# Recebe heuristica, mas não usa, a função é definida assim apenas para poder padronizar a avaliação nos experimentos
def dijkstra(grafo, inicio, fim, heuristica, dist_func, return_dists=False):
    # Inicializa as distâncias para cada nó como infinito e o predecessor como -1
    # Faz isso pois o algoritmo vai "relaxando as distâncias"
    dists = { no:np.inf for no in grafo.nodes}
    predecessor = { no:-1 for no in grafo.nodes}
    dists[inicio] = 0

    # Cria a fila de prioridade e insere o nó inicial
    fila_prioridade = []
    heappush(fila_prioridade, (0, inicio))

    while fila_prioridade:
        # Extrai o nó com o menor custo
        _, atual = heappop(fila_prioridade)

        # Verifica se chegou ao nó final
        if atual == fim:
            break
        
        # Explora os vizinhos do nó atual
        for vizinho in grafo.neighbors(atual):
            # Calcula a nova distância para o vizinho
            dist_g = dists[atual] + dist_func(grafo, atual, vizinho)
            
            # Se a nova distância for menor, atualiza as estruturas de dados
            if dist_g < dists[vizinho]:
                predecessor[vizinho] = atual
                dists[vizinho] = dist_g
                heappush(fila_prioridade, (dist_g, vizinho))

    # Verifica se encontrou um caminho
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