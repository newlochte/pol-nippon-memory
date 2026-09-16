from game.game import Game
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pairs",
        type=int,
        default=8,
        help="number of card pairs",
    )
    args = parser.parse_args()

    game = Game(args.pairs)
    game.run()


if __name__ == "__main__":
    main()
