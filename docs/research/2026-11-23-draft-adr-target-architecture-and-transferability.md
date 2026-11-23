---
title: "Draft ADR 0026 — Three-layer microkernel, state-first persistence, OS-first security, and portable transfer architecture"
category: research
created: 2026-11-23
updated: 2026-11-23
last_reviewed: 2026-11-23
status: draft
implementation_status: none
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr-draft, architecture, target-architecture, microkernel, transferability, security, stage2]
---

# Draft ADR `0026` — Three-layer microkernel, state-first persistence, OS-first security, and portable transfer architecture

> [!NOTE]
> **Non-binding draft stored intentionally under `docs/research/`:** Under [provenance rules](../../provenance.yaml) and `check_interview_minimums.py`, placing a file directly under `docs/adr/` marks it `human-decided` and requires a Phase 1a maintainer interview plus a `decide(...)` pull request (ADR 0008). This document prepares the complete general specification for future promotion to `docs/adr/0026-microkernel-state-first-and-portable-transfer-architecture.md` after maintainer review.

* Proposed Status: draft for promotion via Phase 1a interview + `decide(architecture)` pull request (next available number after [ADR 0025](../adr/0025-targeted-check-after-repair.md); evaluates potential amendments to D-10, D-16, D-17, ADR 0013, ADR 0014, and ADR 0021 decision 3).
* Date prepared: `2026-11-23` · Measurement baseline: commit `24632499` (`2026-11-22`; live worktree count `155` measured `2026-11-23`).

---

## Context

The 100%-line audit of 232 codebase, test, tool, and configuration files (132,668 lines) documented in [the full codebase audit](./2026-11-23-full-codebase-architecture-security-audit.md) revealed that individual bugs across Monotrope trace back to ten repeating structural contradictions (`C-1` to `C-10`):

1. **Inverted trust boundaries (`C-1`, `C-2`):** Paid models expire rigidly under ADR 0022 while unknown `-free` models enter `free_stage` via suffix denylist with unread retention terms and receive real diffs even during `prepare-loop` (`model-endpoints.yaml:490-544`, `scripts/stage2_availability.py:1432,1465`). Meanwhile, ~2,500 lines of in-process guards coexist with `--no-extensions` on paid Pi review rounds (`scripts/stage2.py:3280`), unhashed `tools/pi/node_modules/` (`L4971-5009`), `STAGE2_RED_TOKEN` exposed inside untrusted test `os.environ` (`L543-603`), unscanned gitignored paths in `scripts/leakcheck.py:324` (amid 155 accumulated worktrees), wildcard permissions in `.claude/settings.local.json`, and automatic `$root/tools/bd` execution in user-global hooks.
2. **Asymmetric governance (`C-3`, `C-4`):** `scripts/check_interview_minimums.py:82` assigns `architectural: 0` minimum interview questions unless an ADR file is already edited and claimed; `ruleset` (`decisions/gates.yaml:269-277`) breaks local `make verify` for non-admin cloners; `interview-minimums` relies on full git history without declaring `needs_history: true`; `Makefile` invokes bare `python3` instead of `.venv/bin/python3`; and `docs-links` (`enforcement: report`) silently grew to 199 findings without an expiration valve.
3. **Self-defeating quality ratchets (`C-5`):** `criterion-ledger` locks 1,546 tests (51.9% of all `def test_*`) without any retirement or consolidation mechanism, `tests/test_stage2.py` (28,466 lines) triggers a hardcoded bypass of ADR 0025 targeted verification (`scripts/stage2.py:6911-6912`, driving median 7 full runs/change and 77.3 h lock wait), and `scripts/kit/probe.py:356` serially re-runs 784 passing tests.
4. **Prose-as-database coupling (`C-6`, `C-8`, `C-9`):** Mutable state stored inside editable Markdown requires 50+ fragile regexes and 18 bespoke frontmatter parsers inside an 11,487-line cyclic `stage2.py` monolith, while multi-vendor swarms run 39–90 redundant leakchecks and Opus `stage_merge` checks without an empirical defect benchmark.
5. **Non-portable kit & licensing barriers (`C-7`, `C-10`):** Conflicting `scripts/kit/manifest.yaml` and `scripts/export/manifest.yaml` leave core imports (`bead_render.py`, `stage2_research_limits.py`) orphaned, ship domain-specific Databricks agents and hardcoded `scripts/check_decision_continuity.py` (`floor: true` BLOCK in any external repo), require `DECKEL = 44` test exemptions, lock core rules strictly to Python/`pytest`/Beads/GitHub Actions/macOS `osascript`, and wrap the entire process — including L0/L1 hygiene scripts — under `PolyForm Noncommercial 1.0.0` (`COMMERCIAL.md`).

