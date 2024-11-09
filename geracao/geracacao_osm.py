import osmnx as ox

# Usa a biblioteca de grafos do OpenStreetMap para gerar um grafo que representa a região perto da saída da matemática
def gera_grafo(dist=500):
    endereco = "R. Salomão Dibbo, 151"
    grafo = ox.graph.graph_from_address(endereco, dist=dist, network_type="walk")
    return grafo