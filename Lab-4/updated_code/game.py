import random
from words import WORDS
from feedback import evaluate

MAX_GUESSES = 6


class WordleGame:
    def __init__(self, length=5):
        self.length = length
        self.target = random.choice([w for w in WORDS if len(w) == length])
        self.history = []

    def is_valid(self, guess):
        """A guess is valid if it is alphabetic and the right length."""
        return guess.isalpha() and len(guess) == self.length

    def run(self):
        print(f"Wordle — {self.length} letters, {MAX_GUESSES} guesses. (q to quit)")
        won = False
        # Only accepted guesses are appended to history, so the length of
        # history is the number of turns used; invalid input never counts.
        while len(self.history) < MAX_GUESSES:
            remaining = MAX_GUESSES - len(self.history)
            try:
                guess = input(f"[{remaining} left] > ").strip().lower()
            except EOFError:
                print("\nInput ended. Quitting.")
                break
            if guess == "q":
                print("You quit the game.")
                break
            if not self.is_valid(guess):
                print(f"Invalid guess: enter a {self.length}-letter word "
                      "(letters only). This did not use a turn.")
                continue
            feedback = evaluate(self.target, guess)
            self.history.append((guess, feedback))
            print(" ".join(feedback))
            if guess == self.target:
                won = True
                print(f"Solved in {len(self.history)} guess(es)!")
                break
        else:
            print("Out of guesses!")

        if not won:
            print("The word was:", self.target)
