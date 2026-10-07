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


def ask_play_again():
    try:
        return input("Play again? (y/n): ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def print_session_summary(results):
    """results: list of (length, outcome, guesses_used). Kept in memory only."""
    print("\n##### Session summary #####")
    if not results:
        print("No games played.")
        return
    wins = sum(1 for _, r, _ in results if r == "won")
    print(f"Games played: {len(results)}   Wins: {wins}   "
          f"Losses: {sum(1 for _, r, _ in results if r == 'lost')}   "
          f"Quit: {sum(1 for _, r, _ in results if r == 'quit')}")
    won_guesses = [g for _, r, g in results if r == "won"]
    if won_guesses:
        print(f"Average guesses in won games: {sum(won_guesses) / len(won_guesses):.1f}")
    for i, (length, outcome, used) in enumerate(results, start=1):
        print(f"  Game {i}: {length} letters - {outcome} ({used} guesses)")


def main():
    results = []
    length = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) in SUPPORTED_LENGTHS:
        length = int(sys.argv[1])  # optional: `python main.py 6` skips the prompt
    while True:
        if length is None:
            length = choose_length()
            if length is None:
                break
        game = WordleGame(length)
        outcome = game.run()
        results.append((length, outcome, len(game.history)))
        if outcome == "quit" or not ask_play_again():
            break
        length = None  # let the player pick a new length
    print_session_summary(results)


if __name__ == "__main__":
    main()
