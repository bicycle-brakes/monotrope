---
title: "Decisions — ratchet-mutation-evidence"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-a05
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# ratchet-mutation-evidence — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What counts as mutation evidence for a gate

context: |
  Topic: the mutation-coverage ratchet in tests/test_ci.py.
  Intention: on 2026-10-20 a call-site test (PR #188) named the
  plans-registry renderer only to identify a command, and the ratchet called
  both plans-registry exemptions stale (bead coding-harness-a05).
  Today: any test file that mentions a gate's script and holds some
  mutation-named test counts as that gate's evidence.
  Repository change: option A rewords the test line; option B makes the
  ratchet stricter.
  Architecture change: none.
asked: 2026-10-21, the conversation that reviewed PR #188
answer: "option A now (reword the test line) and option B tracked as bead coding-harness-a05: evidence for a gate is a mutation-named test that actually exercises a fault in that gate's script, not a bare mention anywhere in the file"
answered_by: maintainer
status: answered

In the context of the mutation-coverage ratchet, facing a mention of a
gate's script that emptied two exemptions without any seeded red run, we
decided that evidence for a gate is a mutation-named test that exercises a
fault in that gate's script, to achieve that the ratchet only shrinks when a
gate really gains a red run, accepting a stricter, syntax-based reading of
the test files. — 2026-10-21

Source: the maintainer's choice as recorded in the description of bead
coding-harness-a05 (created 2026-10-21); this session recorded it from
there and did not ask again.

## Details decided by the implementing session

- [DETAIL] D-1 · **One predicate for both checks.** The coverage test and
  the ratchet share `_evidence`; otherwise a gate could count as covered for
  one and uncovered for the other. The `tests/` subject keeps its rule from
  2026-09-08 (the file itself must hold a mutation-named test). Reversible.
- [DETAIL] D-2 · **"Reaches" is read from the syntax tree of one file.** A
  mutation-named test counts when it, or a module-level helper of the same
  file it calls at any depth, uses the script in one of the five shapes in
  `research.md`. `<module>.__file__` and other dunder reads, comparisons,
  docstrings and fixtures do not count. Reason: every genuine case measured
  on 2026-10-25 has one of these shapes, and the bead's example names
  exactly "imports or runs the script". Reversible.
- [DETAIL] D-3 · **ramp-valves gets its seeded red run instead of an
  exemption.** Under the stricter rule it is the one gate without evidence.
  `OHNE_MUTATIONSTEST` says it "may shrink, never grow" and "whoever adds a
  gate writes its mutation test", so the session wrote
  `test_the_ramp_valve_gate_goes_red_when_a_valve_is_due` rather than
  adding an entry. Reversible: the test can be removed and an entry added by
  a later decision.
- [DETAIL] D-4 · **New identifiers are English** (house rule 1); the
  existing German names around them (`OHNE_MUTATIONSTEST`, `_pruefling`,
  `ziel`, `quellen`) stay, since translating them belongs in a pull request
  of its own.
