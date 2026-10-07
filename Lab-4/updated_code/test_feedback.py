import unittest
from feedback import evaluate
from words import WORDS, SUPPORTED_LENGTHS

G, Y, X = "green", "yellow", "gray"


class FeedbackTests(unittest.TestCase):
    def test_all_green(self):
        self.assertEqual(evaluate("crane", "crane"), [G] * 5)

    def test_all_absent(self):
        self.assertEqual(evaluate("crane", "blimp"), [X] * 5)

    def test_guess_has_more_copies_than_target(self):
        # apple has one 'e' (already green at the end) -> extra e's are gray
        self.assertEqual(evaluate("apple", "eerie"), [X, X, X, X, G])

    def test_extra_copy_turns_yellow_only_while_supply_lasts(self):
        # stare has one 'e' (green) and one 'r' (misplaced)
        self.assertEqual(evaluate("stare", "eerie"), [X, X, Y, X, G])

    def test_green_takes_priority_over_earlier_yellow(self):
        self.assertEqual(evaluate("crane", "array"), [Y, G, X, X, X])

    def test_two_copies_both_present(self):
        # target has two 'p's, guess puts them in wrong places
        self.assertEqual(evaluate("apple", "ppxxx"), [Y, G, X, X, X])

    def test_4_letter_repeats(self):
        self.assertEqual(evaluate("moon", "noon"), [X, G, G, G])
        self.assertEqual(evaluate("seed", "eese"), [Y, G, Y, X])

    def test_6_letter_repeats(self):
        self.assertEqual(evaluate("little", "bubble"), [X, X, X, X, G, G])
        self.assertEqual(evaluate("pepper", "pppppp"), [G, X, G, G, X, X])

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            evaluate("crane", "cran")

    def test_every_supported_length_has_words(self):
        for n in SUPPORTED_LENGTHS:
            self.assertTrue([w for w in WORDS if len(w) == n], n)


if __name__ == "__main__":
    unittest.main()
