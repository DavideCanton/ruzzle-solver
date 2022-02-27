import logging
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Generator

from ruzzle_solver.graph import GraphNode, build_graph
from ruzzle_solver.loaders import Board, FileLoader, Mults, Points
from ruzzle_solver.points import LETTER_SCORE
from ruzzle_solver.run import generate_walks
from ruzzle_solver.strategy import TrieStrategy
from ruzzle_solver.trie import Trie


def configure_logger(use_file=False):
    format_msg = "%(message)s"
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    args = dict(format=format_msg)

    if use_file:
        args["filename"] = f"{now}_ruzzle.log"

    logging.basicConfig(**args)
    logger = logging.getLogger(name="ruzzle-solver")
    logger.setLevel(logging.INFO)
    return logger


LOGGER = configure_logger(use_file=False)


def read_words_from_file() -> Generator[str, None, None]:
    with Path("./data/660000_parole_italiane.txt").open() as f_in:
        for line in f_in:
            yield line.strip()


def get_word_points(path: list[GraphNode], points: Points, mults: Mults) -> int:
    word_points = 0
    word_mult = 1

    for node in path:
        node_points = points[node.value.upper()]
        mult_val, mult_type = list(mults.get((node.i, node.j), "  "))

        if mult_type == "L":
            node_points *= 2 if mult_val == "D" else 3
        elif mult_type == "W":
            word_mult *= 2 if mult_val == "D" else 3

        word_points += node_points

    return word_points * word_mult


def print_header(size: int):
    buf = []
    for _ in range(size):
        buf.append("+---")
    buf.append("+")
    header = "".join(buf)
    LOGGER.info(header)


def print_row(row: list[str]):
    buf = []
    for char in row:
        buf.append(f"| {char} ")
    buf.append("|")
    header = "".join(buf)
    LOGGER.info(header)


def print_board(board: Board):
    for row in board:
        print_header(len(row))
        print_row(row)

    print_header(len(board[0]))


def main():
    info = FileLoader("data/in_1.json", LETTER_SCORE).load()
    # info = RandomLoader(LETTER_SCORE, 4, 4).load()

    board = info.board
    points = info.points
    mults = info.mults

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

    if words:
        sorted_words = sorted(words.items(), key=itemgetter(1), reverse=True)
        for (word, word_points) in sorted_words:
            LOGGER.info("%s - Value: %d", word, word_points)

        LOGGER.info("-" * 30)
        LOGGER.info("Found %d words.", len(words))
        LOGGER.info("Best word: %s with value: %d", *(sorted_words[0]))


if __name__ == "__main__":
    main()
