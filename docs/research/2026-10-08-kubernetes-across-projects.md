---
title: "Kubernetes across Coding Harness, LakeSwitch and ADHD Relief"
category: research
status: proposed
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
owner: framework-architect
provenance: ai-generated
produced_by:
  kind: llm-session
  name: codex
  version: "2026-10-08"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, kubernetes, runners, lakeswitch, adhd-relief]
---

# Kubernetes across the three projects

## Recommendation

Start with a bounded, read-only verifier experiment in Coding Harness.
LakeSwitch can later reuse the execution pattern for independent validation
and reconciliation tasks. Keep ADHD Relief's personal assistant on its
accepted macOS architecture. A shared production cluster for all three is
not justified by the workloads inspected.

This is desk research requested by the maintainer on 2026-10-08, not an
architecture decision or an implementation. No image, cluster or service was
started. Kubernetes manages container execution; the projects retain their
contracts, workflow gates, approvals and task ownership.

## Evidence and cut-off

| Repository | Inspected state | What supports the assessment |
| --- | --- | --- |
| Coding Harness | Freshly fetched `origin/main`, `0e231c1`, 2026-10-08 | Workflow, gate runner, dependency lock, accepted Hermes ADR and latest handovers; earlier Kubernetes assessment |
| LakeSwitch | Local checkout `09c9d62`, 2026-10-08; two commits behind its locally known remote | Instructions, README, Python metadata, CLI registration, platform and live-probe specifications, latest journal and its addendum |
| ADHD Relief | Local branch `wechsel-hermes`, `bdce8dc`, 2026-10-08; one commit ahead of its locally known remote | Instructions, canonical arc42 deployment view and latest local handover |

The sibling repositories were read only. Their current GitHub PR states were
not queried, and their deployed systems were not inspected. Their local
documents support an assessment of the design, not proof of a running service.
No personal vault or customer-instance material was read. Primary external
documentation below was checked on 2026-10-08.

## Coding Harness: the strongest first experiment

The existing [gate-runner proposal](2026-09-26-kubernetes-gate-runner.md)
already identifies the right first workload: execute the canonical verifier
for one commit and return evidence. Its historical reasoning needs updating:

- PyYAML is now pinned, with hashes in `requirements-ci.txt`; `make venv`
  creates a checkout-local environment. The runner prefers that environment.
  Dependency pinning alone is no longer a missing capability.
- One image can additionally fix the operating-system tools and interpreter.
  That benefit comes from container packaging. Kubernetes adds job lifecycle,
  scheduling, concurrency controls and resource management.
- The older sample ADR number is historical, not available for a new ADR.
  Later accepted records also choose Hermes on the Mac for unattended writing
  ([ADR 0010](../adr/0010-hermes-first-unattended-writing-agent.md)). Moving that
  writer into Kubernetes would require a separate architecture change.

A verifier Job should receive an exact repository SHA, image digest and
tracker snapshot identity, use a disposable checkout, and call the existing
gate runner. Git history and base refs required by gates must be available;
a source archive alone is insufficient. Hydrate and render the tracker using
the existing bootstrap/render path, without tracker writes. Record its data
revision or render hash: the same code SHA against a changing tracker is not
the same experiment.

Keep the canonical gate list in `decisions/gates.yaml`. Distinguish local and
hosted placements: `make verify` passing in a pod does not establish that
hosted-only checks passed. Compare each placement against its counterpart,
including declared exclusions. Persist commit, base, tool versions, gate
configuration, command, exit code and raw output outside disposable pods.

