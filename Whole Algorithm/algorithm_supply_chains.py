import networkx as nx

def k_most_likely_supply_chains(G, v_inicial, k):
    """
    Calcula as k cadeias de suprimento mais prováveis para o nó v.

    Parâmetros:
        G: Grafo dirigido ponderado (networkx.DiGraph)
        v: Nó de destino (pertencente a Vc ou Ve)
        k: Número de cadeias desejadas

    Retorna:
        Lista das k cadeias mais prováveis (caminho e volume total).
    """

    v = v_inicial

    # Identificar os nós que representam florestas (ajuste conforme necessário)
    forests = {node for node in G.nodes if node.startswith("Forest")}

    # Passo 1: Inverter as arestas e transformar os pesos (volumes) em negativos
    G_reversed = G.reverse(copy=True)
    for u, w, data in G_reversed.edges(data=True):
        data['weight'] = -data['weight']  # Transformar volumes em negativos

    # Passo 2: Usar Bellman-Ford para encontrar os caminhos mais curtos (em termos de peso negativo,
    # porque a função em python de Dijkstra não funcionaria)
    try:
        lengths, paths = nx.single_source_bellman_ford(G_reversed, v, weight='weight')
    except nx.NetworkXUnbounded:
        raise ValueError("O grafo contém ciclos negativos, o que não é permitido!")

    # Depuração: Exibir os caminhos encontrados no grafo invertido
    """    print("\nCaminhos encontrados no grafo invertido:")
    for dest, path in paths.items():
        print(f"Destino: {dest}, Caminho: {path}")"""

    # Ordenar os caminhos pelo volume negativo (menor peso primeiro)
    paths_sorted = sorted(
        paths.items(),
        key=lambda x: sum(G_reversed[u][v]['weight'] for u, v in zip(x[1], x[1][1:]))
    )

    # Ajustar k caso o número de caminhos seja menor que k
    k = min(k, len(paths_sorted))

    # Inicializar variáveis para armazenar os caminhos mais prováveis
    result_chains = []
    count = 0

    # Adicionar os primeiros k caminhos ordenados
    for i in range(k):
        chain = paths_sorted[i][1]
        result_chains.append(chain)
        count += 1

    # Passo 4: Reverter os volumes para valores positivos e calcular o volume total
    final_chains = []
    for chain in result_chains:
        try:
            # Ignorar caminhos com apenas um nó (não são válidos)
            if len(chain) <= 1:
                continue

            # Verificar se o último nó é uma floresta
            if chain[-1] not in forests:
                continue

            # Verificar as arestas no grafo original (re-inverter direção das arestas)
            volume = 0
            valid_chain = True
            for v, u in zip(chain[:-1], chain[1:]):  # Re-inverter direção para G original
                if not G.has_edge(u, v):  # Verificar na direção correta no grafo original
                    print(f"Aresta ausente no grafo original: ({u}, {v}) no caminho {chain}")
                    valid_chain = False
                    break
                # Somar o peso da aresta diretamente (valores positivos no grafo original)
                volume += G[u][v].get('weight', 0)  # Usar peso original, já positivo

            if valid_chain:
                final_chains.append((chain, volume))
        except KeyError as e:
            print(f"Erro ao acessar peso de aresta no caminho: {chain}. Detalhes: {e}")
            continue

    # Depuração final
    if not final_chains:
        print("\nNenhum caminho válido foi encontrado no grafo original!")

    return print(f"Exibindo as {k} supply chains mais prováveis de {v_inicial} em {G}:", final_chains, sep="\n")

