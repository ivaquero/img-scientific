from .path_ring import make_ring_lattice

# 该版本复杂度为 O(n + m)


def reachable_nodes_bfs(G, start):
    seen = set()
    nextlevel = {start}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(G[v])
    return seen


lattice = make_ring_lattice(10, 4)
reachable_nodes_bfs(lattice, 0)  # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
