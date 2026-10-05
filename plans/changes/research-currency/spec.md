---
title: "Spec — research-currency"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-pu9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, docs-research, drift-job, frontmatter]
class: bounded
---

# Spec — research-currency

Part 1 of bead coding-harness-pu9: a nightly list of the research notes whose
last review is too old. Inputs: [`research.md`](research.md) (read at
`87daf91`) and [`decisions.md`](decisions.md). The class is `bounded`, as
the maintainer answered on 2026-10-05 (`decisions.md`, `[DECISION] 1`).

## Problem

The research under `docs/research/` assesses outside tools — CrewAI releases,
the Agent SDK's terms, Omnigent — that change without a commit here. Nothing
says when a note was last checked against its sources and is due again:

- Every note carries `last_reviewed:`, but nothing reads its age. The one age
  rule in the repository covers `plans/` only (`scripts/plans_registry.py`,
  `STALE_AFTER_DAYS = 90`); `scripts/check_docs.py` checks only that the key
  exists (research 1.2).
- `updated:` cannot stand in: it moved on 12 notes on 2026-09-29 with a stamp,
  while their reviews did not (research 1.1).
- The planned re-check agent (part 2) needs to know which note is the oldest,
  in a form it can read without parsing prose (research 1.9).

On 2026-10-05 the oldest review is 19 days old (four notes reviewed
2026-09-16), so on that day the list is empty — and must still say so.

## Terms

- **Note** — a Markdown file under `docs/research/` that the list covers
  (criterion 1).
- **Review date** — the date in a note's `last_reviewed:` (criterion 2).
- **Due** — a note whose review is too old, or whose review date is unusable
  (criteria 3 and 4).
- **The day of the run** — the date the ages are counted to (criterion 6).

## Acceptance criteria

Each criterion holds one condition and names what refutes it. "A fixture"
means a tree the test builds in a temporary directory.

1. **The notes.** The list covers every `*.md` file under `docs/research/`,
   at any depth, whose file name does not start with `_`, and nothing else.
   *Refuted by:* a fixture in which `_INDEX.md`, a non-Markdown file or a file
   outside `docs/research/` is listed, or a note in a subdirectory is not.

2. **The review date is `last_reviewed:`.** It is the top-level
   `last_reviewed:` of the note's YAML header, as a `YYYY-MM-DD` date, quoted
   or not. `updated:`, `created:`, the provenance block `review:` and the git
   history are never consulted.
   *Refuted by:* a fixture note with an old `last_reviewed:` and a recent
   `updated:` that is not due, or one with a recent `last_reviewed:` and an
   old `created:` that is.

3. **Due by age.** A note is due when its review date lies more than 90 days
   before the day of the run. At exactly 90 days it is not due. The 90 is
   one named constant in the script.
   *Refuted by:* a fixture note at 91 days that is not due, or one at 90 days
   that is.

4. **An unusable review date makes a note due, with the reason.** No header,
   a header that is not a YAML mapping, no `last_reviewed:`, an empty or
   `null` value, a value that is not a date, a date later than the day after
   the day of the run, and a file that cannot be read as UTF-8 each make the
   note due, with a reason naming the case; the run goes on to the next note.
   A date on the day after the day of the run is usable.
   *Refuted by:* any of these fixture notes not due, due without its reason,
   or ending the run; a note dated the day after being due.

   *Amendment 2026-10-05 (repair round 1, finding F-3; appended, nothing
   renumbered):* a header with two top-level `last_reviewed:` keys is one more
   case of the list: the note is due, with a reason saying the key stands twice
   — whichever the dates, whichever the order, since which of the two is meant
   cannot be told (`scripts/check_frontmatter_current.py` refuses a doubled
   `updated:` for the same reason). Only a key at the top level counts: a
   `last_reviewed:` inside the `review:` block is not the review date.
   *Also refuted by:* a fixture note with two top-level `last_reviewed:` keys
   that is not due, or whose date is the first or the last of the two.

5. **The order.** Notes with an unusable review date come first, then the
   others by review date, oldest first; ties, and the unusable ones among
   themselves, by path. The same tree and the same day of the run give
   byte-identical output.
   *Refuted by:* a fixture in which a younger note precedes an older one, a
   tie not ordered by path, or two runs whose output differs.

6. **The day of the run** is the running machine's local date, unless
   `--today YYYY-MM-DD` names it.
   *Refuted by:* a run with `--today` whose output depends on the clock, or a
   run without it whose ages are not counted to the local date.

7. **The text output** — the default — names in its first line the number of
   notes, the number due, the threshold and the day of the run; then one line
   per due note with its review date (or that it has none), its age in days
   where known, its path and, for an unusable date, the reason; then one line
   naming the oldest note — the first in the order of criterion 5 — with its
   review date and age, also when no note is due.
   *Refuted by:* a run over a fixture without due notes that does not name
   the oldest note, or a due note without its line.

