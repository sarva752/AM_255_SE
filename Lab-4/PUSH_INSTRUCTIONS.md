# How to submit (≈5 minutes)

1. Record before video (10 s):  `python demo_before.py`   (shows both bugs)
2. Record after video  (10 s):  `python demo_after.py`    (also quickly show `python updated_code/main.py 4` / `6`)
3. Export THIS chat as PDF/doc (browser print → Save as PDF is fine).
4. Create/open your personal Lab repo, then:

```bash
git clone https://github.com/<your-username>/<your-lab-repo>.git
cd <your-lab-repo>
mkdir -p Lab-4 && cp -r /path/to/Lab-4/updated_code/* Lab-4/
# add: before.mp4, after.mp4, chat_history.pdf into Lab-4/
```

To keep the SEPARATE COMMITS per task (the assignment requires them), the easiest way is to
use the bundle, which contains the 4 task commits on top of the original repo:

```bash
git clone 17_wordle_with_commits.bundle wordle && cd wordle
git remote set-url origin https://github.com/<your-username>/<your-lab-repo>.git
git push -u origin HEAD:main        # do NOT push to / PR against SETAPESU26
```
Then add the videos + chat PDF in a final commit under Lab-4/.
Do NOT raise a PR to the SETAPESU26 repo.
