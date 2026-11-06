import networkx as nx

from .path_ring import make_ring_lattice


def shortest_path_dijkstra(G, source):
    """A fast version of Dijkstra's algorithm for equal edges."""
    new_dist = 0
    dist = {}
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in dist:
                dist[v] = new_dist
                nextlevel.update(G[v])
        new_dist += 1
    return dist


lattice = make_ring_lattice(10, 4)
d1 = shortest_path_dijkstra(lattice, 0)
print(d1)
# {0: 0, 8: 1, 1: 1, 2: 1, 9: 1, 6: 2, 7: 2, 3: 2, 4: 2, 5: 3}
d2 = nx.shortest_path_length(lattice, 0)
print(d2)
# {0: 0, 8: 1, 1: 1, 2: 1, 9: 1, 6: 2, 7: 2, 3: 2, 4: 2, 5: 3}
# %timeit shortest_path_dijkstra(lattice, 0)
# 1.51 ms ± 9.93 μs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# %timeit nx.shortest_path_length(lattice, 0)
# 3.7 ms ± 49.2 μs per loop (mean ± std. dev. of 7 runs, 100 loops each)
