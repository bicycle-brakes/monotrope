---
title: "Findings — isolated-attempts"
category: findings
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — isolated-attempts

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1168 files, 5417 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-1-20261122T235341954952Z (295feb1d8d0b); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-1-20261122T235341954952Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1169 files, 5417 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1 (Reading additional input from stdin...)
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-2-20261122T235356283411Z (c70df113a37a); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-2-20261122T235356283411Z` shows it.

Stage-2 call, 2026-11-23: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1169 files, 5417 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1 ([claude-code:unrecognized_model] {"model":"glm-5.3","query_source":"sdk"})
>
> the attempt is saved at refs/stage2/attempts/isolated-attempts/draft-attempt-3-20261123T001221111819Z (c2e275bea16d); `git diff b12fa3c3dfad refs/stage2/attempts/isolated-attempts/draft-attempt-3-20261123T001221111819Z` shows it.
>
> The runner put back:
> - `docs/adr/0026-isolated-writing-attempts.md`
> - `plans/changes/isolated-attempts/design.md`
> - `plans/changes/isolated-attempts/plan.md`
> - `plans/changes/isolated-attempts/spec.md`

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1186 files, 5500 commits, 12 rules.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/changes/isolated-attempts/decisions.md`

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-isolated-writing-attempts.md` +52 -0
> - `plans/changes/isolated-attempts/decisions.md` +6 -3
> - `plans/changes/isolated-attempts/design.md` +71 -0
> - `plans/changes/isolated-attempts/plan.md` +91 -0
> - `plans/changes/isolated-attempts/spec.md` +139 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 3
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
> research-handoff: not measured - isolated-attempts Q-4: answer is not readable (mapping values are not allowed here
>   in "<unicode string>", line 1, column 178:
>      ... next start. The maintainer added: "es müssen sich andere harness ... 
>                                          ^)
> ```

Stage-2 call, 2026-11-23: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1190 files, 5505 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/isolated-attempts/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-isolated-writing-attempts.md` +1 -1
> - `plans/changes/isolated-attempts/decisions.md` +8 -4
> - `plans/changes/isolated-attempts/design.md` +1 -1
> - `plans/changes/isolated-attempts/plan.md` +1 -1
> - `plans/changes/isolated-attempts/spec.md` +1 -1
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 3
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
> research-handoff: not measured - isolated-attempts Q-4: answer is not readable (mapping values are not allowed here
>   in "<unicode string>", line 1, column 178:
>      ... next start. The maintainer added: "es müssen sich andere harness ... 
>                                          ^)
> ```

Stage-2 call, 2026-11-23: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1190 files, 5505 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-isolated-writing-attempts.md` +58 -17
> - `plans/changes/isolated-attempts/design.md` +58 -18
> - `plans/changes/isolated-attempts/plan.md` +68 -31
> - `plans/changes/isolated-attempts/spec.md` +197 -67
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `research-handoff` (block) exited 3
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
> research-handoff: not measured - isolated-attempts Q-4: answer is not readable (mapping values are not allowed here
>   in "<unicode string>", line 1, column 178:
>      ... next start. The maintainer added: "es müssen sich andere harness ... 
>                                          ^)
> ```

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1186 files, 5510 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `frontmatter-current` (block) exited 1
> plans/changes/isolated-attempts/decisions.md: stale — updated 2026-11-22 is older than its last change 2026-11-23 (6184443f)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> - plans/changes/isolated-attempts/spec.md is missing after the draft.
> - plans/changes/isolated-attempts/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-23: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1186 files, 5510 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `frontmatter-current` (block) exited 1
> plans/changes/isolated-attempts/decisions.md: stale — updated 2026-11-22 is older than its last change 2026-11-23 (6184443f)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> - plans/changes/isolated-attempts/spec.md is missing after the draft.
> - plans/changes/isolated-attempts/plan.md is missing after the draft.
> ```

Stage-2 call, 2026-11-23: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 1186 files, 5510 commits, 12 rules.

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/adr/0026-isolated-writing-attempts.md` +163 -0
> - `plans/changes/isolated-attempts/design.md` +189 -0
> - `plans/changes/isolated-attempts/plan.md` +120 -0
> - `plans/changes/isolated-attempts/spec.md` +291 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 20 characters left out …]
> - Runner targeted checks: gate `frontmatter-current` (block) exited 1
> plans/changes/isolated-attempts/decisions.md: stale — updated 2026-11-22 is older than its last change 2026-11-23 (6184443f)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ```
