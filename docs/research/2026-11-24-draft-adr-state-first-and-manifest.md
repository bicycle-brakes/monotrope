---
title: "Draft ADR <NNNN> — State-first machine state, single kit manifest, and shared script primitives"
category: research
created: 2026-11-24
updated: 2026-11-25
last_reviewed: 2026-11-24
status: draft
implementation_status: none
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr-draft, architecture, state-first, kit-manifest, primitives]
---

# Draft ADR `<NNNN>` — State-first machine state, single kit manifest, and shared script primitives

> [!NOTE]
> **Non-binding draft under `docs/research/`:** Under [`provenance.yaml`](../../provenance.yaml) and `scripts/check_interview_minimums.py`, files under `docs/adr/` are `human-decided` and require a Phase 1a maintainer interview plus a `decide(...)` pull request (ADR 0008). The ADR number `<NNNN>` stays unassigned here because `origin/main` ends at [ADR 0025](../adr/0025-targeted-check-after-repair.md) while `0026` and `0027` are drafted on open branches (`feat/central-config` and `feat/review-fewer-rounds`); the final number is assigned at merge.

* Proposed Status: draft for promotion via Phase 1a interview + `decide(architecture)` pull request.
* Linked live Beads: `coding-harness-5ane.11` (State-First), `coding-harness-5ane.10` & `coding-harness-5ane.7` (Single Kit Manifest & `DECKEL -> 0`), `coding-harness-5ane.12` (Shared Primitives); aligned with `coding-harness-oebl` (structured OTel GenAI JSONL audit log) and `feat/central-config`.
* Scope discipline: **Zero conflicts with settled house rules or ADRs.** House Rule 2 (*Beads only*), House Rule 9 (*one entry point and one writer per action*), `COMMERCIAL.md` (PolyForm Noncommercial 1.0.0), ADR 0021, and `coding-harness-6slq` remain untouched.
* Date prepared: `2026-11-24` · Verified baseline: `origin/main` `b9ce3ac0` / `a5b117f8`.

---

## Context

The verified re-check of the codebase at `origin/main` (`b9ce3ac0`, `2026-11-24`, summarized in [the verified audit synthesis](./2026-11-24-verified-audit-synthesis-and-roadmap.md)) confirmed three structural sources of recurring defects across `scripts/` and kit packaging:

1. **Markdown parsed back as mutable machine state (`coding-harness-5ane.11`):** Review-loop rounds, release markers, retired stages, verdicts, and runner audit lines are stored inside human-editable Markdown (`loop.md`, `findings.md`) and parsed back via dozens of ad-hoc regexes. Upcoming orchestration modules (`lanes.py`, `jobs.py`, attempt state) require reliable structured state, and `coding-harness-oebl` already decided to move runner audit output into structured OpenTelemetry GenAI JSONL. Meanwhile, `plans/INDEX.md` and `docs/governance/gate-catalog.md` already prove the clean pattern inside this repository: *machine-readable source -> deterministically rendered Markdown*.
2. **Two diverging kit manifests (`coding-harness-5ane.10`, `coding-harness-5ane.7`):** `scripts/kit/manifest.yaml` (roles) and `scripts/export/manifest.yaml` (travel verdicts) disagree in ways that break exported scripts — specifically, `scripts/export/manifest.yaml` carries `scripts/check_bead_export.py` and `scripts/check_dangling_bead_ids.py` while dropping `scripts/bead_render.py`, which both import. Simultaneously, `scripts/kit/probe.py` relies on `DECKEL = 44` permanently exempted test failures.
3. **Duplicated low-level primitives violating House Rule 9 (`coding-harness-5ane.12`):** Scripts re-implement strict YAML loading, frontmatter span parsing, atomic file writes, and `git` subprocess wrappers across many files with diverging CRLF, symlink, duplicate-key, and `GIT_*` environment handling.

## Decision Drivers

* **House Rule 9 in code:** One canonical writer and reader per recurring action, enforced by tests rather than prose.
* **Reliability for lanes, jobs, and attempts:** Machine state must be atomic, schema-validated, lock-protected, and immune to Markdown table/whitespace/CRLF drift.
* **Honest kit verification:** Every exported script must have its Python imports verified automatically, driving `DECKEL` down from `44` to `0`.
* **Zero rule churn:** Deliver high-leverage structural hygiene without reopening settled governance decisions (Beads, licensing, model routing, or entry points).

## Considered Options

### Option 1 — Keep Markdown state, dual manifests, and per-script helpers
Fix individual regex bugs and add `scripts/bead_render.py` to `scripts/export/manifest.yaml` as point patches.
* *Pros:* Smallest immediate diff.
* *Cons:* New orchestration (`lanes.py`, `jobs.py`, attempt state) would either invent yet another state format or deepen Markdown regex fragility; dual manifests continue drifting silently; duplicated YAML/atomic/git helpers keep reintroducing identical edge-case bugs.

