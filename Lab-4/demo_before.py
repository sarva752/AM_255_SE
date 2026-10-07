"""BEFORE demo (~10s): shows the two original bugs. Run: python demo_before.py"""
import os, sys, time, builtins
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "original_code"))
from game import WordleGame

g = WordleGame(5); g.target = "apple"          # fixed target so the bug is repeatable
script = iter(["eerie", "abc", "abc", "abc", "abc", "abc", "abc"])
def fake_input(prompt=""):
    time.sleep(1.2); s = next(script); print(prompt + s); return s
builtins.input = fake_input
print("### BUG 1: target=apple, guess=eerie (only one 'e' in apple, already green)")
print("### BUG 2: invalid guesses eat turns (6 invalid inputs end the game)\n")
g.run()
