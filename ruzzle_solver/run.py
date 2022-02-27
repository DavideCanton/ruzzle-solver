from collections import deque
from typing import Generator, TypeVar

from .graph import Graph, GraphNode
from .strategy import Strategy


def generate_walks(matrix: Graph, strategy) -> Generator[list[GraphNode], None, None]:
    for node in matrix:
        yield from _generate_walks_from_node(matrix, strategy, node)


T = TypeVar("T")


def _generate_walks_from_node(
    matrix: Graph,
    strategy: Strategy[T],
    node: GraphNode,
) -> Generator[list[GraphNode], None, None]:
    initial_item = strategy.get_init_item(node)

    if not initial_item:
        return

    queue = deque([initial_item])

    while queue:
        data = queue.pop()
        current = strategy.get_current(data)

        if strategy.can_yield(data):
            yield strategy.extract(data)

        for adj in matrix.get(current, []):
            if not strategy.can_enqueue(adj, current, data):
                continue
            queue.appendleft(strategy.get_next_element(adj, current, data))
