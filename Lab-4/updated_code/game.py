import random
from words import WORDS
from feedback import evaluate

MAX_GUESSES = 6
SYMBOLS = {"green": "G", "yellow": "Y", "gray": "-"}


class WordleGame:
    def __init__(self, length=5):
        self.length = length
        self.target = random.choice([w for w in WORDS if len(w) == length])
        self.history = []
        self.result = None  # "won", "lost" or "quit" once the game ends

    def format_history(self):
        """Readable table of accepted guesses: G=correct spot, Y=wrong spot, -=absent."""
        lines = ["Guess history (G = right spot, Y = wrong spot, - = not in word):"]
        for n, (guess, feedback) in enumerate(self.history, start=1):
            letters = " ".join(guess.upper())
            marks = " ".join(SYMBOLS[c] for c in feedback)
            lines.append(f"  {n}. {letters}   {marks}")
        return "\n".join(lines)

    def summary(self):
        """One-game summary shown when the game ends."""
        outcome = {"won": f"Won in {len(self.history)}/{MAX_GUESSES} guesses",
                   "lost": "Lost (out of guesses)",
                   "quit": "Quit early"}[self.result]
        lines = ["", "=== Game summary ===",
                 f"Word length : {self.length}",
                 f"Target word : {self.target.upper()}",
                 f"Result      : {outcome}",
                 f"Guesses used: {len(self.history)}"]
        if self.history:
            lines.append(self.format_history())
        return "\n".join(lines)

    def is_valid(self, guess):
        """A guess is valid if it is alphabetic and the right length."""
        return guess.isalpha() and len(guess) == self.length

    def run(self):
        print(f"Wordle — {self.length} letters, {MAX_GUESSES} guesses. (q to quit)")
        # Only accepted guesses are appended to history, so the length of
        # history is the number of turns used; invalid input never counts.
        while len(self.history) < MAX_GUESSES:
            remaining = MAX_GUESSES - len(self.history)
            try:
                guess = input(f"[{remaining} left] > ").strip().lower()
            except EOFError:
                print("\nInput ended. Quitting.")
                self.result = "quit"
                break
            if guess == "q":
                print("You quit the game.")
                self.result = "quit"
                break
            if not self.is_valid(guess):
                print(f"Invalid guess: enter a {self.length}-letter word "
                      "(letters only). This did not use a turn.")
                continue
            feedback = evaluate(self.target, guess)
            self.history.append((guess, feedback))
            print(self.format_history())
            if guess == self.target:
                self.result = "won"
                print(f"Solved in {len(self.history)} guess(es)!")
                break
        else:
            self.result = "lost"
            print("Out of guesses!")

        print(self.summary())
        return self.result
