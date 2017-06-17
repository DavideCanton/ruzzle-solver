import itertools as it
from collections import deque


class Graph_Node:
    def __init__(self, i, j, c):
        self.i = i
        self.j = j
        self.c = c

    def __hash__(self):
        return hash(self.i) * 13 + hash(self.j) * 17 + hash(self.c) * 19

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "({}, {}, {})".format(self.i, self.j, self.c)


def build_graph(matrix):
    r = len(matrix)
    c = len(matrix[0])

    nodes = {(i, j): Graph_Node(i, j, matrix[i][j])
             for i, j in it.product(range(r), range(c))}
    adj = {}

    for i, j in it.product(range(r), range(c)):
        node = nodes[i, j]
        adj_node = adj[node] = set()

        for oi, oj in it.product([-1, 0, 1], repeat=2):
            i2, j2 = i + oi, j + oj

            if 0 <= i2 < r and 0 <= j2 < c and (i, j) != (i2, j2):
                n = nodes[i2, j2]
                adj_node.add(n)

    return adj


def generate_walks(matrix):
    for node in matrix:
        yield from generate_walks_from_node(matrix, node)


def generate_walks_from_node(matrix, node):
    queue = deque([[node]])

    while queue:
        path = queue.pop()
        current = path[-1]

        yield path

        for adj in matrix.get(current, []):
            if adj in path:
                continue
            queue.appendleft(path + [adj])


def main():
    matrix = [list('abcd'), list('efgh'), list('ijkl'), list('mnop')]

    adj = build_graph(matrix)

    for (k, v) in adj.items():
        print(k, "->", list(map(str, v)))

    for walk in generate_walks(adj):
        print("".join(map(lambda n: str(n.c), walk)))


if __name__ == "__main__":
    main()
