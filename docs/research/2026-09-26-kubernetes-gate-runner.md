---
title: "Kubernetes gate runner — a pinned verifier container, run as a Job (proposal)"
category: research
status: proposed
created: 2026-09-26
last_reviewed: 2026-09-27
updated: 2026-09-29
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-cowork
  version: "2026-09-27"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, kubernetes, verify, reproducibility, gates, proposal]
---

# Kubernetes gate runner — assessment

Read against `main` at `4e7ea5c` on 2026-09-26; nothing in the repository was
changed. Written first as a note in the maintainer's vault and moved here on
2026-09-27, because an assessment of this repository belongs to it; the
maintainer's personal reasons stay in the vault. A desk review: nothing was
built or run.

**Summary.** The first use case is the gate runner (`make verify`) as a
Kubernetes Job, not the agent worker. It needs no model, no subscription and
no tracker write access, and it closes an open requirement of the harness:
reproducible reports.

## Why the gate runner first

The implementation plan requires that a test report records
"interpreter/dependency versions, command, commit and raw-output location"
([plan](../architecture/2026-09-17-implementation-plan.md)), and local and CI
runs should return the same gate IDs and verdicts (bead `coding-harness-bo0`).
Today CI takes Python from `ubuntu-latest`, PyYAML is unpinned, and
`scripts/verify_all.sh` uses the first `python3` it finds that imports
`yaml`. An image with a fixed digest closes that gap. That is the measured
missing function the plan asks of every third-party component.

## Corrections to a first sketch

