import graph_random_d


def reachable_nodes_precheck(G, start):
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            neighbors = set(G[node]) - seen
            stack.extend(neighbors)
    return seen


complete = graph_random_d.make_complete_digraph(100)

# %timeit len(reachable_nodes(complete, 0))
# 1.32 ms ± 53.9 μs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# %timeit len(reachable_nodes_precheck(complete, 0))
# 867 μs ± 15.3 μs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
