---
title: "Implementation verification — derived-file preparation"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-mfv
owner: Data Architect
provenance: ai-generated
produced_by: {kind: llm-session, name: codex, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [stage-2, runner, derived-files]
class: bounded
---

# Implementation verification — derived-file preparation

Before each implement attempt is verified, the runner refreshes derived
metadata so a correct file-only implementation does not need another model
call just to run a renderer. This contract was integrated by PR #102 at merge commit
`2dd8e96fdba238dc88343d62ed073937d3415075` on 2026-10-08.

## Acceptance criteria

1. A first Flash attempt that creates findings.md passes with a regenerated
   plans/INDEX.md, without a repair or fallback solely for that index.
2. Modified or new held documents get today's updated stamp; clean documents,
   unheld files, document bodies and review metadata are unchanged. Deleted
   files are skipped. Document and index paths may not alias another file.
   Duplicate/no headers remain invalid for the verifier.
3. Stamping precedes index rendering, which precedes make verify on every
   attempt, including retries. No preparation command receives model secrets.
4. Preparation failure produces bounded, credential-scrubbed diagnostics,
   collects document refusals together rather than stopping at the first
   document, prevents verification/checkpoint for that attempt and enters the existing
   repair flow. Keep the existing limits: on the default Flash route, one
   Flash repair, then one Sonnet fallback after the initial Flash attempt;
   an explicit Stage-2-off run keeps its single Sonnet attempt. No additional
   attempts. Only
   successful preparation followed by green verification can checkpoint.
   This continuation was explicitly confirmed by the maintainer on 2026-10-08.
5. Real test failures still reach the existing repair flow; regeneration does
   not weaken make verify or change model routing or retry limits.

## Non-goals

Review-loop integration, changing gates, repair of unrelated clean headers,
new renderers, model-policy changes, automatic review approval, architecture.
No design phase: the existing stamp and registry provide the design.

## Verification evidence

Implementation `b602600` passed `make verify`: 1270 passed, 16 skipped
on 2026-10-08. Twenty new regression cases cover preparation and its refusal
boundaries. Final Codex review found no open findings; hosted CI passed
on PR head `dba6ff7`. Tests remain in `tests/test_stage2.py`.
