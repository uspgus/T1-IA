import osmnx as ox

def gera_grafo(dist=500):
    endereco = "R. Salomão Dibbo, 151"
    grafo = ox.graph.graph_from_address(endereco, dist=dist, network_type="walk")
    return grafo