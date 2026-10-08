---
title: "Research — runner-red-gate"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-zci
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner]
---

# Research — runner-red-gate

Phase 1. Facts read on 2026-10-08 at `origin/main` `b32f488`.

## What the runner hands a repair attempt today

`scripts/stage2.py` `verify_attempt` runs `make verify` after each
implement attempt. On a non-zero exit it keeps the **last 80 lines** of
standard output and standard error, scrubbed of the GLM key, and
`implementation_prompt` hands them to the next attempt under "Earlier
post-run diagnostics". The diagnostics are not stored anywhere.

## Why the tail misses the failure

`scripts/verify_all.sh` runs the gates in order and frames each one:
`── [<gate>] $ <command>` before, and after it either `── [<gate>] gruen`,
`── [<gate>] RED (block) — der Lauf ist rot.` or, for a report-only gate,
`── [<gate>] rot, aber nur report …`. The last gates are report-only
(docs-links, markdownlint) and long.

Measured on 2026-10-07: a red run on `feat/stage2-session` printed 5,649
lines; its last 80 were markdownlint report lines and the final
`VERIFY RED` line, while the failing pytest case stood thousands of lines
earlier. In the implement smoke on `test/glm-smoke` (`0d9d5e5`) both the
Flash repair and the Sonnet fallback wrote into `plan.md` that the
diagnostics they received were markdownlint errors in files the change did
not touch; the blocking gate was not among them (bead coding-harness-zci).

## What would help

The sections of the gates that ended `RED (block)`, each bounded, in run
order, carry the failure; report-only sections do not decide the verdict and
can be left out. A run whose output carries no gate frame (make itself
failed, the runner script changed) still needs some evidence: the tail.

## Related, not in this change

A file-tool worker cannot regenerate `plans/INDEX.md` or stamp frontmatter
(bead coding-harness-mfv); keeping a copy of each attempt's diagnostics is a
separate improvement noted on coding-harness-zci.
