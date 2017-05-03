import itertools as it
from collections import deque


class Graph_Node:
    def __init__(self, i, j, c):
        self.i = i
        self.j = j
        self.c = c
        self.p = None

    def __hash__(self):
        return hash(self.i) * 13 + hash(self.j) * 17 + hash(self.c) * 19

    def __str__(self):
        return f"({self.i}, {self.j}, {self.c})"


def build_graph(matrix):
    r = len(matrix)
    c = len(matrix[0])

    adj = {}

    for i in range(r):
        for j in range(c):
            node = Graph_Node(i, j, matrix[i][j])
            adj_node = adj[node] = set()
            offsets = it.product([-1, 0, 1], repeat=2)
            for oi, oj in offsets:
                i2, j2 = i + oi, j + oj
                if 0 <= i2 < r and 0 <= j2 < c and (i2 != i or j2 != j):
                    n = Graph_Node(i2, j2, matrix[i2][j2])
                    adj_node.add(n)
                    n.p = node

    return adj


def generate_walks(matrix):
    for node in matrix:
        queue = deque([(node, 1)])
        path = []
        while queue:
            current, depth = queue.pop()

            path = []
            c = current
            while c:
                path.append(c)
                c = c.p

            if current in path[1:]:
                continue

            yield path

            for adj in matrix[node]:
                queue.appendleft((adj, depth + 1))


def main():
    matrix = [['a', 'b', 'c'],
              ['d', 'e', 'f'],
              ['g', 'h', 'i']]

    adj = build_graph(matrix)

    for (k, v) in adj.items():
        print(k, "->", list(map(str, v)))

    for walk in generate_walks(adj):
        print("".join(map(lambda n: str(n.c), walk)))


if __name__ == "__main__":
    main()
