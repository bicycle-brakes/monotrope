---
title: "Spec — frontmatter-batch-log"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.21
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25", model: "gpt-6.1-terra"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, performance]
class: bounded
appetite: 4
adr_files: []
---

# Spec — frontmatter-batch-log

The frontmatter-current gate obtains clean documents' history in one batch while preserving its existing answers (bead `coding-harness-bxxt.21`, frontmatter batch log). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `68066450`, the research identifies one `git log` process for each clean held document in `scripts/check_frontmatter_current.py`; the reported 6–16 seconds and roughly 893 files came from an external analysis and were not remeasured in that research. The equivalence of a batch with per-path Git history, especially around merges, renames and a subdirectory root, was not established (`research.md`, 2026-11-25).

## Acceptance criteria

1. When the date lookup in `reference_dates` runs, its dirty-set calls and history lookup start at most three Git processes regardless of the number of held documents, including at most one batched history invocation and no per-document Git fallback; preflight and held-file enumeration are outside this count.
   *Refuted by:* four processes, or a per-document Git invocation as the held set grows.

2. When a clean held document has history, its reference date and short hash equal `git log -1 --no-merges --format='%cs %h' -- <path>` from the same root with literal pathspecs enabled and `log.follow` forced to `false` for both calls while retaining all other Git configuration.
   *Refuted by:* a different date or hash after a rename, merge, subdirectory root, or for a name containing `*`, `?`, `[` or a leading `:`.

3. When a held document is modified, staged or untracked, its reference is today's local date labelled `uncommitted`.
   *Refuted by:* a dirty document dated by a commit or labelled with its hash.

4. When a successful batch does not date a clean held document, the check exits 3 with the existing `git log cannot date <file>: no commit changed it` diagnostic for that document.
   *Refuted by:* a pass, another exit code, or a changed path or diagnostic.

5. When the batched history invocation fails, the check exits 3 with one diagnostic naming the command and its stderr, without blaming a document; stderr is bounded to the last 20 lines and 2,000 characters, with a truncation marker when cut, without redaction.
   *Refuted by:* a different exit code, a missing command or stderr, an exceeded bound, a missing truncation marker when cut, redaction, or a diagnostic assigning the failure to a file.

6. When the check or stamp runs, its findings, output, exit status and document changes match the existing behavior for the same inputs, except for literal path matching, disabling `log.follow`, and batch failures specified above.
   *Refuted by:* a changed stale line, verdict, exit status or stamped byte outside those exceptions.

7. When the pull request is prepared, it records five runs of each gate version on the same checkout and machine, running the base commit's complete `scripts/` directory exported with `git archive` to a temporary directory and its gate script with `--root` pointing at that checkout, with each runtime and outcome and both medians; all runs must succeed.
   *Refuted by:* fewer than five runs per version, different checkout trees or machines, a missing median or runtime, an incomplete base `scripts/` export, or any failing run.

8. When the change is proposed to ship, its measured gate runtime is at most half the before runtime under that same-commit, same-machine method.
   *Refuted by:* an after runtime greater than half the before runtime; the lane stops and reports instead of shipping.

## Non-goals

- Changing which documents are held, date policy, the stamp, gate configuration or command-line interface.
- Optimizing the second held-file enumeration or other verification gates.
- Changing Git history semantics beyond literal path matching to obtain a speedup.

## Protected areas

`provenance.yaml`, `decisions/gates.yaml`, `.github/workflows/ci.yml` and `docs/governance/gate-catalog.md` remain untouched: the gate's scope and integration do not change.

## Definition of Done

- `make verify` green; the pull request records the same-commit timing and its outcomes, including the halving threshold.
- Changed documents, models and ADRs outside this change folder: none.
- The protected areas are untouched and the non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.21` (frontmatter batch log), and its last commit carries `Closes-Bead: coding-harness-bxxt.21`.

## Open decisions

[DETAIL] The implementation appetite is four hours, including repairs; it is a reversible stop point for this bounded change. The timing comparison uses the median of five runs per version to limit noise; the individual runs and failures remain visible (decisions.md D-11). No maintainer decision is open.
