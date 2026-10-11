---
title: "ADR answer — LakeSwitch switches to a pinned Coding Harness"
category: research
status: proposed
created: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-11"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, plan, adr-answer, pin, lakeswitch, decision]
---

# ADR answer — LakeSwitch switches to a pinned Coding Harness

First deliverable of bead coding-harness-3ar ("the principle research ->
interview -> decision -> ADR belongs to Coding Harness; the LakeSwitch pilot is
lakeswitch-ai #62"): a one-page plan, smallest version first. Coding Harness
facts read on 2026-10-11 at `origin/main` `99bbe02`; LakeSwitch facts read at
lakeswitch-ai `origin/main` `ce88eee` (2026-10-08). Rows marked *analysis*
come from a read-only comparison made on 2026-10-11 and were spot-checked, not
re-derived line by line. Nothing here is decided; the one open question is
the maintainer's.

## Target picture

LakeSwitch holds no code of its own for the ADR answer. It names one Coding
Harness commit in `harness.lock.yaml`, its CI proves the files it runs are
exactly that commit's, and the gate and the command it runs are Coding
Harness's (`scripts/check_adr_answers.py`, `scripts/harness.py decide adr`).
The answer files under `decisions/answers/<change>/adr.yaml` stay where they
are, in the one format both repositories already share (schema_version 1,
the same eight keys).

## As-is and to-be

| | As-is (2026-10-11) | To-be (by 2026-12-15) |
| --- | --- | --- |
| Coding Harness | Gate `adr-answers`, command `harness decide adr`, ADR 0008, merged in PR #54 (`ba940fb`, 2026-09-30); change `harness-decide-adr` stays `implementation_status: partial`; its finding F-6 (label, PR body, hosted run) is still "open — closes in phase 7" | Same mechanism, able to run in an instance; `harness-decide-adr` complete; F-6 closed |
| Pin | Nothing: no `harness.lock.yaml`, no verify-pin, no exporter. `scripts/export/manifest.yaml` has no reader and its catch-all `drop` leaves out both scripts; `scripts/kit/manifest.yaml` carries them | `harness.lock.yaml` in LakeSwitch names a Coding Harness commit; a verify-pin gate holds it |
| LakeSwitch | Gate M-31 (`decisions/gates.yaml` 345-362, entry `lakeswitch.adranswer:check`), `src/lakeswitch/adranswer.py`, `declared/adr_answer.py`, `declared/answer_pilot.py`, `cli.py cmd_decide_adr`, `tests/adranswer/`, `decisions/answers/pilot.yaml` (expires 2026-12-15); 13 answer files | All of these deleted; the 13 answer files pass Coding Harness's check at the pinned commit |

## SMART value

By **2026-12-15** (the pilot's expiry in `decisions/answers/pilot.yaml`),
lakeswitch-ai `main` has no gate M-31, none of the five LakeSwitch sources
listed above, no `pilot.yaml`; it carries `harness.lock.yaml` naming one
Coding Harness commit; its CI runs a verify-pin gate and the pinned
`adr-answers` gate green over all its answer files (13 at `ce88eee`). Measured
by a `git ls-tree` of lakeswitch-ai `origin/main` and its last CI run. This is
the bead's done-criterion: no second copy of the format. The date is at
risk after the decision of 2026-10-11 (see the addendum).

## The eleven differences

| # | Difference (*analysis*) | Migration step | Side |
| --- | --- | --- | --- |
| 1 | Gate seam: LakeSwitch expects a Python result, Coding Harness returns exit codes 0 / 1 / 3 | A thin adapter entry maps 0 → pass, 1 → fail with the printed lines, 3 → cannot measure | LakeSwitch |
| 2 | Empty tree: LakeSwitch reports nothing examined, not a pass; Coding Harness exits 0 with "examined nothing" | The adapter maps that line to LakeSwitch's nothing-examined verdict; LakeSwitch has features, so it does not arise today | LakeSwitch |
| 3 | Pilot expiry exists only in LakeSwitch | Deleted with the switch (`pilot.yaml`, `answer_pilot.py`); Coding Harness adds nothing | LakeSwitch |
| 4 | Anchor strictness differs | Dry run of the pinned check over LakeSwitch's anchors before the switch; anchors it refuses are repaired in LakeSwitch | LakeSwitch |
| 5 | Coding Harness requires `change` to equal the folder name | Same dry run; any answer file that differs is corrected | LakeSwitch |
| 6 | `answered_by`: LakeSwitch writes the constant `architect`, Coding Harness the `owner_role` from provenance `roles:` | LakeSwitch declares `architect` as the owner role of `decisions/`, so the written value stays the same | LakeSwitch |
| 7 | The Coding Harness command reads a root `provenance.yaml` with `roles:`; LakeSwitch has `decisions/provenance.yaml` without `roles:` — unchanged, the command refuses | Coding Harness lets an instance name where its provenance file lives (default unchanged); LakeSwitch adds `roles:` | both |
| 8 | What the command shows before recording differs | LakeSwitch takes Coding Harness's display; the `shown` key stays as schema_version 1 defines it | LakeSwitch |
| 9 | LakeSwitch runs its language check (M-6 / DL-5) on the commit message; Coding Harness does not | Stays a LakeSwitch rule, run by LakeSwitch's own commit check, not by the pinned command | LakeSwitch |
| 10 | LakeSwitch's messages cite its D-numbers | LakeSwitch accepts Coding Harness's wording (it cites ADR 0008); no instance numbers in framework text | LakeSwitch |
| 11 | Names: gate M-31 vs `adr-answers`, `lakeswitch decide adr` vs `harness decide adr` | `decisions/gates.yaml` points at the pinned gate; M-31 is retired with a note naming its successor | LakeSwitch |

## Work packages, smallest first

| # | Package | Size | Side | Waits for |
| --- | --- | --- | --- | --- |
| 0 | This plan | XS | CH | — (done) |
| 1 | Provenance location for instances (row 7, CH half) in `check_adr_answers.py` and `harness.py`, with tests | S | CH | nothing — touches only those two scripts and their tests |
| 2 | The full pin route, as decided on 2026-10-11 (addendum): bead coding-harness-s6i, then bead coding-harness-dj9 | L | CH | the decision; the merge of change criterion-test-ledger, which edits `decisions/gates.yaml`, `.github/workflows/ci.yml`, `scripts/kit/manifest.yaml`, `docs/WORKFLOW.md`, `prompts/03-plan.md`, `prompts/04-implement.md` and every `plans/changes/*/plan.md` |
| 3 | Dry run: pinned check over LakeSwitch's answer files and anchors (rows 4, 5) | S | LakeSwitch | package 1 |
| 4 | Switch: `harness.lock.yaml`, adapter, `roles:`, gate entry, verify-pin in CI (rows 1, 2, 6-11) | M | LakeSwitch | packages 2 and 3; its own session and change |
| 5 | Delete M-31, the five sources, `tests/adranswer/`, `pilot.yaml` (row 3) | S | LakeSwitch | package 4 green |
| 6 | `harness-decide-adr` to complete, close F-6, close bead coding-harness-3ar | XS | CH | package 5 merged; criterion-test-ledger merged (it edits that change's `plan.md`) |

Note for package 2: criterion-test-ledger introduces ADR 0013 (every
acceptance criterion names its proof) and a criterion-ledger gate that
travels with the kit. An instance that pins the whole kit receives that gate
too; a pin limited to the two ADR-answer scripts does not.

## Not now

- The full release route of bead coding-harness-dj9 (release builder,
  exporter with bundle digest, compatibility contract, upgrade assess) and
  its prerequisite bead coding-harness-s6i — superseded: the decision of
  2026-10-11 makes it the route (addendum).
- A reader for `scripts/export/manifest.yaml`.
- Any extension of the answer format beyond schema_version 1.
- Commit signing (Coding Harness decided against it on 2026-09-30, ADR 0008);
  branch protection; a hosted check of the `decision` label.
- Moving other LakeSwitch gates onto the pin.

## Open decision

`[DECISION]` Does LakeSwitch's switch wait for the full pin route (bead
coding-harness-dj9, which depends on bead coding-harness-s6i), or does Coding
Harness first build a minimal pin slice — a `harness.lock.yaml` naming the
Coding Harness commit plus the sha256 of each travelling file, and a
verify-pin gate that checks them?

- *Wait for dj9 and s6i:* one pin mechanism from the start, no format to
  migrate later; both beads are open with no estimate (2026-10-11), so
  meeting 2026-12-15 is uncertain and may need another decision PR moving the
  pilot's date; the whole kit, including the criterion-ledger gate, arrives
  with it.
- *Minimal slice:* small (package 2 at size S), fits the date; a second,
  interim lock format exists until dj9 replaces it, which costs one later
  migration in LakeSwitch; only the named files are pinned.

*Agent's recommendation (not decided):* the minimal slice, because of the
2026-12-15 deadline; its lock should name the commit and digests in a shape
dj9 can extend rather than replace.

## Addendum 2026-10-11 — the decision

The maintainer answered in the directing conversation on 2026-10-11:
"full pin" (in German: "Vollständiger Pin") — the switch waits for the full
pin route (release builder, `harness.lock.yaml` and verify-pin, bead
coding-harness-dj9; after the first slice of the harness foundation, bead
coding-harness-s6i); no minimal slice is built. The agent's recommendation above was not taken.

Consequences for this plan:

- Package 2 is the full route at size L: bead coding-harness-s6i first, then
  bead coding-harness-dj9. Bead coding-harness-3ar now depends on
  coding-harness-dj9 in the tracker.
- The "Not now" entry for the full release route no longer holds; it is the
  route.
- The 2026-12-15 date is at risk: both beads carry no estimate on
  2026-10-11. If the route cannot finish in time, moving the pilot's expiry
  in LakeSwitch takes a decision pull request there, early enough that gate
  M-31 never turns red.
- Package 1 (provenance location) is unchanged and still waits for nothing.
