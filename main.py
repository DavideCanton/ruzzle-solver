from loaders import RandomLoader
from pathlib import Path
from operator import itemgetter
import logging
from datetime import datetime

from graph import build_graph, generate_walks
from points import LETTER_SCORE
from trie import Trie
from strategy import TrieStrategy

LOGGER = None


def configure_logger(use_file=False):
    global LOGGER

    format_msg = '%(message)s'
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    args = dict(format=format_msg)

    if use_file:
        args["filename"] = "{}_ruzzle.log".format(now)

    logging.basicConfig(**args)
    LOGGER = logging.getLogger(name="ruzzle-solver")
    LOGGER.setLevel(logging.INFO)


def read_words_from_file():
    with Path("./660000_parole_italiane.txt").open() as f_in:
        for line in f_in:
            yield line.strip()


def get_word_points(path, points, mults):
    word_points = 0
    word_mult = 1

    for node in path:
        node_points = points[node.value.upper()]
        mult_val, mult_type = mults.get((node.i, node.j), "  ")

        if mult_type == "L":
            node_points *= 2 if mult_val == "D" else 3
        elif mult_type == "W":
            word_mult *= 2 if mult_val == "D" else 3

        word_points += node_points

    return word_points * word_mult


def print_header(size):
    buf = []
    for _ in range(size):
        buf.append("+---")
    buf.append("+")
    header = "".join(buf)
    LOGGER.info(header)


def print_row(row):
    buf = []
    for char in row:
        buf.append("| {} ".format(char))
    buf.append("|")
    header = "".join(buf)
    LOGGER.info(header)


def print_board(board):
    for row in board:
        print_header(len(row))
        print_row(row)

    print_header(len(board[0]))


def main():
    configure_logger(use_file=False)

    # board, points, mults = FileLoader("in_3.json", LETTER_SCORE).load()
    board, points, mults = RandomLoader(LETTER_SCORE, 4, 4).load()

    print_board(board)

    LOGGER.info("Reading words...")
    words = read_words_from_file()
    LOGGER.info("Building word index...")
    trie = Trie.from_words(words)

    graph = build_graph(board)

    LOGGER.info("Generating words...")

    words = {}

    strategy = TrieStrategy(trie, minlength=3)

    for walk in generate_walks(graph, strategy):
        word = "".join(n.value for n in walk)

        word_points = get_word_points(walk, points, mults)
        if words.get(word, -1) < word_points:
            words[word] = word_points

    for (word, word_points) in sorted(words.items(), key=itemgetter(1)):
        LOGGER.info("%s - Value: %d", word, word_points)

    LOGGER.info("-" * 30)
    LOGGER.info("Found %d words.", len(words))
    LOGGER.info("Best word: %s with value: %d", word, word_points)


if __name__ == "__main__":
    main()
