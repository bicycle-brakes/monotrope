---
title: "Gap analysis: research corpus, running harness and Omnigent-first target"
category: architecture
status: proposed
created: 2026-09-17
last_reviewed: 2026-09-17
owner: maintainer
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

**Snapshot:** repository commit `eddfc0b`, 2026-09-17. The assessment reads
the four documents in [`docs/research/`](../research/_INDEX.md), the
[2026-09-16 target proposal](target-architecture.md), the checked-in mechanism
and Beads. It compares them with the [new target](2026-09-17-omnigent-first-target.md).
`python3 -m pytest tests -q --tb=no` at this commit reported **64 failed,
182 passed, 4 skipped**. These are migration failures, not a measured defect
rate for a working harness. Absence below means absent from this checkout,
not absent from a sibling repository. The research review was measured at
`5a950c2`; its statements about that earlier state are not silently treated
as current measurements.

| Research Markdown | Contribution to this assessment | Boundary or correction |
|---|---|---|
| [`_INDEX.md`](../research/_INDEX.md) | Defines the four dated sources and their pending review status. | It is a catalogue, not an approval of their claims. |
| [ADW reference architecture](../research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md) | Supplies task classes, context controls, traceability, enforcement and the Omnigent topology. | Its unverified runtime and numeric claims need local evidence; its numerous human gates do not replace this harness's decision protocol. |
| [Lake Switch toolchain architecture](../research/Lake-Switch-Architektur-arc42.md) | Supplies roadmap, worker protocol, worktree and backup risks, and candidate runtime policies. | Product and domain machinery remain instance-specific; its separate pre-commit gate list and ticket-body contract would duplicate harness truth. |
| [Omnigent migration plan](../research/Migrationsplan_Omnigent_Referenzarchitektur.md) | Supplies staged exit/abort criteria, policy probes and fallback rehearsal. | Its late parallel rollout is superseded by the maintainer's 2026-09-17 direction; durations and claimed features are not acceptance evidence. |
| [Corpus review](../research/2026-09-16-review-corpus-vs-running-workflow.md) | Tests the other three against the running workflow and identifies what to adopt, keep or decide. | It measured an earlier commit and recommended late Omnigent adoption before the maintainer changed direction. |

