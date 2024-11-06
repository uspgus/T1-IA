import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

def busca_largura(grafo, inicio, fim):
    # Lista que atua como fila, armazenando o nó atual, o comprimento do caminho e o próprio caminho
    fila = [(inicio, 0, [inicio])]  # Cada item: (nó atual, comprimento do caminho, caminho)
    menor_comprimento = float('inf')
    caminhos = []
    
    while fila:
        # Remove o primeiro elemento da lista (como em uma fila)
        nodo_atual, comprimento_atual, caminho = fila.pop(0)

        # Se chegamos ao nó objetivo, verificamos o comprimento e atualizamos o menor comprimento
        if nodo_atual == fim:
            if comprimento_atual < menor_comprimento:
                menor_comprimento = comprimento_atual
            caminhos.append((caminho, comprimento_atual))
            continue

        # Explora os vizinhos do nó atual
        for vizinho in grafo.neighbors(nodo_atual):
            if vizinho not in caminho:  # Evita ciclos
                # Obter o comprimento da aresta atual
                comp_rua = grafo.get_edge_data(nodo_atual, vizinho, 0).get('length', 1)
                novo_comprimento = comprimento_atual + comp_rua
                fila.append((vizinho, novo_comprimento, caminho + [vizinho]))

    return caminhos, menor_comprimento

def busca_largura_melhorado(grafo, inicio, fim):
    # Lista que atua como fila, armazenando o nó atual, o comprimento do caminho e o próprio caminho
    fila = [(inicio, 0, [inicio])]  # Cada item: (nó atual, comprimento do caminho, caminho)
    menor_comprimento = float('inf')
    caminhos = []
    
    while fila:
        # Remove o primeiro elemento da lista (como em uma fila)
        nodo_atual, comprimento_atual, caminho = fila.pop(0)

        # Se chegamos ao nó objetivo, verificamos o comprimento e atualizamos o menor comprimento
        if nodo_atual == fim:
            if comprimento_atual < menor_comprimento:
                menor_comprimento = comprimento_atual
            caminhos.append((caminho, comprimento_atual))
            continue

        # Explora os vizinhos do nó atual
        for vizinho in grafo.neighbors(nodo_atual):
            if vizinho not in caminho:  # Evita ciclos
                # Obter o comprimento da aresta atual
                comp_rua = grafo.get_edge_data(nodo_atual, vizinho, 0).get('length', 1)
                novo_comprimento = comprimento_atual + comp_rua

                # Apenas prosseguir se o novo comprimento não exceder o menor comprimento conhecido
                if novo_comprimento <= menor_comprimento:
                    fila.append((vizinho, novo_comprimento, caminho + [vizinho]))

    # Filtra os caminhos para retornar apenas aqueles com o comprimento mínimo
    return caminhos, menor_comprimento


##Gera grafo das Ruas de São Carlos
endereco = "R. Salomão Dibbo, 151"

grafo = ox.graph.graph_from_address(endereco, dist=200, network_type="walk")

nodes = grafo.number_of_nodes()


inicio = 492900394 # Salomao dibbo 151
fim = 330073747 # saida da matematica


t0 = time.time()
caminhos,menor = busca_largura_melhorado(grafo, inicio, fim)
dt = time.time()-t0

print("Versao melhorada")
print("Número de nós:",nodes)
print(f"Tempo de execução: {dt}")
print(f"Numero de caminhos: {len(caminhos)}")

max_min = caminhos[:1] + caminhos[-1:]

#print(caminhos)
for i,caminho in enumerate(max_min):
    if i == 0:
        print(f"Comprimento caminho mínimo: {caminho[1]}")
    else:
        print(f"Comprimento caminho máximo: {caminho[1]}")
    print(caminho)
    ox.plot_graph_route(grafo, caminho[0])



#Plota histograma das distancias
dists = [caminho[1] for caminho in caminhos]

plt.figure()

plt.hist(dists, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Distancias')
plt.ylabel('Frequency')
#plt.xticks(fontsize=15)
#plt.yticks(fontsize=15)
plt.title('Histograma distancia dos caminhos')
plt.show()