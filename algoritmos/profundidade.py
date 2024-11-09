# Recebe dist_func e heuristica, mas não usa, a função é definida assim apenas para poder padronizar a avaliação nos experimentos
def busca_profundidade(grafo, inicio, fim, heuristica, dist_func):
    # Inicializa a pilha com a tupla (nó inicial, caminho percorrido até agora).
    pilha = [(inicio, [inicio])]
    # Cria um conjunto para manter o registro dos nós já processados.
    processados = set()

    while pilha:
        # Retira o último elemento da pilha (comportamento LIFO).
        atual, caminho = pilha.pop()

        # Verifica se o nó atual é o destino procurado.
        if atual == fim:
            return caminho 

        # Evita reprocessamento de nós
        if atual not in processados:
            processados.add(atual)

            # Itera sobre os vizinhos do nó atual.
            for vizinho in grafo.neighbors(atual):
                if vizinho not in processados:
                    # Adiciona o vizinho à pilha com o caminho atualizado.
                    pilha.append((vizinho, caminho + [vizinho]))

    # Retorna None caso não encontre um caminho até o destino.
    return None
