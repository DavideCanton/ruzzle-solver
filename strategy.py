import sys


class Strategy:
    def get_current(self, data):
        raise NotImplementedError

    def can_yield(self, data):
        raise NotImplementedError

    def can_enqueue(self, adj, current, data):
        raise NotImplementedError

    def get_next_element(self, adj, current, data):
        raise NotImplementedError

    def extract(self, data):
        raise NotImplementedError

    def get_init_item(self, node):
        raise NotImplementedError


class TrieStrategy(Strategy):
    def __init__(self, trie, minlength=None, maxlength=None):
        if minlength is None:
            minlength = 1
        if maxlength is None:
            maxlength = sys.maxsize

        self.trie = trie
        self.minlength = minlength
        self.maxlength = maxlength

    @staticmethod
    def _get_path(data):
        return data[0]

    @staticmethod
    def _get_trie_node(data):
        return data[1]

    @staticmethod
    def _build_data(path, trie_node):
        return (path, trie_node)

    def get_current(self, data):
        return TrieStrategy._get_path(data)[-1]

    def can_yield(self, data):
        path_len = len(TrieStrategy._get_path(data))
        is_correct_len = self.minlength <= path_len <= self.maxlength
        is_end = TrieStrategy._get_trie_node(data).is_end

        return is_correct_len and is_end

    def can_enqueue(self, adj, current, data):
        path = TrieStrategy._get_path(data)
        trie_node = TrieStrategy._get_trie_node(data)

        # it's useless to expand further if reached maxlength
        if adj in path or len(path) == self.maxlength:
            return False

        return trie_node.has_child(adj.value)

    def get_next_element(self, adj, current, data):
        path = TrieStrategy._get_path(data) + [adj]
        trie_node = TrieStrategy._get_trie_node(data).get_child(adj.value)

        return TrieStrategy._build_data(path, trie_node)

    def extract(self, data):
        return TrieStrategy._get_path(data)

    def get_init_item(self, node):
        if not self.trie.root.has_child(node.value):
            return None

        child = self.trie.root.get_child(node.value)

        return TrieStrategy._build_data([node], child)
