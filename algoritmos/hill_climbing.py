def hill_climbing(grafo, inicio, fim, heuristica):
    atual = inicio
    caminho = []
    caminho.append(inicio)

    while True:
        vizinho = grafo.neighbors(atual) 
        melhor_vizinho = min(vizinho, key=lambda x: heuristica(grafo, x, fim))
        if heuristica(grafo, melhor_vizinho, fim) >= heuristica(grafo, atual, fim):
            return caminho
        atual = melhor_vizinho 
        caminho.append(atual)