## Decision Drivers

* **Clean separation of concerns (House Rule 9):** Enforce one canonical writer, parser, git/filesystem primitive, model choke point, and kit manifest rather than parallel side routes.
* **Portability across greenfield and non-Python brownfield repositories:** Allow an existing repository (TypeScript, Go, Rust, Python, polyglot; `master`/`trunk`; existing docs SSG, CI workflow, issue tracker, or `CLAUDE.md`) to adopt Monotrope Day 1 with zero red noise and without forcing Dolt/Node/Pi upfront.
* **Defense-in-depth at real OS boundaries:** Security invariants must hold against untrusted model-authored tests and foreign CLIs regardless of harness or extension flags.
* **Fast developer feedback loop:** Preserve strict correctness while returning targeted verification under 60 seconds and full local `make verify` under 8 minutes.
* **Low cognitive load (ADHD doctrine alignment):** Collapse sprawling special cases, stacked settings, and multi-thousand-line monoliths into explicit schemas and predictable, documented workflows.
* **Measurable ROI:** Track defects found, runtime, retries, and token/request spend objectively before adding heavier orchestration stages.

## Considered Options

### Option 1 — Incremental bug-fixing on the current architecture
Patch individual bugs (`2026-11-30` valves, Pi `--no-extensions`, `free_stage` prompt, selected regex fixes) while keeping `scripts/stage2.py` monolithic, dual manifests intact, Markdown-embedded state primary, and Python/Beads hardcoded.
* *Pros:* Lowest short-term coordination cost; touches existing ADR boundaries minimally.
* *Cons:* Leaves circular imports, ADR 0025's 24-minute `test_stage2.py` penalty, 50+ Markdown state regexes, `DECKEL = 44` kit breakage, and brownfield blockers permanently intact; each repair creates another point exception.

### Option 2 — Clean-slate rewrite in a separate package
Freeze `coding-harness` and rebuild Monotrope from scratch as an external multi-language CLI package before replacing repository workflows.
* *Pros:* Zero legacy baggage during initial prototyping.
* *Cons:* Violates "one active workflow / measure in real work"; stalls urgent security and `2026-11-30` fixes; creates a long-lived two-system divergence (`bestands-drift`) exactly opposite to House Rule 9.

### Option 3 — Phased convergence to a three-layer microkernel, state-first persistence, OS-first security, and bounded lifecycle contracts *(Recommended)*
Converge incrementally in-place along five crisp architectural contracts (`Core / Ports / Optional Stage 2`), keeping every intermediate PR green and < 800 lines while systematically dissolving `C-1` through `C-10`.
* *Pros:* Solves root causes rather than symptoms; preserves daily operability; delivers immediate Stage-0 security and speed wins while unlocking clean greenfield and brownfield adoption.
* *Cons:* Requires 3–5 explicit maintainer decisions (below) covering model data-governance policy, architectural class minimums, criterion-ledger retirement, and open-core licensing scope.

## Decision

Chosen option: **Option 3 — Three-layer microkernel, state-first persistence, OS-first security, and bounded lifecycle contracts.**

If accepted via decision PR, the repository adopts the following **five normative architectural pillars**:

### Pillar 1 — Three-layer microkernel & single kit configuration (`monotrope.yaml`)

1. **Layer A (`monotrope-core`):** Pure deterministic Stage-1 engine requiring only Python 3.12+ stdlib and `PyYAML` (no Dolt, Node.js, Pi, or external LLM accounts). Owns:
   * Four shared primitives enforcing House Rule 9: `_yaml_strict` (duplicate-key safe YAML + frontmatter spans), `_fs_atomic` (symlink-safe temp-write + file/dir `fsync` atomic replace), `_git_exec` (env-sanitized `GIT_*`/`LC_ALL` git runner), and `_verdict` (uniform `0/1/2/3` exit codes across all validators).
   * Declarative gates engine (`decisions/gates.yaml`), parallel Python verify runner (`scripts/verify_runner.py` replacing Bash heredocs), content-addressed local verdict cache, single-pass `BEAD_RENDER`, `validate_change_artefacts.py`, and `monotrope init / upgrade / doctor / verify-pin / prune-worktrees`.
2. **Layer B (Pluggable Ports):** Adapt Monotrope cleanly to diverse projects via four explicit interfaces:
   * `ToolchainPort`: abstracts language setup, formatting/linting, test runner execution, and structured failure/coverage reporting (Python/`pytest`, JS/TS/`vitest`/`jest`, Go/`go test -json`, Rust/`cargo test --message-format=json`, or generic JUnit/TAP).
   * `TrackerPort`: preserves ADR 0004's normalized JSONL contract (`{"id", "status", ...}`) behind `tracker.kind: none | beads | github-issues | linear | jira`.
   * `CIPort`: generates either a standalone pipeline (`ci.mode: generate-full` for greenfield) or a non-invasive isolated workflow / reusable workflow step (`ci.mode: additive` for brownfield) across GitHub Actions (SHA-pinned, least-privilege `permissions:`), GitLab CI, or Buildkite, with clean `SKIPPED (no admin scope)` degradation for `ruleset` on non-admin machines.
   * `HarnessPort`: keeps [`AGENTS.md`](../../AGENTS.md) as single canonical doctrine while generating drift-checked minimal pointer shims (`@AGENTS.md` in `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.codex/`) and abstracting terminal launch (`macos-terminal`, `tmux`, `linux-terminal`, `foreground`) away from macOS-only `osascript`.
3. **Layer C (Optional `monotrope[stage2]`):** Decomposes `scripts/stage2.py` and `tests/test_stage2.py` into acyclic flat domain modules (`stage2_<domain>.py`, Layers 0–4) with strict module-level import rules (`AST` guard test against `ImportFrom` on monkeypatched seams and circular imports), unifying `implement`, `repair`, and `draft` into one `AttemptEngine`.
4. **Single configuration and unified manifest:** Replace hardcoded repo literals (`coding-harness-` prefix, `main`, `docs/architecture/2026-09-17-omnigent-first-target.md`, `BESTAND_OHNE_ARTEFAKT`) with repo-declared `monotrope.yaml` + universal `decisions/adoption.yaml` cutoffs. Retire `scripts/export/manifest.yaml`; maintain one manifest separating `core`, `stage2`, and `local-only` (`bestand`) assets; extract domain-specific agents and repo-local checks (`check_decision_continuity.py`) out of the portable core; and hold `scripts/kit/probe.py` at **`DECKEL = 0`** continuously against both a **greenfield Python fixture** and a **non-Python brownfield fixture**.

### Pillar 2 — State-first persistence (`JSON/JSONL -> rendered Markdown`)

