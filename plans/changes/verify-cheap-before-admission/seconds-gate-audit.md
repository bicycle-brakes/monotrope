---
title: "Seconds-gate audit — verify-cheap-before-admission"
status: draft
implementation_status: none
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "claude-opus-5-5, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [audit, verification, admission]
---

# Seconds-gate audit — verify-cheap-before-admission

This change runs every `seconds` gate outside the machine's verify admission,
in every lane at once (bead coding-harness-bxxt.6, cheap verification before
admission). Plan step 9 asks the orchestrator to audit each current seconds
gate for an operation on shared state that would need serialised
verification, and never to guess. This note is that audit, written down so a
reader can check it (loop row L2-5); the comment in `decisions/gates.yaml`
points here.

Result: **no current seconds gate needs `needs_admission: true`.** Six
concurrent lanes gave every gate the verdict of the serial run.

## How it was checked

1. **Reading.** Each gate's command and script were read for writes: file
   writes, temporary directories, subprocesses, tracker and network access.
   The list is the local selection of the `verify`, `docs` and `drift` jobs
   at `36b4b356` (21 unprotected gates; `pytest` and `leerprobe` are
   `minutes` and stay inside the admission).
2. **Measurement.** One serial run of the 21 gates, then six lanes running
   the whole set concurrently in one checkout (harsher than six worktrees: the
   checkout-local caches are shared too), on 2026-11-14 between 18:59 and
   19:01 UTC, at `36b4b356`, on the maintainer's macOS machine while another
   session held the verify admission. Recorded per gate: exit code in each
   lane against the serial exit code; new entries of
   `git status --porcelain --ignored` in the checkout; files written under
   `~/.npm`, `~/.cache`, `~/.config/gh` and `~/.local/state` since the start.

## Per gate

| Gate | Jobs | What it writes or touches | Shared state? |
| --- | --- | --- | --- |
| `ruff-check`, `ruff-format` | verify | `.ruff_cache/` inside the checkout; ruff writes a `.gitignore` of `*` into it | no — per checkout, ignored |
| `ramp-valves` | verify | runs `ruff check --statistics`; the same per-checkout cache | no |
| `ruleset` | verify | pytest's `.pytest_cache/` (self-ignored) and `__pycache__/` in the checkout; read-only GitHub API calls under the maintainer's `gh` login | no write; API calls are reads (one run's worth per lane) |
| `markdownlint` | verify, docs | `npx --yes markdownlint-cli2`: one uniquely named debug log per call in `~/.npm/_logs/`; the package came from the populated npm cache | no conflicting write measured (see limits) |
| `plans-registry`, `bead-export`, `dangling-beads` | verify, docs | `bd export` into a temporary folder of its own per process (`scripts/bead_render.py`); the Dolt store is only read | no — read-only towards the tracker |
| `plans-registry-strict` | drift | as `plans-registry` | no |
| `frontmatter-current` | verify, docs | reads git history; writes only with `--stamp`, which the gate does not pass | no |
| `criterion-ledger` | verify, docs | reads; its ledger clearing is a runner function, not the gate | no |
| `research-currency` | drift | appends to `$GITHUB_STEP_SUMMARY` only when CI names it | no (locally unset) |
| `docs-links`, `decision-continuity`, `adr-answers`, `interview-minimums`, `question-context`, `research-handoff`, `guard-test-environment`, `gate-schema`, `ci-drift` | verify (most also docs) | read files and git only | no |

## Measured

- **Verdicts.** All 6 × 21 concurrent executions matched the serial exit
  code; 0 mismatches. The serial run had three red gates, all existing
  reds of the checkout, none blocking the local verify verdict:
  `docs-links` (report), `markdownlint` (report) and `plans-registry-strict`
  (drift job).
- **Checkout.** No new path in `git status --porcelain --ignored` after the
  concurrent lanes (the caches existed already and are ignored).
- **Home.** 7 new files in `~/.npm`, all per-call debug logs in
  `~/.npm/_logs/`; 0 in `~/.cache` and `~/.config/gh`. The 4 files in
  `~/.local/state` were the other session's measurement and lock files, not
  the gates'.
- **Time.** The six concurrent lanes took 58.7 s of wall time; the slowest
  serial gates were `markdownlint` (24.9 s), `frontmatter-current` (15.9 s)
  and `ruleset` (13.3 s).

## Limits

- A cold npm cache was not measured: six lanes installing
  `markdownlint-cli2` for the first time at once write the shared npm cache
  together. npm's cache is content-addressed and writes atomically, but this
  audit did not observe it. If a cold-cache collision is ever seen, the
  answer is `needs_admission: true` on `markdownlint` — a maintainer's call,
  since it is an edit of the held gate list.
- The disk use of concurrent work outside the admission is not bounded by
  this change (bead coding-harness-87b0 stays open); the seconds gates write
  no more than the caches above.
- A recipient repository runs its own gates. The kit carries the mark and
  this method, not this verdict: a recipient audits its own seconds gates.