## What already carries

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
| P0 | **Worktree and Beads write behavior is unproven.** Current Dolt is embedded, one-writer; the five-check worktree verification is open. (`coding-harness-m34`) | Keep coordinator-only tracker writes for the first parallel pilot; verify visibility, environment, prefix, write and concurrency in a throwaway repository; decide on server mode from the result. | Parallel coding is possible now, while an untested shared write path could lose claims or block workers. [Beads documents the mode distinction.](https://github.com/gastownhall/beads/blob/main/docs/architecture/dolt.md) |
| P0 | **Policy and sandbox claims are untested.** Research names approval boundaries, telemetry opt-out and sandbox behavior, but no pinned Omnigent deployment or known-bad protocol is present. (`coding-harness-eev`) | Pin a version and host, record effective configuration, prove each boundary on a safe test case, measure egress and rehearse fallback. | The server's claimed controls count only if they fire in the chosen environment. |
| P0 | **Worktree policy and cost-stop semantics are unproven.** The Lake Switch source warns that `block_working_dir_changes` may block `git worktree add` and that `cost_budget` may downgrade a model instead of ending a run. | Probe worktree creation under the effective policy and deliberately cross a small cost limit; add an external kill control if the runtime does not stop. | Parallel isolation and bounded cost are core pilot conditions, not conclusions from a policy name. |
| P0 | **Runtime state and data flow need one explicit contract.** The research alternates between Omnigent-held coordination and Git/Beads as truth. | Define the coordinator's input/output record, worktree ownership, checkpoint and crash-resume procedure in the adapter. | A parallel run must remain reconstructable when Omnigent disappears. |
| P1 | **Proportionality is prose, not an enforced field.** No spec template, four-class validator or design prompt exists. (`coding-harness-9qo`, `coding-harness-jc3`) | Add Spike/Bounded/Feature/Architectural classification, ratchet, class-specific artefacts, Definition of Done and design phase 2b. | The research's useful task classes prevent both underplanning and ceremony on small changes. |
| P1 | **Handover and review templates are incomplete.** Only gate-record and handover templates exist; `findings.md`, plan markings and a generated verification report are absent. | Bring the missing templates and a verdict-only report into the kit, with tests for the fields downstream stages read. | Reviewers and resumed sessions need stable, compact inputs. |
| P1 | **The doctrine and adapters disagree.** `WORKFLOW.md` still names fixed vendors and a late evaluative meta-harness; `CLAUDE.md` points to, but does not import, `AGENTS.md`. (`coding-harness-21f`) | Rewrite doctrine around phase requirements and the confirmed early parallel target; fix the adapter import; keep vendor choices in routing files. | Conflicting instructions make the runtime's behavior unpredictable and erode portability. |
| P1 | **Model routing is not a validated instance file.** Endpoint declarations exist, but `model-routing.yaml`, schema and profile resolution do not. (`coding-harness-qvl`) | Map phase requirement to model and declared endpoint; reject unknown entries before a run. | Parallel dispatch increases the chance of an undeclared provider or residency mismatch. |
| P1 | **Foreign-model disclosure and leak checks are not active here.** The research review identifies residency as a gap in the corpus; no `make leakcheck` or foreign profile exists in this checkout. | Add the barrier before cross-vendor review; require the instance's disclosure decision and endpoint declaration. | A cross-vendor reviewer is useful only if data may be sent there. |
| P1 | **No measured session limits.** The migration research requests time, idle and spend stops, but no runner or session metrics exist here. | Record per-worker wall time, cost, iterations/tool calls, last progress, stop reason and human minutes; test each stop with a fake worker. | Parallelism multiplies cost and stalled work unless each worker is bounded. |
| P1 | **Tracker export discipline is configured but not gated.** `export.auto` is off and a manual export matched the database, but the one-writer export script and identity gate are absent. (`coding-harness-bo0`) | Render once at session end, compare byte identity and test stale/foreign writes. | A rendered file should not become a competing truth or a source of merge conflicts. |
| P1 | **No full Beads restore exercise.** The research distinguishes issue-level JSONL recovery from a full `bd backup`; neither a full-backup policy nor a restore rehearsal is present here. | Establish a version-pinned backup procedure and restore it into a disposable checkout before storage migration or routine parallel operation. | A green export does not prove recovery of Dolt history, branches or non-issue data. |
| P1 | **No explicit planning layer above tasks.** There is no `ROADMAP.md` template in the kit. | Add a short Now/Next/Later roadmap with appetite and links to Beads epics when relevant; keep executable tasks only in Beads. | `bd ready` answers what is executable; a developer also needs the current direction and reason. |
| P1 | **Compaction and discovered-work protocol are incomplete.** The review recommends protecting current decisions and gate state on compaction and linking newly discovered work with `discovered-from`; neither is a tested harness mechanism here. | Add a tested compact handoff or hook, plus a documented discovered-work edge and a check where feasible. | Long or parallel sessions must retain constraints and prevent scope creep from disappearing into an unrelated task. |
| P1 | **The public-template rule conflicts with the chosen runtime.** The older target says no vendor name appears in the harness, while the maintainer now explicitly chooses Omnigent as its reference runtime. | Distinguish runtime/tool names from model-provider, employer and customer identifiers in the public-readiness rule; test the intended boundary. | An overbroad denylist would reject the harness's own target documents. |
| P2 | **The corpus has unresolved document defects.** The [existing review](../research/2026-09-16-review-corpus-vs-running-workflow.md) lists dates, missing images, ADR collisions, unsourced numbers and unverified Omnigent/CVE claims. (`coding-harness-bt8`) | Correct mechanics, attach sources or mark claims unverified, and preserve the research as dated evidence. | A misleading source can be copied into a binding policy or upgrade decision. |
| P2 | **Public adoption is not ready.** No licence, onboarding path or public-readiness scan exists. (`coding-harness-lir`) | Add these after the executable path works and run the kit probe in a fresh repository. | The target is a reusable public template; newcomers need a working first change. |

## Research intake decisions

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
| Obsidian, static site, domain gates and product-specific release machinery | **Keep in instances** | They describe a development environment, not a portable coding harness. |

## Remaining uncertainty

The local test run measures migration state, not how effective a future
Omnigent workflow will be. No concurrent worktree or sandboxed agent was run
for this assessment. The exact Omnigent policy schema, default sandbox and
worktree behavior must be checked against the **pinned release selected for
the pilot**; upstream `main` documentation is a design source, not a version
lock. The first pilot should measure throughput, review findings, human time
and cost against a serial run of comparable work. Whether Dolt server mode is
needed remains a test result, not an architectural assumption.