1. All mutable orchestration and telemetry state — review-loop rounds/stages/verdicts (`loop.state.json`), research checkpoints, repair attempts, and OpenTelemetry GenAI event logs (`coding-harness-oebl`) — MUST be stored canonically in schema-validated atomic JSON/JSONL files under file locks (`receipt_lock` / `fcntl`).
2. Human-facing Markdown (`loop.md`, released blocks in `findings.md`, `plans/INDEX.md`, `gate-catalog.md`) is **deterministically rendered** from structured inputs (`provenance` class `machine-rendered`), never round-tripped back into state via ad-hoc line regexes.
3. Model-supplied metadata (`thread_id`, producer tags, bead IDs, finding text) MUST pass explicit schema validation and YAML/Markdown control-character escaping before entering rendered files.

### Pillar 3 — OS-first security and strict allowlist-only model admission

1. **Allowlist-only data governance:** Eliminate suffix-based auto-admission (`free_stage` `-free` rule) for external models with unread terms. Every foreign endpoint (free or paid, interactive or CI/batch) requires an explicitly verified, non-expired terms reading or a documented `public-data-only` classification with zero source-diff transmission.
2. **Tool-free and diff-free preflight:** `prepare-loop` and `prepare-explore` MUST perform only lightweight connectivity probes carrying **zero repository diffs, zero filenames, and zero local tools** prior to maintainer acknowledgement.
3. **Host OS sandboxing:** Wrap foreign review, exploration, implement, repair, and untrusted red-first test executions in host OS confinement (`sandbox-exec` Seatbelt on macOS, `bwrap`/`landlock` on Linux) explicitly denying `~/.ssh`, `~/.config/cc-routing/`, `.git/`, `.beads/`, `.claude/worktrees/`, and write access outside scoped attempt workspaces. Never leave anti-forgery tokens or distinguishable leg markers inside child `os.environ` — pass proof channels over explicit inherited descriptors (`pass_fds`) controlled out-of-process.
4. **Sealed tool integrity & hook trust:** Hash both `.venv/` and `tools/pi/node_modules/` in `tool_state()`; attach the hardened single pathlock extension to **every** Pi review and exploration call; deduplicate `secret_values()` scrubbing across all foreign runners; cache repository/history `leakcheck` per immutable tree OID while explicitly flagging gitignored paths; forbid blanket wildcard approvals in `.claude/settings.local.json` from bleeding into `night.py`; and stop user-global hooks from executing `$root/tools/bd` on untrusted clones.

### Pillar 4 — Bounded lifecycle governance (replacing append-only ratchets)

1. **`criterion-ledger` lifecycle:** Extend ADR 0013 and `scripts/check_criterion_ledger.py` to read `decisions/adoption.yaml` cleanly (`coding-harness-wpv`) and accept explicit, peer-reviewed traceability transfers (`superseded_by: tests/<path>::<fn> — <reason>` and `retired: <reason>`) plus expiring transition markers (`@pytest.mark.transition(until_bead=...)`).
2. **`architectural` oversight consistency:** Set `MINIMUMS["architectural"] = 5` in `scripts/check_interview_minimums.py` (`L82`) and require every `architectural` change to carry either a claimed ADR file under `docs/adr/` or an explicit maintainer waiver. Declare `needs_history: true` explicitly on `interview-minimums` in `decisions/gates.yaml`.
3. **Self-expiring `report` gates:** Every gate set to `enforcement: report` MUST declare either a `promote_by` date or a `sunset_by` date verified by `scripts/ramp_valves.py` (preventing unowned alert rot such as the 199-finding `docs-links` backlog).
4. **Fast, non-redundant verification & ROI telemetry:** Remove `stage2.py:6911-6912` once `test_stage2.py` splits cleanly (restoring ADR 0025 targeted verify), run `probe.py` test suites with `-n auto --dist worksteal` locally only on `Mechanismus`/manifest diffs (unconditionally in CI), maintain an empirical 10–15 historical-bug offline replay benchmark for Stage-2 models/swarms, and gate unused pinned packages (`pydantic`, `Jinja2`) explicitly via schema validation vs. removal.

### Pillar 5 — Four-tier staged adoption funnel (`L0` to `L3`)

Every repository chooses its entry tier explicitly in `monotrope.yaml`:

