import itertools as it
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class GraphNode:
    i: int
    j: int
    value: str


IndexTuple = tuple[int, int]
Graph = dict[GraphNode, set[GraphNode]]


def build_graph(matrix: list[list[str]]) -> Graph:
    rows = len(matrix)
    cols = len(matrix[0])

    nodes = {
        (i, j): GraphNode(i, j, matrix[i][j])
        for i, j in it.product(range(rows), range(cols))
    }

    adjacents = {
        nodes[i, j]: _get_adjacents(i, j, rows, cols, nodes)
        for i, j in it.product(range(rows), range(cols))
    }

    return adjacents


def _get_adjacents(
    i: int,
    j: int,
    rows: int,
    cols: int,
    nodes: dict[IndexTuple, GraphNode],
) -> set[GraphNode]:
    adjacents_of_node = set()

    for offset_i, offset_j in it.product([-1, 0, 1], repeat=2):
        adj = i + offset_i, j + offset_j

        if _is_valid_adjacent((i, j), rows, cols, adj):
            node = nodes[adj]
            adjacents_of_node.add(node)

    return adjacents_of_node


def _is_valid_adjacent(
    node: IndexTuple,
    rows: int,
    cols: int,
    adj: IndexTuple,
) -> bool:
    return adj[0] in range(rows) and adj[1] in range(cols) and node != adj
