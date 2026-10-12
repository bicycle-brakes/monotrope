---
title: "Spec — provenance-location"
status: draft
implementation_status: partial
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, provenance, adr-answers, kit]
class: bounded
appetite: 2  # hours of phase 4, repair rounds included — a stop, not an estimate
---

# Spec — `provenance-location`

After this change, the command `python3 scripts/harness.py decide adr` also
works in an instance that keeps its provenance map at
`decisions/provenance.yaml`, and refuses when an instance holds a map at both
places (bead coding-harness-3ar.1; package 1 of
`docs/research/2026-10-11-adr-answer-pin-plan.md`). Research:
[`research.md`](research.md), read against `origin/main` on 2026-10-12.
Decisions: [`decisions.md`](decisions.md) — the search order is the
maintainer's answer to Q-1 of 2026-10-12.

## Problem

- The command looks for the map at one place only. `answering_role(root)`,
  the one read site of the map in the command, reads `root /
  "provenance.yaml"` (module constant `PROVENANCE`), and `main()` calls it on
  every run, before any question and any write (research, question 1;
  `scripts/harness.py` at `12d9aa9`).
- An instance whose map lies at `decisions/provenance.yaml` — LakeSwitch's
  does (read on GitHub on 2026-10-12, `decisions.md`) — therefore gets "cannot
  read provenance.yaml" before anything else is checked. It cannot use the
  command at all, and adding `roles:` to its map would not change that (pin
  plan, differences table, row 7).
- Nothing names a second place today: of the three ways this repository
  names a location — an option naming the tree, an environment variable, a
  key in a config file — none names the map (research, question 2). The
  maintainer chose a fixed search order over a setting (`decisions.md`, Q-1).

## Terms

- **The map** — the provenance map: a YAML file whose `paths:` entry for
  `decisions/answers/` names an `owner_role`, which `roles:` declares.
- **The two places** — `provenance.yaml` at the top of the tree, and
  `decisions/provenance.yaml` below it.
- **The tree** — the directory `--root` names; without `--root`, this
  repository.
- **Present** — something stands at the path: a file, a directory, or a
  symbolic link, also one that points nowhere.
- **Refuses** — exits 2, prints a line starting `refused:` and then "Nothing
  was written.", before any question is asked and before any file is
  written; in the terminal flow and in the recording flow (`--change`,
  `--answer`, `--reason`, `--stated-in`) alike.

## Acceptance criteria

"A tree" below is a git repository a test builds in a temporary directory,
with at least one feature anchor.

1. When the map is present at the top of the tree only, the command reads
   it: `answered_by` in the written answer is the role that map names, as
   today.
   *Refuted by:* a tree with only a top-level map that refuses, or whose
   written `answered_by` is another role.

2. When the map is present at `decisions/provenance.yaml` only, the command
   reads it: `answered_by` is the role that map names, in an answer recorded
   with `--change` and in one typed in the terminal.
   *Refuted by:* such a tree that refuses as if there were no map, or writes
   another role.

3. If both places are present, the command refuses, and its message names
   `provenance.yaml` and `decisions/provenance.yaml` and says to keep one of
   them — whatever the two hold: the same map twice, a map beside a file that
   is not YAML, a map beside a directory, a link that points nowhere beside a
   map.
   *Refuted by:* a tree with both places present where the command asks,
   writes, exits other than 2, or names only one path; in particular one where
   a broken entry at one place lets the map at the other be read.

4. If neither place is present, the command refuses, names both places it
   looked at, and shows the entry to add (`prefix: "decisions/answers/"` with
   `owner_role:`), as the refusal does today.
   *Refuted by:* a tree without a map where the command asks, writes, or
   whose message lacks either place or the entry.

5. If the map found cannot serve — it cannot be read as YAML, it is not a
   mapping, it has no `paths:` entry for `decisions/answers/`, that entry has
   no `owner_role:`, or the role is not declared under `roles:` — the command
   refuses with today's message for that case, and the message names the map
   it read by its path from the top of the tree: `decisions/provenance.yaml`
   when that one was read, `provenance.yaml` when the top-level one was.
   *Refuted by:* any of these cases, at either place, where the command asks,
   writes, or exits other than 2; a message about a map at
   `decisions/provenance.yaml` that lacks that path; a message about a
   top-level map that names `decisions/provenance.yaml`.

6. If the map at `decisions/provenance.yaml` has the entry for
   `decisions/answers/` with an `owner_role:` but no `roles:` key at all —
   LakeSwitch's map today — the command refuses with today's message that the
   role "names no role under `roles:`", naming `decisions/provenance.yaml`
   and the line to add.
   *Refuted by:* such a tree where the command asks, writes, exits other than
   2, or whose message lacks `roles:` or the path.

7. When `--root` names a tree, the two places are looked for in that tree
   only, never in the working directory.
   *Refuted by:* a run from a working directory that holds a map naming one
   role, with `--root` naming a tree whose map at `decisions/provenance.yaml`
   names another, that writes the first role or refuses.

8. On this repository, which holds its map at the top only, the command still
   finds `framework-architect` as the answering role.
   *Refuted by:* the lookup on this repository refusing or giving another
   role — for instance once a `decisions/provenance.yaml` is added here.

## Non-goals

