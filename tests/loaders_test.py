import json
import string
from io import StringIO

import pytest

from ruzzle_solver.loaders import FileLoader, Points, RandomLoader


@pytest.fixture
def scores() -> dict[str, Points]:
    return {"it": {"a": 1, "b": 2, "c": 3}}


def test_file_loader(scores):
    s = {
        "board": [
            "abc",
            "bca",
        ],
        "lang": "it",
        "mults": {
            "0-0": "DL",
            "1-1": "TW",
        },
    }
    file = StringIO(json.dumps(s))

    loader = FileLoader(file, scores)
    info = loader.load()

    assert info.board == s["board"]
    assert info.points == scores["it"]
    assert info.mults == {
        (0, 0): "DL",
        (1, 1): "TW",
    }


def test_file_loader_unknown_lang(scores):
    s = {
        "board": [],
        "lang": "foo",
        "mults": {},
    }
    file = StringIO(json.dumps(s))

    loader = FileLoader(file, scores)
    with pytest.raises(KeyError):
        loader.load()


def test_random_loader(scores):
    loader = RandomLoader(scores, 2, 3)
    info = loader.load()

    assert len(info.board) == 2
    assert all(len(r) == 3 for r in info.board)
    assert all(c in string.ascii_lowercase for r in info.board for c in r)
    assert info.points == scores["it"]
    assert info.mults == {}

    vowels = sum(1 if c in "aeiou" else 0 for r in info.board for c in r)
    cons = 6 - vowels

    assert vowels == 3
    assert cons == 3
