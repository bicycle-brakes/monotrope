---
title: "Findings — stage2-flash-runner"
category: findings
status: draft
implementation_status: partial
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-qcp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-flash-runner

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 251 files, 564 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S1 | BLOCKER | SPEC | spec-review | plans/changes/stage2-flash-runner/spec.md:131 | [GAP] “Named test commands” has no defined command set or source. For a plan requiring a direct unittest command, the implementer must decide whether to permit it alongside `make verify`. This leaves both executable plans and the model’s shell permissions undecided. | Codex | taken — criterion 9 gives the model no shell and makes the runner own exactly `make verify` and the named git checkpoint commands | no |
| S2 | BLOCKER | SPEC | spec-review | plans/changes/stage2-flash-runner/spec.md:165 | [AMBIGUITY] Criterion 15 can require credential scrubbing on both routes, while criterion 13 forbids Stage 1 from reading `GLM_KEY`. For a Stage-1 answer containing a key fragment, the global reading requires knowing the key to redact it; a Flash-only reading leaves that fragment untouched. The required Stage-1 behavior is unspecified. | Codex | taken — criterion 15 limits GLM-key scrubbing to Flash and says Stage 1 never reads that key | no |
| S3 | BLOCKER | SPEC | spec-review | plans/changes/stage2-flash-runner/spec.md:182 | [AMBIGUITY] “Written artefacts” can mean runner-written outputs or also files written by the implementation model. If a stand-in commits a source file containing a credential fragment while returning a clean answer and satisfying all post-run checks, the first reading permits success after output scrubbing; the second requires that source file to be scrubbed as well, including on failure. The redaction boundary is unspecified. | Codex | taken — criterion 15 defines runner output, removes model shell access and adds exact-key removal plus refusal for a changed file | no |

Reviewer session: codex 01a11588-e851-7302-9fdc-2e30e7726fab

Stage-2 call, 2026-10-07: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 253 files, 567 commits, 12 rules.

Stage-2 call, 2026-10-07: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 253 files, 568 commits, 12 rules.

## Phase 6 — Opus 5.5, 2026-10-07