- **The other readers of the map.** `scripts/check_frontmatter_current.py`,
  `scripts/ramp_valves.py` and `scripts/stage2.py` (through the first) keep
  reading the top-level map only. They follow the order in a later change,
  once an instance needs one of them (`decisions.md`).
- **`scripts/check_adr_answers.py`.** It never opens the map (research,
  question 1), so it does not change, although the package statement names
  it.
- **A third place, or a place an instance configures** — an option, an
  environment variable, a key. The maintainer chose the fixed order and
  accepted that a third place needs a change to it (`decisions.md`, Q-1).
- **The shape of the map.** Which entry counts when two carry the prefix
  `decisions/answers/` (the first, as today), and what a role under `roles:`
  holds, stay as they are.
- **Texts that name the map.** The header comment of `provenance.yaml`, which
  names readers that do not hold today (`decisions.md`); the spec of the
  change `harness-decide-adr`, whose criterion 10 speaks of "the
  `provenance.yaml`" and stays true of this repository.
- **LakeSwitch's half** — adding `roles:` to its map (pin plan, row 7, its
  package 4), and a `paths:` entry for `decisions/answers/` whose
  `owner_role` names `architect`: this command reads only the entry for
  `decisions/answers/` (loop row L3-1); the pin plan's row 6 named
  `decisions/` until it was corrected with this change.

No design phase: a `bounded` change never runs 2b (`docs/WORKFLOW.md`,
"Change classes, the ADR question and decision pull requests").

## Protected areas

- `provenance.yaml` — `human-decided`; an edit would make this pull request
  a decision pull request (AGENTS.md, house rule 8).
- `scripts/check_adr_answers.py`, `scripts/check_frontmatter_current.py`,
  `scripts/ramp_valves.py`, `scripts/stage2.py` — the non-goals above.
- `scripts/kit/manifest.yaml` — `scripts/harness.py` and its test already
  travel as `mechanismus`, and the new tests build their own trees, so they
  hold in the probe's copy.

## Definition of Done

- `make verify` green.
- Moved in the same pull request: the module docstring of
  `scripts/harness.py`, which gains where the map is looked for. No other
  document states where the command reads the map (a search over `docs/`,
  `prompts/`, `templates/` and `scripts/kit/manifest.yaml` on 2026-10-12
  found none).
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list: `scripts/harness.py`,
  `tests/test_harness_decide_adr.py`, this change folder and the rendered
  `plans/INDEX.md`.
- Bead: the pull request closes coding-harness-3ar.1, and its last commit
  carries the trailer `Closes-Bead: coding-harness-3ar.1`
  (`prompts/07-commit.md`).
- Special runs: none.

## The ADR question

Not owed. Only a `feature` owes an answer (`docs/WORKFLOW.md`, "Change
classes, the ADR question and decision pull requests"); the header therefore
carries neither `change:` nor `adr_question:`, as no `bounded` spec in this
repository does, and `harness.py decide adr` refuses to record an answer for
a `bounded` change. Shown for the maintainer all the same — were it asked,
the proposal would be **no**, because the change widens where one command
looks for a file it already reads, in an order the maintainer fixed in Q-1,
and decides no boundary, format or interface that an ADR would need to hold.

## Open decisions

### `[DECISION]`

None open. Q-1, how the command finds the map, is answered (`decisions.md`).

### `[GAP]`s — closed by reading

- **The read site.** `answering_role` is the only one; `main()` calls it in
  both flows, after checking the recording options and before the git check
  and any question (research, question 1; `scripts/harness.py` at
  `12d9aa9`).
- **Who uses the constant.** `PROVENANCE` is used in `scripts/harness.py`
  only; no test names it (search over `tests/`, 2026-10-12).
- **Where the location is documented.** Nowhere outside the code (Definition
  of Done).
- **The phase gate.** `scripts/validate_change_artefacts.py` does not exist;
  `python3 scripts/plans_registry.py --check` stands in, as for the changes
  `harness-decide-adr` and `research-currency`.
- **The baseline.** `tests/test_harness_decide_adr.py` passes, 46 tests, at
  `12d9aa9`.

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change.

- **"Present" includes a directory and a link that points nowhere.** An
  entry someone put at one of the two places is meant as the map; reading
  the other place silently would be the hidden choice the refusal over both
  places exists to prevent, and deleting one entry undoes the refusal.
- **The refusal over both places does not compare contents.** The
  maintainer's rule is "when both exist"; two identical copies are still two
  files to keep in step.
- **Messages name the map by its path from the top of the tree.** With two
  possible places, whoever repairs the map must know which file is meant;
  the proposed entry text in the messages stays as it is.
- **The entry looked for is `prefix: "decisions/answers/"` wherever the map
  lies.** The prefixes of a map are paths from the top of the tree — this
  repository's are, and the pin plan names LakeSwitch's owner entry
  `decisions/` the same way; LakeSwitch's map itself was not read in this
  phase.
- **The order of checks in `main()` stays.** The recording options first,
  the map next, the git work tree after; no criterion asks to move them.
- **Appetite 2 hours.** One function and one parametrised test file; the
  stage-2 review loop's repair rounds are counted in.
- **Phase 2a not run.** It is optional for a `bounded` change
  (`docs/WORKFLOW.md`, "Which change gets what"); the eight criteria each
  carry their refutation, and phase 6 reads the result against them.
