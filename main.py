import argparse
import logging
import multiprocessing as mp
import pickle
from collections.abc import Iterable, Iterator, Mapping, Sequence
from datetime import datetime
from operator import itemgetter
from pathlib import Path

from ruzzle_solver.graph import Graph, GraphNode, build_graph
from ruzzle_solver.loaders import (
    Board,
    FileLoader,
    LoadedInfo,
    Mults,
    Points,
    RandomLoader,
)
from ruzzle_solver.points import LETTER_SCORE
from ruzzle_solver.run import generate_walks
from ruzzle_solver.strategy import Strategy, TrieStrategy
from ruzzle_solver.trie import Trie


def configure_logger(use_file: bool = False) -> None:
    format_msg = "%(message)s"
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    args = {"format": format_msg, "level": logging.INFO}

    if use_file:
        args["filename"] = f"{now}_ruzzle.log"

    logging.basicConfig(**args)  # type: ignore


logger = logging.getLogger(__name__)


def read_words_from_file() -> Iterator[str]:
    with Path("./data/660000_parole_italiane.txt").open(encoding="utf-8") as f_in:
        for line in f_in:
            yield line.strip()


def get_word_points(path: Sequence[GraphNode], points: Points, mults: Mults) -> int:
    word_points = 0
    word_mult = 1

    for node in path:
        node_points = points[node.value.upper()]

        match mults.get((node.i, node.j)):
            case ("L", "D"):
                node_points *= 2
            case ("L", "T"):
                node_points *= 3
            case ("W", "D"):
                word_mult *= 2
            case ("W", "T"):
                word_mult *= 3

        word_points += node_points

    return word_points * word_mult


def print_header(size: int) -> None:
    buf = ["+---"] * size
    buf.append("+")
    header = "".join(buf)
    logger.info(header)


def print_row(row: Iterable[str]) -> None:
    buf = [f"| {char} " for char in row]
    buf.append("|")
    header = "".join(buf)
    logger.info(header)


def print_board(board: Board) -> None:
    for row in board:
        print_header(len(row))
        print_row(row)

    print_header(len(board[0]))


def create_parser():
    configure_logger(use_file=False)

    parser = argparse.ArgumentParser(description="Solver for ruzzle.")
    subparsers = parser.add_subparsers(help="sub command")

    parser.add_argument(
        "-n",
        "--num",
        help="The num of processes",
        choices=["auto"] + [str(n) for n in range(1, mp.cpu_count() + 1)],
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Regenerats the cache",
        action="store_true",
        default=False,
    )

    parser_file = subparsers.add_parser("file", help="Reads the schema from a json file.")
    parser_file.add_argument(
        "file", type=argparse.FileType("r", encoding="UTF-8"), help="The json file"
    )
    parser_file.set_defaults(action="file")

    parser_rand = subparsers.add_parser("rand", help="Generates a random schema.")
    parser_rand.add_argument("rows", type=int, help="The number of rows.")
    parser_rand.add_argument("cols", type=int, help="The number of columns.")
    parser_rand.set_defaults(action="rand")

    return parser


def main(args: argparse.Namespace) -> None:
    use_parallelism, parallelism_degree = _get_args(args)

    if args.action == "file":
        logger.info("Loading from file %s", args.file.name)
        info = FileLoader(args.file, LETTER_SCORE).load()
    else:
        logger.info("Generating schema with size (%s, %s)", args.rows, args.cols)
        info = RandomLoader(LETTER_SCORE, args.rows, args.cols).load()

    board = info.board

    print_board(board)

    trie = _load_trie(args.force, use_parallelism, parallelism_degree)
    graph = build_graph(board)

    logger.info("Generating words...")

    strategy = TrieStrategy(trie, minlength=3)

    found, words, walks = _find_words(info, graph, strategy)

    if not found:
        logger.info("No words found")

    if words:
        sorted_words = sorted(words.items(), key=itemgetter(1), reverse=True)
        for word, word_points in sorted_words[:10]:
            logger.info("%s - Value: %d", word, word_points)

        logger.info("-" * 30)
        logger.info("Found %d words.", len(words))
        logger.info("Best word: %s with value: %d", *(sorted_words[0]))
        logger.info("%s", walks[sorted_words[0][0]])


def _find_words[T](
    info: LoadedInfo, graph: Graph, strategy: Strategy[T]
) -> tuple[bool, Mapping[str, int], Mapping[str, Sequence[GraphNode]]]:
    words: dict[str, int] = {}
    walks: dict[str, Sequence[GraphNode]] = {}
    points, mults = info.points, info.mults
    found = False
    for walk in generate_walks(graph, strategy):
        word = "".join(n.value for n in walk)
        found = True

        word_points = get_word_points(walk, points, mults)
        if words.get(word, -1) < word_points:
            words[word] = word_points
            walks[word] = walk
    return found, words, walks


def _get_args(args: argparse.Namespace) -> tuple[bool, int | None]:
    match args.num:
        case None:
            use_parallelism = False
            parallelism_degree = None
        case "auto":
            use_parallelism = True
            parallelism_degree = None
        case num:
            use_parallelism = True
            parallelism_degree = int(num)

    logger.info(
        "Concurrency arguments use_parallelism=%s, parallelism_degree=%s",
        use_parallelism,
        parallelism_degree,
    )

    return use_parallelism, parallelism_degree


def _load_trie(force: bool, use_parallelism: bool, parallelism_degree: int | None) -> Trie:
    cache = Path("./tree.pickle")
    cache_loaded = False

    if cache.exists() and not force:
        try:
            logger.info("Loading trie from cache")
            with cache.open("rb") as c:
                trie = pickle.load(c)
            cache_loaded = True
        except Exception as e:
            logger.warning("Error loading cache: %s", e)

    if not cache_loaded:
        logger.info("Reading words...")
        words = read_words_from_file()
        logger.info("Building word index...")
        trie = Trie.from_words(
            words,
            use_parallelism=use_parallelism,
            parallelism_degree=parallelism_degree,
        )
        with cache.open("wb") as f_out:
            pickle.dump(trie, f_out)
    return trie


if __name__ == "__main__":
    args = create_parser().parse_args()
    main(args)
