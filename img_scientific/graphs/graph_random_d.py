import matplotlib.pyplot as plt
import networkx as nx


def all_pairs_directed(nodes):
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i != j:
                yield u, v


def make_complete_digraph(n):
    G = nx.DiGraph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(all_pairs_directed(nodes))
    return G


complete_digraph = make_complete_digraph(5)

nx.draw_circular(complete_digraph, node_color="C2", node_size=1000, with_labels=True)
plt.show()
