# Master file

# Gustavo Ferreira, Murilo Zabott, João Pedro Farjoun, Tomás Ribeiro
# 2nd Semester 2024
# University of São Paulo, Institute of Mathematical and Computer Science

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

from algoritmos import a_estrela, best_first, hill_climbing, busca_largura, busca_profundidade
from geracao import geracacao_osm, geracao_custom
from heuristicas import heuristica_osm, heuristica_custom

import time
import matplotlib.pyplot as plt
import osmnx as ox

def experimento_1():
    grafo = geracacao_osm.gera_grafo()
    
    # OpenStreetMap usa ids fixos para identificar nós
    # Define nós de inicio e fim
    inicio = 492900394  # Salomão Dibbo 151
    fim = 330073747  # Saída da matemática

    # Configurações quanto à exibição dos caminhos
    show_plot=False # Define se exibe os plots na execução do programa
    save_plot=True # Define se salva as figuras de plot dos caminhos nos arquivos em /resultados
    
    # Definindo uma lista das funções de busca e a função distância para o algoritmo A* e calcular o comprimento do caminho
    funcoes_busca = [a_estrela, best_first, hill_climbing, busca_largura, busca_profundidade]

    # grafo[x][y] retorna atributos da aresta (x,y), length é a distância entre os nós (vêm direto do OSM)
    dist_func = lambda grafo, a, b : grafo[a][b][0]['length']
    
    for alg in funcoes_busca:
        # Algoritmo a_estrela precisa de um parâmetro a mais, função pra calcular g(n)
        if alg == a_estrela:
            caminho = alg(grafo, inicio, fim, heuristica_osm, dist_func)
        # bfs e dfs não precisam de heurística
        elif alg == busca_largura or alg == busca_profundidade:
            caminho = alg(grafo, inicio, fim)
        else:
            caminho = alg(grafo, inicio, fim, heuristica_osm)

        if caminho:
            ox.plot_graph_route(grafo, caminho, show=show_plot, save=save_plot, filepath=f"./resultados/experimento_1/{alg.__name__}.png")
            comprimento = sum([dist_func(grafo, caminho[i], caminho[i+1]) for i in range(len(caminho)-1)])
        else:
            print(f"Caminho não encontrado para algoritmo: {alg.__name__}")

def experimento_2():
    # grafo = geracao_custom.gera_grafo()
    
    # t0 = time.time()
    # caminho, comprimento = busca_best_first(grafo, inicio, fim)
    # dt = time.time() - t0

    # print("Busca Best-First")
    # print("Número de nós:", nodes)
    # print(f"Tempo de execução: {dt:.4f} segundos")
    # print(f"Comprimento do caminho encontrado: {comprimento}")

    # plt.figure()
    # plt.hist([comprimento], bins=10)  # Aqui, comprimento único para visualização simples
    # plt.grid(axis='y', alpha=0.75)
    # plt.xlabel('Distância')
    # plt.ylabel('Frequência')
    # plt.title('Distância do caminho encontrado')
    # plt.show()

    return 1


def experimento_3():
    # Comparar A* com Dijkstra
    return 1

if __name__ == "__main__":
    experimento_1()
    # experimento_2()
    # experimento_3()