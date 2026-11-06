import networkx as nx


def adjacent_edges(nodes, halfk):
    """
    Yields edges between each node and `halfk` neighbors.
    halfk: number of edges from each node
    """
    n = len(nodes)
    for i, u in enumerate(nodes):
        for j in range(i + 1, i + halfk + 1):
            v = nodes[j % n]
            yield u, v


def make_ring_lattice(n, k):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(adjacent_edges(nodes, k // 2))
    return G


lattice = make_ring_lattice(10, 4)
