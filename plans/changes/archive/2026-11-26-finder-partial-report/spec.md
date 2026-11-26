---
title: "Spec — finder-partial-report"
status: accepted
implementation_status: done
date: 2026-11-19
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm]
class: bounded
appetite: 4
adr_files: []
---

# Spec — finder-partial-report

Finder seats retain valid locator entries from their first readable answer while exposing rejected entries (bead `coding-harness-yd8w`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-19, research found that one malformed locator invalidates a whole finder answer and stops the run before map merge (`research.md`, Runner exploration). In the incident recorded in `decisions.md` Q-1, 36 of 102 entries lacked an exact reference, so the entire answer was rejected. The format was requested in the prompt and checked afterward, rather than enforced where supported (Q-3).

## Acceptance criteria

1. When a finder is launched through Claude Code, its call enforces the shared locator JSON Schema.
   *Refuted by:* a finder call missing the schema or using a different schema.
   *Basis:* decisions.md#Q-3.
2. When a finder is launched through Pi, its prompt includes the same locator JSON Schema.
   *Refuted by:* a Pi finder prompt omitting or differing from that schema.
   *Basis:* decisions.md#Q-3.
3. When a finder report is validated, the locator rules derive from the same schema used by the finder calls.
   *Refuted by:* a change to a schema rule is ignored by validation or a call receives a different rule.
   *Basis:* decisions.md#Q-3.
4. When a process-successful first answer has the four nonempty category lists but contains malformed entries, every valid entry and no malformed entry reaches map merge without another finder call.
   *Refuted by:* a valid entry is lost, an invalid entry reaches merge, the merge stops solely because entries were dropped, or a correction is requested.
   *Basis:* decisions.md#Q-2.
5. When an entry is not an object, has missing, extra or invalid fields, or has a required string consisting only of whitespace or empty, that entry is dropped and its own validation errors are recorded.
   *Refuted by:* an invalid entry is retained or a dropped entry has no applicable error.
   *Basis:* decisions.md#Q-2; decisions.md, agent details S-1, S-2, S-4 and S-6.
6. When filtering removes every entry of a category, the retained report contains exactly `{"not_read": "every entry of this category was dropped by locator validation (finder-partial-report)"}` in that category, provided at least one entry of the answer survives (otherwise criterion 12 applies).
   *Refuted by:* an empty category, another marker, or a marker alongside a retained entry.
   *Basis:* decisions.md, agent detail S-7.
7. When entries are dropped, the published partial fence and manifest identify their finder seat, category, original entries and exact per-entry validation errors as filtered gaps.
   *Refuted by:* either record omits or misidentifies a dropped entry, category, seat or error, or represents it as retained evidence.
   *Basis:* decisions.md#Q-2; decisions.md, agent details S-1, S-4 and S-5.
8. When entries are dropped, they are excluded from the map's `gaps` and `not_read` lists except for the fixed marker for an emptied category.
   *Refuted by:* a dropped entry or its validation error is inserted into either map list.
   *Basis:* decisions.md, agent detail S-5.
9. When a filtered finder answer is stored, its outcome is `ok` and its dropped entries are recorded in a `filtered` list beside it.
   *Refuted by:* a different outcome or missing filtered details in the stored record.
   *Basis:* decisions.md, agent detail S-8.
10. When a run resumes with a reusable filtered finder record, it reuses the retained answer and publishes the same filtered gaps without launching that finder again.
    *Refuted by:* a repeat finder call, changed retained entries or missing or changed gaps on resume.
    *Basis:* decisions.md, agent detail S-8.
11. When a map is merged, the existing exact-union check uses the retained reports of all three finder seats.
    *Refuted by:* an added or missing retained locator or altered finder origin passes the check.
    *Basis:* research.md, Map merge; decisions.md#Q-2.
12. If the outer answer is invalid JSON, has duplicate keys or non-finite values, lacks exactly the four categories, or has a non-list or originally empty category, the existing invalid-report outcome stops the run before map merge. The same outcome stops the run when locator validation drops every entry of all four categories: criterion 6's marker applies only while at least one entry of the answer survives, so a seat never yields a map built from no located place.
    *Refuted by:* such an answer being accepted or reaching merge.
    *Basis:* decisions.md, agent detail S-2 and S-6; research.md, Finder stage; loop row L3-8 (fixed, `tests/test_stage2_swarm.py::test_finder_all_entries_dropped_stops`).
13. If a finder call fails or is refused, its existing failure or refusal outcome remains in force before map merge.
    *Refuted by:* a failed or refused finder being treated as successful or reaching merge.
    *Basis:* research.md, Run outcome; decisions.md#Q-2.

14. When a Claude finder call succeeds, the runner reads its JSON envelope's `structured_output` object and stores the serialized object as the answer, excluding the envelope.
    *Refuted by:* storing the envelope or result text, or failing to use the structured object.
    *Basis:* decisions.md, agent detail S-9.
15. If a Claude finder call exits successfully without `structured_output` and has not ended at a turn, budget or API limit, it is classified as an invalid report and stops before merge.
    *Refuted by:* accepting the answer or classifying it as a failed call.
    *Basis:* decisions.md, agent detail S-9.
16. If a Claude finder call exits nonzero or its result identifies a turn, budget or API limit before the model answered, it retains the failed-call outcome.
    *Refuted by:* classifying such a process or limit failure as an invalid report or accepting it.
    *Basis:* decisions.md, agent details S-9 and S-15.
17. When a filtered `ok` finder record is published as a partial fence, the fence contains its slot, outcome and filtered list without the raw answer.
    *Refuted by:* an omitted field or the raw answer in that fence.
    *Basis:* decisions.md, agent detail S-11.
18. When finder seats receive their prompt, all receive the same prompt with the shared schema appended and the same prompt hash.
    *Refuted by:* differing finder prompts or hashes, or a missing appended schema.
    *Basis:* decisions.md, agent detail S-12.
19. When the locator schema contains an unsupported keyword, validation refuses it rather than silently ignoring it.
    *Refuted by:* validation proceeding while ignoring an unsupported keyword.
    *Basis:* decisions.md, agent detail S-13.
20. When a non-finder Claude seat is launched, it retains text output format.
    *Refuted by:* a non-finder Claude call requesting JSON output.
    *Basis:* decisions.md, agent detail S-9.

21. When a Claude finder succeeds, its stored stdout is the serialized `structured_output` object; on every other path it contains only the envelope's `result` text or is empty.
    *Refuted by:* stored or published stdout containing the envelope, session ID or cost.
    *Basis:* decisions.md, agent detail S-14.
22. When finder validation checks an answer, it derives the outer shape as well as entry rules from the schema, and a violation inside a category array item is an entry fault while another schema violation is an outer fault.
    *Refuted by:* an outer schema rule being ignored or a violation being assigned to the wrong boundary.
    *Basis:* decisions.md, agent detail S-16.
23. If the schema file is missing, invalid JSON or contains an unsupported keyword, the run ends incomplete with a reason naming the file before any finder call starts.
    *Refuted by:* a finder call starting or the run blaming a finder or omitting the schema file from the reason.
    *Basis:* decisions.md, agent detail S-17.
24. When the schema contains `description`, `title` or `$schema` annotations, validation accepts and ignores them and the schema descriptions convey the exact-symbol-or-section reference rules, excluding line numbers, bare paths and prose.
    *Refuted by:* an annotation being rejected or enforced, or the reference guidance being absent from the schema seen by a finder.
    *Basis:* decisions.md, agent detail S-18.
25. When a locator field passes the schema's type, closed-field and non-whitespace checks, its path and reference form remains subject to existing merge resolution rather than new finder filtering rules.
    *Refuted by:* a nonblank locator being filtered solely for its path or reference form or bypassing existing merge resolution.
    *Basis:* decisions.md, agent detail S-19.
26. Before any finder call, the installed Claude Code must meet the declared minimum version for `--json-schema`; otherwise the run ends incomplete.
    *Refuted by:* a finder call starting with an older version or the run failing to report the minimum and installed versions.
    *Basis:* decisions.md, spec-review round 2 facts; findings.md, review row L3-3.

## Non-goals

- Accepting whole-file locators without an exact reference, selecting finder seats, changing topic or merge validation, or changing other failure policies.
- Finder retries, an ADR amendment, or structured output for all Pi and OpenCode Go calls; the latter is separate follow-up work (bead `coding-harness-fagu`, structured output for fixed-shape calls).
- Design phase 2b does not run for this bounded change.

## Protected areas

Security and leak checks, availability selection, model configuration and other change folders remain untouched; this repair is limited to finder report recovery and its format.

## Definition of Done

- Targeted tests and `make verify` pass.
- The finder map, runner, finder prompt, locator schema and their tests move with this spec and plan; no ADR or model changes.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes bead `coding-harness-yd8w`; its last commit carries `Closes-Bead: coding-harness-yd8w`.
- Special runs: none.

## Open decisions

None open.

- [DETAIL] The locator schema lives beside the finder prompt; a small interpreter refuses unsupported keywords, avoiding a dependency while preventing silent divergence.
- [DETAIL] The schema is appended to the shared finder prompt; descriptions retain the exact-reference guidance, and all seats retain one prompt and hash.
- [DETAIL] Claude finder answers use the structured output field; the envelope is excluded to avoid publishing session and cost data.
- [DETAIL] The filtered success fence contains only slot, outcome and filtered entries; the retained answer already appears in the map.
- [DETAIL] Required strings must contain a non-whitespace character, so whitespace cannot masquerade as a usable value.
- [DETAIL] Schema category names are checked against the merge categories so the existing merge contract cannot silently diverge.
- [DETAIL] The four-hour phase-4 appetite includes repairs; no appetite was stated and this is a bounded runner change.
- [DETAIL] Duplicate JSON keys and non-finite values invalidate the outer answer: the existing parser cannot identify a reliable entry boundary after rejecting them.
- [DETAIL] The fixed marker is attributed to the finder seat in the retained report; the existing merge treats the runner-supplied marker as report data, preserving its exact-union contract.
