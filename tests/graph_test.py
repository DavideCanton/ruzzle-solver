from ruzzle_solver.graph import GraphNode, build_graph


def test_build_graph():
    matrix = [["a", "b", "c"], ["d", "e", "f"]]

    graph = build_graph(matrix)

    nodes = [GraphNode(n // 3, n % 3, chr(ord("a") + n)) for n in range(6)]

    na, nb, nc, nd, ne, nf = nodes

    assert all(n in graph for n in nodes)
    assert graph[na] == {nb, nd, ne}
    assert graph[nb] == {na, nc, nd, ne, nf}
    assert graph[nc] == {nb, ne, nf}
    assert graph[nd] == {na, nb, ne}
    assert graph[ne] == {na, nb, nc, nd, nf}
    assert graph[nf] == {nb, nc, ne}