### Option 2 — Adopt state-first JSON/JSONL, one kit manifest, and shared primitives *(Recommended)*
Standardize machine state on locked JSON/JSONL with deterministic Markdown rendering, unify kit classification into one manifest aligned with `feat/central-config`, and centralize YAML, atomic-FS, and git primitives.
* *Pros:* Directly unblocks `lanes.py`, `jobs.py`, `coding-harness-oebl`, and `coding-harness-vg9`; eliminates an entire class of parser and export-dependency bugs; stays 100% within existing house rules.
* *Cons:* Requires a short dual-read migration window for active `loop.md` files and incremental test cleanup to move `DECKEL` from `44` to `0`.

## Decision

Chosen option: **Option 2 — State-first JSON/JSONL, single kit manifest, and shared script primitives.**

### 1. State-first machine persistence (`coding-harness-5ane.11`, aligned with `coding-harness-oebl`)

1. All mutable orchestration state — review-loop rounds, consumed/retired stages, Phase-6 verdicts, lane state (`lanes.py`), detached job state (`jobs.py`), and attempt state — MUST persist canonically in schema-validated, file-locked JSON/JSONL files.
2. Human-facing Markdown (`loop.md`, released blocks in `findings.md`, `plans/INDEX.md`, `gate-catalog.md`) is deterministically rendered from structured state (`machine-rendered`), never parsed back via regexes to recover control state.
3. Structured runner event/audit logs follow the OpenTelemetry GenAI JSONL contract established in `coding-harness-oebl` (one producer, one read interface, many readers; plain files only, no visual dashboards per `AGENTS.md`).
4. A bounded dual-read fallback handles in-flight `loop.md` files during migration and is removed once active changes roll over.

### 2. Single kit manifest & dependency-verified export (`coding-harness-5ane.10`, `coding-harness-5ane.7`)

1. Retire `scripts/export/manifest.yaml`; maintain **one** declarative kit manifest (`scripts/kit/manifest.yaml`, aligned with `feat/central-config`) as the single source of truth for what travels with the kit vs. stays repository-local (`bestand`).
2. `scripts/kit/probe.py` MUST verify static import closure for every exported Python script so missing dependencies (such as `scripts/bead_render.py`) fail immediately at manifest check time rather than at runtime in a target repository.
3. Drive `DECKEL` in `scripts/kit/probe.py` monotonically from `44` to `0` by isolating repository-inventory tests into `bestand` and fixing genuine portability gaps in `mechanismus` tests.

### 3. Shared script primitives (`coding-harness-5ane.12`)

1. Extract and standardize three leaf primitives under `scripts/` (requiring Python 3.12+ stdlib + `PyYAML` only):
   * `_yaml_strict.py`: single duplicate-key-rejecting `SafeLoader` and BOM/CRLF-safe frontmatter span reader;
   * `_fs_atomic.py`: single symlink-safe (`lstat` check) temp-file + `fsync` + `os.replace` writer;
   * `_git_exec.py`: single `GIT_*`/`LC_ALL`-sanitized git subprocess runner with explicit timeouts.
2. All new and refactored scripts MUST import these shared primitives rather than introducing local copies, enforced by an AST/import guard test.

## Consequences

### Positive
* `lanes.py`, `jobs.py`, `stage2.py` attempts, and `coding-harness-oebl` share one clean, lock-safe JSON/JSONL persistence pattern.
* Eliminates Markdown regex state corruption, CRLF/table escaping regressions, and silent missing-import bugs in exported kits.
* Keeps future multi-language transfer (`TypeScript`, `Rust`, `SQL`, `PySpark`, documented separately as non-normative notes) clean because structured JSON/JSONL state and a single manifest do not hardcode Python prose formats.

### Negative / Migration costs
* Existing `loop.md` readers and tests require updating in coordinated slices (`coding-harness-5ane.11`, `coding-harness-vg9`).
* Consolidating `scripts/kit/manifest.yaml` and retiring `scripts/export/manifest.yaml` requires updating `tests/test_kit.py` (including removing `test_the_kit_list_is_not_derivable_from_the_export_list` once one manifest is decided).

## Validation

* **State-first:** Unit and concurrency tests confirm atomic locked reads/writes of loop/lane/job JSON state, deterministic Markdown rendering round-trips, and zero control-flow regex reads of rendered tables.
* **Single manifest:** `python3 scripts/kit/probe.py --strict` verifies transitive Python import closure for all carried scripts (`bead_render.py` included) and enforces a shrinking `DECKEL` ratchet reaching `0`.
* **Shared primitives:** Guard test verifies zero new duplicate `SafeLoader` subclasses or ad-hoc atomic writers outside `_yaml_strict.py`, `_fs_atomic.py`, and `_git_exec.py`.

---

## Promotion Checklist (when moving to `docs/adr/<NNNN>-state-first-and-single-manifest.md`)

1. Run Phase 1a maintainer interview recording `>= 5` answered records in `plans/changes/<name>/decisions.md`.
2. Assign the next free ADR number `<NNNN>` after open branches (`0026`/`0027`) at merge time and claim it in `spec.md` (`adr_files`).
3. Copy the finalized decision into `docs/adr/<NNNN>-state-first-and-single-manifest.md` using [`templates/adr.md`](../../templates/adr.md).
4. Open a dedicated `decide(architecture): ...` PR with label `decision` and `.github/PULL_REQUEST_TEMPLATE/decision.md` (House Rule 8).
