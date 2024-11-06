import numpy as np
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

def busca_largura(grafo, inicio, fim):
    caminhos = []
    busca_largura_rec(grafo, inicio, fim, caminhos)
    caminhos.sort(key=lambda t: t[1])
    return caminhos


def busca_largura_rec(grafo, inicio, fim, caminhos, comprimento=0, caminho=[]):
    comp_rua = grafo.get_edge_data(caminho[-1], inicio, 0)['length'] if (caminho) else 0

    if inicio == fim:
        caminhos.append((caminho + [inicio], comprimento + comp_rua))
        return

    fila = [(vizinho) for vizinho in grafo.neighbors(inicio) if vizinho not in caminho]
    
    for vizinho in fila:
        busca_largura_rec(grafo, vizinho, fim, caminhos, comprimento + comp_rua, caminho + [inicio])

    return

##Ignora caminhos piores q o melhor já encontrado

def busca_largura_melhorado(grafo, inicio, fim):
    caminhos = []
    busca_largura_rec_melhorado(grafo, inicio, fim, caminhos)
    caminhos.sort(key=lambda t: t[1])
    return caminhos

def busca_largura_rec_melhorado(grafo, inicio, fim, caminhos, menor_comprimento=1_000_000, comprimento=0, caminho=[]):
    comp_rua = grafo.get_edge_data(caminho[-1], inicio, 0)['length'] if caminho else 0

    if comprimento + comp_rua > menor_comprimento:
        return menor_comprimento

    if inicio == fim:
        if comprimento + comp_rua < menor_comprimento:
            menor_comprimento = comprimento + comp_rua
        caminhos.append((caminho + [inicio], comprimento + comp_rua))
        return menor_comprimento

    fila = [(vizinho, comprimento + comp_rua, caminho + [inicio]) for vizinho in grafo.neighbors(inicio) if vizinho not in caminho]
    
    for (vizinho, novo_comprimento, novo_caminho) in fila:
        menor_comprimento = busca_largura_rec_melhorado(grafo, vizinho, fim, caminhos, menor_comprimento, novo_comprimento, novo_caminho)

    return menor_comprimento

##Gera grafo das Ruas de São Carlos
endereco = "R. Salomão Dibbo, 151"

grafo = ox.graph.graph_from_address(endereco, dist=200, network_type="walk")

nodes = grafo.number_of_nodes()


inicio = 492900394 # Salomao dibbo 151
fim = 330073747 # saida da matematica


t0 = time.time()
caminhos = busca_largura(grafo, inicio, fim)
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