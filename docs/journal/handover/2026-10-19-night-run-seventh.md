---
title: "Session handover — seventh night run, as of 2026-10-19"
category: handover
created: 2026-10-19
updated: 2026-10-19
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-10-19"
tags: [handover, session, night-run, research-swarm, ci]
target_ref: origin/main
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The night of 2026-10-18 to 2026-10-19 followed the night-run plan
([PR #165](https://github.com/MPAdesso/coding-harness/pull/165), bead
coding-harness-yuw). Every queue item ran. The morning page is late: the
Claude session limit stopped the orchestrator from about 00:25 UTC until
07:38 UTC, so this file lands after the 08:00 Europe/Berlin target.

- **Research swarm** (bead coding-harness-icw, branch
  `explore/research-swarm`, draft decision
  [PR #158](https://github.com/MPAdesso/coding-harness/pull/158)). Plan
  steps 1–5 and 7–12 are implemented and tested offline, at `c3c07ff`.
  The last full `make verify` was green at `6750869`: 2926 passed,
  16 skipped.
- **GLM narrowing**
  ([PR #166](https://github.com/MPAdesso/coding-harness/pull/166)) is open
  and not merged. GLM through OpenCode Go is no longer excluded; the outage
  until 2026-10-21 covers only the Z.ai route.
- **Merged on the maintainer's request on 2026-10-18:** #157 and #159–#164,
  by a Haiku sub-agent with merge commits, after green checks.
- **CI time** is measured and recorded in bead coding-harness-7so (make CI
  faster). The pytest step is about 80 % of the hosted gates job.

## Next step

Read [PR #166](https://github.com/MPAdesso/coding-harness/pull/166) and
decide on it, together with the proposed replacement text for ADR 0021
line 223. Once it is merged, merge `origin/main` into
`explore/research-swarm`; that branch still carries the old GLM exclusion.

## Research swarm — what the night did

All spans below were measured with `date -u` and count against the 17 h
20 min appetite (decision Q-14).

| Step | Content | Commit | Span |
|---|---|---|---|
| main sync | #157 merged in; `stage2_availability.py` reconciled | `1f86c04` | about 31 min |
| 12 | Resumable state store (Q-13): sealed per-slot records outside the repository, exact-binding reuse, lock | `bf81465` | about 35 min |
| 2 (part) | Per-invocation role, data-class and free-seat checks | `ecd8e04` | about 21 min |
| 3 | New run replaces the old one; store wired; Zen transport removed | `c1a8431` | 1 h 32 min |
| 8, 9 | Obligation inventory; `research-handoff` gate | `9078c3c` | about 32 min |
| 10 | Doctrine, prompts and spec template | `c3c07ff` | about 26 min |

Measured in total: about 9 h 52 min of 17 h 20 min, so about 7 h 28 min
remain. This is the orchestrator's sum of the plan's Time used sections.

### For the maintainer's review

- The step-3 run module was drafted before its tests. Its only red evidence
  is a collection error. Every later step recorded assertion failures first.
- The judge model's JSON answer schema is an agent [DETAIL]
  (`plans/changes/research-swarm/plan.md`, "New run verified"). The
  maintainer has not seen it.
- The maintainer stated on 2026-10-18 that dynamic seat selection and resume
  are essential. Both stay; no slimmer variant is proposed.

### Still open

1. Step 6, the real-Pi isolation capture (finding F-1). It needs the
   maintainer present.
2. 19 ledger rows are "not yet written". They belong to catalog and
   preparation tests, mainly `tests/test_stage2_research_catalog.py`.
3. The phase-6 review, through a fresh read-only Codex session
   (`stage2.py review`), after step 6.
4. The new `research-handoff` gate has not had a hosted CI run yet.

## CI time (bead coding-harness-7so)

- Hosted runs on main from 2026-10-18 (after the #162–#164 merges): the gates
  job took 6 min 18 s to 8 min 33 s. The single-process pytest step took
  294–412 s, and the kit probe 41–53 s.
- Locally, the research-swarm branch takes `make verify` from 10 min 42 s
  (2284 tests) to 16 min 07 s (2926 tests).
- Proposed next steps: add `--durations=25` to the CI pytest call, then
  pytest-xdist (bead coding-harness-d5a).

## Decisions and preferences from this session

- Codex may be used again, including for implementation (maintainer,
  2026-10-18).
- GLM through Z.ai is off until 2026-10-21 20:34 Asia/Singapore. GLM through
  OpenCode Go works.
- Dynamic seat selection and resume are essential for the research swarm
  (maintainer, 2026-10-18).

## Pull requests awaiting the maintainer

- [#166](https://github.com/MPAdesso/coding-harness/pull/166): GLM through
  OpenCode Go is not excluded. It proposes text for ADR 0021 line 223.
- [#165](https://github.com/MPAdesso/coding-harness/pull/165): the night-run
  plan (bead coding-harness-yuw).
- [#158](https://github.com/MPAdesso/coding-harness/pull/158): the research
  swarm decision PR. It stays a draft until step 6 and phase 6 are done.

## Parallel sessions and ownership

One orchestrating Claude Code session, the sole tracker writer. Sub-agents
worked only in `.claude/worktrees/research-swarm`. Nothing runs now. Beads
were written and pushed: checkpoint comments on coding-harness-icw and the
measurement on coding-harness-7so. No bead was opened or closed.
