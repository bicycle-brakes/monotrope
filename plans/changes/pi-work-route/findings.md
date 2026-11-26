---
title: "Findings — pi-work-route"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-363r.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — pi-work-route

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5969 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-work-verbs-through-pi.md` +49 -0
> - `plans/changes/pi-work-route/design.md` +62 -0
> - `plans/changes/pi-work-route/plan.md` +76 -0
> - `plans/changes/pi-work-route/spec.md` +87 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 1
> archive/2026-11-06-interview-fenced-examples: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-kimi-admission: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ledger-instance-layout: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ledger-marker: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-loop-until-clean: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-malformed-answer-retry: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-merge-queue: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-mutation-evidence-module: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-catalog-move: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-catalog-redirect: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-pin: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-plan-held-paths: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-provenance-location: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ratchet-mutation-evidence: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-red-first-install: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-red-first-pytest-failed: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-registry-block-last: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-fixed-line-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-fixed-lines: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-restore-status: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-research-swarm: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-restore-symlink-parent: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-loop-deep-b: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-release-lock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-verdict-validated: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-run-report: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-runner-time-line: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-runner-time-line-exits: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-sol-effort: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-stage2-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-stage2-repair: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-swarm-time-limits: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-terms-expiry: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-terms-test-fixtures: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-test-key-runtime: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-test-strength-rows: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-tolerate-derived-leftovers: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-venv-pycache: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-absolute-python: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-duration: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-machine-lock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-stages-new-files: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-worker-cap: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-workflow-promises: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-address-drift-warning: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-adr-0016-docs-check: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-archive-closed-changes: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-decision-statement-skeleton: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-docs-job-report-header: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-explore-provenance: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-go-wire-apis: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-guard-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-midnight-stamp-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-heartbeat: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-machine-facts: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-stall-guard: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-no-work-done: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-no-work-ledger-marker: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-omnigent-test-not-blocking: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-origin-cell: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-origin-check-across-blocks: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-outcome-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-pi-no-compaction: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-raising-fault-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-red-first-own-refs: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-redraft-after-scope: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-repair-targeted-check: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-research-free-paid: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-runner-clock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-status-fields-restore: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-swarm-citation-feedback: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-swarm-report-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-targeted-check-more-verbs: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-time-records-data: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-triage-verb: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-cheap-first: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-step-limit: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-tmp-cleanup: exempt - legacy, no research-swarm/v2 evidence
> research-handoff: pi-work-route: the spec exists but no complete v2 run exists
> research-handoff: 1 finding(s)
> ```