Later candidates are a matrix of commits or synthetic fixtures using Indexed
Jobs, followed by read-only drift checks using CronJobs. Agent workers come
later still: retain the leak-check entry point, existing model routing,
credential boundaries and one tracker writer. A scheduler must never assign
unlimited writing sessions or turn a retry into another publish operation.
The [Jobs documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
describes indexed execution, deadlines and retries, including possible
duplicate execution even for a single-completion Job.

## LakeSwitch: execution around the engine

The inspected implementation exposes contract validation, compose planning,
code generation, synthetic fixtures and reconciliation. These are CLI workloads,
not an inspected long-running web service. The local metadata still requires
Python 3.11; the Coding Harness handover records a maintainer preference to
move LakeSwitch to 3.12, but that is not implemented in the checkout inspected.
Use each project's actual pins when building its image.

| Candidate | Kubernetes form | Practical boundary |
| --- | --- | --- |
| Validate contracts and check generated artifacts | Job per immutable input package | Return findings and generated output; acceptance stays with the maintainer |
| Repeat synthetic fixture checks | Indexed Job per seed/profile/run | Independent workspaces and separately identified results |
| Reconciliation over independent slices | Jobs with bounded parallelism | Establish valid partitioning, complete coverage and final aggregation first |
| Live source probes | Future Job per approved probe | The inspected CLI does not register the live-probe module; its specification is not an implementation |
| Periodic platform checks | Future CronJob | Add only once a concrete check exists; preserve the deployment scope of each proof |

LakeSwitch distinguishes exit codes for clean results, gaps, breaches and
human refusal. Kubernetes initially sees process success or failure; a Job
adapter must preserve the domain verdict and avoid treating a declared gap or
pending decision as a transient infrastructure failure to retry.

Keep data processing in the chosen lakehouse or database runtime. Kubernetes
could coordinate LakeSwitch's work without becoming the data platform. CPU
limits on a pod do not cap remote query spending or model charges; retain
domain budgets and account-level limits. Parallelism must respect source-system
load and the scope of each comparison.

Use CI or an ordinary container first. A customer that already operates a
cluster, or measured demand for many independent runs, can justify a Kubernetes
adapter. A new dedicated cluster solely for the current CLI adds an operator
responsibility without an established product requirement.

## ADHD Relief: retain the macOS core

The canonical deployment view selects a MacBook, later a Mac mini, Hermes under
a dedicated service user, launchd, local Vault access and CouchDB as a Homebrew
service. Native calendar/reminder bridges, MapKit and the screen intervention
depend on the Mac and its user session. Linux pods would require bridges back
to the host and a redesign of credentials and Vault permissions; they would
not replace those dependencies.

An optional later split could run the Telegram gateway, outbound scanner or
speech transcription on an always-on host, while native bridges remain local.
Those are candidates, not deployments established here. CouchDB would need
durable storage and a tested restore path; a StatefulSet/PVC is not itself a
backup or high-availability design. The
[storage documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
explains the separation between pod lifecycle and persistent storage.

For one personal system, launchd on the Mac or a simple service on an always-on
host is the smaller operating burden. Kubernetes on the same sleeping MacBook
cannot remove that host's availability dependency. Its CronJobs also provide
approximate scheduling, not a precise alarm clock: duplicate or missed Jobs
are possible, and work must tolerate repetition
([CronJob documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)).
Keep time-sensitive anchors and existing catch-up rules in the personal system.

## Shared platform boundaries

Share image-building conventions and a result format before sharing runtime
credentials, storage or a cluster. Separate project namespaces can organise
development runs, but namespaces alone do not isolate a personal Vault from
untrusted agent code. Production isolation would need a chosen trust model,
RBAC, quotas, restricted pod privileges and effective network enforcement
([multi-tenancy documentation](https://kubernetes.io/docs/concepts/security/multi-tenancy/)).

Do not mount a personal Vault, home directory, Docker socket or shared writable
tracker into experimental workers. Keep verifier credentials read-only and
separate any later publishing controller from workers. Kubernetes Secrets do
not automatically prevent a process that receives a credential from using or
exposing it ([Secrets guidance](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)).

NetworkPolicy requires a supporting network plugin; merely applying its YAML
does not enforce isolation. Standard rules operate on IPs/ports and selectors,
so a hostname allowlist needs an additional supported mechanism. Verify both
permitted and forbidden traffic on the chosen runtime
([network-policy documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/)).
The historical k3s/Cilium issues in the older note were not re-investigated
here and must not be read as current findings.

## Proposed first pilot and adoption trigger

1. Package only the Coding Harness verifier, with a digest-pinned base and the
   existing tool pins. Run the same commit as a local container and compare it
   with the corresponding canonical checks. Include a deliberately broken input.
2. Run the same image as one Kubernetes Job, first against synthetic inputs,
   with a deadline, bounded resources and no automatic application retries.
   Export successful and failed reports before cleanup; test absence of push
   authority. Repetition must produce no shared-state mutation.
3. Compare a small independent matrix with CI/container execution: total time,
   setup and maintenance effort, resource use and completeness of evidence.
   Adopt Kubernetes only if that comparison shows value, or explicitly choose
   a bounded learning exercise as its purpose. Stop after the experiment if
   container execution already meets the need.

OrbStack offers a local single-node development cluster and shares locally
built images with it ([OrbStack documentation](https://docs.orbstack.dev/kubernetes/)).
Its inspected page does not establish NetworkPolicy enforcement, and no local
installation was checked. Select the runtime only after verifying availability
and the controls needed by the experiment. A single development node does not
establish resilience to host failure. Production operation adds infrastructure,
access, upgrades and recovery responsibilities
([production guidance](https://kubernetes.io/docs/setup/production-environment/)).

The pilot is proposed, not authorised by this research request. Its owning
session must classify new paths, follow the normal spec/design/plan workflow
and obtain the maintainer's architecture decision before implementation. No
Argo CD, operators, monitoring stack or three-project migration is needed to
answer the first experiment's question.
