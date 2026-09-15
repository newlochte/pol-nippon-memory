# execute

# python3 game/words.py -r 2


# to get one line

# from game.words import get_word
# japanese, romaji, english, polish = get_word(2)


# to get everything

# from game.words import load_words
# words = load_words()


from pathlib import Path

import yaml

# (japanese, romaji, english, polish)
WordTuple = tuple[str, str, str, str]

def load_words():
    path = Path(__file__).parent / "data/word_list.yaml"
    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_word(row):
    return load_words()[row - 1]


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=int, required=True)
    row = parser.parse_args().r

    sys.stdout.reconfigure(encoding="utf-8")
    print(get_word(row))