Stage-2 call, 2026-11-25: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1208 files, 5970 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 1
> archive/2026-11-06-interview-fenced-examples: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-kimi-admission: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ledger-instance-layout: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ledger-marker: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-loop-until-clean: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-malformed-answer-retry: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-merge-queue: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-mutation-evidence-module: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-catalog-move: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-catalog-redirect: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-pi-pin: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-plan-held-paths: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-provenance-location: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-ratchet-mutation-evidence: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-red-first-install: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-red-first-pytest-failed: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-registry-block-last: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-fixed-line-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-fixed-lines: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-repair-restore-status: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-research-swarm: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-restore-symlink-parent: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-loop-deep-b: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-release-lock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-review-verdict-validated: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-run-report: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-runner-time-line: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-runner-time-line-exits: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-sol-effort: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-stage2-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-stage2-repair: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-swarm-time-limits: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-terms-expiry: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-terms-test-fixtures: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-test-key-runtime: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-test-strength-rows: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-tolerate-derived-leftovers: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-venv-pycache: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-absolute-python: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-duration: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-machine-lock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-stages-new-files: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-verify-worker-cap: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-06-workflow-promises: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-address-drift-warning: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-adr-0016-docs-check: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-archive-closed-changes: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-decision-statement-skeleton: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-docs-job-report-header: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-explore-provenance: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-go-wire-apis: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-guard-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-midnight-stamp-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-heartbeat: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-machine-facts: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-night-stall-guard: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-no-work-done: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-no-work-ledger-marker: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-omnigent-test-not-blocking: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-origin-cell: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-origin-check-across-blocks: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-outcome-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-pi-no-compaction: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-raising-fault-test: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-red-first-own-refs: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-redraft-after-scope: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-repair-targeted-check: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-research-free-paid: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-runner-clock: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-status-fields-restore: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-swarm-citation-feedback: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-swarm-report-format: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-targeted-check-more-verbs: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-time-records-data: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-triage-verb: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-cheap-first: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-step-limit: exempt - legacy, no research-swarm/v2 evidence
> archive/2026-11-16-verify-tmp-cleanup: exempt - legacy, no research-swarm/v2 evidence
> research-handoff: pi-work-route: the spec exists but no complete v2 run exists
> research-handoff: 1 finding(s)
> ```

Stage-2 call, 2026-11-25: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1208 files, 5971 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/pi-work-route/draft-attempt-3-20261125T202812090185Z (68820899797d); `git diff 1627adb3eaec refs/stage2/attempts/pi-work-route/draft-attempt-3-20261125T202812090185Z` shows it.
>
> The runner put back:
> - `docs/adr/0026-work-verbs-through-pi.md`
> - `plans/INDEX.md`
> - `plans/changes/pi-work-route/design.md`
> - `plans/changes/pi-work-route/plan.md`
> - `plans/changes/pi-work-route/spec.md`

Stage-2 call, 2026-11-26: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1279 files, 6021 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - plans/changes/pi-work-route/spec.md is missing after the draft.
> - plans/changes/pi-work-route/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-26: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1279 files, 6021 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - plans/changes/pi-work-route/spec.md is missing after the draft.
> - plans/changes/pi-work-route/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-26: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1279 files, 6021 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/pi-work-route/draft-attempt-3-20261126T183037710036Z (0ac6cc205b65); `git diff ba17925c124d refs/stage2/attempts/pi-work-route/draft-attempt-3-20261126T183037710036Z` shows it.

Stage-2 call, 2026-11-26: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1279 files, 6025 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - plans/changes/pi-work-route/spec.md is missing after the draft.
> - plans/changes/pi-work-route/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-26: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1279 files, 6025 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0027-work-verbs-through-pi.md` +46 -0
> - `plans/changes/pi-work-route/design.md` +62 -0
> - `plans/changes/pi-work-route/plan.md` +69 -0
> - `plans/changes/pi-work-route/spec.md` +126 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 1
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-16 (decision): Is a CVE record with an empty public rendering on NVD (client-rendered shell only) sufficient evidence of severity for an internal risk decision, or must a second primary rendering be retrieved first? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:deepseek-v4.1-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:deepseek-v4.1-flash/C4] - link it in a maintainer-answered Q-record' [… 16 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-17 (decision): How should this topic be re-attempted given that all search calls timed out this session — via retry with different queries, or via direct fetches of known vendor security pages? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:glm-5.3-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:glm-5.3-flash/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:glm-5.3-flash/C3] - link it in [… 48 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-18 (decision): What level of uncertainty is acceptable when deciding fallback ordering and file-write boundaries while primary incident evidence remains unretrieved? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:hy4-flash-free/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:hy4-flash-free/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-19 (decision): Given that no advisory text could be read this session, how much unverified public risk should be assumed when designing fallback order and write confinement? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:mimo-v2.6-flash/C4, 43fdfb08b4ae42db3dc9b8f89069d7d0/11/opencode-go:mimo-v2.6-flash/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-20 (decision): The Q-3 answer treats GLM 5.3 Flash on Go as open-ended, but its Go terms record valid_until 2026-12-14. Should the automatic DeepSeek-to-GLM fallback be checked against that date too, or is the decision meant to rest on GLM without any end date? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/2/claude-code-plan:claude-haiku-5-5/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-21 (decision): Which read/edit/write tool list should the Pi write route expose to the model: the names of WORK_WRITE_TOOLS (Read, Grep, Glob, Edit, Write), the lowercase names of PI_TOOLS, or a new declaration? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/2/claude-code-plan:claude-haiku-5-5/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/2/claude-code-plan:claude-haiku-5-5/C7] - link it in a maintainer-answered Q-record's  [… 14 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-22 (decision): The implement GLM_KEY refusal is pinned by a test. Once the Go route is first, should a missing OPENCODE_GO_KEY refuse the verb, or fall through to the next route? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/2/claude-code-plan:claude-haiku-5-5/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/2/claude-code-plan:claude-haiku-5-5/C4] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-23 (decision): Should a write-capable Pi work attempt reuse the attempt loop's existing endpoint branch (a third transport beside `run_codex` and `run_work_model`) or reuse `run_reviewer`'s Pi launch shape, given that `run_attempts` today picks the transport purely by `endpoint == CODEX` and `repair_prompt` picks its answer format the same way? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/2/opencode-go:deepseek-v [… 216 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-24 (decision): Where should the DeepSeek-default / GLM-fallback model choice be declared, and which reader enforces the automatic switch when `valid_until` lapses — a new declared parameter in `model-endpoints.yaml` in the style of `spec_review`, or a constant in `scripts/stage2.py` — so that `declaration_problem`/`preflight` remain the one refusal point? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/2/opencode-go [… 227 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-25 (decision): House rule 9 requires model choice to be a declared parameter of the one route, but the CLI currently allows --model only for the session verb and the work-verb route lists are hard-coded tuples; what exact parameter surface (flag, model-endpoints.yaml default block like spec_review's fallback_endpoint/fallback_model, or both) will carry the Q-3 DeepSeek-default-with-GLM-fallback for work verbs? [… 265 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-26 (decision): Which number does the new ADR take: 0026, the next free number in this worktree, or a later number because 0026 and 0027 are drafted on other branches? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/claude-code-plan:claude-haiku-5-5/C2] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-27 (decision): Q-3 states that GLM 5.3 Flash has no end date, but its recorded valid_until is 2026-12-14. Which dated reading should govern the automatic fallback from DeepSeek to GLM: DeepSeek's valid_until alone, or GLM's own dated reading as well? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/claude-code-plan:claude-haiku-5-5/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-28 (decision): Should the new ADR also supersede the Codex-then-Sonnet repair order in ADR 0017? And since ADR 0015 is already superseded by ADR 0017, should the pointer for ADR 0015 point to ADR 0017 instead? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/claude-code-plan:claude-haiku-5-5/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-29 (decision): Does the new ADR supersede ADR 0011 Decision point 2 and ADR 0007's explore and implement on GLM 5.3 Flash through Claude Code, as Q-1 part 3 implies, even though Q-4 names only the affected parts of ADRs 0007, 0011 and 0015 without listing these? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/claude-code-plan:claude-haiku-5-5/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-30 (decision): Does the new Python write-tool module replace the JavaScript session policy (scripts/stage2_session_policy.mjs) for Pi sessions, or does it sit beside it for the work route only? ADR 0012 currently describes only the JavaScript mechanism. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/claude-code-plan:claude-haiku-5-5/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-31 (decision): Which number does the new work-verbs ADR take, given that 0026 is free in this tree but recorded as drafted on other lanes (and another change calls 0028 the next unused on 2026-11-19)? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C3] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-32 (decision): Does the supersession set become ADR 0007, 0011 and 0017 — and possibly 0020 for the explore move — instead of 0007, 0011 and the already-superseded 0015? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C4, 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-33 (decision): Is `architectural` the right class for a route and fallback change that keeps the existing verbs and their prompts, when earlier routing ADRs travelled in `feature` changes? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-34 (decision): How does phase 2 proceed when `spec.md` makes gate `research-handoff` red because no complete research-swarm/v2 run exists, while the maintainer has already agreed to continue on the partial research? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C2] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-35 (decision): Is `model-endpoints.yaml` `human-decided` as ADR 0007 decision 6 says, and should the provenance map gain that entry so the change's edits to it are held as a decision pull request? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:deepseek-v4.1-flash/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-36 (decision): Should the new ADR supersede the affected parts of ADR 0017 — the accepted record that fixes the live repair chain Q-2 reorders — in addition to or instead of ADR 0015, which is already superseded by 0017 and holds no current routing force? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:glm-5.3-flash/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:glm-5.3-flash/C6] - link it in a mai [… 42 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-37 (decision): Does the phase-1 explore re-routing of Q-1 part 3 (GLM 5.3 Flash explore moving onto Pi) require a pointer or amendment to ADR 0020, whose Decision fixes the bounded/spike explore route, given that Q-4's pointer list names only ADRs 0007, 0011 and 0015? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:glm-5.3-flash/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/3/opencode-go:glm-5.3-flash/C6] - lin [… 55 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-38 (decision): Should the new ADR also supersede or amend the affected parts of ADR 0017 (repair order), ADR 0020 (explore through GLM 5.3 Flash for bounded and spike changes) and ADR 0016 (GLM draft fallback through Claude Code), which Q-4 does not name? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/4/claude-code-plan:claude-haiku-5-5/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/4/claude-code-plan:claude-haiku-5-5/C6] -  [… 58 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-39 (decision): The interview answer Q-4 names a new ADR that supersedes the affected parts of ADR 0007, 0011 and 0015. ADR 0017 decision 6 states that initial implementation, Explore and the draft's GLM fallback retain their models, and ADR 0011 decision 2 states explore and implement stay on GLM 5.3 Flash. Which records must carry the pointer for the change to be consistent, and does ADR 0015 — already supers [… 168 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-40 (decision): House rule 11 says state a program reads back is a schema-validated JSON file written by code, never Markdown parsed back; the policy now in force is the §4 routing table, which a suite test parses. Should the work-verb route stay in that table, or move into declared machine-read state, and which gate would then hold it? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/4/opencode-go:deepseek-v4.1-flash [… 136 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-41 (decision): Which confinement is the documented boundary for a write-capable Pi work run — the existing JavaScript session policy extension of ADR 0012 decision 3, reused, or a separate tool module — and does ADR 0011 decision 4, which accepted unconfined reads for reviewers only, need restating for a run that writes? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/4/opencode-go:deepseek-v4.1-flash/C6] - link it  [… 50 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-42 (decision): Responsibility: `docs/WORKFLOW.md` travels as kit mechanism while `scripts/` and `model-endpoints.yaml` are `bestand` and stay in this repository, and the architecture target puts model names into a per-instance routing file instead of the doctrine. Does widening the runner's work routes change the kit/instance split, or only deepen a script the kit does not carry? [claims: 43fdfb08b4ae42db3dc9b [… 110 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-43 (decision): The `opencode-go` remark is a declaration maintained by the orchestrating session under ADR 0024 and held by a test with required sentences. Widening the entry's callers edits that declaration; it is not stated which part of the widening's text belongs in the remark and which in the new ADR. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/4/opencode-go:deepseek-v4.1-flash/C4, 43fdfb08b4ae42db3dc9b8f89 [… 106 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-44 (decision): Does the GLM-off-Claude-Code part (Q-1 item 3) retire the glm-coding-plan endpoint for explore/implement entirely or leave it as an inner fallback, which determines whether the Z.ai terms-expiry tests (test_stage2_zai_terms) keep their current meaning? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/4/opencode-go:glm-5.3-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/4/opencode-go:glm-5.3-flash/C4] - link [… 54 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-45 (decision): Does a Pi work-verb run on OpenCode Go (implement, repair, and explore on the new route) count as a 'Go launch' under go-access-point, so that its address checks bind it? Its Terms list names four kinds and does not name this one, while decision Q-1 says 'every Go path'. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C1] - link it in a maintainer-answered Q-record' [… 16 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-46 (decision): Is an automatic switch from DeepSeek V4.1 Flash to GLM 5.3 Flash on lapse acceptable under terms-expiry, given that its criterion 5 refuses an expired dispatch and its Non-goals exclude provider substitution and new model ids? The alternative is that a lapse refuses the work route. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C4, 43fdfb08b4ae42db3dc9b8f89069d7d0/ [… 100 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-47 (decision): Does stage2-session criterion 11's rule of exactly one runner-supplied extension bind the work route's own read/edit/write tool module when Pi loads it, or only the interactive session verb's dispatch? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-48 (decision): Does a Pi run that implements or repairs count as a "Go launch" under the go-access-point address record and its admission policy, and must the new ADR of Q-4 therefore also carry a pointer to the record that owns which launches may reach OpenCode Go? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C1] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-49 (decision): Which Pi confinement mechanism is canonical for the lane-worktree write boundary once both exist — stage2-session's runner-supplied policy extension (shell allowed, built-in file tools blocked by path) or Q-5's own plain-Python read/edit/write tools with no shell — and which one retires or points to the other? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C5, 43fdfb [… 125 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-50 (decision): Q-3 relies on GLM 5.3 Flash having "no end date" for a gapless automatic fallback, while the terms-expiry rule gives every record whose provider names no end date the reading date plus 30 days; which premise governs the automatic fallback, and what happens when the fallback model's own declared date passes? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C2, 43fdfb08b [… 122 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-51 (decision): Does the accepted, done go-access-point boundary cover the new work-verb Pi launches on opencode-go without extending its 'Go launch' enumeration and acceptance criteria, or does pi-work-route owe an update to that neighbour spec (or ADR 0024) so the address-admission checks name the work-verb launch family? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:glm-5.3-flash/C1, 43fdfb08b4ae42 [… 111 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-52 (decision): How exactly does Q-3's automatic DeepSeek-to-GLM fallback compose with terms-expiry's rules: is the fallback a routing-level declared parameter that never renews or extends the DeepSeek valid_until, and who records the fallback decision given that renewal itself still requires a maintainer decision pull request? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:glm-5.3-flash/C3, 43fdfb08b4 [… 115 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-53 (decision): What is the replacement relationship between pi-work-route's plain-Python path-checked write tools (Q-5, no shell) and stage2-session's still-partial JavaScript policy extension: which one governs a work-verb Pi run, do the neighbour's extra protections (the extension's own file, .stage2-sessions/, .pi/) carry into the Python tools, and is 'no shell' now the floor that supersedes ask-before-dang [… 146 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-54 (decision): Does reordering the implement and repair routes (Go first, then Codex, then Claude) preserve repair-targeted-check's prerequisites — targeted checks per repair attempt, full verification before phase 6, and full verify whenever a repair touches prompts/ — and does the route change itself, by touching prompts or scripts, trigger those heavier checks during its own implementation? [claims: 43fdfb0 [… 118 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-55 (decision): The packet records DeepSeek's terms through 2026-11-30 and no renewal. Should the maintainer obtain a fresh terms reading before that date, and how should the 'renewed monthly' rule be recorded as dated readings? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/claude-code-plan:claude-haiku-5-5/C1] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-56 (decision): Does Q-1 part 3's plain 'GLM 5.3' mean the Flash route (glm-5.3-flash) or the non-Flash GLM route that commit a0154976 moved to glm-5.4? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/claude-code-plan:claude-haiku-5-5/C2] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-57 (decision): Does the Q-5 write boundary retire the JavaScript policy extension built in d225f50d, or do both stand? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/claude-code-plan:claude-haiku-5-5/C4] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-58 (decision): Should the default Go model named in Q-4 be recorded in the new ADR, as Q-4 asks, or in model-endpoints.yaml, as the 42940af6 rule assigns which models run on an endpoint? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/claude-code-plan:claude-haiku-5-5/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-59 (decision): Should the planned new ADR supersede ADR 0017 as well — the ADR that superseded 0015 and states the current repair chain — instead of only 0007, 0011 and 0015? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/opencode-go:deepseek-v4.1-flash/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-60 (decision): Is the 'Only through Claude Code … not covered by the subscription' sentence still the maintainer's contractual reading, or is it the outdated claim the 2026-10-11 research says it is? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/opencode-go:deepseek-v4.1-flash/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-61 (decision): Should the new work-verb ADR also carry a pointer into ADR 0017, whose Decision fixes the repair order Q-2 changes, or is 0017 intended to remain untouched alongside the new route declaration? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/6/opencode-go:glm-5.3-flash/C1] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-62 (decision): Should the Python path checks cover every case the JavaScript policy covers (outside the worktree, symlink out, not-yet-existing path), or a narrower set? This sets how far the new tests must go beyond tests/test_stage2_session_policy.py::test_a_path_outside_the_worktree_is_blocked. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/claude-code-plan:claude-haiku-5-5/C2] - link it in a maintainer-answer [… 28 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-63 (decision): When the implement/repair/explore route lists change, are the existing order tests (implement Flash → Flash-repair → Sonnet, repair Codex → Codex → Sonnet) rewritten to the new order, or kept as the record of the old route? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:deepseek-v4.1-flash/C1] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-64 (decision): Does the write boundary need a real pinned-Pi contract for a writable work call, in the shape of `test_real_reviewer_tool_contract`, or are stand-in tests plus the JavaScript session policy accepted as the proof? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:deepseek-v4.1-flash/C5, 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:deepseek-v4.1-flash/C6] - link it in a maintainer-answered [… 26 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-65 (decision): Q-5 requires macOS, Linux and Windows, but the mapped gate set declares one interpreter leg and no per-OS leg; does the change accept that no gate measures the other two platforms, or is a platform gate part of it? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:deepseek-v4.1-flash/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-66 (decision): What becomes of the checks that bind explore/implement to Z.ai (expired-terms refusal, missing `GLM_KEY` refusal, explorer environment) once the Go route runs first? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:deepseek-v4.1-flash/C2] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-67 (decision): When a work verb's current credential is missing or its terms have lapsed, should the verb fall back to the Pi-on-Go route (and to Codex, then Sonnet) instead of refusing as today's tests pin — and which of the pinned refusal tests (C4) survive as the refusal of last resort when every route is unavailable? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/7/opencode-go:glm-5.3-flash/C2, 43fdfb08b4ae42db [… 109 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-68 (decision): When deepseek-v4.1-flash terms lapse after valid_until 2026-11-30 (a UTC-dated expiry), and a GLM key or OpenCode Go key is missing, which verb refuses and with what message? This edge case is not stated in Q-3 and the refusal path is not verified in the code I read. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/claude-code-plan:claude-haiku-5-5/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/8/claude-code-p [… 85 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-69 (decision): House rule 4 states the two-writing-session limit without enforcement. If a write-capable Pi run starts in a lane worktree while another writing session runs, which session writes the tracker, and does the write route need a check before its first write? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/claude-code-plan:claude-haiku-5-5/C6] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-70 (decision): The routing decisions were answered on partial research (topics 1, 2 and 4 timed out). Is the missing coverage of those topics acceptable for the ADR, or must the decision name which claims rest on the incomplete topics? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/claude-code-plan:claude-haiku-5-5/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-71 (decision): When a stop has to be chosen: should an expired or unread `modelle_terms` record for the default Go model refuse the whole implement/repair run (today's `preflight` behaviour) or skip that model and continue with the declared fallback? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C4] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-72 (decision): Which confinement applies to a write-capable Pi work run: the existing session policy (path-checked file tools plus name-allowed shell with dangerous-pattern asks), the stricter repository-seat lock shape (only named tools exist), or only the new Python tools with no shell at all? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/8/o [… 95 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-73 (decision): Which of the POSIX-shaped pieces (the `/bin/sh` wrapper, the process-group kill in `launch`, the macOS-only session dispatch) must change for the Windows half of the write-boundary requirement, and which stay out of scope? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C6] - link it in a maintaine [… 36 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-74 (decision): Should the runner's pre-call tool digest cover `scripts/`, `tools/pi/` or the policy/tool extension for a work route that may write the tree, or stay `.venv/`-only? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-75 (decision): What time limit, if any, applies to a Pi work call, given that implement and repair calls today run untimed while reviewer and probe calls carry a limit and a killed process group? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:deepseek-v4.1-flash/C3] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-76 (decision): When the default Go route is refused mid-lane because DeepSeek's valid_until has lapsed, should that Refused be treated as an attempt failure that consumes one route slot and hands diagnostics onward (Q-2 order), or should the model-fallback (DeepSeek→GLM) happen inside the Go route without touching the route list? The decisions record both mechanisms (Q-2 order, Q-3 automatic fallback) without  [… 235 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-77 (decision): The implement/repair fallback order contains a leak-check BLOCK rule ('stops without a fallback', ADR 0017); does that property extend unchanged to a leak-check BLOCK on the new Go-first route, or does a Go-route leak failure hand off to Codex? The decisions do not state it. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/8/opencode-go:glm-5.3-flash/C2] - link it in a maintainer-answered Q-record's re [… 12 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-78 (decision): Should confinement of file writes be enforced by the coding harness (path-scoped writes) or delegated to the model service, and which authority should the maintainer treat as normative? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:deepseek-v4.1-flash/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:deepseek-v4.1-flash/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-79 (decision): Do practitioners recommend routing only read-only or exploratory coding work to cheaper models while keeping writes on a stronger model, and under what conditions? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:glm-5.3-flash/C7] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-80 (decision): Should a cheaper model service be adopted when it requires custom configuration even though Pi already includes an equivalent provider or endpoint? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:hy4-flash-free/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:hy4-flash-free/C5] - link it in a maintainer-answered Q-record's research_items
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-81 (decision): What fallback order should routing of coding work through Pi onto a cheaper model service use — cheapest-first, capability-first, or failure-triggered — given that no retrieved page states such an order? [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:mimo-v2.6-flash/C1, 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:mimo-v2.6-flash/C4, 43fdfb08b4ae42db3dc9b8f89069d7d0/9/opencode-go:mimo [… 76 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-82 (disagreement): The haiku seat found no Python equivalent of the JavaScript path policy in what it read. The glm and deepseek seats identify restoration_parent_problem as a Python check that resolves symlinked ancestors and refuses escapes. It guards the runner's own restoration writes, not a model tool module, so whether it counts as an equivalent is open. No seat claims that a Python tool module exists. [ [… 277 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-83 (disagreement): The deepseek seat calls run_reviewer the only existing Pi launch. The glm seat cites stage2_session.py::cli_argv, a writable interactive Pi launch, and a research-seat launch through Run.pi_command, which also appears in a topic-7 test excerpt. The claim holds only if read as limited to stage2.py; that scope is not stated. Its other parts (read-only, store-dependent, models_store never set b [… 307 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-84 (disagreement): The glm seat says a Pi route joins run_attempts only as a third branch at the one completion boundary, with everything else endpoint-agnostic. The deepseek seat reports that the HEAD-move check is also guarded by endpoint == CODEX, and the fully shown repair_prompt excerpt selects the answer format by endpoint. The glm seat's own topic-4 counter-evidence lists further endpoint == CODEX sites [… 395 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-85 (disagreement): Both seats agree on the code: any non-Codex repair gets the file-tools format and delegated must-runs. They diverge on design. The deepseek seat treats that contract as fitting a no-shell Pi repair unchanged; the glm seat says a third declared case is needed instead of silently reusing either format. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/1/opencode-go:deepseek-v4.1-flash/C5, 43fdfb08b4ae [… 113 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-86 (disagreement): The haiku seat's C6 calls the spec_review fallback a non-review caller and the one declared parameter that routes a Go model outside the review loop. But the spec review is itself a review phase (2a), and the opencode-go remark, cited by haiku's own C4 and by deepseek's C4, names the research swarm and the session verb as further Go callers outside the loop. Settled against C6. [claims: 43fd [… 273 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-87 (disagreement): The glm seat concludes from the contiguous 0001–0025 listing that Q-4's placeholder resolves to ADR 0026. The deepseek and haiku seats agree that 0026 is the next free number in this worktree, but cite another change's 2026-11-19 notes (0026 and 0027 drafted on other branches, 0028 next unused) and a handover recording an untracked 0026 draft. Nobody checked those branches, so whether 0026 i [… 318 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-88 (disagreement): The glm seat says the new tool module must be registered in the kit manifest or the kit test goes red. The deepseek seat reports a catch-all scripts/ rule with role bestand, which would classify a module under scripts/ without a new rule, though the module would then not travel to instances. The outcome depends on whether the module lives under scripts/ or tools/pi/. [claims: 43fdfb08b4ae42d [… 181 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-89 (disagreement): On finder-partial-report, the deepseek and glm seats call it related and the haiku seat calls it unrelated. All three agree it covers only finder locator validation; deepseek adds that it does not cover the timed-out topics. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C7, 43fdfb08b4ae42db [… 109 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-90 (disagreement): On terms-expiry, the deepseek and haiku seats label the relation a contradiction: the reading-date-plus-30-days rule undercuts Q-3's 'no end date' premise, and haiku adds the provider-substitution non-goal and the refusal at dispatch. The glm seat labels it related and, in its counter-evidence, treats a routing-level fallback that never extends a reading as compatible. The cited texts do not [… 292 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-91 (disagreement): On stage2-session, the deepseek seat labels the relation a contradiction; the glm and haiku seats call it related. The facts agree: a JavaScript extension that permits a shell with asks, against Q-5's Python tools with no shell. Only the classification differs. [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C7, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:dee [… 217 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-92 (neighbour contradicts): contradicts for plans/changes/archive/2026-11-06-terms-expiry/spec.md: three counting related or contradicts relations [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C3, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C4, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C5, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/ope [… 218 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-93 (neighbour split): split for plans/changes/finder-partial-report/spec.md: 3 counting relations (2 related or contradicts, 1 unrelated) [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/claude-code-plan:claude-haiku-5-5/C2, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C7, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:glm-5.3-flash/C7] - link it in a maintainer-answered Q-record's research_it [… 57 characters left out …]
> research-handoff: pi-work-route: open research item 43fdfb08b4ae42db3dc9b8f89069d7d0/H-94 (neighbour contradicts): contradicts for plans/changes/stage2-session/spec.md: three counting related or contradicts relations [claims: 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C5, 43fdfb08b4ae42db3dc9b8f89069d7d0/5/opencode-go:deepseek-v4.1-flash/C6] - link it in a maintainer-answered Q-record's research_items and name its path in research_neighbours keep or drop
> research-handoff: 94 finding(s)
> ```

Stage-2 call, 2026-11-26: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.4 · reason two Codex draft attempts failed · leak check clean over 1283 files, 6026 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.4","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/pi-work-route/draft-attempt-3-20261126T185637626766Z (9849a1e395e5); `git diff 6820e20c9fdb refs/stage2/attempts/pi-work-route/draft-attempt-3-20261126T185637626766Z` shows it.
>
> The runner put back:
> - `docs/adr/0027-work-verbs-through-pi.md`
> - `plans/INDEX.md`
> - `plans/changes/pi-work-route/design.md`
> - `plans/changes/pi-work-route/plan.md`
> - `plans/changes/pi-work-route/spec.md`
