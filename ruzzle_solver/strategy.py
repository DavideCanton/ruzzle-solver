from __future__ import annotations

import sys
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self

from .graph import GraphNode
from .trie import Node, Trie


class Strategy[T](metaclass=ABCMeta):
    @abstractmethod
    def get_current(self, data: T) -> GraphNode: ...

    @abstractmethod
    def get_next_element(self, adj: GraphNode, current: GraphNode, data: T) -> T | None: ...

    @abstractmethod
    def stop_exploring(self, data: T) -> bool: ...

    @abstractmethod
    def extract(self, data: T) -> Sequence[GraphNode] | None: ...

    @abstractmethod
    def get_init_item(self, node: GraphNode) -> T | None: ...


@dataclass
class SeqNode:
    last: GraphNode
    length: int
    prev: SeqNode | None
    items: frozenset[GraphNode]

    @classmethod
    def Single(cls, node: GraphNode) -> Self:
        return cls(node, 1, None, frozenset([node]))

    @classmethod
    def Add(cls, node: GraphNode, seq: SeqNode) -> Self:
        return cls(node, seq.length + 1, seq, seq.items | frozenset([node]))

    def __len__(self) -> int:
        return self.length

    def __contains__(self, node: GraphNode) -> bool:
        return node in self.items

    def to_seq(self) -> Sequence[GraphNode]:
        ret = []
        cur: SeqNode | None = self
        while cur:
            ret.append(cur.last)
            cur = cur.prev
        return ret[::-1]


type S = tuple[SeqNode, Node]


@dataclass
class TrieStrategy(Strategy[S]):
    trie: Trie
    minlength: int = 1
    maxlength: int = sys.maxsize

    def get_current(self, data: S) -> GraphNode:
        return data[0].last

    def stop_exploring(self, data: S) -> bool:
        # it's useless to expand further if reached maxlength
        return len(data[0]) == self.maxlength

    def get_next_element(self, adj: GraphNode, _current: GraphNode, data: S) -> S | None:
        path, trie_node = data

        if adj in path:
            return None

        if (child := trie_node.get_child(adj.value)) is None:
            return None

        return (SeqNode.Add(adj, path), child)

    def extract(self, data: S) -> Sequence[GraphNode] | None:
        if self.minlength <= len(data[0]) <= self.maxlength and data[1].is_end:
            return data[0].to_seq()

        return None

    def get_init_item(self, node: GraphNode) -> S | None:
        if child := self.trie.root.get_child(node.value):
            return (SeqNode.Single(node), child)
        else:
            return None