| Tier | Target audience | Required runtime | Enforced gates | Key adoption invariant |
| --- | --- | --- | --- | --- |
| **L0 · Discipline** | Any repo, 15-min trial | Markdown + Git only | Manual / PR checklist | Zero build or CI edits |
| **L1 · Stage-1 Core** | Greenfield Day-1 / Brownfield Wk 2 | Python (`stdlib + PyYAML`) | Deterministic L1 gates + `adoption.yaml` | `tracker: none`, `ci.mode: additive` supported; Day-1 green |
| **L2 · Polyglot Guarded** | Polyglot teams | Project toolchain + optional CLI | `ToolchainPort` + scoped `leakcheck` + optional tracker | Works across TS/Go/Rust/Python |
| **L3 · Multi-Vendor Stage 2** | Advanced agentic teams | `monotrope[stage2]` + OS sandbox + Node/Pi | Swarms, loop state, ADR 0023/0025, OTel log + budget stop | Enterprise API endpoints; ROI benchmarked |

## Consequences

### Positive
* Eliminates the structural divergence between promise and reality (`C-1` through `C-10`) in a single coherent blueprint.
* Restores daily iteration velocity by dropping full verification from ~24–26 minutes toward <8 minutes and returning routine `implement`/`repair` loops to <60-second targeted checks.
* Moves foreign-model containment from bypassable JS extensions and environment strings onto OS sandboxes and explicit allowlists.
* Makes both greenfield bootstrapping and non-Python brownfield incremental adoption friction-free and verifiable on every PR (`DECKEL = 0`).

### Negative / Migration costs
* Separating `stage2.py` + `test_stage2.py` and consolidating `criterion-ledger` entries touches ~57 plan ledgers and requires clean redirect syntax first (`DRAFT-E2.2`).
* Replacing Markdown state parsing with `loop.state.json` requires a brief dual-read transition window for any active changes at migration cut-over.
* Eliminating suffix-based `-free` auto-admission may reduce the free review-swarm seat count unless zero-retention free endpoints are explicitly reviewed and allowlisted.
* Splitting core vs. commercial licensing (if chosen by the maintainer) requires clear repo/package boundaries and contributor license alignment.

## Validation

Acceptance of this architecture once promoted and implemented is measured objectively by:

1. **Security invariants:** Static and runtime tests proving zero diff transmission in `prepare-loop`/`prepare-explore`, `tool_state()` digesting `tools/pi/node_modules/`, zero `--no-extensions` review calls, out-of-process `RED_PROBE` descriptor proofs, OS sandbox denial of `~/.ssh`, `.beads/`, and `~/.config/cc-routing/`, and zero untrusted `$root/tools/bd` execution in hooks.
2. **Acyclic modularity & targeted verify:** `tests/test_stage2_architecture.py` asserts zero cycles across `stage2_*.py`, zero `ImportFrom` monkeypatch leaks, `scripts/stage2.py < 400` lines, and `Stage-2` ADR 0025 targeted checks active without full-verify fallback (`coding-harness-vg9`).
3. **Transferability proof (`DECKEL = 0`):** `python3 scripts/kit/probe.py --strict` passes cleanly with zero exempted tests across **both** a clean greenfield Python throwaway repository and a synthetic TypeScript/Go brownfield fixture (`master`, `tracker: none`, `ci.mode: additive`, pre-existing SSG docs and `CLAUDE.md`).
4. **Performance & cost baselines:** Local `make verify` completes `< 480 s`, `leerprobe` runs `< 45 s`, SessionStart `close_merged_beads` runs `< 100 ms`, `stage_merge` spends zero LLM tokens on deterministic unions, and Stage-2 swarms demonstrate positive net defect yield on the 10–15 historical-bug replay suite.

---

## Open Maintainer Decisions (required before Phase 1a / `decide` PR promotion)

Each open policy choice is structured in the ADR 0018 decision-context format:

