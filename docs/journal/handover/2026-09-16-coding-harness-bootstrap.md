---
title: "coding-harness bootstrap — repository, tracker, separation plan — as of 2026-09-16"
category: handover
created: 2026-09-16
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: Cline
  version: "2026-09-16"
tags: [handover, bootstrap, migration, beads, separation]
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-09-29
---

# Handover — coding-harness bootstrap

Written in English because that is the decided direction for content
artefacts. This file is the first document of this repository and doubles as
the migration's anchor: every open item that conceptually belongs here but is
still tracked in `portfolio-agentic-engineering` is referenced from here by
full id. **No tracker items were imported** — one item, one tracker; the new
tracker starts empty except the beads created by this session.

## What this repository is

The source of truth for the coding workflow: seven phases, three stages, the
session handover, the kit that carries the process into new repositories, and
the research corpus. It splits one role out of
`portfolio-agentic-engineering`, which was carrying four at once (framework
governance, coding workflow, OSI→lakeswitch transfer logistics, domain
content) — a mixing its own architecture register documents (categories D and
E, measured 2026-09-15).

The three-repo topology after the separation:

| Repo | Role |
|---|---|
| `coding-harness` (here) | doctrine, prompts, templates, kit, model routing, research — later the template repository |
| `portfolio-agentic-engineering` | framework governance, transfer logistics, domain content |
| `lakeswitch-ai` | product repo, clean-room workflow instance — untouched by this migration |

## What this session did (2026-09-16)

- Created the private repository and cloned it to `~/coding-harness`.
- Bootstrapped the tracker with an **explicit prefix**:
  `bd init --prefix coding-harness --non-interactive`. Verified output:
  *Issues will be named: coding-harness-\<hash\>*. The prefix is not
  correctable afterwards (the failure mode behind
  `portfolio-agentic-engineering-wp-p0.1`).
