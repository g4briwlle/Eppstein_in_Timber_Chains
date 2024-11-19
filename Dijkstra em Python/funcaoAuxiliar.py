import networkx as nx
import pandas as pd
from IPython.display import display, clear_output
from time import sleep

def dijkstra_with_table(G, source):
    """
    Executa o algoritmo de Dijkstra mostrando o passo a passo em formato de tabela.
    
    Parâmetros:
    - G: Grafo (do NetworkX).
    - source: Nó de origem.
    """
    # Inicialização
    nodes = list(G.nodes())
    distances = {node: float('inf') for node in nodes}
    distances[source] = 0
    predecessors = {node: None for node in nodes}
    visited = []
    unvisited = nodes.copy()

    # Passo a passo
    while unvisited:
        # Escolher o nó não visitado com a menor distância
        current_node = min(unvisited, key=lambda node: distances[node])

        # Atualizar os vizinhos do nó atual
        for neighbor in G.neighbors(current_node):
            if neighbor in visited:
                continue
            new_distance = distances[current_node] + G[current_node][neighbor]['weight']
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node

        # Atualizar listas de visitados e não visitados
        visited.append(current_node)
        unvisited.remove(current_node)

        # Gerar tabela do estado atual
        table = {
            'Vértice': nodes,
            'Distância': [distances[node] for node in nodes],
            'Antecessor': [predecessors[node] for node in nodes],
            'Visitado': ['Sim' if node in visited else 'Não' for node in nodes]
        }
        df = pd.DataFrame(table)

        # Exibir o estado atual
        clear_output(wait=True)
        print(f"Nó Atual: {current_node}")
        display(df)
        sleep(1)