---
title: "Spec — ratchet-mutation-evidence"
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
tags: [spec, mutation-coverage, ratchet]
class: bounded
appetite: 1
adr_files: []
---

# Spec — ratchet-mutation-evidence

The mutation-coverage checks in `tests/test_ci.py` count a gate as covered
only by a mutation-named test that reaches the gate's script, not by a file
that mentions it (bead coding-harness-a05; the maintainer's option B,
2026-10-21, `decisions.md` Q-1). Research: `research.md`.

## Acceptance criteria

1. A test file that names a gate's script, but whose mutation-named tests do
   not reach it — a mention in another test, a comparison against a command,
   a read of `<module>.__file__` — is no evidence for that gate.
   *Refuted by:* `_evidence` returning a test for such a file (red against
   the mention rule of `f8a6b33`).
2. A mutation-named test that reaches the script is evidence: a call into
   the imported module, the same through an alias, a name imported from the
   module, a path constant run through a helper chain of the same file, a
   command list naming the script path.
   *Refuted by:* one of these five shapes returning no evidence.
3. The coverage check and the ratchet decide with the same rule; on this
   repository every gate outside `OHNE_MUTATIONSTEST` has evidence and no
   gate inside it has.
   *Refuted by:* `test_every_gate_step_has_a_mutation_test` or
   `test_the_mutation_ratchet_only_turns_one_way` red on the tree.
4. The `ramp-valves` gate, whose evidence was only mentions, has a seeded
   red run: a valve that is due and still open makes `ramp_valves.py` exit 1.
   *Refuted by:* `ramp_valves.main()` returning 0 with a due valve.
5. The exemption list does not grow: `OHNE_MUTATIONSTEST` keeps its seven
   entries of `f8a6b33`.
   *Refuted by:* an added entry in the diff.

## Non-goals

- Real mutation testing (running each test against a mutated script).
- Following pytest fixtures, `conftest.py` or helpers in another file.
- Judging whether a reaching test asserts the red run; the name rule
  `MUTATIONS_NAMEN` stays as it is.
- Removing the plans-registry exemptions; their seeded red run is still
  outstanding.
- Translating the existing German identifiers of the section.
- Constructs written to fool the static reading (maintainer, 2026-10-26,
  phase-6 rows R10-1 and R10-2): a command variable reassigned in every
  branch before the call, and a helper default evaluated at import time.
  Evidence taken from the run itself is follow-up work
  (coding-harness-4ft9).

## Definition of Done

- The criterion-1 test red against the mention rule before the edit.
- `make verify` green apart from the environment-only reds named in
  `findings.md`.
- The last commit carries `Closes-Bead: coding-harness-a05`.

## Open decisions

None open.

- [DETAIL] D-1 to D-4 in `decisions.md`: one predicate for both checks; the
  five shapes read from one file's syntax tree; a seeded red run for
  ramp-valves instead of an exemption; English names for new code.
