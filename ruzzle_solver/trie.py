import itertools as it
import multiprocessing as mp
import operator
from dataclasses import dataclass, field
from typing import Generator, Iterable


@dataclass(eq=True)
class Node:
    char: str
    children: dict[str, "Node"] = field(default_factory=dict)
    parent: "Node | None" = field(default=None)
    is_end: bool = field(default=False)

    def has_child(self, child: str):
        return child in self.children

    def get_child(self, child: str):
        return self.children[child]


class Trie:
    root: Node

    def __init__(self):
        self.root = Node(None)

    @staticmethod
    def from_words(
        words: Iterable[str],
        use_parallelism: bool = True,
        parallelism_degree: int | None = None,
    ) -> "Trie":
        words = sorted(words)

        if use_parallelism:
            words_dict = [
                list(g) for _, g in it.groupby(words, key=operator.itemgetter(0))
            ]
            if parallelism_degree is None:
                parallelism_degree = mp.cpu_count()
            else:
                parallelism_degree = max(1, parallelism_degree)

            with mp.Pool(parallelism_degree) as p:
                tries = p.map(Trie._make_trie, words_dict)
        else:
            tries = [Trie._make_trie(words)]

        trie = Trie()
        for t in tries:
            r = t.root
            for (c, rr) in r.children.items():
                trie.root.children[c] = rr

        return trie

    @staticmethod
    def _make_trie(words: Iterable[str]) -> "Trie":
        trie = Trie()

        cur_node = trie.root
        cur_word = ""

        for word in words:
            cur_word, cur_node = Trie._insert_word(word, cur_word, cur_node)

        return trie

    @staticmethod
    def _insert_word(word: str, cur_word: str, cur_node: Node) -> tuple[str, Node]:
        cur_word, cur_node = Trie._backtrack_word(word, cur_word, cur_node)
        cur_node = Trie._traverse_and_insert(cur_node, word[len(cur_word) :])
        return word, cur_node

    @staticmethod
    def _backtrack_word(
        word: str, current_word: str, current: Node
    ) -> tuple[str, Node]:
        c: Node | None = current

        while word[: len(current_word)] != current_word:
            assert c is not None
            c = c.parent
            current_word = current_word[:-1]

        assert c is not None
        return current_word, c

    @staticmethod
    def _traverse_and_insert(current: Node, word: str) -> Node:
        for char in word:
            if not current.has_child(char):
                current.children[char] = Node(char)
                current.children[char].parent = current
            current = current.get_child(char)

        current.is_end = True

        return current

    def add_word(self, word: str) -> None:
        Trie._traverse_and_insert(self.root, word)

    def __contains__(self, word: str) -> bool:
        current = self.root

        for char in word:
            if not current.has_child(char):
                return False
            current = current.get_child(char)

        return current.is_end

    def words(self) -> Generator[str, None, None]:
        cur_word: list[str] = []
        stack = [(self.root, -1)]

        while stack:
            current, depth = stack.pop()

            if depth >= 0:
                cur_word = cur_word[:depth]
            cur_word.append(current.char)

            if current.is_end:
                yield "".join(cur_word)

            for child in current.children.values():
                stack.append((child, depth + 1))


def main():
    words = ["casa", "casino", "casotto", "casinino", "casottone", "pippo", "pluto"]
    trie = Trie.from_words(words)

    print(list(trie.words()))

    for word in words:
        print(word in trie)


if __name__ == "__main__":
    main()
