import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
from heapq import heappop, heappush

def heuristica(grafo, atual, fim):
    # Calcula a distância em "linha reta" (haversine) até o destino
	lat_1, lon_1 = grafo.nodes[atual]['y'], grafo.nodes[atual]['x']
	lat_2, lon_2 = grafo.nodes[fim]['y'], grafo.nodes[fim]['x']

	distancia = ox.distance.great_circle(lat_1, lon_1, lat_2, lon_2)
	
	# garante que a heuristica é otimista
	return 0.9 * distancia

def busca_best_first(grafo, inicio, fim):
    # Priority Queue para armazenar (distância estimada, nó atual, caminho percorrido)
    # python pq é min-heap por padrão
    fila_prioridade = []
    heappush(fila_prioridade, (0, inicio, [inicio]))
    
    visitados = set()
    
    while fila_prioridade:
        estimativa, atual, caminho = heappop(fila_prioridade)
        
        # Se o nó atual é o destino, retornar o caminho encontrado
        if atual == fim:
            comprimento_total = sum([grafo.get_edge_data(caminho[i], caminho[i+1], 0)['length'] for i in range(len(caminho)-1)])
            return caminho, comprimento_total
        
        if atual not in visitados:
            visitados.add(atual)
            
            # Explora os vizinhos do nó atual
            for vizinho in grafo.neighbors(atual):
                if vizinho not in visitados:
                    # best-first usa apenas h(n)
                    estimativa_vizinho = heuristica(grafo, vizinho, fim)
                    heappush(fila_prioridade, (estimativa_vizinho, vizinho, caminho + [vizinho]))
                    
    return None  # Retorna None se não encontrar o caminho

# Configuração inicial: cria o grafo das ruas de São Carlos
endereco = "R. Salomão Dibbo, 151"
grafo = ox.graph.graph_from_address(endereco, dist=500, network_type="walk")
nodes = grafo.number_of_nodes()

# Definindo nós de início e fim
inicio = 492900394  # Salomão Dibbo 151
fim = 330073747  # saída da matemática

# Executa a busca Best-First
t0 = time.time()
caminho, comprimento = busca_best_first(grafo, inicio, fim)
dt = time.time() - t0

print("Busca Best-First")
print("Número de nós:", nodes)
print(f"Tempo de execução: {dt:.4f} segundos")
print(f"Comprimento do caminho encontrado: {comprimento}")

# Exibe o caminho encontrado
if caminho:
    print("Caminho:", caminho)
    ox.plot_graph_route(grafo, caminho)
else:
    print("Caminho não encontrado.")

# Plota histograma das distâncias (caso haja múltiplos caminhos)
# Aqui adicionamos a análise caso existam múltiplos caminhos.
# Exemplo para fins de teste (pode ser ajustado para outros casos).

plt.figure()
plt.hist([comprimento], bins=10)  # Aqui, comprimento único para visualização simples
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Distância')
plt.ylabel('Frequência')
plt.title('Distância do caminho encontrado')
plt.show()
