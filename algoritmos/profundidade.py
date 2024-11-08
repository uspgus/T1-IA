def busca_profundidade(grafo, inicio, fim, heuristica, dist_func):
    pilha = [(inicio, [inicio])]
    processados = set()

    while pilha:
        atual, caminho = pilha.pop()

        if atual == fim:
            return caminho
        
        if atual not in processados:
            processados.add(atual)

            for vizinho in grafo.neighbors(atual):
                if vizinho not in processados:
                    pilha.append((vizinho, caminho + [vizinho]))

    return None