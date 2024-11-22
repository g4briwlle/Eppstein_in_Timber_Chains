from graphviz import Digraph
from synthetic_data import *

# Criar a visualização com Graphviz
dot = Digraph(comment='Supply Chain Graph', format='png')

# Adicionar os nós ao grafo
for node, attrs in G.nodes(data=True):
    label = f"{node}\n({attrs['type']})"
    color = "green" if attrs['type'] == "forest" else "blue" if attrs['type'] == "company" else "red"
    dot.node(node, label=label, style="filled", fillcolor=color, fontcolor="white")

# Adicionar as arestas ao grafo
for u, v, attrs in G.edges(data=True):
    label = f"Vol: {attrs['weight']}"  # Apenas o volume
    dot.edge(u, v, label=label)

# Renderizar e visualizar o grafo
dot.render("supply_chain_graph", view=True)
