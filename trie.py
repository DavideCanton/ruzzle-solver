import string
import operator
import itertools as it
import multiprocessing as mp


class Node:
    def __init__(self, char, is_end=False):
        self.char = char
        self.children = {}
        self.parent = None
        self.is_end = is_end

    def has_child(self, child):
        return child in self.children

    def get_child(self, child):
        return self.children[child]


class Trie:
    def __init__(self):
        self.root = Node(None)

    @staticmethod
    def from_words(words, parallelism_degree=None):
        words = sorted(words)
        words_dict = [list(g) for k, g in it.groupby(words, key=operator.itemgetter(0))]

        if parallelism_degree is None:
            parallelism_degree = mp.cpu_count()
        else:
            parallelism_degree = max(1, parallelism_degree)

        with mp.Pool(parallelism_degree) as p:
            tries = p.map(Trie._make_trie, words_dict)

        trie = Trie()
        for t in tries:
            r = t.root
            e = next(iter(r.children.items()))
            trie.root.children[e[0]] = e[1]

        return trie

    @staticmethod
    def _make_trie(words):
        trie = Trie()

        cur_node = trie.root
        cur_word = ""

        for word in words:
            cur_word, cur_node = Trie._insert_word(word, cur_word, cur_node)

        return trie

    @staticmethod
    def _insert_word(word, cur_word, cur_node):
        cur_word, cur_node = Trie._backtrack_word(word, cur_word, cur_node)
        cur_node = Trie._traverse_and_insert(cur_node, word[len(cur_word):])
        return word, cur_node

    @staticmethod
    def _backtrack_word(word, current_word, current):
        while word[:len(current_word)] != current_word:
            current = current.parent
            current_word = current_word[:-1]
        return current_word, current

    @staticmethod
    def _traverse_and_insert(current, word):
        for char in word:
            if not current.has_child(char):
                current.children[char] = Node(char)
                current.children[char].parent = current
            current = current.get_child(char)

        current.is_end = True

        return current

    def add_word(self, word):
        Trie._traverse_and_insert(self.root, word)

    def __contains__(self, word):
        current = self.root

        for char in word:
            if not current.has_child(char):
                return False
            current = current.get_child(char)

        return current.is_end

    def words(self):
        cur_word = []
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
    words = ["casa", "casino", "casotto", "casinino", "casottone"]
    trie = Trie.from_words(words)

    print(list(trie.words()))

    for word in words:
        print(word in trie)


if __name__ == "__main__":
    main()
