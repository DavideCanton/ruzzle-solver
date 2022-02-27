import json
import random
import string
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path

Board = list[list[str]]
Points = dict[str, int]
Mults = dict[tuple[int, int], str]


@dataclass
class LoadedInfo:
    board: Board
    points: Points
    mults: Mults


class Loader(metaclass=ABCMeta):
    @abstractmethod
    def load(self) -> LoadedInfo:
        pass


class FileLoader(Loader):
    def __init__(self, name, letter_scores):
        self.name = name
        self.letter_scores = letter_scores

    def load(self) -> LoadedInfo:
        def build_key(k):
            return tuple(map(int, k.split("-")))

        with Path(self.name).open() as in_json:
            json_obj = json.load(in_json)

        board = json_obj["board"]
        points = self.letter_scores[json_obj["lang"]]
        mults = {build_key(k): v for (k, v) in json_obj["mults"].items()}

        return LoadedInfo(board, points, mults)


class RandomLoader(Loader):
    def __init__(self, letter_scores, rows, cols=None):
        self.rows = rows
        self.cols = rows if cols is None else cols
        self.letter_scores = letter_scores

    def load(self) -> LoadedInfo:
        def split_list(cnt, lst):
            return [list(el) for el in zip(*[iter(lst)] * cnt)]

        letters = []

        for _ in range(int(self.rows * self.cols * 0.5)):
            letters.append(random.choice("aeiou"))

        cons = list(set(string.ascii_lowercase) - set("aeiou"))
        remaining = self.rows * self.cols - len(letters)

        for _ in range(remaining):
            letters.append(random.choice(cons))

        random.shuffle(letters)

        board = split_list(self.cols, letters)

        return LoadedInfo(board, self.letter_scores["it"], {})
