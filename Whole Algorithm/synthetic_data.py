import os
import pickle
import networkx as nx
import random

def create_acyclic_flow_balanced_graph():
    G = nx.DiGraph()

    # Parâmetros ajustados
    num_forests = 4      # Número de florestas licenciadas
    num_companies = 10   # Número de empresas intermediárias
    num_consumers = 5    # Número de consumidores finais
    total_volume = 100   # Volume total inicial produzido pelas florestas

    # Gerar nós de florestas, empresas e consumidores
    forests = [f"Forest_{i}" for i in range(1, num_forests + 1)]
    companies = [f"Company_{i}" for i in range(1, num_companies + 1)]
    consumers = [f"Consumer_{i}" for i in range(1, num_consumers + 1)]

    # Adicionar nós ao grafo
    for forest in forests:
        G.add_node(forest, type="forest")
    for company in companies:
        G.add_node(company, type="company")
    for consumer in consumers:
        G.add_node(consumer, type="consumer")

    # Distribuir o volume total pelas florestas
    forest_volumes = {forest: total_volume // num_forests for forest in forests}

    # Criar arestas de florestas para empresas (garantindo aciclicidade)
    company_inflows = {company: 0 for company in companies}
    for forest in forests:
        volume = forest_volumes[forest]
        targets = random.sample(companies, random.randint(2, 3))  # Conectar a 2-3 empresas
        for target in targets:
            if volume > 0:
                allocated_volume = max(1, volume // len(targets))  # Garantir volume mínimo de 1
                G.add_edge(forest, target, weight=allocated_volume)
                volume -= allocated_volume
                company_inflows[target] += allocated_volume

    # Criar arestas de empresas para empresas e consumidores
    consumer_inflows = {consumer: 0 for consumer in consumers}
    for company in companies:
        max_outflow = company_inflows[company]
        if max_outflow > 0:
            # Conectar a outras empresas ou consumidores, garantindo aciclicidade
            targets = random.sample(companies + consumers, random.randint(2, 3))
            for target in targets:
                if target != company and not nx.has_path(G, target, company):  # Evitar ciclos
                    allocated_volume = max(1, max_outflow // len(targets))  # Garantir volume mínimo de 1
                    G.add_edge(company, target, weight=allocated_volume)
                    max_outflow -= allocated_volume
                    if target in consumers:
                        consumer_inflows[target] += allocated_volume

    # Ajustar volumes finais para balancear o fluxo total
    total_input = sum(forest_volumes.values())
    total_output = sum(consumer_inflows.values())
    assert total_input >= total_output, "O fluxo total não está balanceado!"

    # Garantir que o grafo seja acíclico
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("O grafo gerado não é acíclico! Algo deu errado na lógica de criação.")

    return G


# Caminho para salvar o grafo
graph_file_path = "balanced_supply_chain_graph.pkl"

# Função para salvar o grafo
def save_graph(graph, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(graph, f)
    print(f"Grafo salvo em: {file_path}")

# Função para carregar o grafo
def load_graph(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)


# Criar ou carregar o grafo
if os.path.exists(graph_file_path):
    print(f"Arquivo encontrado: {graph_file_path}. Carregando o grafo salvo...")
    G = load_graph(graph_file_path)
else:
    print(f"Arquivo não encontrado: {graph_file_path}. Criando um novo grafo...")
    G = create_acyclic_flow_balanced_graph()
    save_graph(G, graph_file_path)

if __name__ == "__main__":
    # Exibir informações do grafo
    print("Número de nós:", G.number_of_nodes())
    print("Número de arestas:", G.number_of_edges())

    # Opcional: Exibir as arestas do grafo
    print("\nArestas do grafo:")
    for u, v, data in G.edges(data=True):
        print(f"{u} -> {v}, Volume: {data['weight']}")
