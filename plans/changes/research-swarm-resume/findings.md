---
title: "Findings — research-swarm-resume"
category: findings
status: draft
implementation_status: none
date: 2026-11-26
created: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — research-swarm-resume

Stage-2 call, 2026-11-26: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1287 files, 6038 commits, 12 rules.

Stage-2 call, 2026-11-26: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1290 files, 6040 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-26

Spec fingerprint: sha256:c3e95f015ca12ed37c5d412f91572296638a23fb60850c56789234a4a9375768

Spec review commit: 966cd659d386c912d168be3b33dbdb7e8cd973b3

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | Acceptance criterion 1; `scripts/stage2_research_snapshot.py`, `changed_against_stored` | [AMBIGUITY] "The same frozen inputs" names two different resumes, and the fix differs between them. The store's matching resume does not require identical frozen bytes: `changed_against_stored` compares every frozen path except `research.md`, tolerates that file's own appended tail and its `updated:` restamp, and never compares HEAD. Reading A takes "same frozen inputs" literally, so a resume after the maintainer commits the run's own publication — HEAD moved, only `research.md` changed — is not the case the criterion names, and criterion 1 stays green there even if the drift is untouched. Reading B takes the store's notion, so that resume is in scope and every repository prompt, topic 6's mapped history included, must be rebuilt from the first run's stored values rather than from the current freeze (`Run.open` freezes the current tree; `stage_history` reads `manifest["head"]`). Under A there is little to change in the observed case; under B the map and the history must be replayed. The human settles which. | deepseek-v4.1-flash | in spec — Reading B recorded as [DETAIL] in spec.md (criterion 1 and Open decisions; standing grant for bounded non-BLOCKER spec-review rows) | — |
| S-2 | MAJOR | SPEC | base | Acceptance criterion 1; Non-goals | Nothing in the spec requires a repository prompt to keep what it carries today, so the cheapest way to meet criterion 1 is to delete the drifting part instead of neutralising it. Topic 6's `# Mapped history (data)` is built from live git at the freeze's head (`build_research_history`), and any map entry resolved from `research.md` comes from the current freeze's bytes (`merge_research_map`), so dropping that section or that entry makes every prompt byte-identical while shrinking what every repository seat sees and leaving topic 6's commit citations unsupported (`validate_research_report` needs `history` for them). No criterion, non-goal or Definition-of-Done line says the seat's packet must be preserved, so the implementer picks silently between neutralising the drifting bytes and removing the evidence. | deepseek-v4.1-flash | in spec — criterion 5 and [DETAIL] added to spec.md preserving mapped excerpts and topic-6 history | — |
| S-3 | MAJOR | SPEC | base | Definition of Done; Non-goals | The spec never says whether a run stored before the fix must still resume after it, which is the operational case the bead exists for. Reuse revalidates a stored record against the current run's inputs: `plan_reuse`'s validity calls `Run.validate_topic`, which passes `self.sources`, `self.history` and `self.map["neighbours"]` to `validate_research_report`. A fix that changes the packet, the history or the sources can therefore reject finished pre-fix slots, while the two-run regression the DoD names runs both runs on the fixed code and cannot detect it. No criterion, non-goal or DoD line says whether pre-fix stores must stay resumable, or whether the fix may invalidate or clear them, so the answer is invented during building. | deepseek-v4.1-flash | in spec — pre-fix store handling stated in spec.md Non-goals and Open decisions [DETAIL] | — |
