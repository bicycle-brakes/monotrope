#!/usr/bin/env bash
# check_worktree_state.sh — precondition for every agent session in a worktree.
#
# Fails closed: any suspicious state exits 1 with a repair hint. The ONLY
# auto-repair is a detached HEAD that sits on an ancestor of the expected
# branch — that one reattaches, because nothing can have been lost.
#
#   scripts/check_worktree_state.sh <worktree> <expected-branch> [min-known-sha]
#
# Pass "-" as the expected branch to accept whichever branch is checked out.
# That still refuses a detached HEAD and a half-finished rebase — it only drops
# the identity check, for callers that have no branch to expect.
#
# The incident class this prevents: a detached HEAD at an OLD review base. The
# agent works from a commit taken before the last round, the commits since are
# invisible to it, and the diff it reviews is not the diff that will merge.
#
# Exit: 0 usable (possibly after reattaching) · 1 do not work here.
set -euo pipefail

WT="${1:?usage: check_worktree_state.sh <worktree> <expected-branch> [min-known-sha]}"
BRANCH="${2:?expected branch missing}"
MIN_SHA="${3:-}"

[ -d "$WT" ] || { echo "✗ $WT: no such directory" >&2; exit 1; }
cd "$WT"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || { echo "✗ $WT: not a git worktree" >&2; exit 1; }

# 1. Rebase or merge in progress?
#    rev-parse --git-path resolves these correctly inside a LINKED worktree,
#    where .git is a file and the real directory lives elsewhere.
for marker in rebase-merge rebase-apply MERGE_HEAD CHERRY_PICK_HEAD; do
  p="$(git rev-parse --git-path "$marker")"
  if [ -e "$p" ]; then
    echo "✗ $WT: $marker in progress — finish it ('git rebase --continue')" >&2
    echo "  or abort it ('git rebase --abort' / 'git merge --abort')." >&2
    echo "  No agent session starts from a half-finished operation." >&2
    exit 1
  fi
done

# 2. Detached HEAD? Reattach ONLY when HEAD is an ancestor of the branch tip.
#    With BRANCH="-" there is no tip to compare against, so a detached HEAD is
#    always a hard stop: reattaching would mean guessing which branch was meant.
current="$(git rev-parse --abbrev-ref HEAD)"
if [ "$current" = "HEAD" ]; then
  tip=""
  [ "$BRANCH" != "-" ] && tip="$(git rev-parse --verify --quiet "$BRANCH" || true)"
  if [ -n "$tip" ] && git merge-base --is-ancestor HEAD "$tip"; then
    echo "⚠ $WT: detached HEAD at $(git rev-parse --short HEAD) — reattaching to $BRANCH"
    git checkout "$BRANCH"
  elif [ "$BRANCH" = "-" ]; then
    echo "✗ $WT: detached HEAD at $(git rev-parse --short HEAD), and no branch" >&2
    echo "  was named to reattach to. Check out the branch this work belongs on" >&2
    echo "  before starting — guessing one is not something a script may do." >&2
    exit 1
  else
    echo "✗ $WT: detached HEAD at $(git rev-parse --short HEAD), NOT on $BRANCH." >&2
    echo "  Work done here would sit on no branch. Inspect 'git reflog' and" >&2
    echo "  repair by hand — this is not a state a script may guess at." >&2
    exit 1
  fi
fi

# 3. Wrong branch? ("-" means: any branch, as long as it is one)
now="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "-" ] && [ "$now" != "$BRANCH" ]; then
  echo "✗ $WT: on branch '$now', expected '$BRANCH' — refusing to start." >&2
  exit 1
fi

# 4. Did HEAD move BACKWARD since we last recorded it?
#    This is the incident class itself: HEAD is an ancestor of where we were,
#    so commits that existed are no longer reachable from here.
if [ -n "$MIN_SHA" ]; then
  if ! git cat-file -e "${MIN_SHA}^{commit}" 2>/dev/null; then
    echo "✗ $WT: recorded commit $MIN_SHA does not exist in this repository." >&2
    echo "  The record and the tree disagree; do not work until that is explained." >&2
    exit 1
  fi
  head="$(git rev-parse HEAD)"
  if [ "$head" != "$MIN_SHA" ] && git merge-base --is-ancestor "$head" "$MIN_SHA"; then
    echo "✗ $WT: HEAD moved BACKWARD — $(git rev-parse --short "$head") is behind" >&2
    echo "  the recorded $(git rev-parse --short "$MIN_SHA"). Commits are missing." >&2
    echo "  Diagnose with 'git reflog'. No agent works from this state." >&2
    exit 1
  fi
fi

echo "✓ worktree usable: $now @ $(git rev-parse --short HEAD)"
