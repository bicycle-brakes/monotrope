---
title: "Night-run plan — 2026-10-21/22"
category: research
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-21"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-yuw
tags: [night-run, plan, stage-2, research-swarm, phase-6]
---

# Night-run plan — 2026-10-21/22

**Proposed operational plan, not an execution report.** The maintainer asked
on 2026-10-21 (about 18:00 Europe/Berlin) for a plan for tonight's session.
It follows the [night-run concept](2026-10-12-night-run.md) and the form of
the [previous plan](2026-10-20-night-run-plan.md): one orchestrating Claude
Code session, a queue set in advance, every result a pull request, no merge.
It grants no new model, architecture, merge or deployment permission. Task
state stays in Beads.

## Three priorities

1. Bring the research swarm (bead coding-harness-icw,
   [PR #158](https://github.com/bicycle-brakes/monotrope/pull/158)) to a
   phase-6 round without BLOCKER or MAJOR, so the maintainer can decide its
   merge in the morning.
2. One heavy job at a time: the machine has 8 GB RAM and 8.0 of 9.2 GB swap
   in use (measured 2026-10-21, about 18:00).
3. Pushed checkpoints, an accurate PR body and one morning page by 08:00
   Europe/Berlin.

## Starting state (2026-10-21, about 18:00 Europe/Berlin)

- #158 at `febe2aa` pushed up to `825ae65`: CI green at `825ae65`
  (run 39618859539). Since round 13 it carries Q-18 (the maintainer chooses
  the seat models on intelligence against cost) and the exclusion fix from
  PR #208.
- Phase-6 round 14 (2026-10-21): Codex F-58 to F-60 (MAJOR), independent
  deepseek-v4.1-flash through Pi D-3 to D-7 (one MAJOR). All eight rows were
  taken. The runner's repair failed twice with Codex (attempt 1: an older
  test went red; attempt 2: red-first proof refused on form) and is running
  attempt 3 on Sonnet 5.5; its result is not read at the time of writing.
- Open point in the repair: the orchestrator's taken status for D-6 said an
  exclusion "binds whatever its declared class". That contradicts the earlier
  reviewed rule O197-2 (a customer-only exclusion does not deny framework
  admission), and attempt 2 rewrote that test. The orchestrator proposed to
  restore it and keep D-6 to: an unknown class is malformed (exit 2), an
  exclusion of the public class binds the online seats. **The maintainer
  answered on 2026-10-21 (about 18:30): exclusions stay class-scoped as
  before** ("sperrung für kundenkonto wie vorgesehen"); the work is bead
  coding-harness-dxso.
- Budget: Claude and Codex not read. GLM through Z.ai is available again
  since 2026-10-21 14:34 Europe/Berlin; GLM through OpenCode Go works.
- The Artificial Analysis key (`ARTIFICIAL_ANALYSIS_API_KEY`) is not yet
  provided; the live intelligence reading stays unverified.

## Queue

| # | Item | Worker | Done when, or stop |
|---|---|---|---|
| 1 | Read the round-14 repair result (attempt 3, Sonnet 5.5). Then bead coding-harness-dxso: restore the O197-2 test (a customer-only exclusion does not deny framework admission); an exclusion naming no declared data class is malformed (exit 2); an exclusion of the public class binds the online seats and free researchers; correct D-6's Status | Orchestrator; one Sonnet sub-agent for the repair, red test first | Every round-14 row `fixed — tests/…` or left open with its reason; coding-harness-dxso closed; full `make verify` green; committed and pushed |
| 2 | Phase-6 round 15: `stage2.py review research-swarm` | Fresh read-only Codex session | Findings committed unchanged in `findings.md` |
| 3 | Triage round 15 and repair taken rows through `stage2.py repair research-swarm` | Orchestrator triages; Codex repairs, Sonnet after two failed checks (ADR 0017) | Rows fixed, `make verify` green, pushed. A row that needs a maintainer decision stays open with a prepared question |
| 4 | Round 16 only if round 15 took a BLOCKER or MAJOR | Fresh read-only Codex session | Rounds stop at round 16; the rest goes to the morning page |
| 5 | Refresh #158: merge origin/main if it moved, PR body (rounds 14–16, commits, known limits), wait for green CI | Orchestrator | Body current, CI green, decision block drafted for the morning page; no merge |
| 6 | Reserve: name the slow tests for the CI work (bead coding-harness-7so): one local `pytest --durations=30` run, read-only | Orchestrator | A dated measurement as a comment on the bead; no code change |
| 7 | Morning handover | Orchestrator | A dated file under `docs/journal/handover/` as a pull request by 08:00 Europe/Berlin |

Items run strictly one after another. **No two `make verify` runs at the same
time** and at most one foreign call or sub-agent at a time.

## Not tonight

- No merge of any pull request, including #158.
- No independent Pi reviewer: `stage2.py session` needs the maintainer to
  start the command in the VS Code terminal (bead coding-harness-rm8), so
  DeepSeek does not run unattended. Codex alone reviews rounds 15 and 16.
- No live research-swarm run and no Artificial Analysis call; offline tests
  and local doubles only.
- No work on the beads recorded today: Pi as a phase-6 reviewer
  (coding-harness-duue), Pi as a repair fallback (coding-harness-vcci),
  providers other than OpenCode Go (coding-harness-fqf9), the CI/verify split
  and dev/test/prod (coding-harness-7so beyond item 6), the agent dashboard
  candidates (coding-harness-326), TokenEconomizer (coding-harness-52pd), the
  class in every bead (coding-harness-680l). Each needs an interview first.

## Stop rules

- At 10 % of a five-hour window left, start no new large step; at about 5 %
  checkpoint and wait for the reset.
- Two failed repairs, a missing maintainer decision or an unresolved ambiguity
  stop that item; record the reason and go on with the next independent item.
  No question is asked overnight and no answer is invented.
- A leak-check BLOCK ends foreign calls without fallback.
- Tracker first, git second. The orchestrator is the only tracker writer; it
  writes a checkpoint comment on coding-harness-icw after each green step and
  only while no `make verify` runs.
- No force push, amend, bare stash, customer instance or secret read; the
  Artificial Analysis key is never read or printed.

## Morning page (08:00 Europe/Berlin)

One page: the phase-6 verdict for #158 and its decision block, the D-6
repair (bead coding-harness-dxso), pull requests awaiting the maintainer, where work
stopped and why, the CI slow-test measurement, and the time the morning
review took.


## Addendum — 2026-10-21, maintainer-approved follow-on queue

The maintainer asked Codex to append the recommended beads and continue while
budget remains. Finish the research-swarm queue first; its review limit stays
round 16. One change per worktree, one heavy job or foreign call at a time,
each green checkpoint committed and pushed. No merge and no new model or
architecture permission. Publish the handover before an observable budget
stop. Remaining budget that cannot be measured is recorded as not read.

Order recommended from the tracker and main `86bc7ea`, read on 2026-10-21:

| Order | Work and bead | Why next / completion boundary |
|---|---|---|
| 8 | Reconcile the merged repair stack with Beads: own tooling (`coding-harness-011`), commit guard (`coding-harness-wqw`), record location (`coding-harness-5j4`), diff bounds (`coding-harness-4p1`), locking (`coding-harness-1wo`), record robustness (`coding-harness-3ql`), parser/evidence (`coding-harness-0an`), exclusions (`coding-harness-16z`), failed-stage retirement (`coding-harness-tex`) | Still listed open or in progress; check acceptance against the merged PR before closing or writing duplicate code. Research seats (`coding-harness-4295`) close only after #158 merges. |
| 9 | Restore must not follow a parent symlink outside the worktree (`coding-harness-10w`) | Protect outside files; a disposable reproduction must prove they remain intact. |
| 10 | Reviewer prose must not become trusted loop state (`coding-harness-i70`) | A forged state line cannot bypass discovery or choose a model. |
| 11 | Refuse index-only changes (`coding-harness-0c8`) | Preserve staged work; a dirty index refuses before the call or commit. |
| 12 | Reject invalid phase-6 verdicts (`coding-harness-5mx`), then malformed loop rows next to valid ones (`coding-harness-vque`, separate change) | No false completed review; invalid output keeps the loop record and exits nonzero. |
| 13 | Lock phase-6 release of the loop record (`coding-harness-751`) | A held record lock refuses release without changing the record. |
| 14 | Runner measures time; timing tests assert order (`coding-harness-9wp`, related `coding-harness-jik`) | Inspect the existing worktree first. Remove accounting-only repair failures; no test retries to green. |
| 15 | Fast pre-check and useful failure evidence (`coding-harness-csm`) | Inspect the existing worktree. A red named test skips full verify and reports scrubbed assertions; green pre-check still requires full verify. |
| 16 | Reliable interactive launch (`coding-harness-rm8`, overlapping report `coding-harness-bas`) | Compare reports before duplicate fixes. Use a short private launcher and distinguish dispatch acceptance from actual startup. Real launch qualification stays attended unless separately authorized. |
| 17 | Enforce paid reviewers' read boundary (`coding-harness-21dl`) | Prepare research and the required design/interview; an unresolved architecture decision goes to the morning page. |
| 18 | Measure CI cost (`coding-harness-7so`) | One dated durations measurement, as item 6 permits. CI/verify separation and dev/test/prod need an interview before implementation. |

Before each implementation, reproduce on current main, read existing artifacts
and run the workflow required by its class. An already merged fix is checked
and reconciled, not rebuilt. Open decisions stop that item, not independent
work later in the queue. Task status remains in Beads.

### Interview queue after the bounded repairs

1. Alternative phase-6 reviewer through Pi (`coding-harness-duue`), then the
   repair fallback (`coding-harness-vcci`): settle model choice and routing;
   consolidate overlapping implementer work (`coding-harness-4ji`).
2. Every change has a bead and an explicit workflow class
   (`coding-harness-680l`): decide storage and agreement with change artifacts.
3. Writing-attempt isolation (`coding-harness-s9r`) and preserving failed
   work (`coding-harness-znc`): settle threat model and evidence retention.

Provider expansion, TokenEconomizer, dashboards and kit export remain behind
this reliability work. The dashboard waiting period remains in force.

## Addendum — 2026-10-21, evening: reordered queue and beads added without interview

The maintainer approved this order in the conversation of 2026-10-21. It
replaces the order of items 9–18 above; their completion boundaries stay as
written. The research swarm (#158: repair F-61 and F-62 from the saved
candidate, prove red first, full `make verify`, round 16) still comes first.

Why the new order: almost every item changes `scripts/stage2.py`, the tool
that runs the repairs. The beads that keep a failed attempt cheap and
retryable go first, so later items lose fewer attempts.

| Order | Work and bead | Completion boundary, and where it may stall |
|---|---|---|
| 9 | Diagnostics must not carry test secrets into `findings.md` (`coding-harness-8hr`) | A failed attempt whose traceback holds a fixture key can be retried without a leak-check BLOCK. |
| 10 | Runner measures time; timing tests assert order (`coding-harness-9wp`, with the load-sensitive test `coding-harness-jik`) | Built by hand, not through `stage2.py`: the fix lives mostly in tests, and the repair runner's red-first check has failed on test-only fixes before (`coding-harness-0ho`, which needs an interview). |
| 11 | Fast pre-check and full failure messages (`coding-harness-csm`) | As item 15 above. |
| 12 | Stage new files before `make verify` (`coding-harness-fdz`) | The kit probe sees an attempt's new files. Must agree with item 15 (index-only changes) — same code path; build them one after the other. |
| 13 | Restore must not follow a parent symlink (`coding-harness-10w`) | As item 9 above. |
| 14 | Reviewer prose must not become loop state (`coding-harness-i70`) | As item 10 above. |
| 15 | Refuse index-only changes (`coding-harness-0c8`) | As item 11 above. |
| 16 | One change for the loop-row parser: invalid phase-6 verdicts (`coding-harness-5mx`), malformed rows next to valid ones (`coding-harness-vque`), row ids that are not `L<n>-<m>` (`coding-harness-6jg`) | One branch, one pull request, because all three touch the same parser; separate tests per bead. |
| 17 | Lock phase-6 release of the loop record (`coding-harness-751`) | As item 13 above. |
| 18 | Reliable interactive launch (`coding-harness-rm8`, `coding-harness-bas`) | As item 16 above; real launch stays attended. |
| 19 | Paid reviewers' read boundary (`coding-harness-21dl`) | Research and interview preparation only, as item 17 above. |
| 20 | CI durations measurement (`coding-harness-7so`) | As item 18 above. |
| Filler | Reconcile `WORKFLOW.md` with the tree (`coding-harness-i0l`) | Read-only; taken whenever an item above is blocked. Output: a dated report and one bead per missing piece. |

Moved to the interview queue: the Sonnet fallback that loses Flash's edits
(`coding-harness-6ie`) overlaps with writing-attempt isolation
(`coding-harness-s9r`) and preserved failed work (`coding-harness-znc`), so it
joins item 3 of the interview queue.

Known stall points for the whole night:

- The runner repairs itself; the round-15 repair call exited 1 with an
  unexplained cause. If it recurs, the item is built by hand or stops.
- No merge overnight: changes to the same file become stacked pull requests,
  and the morning merge needs rebases from the bottom.
- One full `make verify` takes about ten minutes (measured 2026-10-16) plus a
  review loop per change; items 9–20 are more than one night. Unfinished
  items go to the morning page.
- Budget remaining is not read; the stop rules above apply.