8. **The JSON output** (`--format json`) is one object: `schema_version: 1`,
   `today`, `threshold_days`, `corpus` (`"docs/research/"`) and `notes` —
   every note, due or not, in the order of criterion 5, each with `path`
   (relative to the repository root, `/`-separated), `last_reviewed` (an ISO
   date, or `null` when unusable), `age_days` (an integer, or `null` when
   unusable), `due` (a boolean) and `problem` (the reason, or `null`).
   *Refuted by:* output that `json.loads` refuses, a missing key, a note
   missing, or `notes` out of order.

9. **The job summary.** When the environment variable `GITHUB_STEP_SUMMARY`
   names a file, the run appends to it a Markdown section with the facts of
   the text output — or the "not measured" line of criterion 10. Without the
   variable it writes no file.
   *Refuted by:* a run with the variable set that leaves the file unchanged,
   or a run without it that creates a file.

10. **Never red over its content.** The run exits 0 whenever it produces the
    list, however many notes are due. It exits 3 with a line beginning
    `research-currency: not measured` when `docs/research/` is not a
    directory or holds no note — an empty list there would be a measurement
    of nothing.
    *Refuted by:* a fixture with due notes exiting non-zero, or a fixture
    without `docs/research/` or without a note exiting 0.

11. **It only reads.** Apart from the job summary of criterion 9 the run
    writes nothing, and it needs neither git, nor the network, nor the
    tracker.
    *Refuted by:* a fixture whose files differ in any byte after a run, or a
    run that fails in a directory that is not a git work tree.

12. **The gate.** `decisions/gates.yaml` carries `research-currency` with
    the command `python3 scripts/check_research_currency.py`, job `drift`,
    enforcement `report`, `floor: false`, placement `both`, and neither
    `needs_tracker` nor `needs_history`; its reason says `report` is the
    level the maintainer chose, not a step towards `block`.
    `.github/workflows/ci.yml` is regenerated: its `drift` job runs the step
    with `continue-on-error: true`, its `verify` job does not run it.
    *Refuted by:* `ci-drift` red, the step in the `verify` job, or the step
    without `continue-on-error: true`.

13. **No ratchet grows.** The script has a caller (the generated workflow), a
    test, and mutation evidence — a test whose name matches the pattern of
    `tests/test_ci.py` (`MUTATIONS_NAMEN`) and which fails when a due note is
    not listed. `OHNE_AUFRUFER`, `OHNE_TEST`, `OHNE_MUTATIONSTEST` and the
    kit's `REIST_NICHT` are unchanged.
    *Refuted by:* `tests/test_ci.py` red, or any of the four lists longer.

14. **The kit carries it.** `scripts/check_research_currency.py` and
    `tests/test_research_currency.py` have the role `mechanismus` in
    `scripts/kit/manifest.yaml`. The tests build their own trees and read no
    note of this repository, so they hold in the probe's copy.
    *Refuted by:* `probe.rolle` giving another role for either file, or the
    gate `leerprobe` red.

15. **On this repository.** Run on the commit that introduces it, on any
    day before 2026-12-16, the script exits 0, lists no note as due, and
    names `docs/research/2026-09-16-review-corpus-vs-running-workflow.md`
    (reviewed 2026-09-16) as the oldest. `make verify` stays green.
    *Refuted by:* another exit code, a due note, another oldest note, or
    `make verify` red.

16. **The meaning is written where readers look.** `docs/research/_INDEX.md`
    says, in one paragraph, that a note's `last_reviewed:` is the day its
    content was last checked against its sources — an edit moves `updated:`,
    not this — that whoever re-checks a note sets it, and that the nightly
    `drift` job lists the notes whose review is more than 90 days old
    (`scripts/check_research_currency.py`).
    *Refuted by:* `_INDEX.md` without that paragraph, or one that contradicts
    criteria 2 or 3.

## What part 2 may rely on

Written for the re-check agent, which is not built here; its runner waits for
bead coding-harness-6hx. Nothing in this section is a criterion of this
change beyond criteria 1–10.

- **Its input** is `python3 scripts/check_research_currency.py --format
  json`. `notes[0]` is the oldest note — a note with an unusable review date
  before any dated one. Whether part 2 takes only due notes or the oldest
  regardless is part 2's decision; the list carries every note so that it
  can do either.
- **Its effect on the list** is the review date. A re-check that is merged
  sets the note's `last_reviewed:` to the day of the re-check, in the same
  pull request as its addendum — `updated:` moves too, as the gate
  `frontmatter-current` already demands. The note then leaves the due list
  and the head of the order.
