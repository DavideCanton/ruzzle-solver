class Node:
    def __init__(self, char, is_end=False):
        self.char = char
        self.children = {}
        self.parent = None
        self.is_end = is_end


class Trie:
    def __init__(self):
        self.root = Node(None)

    @staticmethod
    def from_words(words):
        trie = Trie()

        for word in words:
            trie.add_word(word)

        return trie

    def add_word(self, word):
        current = self.root

        for char in word:
            if char not in current.children:
                current.children[char] = Node(char)
                current.children[char].parent = current
            current = current.children[char]

        current.is_end = True

    def __contains__(self, word):
        current = self.root

        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]

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
    words = ["casa", "pippo", "prova"]
    trie = Trie.from_words(words)

    print(list(trie.words()))

    for word in words:
        print(word in trie)


if __name__ == "__main__":
    main()
