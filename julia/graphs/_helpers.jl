"""
_helpers.jl -- graph/network construction + metric helpers for the graphs topic.

Mirrors the Python algorithms in ``img_scientific/graphs/`` (path_ring,
graph_random, metric_clustering, path_shortest). Design note for the Makie
ecosystem: GraphMakie's ``graphplot`` needs a *real* ``Graphs.jl`` object for
drawing, but that object only exposes ``nv``/``edges`` (not a fast neighbour
index). So we keep the graph structure in a plain ``adjacency`` list (1-indexed,
``Vector{Vector{Int}}``) that every metric runs on -- this is pure Base, so the
offline stub harness exercises the algorithms for real -- and build a thin
``SimpleGraph`` in parallel purely to hand to ``graphplot``.

``adjacent_edges`` / ``make_ring_lattice`` reproduce the Python ring lattice
exactly, and ``watts_strogatz`` follows Watts & Strogatz (1998) with a seeded
RNG (the Python ``nx.watts_strogatz_graph`` is unseedable, so both sides use our
own builder for reproducibility).
"""

using Graphs
using GraphMakie

# --- edge enumeration (nodes are 1..n) ---------------------------------------

"""Ring-lattice edges: each node joined to its ``halfk`` forward neighbours."""
function adjacent_edges(n, halfk)
    e = Tuple{Int, Int}[]
    for i0 in 0:n-1
        for s in 1:halfk
            push!(e, (i0 + 1, mod(i0 + s, n) + 1))
        end
    end
    e
end

"""Edge from each node to its diametrically opposite ring node (needs ``n`` even)."""
opposite_edges(n) = [(i0 + 1, mod(i0 + n ÷ 2, n) + 1) for i0 in 0:n-1]

"""All unordered node pairs (i < j) -- the candidate set for Erdős–Rényi graphs."""
all_pairs_undirected(n) = [(i, j) for i in 1:n for j in i+1:n]

# --- adjacency + drawing-object builders -------------------------------------

adjacency(n, edges) = begin
    adj = [Int[] for _ in 1:n]
    for (u, v) in edges
        push!(adj[u], v)
        push!(adj[v], u)
    end
    adj
end

build_graph(n, edges) = begin
    g = SimpleGraph(n)
    for (u, v) in edges
        add_edge!(g, u, v)
    end
    g
end

build_digraph(n, arcs) = begin
    g = SimpleDiGraph(n)
    for (u, v) in arcs
        add_edge!(g, u, v)
    end
    g
end

# --- graph builders (return the undirected edge list) ------------------------

ring_lattice_edges(n, k) = adjacent_edges(n, k ÷ 2)

"""Erdős–Rényi G(n, p): keep every candidate pair independently with prob p."""
er_np_edges(n, p, rng) = [pr for pr in all_pairs_undirected(n) if rand(rng) < p]

"""Erdős–Rényi G(n, m): pick m distinct pairs uniformly (partial Fisher-Yates)."""
function er_nm_edges(n, m, rng)
    pairs = all_pairs_undirected(n)
    order = collect(1:length(pairs))
    m = min(m, length(pairs))
    for i in 1:m
        j = rand(rng, i:length(order))
        order[i], order[j] = order[j], order[i]
    end
    [pairs[order[i]] for i in 1:m]
end

"""``k``-regular graph edges: ``a`` ring neighbours plus (if k odd) opposites."""
function regular_edges(n, k)
    a, b = divrem(k, 2)
    e = adjacent_edges(n, a)
    if b == 1
        isodd(n) && error("Can not make a regular graph")
        append!(e, opposite_edges(n))
    end
    e
end

"""Watts-Strogatz small-world graph from a ring lattice, rewired with prob p."""
function watts_strogatz_edges(n, k, p, rng)
    adj = [Set{Int}() for _ in 1:n]
    for (u, v) in adjacent_edges(n, k ÷ 2)
        push!(adj[u], v)
        push!(adj[v], u)
    end
    base = Tuple{Int, Int}[]
    for u in 1:n
        for v in adj[u]
            u < v && push!(base, (u, v))
        end
    end
    for (u, v) in base
        if rand(rng) < p && (v in adj[u])
            cands = [w for w in 1:n if w != u && !(w in adj[u])]
            if !isempty(cands)
                w = cands[rand(rng, 1:length(cands))]
                delete!(adj[u], v)
                delete!(adj[v], u)
                push!(adj[u], w)
                push!(adj[w], u)
            end
        end
    end
    edges = Tuple{Int, Int}[]
    for u in 1:n
        for v in adj[u]
            u < v && push!(edges, (u, v))
        end
    end
    edges