- Set `git config beads.role maintainer` (silences the role warning,
  GH#2950) and `bd config set export.auto true` — the rendered export
  (`.beads/issues.jsonl`) now updates after writes without a separate render
  script.
- Confirmed the Dolt remote `origin` was registered automatically
  (`git+https://github.com/MPAdesso/coding-harness.git`); transport follows
  the `refs/dolt/data` model.
- Added `tools/bd` (version pin `1.1.2` in `tools/beads/VERSION`, refuses
  `init`/`migrate`/`upgrade`, escape hatch `BD_PIN_BYPASS=1`) — the
  guardrails exist from day one here, which portfolio never had.
- Laid the skeleton: `plans/changes/`, `plans/changes/archive/`,
  `plans/specs/` (empty, per the kit manifest's `geruest_ordner`),
  `docs/journal/handover/`, `docs/research/`, house `AGENTS.md` (English),
  `README.md`.
- Deliberately **no** `ci.yml` yet: an empty gate list would be a claim
  without content. It arrives with the first mechanism files (Phase 3.2),
  then holds exactly the gates those files need — one list, per repo.

## The separation plan (agreed with the maintainer)

Phases, each measured (Leerprobe `scripts/kit/probe.py` from portfolio +
`make verify` in both repositories), each moving ownership completely —
never copying:

1. **Phase 2 — research corpus intake** into `docs/research/` (lowest
   coupling, highest volume; this is what burst portfolio's frame).
2. **Phase 3 — mechanism migrates**, in order: templates → validators
   (`validate_change_artefacts.py`, `plans_registry.py`) → kit → cc-routing
   (`cc-*.sh`, `model-endpoints.yaml`) → prompts → `docs/WORKFLOW.md` last.
3. **Phase 4 — portfolio becomes a consumer**: mechanism files removed there,
   references rewritten, `zfyv` closed with a pointer here.
4. **Template switch** only after the Leerprobe sits at roughly ≥95 % and one
   full seven-phase run has happened in this repository.

## Open items — referenced, not imported

These live in the portfolio tracker and stay there until closed:

| Bead | State 2026-09-16 | Bearing on this repo |
|---|---|---|
| `portfolio-agentic-engineering-zfyv` | in progress | the workflow establishment this repo inherits; closes with a pointer here at Phase 4 |
| `portfolio-agentic-engineering-uqvm` | open | first full seven-phase run with metrics — its successor should run HERE, on real work |
| `portfolio-agentic-engineering-kmwa` | open | stage-2 keys and endpoints (`~/.config/cc-routing/secrets.env`); blocks nothing here |
| `portfolio-agentic-engineering-69il` | being fixed 2026-09-16 | the WORKFLOW §2 gate-sentence defect must be fixed BEFORE step 3.6 moves the file |
| `portfolio-agentic-engineering-wp-p3.7.2` / `-wp-p3.7.4` | open | skills-drift and tracker-drift gates — patterns to do better here, not to copy blindly |

## Standing constraints

- **English** for content artefacts, commit messages and PR bodies.
- **One writer per tracker.** A parallel session was working in portfolio
  during this bootstrap (the 69il fix and the #159 merge); portfolio was only
  read, never written.
- **The customer instance stays out of bounds** — requirements travel, never
  expressions.
- `docs/WORKFLOW.md` numbers carry their cut-off: everything measured there
  says *measured 2026-09-15, af09f8e*; after the move, re-measure instead of
  carrying stale counts.

## What to do first, next session

1. Check whether PR #159 (readability pass) and the 69il fix landed on
   portfolio master — both gate migration step 3.6.
2. Start Phase 2: intake the research corpus into `docs/research/`.
3. Keep this handover's table honest: when a portfolio bead closes, strike
   the row here with its closing date.

---

## Migration state — appended 2026-09-16, evening session

- **Phase 2 done** (commit `b15592a`): the three research documents carry
  frontmatter; `docs/research/_INDEX.md` added; provenance classes are
  `ai-drafted-reviewed` with review pending — the maintainer corrects a
  class where the hand differed. `coding-harness-anw` closed.
- **Phase 3 done** (commit `5efe809`): the 24 mechanism entries of
  portfolio's kit manifest adopted from portfolio master `4ce8240` — which
  already carried the 69il fix (PR #160) and the readability pages
  (PR #159). Deliberate deviations: no `ci.yml` yet (`coding-harness-bo0`),
  `.beads/issues.jsonl` stays this repository's own export.
- **Measured baseline** (portfolio venv, 2026-09-16): `pytest tests/ -q` =
  **64 failed, 182 passed, 4 skipped**; with `tests/test_kit.py` excluded it
  reads 167 passed, 60 failed. Classes of the 60: 27 `test_ci` (bo0), 21
  `test_regelwerk`, 11 `test_feedback_channel`, 1 `test_model_endpoints`
  (`.claude/agents`, seam 1). The four red kit tests:
  `test_every_tracked_file_has_a_role`,
  `test_the_kit_list_is_not_derivable_from_the_export_list`,
  `test_the_two_manifests_really_disagree_somewhere`,
  `test_the_role_check_goes_red_when_a_rule_is_removed`. The Leerprobe is
  the acceptance run for this migration.
- **Phase 4a/4b opened in portfolio:** PR #162 (branch
  `docs/sever-pointers-coding-harness`) carries ADR-032, the AGENTS.md
  banner, the rendered adr index **and the Phase-4b severance** (the
  mechanism copies removed there; per-gate decisions applied:
  plans/plans-drift/ramp-valves rebuild as portfolio-owned copies,
  kit-probe dropped, pytest kept without the six mechanism test files,
  ci_gates.py kept). Not merged; the maintainer's merge is the acceptance.
- **Live reproduction of portfolio's wp-p0.1:** `bd create` produced
  short-prefix ids (`portfolio-vevj`, `portfolio-prrw`, `portfolio-lcb8`)
  in a worktree and in the main checkout — with `issue-prefix` correctly
  set in `config.yaml`, and with `BD_ISSUE_PREFIX` set as well and **not
  honored**. Documented in PR #162's description. The branch head's export
  is clean: none of the three reaches master through PR #162.

---

## Session state — appended 2026-09-16, late evening, measured at `4ffe21d`

The session that carried this file's pull request through two review rounds
ended without writing a handover. This section reconstructs the state from
git, the tracker and the pull-request pages, and re-measures every number
below at branch head `4ffe21d` (on `main` head `5a950c2`) unless a line
names another commit. Working tree clean, nothing stashed, every branch
pushed, no tracker item in progress.

### Three pull requests in flight here — all open, none merged

| PR | Branch | Latest review (UTC) | Verdict |
|---|---|---|---|
| #1 | `docs/bootstrap-handover-migration-state` (this file) | 21:01, round two | mergeable; four non-blocking findings, resolved below |
| #2 | `docs/research-review-corpus-vs-workflow` | 21:34 | mergeable after four text corrections |
| #3 | `docs/target-architecture` | 21:34 | not mergeable; four blocking findings |

**PR #2, the four corrections:** the review argues the prefix defect from an
unverified premise, although portfolio's `scripts/bd_neu.py` (present at
`4ce8240`) documents the cause — an eight-character cap in `bd rename-prefix`
and a database configuration holding `portfolio`, neither worktrees nor
directory names; the history table of the toolchain document has three rows
dated 2026-09-17, not four; SBOM lives in toolchain §8.4, not §8.6; and the
rule-set line "Was gilt, nicht was wünschenswert wäre" is paraphrased as a
quotation. The review also proposes team levels T0–T4 while PR #3 records
T0–T2 — the two documents disagree on the one vocabulary D-1 was meant to
settle.

**PR #3, the four blocking findings:** the document claims seventeen
decisions "decided in interview" while its review block is unsigned
(`approved_by: null`) — the maintainer signs, or the status line reads "as
recorded by the session, unconfirmed"; the pull-request text describes the
first of three commits, not the head; the document contradicts its own counts
(§4 "six decisions" lists S1–S8, §5.1 "eight layers" lists H1–H9, §6 and §7
are misnumbered); and it cites PR #2's document by name and section, so #2
merges first. Five content findings follow (lakeswitch gate count, the
`bd init` prefix limit, the denylist gate flagging the document itself, the
home of `docs/architecture/`, eighteen occurrences of "Leerprobe").

### The round-two findings on this pull request, status now

1. **Commit identity.** The clone's `git config user.email` is still the
   literal placeholder `<deine commit-adresse>` (checked at this
   measurement); every commit on `main` and on the three branches carries
   it, as does the `owner` field of all five tracker items. Set it before the
   next commit. Whether to rewrite history is the maintainer's call.
2. **The severance in portfolio PR #162 is half, not whole.** Correcting the
   bullet above: at `ccda349` the pull request removes 12 of the 24 manifest
   entries (`prompts/`, `kit/`, the two governance documents,
   `plans/_README.md`, six test files; `WORKFLOW.md` became a signpost) and
   keeps 12 as portfolio-owned copies (the seven workflow scripts, both
   templates, `ruff.toml`, `provenance.yaml`, `ci.yml`). The kept twelve are
   deliberate duplicates across repositories and want recording as such —
   in ADR-032 there, and in this repository's own manifest.
3. **The measurement commit.** The baseline above was measured at `5efe809`
   and reproduced unchanged at `4ffe21d` (table below).
4. **The Dolt push after the note change ran.** `refs/dolt/data` on origin
   advanced to `0252828` at 22:42:38 +0200, between the export
   (`export-state.json`, 22:42:32) and the git commit (22:42:42). The
   rendered export matches the database: five items.

### Baseline reproduced at `4ffe21d` (venv `~/.venvs/portfolio-agentic-engineering`, 2026-09-16 late evening)

| Command | Result |
|---|---|
| `pytest tests/ -q` | 64 failed, 182 passed, 4 skipped |
| same, `--ignore=tests/test_kit.py` | 60 failed, 167 passed, 4 skipped |
| red per file | 27 `test_ci`, 21 `test_regelwerk`, 11 `test_feedback_channel`, 4 `test_kit`, 1 `test_model_endpoints` |

The eleven red channel tests are portfolio-shaped assumptions, not defects of
this file: they require at least twenty handovers and at least one with
`direction: framework->project`. This file's frontmatter passes
`scripts/handover_schema.py` (all fields allowed, all common fields present,
direction declared). Whether the channel contract applies to this repository
is a decision for the test classification (`coding-harness-2ee`).

### The portfolio side (PR #162 at `ccda349`, base `master` `8a8f3ea`)

Round two (21:01 UTC) found the branch mechanically green — 32 gates, both
CI runs green — and not mergeable on content; the addendum (21:15 UTC) added
seven findings. The blocking ones: the link gate was silenced for living
documents (105 dead references in living tiers with the exception list
emptied); the body of `AGENTS.md` contradicts its own "moved" banner; the
work entry is broken (`/workflow-start` and `make change` point at deleted
prompts, pinned as expected by a test); ADR-032 describes a pull request
other than the one it sits in (says all 24 entries go, 12 stay); three
remaining enforcers lose their tests while their bookkeeping says otherwise;
the tracker export was trimmed by hand (Dolt holds 623 items, the export 621,
manifest not re-rendered — `portfolio-lcb8` and `portfolio-prrw` still open);
the bead `zfyv` carries a note written in the future tense one commit after
the severance it waits for.

What bears on this repository:

- **Nine test functions were deleted there and exist nowhere here** —
  four from `test_human_gates.py`, five from `test_workflow_entry.py`. The
  commit says "move with quality-gates"; this repository has neither file.
  Decide: adopt the nine here, or record the loss in ADR-032. Not a copy
  task — the four human-gate tests read a portfolio artefact
  (`templates/run-log/run-log-schema.yaml`).
- **The move itself is lossless:** all 21 files deleted there and the 12
  kept copies are byte-identical with this repository's `main` at
  `5a950c2`; nothing among them changed between `4ce8240` and `8a8f3ea`.
- **`kit-probe` moves here.** Portfolio dropped the gate; it becomes this
  repository's acceptance gate in the `ci.yml` still to come
  (`coding-harness-bo0`).
- PR #159 (readability) merged 16:09 UTC as `a322600`, PR #160 (69il fix)
  merged 17:50 UTC as `4ce8240` — both before Phase 3 took its copy, so
  step 3.6's precondition from the first section is met.

### Tracker

Five items: two closed (`coding-harness-tmr`, `coding-harness-anw`), three
open and unclaimed (`coding-harness-2ee`, `-9qo`, `-bo0`). None of the three
document pull requests has an item, which PR #2's review names as the third
occurrence of the same gap: the one-writer rule produced no tracker item for
two documents and a tracker write for the third. This session wrote nothing
to the tracker either — it could not tell whether another session was
running — and leaves the rule question to the next one (item 3 below).

### What to do first, next session

1. Set `git config user.email` in this clone before any commit.
2. Merge in order: PR #1 (this file; findings 2 and 3 of round two are
   folded into this section) → PR #2 after its four text corrections →
   PR #3 after the maintainer signs the review block and the document is
   rebased on #2's merged text, with the counts and the T0–T2 decision
   reconciled.
3. Decide the tracker rule for document-only work: an item per pull request,
   or a house-rule clause saying what a session does when it cannot write.
   Then create the items — one writer, then `tools/bd dolt push`.
4. Decide the nine lost tests (adopt here or record the loss) and record the
   twelve kept copies as deliberate duplicates — both feed portfolio #162's
   next round.
5. Then the ready items: classify the 60 red tests (`-2ee`), carve the
   template slice (`-9qo`), bring `ci.yml` with the `kit-probe` gate
   (`-bo0`).