A fresh session reviewed: Codex, the declared reviewer of this `bounded` change, had no credit, so the Claude path applied, and the phase-2a session was a Codex session that could not be resumed here. The three 2a rows (S1–S3) arrived in the current spec as recorded: criterion 9 gives the model no shell and the runner exactly `make verify` and the checkpoint git commands; criterion 15 limits GLM-key scrubbing to the Flash route and adds the exact-key removal and refusal for changed files. `make verify` at f4be825: `VERIFY GREEN — every local gate of the 'verify' job passed.`

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | BLOCKER | MAINT | review | docs/WORKFLOW.md:701 | [DIVERGENT] Two places answer "can a foreign model's file tools read outside the worktree, for example `~/.config/cc-routing/secrets.env`?" in opposite ways. The new §4 text says the GLM key "is unavailable to the implementation model's file tools", and spec criterion 15 rests on "the model's no-shell tool boundary keeps the credential unavailable" (spec.md:206). The same §4 (docs/WORKFLOW.md:710-714) and the runner's own docstring (scripts/stage2.py:35-37) say reads are "asked, not confined" and the models "can read the rest of the disk". If the second is true, a Flash implementer can `Read` the secrets file and put the key into its answer or a file, and the credential barrier is only the exact-key scrub (see F6-2, F6-6). If the first is true (Claude Code's `--restricted` help says it confines the file tools to the working directories, unmeasured here), the "not confined" paragraph and docstring are false. One answer has to stand in both places. (criterion 15, 17) | Opus 5.5 | open | — |
| F6-2 | MAJOR | SPEC | review | scripts/stage2.py:200 | [AMBIGUITY] Criterion 15 says "the full key and therefore every eight-character fragment of it are absent" from the Flash streams and runner artefacts, and is refuted by "a runner artefact retaining a key fragment". `scrub` replaces only exact occurrences of the whole key. Case: the Flash process prints an eight-character prefix of the key without the full key (an error message that masks a key, or a model quoting a truncated key it read — see F6-1); the prefix stays in the printed stderr tail and in the explore answer appended to `research.md`. Reading A: fragments only need to vanish as parts of the whole key (the code and the tests, which plant only the whole key, satisfy it). Reading B: no standalone fragment may survive (the code does not). The spec has to say which. (criterion 15) | Opus 5.5 | open | — |
| F6-3 | MAJOR | SPEC | review | plans/changes/stage2-flash-runner/spec.md:242 | The real Codex phase-6 review did not run through the runner: Codex had no credit, and this verdict came from Opus 5.5 on the Claude path. The Flash explore (research.md audit line, attempt 1, route flash) and two GLM review-loop calls (findings.md audit lines) are present as evidence; the third required live call is not. As written, the criterion is refuted until either a Codex `review` runs through `stage2.py` or the maintainer amends the criterion. (criterion 19) | Opus 5.5 | open | — |
| F6-4 | MAJOR | MAINT | review | scripts/stage2.py:1093 | The documented recovery path fails after a model process dies mid-implementation. Case: the first Flash attempt edits `src/…` and `plan.md`, then exits non-zero (a Z.ai outage or rate limit mid-run). The verb exits 1 correctly and leaves those edits uncommitted. The step that `prompts/04-implement.md` and spec criterion 12 name next, `implement <change> --stage2-off …`, is refused with exit 2 because the worktree "has pre-existing changes outside this change's findings.md". The same happens when the Flash repair process fails after a first attempt that changed files. No operative text says the partial work must be discarded or committed first, or by whom. (criterion 10, 12) | Opus 5.5 | open | — |
| F6-5 | MINOR | SPEC | review | tests/test_stage2.py:477 | No test reaches several refusals of the new verbs. The leak-refusal test runs only `spec-review`, `review` and `review-loop`; nothing plants a leak before the first `explore` call or the first Flash `implement` attempt. The declaration-fault test (tests/test_stage2.py:496) is parametrised only over `spec-review` and `review-loop`, so a declaration that drops `glm-5.3-flash` or `claude-code-plan` is never shown to stop `explore` or `implement`. The missing-`GLM_KEY` refusal (tests/test_stage2.py:1271) is tested only for `review-loop`. The code does these checks; no test would turn red if they went. (criterion 4, 5) | Opus 5.5 | open | — |
| F6-6 | MINOR | MAINT | review | scripts/stage2.py:877 | The exact-key scan sees only tracked changes and untracked files that are not ignored (`git ls-files --others --exclude-standard`). Case: an attempt or the gate writes the key into a gitignored path in the worktree. `remove_changed_credential` does not see it, the key stays on disk, and the verb can succeed. Criterion 15 covers "a regular file changed by the attempt, including by the gate run", with no exception for ignored files. The file would not be committed, which limits the exposure. (criterion 15) | Opus 5.5 | open | — |
| F6-7 | MINOR | SPEC | review | scripts/stage2.py:1043 | The final `git status` of `checkpoint` is outside the `try` that turns a runner git failure into `CallFailed`. If that command fails after the commit, the verb exits 2 ("refused") instead of 1. Criterion 11 requires exit 1 for a runner-owned git command that fails after the post-run checks. (criterion 11) | Opus 5.5 | open | — |

Checked and found to hold: both verbs and `--stage2-off` parsing, existing verbs rejecting the flag (1, 13); explore preflight on `research.md` alone and implement on `spec.md` plus `plan.md` (2); Flash pinning of endpoint, model, effort, URL and all six model variables, with review-loop staying on `glm-5.3` (3); a declaration and leak check before every attempt, including the repair and the Sonnet fallback, and no fallback after a leak refusal (4, 5); explore and implement argv, prompts and tool sets (6, 8, 9); the post-run checks, a single checkpoint commit and the order Flash → Flash repair → Sonnet with accumulated diagnostics and no further attempt (10, 11); a failed or empty process stopping with exit 1 (12); `--stage2-off` starting only Haiku 4.5 or Sonnet 5.5 without reading `GLM_KEY` (13); route lines in `research.md` and `plan.md` (14); the exact-key scan after each Flash model run, after every `make verify` while a key is held and again before the commit (15); per-attempt audit lines (16); the operative texts and their planted-copy tests (17); existing verbs unchanged (18). These checks read the code and tests; nothing was run against a model.

Phase 6 verdict: Opus 5.5, 2026-10-07
