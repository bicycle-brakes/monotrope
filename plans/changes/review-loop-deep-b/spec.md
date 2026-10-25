---
title: "Spec — review-loop-deep-b"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: to be filed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 2
adr_files: []
---

# Spec — review-loop-deep-b

The review-loop runner keeps a round when a replacement is refused or never
starts, applies the maintainer's exclusions everywhere it selects, names
every member's words, scrubs every key of the secrets file, leaves no
reviewer running after an interruption, and reads catalog ids and header
rows strictly (deep review part B, 2026-10-25). Research: `research.md`.

## Acceptance criteria

1. A Flash replacement that the declaration refuses at `checked_prompt` is
   named in the round as `<id> not admitted: <reason>`, is not called and
   not consumed, and the next unconsumed rung is tried; the round with the
   other members' rows is written (DL-B-1).
   *Refuted by:* no round written, a refused rung consumed or called.
2. A discovered free id that an `ausgeschlossen` entry names is dropped
   from the free selection and named with its reason; the other free
   members review (DL-B-2).
   *Refuted by:* the free stage refused whole, or the drop not named.
3. A paid model an `ausgeschlossen` entry names is not on the ladder, not
   in the Flash swarm, and `skipped_models` names it with its reason
   (DL-B-2).
   *Refuted by:* the model on the ladder or in the Flash stage.
4. Each kept non-row block of a round is preceded by a runner line
   `From <member>:`; the record still reads the quoted words as the
   reviewer's and the rows as before (DL-B-3).
   *Refuted by:* a kept block without its member, or a runner line read
   as a reviewer line.
5. Every value of the secrets file (at least `OPENCODE_GO_KEY` and
   `GLM_KEY`) is scrubbed from a reviewer's answer, its failure line and
   its printed standard error (DL-B-4).
   *Refuted by:* the `GLM_KEY` value in the loop record or on stderr.
6. When the runner is interrupted (`KeyboardInterrupt`) or terminated
   (`SIGTERM`), every running timed program's process group is killed
   before the runner exits; the interrupt propagates as before, SIGTERM
   exits 143 (DL-B-5).
   *Refuted by:* a launched program still running after the exit.
7. After a timeout kill, collecting the output waits at most
   `KILL_DRAIN_SECONDS` for a descendant that left the group (DL-B-6).
   *Refuted by:* the stop waiting out an escaped descendant.
8. A catalog id outside `[A-Za-z0-9][A-Za-z0-9._:/-]*` is never selected
   for the free stage and is named as dropped; `render_table` escapes an
   unescaped `|` in a cell (DL-B-7).
   *Refuted by:* such an id reviewing, or a `|` in a cell moving columns.
9. A replacement whose launch the round deadline prevents — checked after
   its leak check and again at launch — writes no call line and is not
   consumed (DL-B-10).
   *Refuted by:* `rung:<id>` consumed for a rung that never ran.
10. A table line whose cells after the first are the column names
    (Severity, Dimension, Origin, Where, Finding; any case) is furniture,
    whatever its first cell (DL-B-11).
    *Refuted by:* such a header read as a finding row.
11. The real `model-endpoints.yaml` excludes `kimi-k3-free`, `k3-free`,
    `kimi-for-coding` and `moonshot/k3`, and admits every declared paid
    model and no declared model is excluded (DL-B-12).
    *Refuted by:* a Kimi id admitted, or a declared model excluded.
12. A reviewer stopped by the round deadline is reported with the round
    limit and the seconds it was given, not as "45 minutes" (DL-B-14).
    *Refuted by:* "the reviewer time limit of 45 minutes" for a call that
    had less.
13. A catalog model definition crosses into Pi's active configuration
    with the fields `id`, `name`, `api`, `baseUrl`, `reasoning`, `input`,
    `contextWindow`, `maxTokens`, `cost`, and `provider` when it is the
    store's own provider, only; `samplingParams`,
    `headers`, `compat` and every other field are dropped, named on stderr
    at discovery, and the fetched store stays unchanged (RS-3-3 of the
    research-swarm review). `baseUrl` is not checked here (DL-B-8).
    *Refuted by:* a `samplingParams` model or a catalog header in
    `models.json`.
14. A catalog header value that is not a string does not break activation
    (RS-3-8).
    *Refuted by:* an exception from `activate_overlay`.

## Non-goals

- DL-B-8, DL-B-9, DL-B-13: open questions for the maintainer
  (`decisions.md`, `findings.md`).
- The DL-A rows (another change, `fix/review-loop-deep-a`).

## Known limits (2026-10-25)

- A refused rung stays in the snapshot: its own later round is refused by
  the declaration as before; `release-loop --stage-failed` retires it.
- Between the deadline check and the launch a call line can still be
  written for a replacement `remaining()` then refuses; it is not
  consumed, and the round names it.
