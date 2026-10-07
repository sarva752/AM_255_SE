# Run this from the ROOT of your Lab repo (the folder that CONTAINS the Lab-4 folder).
# It re-creates the separate commits: baseline -> Task 1 -> Task 2 -> Task 3 -> Task 4.
$ErrorActionPreference = "Continue"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed / not on PATH. Install it, then CLOSE and reopen VS Code." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path ".git")) { Write-Host "Run this from your repo root (no .git here)." -ForegroundColor Red; exit 1 }
if (-not (git config user.name) -or -not (git config user.email)) {
    Write-Host "Set your identity first:" -ForegroundColor Yellow
    Write-Host '  git config --global user.name "Your Name"'
    Write-Host '  git config --global user.email "you@example.com"'
    exit 1
}
$bundle = Join-Path (Get-Location) "Lab-4\17_wordle_with_commits.bundle"
if (-not (Test-Path $bundle)) { Write-Host "Bundle not found at $bundle" -ForegroundColor Red; exit 1 }

$tmp = Join-Path $env:TEMP "wordle_src"
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
git clone -q $bundle $tmp
if ($LASTEXITCODE -ne 0) { Write-Host "Clone of bundle failed." -ForegroundColor Red; exit 1 }

function Get-Hash($pattern) { (git -C $tmp log --format=%H --grep=$pattern -n 1 --all).Trim() }
function Export-Tree($hash, $dest) {
    $zip = "$tmp.zip"
    if (Test-Path $zip) { Remove-Item $zip -Force }
    git -C $tmp archive --format=zip -o $zip $hash
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Expand-Archive -Path $zip -DestinationPath $dest -Force
}

$base = (git -C $tmp log --format=%H --grep="Updated scenario title" -n 1 --all).Trim()
$dest = "Lab-4\updated_code"

# Baseline: original code + "before" demo
Export-Tree $base $dest
git add "Lab-4/original_code" "Lab-4/demo_before.py" "Lab-4/updated_code"
git commit -q -m "Lab 4: baseline - original code and before-demo script"

foreach ($n in 1..4) {
    $h = Get-Hash "^Task ${n}:"
    if (-not $h) { Write-Host "Could not find Task $n commit" -ForegroundColor Red; exit 1 }
    $msg = (git -C $tmp log -1 --format=%s $h).Trim()
    Export-Tree $h $dest
    git add "Lab-4/updated_code"
    git commit -q -m $msg
    Write-Host "Committed: $msg" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done. Now copy before.mp4, after.mp4, chat_history.pdf, Lab4_Prompt_Log.pdf into Lab-4, then:" -ForegroundColor Cyan
Write-Host '  git add Lab-4 ":!Lab-4/17_wordle_with_commits.bundle"'
Write-Host '  git commit -m "Lab 4: add videos, chat history, prompt log"'
Write-Host '  git push'
git log --oneline
