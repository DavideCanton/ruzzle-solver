from __future__ import annotations

import itertools as it
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(eq=True, frozen=True)
class GraphNode:
    i: int
    j: int
    value: str = field(compare=False, hash=False)


type IndexTuple = tuple[int, int]
type Graph = dict[GraphNode, set[GraphNode]]


def build_graph(matrix: Sequence[Sequence[str]]) -> Graph:
    rows = len(matrix)
    cols = len(matrix[0])

    nodes = {
        (i, j): GraphNode(i, j, value)
        for i, row in enumerate(matrix)
        for j, value in enumerate(row)
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
        node = (i, j)

        if node != adj and 0 <= adj[0] < rows and 0 <= adj[1] < cols:
            adjacents_of_node.add(nodes[adj])

    return adjacents_of_node