end

# --- metric algorithms on the plain adjacency list ---------------------------

"""BFS distances from ``src`` (``-1`` = unreachable)."""
function bfs_dists(adj, n, src)
    d = fill(-1, n)
    d[src] = 0
    frontier = [src]
    while !isempty(frontier)
        next = Int[]
        for u in frontier
            for v in adj[u]
                if d[v] == -1
                    d[v] = d[u] + 1
                    push!(next, v)
                end
            end
        end
        frontier = next
    end
    d
end

"""Mean shortest-path length over every reachable (source, target) pair."""
function characteristic_path_length(adj, n)
    total, count = 0, 0
    for src in 1:n
        d = bfs_dists(adj, n, src)
        for v in 1:n
            if d[v] >= 0
                total += d[v]
                count += 1
            end
        end
    end
    count == 0 ? NaN : total / count
end

"""Local clustering of node ``u`` (NaN when degree < 2)."""
function node_clustering(adj, u)
    nbrs = adj[u]
    k = length(nbrs)
    k < 2 && return NaN
    exist = 0
    for i in 1:k
        for j in i+1:k
            (nbrs[j] in adj[nbrs[i]]) && (exist += 1)
        end
    end
    exist / (k * (k - 1) / 2)
end

"""Average node clustering coefficient (ignoring degree-<2 nodes)."""
function clustering_coefficient(adj, n)
    vals = [node_clustering(adj, u) for u in 1:n]
    finite = filter(!isnan, vals)
    isempty(finite) ? NaN : sum(finite) / length(finite)
end

# --- reachability + connectivity ---------------------------------------------

"""Number of nodes reachable from ``src`` (including ``src`` itself)."""
reachable_count(adj, n, src) = count(>=(0), bfs_dists(adj, n, src))

"""True when every node is reachable from node 1 (undirected)."""
is_connected(adj, n) = reachable_count(adj, n, 1) == n

"""Fraction of ``iters`` fresh ``G(n, p)`` draws that are connected."""
function prob_connected(n, p, iters, rng)
    hits = 0
    for _ in 1:iters
        adj = adjacency(n, er_np_edges(n, p, rng))
        hits += is_connected(adj, n) ? 1 : 0
    end
    hits / iters
end

"""Vector of reachable-set sizes, one entry per start node."""
cluster_sizes(adj, n) = [reachable_count(adj, n, src) for src in 1:n]

# --- sampled characteristic path length ---------------------------------------

"""Shortest-path lengths for ``trials`` random node pairs (1-indexed)."""
function sample_path_lengths(adj, n, rng, trials)
    n < 2 && return Int[]
    dist_cache = [bfs_dists(adj, n, src) for src in 1:n]
    out = Int[]
    for _ in 1:trials
        u = rand(rng, 1:n)
        v = rand(rng, 1:n)
        if u != v
            d = dist_cache[u][v]
            d >= 0 && push!(out, d)
        end
    end
    out
end

"""Mean of ``sample_path_lengths`` -- a cheap Monte-Carlo characteristic path length."""
function estimate_path_length(adj, n, rng, trials)
    ls = sample_path_lengths(adj, n, rng, trials)
    isempty(ls) ? NaN : sum(ls) / length(ls)
end

# --- colour helper for the network charts ------------------------------------

const TAB10 = (:steelblue, :orangered, :seagreen, :goldenrod, :mediumorchid,
               :cyan, :brown, :pink, :gray40, :olive)

"""Map a matplotlib-style colour name (``"C3"`` or ``"red"``) to a Makie symbol."""
function tab_color(c)
    s = string(c)
    if length(s) > 1 && (s[1] == 'C') && all(isdigit, SubString(s, 2))
        return TAB10[(parse(Int, SubString(s, 2)) % 10) + 1]
    end
    to_color(s)
end
