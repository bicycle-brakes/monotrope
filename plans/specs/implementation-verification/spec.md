---
title: "Implementation verification — derived-file preparation"
status: accepted
implementation_status: done
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-11-18
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
   plans/INDEX.md, without a repair or fallback solely for that index. The
   attempt still has to have done work: creating or regenerating findings.md
   and the index is the runner's own bookkeeping and cannot satisfy the
   no-work check (bead coding-harness-te7q).
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

## Local verification measurement

The runner's local checks also leave the evidence one slip count is derived
from (bead coding-harness-bxxt.7, integrated 2026-11-15): a targeted check
records start and completion rows through `scripts/verify_duration.py` around
its execution into a targeted history beside the duration history, with the
checked tree's content identity — without the change's own `plan.md` and
`findings.md`, where the runner's bookkeeping lands between the checks —
captured on both sides, and the runner's admitted full check (`full_verify`)
carries its comparison context in runner-owned environment variables that the
shell's start record captures as additive fields with a version-2 marker.
Nothing about a slip is stored — no slip event, tally, receipt or consumed
marker; `python3 -m scripts.verify_duration slips` derives the count from both
local histories and reports it beside the number of incomplete or not
countable runs. A slip is a red full run that immediately follows a green
targeted check of the same identity. Interrupted work, conflicting records,
moved trees, unknown identities and the other side of such a possible pair are
reported as gaps beside the count, never as evidence of zero; legacy runs and
change-less full runs are reported outside the count without making the read
partial. Missing history is unavailable, as is a scope that selects no run at
all.
Reading never appends, repairs or creates
history, and a failed measurement write never changes a verification
verdict. Admission, gate selection and the full check's semantics stay
untouched; the targeted route's selection and limits remain this spec's
subject above.

## Verification evidence

Implementation `b602600` passed `make verify`: 1270 passed, 16 skipped
on 2026-10-08. Twenty new regression cases cover preparation and its refusal
boundaries. Final Codex review found no open findings; hosted CI passed
on PR head `dba6ff7`. Tests remain in `tests/test_stage2.py`.
