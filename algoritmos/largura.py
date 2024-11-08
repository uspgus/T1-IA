def busca_largura(grafo, inicio, fim):
    # Lista que atua como fila, a agenda do algoritmo, armazenando o nó atual e o próprio caminho
    fila = [(inicio, [inicio])]  # Cada item: (nó atual, comprimento do caminho, caminho)
    
    # Armazena itens que já foram agendados ou processados, para evitar reprocessamento
    agendados = set([inicio])

    while fila:
        # Remove o primeiro elemento da lista (como em uma fila)
        atual, caminho = fila.pop(0)

        # Se chegamos ao nó objetivo, verificamos o comprimento e atualizamos o menor comprimento
        if atual == fim:
            return caminho

        # Explora os vizinhos do nó atual
        for vizinho in grafo.neighbors(atual):
            # Evita reprocessamento de nós
            if vizinho not in agendados: 
                fila.append((vizinho, caminho + [vizinho]))
                agendados.add(vizinho)

    return None