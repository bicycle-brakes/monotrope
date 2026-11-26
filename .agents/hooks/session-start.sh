#!/usr/bin/env python3
"""Antigravity SessionStart hook for coding-harness (.agents/hooks/session-start.sh).

Invoked by Antigravity with cwd set to `.agents/` (the directory containing `hooks.json`).
Outputs `{"injectSteps": [{"systemMessage": {"systemMessage": "..."}}]}` on stdout.
Runs `tools/bd prime` only when HEAD is an ancestor of `origin/main` (trust check).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=10, check=False)


def trusted_for_repo_tools(repo: Path) -> bool:
    if git(repo, "rev-parse", "-q", "--verify", "origin/main").returncode != 0:
        return False
    return git(repo, "merge-base", "--is-ancestor", "HEAD", "origin/main").returncode == 0


def latest_handover_resume(repo: Path) -> tuple[str, str]:
    handover_dir = repo / "docs" / "journal" / "handover"
    files = sorted(handover_dir.glob("*.md")) if handover_dir.is_dir() else []
    if not files:
        return "none found", ""
    newest = files[-1]
    rel = str(newest.relative_to(repo))
    try:
        text = newest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return rel, "(not read)"
    marker = "# Resume here"
    idx = text.find(marker)
    snippet = text[idx:] if idx >= 0 else text
    return rel, snippet[:6000]


def count_other_harnesses() -> str:
    try:
        res = subprocess.run(["pgrep", "-fl", "claude|codex|agy"], capture_output=True, text=True, timeout=5, check=False)
    except OSError:
        return "not read"
    if res.returncode not in (0, 1):
        return "not read"
    lines = [ln for ln in res.stdout.splitlines() if ln.strip() and "session-start.sh" not in ln]
    return str(len(lines))


def run_bd_prime(repo: Path) -> str:
    bd = repo / "tools" / "bd"
    if not bd.is_file():
        return "tools/bd: not found"
    if not trusted_for_repo_tools(repo):
        return "tools/bd prime: skipped (HEAD is not an ancestor of origin/main)"
    try:
        res = subprocess.run([str(bd), "prime"], cwd=repo, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"tools/bd prime: not read ({type(exc).__name__})"
    if res.returncode != 0:
        return f"tools/bd prime: exited {res.returncode}"
    return res.stdout[:12000]


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    try:
        _ = sys.stdin.read()
    except OSError:
        pass
    latest, resume = latest_handover_resume(repo)
    others = count_other_harnesses()
    prime = run_bd_prime(repo)
    parts = [
        "coding-harness session start (Antigravity SessionStart hook).",
        f"Newest handover: {latest}",
    ]
    if resume:
        parts.append(resume)
    parts.append(
        f"Processes matching claude|codex|agy on this machine: {others} "
        "(check for a second session in this checkout before changing files)."
    )
    if prime:
        parts.append(prime)
    payload = {"injectSteps": [{"systemMessage": {"systemMessage": "\n\n".join(parts)}}]}
    sys.stdout.write(json.dumps(payload) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
