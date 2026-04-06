import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def rewire(G, p):
    nodes = set(G)
    rng = np.random.default_rng(42)
    for u, v in G.edges():
        if rng.random() < p:
            choices = nodes - {u} - set(G[u])
            new_v = rng.choice(list(choices))
            G.remove_edge(u, v)
            G.add_edge(u, new_v)


def draw(g, node_size=800, font_size=16):
    nx.draw(
        g,
        with_labels=True,
        pos=nx.circular_layout(g),
        node_color="red",
        node_size=node_size,
        font_color="white",
        font_size=font_size,
        font_weight="bold",
    )


n = 10
k = 4
ps = [0, 0.2, 1.0]

_, axes = plt.subplots(1, 3, figsize=(12, 6), constrained_layout=True)

for p, ax in zip(ps, axes.flatten()):
    g = nx.random_graphs.watts_strogatz_graph(n, k, p)
    draw(g, node_size=200, font_size=12)
    ax.axis("equal")

plt.show()
