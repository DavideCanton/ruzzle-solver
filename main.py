import json
import random
import string
from operator import itemgetter
from pathlib import Path

from graph import build_graph, generate_walks
from points import LETTER_SCORE
from trie import Trie
from strategy import TrieStrategy


def read_words_from_file():
    with Path("./660000_parole_italiane.txt").open() as f_in:
        for line in f_in:
            yield line.strip()


def get_word_points(path, points, mults):
    word_points = 0
    word_mult = 1

    for node in path:
        node_points = points[node.value.upper()]
        mult = mults.get((node.i, node.j))

        if mult in ("DL", "TL"):
            node_points *= 2 if mult[0] == "D" else 3

        word_points += node_points

        if mult == "DW":
            word_mult *= 2
        if mult == "TW":
            word_mult *= 3

    word_points *= word_mult
    return word_points


def build_key(k):
    return tuple(map(int, k.split("-")))


def load_board_from_file(name):
    with Path(name).open() as in_json:
        json_obj = json.load(in_json)

    board = json_obj["board"]
    points = LETTER_SCORE[json_obj["lang"]]
    mults = {build_key(k): v for (k, v) in json_obj["mults"].items()}

    return (board, points, mults)


def random_board(n):
    letters = []

    for _ in range(n * 2 - 2):
        letters.append(random.choice("aeiou"))

    cons = list(set(string.ascii_lowercase) - set("aeiou"))

    for _ in range(n * n - n * 2 + 2):
        letters.append(random.choice(cons))

    random.shuffle(letters)

    board = [letters[i:i + n] for i in range(0, n * n, n)]

    return board, LETTER_SCORE["it"], {}


def print_header(size):
    for _ in range(size):
        print("+---", end="")
    print("+")


def print_row(row):
    for char in row:
        print("| {} ".format(char), end="")
    print("|")


def print_board(board):
    for row in board:
        print_header(len(row))
        print_row(row)

    print_header(len(board[0]))


def main():
    board, points, mults = load_board_from_file("in_3.json")
    # board, points, mults = random_board(100)

    print_board(board)

    print("Reading words...")
    words = read_words_from_file()
    print("Building word index...")
    trie = Trie.from_words(words)

    graph = build_graph(board)

    print("Generating words...")

    words = {}

    strategy = TrieStrategy(trie, minlength=3)

    for path in generate_walks(graph, strategy):
        word = "".join(n.value for n in path)

        word_points = get_word_points(path, points, mults)
        if words.get(word, -1) < word_points:
            words[word] = word_points

    for (word, word_points) in sorted(words.items(), key=itemgetter(1)):
        print(word, "- Value:", word_points)

    print("-" * 30)
    print("Found", len(words), "words.")
    print("Best word:", word, "with value:", word_points)


if __name__ == "__main__":
    main()
