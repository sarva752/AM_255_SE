from collections import Counter


def evaluate(target, guess):
    """Return a list of "green" / "yellow" / "gray" for each letter of guess.

    Standard Wordle rules:
      1. Exact matches (green) are resolved first.
      2. Each remaining target letter can satisfy at most one guess letter,
         so repeated letters in the guess only turn yellow while unmatched
         copies remain in the target.
    Works for any word length as long as target and guess have equal length.
    """
    if len(target) != len(guess):
        raise ValueError("target and guess must have the same length")

    result = ["gray"] * len(guess)

    # Pass 1: exact matches; count target letters NOT used by a green.
    remaining = Counter()
    for i, ch in enumerate(guess):
        if ch == target[i]:
            result[i] = "green"
        else:
            remaining[target[i]] += 1

    # Pass 2: present-but-misplaced letters, left to right, limited by supply.
    for i, ch in enumerate(guess):
        if result[i] == "green":
            continue
        if remaining[ch] > 0:
            result[i] = "yellow"
            remaining[ch] -= 1

    return result
