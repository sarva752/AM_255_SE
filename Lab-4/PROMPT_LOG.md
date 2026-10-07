# Lab 4 – Wordle (17_wordle) – Prompt / change log

NOTE: The official deliverable is your *exported full chat* (PDF/doc). This log is a
summary to go alongside it.

| # | Prompt (summary) | Result | Commit |
|---|------------------|--------|--------|
| 0 | "Inspect the repo + README, reproduce the bugs before changing anything" | Bug 1: `eerie` vs `apple` gives 2 extra yellow `e`s (yellow check uses `ch in target`, ignoring counts). Bug 2: `continue` inside `for _ in range(6)` makes invalid guesses consume a turn. | – |
| 1 | "Fix duplicate-letter feedback: greens first, each target letter satisfies at most one guess letter" | `feedback.py` uses a `Counter` of target letters not consumed by greens; yellows only while supply remains. | Task 1 |
| 2 | "Add win/loss handling, 6 accepted-guess limit, invalid guesses must not consume a turn" | `for` → `while len(history) < 6`; history only holds accepted guesses; quit/EOF handled. | Task 2 |
| 3 | "Add 4/5/6-letter modes using in-memory words" | Added 4- & 6-letter words (list only had 5), `SUPPORTED_LENGTHS`, length menu / `python main.py 6`, unit tests for feedback. | Task 3 |
| 4 | "Show readable history after each accepted guess and a final summary, no entries for invalid attempts" | `format_history()`, per-game `summary()`, session summary with play-again. 20 unit tests total. | Task 4 |

Constraints respected: stdlib only, all state in memory, project structure kept.
