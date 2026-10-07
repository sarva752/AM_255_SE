import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game import WordleGame, MAX_GUESSES
from words import WORDS


def play(length, target, inputs):
    """Run one game with scripted input; return (game, outcome, printed output)."""
    g = WordleGame(length)
    g.target = target
    out = io.StringIO()
    with patch("builtins.input", side_effect=list(inputs)), redirect_stdout(out):
        outcome = g.run()
    return g, outcome, out.getvalue()


class GameTests(unittest.TestCase):
    def test_win_first_guess(self):
        g, outcome, _ = play(5, "crane", ["crane"])
        self.assertEqual(outcome, "won")
        self.assertEqual(len(g.history), 1)

    def test_win_on_final_allowed_guess(self):
        wrong = ["stone"] * (MAX_GUESSES - 1)
        g, outcome, _ = play(5, "crane", wrong + ["crane"])
        self.assertEqual(outcome, "won")
        self.assertEqual(len(g.history), MAX_GUESSES)

    def test_loss_after_six_wrong_guesses(self):
        g, outcome, out = play(5, "crane", ["stone"] * MAX_GUESSES)
        self.assertEqual(outcome, "lost")
        self.assertIn("Out of guesses", out)
        self.assertIn("CRANE", out)  # target revealed

    def test_no_seventh_guess_is_requested(self):
        # exactly 6 inputs supplied; a 7th input() call would raise StopIteration
        play(5, "crane", ["stone"] * MAX_GUESSES)

    def test_invalid_guesses_do_not_consume_turns_or_history(self):
        bad = ["abc", "toolong", "", "12345", "cr4ne", "cran e"]
        g, outcome, _ = play(5, "crane", bad * 3 + ["stone"] * MAX_GUESSES)
        self.assertEqual(outcome, "lost")
        self.assertEqual(len(g.history), MAX_GUESSES)  # only valid guesses counted

    def test_quit_immediately_and_midgame(self):
        g, outcome, _ = play(5, "crane", ["q"])
        self.assertEqual((outcome, len(g.history)), ("quit", 0))
        g, outcome, out = play(5, "crane", ["stone", "q"])
        self.assertEqual((outcome, len(g.history)), ("quit", 1))
        self.assertIn("Game summary", out)

    def test_input_is_case_and_space_insensitive(self):
        g, outcome, _ = play(5, "crane", ["  CRANE  "])
        self.assertEqual(outcome, "won")

    def test_all_lengths_playable_and_enforced(self):
        for n in (4, 5, 6):
            target = next(w for w in WORDS if len(w) == n)
            wrong_len = "a" * (n + 1)
            g, outcome, _ = play(n, target, [wrong_len, target])
            self.assertEqual(outcome, "won", n)
            self.assertEqual(len(g.history), 1, n)

    def test_history_has_no_duplicates_from_invalid_attempts(self):
        g, _, _ = play(5, "crane", ["stone", "bad", "stone", "q"])
        self.assertEqual([h[0] for h in g.history], ["stone", "stone"])

    def test_history_printed_after_each_accepted_guess_only(self):
        _, _, out = play(5, "crane", ["stone", "bad", "grape", "q"])
        # one history table per accepted guess + one inside the final summary
        self.assertEqual(out.count("Guess history"), 2 + 1)


if __name__ == "__main__":
    unittest.main()