### `Q-ARCH-1` · Open-Core vs. full PolyForm Noncommercial licensing boundary (`C-10`)
* **Topic:** Licensing model for `Layer A` (`monotrope-core`) vs. `Layer C` (`monotrope[stage2]`).
* **Intention:** Resolve the conflict between external brownfield/enterprise adoption ambitions and noncommercial source protection ([COMMERCIAL.md](../../COMMERCIAL.md)).
* **Today:** The entire repository — including plain Markdown prompts, templates, and L1 deterministic validators — sits under `PolyForm Noncommercial 1.0.0`.
* **Repository change:** Separate package/license boundary (Option A) vs. retain uniform PolyForm across all files (Option B) vs. Apache-2.0 core / PolyForm commercial extension.
* **Architecture change:** Determines whether external brownfield companies can adopt Stage 1 (`monotrope-core`) legally without bespoke bilateral contracts (`D-17` amendment if re-split).
* **Question:** Should `Layer A` (`monotrope-core`: workflow doctrine, templates, L0/L1 deterministic gates, CLI) use an OSI open-source license (Apache-2.0) while keeping `Layer C` multi-vendor Stage-2 orchestration / enterprise runners under PolyForm/Commercial, or should the entire repository stay PolyForm Noncommercial 1.0.0? *(Recommendation: Open-Core Apache-2.0 for `Layer A` + PolyForm/Commercial for `Layer C`; enables zero-friction L0/L1 adoption everywhere while protecting proprietary orchestration.)*

### `Q-ARCH-2` · Retire suffix-based unread `-free` auto-admission (`C-1`)
* **Topic:** Admission policy for `free_stage` and `research_swarm.online_free` in [model-endpoints.yaml](../../model-endpoints.yaml).
* **Intention:** Close `C-1` where unknown `-free` models with unread retention terms receive up to 2,000 lines of real code diffs (`2026-11-06` leak precedent).
* **Today:** ADR 0021 Decision 3 auto-admits `-free` catalog matches via suffix denylist without a privacy terms reading; `prepare-loop` already sends the diff before approval.
* **Repository change:** Replace `free_stage` suffix matching with an explicit `allowlist` requiring a verified zero-training/retention terms record (or restrict unread free models strictly to synthetic/zero-diff tasks), amending ADR 0021 Decision 3.
* **Architecture change:** Aligns `free_stage` with ADR 0022's strict allowlist invariant (`not listed is BLOCK`).
* **Question:** Do you approve amending ADR 0021 Decision 3 to remove suffix-based unread `-free` auto-admission and require explicit dated privacy readings for every Stage-2 model, including free models? *(Recommendation: Yes — security and data governance must not invert between free and paid tiers.)*

### `Q-ARCH-3` · Close the `architectural` interview floor loophole (`C-3`)
* **Topic:** Minimum interview requirements for `class: architectural` in [check_interview_minimums.py](../../scripts/check_interview_minimums.py).
* **Intention:** Eliminate the `C-3` paradox where the riskiest change class allows `0` interview answers when omitting an ADR edit.
* **Today:** `MINIMUMS = {"feature": 3, "spike": 3, "bounded": 1, "architectural": 0}`; `check_adr_answers.py` only inspects `feature`.
* **Repository change:** Set `MINIMUMS["architectural"] = 5` and fail any `architectural` change that neither edits/adds a claimed file under `docs/adr/` nor carries an approved maintainer exemption (`decisions/adoption.yaml` cutoff preserves archived stock).
* **Architecture change:** Aligns enforcement with [`AGENTS.md`](../../AGENTS.md) and [`WORKFLOW.md`](../WORKFLOW.md) (`architectural` implies an ADR).
* **Question:** Should `check_interview_minimums.py` enforce `architectural >= 5` unconditionally and require an ADR (or explicit maintainer waiver) for all prospective `architectural` changes? *(Recommendation: Yes — highest architectural blast radius should never carry the lowest governance floor.)*

