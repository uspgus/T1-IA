def hill_climbing(grafo, inicio, fim, heuristica, dist_func):
    atual = inicio
    caminho = []
    caminho.append(inicio)

    while True:
        vizinhos = list(grafo.neighbors(atual))
        
        if len(vizinhos)==0:
            return caminho
        
        melhor_vizinho = min(vizinhos, key=lambda x: heuristica(grafo, x, fim))
        
        if heuristica(grafo, melhor_vizinho, fim) >= heuristica(grafo, atual, fim):
            return caminho
        
        atual = melhor_vizinho 
        caminho.append(atual)