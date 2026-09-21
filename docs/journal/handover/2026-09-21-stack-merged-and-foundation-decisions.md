---
title: "Session handover — gate stack merged, foundation decisions recorded, 2026-09-21"
category: handover
created: 2026-09-21
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-21"
tags: [handover, gates, 2ee, bo0, foundation, lakeswitch]
target_ref: "6381712"
bead: coding-harness-bl2
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The gate machinery and the whole red-test triage are on `main`: pull requests
#15, #14 and #13 were merged top-down into #11, and #11 was merged into `main`
as `6381712` on 2026-09-21. CI on `main` is green at that commit — the first
green run this repository has had. Three pull requests stay open and are not
merge-ready: the three amendment ADRs (#12), the Omnigent-first target (#8,
draft) and the Claude Code session display (#10). In the sibling repository
`lakeswitch-ai`, the maintainer settled four decisions that make this
repository the owner of a Pydantic/Jinja2 and human-gate foundation
(lakeswitch-ai pull request #37, decisions D-45 to D-48). The follow-up work
from the review and from those decisions is filed as eleven beads.

## Next step

Claim the bead "CI runs every gate even after a red block gate"
(`coding-harness-bl2`) and make the generated workflow run every gate step
after a failure; it is small, it unblocks honest CI evidence for everything
that follows, and two latent gate bugs were hidden by exactly this behaviour.

## Needed from the maintainer

- **Accept or amend the three ADRs in pull request #12 yourself.** `docs/adr/`
  admits only `human-decided`; the ADRs carry no provenance declaration and
  ADR 0003 still says the scan's rejections are "unchanged from D-17" although
  D-17 also denies vendor names. Recommendation: fix that sentence, accept,
  then merge #12 into `docs/omnigent-first-target` **before** #8 reaches
  `main` — otherwise the `decision-continuity` block gate turns `main` red.
- The `AGENTS.md` block in pull request #8 came from a Codex session while the
  file's class is `human-written`; it needs your explicit acceptance.

## Decisions and preferences

Settled by the maintainer on 2026-09-21 and recorded in lakeswitch-ai pull
request #37 (`plans/changes/unified-research-and-work-management/decision-interview.md`);
they are not asked again:

- **One source, pinned copy.** Coding Harness is the single source of a
  process-generic declared-document foundation; instances adopt it as a
  digest-pinned kit copy, never from a package registry; lakeswitch-ai extends
  it for data engineering and may add but not remove (lakeswitch D-45).
- **First slice.** The gate manifest is the first validated document and the
  verify report the first render — not the export manifest (lakeswitch D-45).
- **Path and packaging.** `harness.foundation` inside one top-level `harness/`
  package, same path everywhere, one prefix for every control; lakeswitch-ai
  ships the copy in its wheel (lakeswitch D-46).
- **One exact pin.** Pydantic 2.13.5, Jinja2 3.1.6, Python 3.11 and 3.12; no
  range (lakeswitch D-47).
- **Roster.** `decisions/roster.yaml` at the same path everywhere; schema and
  reader travel, content is instance-owned; the inherited data-engineering
  roles leave this repository (lakeswitch D-48).

The decision identifiers of lakeswitch-ai collide with this repository's own
D-1 to D-17 and O-1 to O-4; "D-17" means two different things. A prefix is
chosen before promotion (`coding-harness-mr2`).

Merging was done top-down on purpose: each lower pull request only became
green once it contained the upper ones, so `main` never carried a red state.

## Open work and blockers

Task status lives in Beads; this list only points.

- Review follow-ups for the gate machinery: CI stops at the first red gate
  (`coding-harness-bl2`), floor gates that measure nothing in CI
  (`coding-harness-4t8`), reader and workflow hardening (`coding-harness-tqa`).
- Foundation chain, in dependency order: project file and hash lock
  (`coding-harness-ei0`), foundation first slice (`coding-harness-s6i`), roster
  (`coding-harness-1wl`), human-gate catalogue (`coding-harness-car`), release
  builder and lock (`coding-harness-dj9`).
- Promotion of the lakeswitch interview into harness specifications
  (`coding-harness-mr2`).
- Agent definitions carry domain content and cite an `AGENTS.md` section that
  does not exist (`coding-harness-rqc`).
- Session display, pull request #10: the parallel-session scan drops sessions
  with an empty name or status (`coding-harness-hit`).
- Closed on 2026-09-21 with the merge of pull request #11: the gate file bead
  (`coding-harness-bo0`); its five acceptance criteria hold on `main`. This
  unblocked public readiness (`coding-harness-lir`).
- Still in progress: the three ADRs (`coding-harness-nkr`), with a dated note
  from this session.
- Checked and left open: the `CLAUDE.md` import bead (`coding-harness-21f`) —
  `CLAUDE.md` on `main` points to `AGENTS.md` in prose and still carries bare
  `bd` commands. In portfolio-agentic-engineering the severance bead
  (`portfolio-agentic-engineering-vmz9`) stays open: its pull request #162
  merged, but deliberately without deletions, and four mechanism files are
  still on `master`. That tracker was read from its export only, because its
  migration to bd 1.3.0 is a draft (pull request #163). lakeswitch-ai has no
  tracker.

## Working state and parallel-session boundary

- Branch `docs/handover-2026-09-21-stack-merged`, cut from `main` at
  `6381712`. Uncommitted at the time of writing: this file and the re-rendered
  `.beads/issues.jsonl`.
- A Cline session implemented the first round of review fixes on the four
  stack branches and had finished before this session wrote anything here. A
  Codex session on lakeswitch-ai pull request #37 was paused; this session
  took over that branch with three additional commits (`db8f03b`, `2e7203e`,
  `5315624`). If the Codex session resumes, it must pull first — a force-push
  of its old commit would drop D-45 to D-48.
- No parallel session in this checkout at the end (session scan, 2026-09-21).
- Worktree `/Users/mikypiky/coding-harness-wt-claude-code` on
  `feat/claude-code-session-display` belongs to pull request #10 and was not
  touched. The merged stack branches still exist on the remote.
- A mistake of this session, repaired: `bd update --notes` replaces notes. The
  notes of `coding-harness-nkr` and `coding-harness-bo0` were overwritten and
  restored from the committed export at `6381712`, with the new note appended.
  Use `--append-notes`.

## Validation

All on 2026-09-21.

- Combined stack, local, before merging: `scripts/verify_all.sh` reported
  VERIFY GREEN at `8907b42` — 267 passed, 15 skipped; `docs-links` and
  `markdownlint` red at report level as declared.
- CI: green on pull request #15 at `8907b42`, on #14 at `8f4705b`, on #13 at
  `da3dcd5`, on #11 at `6f51901`, and on `main` at `6381712`.
- Fixes this session added to the stack: lint and format of the skip sentinel
  (`07f1bb0`), the kit probe declares the RB-P5 case (`094cd09`), format of
  `tests/test_entry_points.py` (`749bc6d`), the lychee report is ignored so the
  strict kit probe holds in CI (`4a45b2c`), `export-identity` skips visibly
  where the wrapper finds no tracker binary, with `tools/bd` exiting 127 for
  exactly that case (`8907b42`).
- lakeswitch-ai: `lakeswitch verify` after each of the three commits showed
  only the two known provenance-coverage findings on the change package.
- Not run: anything on Linux besides CI; the session-display scripts of pull
  request #10 beyond the review; pull requests #8 and #12 have had no CI run
  since `main` gained a workflow.
- Not read in full: the research documents of pull request #8, most of
  `tests/test_ci.py`, `plans/changes/2ee-triage/research.md`.
