import sys

from game import WordleGame
from words import SUPPORTED_LENGTHS


def choose_length():
    """Ask for 4, 5 or 6 letters; re-ask on bad input. Returns None on quit/EOF."""
    options = "/".join(str(n) for n in SUPPORTED_LENGTHS)
    while True:
        try:
            choice = input(f"Choose word length ({options}), or q to quit: ").strip().lower()
        except EOFError:
            return None
        if choice == "q":
            return None
        if choice.isdigit() and int(choice) in SUPPORTED_LENGTHS:
            return int(choice)
        print(f"Please enter one of: {options}.")


if __name__ == "__main__":
    # Optional: `python main.py 6` skips the prompt.
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) in SUPPORTED_LENGTHS:
        length = int(sys.argv[1])
    else:
        length = choose_length()
    if length is not None:
        WordleGame(length).run()
