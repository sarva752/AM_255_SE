"""AFTER demo (~10s): bug fixed + new features. Run: python demo_after.py"""
import os, sys, time, builtins
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "updated_code"))
from game import WordleGame

g = WordleGame(5); g.target = "apple"
script = iter(["eerie", "abc", "stone", "", "apple"])
def fake_input(prompt=""):
    time.sleep(1.2); s = next(script); print(prompt + s); return s
builtins.input = fake_input
print("### FIXED: eerie vs apple -> only the last 'e' is green; invalid guesses are free;")
print("### history + summary shown. Also try: python updated_code/main.py 4  (or 6)\n")
g.run()