| First sketch | Checked | Correction |
|---|---|---|
| Every bead becomes a Job; the pod claims, works and pushes | Each pod would be another clone pushing `refs/dolt/data`, which is seam 1 of the Agent SDK note and not yet measured ([ADR 0005](../adr/0005-workers-claim-their-own-bead.md): "A second machine is outside one Omnigent server's policies"). W2 also keeps worker-side tracker access disabled | Pods never write the tracker and never push; they read only |
| API keys as a Secret, agents in the pod | [`model-endpoints.yaml`](../../model-endpoints.yaml): the subscription only through officially supported tools; an own integration takes `anthropic-api`. `--bare` reads neither the subscription login nor `CLAUDE_CODE_OAUTH_TOKEN` | Model calls from pods only after decision 1 of `docs/research/2026-09-26-agent-sdk-and-formal-models.md`; until then without a model |
| NetworkPolicy "model API and GitHub only" | Standard NetworkPolicy works with IPs and CIDRs, not host names. Cilium offers FQDN rules but has known start-up problems in k3d. k3s enforces policies through kube-router, which filters nothing in the first milliseconds after a pod starts (open issue k3s#14711) | Default deny plus an egress proxy with a host list, and a known-bad test: a forbidden host must fail |
| k3d on the Mac | OrbStack has a built-in single-node Kubernetes; locally built images run without a registry (a tag other than `:latest`, or `imagePullPolicy: IfNotPresent`). Whether OrbStack enforces NetworkPolicies is not documented | Stages 1 to 3 on OrbStack, stage 4 on k3d (k3s) |
| Argo CD reads the repository | The repository is private | A read-only token (fine-grained PAT or deploy key); secrets never in git, later Sealed Secrets or SOPS |
| Just create `deploy/` | Kit manifest: an unclassified file is a BLOCK, and the `leerprobe` gate blocks | Classify `deploy/` in `scripts/kit/manifest.yaml`, `scripts/export/manifest.yaml` and `provenance.yaml` |
| The container runs the gates | `scripts/verify_all.sh` has no commands of its own; the only list is `decisions/gates.yaml` (D-10) | The image calls only `scripts/verify_all.sh` and names no gate |

## Stages

Each stage is complete on its own.

| Stage | What | Evidence, known-bad included | Effort |
|---|---|---|---|
| **1 · Image** | `deploy/verify.Dockerfile`: base image pinned by digest, tool versions from `decisions/gates.yaml`, `bd` through `tools/beads/install.sh` (checksum), the tracker read-only through `git fetch origin refs/dolt/data`; entry point `scripts/verify_all.sh` | The same gate IDs and verdicts as CI on the same SHA; a deliberately broken commit turns red | about one session |
| **2 · Job** | OrbStack Kubernetes. A Job receives a SHA, clones read-only, runs and stores the report as an artifact; a Secret with a read-only token; CPU and memory limits | The Job is green on `main`; a pod without a push credential cannot push (probe) | about one session |
| **3 · Parallel** | An Indexed Job over N SHAs, for example the last five merges | N reports, each with its SHA and versions | one or two sessions |
| **4 · Egress** | On k3d: NetworkPolicy default deny; only the path to the egress proxy is allowed, and the proxy allows only `github.com` | A forbidden host fails, an allowed one works; the start-up window of k3s#14711 is documented | one or two sessions |
| **5 · GitOps** | Argo CD reads `deploy/` and rolls out through Kustomize | A commit in `deploy/` changes the cluster; a rollback through git works | about one session |
| **6 · Later** | The M1 qualification runner (`claude -p`, fixtures × 3) as an Indexed Job; Grafana and Prometheus; optionally MLflow OSS for the result records | After decision 1 of the Agent SDK note, once fixtures exist and the Omnigent status is settled | open |

**Open: the M0 status.** The repository still names M0 as next. A note in the
maintainer's vault reports that the lakeswitch journal of 2026-09-24 dropped
the M0 pilot and uses Omnigent without its sandbox; not verified here. Stages
1 to 5 do not depend on it; stage 6 does.

## Bead proposal, not created

Create it when no other session writes the tracker (house rule 4).

- **Title:** Pinned verify container and Kubernetes Job runner
- **Class:** Architectural: a new runtime component, so an ADR is required.
- **Scope:** stages 1 to 3; stages 4 and 5 get a bead each.
- **Acceptance:** the evidence of stages 1 to 3; `deploy/` classified in both
  manifests and in `provenance.yaml`; `make verify` green.
- **Out of scope:** model calls, tracker writes from pods, Omnigent.

## ADR draft, not committed as an ADR

```markdown
# ADR 0006 — Run the canonical verifier in a pinned container, optionally as a Kubernetes Job

Status: proposed (draft, not committed)

## Context
- Reports must be reproducible: every test report records its
  interpreter/dependency versions, command, commit and raw-output location
  (implementation plan). Today CI takes Python from ubuntu-latest, PyYAML is
  unpinned, and scripts/verify_all.sh picks the first local python3 that
  imports yaml.
- Local and CI must return the same gate IDs and verdicts for the same
  candidate (coding-harness-bo0).
- M0, if it stays, needs a disposable, pinned runtime; M1 qualification needs
  stable initial repositories and three runs per fixture.
- Seam 1 (claims across machines) is unmeasured; W2 keeps worker-side tracker
  access disabled.
- Declared secondary driver: the maintainer wants hands-on Kubernetes practice.

## Decision
1. One image, built from a base pinned by digest. Tool versions come from
   decisions/gates.yaml; bd comes from tools/beads/install.sh (checksum).
   The entry point is scripts/verify_all.sh. The image lists no gate.
2. The image runs the same way locally and as a Kubernetes Job. A Job receives
   one commit SHA, clones read-only, runs, and stores the report as an artifact.
3. No pod writes the tracker or pushes to origin. The credential is read-only;
   refs/dolt/data is fetched, never pushed.
4. Parallel runs use Indexed Jobs: one index is one SHA, later one
   fixture x run.
5. Model calls from pods stay out of scope until decision 1 of
   docs/research/2026-09-26-agent-sdk-and-formal-models.md is taken.
   --bare requires anthropic-api.

## Consequences
+ Reproducible reports; the same verdict locally, in CI and in a pod.
+ A substrate for the M1 qualification runner.
- The new path deploy/ must be classified in the kit and export manifests and
  in provenance.yaml.
- Image maintenance: the digest and tool versions need updates.
- A local cluster is not a security boundary (IS-5 still holds). Standard
  NetworkPolicy is IP-based; host allowlists need an egress proxy; k3s leaves
  a short unfiltered window at pod start (k3s-io/k3s#14711).

## Alternatives
- CI only: no local parity, no dedicated runtime for M0/M1.
- Container without Kubernetes: enough for reproducibility alone; lacks
  scheduling, parallel indexed runs and network policy.
- Kubernetes as an Omnigent sandbox adapter: depends on the Omnigent status.

## Evidence required for acceptance
- Same gate IDs and verdicts as CI on the same SHA.
- A known-bad commit fails inside the pod.
- A pod without a push credential cannot push.
- (Stage 4) A forbidden host is unreachable; an allowed one works.
```

## Limits and evidence status

- A desk review: no image was built, no cluster started.
- OrbStack, k3d, k3s and Cilium statements come from their documentation and
  issue trackers as read on 2026-09-26.
- The tracker was not read; bead `coding-harness-bo0` is cited from the
  architecture documents.

## Sources

- [OrbStack: Kubernetes](https://docs.orbstack.dev/kubernetes/)
- [k3s-io/k3s#14711: NetworkPolicy gap at pod start](https://github.com/k3s-io/k3s/issues/14711)
- [cilium/cilium#30706: Cilium in k3d does not start correctly](https://github.com/cilium/cilium/issues/30706)
- [Claude Code: headless mode and `--bare`](https://code.claude.com/docs/en/headless)
- [Claude Code: authentication and `setup-token`](https://code.claude.com/docs/en/authentication)
