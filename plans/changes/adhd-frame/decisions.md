---
title: "Decisions — adhd-frame"
status: accepted
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-q24
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# adhd-frame — Decisions

**Provisional answers, chosen by the agent, awaiting the maintainer.** The
maintainer is away until Sunday 2026-10-04 and asked on 2026-09-30 that the
session work off as much of the plan as possible meanwhile. The phase 1a
interview could not be held; the orchestrating session took each
recommendation of `research.md` ("Open points for the phase 1a interview")
as a provisional answer. Nothing takes effect before the maintainer merges
the pull request (house rule 8); the pull request lists each answer for
confirmation.

## Provisional answers

1. **Q1 — the handover-skill rename travels in this pull request: (a).**
   The repository's skill is renamed to `handover` and says "always a pull
   request", with its consequential lines: `AGENTS.md`, the `install.sh`
   file list, the README row and the hook's display strings. No agent runs
   `tools/claude-code/install.sh`: reinstalling changes files under
   `~/.claude` and, as a side effect, turns on the handover trust list at
   session start (research section 2.4). The pull request names the
   reinstall as the maintainer's step, with `install.sh --check` first.
2. **Q2 — the acceptance card lives in the pull request templates: (b).**
   Both templates gain "What could break" and
   `done: <evidence> · <time used> of <appetite>`; `prompts/07-commit.md`
   points to them in one sentence.
3. **Q3 — the plan card does not wait for an "ok": (b).** It is shown when
   phase 3 ends, and phase 4 starts unless the maintainer says stop; an "ok"
   is asked only when the card widens the scope or appetite set earlier.
4. **Q4 — who answers the appetite stop: (b).** An orchestrating session
   may answer cut, park or drop; only the maintainer may answer continue.

## Note on the order of work

Open PR #60 edits `prompts/03-plan.md` and `prompts/04-implement.md` and
stays unmerged by the maintainer's decision. This change places its text so
that no hunk is shared with #60 (research section on the overlap); the
merge itself was not tried.

## Addendum 2026-10-05: the maintainer confirms all four answers

The maintainer went through the four provisional answers one at a time in
the Claude Code session on 2026-10-05 and confirmed each as written above:
the skill rename travels in this pull request (1), the acceptance card lives
in the pull request templates (2), the plan card starts phase 4 unless the
maintainer says stop (3), and only the maintainer may answer "continue" at
an appetite stop (4). They are no longer provisional.
