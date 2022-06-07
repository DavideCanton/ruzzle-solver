from collections import deque
from typing import Generator, Sequence, TypeVar

from .graph import Graph, GraphNode
from .strategy import Strategy


def generate_walks(
    matrix: Graph, strategy
) -> Generator[Sequence[GraphNode], None, None]:
    for node in matrix:
        yield from _generate_walks_from_node(matrix, strategy, node)


T = TypeVar("T")


def _generate_walks_from_node(
    matrix: Graph,
    strategy: Strategy[T],
    node: GraphNode,
) -> Generator[Sequence[GraphNode], None, None]:
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
            if (next := strategy.get_next_element(adj, current, data)) is None:
                continue
            queue.appendleft(next)
