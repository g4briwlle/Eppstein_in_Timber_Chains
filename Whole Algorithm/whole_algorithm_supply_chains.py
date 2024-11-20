import networkx as nx

def k_most_likely_supply_chains(G, v, k):
    """
    Calcula as k cadeias de suprimento mais prováveis para o nó v.

    Parâmetros:
        G: Grafo dirigido ponderado (networkx.DiGraph)
        v: Nó de destino (pertencente a Vc ou Ve)
        k: Número de cadeias desejadas

    Retorna:
        C: Lista das k cadeias mais prováveis
    """

    # Inverter arestas e transformar pesos (volumes) em negativos
    G_reversed = G.reverse(copy=True)
    for u, w, data in G_reversed.edges(data=True):
        data['weight'] = -data['weight']

    # Aplicar Dijkstra para encontrar os caminhos mais curtos de v para todos os nós
    C = nx.single_source_dijkstra_path(G_reversed, v)
    
    # Ordenar as cadeias por volume negativo (menor peso primeiro)
    C = sorted(C.items(), key=lambda x: sum(G_reversed[u][v]['weight'] for u, v in zip(x[1], x[1][1:])))

    # Ajustar o valor de k caso necessário
    k = min(k, len(C))

    # Inicializar variáveis
    count = 0
    result_chains = []
    i = 0

    # Loop principal para encontrar as k cadeias
    while count < k:
        result_chains.append(C[i][1])  # Adicionar cadeia mais provável
        count += 1
        i += 1

        # Aplicar o algoritmo de Eppstein para encontrar as k cadeias mais curtas adicionais
        P = nx.shortest_simple_paths(G_reversed, source=C[i-1][1][0], target=C[i-1][1][-1])
        P = list(P)[:k]  # Limitar a k caminhos
        P = sorted(P, key=lambda path: sum(G_reversed[u][v]['weight'] for u, v in zip(path, path[1:])))

        # Comparar os volumes das novas cadeias com os já encontrados
        j = 1
        while j < len(P) and count < k:
            sigma_pj = sum(G_reversed[u][v]['weight'] for u, v in zip(P[j], P[j][1:]))
            sigma_ci = sum(G_reversed[u][v]['weight'] for u, v in zip(C[i][1], C[i][1][1:]))
            
            if sigma_pj < sigma_ci:  # Comparar volumes
                result_chains.append(P[j])  # Adicionar nova cadeia
                count += 1
            j += 1

    # Reverter volumes para valores positivos
    final_chains = []
    for chain in result_chains:
        volume = sum(-G[u][v]['weight'] for u, v in zip(chain, chain[1:]))
        final_chains.append((chain, volume))

    return final_chains
