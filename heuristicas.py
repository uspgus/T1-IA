import numpy as np
import osmnx as ox

def heuristica_custom(grafo, a, b):
	return 0.9 * np.linalg.norm(grafo.nodes[a]['pos'] - grafo.nodes[b]['pos'])

def heuristica_osm(grafo, a, b):
    # Calcula a distância em "linha reta" (haversine) até o destino
	lat_1, lon_1 = grafo.nodes[a]['y'], grafo.nodes[a]['x']
	lat_2, lon_2 = grafo.nodes[b]['y'], grafo.nodes[b]['x']

	distancia = ox.distance.great_circle(lat_1, lon_1, lat_2, lon_2)
	
	# garante que a heuristica é otimista
	return 0.9 * distancia