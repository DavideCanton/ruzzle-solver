import string
import random
from pathlib import Path
import json


class FileLoader:
    def __init__(self, name, letter_scores):
        self.name = name
        self.letter_scores = letter_scores

    def load(self):
        def build_key(k):
            return tuple(map(int, k.split("-")))

        with Path(self.name).open() as in_json:
            json_obj = json.load(in_json)

        board = json_obj["board"]
        points = self.letter_scores[json_obj["lang"]]
        mults = {build_key(k): v for (k, v) in json_obj["mults"].items()}

        return (board, points, mults)


class RandomLoader:
    def __init__(self, letter_scores, rows, cols=None):
        self.rows = rows
        self.cols = rows if cols is None else cols
        self.letter_scores = letter_scores

    def load(self):
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

        return board, self.letter_scores["it"], {}
