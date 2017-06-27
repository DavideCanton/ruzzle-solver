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
    def from_words(words):
        trie = Trie()

        current = trie.root
        current_word = ""

        for word in sorted(words):
            while word[:len(current_word)] != current_word:
                current = current.parent
                current_word = current_word[:-1]

            for char in word[len(current_word):]:
                if not current.has_child(char):
                    current.children[char] = Node(char)
                    current.children[char].parent = current
                current = current.get_child(char)

            current.is_end = True
            current_word = word

        return trie

    def add_word(self, word):
        current = self.root

        for char in word:
            if not current.has_child(char):
                current.children[char] = Node(char)
                current.children[char].parent = current
            current = current.get_child(char)

        current.is_end = True

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
