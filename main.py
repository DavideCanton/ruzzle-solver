from pathlib import Path
import json
from trie import Trie
from graph import build_graph, generate_walks
from points import LETTER_SCORE


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


def main():
    with Path("in_2.json").open() as in_json:
        json_obj = json.load(in_json)

    board = json_obj["board"]
    points = LETTER_SCORE[json_obj["lang"]]
    mults = {tuple(map(int, k.split("-"))): v
             for (k, v) in json_obj["mults"].items()}

    print("Reading words...")
    words = read_words_from_file()
    print("Building word index...")
    trie = Trie.from_words(words)

    graph = build_graph(board)

    print("Generating words...")

    words = {}

    for path in generate_walks(graph, minlength=3):
        word = "".join(map(lambda n: n.value, path))

        if word in trie:
            word_points = get_word_points(path, points, mults)
            if words.get(word, -1) < word_points:
                words[word] = word_points

    for (word, word_points) in sorted(words.items(), key=lambda t: t[1]):
        print(word, "- Value:", word_points)


if __name__ == "__main__":
    main()
