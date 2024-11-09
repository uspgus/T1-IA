from heapq import heappop, heappush

# Recebe dist_func, mas não usa, a função é definida assim apenas para poder padronizar a avaliação nos experimentos
def best_first(grafo, inicio, fim, heuristica, dist_func):
    # Fila de prioridade para armazenar (f(n) = h(n), nó head, caminho percorrido)
    # Heap Queue do Python é min_heap por padrão, ótimo pois buscamos sempre a menor f(n)
    fila_prioridade = []
    heappush(fila_prioridade, (0, inicio, [inicio]))
    
    # Armazena nós que já foram processados (nó teve seus vizinhos adicionados na fila de prioridade)
    # Evita reprocessamento e ciclos
    processados = set()
    
    while fila_prioridade:
        _, atual, caminho = heappop(fila_prioridade)
        
        # Se o nó atual é o destino, retornar o caminho encontrado
        if atual == fim:
            return caminho
        
        if atual not in processados:
            processados.add(atual)
            
            # Explora os vizinhos do nó atual
            for vizinho in grafo.neighbors(atual):
                if vizinho not in processados:
                    # best-first usa apenas h(n)
                    estimativa_vizinho = heuristica(grafo, vizinho, fim)
                    heappush(fila_prioridade, (estimativa_vizinho, vizinho, caminho + [vizinho]))
                    
    return None  # Retorna None se não encontrar o caminho