### `Q-ARCH-4` · Support `tracker.kind: none` as default L0/L1 brownfield onboarding mode (`T-6`)
* **Topic:** Mandatory Dolt/Beads requirement in Stage-1 transfer kits.
* **Intention:** Remove the #1 operational barrier blocking 30-minute L1 brownfield trials.
* **Today:** Four `floor: true` gates (`plans-registry`, `bead-export`, `dangling-beads`, `plans-registry-strict`) require a hydrated Dolt tracker (`tools/bd`), forcing non-Python teams to install Go/Dolt binaries before running a single check.
* **Repository change:** Introduce `tracker.kind: none | beads | github-issues | linear | jira` in `monotrope.yaml`; when `none`, tracker-dependent gates cleanly check git/branch metadata or report skipped-by-config (`0` exit on L1 non-tracker repos).
* **Architecture change:** Makes Beads an explicit high-value L2/L3 opt-in rather than a monolithic prerequisite (`TrackerPort` behind ADR 0004 JSONL).
* **Question:** May exported brownfield L1 configurations default to `tracker.kind: none` (while keeping `beads` `floor: true` in Monotrope itself and optional at L2/L3)? *(Recommendation: Yes — decoupling governance discipline from Dolt installation dramatically increases real adoption.)*

### `Q-ARCH-5` · Consolidation & retirement syntax in `criterion-ledger` (`C-5`, `R-1`)
* **Topic:** Evolution of `check_criterion_ledger.py` (ADR 0013) to allow safe test deduplication and Stage-2 modularization.
* **Intention:** Unblock removal of 600–910 duplicate/micro tests (`test_stage2.py` split, `R-1..R-6`) without losing requirement traceability.
* **Today:** Every `plan.md` test reference (1,546 functions, mostly archived) stays frozen permanently with zero syntax for consolidation or transition-test expiry.
* **Repository change:** Support structured `superseded_by: <test_id>` / `retired: <bead + reason>` mappings (in `decisions/ledger-redirects.yaml` or ledger entries) and `@pytest.mark.transition(until_bead=...)`, audited during Phase 6 reviews and validated via `BEAD_RENDER`.
* **Architecture change:** Converts an append-only lock into a traceable evolution contract aligned with ADR 0013's intent.
* **Question:** Should `check_criterion_ledger.py` be extended with machine-verified `superseded_by` / `retired` redirects and bead-bound `@pytest.mark.transition` expiry? *(Recommendation: Yes — prerequisite for shrinking `make verify` from ~25 min below 8 min.)*

---

## Promotion Checklist (when promoting to `docs/adr/0026-...`)

1. Run Phase 1a maintainer interview recording answers to `Q-ARCH-1` .. `Q-ARCH-5` in `plans/changes/<name>/decisions.md`.
2. Verify whether continuity updates (`docs/architecture/` target note and `scripts/check_decision_continuity.py` `AMENDMENT_ADRS`) are owed for amended decisions (`D-10`, `D-16`, `D-17`).
3. Create the `spec.md` claiming `adr_files: [docs/adr/0026-microkernel-state-first-and-portable-transfer-architecture.md]`.
4. Move the accepted decision prose into `docs/adr/0026-microkernel-state-first-and-portable-transfer-architecture.md` using [the ADR template](../../templates/adr.md).
5. Open a dedicated `decide(architecture): ...` PR with label `decision` and `.github/PULL_REQUEST_TEMPLATE/decision.md` (House Rule 8); never self-approve or merge until the maintainer confirms.

---

## Companion drafts in this PR

* Full audit evidence and Section 10 synthesis: [2026-11-23-full-codebase-architecture-security-audit.md](./2026-11-23-full-codebase-architecture-security-audit.md)
* Prioritized Draft Beads Epics & Tasks derived from Sections 1–10: [2026-11-23-draft-beads-backlog-from-audit.md](./2026-11-23-draft-beads-backlog-from-audit.md)
