---
title: "Gap analysis: research corpus, running harness and Omnigent-first target"
category: architecture
status: proposed
created: 2026-09-17
last_reviewed: 2026-09-19
updated: 2026-09-29
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex
  version: "2026-09-17"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [assessment, research, workflow, omnigent, gaps]
---

# Gap analysis: research versus the running harness

> **Read this first.** This document measures the repository against the
> [Omnigent-first target](2026-09-17-omnigent-first-target.md), at commit
> `eddfc0b` on 2026-09-17.
>
> - **What already works:** file-based change flow, one Beads tracker,
>   declared model endpoints, the kit manifest, the rule ladder.
> - **What blocks the pilot (P0):** no one-command quality gate
>   (`coding-harness-bo0`) and rules whose enforcers are missing here
>   (`coding-harness-2ee`).
> - **How to read it:** the tables carry the evidence; the diagrams and
>   summaries are reading aids, not sources.

**Snapshot:** repository commit `eddfc0b`, 2026-09-17. The assessment reads
the four original sources and their index in [`docs/research/`](../research/_INDEX.md), the
[2026-09-16 target proposal](target-architecture.md), the checked-in mechanism
and Beads. It compares them with the [new target](2026-09-17-omnigent-first-target.md).
`python3 -m pytest tests -q --tb=no` at this commit reported **64 failed,
182 passed, 4 skipped**. These are migration failures, not a measured defect
rate for a working harness. Absence below means absent from this checkout,
not absent from a sibling repository. The research review was measured at
`5a950c2`; its statements about that earlier state are not silently treated
as current measurements. The 2026-09-18 revision adds primary-source research
and reconciles the target documents; it does not claim a new runtime test.
The [decision continuity table](2026-09-17-omnigent-first-target.md#decision-continuity)
records every retained or amended interview outcome. A 2026-09-19
readability revision restructured presentation only — diagrams and summaries
were added; no finding changed.

One map before the table: the research corpus feeds this assessment, this
assessment feeds the target, the target drives the implementation plan.

```mermaid
flowchart LR
    R["Research corpus + index"] --> G["This gap analysis at eddfc0b"]
    G --> T["Omnigent-first target"]
    T --> P["Implementation plan"]
```

| Research Markdown | Contribution to this assessment | Boundary or correction |
|---|---|---|
| [`_INDEX.md`](../research/_INDEX.md) | Catalogues the dated sources, addenda and their review status. | It is a catalogue, not an approval of their claims. |
| [ADW reference architecture](../research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md) | Supplies task classes, context controls, traceability, enforcement and the Omnigent topology. | Its unverified runtime and numeric claims need local evidence; its numerous human gates do not replace this harness's decision protocol. |
| [Lake Switch toolchain architecture](../research/Lake-Switch-Architektur-arc42.md) | Supplies roadmap, worker protocol, worktree and backup risks, and candidate runtime policies. | Product and domain machinery remain instance-specific; its separate pre-commit gate list and ticket-body contract would duplicate harness truth. |
| [Omnigent migration plan](../research/Migrationsplan_Omnigent_Referenzarchitektur.md) | Supplies staged exit/abort criteria, policy probes and fallback rehearsal. | Its late parallel rollout is superseded by the maintainer's 2026-09-17 direction; durations and claimed features are not acceptance evidence. |
| [Corpus review](../research/2026-09-16-review-corpus-vs-running-workflow.md) | Tests the other three against the running workflow and identifies what to adopt, keep or decide. | It measured an earlier commit and recommended late Omnigent adoption before the maintainer changed direction. |
| [CrewAI assessment](../research/2026-09-18-crewai-assessment.md) | Checks OSS Flow, feedback and checkpoint primitives against the target. | Defers a second coordinator; an adapter needs a measured gap and a bounded pilot. |
| [Open Code Review assessment](../research/2026-09-18-open-code-review-assessment.md) | Checks an independent code-review engine and its proposed findings path. | Advisory candidate only; the harness reviewer and verifier retain authority. |
| [Agent Skills assessment](../research/2026-09-18-agent-skills-assessment.md) | Checks reusable techniques against phase, tracker and gate ownership. | Selective adaptation may help; wholesale installation would duplicate authorities. |

The [human-planning and gap addendum](../research/2026-09-18-human-planning-and-harness-gaps.md)
adds primary-source checks for isolation, evaluations and attention support.
Its proposed defaults require local usability validation.

## What already carries

Five capabilities are real today — each with its evidence and the reason to
keep it.

| Capability | Evidence at this snapshot | Keep because |
|---|---|---|
| File-based change flow, human question protocol and fresh-context review | [`AGENTS.md`](../../AGENTS.md), [`WORKFLOW.md`](../WORKFLOW.md), [`prompts/`](../../prompts/) | A new session and reviewer can consume artefacts rather than conversation history. |
| Beads as one operational tracker, pinned CLI and Dolt transport | [`tools/bd`](../../tools/bd), `.beads/config.yaml`, `refs/dolt/data`; `bd 1.3.0` and a create/claim/close/export/push test passed on 2026-09-17 | A single status graph survives session changes. The JSONL file is a rendered view. |
| Endpoint declarations and provenance schema | [`model-endpoints.yaml`](../../model-endpoints.yaml), [`provenance.yaml`](../../provenance.yaml), `tests/test_model_endpoints.py` | Routing and evidence can be checked against declared operators and sources. |
| Kit manifest and copy probe | [`scripts/kit/manifest.yaml`](../../scripts/kit/manifest.yaml), [`scripts/kit/probe.py`](../../scripts/kit/probe.py) | Portability can be measured. Four kit tests are still red at this snapshot. |
| Rule enforcement ladder and ramp valves | [`regelwerk.md`](../governance/regelwerk.md), [`ramp_valves.py`](../../scripts/ramp_valves.py) | Research requirements can become enforceable rules or dated debt. |

## Gaps ordered by effect on the target

Priority means delivery urgency: **P0** belongs in or around the first
parallel pilot, with its exact entry condition set in the implementation plan;
**P1** is needed before routine use; **P2** improves scale or public adoption.
Each row names evidence, action and reason. A Bead ID is only a
tracker pointer, not the explanation.

| Priority | Gap and evidence | Implement | Why |
|---|---|---|---|
| P0 | **No one-command quality gate.** No `Makefile`, platform-neutral gate file or `.github/workflows/ci.yml` exists; 27 CI tests fail. The old doctrine still calls a `ci.yml`-derived `make verify`, while decision D-10 selects a neutral manifest and CI derived from it. (`coding-harness-bo0`) | Add the gate manifest, runner, CI adapter and a known-bad test per gate; make Omnigent call the same runner. | Parallel outputs cannot be integrated safely without one repeatable verdict. |
| P0 | **Rules claim enforcers that are missing here.** 21 rule tests fail; some rows belong to the framework instance. (`coding-harness-2ee`) | Keep only harness rules, rebuild real enforcers, or lower a row with a dated valve. | A green policy prompt cannot compensate for a rule whose gate is absent. |
| P0 | **Parallel orchestration has no runnable harness adapter.** No Omnigent agent spec, pinned runtime record, policy config or test protocol exists in this checkout. The previous proposal defers parallelism to M3. | Build a first two-worker pilot in a throwaway repository, with explicit scopes, separate worktrees, bounded sessions and serial integration. | The maintainer wants coordination from the start; a concrete pilot is the earliest test of that choice. |
| P0 | **Worktree and Beads write behavior is unproven.** Embedded Dolt is single-writer, the five-check protocol is open, and current instructions prohibit writes while another session runs. (`coding-harness-m34`) | Make W0 isolation and W1 explicit coordinator permission/locking mandatory before M0 in a disposable store. Keep workers on snapshots. W2 direct writers separately require all five checks, supported mode, restore and a rule change. | The proposed topology cannot assume authority from the current rule; a test sample cannot grant embedded multi-writer support. |
| P0 | **Policy and sandbox claims are untested.** Research names approval boundaries, telemetry opt-out and sandbox behavior, but no pinned Omnigent deployment or known-bad protocol is present. (`coding-harness-eev`) | Pin a version and host, record effective configuration, prove each boundary on a safe test case, measure egress and rehearse fallback. | The server's claimed controls count only if they fire in the chosen environment. |
| P0 | **Worktree policy and cost-stop semantics are unproven.** The research warns about directory-change policies and cost policies that may downgrade instead of stopping. | Probe legitimate worktree creation and real termination; enforce finite total-run and worker budgets covering coordinator, review, retries and in-flight calls. | Per-worker limits alone leave aggregate spend and orphaned child processes unbounded. |
| P0 | **Runtime state and data flow need one explicit contract.** The sources alternate between runtime-held coordination and Git/Beads truth. | Record run/attempt ownership, checkpoints and remaining budgets; reject stale results; cancel descendants before reassignment. Define serial candidate assembly, evidence bound to SHAs/contract/configuration and human final merge. | A restart or code change must not reuse permissions, duplicate claims or accept an obsolete green verdict. |
| P0/P1 | **Proportionality is prose, not an enforced field.** Spec/class templates and validators are missing. (`coding-harness-9qo`, `coding-harness-jc3`) | Deliver all D-2 fields before M0: goal, acceptance, non-goals, class, protected areas, failure mode, size/context budget and change-specific DoD. Complete class ratchet and design phase 2b by M1. | Omitting protected areas or failure behavior leaves worker scope underspecified. |
| P0/P1 | **Handover and review templates are incomplete.** Findings, plan markings and generated verification reports are absent. | Ship the minimum review contract before M0: SPEC/MAINT, base/fix origin, severity, ambiguity/divergence and two-round escalation. Complete kit templates by M1. | An empty valid findings list must pass; an ambiguous or divergent result must block. |
| P1 | **The doctrine and adapters disagree.** `WORKFLOW.md` still names fixed vendors and a late evaluative meta-harness; `CLAUDE.md` points to, but does not import, `AGENTS.md`. (`coding-harness-21f`) | Rewrite doctrine around phase requirements and the confirmed early parallel target; fix the adapter import; keep vendor choices in routing files. | Conflicting instructions make the runtime's behavior unpredictable and erode portability. |
| P1 | **Model routing is not a validated instance file.** Endpoint declarations exist, but `model-routing.yaml`, schema and profile resolution do not. (`coding-harness-qvl`) | Map phase requirement to model and declared endpoint; reject unknown entries before a run. | Parallel dispatch increases the chance of an undeclared provider or residency mismatch. |
| P1 | **Foreign-model qualification is incomplete.** No active foreign profile/leak gate exists here. | Retain all D-13 conditions: three full seven-phase runs with metrics, lakeswitch disclosure, green leak checks in each run and declared endpoint residency. Check all model calls, including coordinator/routing. | Cross-vendor use needs both measured workflow readiness and permission to transmit the data. |
| P0 | **No measured run supervision.** No qualified runner proves bounded retries, ownership takeover or child cancellation. | Start with two coding workers and at most two attempts per task; test whole-run spend/time/call limits, approval timeout, stopped-writer takeover and rejection of late results. | A retry must not reset cost or accidentally activate a second coordinator. |
| P0 | **Tracker export discipline is configured but not gated.** Auto-export is off; renderer and identity gate are absent. (`coding-harness-bo0`) | Deliver renderer and identity gate together before M0; render only at coordinator session end under the lock. | An identity gate cannot depend on an undelivered renderer or allow concurrent writers. |
| P1 | **No full Beads restore exercise.** The research distinguishes issue-level JSONL recovery from a full `bd backup`; neither a full-backup policy nor a restore rehearsal is present here. | Establish a version-pinned backup procedure and restore it into a disposable checkout before storage migration or routine parallel operation. | A green export does not prove recovery of Dolt history, branches or non-issue data. |
| P1 | **No explicit human planning surface.** The kit lacks a roadmap/start-page contract; the Lake Switch source contains an Obsidian pattern without a portable implementation here. | Add Now/Next/Later direction, a generated next-action/decision/resume view and a human idea inbox; keep executable status in Beads. Trial optional Obsidian, Foam or Zettlr with attention-friendly defaults. | Humans need a small entry point and an easy restart after interruption, without maintaining another task database. |
| P0/P1 | **Compaction and discovered-work protocol are incomplete.** The review proposes protected resume context but no tested mechanism exists here. | Before M0, define and test a packet containing IDs, SHAs, scope, decisions, verdicts, checkpoint and remaining budgets plus startup preflight. Complete discovered-work and spec-delta conventions in M1. | A fresh context must not lose constraints or silently expand scope. |
| P1 | **The public-template rule conflicts with the chosen runtime.** The older target says no vendor name appears in the harness, while the maintainer now explicitly chooses Omnigent as its reference runtime. | Distinguish runtime/tool names from model-provider, employer and customer identifiers in the public-readiness rule; test the intended boundary. | An overbroad denylist would reject the harness's own target documents. |
| P2 | **The corpus has unresolved document defects.** The [existing review](../research/2026-09-16-review-corpus-vs-running-workflow.md) lists dates, missing images, ADR collisions, unsourced numbers and unverified Omnigent/CVE claims. (`coding-harness-bt8`) | Correct mechanics, attach sources or mark claims unverified, and preserve the research as dated evidence. | A misleading source can be copied into a binding policy or upgrade decision. |
| P1 | **Public adoption is not ready.** No licence, onboarding or public scan exists. (`coding-harness-lir`) | Start foundations immediately and finish by M1, retaining D-17; publish only after the declared kit-probe and unfamiliar-reader qualification. | The original decision required early foundations, not a P2 deferral. |
| P0 | **Checkers can be weakened unless protected.** The ADW source requires protected controls; this checkout has no qualified worker boundary. | Prevent ordinary workers from editing active gates, hooks, policies or expected outcomes; evaluate maintenance changes with an approved verifier and a harmless bypass fixture. | A worker must not approve itself by changing its acceptance conditions. |
| P0 | **Worktrees share Git resources.** Separate directories alone do not restrict shell, symlink, child-process or shared-ref writes. | Test and constrain each route, mediate branch operations and hold M0 if isolation fails. | File separation is not a security boundary. [Git reference](https://git-scm.com/docs/git-worktree) |
| P1 | **No behavioral qualification set.** Existing schema/script tests do not establish agent or reviewer correctness. | Run fixed faulty, clean and ambiguous cases repeatedly; protect expected outcomes; compare outcomes, false positives and cost before model/prompt/runtime upgrades. | A required real defect would reward false positives; a clean real PR may pass. |
| P1 | **Third-party components lack a qualification boundary.** CrewAI, Open Code Review and Agent Skills have not been run against this harness; upstream docs do not establish worktree isolation, review dispositions or gate authority. | Keep Omnigent as selected coordinator; require a pinned, synthetic, bounded comparison for any adapter or selectively imported skill. Protect rules and prompts as control inputs, and retain D-13 before real foreign calls. | Optional additions must demonstrate a named gain without adding a second tracker, gate list or unreviewed authority. |
| P1 | **Kit copying does not prove a usable instance.** A manifest and empty scaffold probe omit complete contracts and update/rollback behavior. | Specify each artifact's role/destination, render useful scaffolds, complete a first Bounded change and resume, then rehearse a preserving update and rollback. | Reusability requires a working path, not just copied files. |
| P1 | **Architecture decisions can disappear during rewrite.** The first new draft omitted LikeC4 and parts of the original interview. | Retain D-15's shared LikeC4 specification, arc42/MADR and applicable build gate; map every D/O decision explicitly. | A sequencing change must not silently reopen agreed architecture. |

## Research intake decisions

One disposition per research proposal — adopt, adapt, or decline, each with a
reason.

| Research proposal | Disposition | Reason |
|---|---|---|
| Phase artefacts, fresh-context review, living spec and dated handover | **Retain and complete** | The existing workflow already has the right ownership model; validators and templates are incomplete. |
| Four task classes, one-way ratchet, requirement-to-test trace, search-first dependency check | **Adopt proportionately** | These close real gaps; begin with fields and actionable checks before adding broad audit machinery. |
| Roadmap, `discovered-from` edges, compaction protect list and living-spec delta vocabulary | **Adopt with one owner each** | These fill direction, provenance and resume gaps without creating a second task tracker or a second gate list. |
| Omnigent as runtime with policies, sandbox, budgets and parallel dispatch | **Adopt as the target, prove locally** | Official [agent](https://github.com/omnigent-ai/omnigent/blob/main/docs/AGENT_YAML_SPEC.md) and [policy](https://github.com/omnigent-ai/omnigent/blob/main/docs/POLICIES.md) documentation describes the mechanisms; the corpus does not prove this installation or exact release. |
| Parallel agents only at migration M3; Polly optional | **Superseded by 2026-09-17 direction** | Parallel coordination belongs in M0. Production breadth still grows through measured gates. |
| Human approval at every G0–G3/G5 gate | **Do not adopt wholesale** | The solo workflow asks the human for intent and exceptions; machine presence and verification gates carry routine checks. |
| Transcribe every plan step into Beads | **Use when independent workers need claims** | One Bead per change keeps the serial path small; parallel task Beads become useful after tracker coordination is proven. |
| A second pre-commit gate list, a second ticket contract, confidence-scored learned rules | **Do not adopt** | Each would create a competing source of truth or unmeasured authority. |
| Portable human planning templates and status projections | **Adopt in M1** | They reduce reconstruction work and can be used with any Markdown editor. Obsidian/Foam configurations are optional adapters; personal knowledge stays local. |
| Static site, domain gates and product-specific release machinery | **Keep in instances** | They remain instance concerns and do not replace harness authorities. |

## Remaining uncertainty

The local test run measures migration state, not how effective a future
Omnigent workflow will be. No concurrent worktree or sandboxed agent was run
for this assessment. The exact Omnigent policy schema, default sandbox and
worktree behavior must be checked against the **pinned release selected for
the pilot**; upstream `main` documentation is a design source, not a version
lock. The first pilot should measure throughput, review findings, human time
and cost against a serial run of comparable work. Whether Dolt server mode is
needed remains a test result, not an architectural assumption.