- **The form is versioned.** A change to a key or its meaning raises
  `schema_version`.

## Non-goals

In this change, not now:

- **Part 2** — the re-check agent, its prompt, its runner, its schedule, any
  web access, any pull request opened by a machine.
- **Anything red** — no `block`, no valve towards it, no exit code that
  depends on how many notes are due.
- **Other folders** — `docs/architecture/`, `docs/adr/`,
  `docs/governance/`, the handovers; `plans/` keeps its own age rule.
- **New header fields or exemptions** — a per-note threshold, a "frozen"
  marker, an exemption by `status:` for superseded or deprecated notes (rule
  RB-S4's pointer pages).
- **Editing any note's header** — no `last_reviewed:` is set or moved by this
  change or by the script.
- **The maintainer's display and notifications** — `tools/claude-code/`, an
  issue, a message; a job summary for other gates (bead coding-harness-1jg.4).
- **Sharing code** — the constant and the header reader stay out of
  `scripts/plans_registry.py` and `scripts/check_frontmatter_current.py`.
- **Link checking and translation** of the notes.

## Open decisions

### `[DECISION]`

None open. `[DECISION] 1` — the class — is answered: the maintainer chose
`bounded` on 2026-10-05 ("small addition to the nightly job: turns nothing
red, decides nothing; the ADR question belongs to part 2";
`decisions.md`, addendum 2026-10-05). Had the answer been "option 2", the
header would have become `class: feature` with `change: research-currency`
and an ADR proposal; it was not.

### `[GAP]`s — closed by reading

- **The phase gate.** `scripts/validate_change_artefacts.py` does not exist;
  `python3 scripts/plans_registry.py --check` stands in, as for
  `harness-decide-adr` (research 1.8).
- **How report-only is declared.** `enforcement: report`, which the generator
  turns into `continue-on-error: true` (research 1.4).
- **What a new script owes.** A caller, a test and a mutation test, or the
  ratchets in `tests/test_ci.py` go red (research 1.5).
- **What reaches the maintainer today.** The run page only; no job summary,
  nothing in the display (research 1.7).

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change.

- **90 days, "more than".** The one age rule the repository already has for
  `last_reviewed:` (`plans_registry.py`, documented in `plans/_README.md`):
  one number for one field. A month — the pace at which the assessed tools
  change (`docs/architecture/target-architecture.md`, constraint C3) — would
  list the first notes on 2026-10-17 and every note of today's corpus by
  2026-11-05, and a list where everything is due stops saying which note
  matters. Changing it is one constant.
- **Its own constant.** `STALE_AFTER_DAYS` by the same name, but not imported
  from `plans_registry.py`: a change to the plans rhythm should not move the
  research rhythm silently.
- **"Reviewed" means `last_reviewed:`.** `updated:` records edits and stamps
  (research 1.1); `review:` is the provenance sign-off; git dates record
  edits too.
- **`_INDEX.md` is not a note**, nor is any `_`-prefixed file: the index is a
  reading map, not a source review; `plans_registry.py` skips such files the
  same way.
- **The German intake documents age like any note.** The maintainer's
  wording is "the research under `docs/research/`", without exception;
  nothing marks a note as frozen, and listing one costs one line. Whether
  part 2 re-checks them is part 2's question.
- **An unusable date is due and sorts first.** An unknown age is treated as
  the oldest — an unreadable value is a finding, not a reason to skip
  (`plans/_README.md`).
- **One day of slack for a future date**, as `frontmatter-current` allows:
  the nightly run is in UTC, a review is dated in the maintainer's time zone.
- **Exit 0 over any content, exit 3 when nothing was measured.** "Never red"
  covers the list; `enforcement: report` keeps the job green even on exit 3,
  which marks only the step. A list over a missing corpus would claim a
  measurement that did not happen (rule RB-G7: an empty set is no result).
- **Where it shows: the step log and the job summary.** The run page is where
  the maintainer chose to have it; the summary puts it on that page without
  opening a log. Part 2, once built, is the channel that comes to the
  maintainer — as a pull request.
- **The JSON carries every note**, not only due ones, so part 2 can choose
  without a second run.
- **`--today`** makes the output a function of the tree and one date, which
  is what "deterministic" asks; the tests and part 2 can pin it.
- **Kit role `mechanismus`** for the script and its test, for the reason the
  sibling gate gives: the gate file travels, so its script does. In a
  repository without `docs/research/` it says "not measured", which is true.
- **Names:** script `scripts/check_research_currency.py`, gate
  `research-currency`, test file `tests/test_research_currency.py` — the
  `check_*` form of the sibling checks.
- **Phase 2a not run:** it is optional; sixteen criteria each carry their
  refutation, and phase 6 reads the result against them.
