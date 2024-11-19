# main.py

import networkx as nx
import matplotlib.pyplot as plt
from funcaoAuxiliar import dijkstra_with_table  # Importar a função

# Criar o grafo direcionado
G = nx.DiGraph()
# Primeira entrada da tupla é o vértice de origem. A segunda entrada é o vértice de destino. A terceira é o peso da aresta.
edges = [('C1', 'F1', 1), ('C2', 'F1', 2), ('C2', 'F2', 1), ('C2', 'F3', 3), ('C3', 'F3', 2), ('E1', 'C1', 3), ('E3', 'C1', 4), ('C1', 'C2', 2), ('C3', 'C2', 1), ('E3', 'C2', 7), ('E2', 'C3', 4), ('E4', 'C3', 3), ('E3', 'C3', 2)]
G.add_weighted_edges_from(edges)

# Configurar os nós
licensed_forests = ['F1', 'F2', 'F3']
companies = ['C1', 'C2', 'C3']
end_consumers = ['E1', 'E2', 'E3', 'E4']

# Atribuir cores aos nós
node_colors = []
for node in G.nodes():
    if node in licensed_forests:
        node_colors.append('green')  # Florestas licenciadas
    elif node in companies:
        node_colors.append('blue')   # Companhias do setor
    elif node in end_consumers:
        node_colors.append('red')    # Consumidores finais

# Mostrar o grafo original
pos = nx.spring_layout(G, k=3, seed=42)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Florestas Licenciadas', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Companhias do Setor', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Consumidores Finais', markerfacecolor='red', markersize=10)
]
plt.legend(handles=legend_elements, loc='upper right')
plt.title("Grafo Original")
plt.show()

# Executar a visualização do algoritmo de Dijkstra
dijkstra_with_table(G, source='E3')