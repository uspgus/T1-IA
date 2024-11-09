import numpy as np
from heapq import heappop, heappush

def a_estrela(grafo, inicio, fim, heuristica, dist_func):
    # Inicializa as distâncias para cada nó como infinito e o predecessor como -1
    dists = { no: np.inf for no in grafo.nodes }
    predecessor = { no: -1 for no in grafo.nodes }
    dists[inicio] = 0  # Define a distância do nó inicial como 0

    # Cria a fila de prioridade e insere o nó inicial com sua heurística
    fila_prioridade = []
    heappush(fila_prioridade, (heuristica(grafo, inicio, fim), inicio))

    while fila_prioridade:
        # Extrai o nó com a menor heurística + custo
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
                heuristica_f = dist_g + heuristica(grafo, vizinho, fim)
                heappush(fila_prioridade, (heuristica_f, vizinho))

    # Verifica se o caminho foi encontrado
    if predecessor[fim] == -1:
        return None

    # Reconstrói o caminho a partir do dicionário de predecessores
    caminho = []
    x = fim
    while x != inicio:
        caminho.append(x)
        x = predecessor[x]
    caminho.append(inicio)

    return caminho[::-1]  # Retorna o caminho na ordem correta

def a_estrela_countexp(grafo, inicio, fim, heuristica, dist_func):
    # Inicializa as distâncias para cada nó como infinito e o predecessor como -1
    dists = { no: np.inf for no in grafo.nodes }
    predecessor = { no: -1 for no in grafo.nodes }
    dists[inicio] = 0  # Define a distância do nó inicial como 0

    # Cria a fila de prioridade e insere o nó inicial com sua heurística
    fila_prioridade = []
    heappush(fila_prioridade, (heuristica(grafo, inicio, fim), inicio))

    # Contador de nós explorados
    explorados = 0

    while fila_prioridade:
        # Extrai o nó com a menor heurística + custo
        _, atual = heappop(fila_prioridade)
        
        explorados += 1  # Incrementa o contador de nós explorados

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
                heuristica_f = dist_g + heuristica(grafo, vizinho, fim)
                heappush(fila_prioridade, (heuristica_f, vizinho))

    # Verifica se o caminho foi encontrado
    if predecessor[fim] == -1:
        return None, explorados
    
    # Reconstrói o caminho a partir do dicionário de predecessores
    caminho = []
    x = fim
    while x != inicio:
        caminho.append(x)
        x = predecessor[x]
    caminho.append(inicio)

    return caminho[::-1], explorados  # Retorna o caminho na ordem correta e o número de nós explorados
