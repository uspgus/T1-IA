# Recebe dist_func, mas não usa, a função é definida assim apenas para poder padronizar a avaliação nos experimentos
def hill_climbing(grafo, inicio, fim, heuristica, dist_func):
    # Inicializa o nó atual com o nó de início.
    atual = inicio
    # Inicializa o caminho com o nó de início.
    caminho = []
    caminho.append(inicio)

    while True:
        # Se chegou ao destino retorna caminho
        if atual == fim:
            return caminho

        vizinhos = list(grafo.neighbors(atual))
        
        # Verifica se o nó atual não possui vizinhos (beco sem saida)
        if len(vizinhos) == 0:
            return None

        # Seleciona o vizinho com o menor valor heurístico em relação ao destino.
        melhor_vizinho = min(vizinhos, key=lambda x: heuristica(grafo, x, fim))
        
        # Verifica se o valor heurístico do melhor vizinho não é melhor do que o do nó atual.
        # Isso significa que não há como avançar para um nó que "aproxime mais" do destino.
        if heuristica(grafo, melhor_vizinho, fim) >= heuristica(grafo, atual, fim):
            return None
        
        # Adiciona o melhor vizinho ao caminho.
        caminho.append(melhor_vizinho)
        atual = melhor_vizinho
