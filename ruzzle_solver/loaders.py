from __future__ import annotations

import json
import random
import string
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol, TextIO, cast

type Board = Sequence[Sequence[str]]
type Points = Mapping[str, int]
type Mults = Mapping[tuple[int, int], tuple[str, str]]


@dataclass
class LoadedInfo:
    board: Board
    points: Points
    mults: Mults


class Loader(Protocol):
    def load(self) -> LoadedInfo:
        pass


@dataclass
class FileLoader(Loader):
    file: TextIO
    letter_scores: Mapping[str, Points]

    def load(self) -> LoadedInfo:
        def build_key(k):
            return tuple(map(int, k.split("-")))

        json_obj = json.load(self.file)

        board = json_obj["board"]
        points = self.letter_scores[json_obj["lang"]]
        mults = {
            build_key(k): cast(tuple[str, str], tuple(v)) for (k, v) in json_obj["mults"].items()
        }

        return LoadedInfo(board, points, mults)


@dataclass
class RandomLoader(Loader):
    letter_scores: Mapping[str, Points]
    rows: int
    cols: int

    def load(self) -> LoadedInfo:
        def split_list(cnt, lst):
            return [list(el) for el in zip(*[iter(lst)] * cnt, strict=False)]

        letters = []

        vowels = "aeiou"

        for _ in range(int(self.rows * self.cols * 0.5)):
            letters.append(random.choice(vowels))

        cons = list(set(string.ascii_lowercase) - set(vowels))
        remaining = self.rows * self.cols - len(letters)

        for _ in range(remaining):
            letters.append(random.choice(cons))

        random.shuffle(letters)

        board = split_list(self.cols, letters)

        return LoadedInfo(board, self.letter_scores["it"], {})
