import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .metric_clustering import clustering_coefficient
from .path_shortest import characteristic_path_length


def run_one_graph(n, k, p):
    ws = nx.watts_strogatz_graph(n, k, p)
    mpl = characteristic_path_length(ws)
    cc = clustering_coefficient(ws)
    # tuple of (mean path length, clustering coefficient)
    return mpl, cc


ps = np.logspace(-4, 0, 9)


def run_experiment(ps, n=1000, k=10, iters=20):
    res = []
    for p in ps:
        print(p)
        t = [run_one_graph(n, k, p) for _ in range(iters)]
        means = np.array(t).mean(axis=0)
        print(means)
        res.append(means)
    return np.array(res)


res = run_experiment(ps)
L, C = np.transpose(res)
L /= L[0]
C /= C[0]

_, ax = plt.subplots()

ax.plot(ps, C, "s-", lw=1, label="C(p) / C(0)")
ax.plot(ps, L, "o-", lw=1, label="L(p) / L(0)")
ax.set(
    xlabel="Rewiring probability (p)",
    xscale="log",
    title="Normalized clustering coefficient and path length",
    xlim=(0.00009, 1.1),
    ylim=(-0.01, 1.01),
)
plt.show()
