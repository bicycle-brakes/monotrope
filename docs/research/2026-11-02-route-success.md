---
title: "Route success — which runner route gets implement and repair accepted, and at what cost"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-hleu
tags: [spike, stage-2, routing, measurement]
---

# Route success — implement and repair, by route

Spike of bead coding-harness-hleu ("choose the work route by measured success,
measure first"; maintainer 2026-10-28, "Mach das"). The question: does the
data support a routing change, for example Sonnet first on changes to
`scripts/stage2.py`, where on 2026-10-28 GLM attempts of 1.6–2.2 h were
rejected while Sonnet took about 13 minutes?

## Data and method

- **Source:** the time lines the runner writes into `plans/changes/*/plan.md`
  (format `<date> <start>–<end> UTC, <seconds> s — <verb> · attempt <n> ·
  route <r> · model <m> · accepted|rejected · measured by the runner`), read
  from `main` at `c9692afd` on 2026-11-02, archived changes included. 214
  implement and repair lines from 33 changes, 2026-10-22 to 2026-11-01. Lines
  before 2026-10-22 carry no runner measurement and are not counted.
- **Chains:** consecutive attempts of one verb call (attempt 1, 2, 3) in one
  change; a chain is accepted when any of its attempts is.
- **Large file:** a change counts as touching `scripts/stage2.py` when its
  `plan.md` names that path — an approximation, not the merged diff.
- **Rejection causes:** the 257 failure blocks ("Attempt N (route) failed its
  post-run checks") in the changes' `findings.md`, classified by keyword,
  first match wins. A coarse classifier; "make verify or a gate red" is the
  catch-all.
- Only changes merged into `main` are counted; the lane branches of
  2026-11-02 are not.

## Results

### Per attempt

| Verb, route | Attempts | Accepted | Rate | Median minutes | Total hours |
| --- | --- | --- | --- | --- | --- |
| repair, codex | 96 | 58 | 60 % | 14.9 | 28.6 |
| repair, codex-repair | 37 | 20 | 54 % | 16.4 | 12.8 |
| repair, stage-1 (Sonnet 5.5) | 24 | 4 | 17 % | 14.3 | 8.5 |
| implement, flash (GLM 5.3 Flash) | 22 | 5 | 23 % | 45.2 | 18.0 |
| implement, flash-repair | 17 | 5 | 29 % | 26.0 | 9.1 |
| implement, stage-1 (Sonnet 5.5) | 18 | 8 | 44 % | 12.4 | 3.1 |

### Per chain

| Verb, first route | Chains | Accepted at attempt 1 | Accepted later | Never | Median minutes to acceptance | Hours in rejected attempts |
| --- | --- | --- | --- | --- | --- | --- |
| repair, codex | 96 | 58 | 22 | 16 | 16.5 | 26.9 |
| implement, flash | 22 | 5 | 11 | 6 | 63.8 | 23.2 |
| implement, stage-1 | 7 | 2 | 0 | 5 | 13.5 | 0.8 |
| repair, stage-1 | 7 | 2 | 0 | 5 | 14.4 | 0.9 |

Which route got a chain accepted: of 96 repair chains, 58 by Codex at once,
20 by the Codex repair attempt, 2 by Sonnet, 16 never. Of 22 implement chains
that started on Flash, 5 by Flash at once, 5 by the Flash repair attempt, 6 by
Sonnet as the third attempt, 6 never.

### Large file or not

| Verb, route | `stage2.py` changes: rate (n) | other changes: rate (n) |
| --- | --- | --- |
| implement, flash | 27 % (15) | 14 % (7) |
| implement, stage-1 | 36 % (14) | 75 % (4) |
| repair, codex | 63 % (81) | 47 % (15) |

### Why attempts were rejected

| Cause (first keyword match) | Blocks |
| --- | --- |
| `make verify` or a gate red | 175 |
| the answer missed the fixed-line form | 26 |
| the new test was green on the baseline (not red first) | 25 |
| a protected or out-of-scope path was touched | 24 |
| refs moved by another lane while the proof ran | 7 |

## Reading

1. **Repair works mostly as designed.** Codex gets 83 % of repair chains
   accepted (80 of 96), most at the first attempt, in a median 16.5 minutes.
2. **Implement on Flash is the expensive path.** A chain that starts on Flash
   takes a median 64 minutes to acceptance, 6 of 22 never get there, and 23
   hours went into rejected attempts of those chains in ten days. Each Flash
   attempt runs a median 45 minutes against Sonnet's 12.
3. **The data does not show that "Sonnet first on `stage2.py`" would be
   better.** Flash did not do worse on `stage2.py` changes (27 %) than on others
   (14 %), and the seven chains that started on Sonnet were accepted twice. The
   samples are small, and Sonnet mostly ran as the third attempt on cases two
   others had already failed — a selection effect that makes its rate look
   worse and its speed look better than a first attempt would.
4. **About a third of named rejections are not about the model's code:** 26
   answers missed the fixed-line form, 24 touched paths the attempt may not
   touch, 25 tests were already green before the repair (a weak test, or a
   fix already in the baseline — on the unmerged lane branches of
   2026-11-01/02 that happened through committed stopped attempts, bead
   coding-harness-c99h), and 7 proofs were voided by another lane (bead
   coding-harness-wkxm). These fail any route alike.
5. **About 50 runner hours in ten days went into rejected attempts**
   (repair 26.9 h, implement 23.2 h, counting the chains above).

## Recommendation

- **No routing change now.** The hypothesis of 2026-10-28 is not confirmed;
  proposing a decision pull request on this data would ask the maintainer to
  decide on noise.
- **Remove the route-independent rejections first,** then measure again:
  the runner writes the fixed-line skeleton per taken row (bead
  coding-harness-k93f), a scope guard for repairs (bead coding-harness-t83),
  proofs in a private clone (bead coding-harness-wkxm), stopped attempts on
  side refs (bead coding-harness-c99h).
- **Record the cause in the time line itself,** so the next measurement needs
  no keyword classifier: one cause field per rejected attempt (beads
  coding-harness-zaqf, runner event log and report, and coding-harness-v6vk,
  time records as data).
- **One option for the maintainer to weigh later:** after one rejected Flash
  implement attempt, go to Sonnet directly instead of the Flash repair
  attempt. In this data Flash repair and Sonnet each finished 5 or 6 of the
  22 Flash chains, so the option saves time only if Sonnet keeps its
  12-minute median as a second attempt; bead coding-harness-6ie (Sonnet
  continues Flash's edits) changes that picture and should land first.

## Reproduce

The script that produced the tables reads only `git show` output of the
named commit; it is kept in the session's scratchpad (`hleu.py`), not in the
repository. Its rules are the ones under "Data and method".
