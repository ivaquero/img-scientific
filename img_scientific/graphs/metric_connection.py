import graph_random
import graph_random_d
import numpy as np


def reachable_nodes(G, start, directed=False):
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            if directed:
                stack.extend(G.successors(node))
            else:
                stack.extend(G.neighbors(node))
    return seen


def is_connected(G):
    start = next(iter(G))
    reachable = reachable_nodes(G, start)
    return len(reachable) == len(G)


def is_connected_digraph(G):
    for start in G:
        reachable = reachable_nodes(G, start, directed=True)
        if len(reachable) < len(G):
            return False
    return True


reachable_nodes(graph_random.random_graph, 0)  # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
is_connected(graph_random.random_graph)  # False

complete_digraph = graph_random_d.make_complete_digraph(5)
is_connected_digraph(complete_digraph)  # True

# p 的临界值
n = 10
p_crt = np.log(n) / n  # 0.23025850929940458


# 生成 iters 个随机图
def prob_connected(G, iters=100):
    tf = [is_connected(G) for _ in range(iters)]
    return np.mean(tf)


np.random.default_rng(17)
prob_connected(n, iters=10000)  # 0.3407
