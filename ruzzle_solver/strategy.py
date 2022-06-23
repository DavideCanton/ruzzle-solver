import sys
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Sequence, TypeVar

from .graph import GraphNode
from .trie import Node, Trie

T = TypeVar("T")


class Strategy(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get_current(self, data: T) -> GraphNode:
        raise NotImplementedError

    @abstractmethod
    def get_next_element(self, adj: GraphNode, current: GraphNode, data: T) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def stop_exploring(self, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def extract(self, data: T) -> Sequence[GraphNode] | None:
        raise NotImplementedError

    @abstractmethod
    def get_init_item(self, node: GraphNode) -> T | None:
        raise NotImplementedError


@dataclass
class SeqNode:
    last: GraphNode
    length: int
    prev: "SeqNode | None"
    items: frozenset[GraphNode]

    @staticmethod
    def single(node: GraphNode):
        return SeqNode(node, 1, None, frozenset([node]))

    @staticmethod
    def add(node: GraphNode, seq: "SeqNode"):
        return SeqNode(node, seq.length + 1, seq, seq.items | frozenset([node]))

    def __len__(self):
        return self.length

    def __contains__(self, node: GraphNode):
        return node in self.items

    def to_list(self) -> list[GraphNode]:
        ret = []
        cur: SeqNode | None = self
        while cur:
            ret.append(cur.last)
            cur = cur.prev
        return ret[::-1]


S = tuple[SeqNode, Node]


@dataclass
class TrieStrategy(Strategy[S]):
    trie: Trie
    minlength: int = field(default=1)
    maxlength: int = field(default=sys.maxsize)

    def get_current(self, data: S) -> GraphNode:
        return data[0].last

    def stop_exploring(self, data: S) -> bool:
        # it's useless to expand further if reached maxlength
        return len(data[0]) == self.maxlength

    def get_next_element(
        self, adj: GraphNode, _current: GraphNode, data: S
    ) -> S | None:
        path, trie_node = data

        if adj in path:
            return None

        if (child := trie_node.get_child(adj.value)) is None:
            return None

        return (SeqNode.add(adj, path), child)

    def extract(self, data: S) -> Sequence[GraphNode] | None:
        if self.minlength <= len(data[0]) <= self.maxlength and data[1].is_end:
            return data[0].to_list()

        return None

    def get_init_item(self, node: GraphNode) -> S | None:
        if (child := self.trie.root.get_child(node.value)) is None:
            return None

        return (SeqNode.single(node), child)
