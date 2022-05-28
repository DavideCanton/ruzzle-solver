import sys
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .graph import GraphNode
from .trie import Node, Trie

T = TypeVar("T")


class Strategy(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get_current(self, data: T) -> GraphNode:
        raise NotImplementedError

    @abstractmethod
    def can_yield(self, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def can_enqueue(self, adj: GraphNode, current: GraphNode, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_next_element(self, adj: GraphNode, current: GraphNode, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def extract(self, data: T) -> list[GraphNode]:
        raise NotImplementedError

    @abstractmethod
    def get_init_item(self, node: GraphNode) -> T | None:
        raise NotImplementedError


S = tuple[list[GraphNode], Node]


@dataclass
class TrieStrategy(Strategy[S]):
    trie: Trie
    minlength: int = field(default=1)
    maxlength: int = field(default=sys.maxsize)

    @staticmethod
    def _get_path(data: S) -> list[GraphNode]:
        return data[0]

    @staticmethod
    def _get_trie_node(data: S) -> Node:
        return data[1]

    @staticmethod
    def _build_data(path, trie_node) -> S:
        return (path, trie_node)

    def get_current(self, data: S) -> GraphNode:
        return TrieStrategy._get_path(data)[-1]

    def can_yield(self, data: S) -> bool:
        path_len = len(TrieStrategy._get_path(data))
        is_correct_len = self.minlength <= path_len <= self.maxlength
        is_end = TrieStrategy._get_trie_node(data).is_end

        return is_correct_len and is_end

    def can_enqueue(self, adj: GraphNode, _current: GraphNode, data: S) -> bool:
        path = TrieStrategy._get_path(data)
        trie_node = TrieStrategy._get_trie_node(data)

        # it's useless to expand further if reached maxlength
        if adj in path or len(path) == self.maxlength:
            return False

        return trie_node.get_child(adj.value) is not None

    def get_next_element(self, adj: GraphNode, _current: GraphNode, data: S) -> S:
        path = TrieStrategy._get_path(data) + [adj]
        trie_node = TrieStrategy._get_trie_node(data).get_child(adj.value)

        return TrieStrategy._build_data(path, trie_node)

    def extract(self, data: S) -> list[GraphNode]:
        return TrieStrategy._get_path(data)

    def get_init_item(self, node: GraphNode) -> S | None:
        if (child := self.trie.root.get_child(node.value)) is None:
            return None

        return TrieStrategy._build_data([node], child)
