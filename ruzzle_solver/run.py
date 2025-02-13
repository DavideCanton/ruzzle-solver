from __future__ import annotations

from collections import deque
from collections.abc import Iterator, Sequence

from .graph import Graph, GraphNode
from .strategy import Strategy


def generate_walks[T](matrix: Graph, strategy: Strategy[T]) -> Iterator[Sequence[GraphNode]]:
    for node in matrix:
        yield from _generate_walks_from_node(matrix, strategy, node)


def _generate_walks_from_node[T](
    matrix: Graph, strategy: Strategy[T], node: GraphNode
) -> Iterator[Sequence[GraphNode]]:
    initial_item = strategy.get_init_item(node)

    if not initial_item:
        return

    queue = deque([initial_item])

    while queue:
        data = queue.pop()

        if (item := strategy.extract(data)) is not None:
            yield item

        if strategy.stop_exploring(data):
            continue

        current = strategy.get_current(data)
        for adj in matrix.get(current, []):
            if (next_el := strategy.get_next_element(adj, current, data)) is None:
                continue
            queue.appendleft(next_el)
