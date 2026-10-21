---
title: "Session handover — research model exclusions, for Claude, as of 2026-10-21"
category: handover
created: 2026-10-21
updated: 2026-10-21
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: Codex
  version: "2026-10-21"
tags: [handover, session, research-swarm, security, model-admission]
target_ref: a05360c1ca6a72ebc50ba8058e332f09323b163d
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The maintainer requested progressively deeper technical analysis of a P1 review
finding, then a handover to Claude. The research swarm can select and invoke a
model that the global `ausgeschlossen[].modelle` declaration forbids for framework
content. This session read the affected implementation and reproduced contradictory
admission decisions with isolated functions; it did not repair code or launch any
foreign model. The affected research-swarm decision pull request is still open at
the reviewed commit ([PR #158](https://github.com/bicycle-brakes/monotrope/pull/158),
`a05360c1ca6a72ebc50ba8058e332f09323b163d`, read on 2026-10-21).
The fetched main branch is `165db6aae1cd1a9b56c0fe92685f8f127cd3754a` and does
not yet contain this research implementation.

## Next step

Reproduce the global-exclusion bypass against the current head of PR #158 in an
isolated worktree, using an otherwise admitted repository-seat model; confirm the
head before relying on the line references below.

## Needed from the maintainer

Nothing right now. The current request authorizes this handover; implementation
was discussed as a proposed next action, not performed or explicitly requested
in this session.

## Decisions and preferences

- Speak German with the maintainer; keep repository artifacts English. Explain
  the concrete behavior, distinguish measured evidence from inference, and keep
  user-facing updates short.
- The maintainer asked for technical depth, including the complete call path,
  data exposure, failure behavior and what a complete repair must cover.
- Do not merge the handover or the research-swarm decision PR on your own.
- A framework exclusion must block private research roles. The proposed repair
  must preserve data-class distinctions; a framework exclusion alone does not
  establish a public-web prohibition. This is an implementation recommendation
  from analysis, not a new maintainer policy decision.
- Existing foreign-model routing and leak-check rules remain binding. No live
  model probe is needed to reproduce the admission defect.

## Open work and blockers

Task status remains in Beads. The existing research-swarm work item is “Phase 1
as a bounded research swarm: three researchers, one critique round, one judge”
(`coding-harness-icw`), read as in progress on 2026-10-21. No finding-specific
issue was created, claimed or closed by this session, and no tracker writes or
tracker synchronization were performed because another writing session was
reported active. Coordinate ownership with the tracker writer before changing
task status or repairing the research-swarm branch.

### Root cause and exact call path

All locations in this section refer to `a05360c`, not main's current files.
Read them with `git show a05360c:<path>` if the checkout is on main.

1. The existing global predicate reads `ausgeschlossen` and rejects matching
   framework model IDs/prefixes, including case-insensitive comparisons against
   full IDs and their last slash-separated segment. Missing `klasse` defaults to
   `framework`; malformed exclusion structures produce a refusal reason. The
   established paid and free review admission paths call it
   (`scripts/stage2.py`, `excluded_problem`, `declaration_problem`,
   `free_admission_problem`).
2. Research selection checks terms, cost, catalog eligibility and timed
   exclusions, but never the global predicate. An otherwise eligible denied
   model gets `admitted=True`. Both preferred seats and the substitute pool can
   use it (`scripts/stage2_availability.py:482`, `_go_outcome`; `:475`,
   `_admitted_pool`; `:513`, `usable`; `:537`, `fill`).
3. The probe's default admission checks endpoint existence, membership in
   `modelle` or `modelle_terms`, and residency, but no global exclusion. The
   fixed-text leak check therefore does not correct the missing authorization
   check (`scripts/stage2_availability.py:176`, `research_declaration_problem`;
   `:196`, `_checked_probe`; `:237`, `probe_go`; `:302`, `probe_claude`).
4. Selected repository seats become both `finder_agents` and `repository_agents`
   (`scripts/stage2_availability.py`, `research_roles`).
5. Initial role-set validation and the check before each individual invocation
   both call `invocation_problem`, which does not read `ausgeschlossen`
   (`scripts/stage2_swarm.py:314`, `invocation_problem`; `:376`, `role_launches`;
   `scripts/stage2_research_run.py:274`, `open`; `:416`, `gate`).
6. The dispatcher does refuse blocked gates before launching and records them
   as `refused`. The start barrier is present; its admission predicate is
   incomplete (`scripts/stage2_research_dispatch.py:206`, `launch_next`).

### Earliest private payload and scope

The first sensitive request can be the finder, before any repository tool is
used. `build_brief` includes research.md without earlier runner blocks, the
change and bead identity, and decisions.md/spec.md when present. `private_brief`
adds AGENTS.md, and `finder_prompt` appends that content directly to the model
request (`scripts/stage2_research_run.py:345`, `:361`, `:364`).

Later repository prompts add the finder map and, for the applicable topics,
neighbour/history packets (`scripts/stage2_research_run.py:384`). The Go
repository launcher runs in the repository root with read tools and its path
lock extension (`:620`). Restricting reads to the worktree does not authorize a
globally forbidden recipient to receive worktree content.

At this commit, each repository seat has one planned finder slot and eight
repository-topic slots (`:753`, `stage_finders`; `:828`, `topic_entries`). This
describes the plan, not observed launches: stored-result reuse or an early stop
can reduce actual calls. No actual disclosure was measured in this session.

### Isolated evidence obtained on 2026-10-21

The reproduction loaded original function/class definitions from the reviewed
commit using Python's abstract syntax tree, then supplied temporary YAML and
stand-ins for terms/cost/catalog evidence. It made no network or model calls.

For an otherwise admitted `deepseek-v4.1-flash` with a framework exclusion:

```text
excluded_problem: refusal reason naming the exclusion
research_declaration_problem: None
invocation_problem(role=repository): None
_go_outcome: state=not-probed, admitted=True, tool_support=None
usable: True
_admitted_pool: contains deepseek-v4.1-flash
```

An additional isolated matrix confirmed that the existing global predicate
refuses each of the following while the research invocation predicate accepts:

| Case | Role | Endpoint |
|---|---|---|
| Exact DeepSeek framework exclusion | repository | opencode-go |
| Uppercase `DEEPSEEK-` exclusion prefix | finder | opencode-go |
| Malformed `ausgeschlossen` mapping instead of list | repository | opencode-go |
| `claude-opus-` exclusion prefix | judge | claude-code-plan |
| `claude-haiku-` exclusion prefix | repository | claude-code-plan |

These are predicate-level reproductions, not complete CLI or dispatcher runs.
The supplied review reported a broader stand-in reproduction of preparation and
130 passing selected tests on `a05360c`; those tests were not rerun or adopted as
new validation evidence by this session.

### Repair shape proposed, not implemented

Prefer one shared exclusion predicate over the parsed declaration and applicable
data class, with the existing root-reading API delegating to it. That would let
the research code use the same matching and malformed-configuration behavior
without importing the runner into its helper modules.

The shared decision must cover private seat selection, the substitute path,
probe authorization and private role invocation. Include Claude seats and Opus
roles; a Go-only candidate filter leaves invocation paths open. Do not replace
the research declaration with the old paid declaration wholesale: research
deliberately also admits models through `modelle_terms` without adding them to
the review ladder.

Selection currently caches outcomes by `endpoint/model`, and the same model may
serve a private repository seat and a public online seat. A single blanket
`state=excluded` can therefore wrongly conflate data classes. Separate shared
reachability evidence from role/data-class authorization. The exact policy for
fixed-text, source-free probes must be made explicit; it should not silently
reclassify a private seat as public to bypass its exclusion.

The configuration hash in the receipt invalidates a receipt when configuration
changes before consumption. It cannot correct an exclusion ignored at creation.
After consumption, the per-call gate already re-reads configuration and must
enforce newly added exclusions. Its internal dispatcher lock does not lock out
external configuration writers; atomic revocation across file writes and
process launch is a separate concurrency concern, not required to reproduce
this finding and not measured here.

### Regression evidence needed for a repair

The current test named
`test_unadmitted_or_excluded_models_are_never_probed_or_selected` changes only
`availability_preflight.exclude_until`; it does not exercise `ausgeschlossen`
(`tests/test_stage2_research_availability.py:374`).

Use red-first tests for the actual global list: preferred private seat,
substitute, direct probe, direct private invocation, both endpoint families,
prefix/case behavior, malformed exclusion configuration, and a denial added
after selection. Preserve an otherwise authorized public-web call under a
framework-only exclusion. At the invocation boundary, assert `refused` and zero
calls to the affected launch function; checking an error string alone is weaker.
A synthetic private marker in the finder prompt can demonstrate protection of
the earliest sensitive request without sending real repository content.

## Working state and parallel-session boundary

- Main checkout: `/Users/mikypiky/coding-harness`, branch `main`,
  `165db6a`, measured on 2026-10-21. Its untracked `.codex/agents/` was left
  untouched. The start hook reported `coding-harness-dd` working in this same
  checkout; the later session-scan command printed no rows, which does not
  establish that the other session stopped.
- Handover branch: `docs/handover-2026-10-21-research-exclusions`, based on freshly
  fetched `origin/main` at `165db6a`.
- Handover worktree:
  `/Users/mikypiky/coding-harness/.claude/worktrees/handover-2026-10-21-research-exclusions`.
  This session owns only this handover worktree and document, not the repair.
- The research branch is `explore/research-swarm`; its local registered worktree
  was at `4f641b4`, while GitHub reports PR #158 at `a05360c`. Do not assume that
  worktree is current or idle, and do not reset it without coordinating ownership.
- An additional open handover PR was observed on 2026-10-21:
  [PR #207](https://github.com/bicycle-brakes/monotrope/pull/207),
  “the closed merge queue and the open research swarm.” Its document was not
  read by this session. The earlier repair-stack handover was read, but its
  historical PR state must not be treated as current.
- The handover commit and PR URL are provided in the publishing result in chat;
  find the PR by the handover branch above when resuming without chat.

## Validation

- Completed on 2026-10-21: source inspection of `a05360c` and isolated admission
  reproductions described above. No real foreign-model calls or CLI end-to-end
  reproduction were performed, and no implementation files changed.
- GitHub initially failed in the restricted environment. An approved expanded
  network invocation subsequently fetched main and read the open PR identities;
  GitHub must not be described as still wholly unreadable.
- Handover validation on base `165db6a`, 2026-10-21:
  `/Users/mikypiky/coding-harness/.venv/bin/python3 -B -m pytest tests/test_feedback_channel.py -q -p no:cacheprovider`
  from the handover worktree: **59 passed, 13 skipped**. The startup preview
  (`~/.Codex/hooks/handover.sh show`) found this document and its next step.
  The full implementation suite was not rerun for this Markdown-only handover.
- Current GitHub checks for PR #158 at `a05360c`, read on 2026-10-21:
  `gates (3.12)` failed, `verify` failed, `drift` skipped
  ([workflow run](https://github.com/bicycle-brakes/monotrope/actions/runs/39605733263)).
  The failure logs were not read; no causal link to this finding is asserted.
