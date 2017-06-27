import itertools as it
from collections import deque
from strategy import TrieStrategy


class GraphNode:
    def __init__(self, i, j, value):
        self.i = i
        self.j = j
        self.value = value

    def __hash__(self):
        return hash(self.i) * 13 + hash(self.j) * 17 + hash(self.value) * 19

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "({}, {}, {})".format(self.i, self.j, self.value)


def build_graph(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    nodes = {(i, j): GraphNode(i, j, matrix[i][j])
             for i, j in it.product(range(rows), range(cols))}
    adj = {}

    for i, j in it.product(range(rows), range(cols)):
        node = nodes[i, j]
        adj_node = adj[node] = set()

        for offset_i, offset_j in it.product([-1, 0, 1], repeat=2):
            i_2, j_2 = i + offset_i, j + offset_j

            if 0 <= i_2 < rows and 0 <= j_2 < cols and (i, j) != (i_2, j_2):
                node = nodes[i_2, j_2]
                adj_node.add(node)

    return adj


def generate_walks(matrix, strategy):
    for node in matrix:
        yield from generate_walks_from_node(matrix, strategy, node)


def generate_walks_from_node(matrix, strategy, node):
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


def main():
    matrix = ["abcd", "efgh", "ijkl", "mnop"]

    adj = build_graph(matrix)

    for (key, value) in adj.items():
        print(key, "->", list(map(str, value)))

    strategy = TrieStrategy(None, minlength=4, maxlength=4)

    for walk in generate_walks(adj, strategy):
        print("".join(map(lambda n: str(n.value), walk)))


if __name__ == "__main__":
    main()
