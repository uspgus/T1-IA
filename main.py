# Master file

# Gustavo Ferreira, Murilo Zabott, João Pedro Farjoun, Tomás Ribeiro
# 2nd Semester 2024
# University of São Paulo, Institute of Mathematical and Computer Science

import warnings
warnings.simplefilter("ignore", category=FutureWarning) # evitar avisos dos modulos como matplotlibe e osmnx

from algoritmos import a_estrela, best_first, hill_climbing, busca_largura, busca_profundidade
from geracao import geracacao_osm, geracao_custom
from heuristicas import heuristica_osm, heuristica_custom

import os
import time
import matplotlib.pyplot as plt
import osmnx as ox
import numpy as np
import networkx as nx

# Para o experimento I usamos uma rede do dataset do OpenStreetMap (biblioteca osmnx)
# a fim de deixar a visualização dos caminhos mais interessante
def experimento_1():
    grafo = geracacao_osm.gera_grafo()
    
    # OpenStreetMap usa ids fixos para identificar nós
    # Define nós de inicio e fim
    inicio = 505829905
    fim = 330073747  # Saída da matemática

    # Configurações quanto à salvar ou exibir caminhos
    show_plot=False
    save_plot=True
    
    funcoes_busca = [a_estrela, best_first, hill_climbing, busca_largura, busca_profundidade]

    # definindo uma função distância para poder calcular g(n) no algoritmo A*
    # grafo[x][y] retorna atributos da aresta (x,y), length é a distância entre os nós (vêm direto do OSM)
    dist_func = lambda grafo, a, b : grafo[a][b][0]['length']
    
    fig_comps, axs = plt.subplots(figsize=(8, 5)) # Figura pro gráfico dos comprimentos

    os.makedirs("./resultados/experimento_1", exist_ok=True)

    for alg in funcoes_busca:
        # Pra simplificar a chamada, todas as funções recebem a heuristica e função de distância (pra calcular g(n))
        # Mas só as que precisam desses argumentos de fato os usam
        caminho = alg(grafo, inicio, fim, heuristica_osm, dist_func)

        if caminho:
            # Exibir/Salvar visualização dos caminhos e plotar o comprimento
            ox.plot_graph_route(grafo, caminho, show=show_plot, save=save_plot, filepath=f"./resultados/experimento_1/{alg.__name__}.png")
            comprimento = sum([dist_func(grafo, caminho[i], caminho[i+1]) for i in range(len(caminho)-1)])
            axs.bar(alg.__name__, comprimento, width=0.4)

        else:
            print(f"Caminho não encontrado para algoritmo: {alg.__name__}")

    # Salvar figura do comprimento dos caminhos
    axs.set_title('Comprimento dos caminhos por algoritmo')
    axs.set_ylabel('Comprimento do caminho (m)')
    fig_comps.tight_layout()
    fig_comps.savefig(fname="./resultados/experimento_1/comprimentos.png")

def experimento_2():
    parametros_grafos = [(2000, 0.01), (2000, 0.02), (2000, 0.03)]
    funcoes_busca = [a_estrela, best_first, hill_climbing, busca_largura, busca_profundidade]
    nomes_algoritmos = ['A*', 'Best-First', 'Hill Climbing', 'Largura', 'Profundidade']

    # Gerar os grafos
    grafos = [geracao_custom.gera_grafo(n, l) for n, l in parametros_grafos]

    # Selecionar 10 pares de vértices distintos
    np.random.seed(0)
    pares_vertices = [tuple(np.random.choice(2000, 2, replace=False)) for _ in range(100)]

    # Resultados de distância e tempo
    resultados_distancia = {nome: [] for nome in nomes_algoritmos}
    resultados_tempo = {nome: [] for nome in nomes_algoritmos}
    resultados_ncaminhos = {nome: [] for nome in nomes_algoritmos}

    # função distância para o g(n) no A*
    dist_func = lambda grafo, a, b: grafo[a][b]['weight']

    # Avaliar os algoritmos nos grafos
    for grafo in grafos:
        for func, nome in zip(funcoes_busca, nomes_algoritmos):
            distancias = []
            tempos = []
            n_caminhos_completos = 0
            for origem, destino in pares_vertices:
                inicio = time.time()
                caminho = func(grafo, origem, destino, heuristica_custom, dist_func)
                fim = time.time()

                if caminho and caminho[-1]==destino:
                    distancia = sum(grafo[u][v]['weight'] for u, v in zip(caminho[:-1], caminho[1:]))
                    distancias.append(distancia)
                    n_caminhos_completos += 1
                tempos.append(fim - inicio)

            # Média das distâncias e tempos
            resultados_distancia[nome].append(np.mean(distancias) if distancias else 0)
            resultados_tempo[nome].append(np.mean(tempos))
            resultados_ncaminhos[nome].append(n_caminhos_completos)

    # Plotar os gráficos
    fig, axes = plt.subplots(3, 1, figsize=(14, 14))
    x = np.arange(len(nomes_algoritmos))
    largura = 0.25
    
    for i, label in enumerate(['λ=0.01', 'λ=0.02', 'λ=0.03']):
        axes[0].bar(x + i * largura, [resultados_distancia[nome][i] for nome in nomes_algoritmos], width=largura, label=label)

    axes[0].set_title('Distância Média dos Caminhos')
    axes[0].set_xticks(x + largura, nomes_algoritmos)
    axes[0].set_ylabel('Distância Média (m)')
    axes[0].legend(loc='upper left', ncols=3)
    axes[0].set_yscale("log")

    # Gráfico de tempos
    for i, label in enumerate(['λ=0.01', 'λ=0.02', 'λ=0.03']):
        axes[1].bar(x + i * largura, [resultados_tempo[nome][i] for nome in nomes_algoritmos], width=largura, label=label)

    axes[1].set_title('Tempo Médio de Execução')
    axes[1].set_xticks(x + largura, nomes_algoritmos)
    axes[1].set_ylabel('Tempo (s)')
    axes[1].legend(loc='upper left', ncols=3)
    axes[1].set_yscale("log")

    # Gráfico de n_caminhos
    for i, label in enumerate(['λ=0.01', 'λ=0.02', 'λ=0.03']):
        axes[2].bar(x + i * largura, [resultados_ncaminhos[nome][i] for nome in nomes_algoritmos], width=largura, label=label)

    # Para fazer caber a legenda sem sobreposição com o gráfico    
    y_min, y_max = axes[2].get_ylim()
    axes[2].set_ylim(y_min, y_max*1.1)

    axes[2].set_title('Número de caminhos completos encontrados')
    axes[2].set_xticks(x + largura, nomes_algoritmos)
    axes[2].set_ylabel('Número de caminhos')
    axes[2].legend(loc='upper left', ncols=3)

    fig.tight_layout()
    os.makedirs("./resultados/experimento_2", exist_ok=True)
    fig.savefig(fname="./resultados/experimento_2/metricas.png")


def experimento_3():
    # Comparar A* com Dijkstra
    return 1

if __name__ == "__main__":
    experimento_1()
    experimento_2()
    # experimento_3()