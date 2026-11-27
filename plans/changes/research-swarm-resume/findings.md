---
title: "Findings — research-swarm-resume"
category: findings
status: draft
implementation_status: none
date: 2026-11-26
created: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-27
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

Stage-2 call, 2026-11-26: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1290 files, 6045 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-26

Spec fingerprint: sha256:da86e8f8275563f8ed85ad8146a477a01e49a8b488013b6db07f07cb367c445b

Spec review commit: 3f55efa3e97dea986b42cd751df04d201cc72fe8

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-4 | MAJOR | SPEC | base | Acceptance criterion 5; Open decisions [DETAIL] S-1; Non-goals (first bullet); Definition of Done (documentation line); `scripts/stage2_research_snapshot.py`, `stored_binding` | [AMBIGUITY] Criterion 5 and the S-1 [DETAIL] build the map and topic 6's history from "the first run's stored frozen inputs", but the store does not hold those inputs today. `stored_binding` keeps path digests, the normalised digest of `research.md`, the append, the prepared publication with its day, and the brief. It keeps no frozen HEAD (which `build_research_history` needs), no map, no history and none of the original `research.md` bytes. The stored publication prefix is the corrected header, not the bytes that `merge_research_map` resolved against in run 1. Reading A: adding these values to the stored run record is allowed, because `changed_against_stored` still compares exactly what it compares now; the fix persists them and replays them. Reading B: the binding's shape is part of the "frozen-binding contract" that Non-goal 1 protects, and WORKFLOW Q-13 describes it as "the digests of the frozen inputs", with the DoD expecting no documentation change. The fix may then only reconstruct from what is already stored, such as the map and history fences in run 1's published tail. That works only when run 1 published, and it cannot recover run 1's original `research.md` extents. Which of the two is allowed decides the design. | Opus | in spec — Reading A recorded as [DETAIL] S-4 in spec.md (persisting replayable origin-baseline fields in stored run record is in scope; WORKFLOW Q-13 update allowed) | — |
| S-5 | MAJOR | SPEC | base | Acceptance criteria 1 and 5; Definition of Done (two-run regression); `Store.resume_source`, `Run.open` | [AMBIGUITY] "The first run" has two readings once a resume itself resumes, and only the latest stored run is ever a source. Reading A: the run that launched the seat (`launched_in`). Run 2 must then store the replayed run-1 inputs rather than its own freeze, and run 3 replays them, so the seats run 2 adopted from run 1 keep their hash. Reading B: the immediate source run. Run 2's binding is built from its live freeze, which already holds run 1's appended tail. Run 3 then builds from that freeze, the seats adopted from run 1 get a new prompt hash, and the drift returns one resume later. The maintainer's own observation spans three runs (pi-work-route runs 1–3, `decisions.md` Q-1). The DoD's two-run regression cannot go red under either reading, so whether replayed inputs carry forward is invented while building. | Opus | in spec — Reading A recorded in criteria 1/2, DoD (3-run regression), and [DETAIL] S-5 in spec.md | — |
| S-6 | MAJOR | SPEC | base | Acceptance criteria 2, 4 and 5; Non-goals (third bullet); `Run.validate_topic`, `Run.compose`, `Run.warn_judge_allowance` | [AMBIGUITY] The spec replays first-run inputs into the prompt but does not say whether the rest of the run uses them too. Today these all read `self.sources`, `self.map` and `self.history` from the current freeze: reuse validity (`plan_reuse` calls `validate_topic`), the validation of a newly launched seat, the judge packet and the published `map` and `history` fences. Reading A, replay into the prompt text only: stored and relaunched reports are validated against the republished `research.md` (corrected header, removed skeleton notices, appended tail) and against history at the moved HEAD, which is not what the seat was shown. A citation that no longer resolves gets the `validation` reason and the seat is relaunched, so criterion 2 goes red in exactly the committed-publication case the DoD names. Criterion 5's "history entries `validate_research_report` requires" then names a different history from the one in the prompt. Reading B, replay everywhere: reuse holds, but run 2 publishes run-1 extents and history under its own `baseline HEAD` line, which touches Non-goal 3's "published research content". The two give different reuse results and different published records. | Opus | in spec — Reading B recorded in criteria 2/5, Non-goals, and [DETAIL] S-6 in spec.md | — |
| S-7 | MAJOR | SPEC | base | Acceptance criterion 5; Definition of Done ("non-empty mapped excerpts"); `Run.repository_prompt`, `stage2_research_map.merge_research_map` | [AMBIGUITY] The repository prompt carries no excerpt text. For each resolved entry, its `# Finder map (data)` packet holds only `extent` (start and end line) and `excerpt_sha256`, and `merge_research_map` says it returns "extents and hashes, never whole frozen-file snapshots". So "preserves the finder map's resolved excerpts" has two readings. Reading A: keep the resolved entries with their extent and hash, as today. Reading B: excerpt text must appear in the prompt, which adds new content and changes every repository prompt hash. Under Reading A the refutation "drops mapped source excerpts" can never be observed, because the prompt has no excerpt to drop. An implementer can then drop or blank `extent` and `excerpt_sha256`, the fields that shift when `research.md` is republished with its corrected header and appended tail. That reaches byte-identity and leaves criterion 5 green: the deletion route S-2 was meant to close. | Opus | in spec — Reading A tightened in criterion 5, DoD, and [DETAIL] S-2 & S-7 in spec.md (explicitly requires non-empty extent and excerpt_sha256) | — |

Stage-2 call, 2026-11-26: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1290 files, 6047 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-26

Spec fingerprint: sha256:ce4aeeb8ed36b45e605da40e9e7ec338ea08a54a565ace715e0f74443ccbbeb6

Spec review commit: 46e509abfb24ac7f370ac3350a74ef432e77cf6e

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-8 | MAJOR | SPEC | base | Acceptance criteria 2, 3 and 5; Open decisions [DETAIL] S-6; Definition of Done (three-run regression); `Run.claude_command` (`cwd = self.root` when `tools == "repository"`), `stage2_research_report._reference` | The spec ties a resumed run's prompts and validation to the origin baseline. It says nothing about what a seat launched on that resumed run actually reads. A repository seat runs with `cwd = self.root`, which is the live worktree. So the seat relaunched under criterion 3 sees the published `research.md`: corrected provenance header, skeleton notices removed, and run 1's appended tail. After a commit it also sees git history at the moved HEAD. Its prompt and, under S-6, its validation use run 1's original `research.md` bytes and run 1's history. `_reference` checks `path::reference` citations against `sources` and commit citations against `history["commits"]`. A `research.md` line citation taken from the live file is checked against bytes whose lines have shifted. A topic-6 citation of the publication commit is checked against a history that does not contain it. Both come back unsupported, and this hits exactly the run-2 seat that DoD run 3 must reuse. The deterministic regression uses scripted seats that read nothing, so it stays green either way. Nothing settles which of these holds: a seat launched on a resumed run must be given a view of the origin baseline; or its own citations are checked against its live view while reused results are checked against the baseline; or the mismatch is accepted. The implementer will pick one silently. | Opus | in spec — final draft after round 3: reused seats validate against origin baseline, newly launched seats validate against live worktree + origin baseline fallback (criterion 2 & [DETAIL] S-6/S-8/S-9) | — |
| S-9 | MINOR | SPEC | base | Open decisions [DETAIL] S-6 ("recording the replayed baseline HEAD truthfully"); Non-goals (third bullet); `Run.compose` (`baseline HEAD … · input digest …` line), `Run.manifest_record` (`head`, `digest`, `untracked`) | [AMBIGUITY] "Recording the replayed baseline HEAD truthfully" has two readings. Reading A: run 2's `baseline HEAD` line and manifest-fence `head` name the origin run's HEAD, because that HEAD produced the published `history` fence. They then disagree with `input digest` and `digest`, which hash run 2's own HEAD and paths, unless those are replayed too. Reading B: `head` and `digest` keep run 2's own freeze, as today, and the origin HEAD goes into an added field. Run 2's `baseline HEAD` line then names a HEAD that its published `history` fence was not built from. The two readings publish different record bytes and tell a reader of the resumed block different baselines. The spec does not say which one applies. | Opus | in spec — Reading B recorded as [DETAIL] in spec.md (criterion 5 & Open decisions: keep own head/digest, add origin_head; bounded standing grant for non-BLOCKER spec-review rows) | — |
| S-10 | MINOR | SPEC | base | Definition of Done (three-run regression); Acceptance criterion 2 ("fails another seat"); `Run.stage_topics`, `stage2_research_judge.build_research_judge_packet` | The three-run regression cannot be built as written. If run 2 "reuses all other seats", seat A is the only seat run 2 launches. A seat B other than A can only fail in run 2 if B also had no finished result in run 1, and "run 1 fails seat A" does not say that. Once B succeeds, run 3 also cannot "launch only seat B": the topic stage then completes, and the judge launches on every run that reaches it, because its packet is built with that run's own `run_id`. So the test author has to invent the scenario. B could be the judge. B could be a second repository seat that run 1 also failed or left interrupted, with "only" counted over repository-topic seats. Or B could be A failing a second time. In that last case no seat launched in run 2 is reused in run 3, so the S-5 carry-forward of a run-2 seat is never tested. | Opus | in spec — three-run scenario fixed in criterion 2, DoD & [DETAIL] S-5/S-10 (run 1 fails A+B; run 2 succeeds A, fails B; run 3 launches only B among repo-topic seats then judge) | — |

Stage-2 call, 2026-11-26: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1290 files, 6053 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1290 files, 6055 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1290 files, 6056 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1290 files, 6057 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1290 files, 6059 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1290 files, 6060 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1290 files, 6060 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1290 files, 6060 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1290 files, 6061 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1290 files, 6062 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1290 files, 6063 commits, 12 rules.

Stage-2 call, 2026-11-26: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1290 files, 6063 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1290 files, 6069 commits, 12 rules.

Stage-2 call, 2026-11-27: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6075 commits, 12 rules.

## Phase 6 — Codex, 2026-11-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:1644` | A seat relaunched in run 2 can produce a valid report citing the publication commit or a new heading in the live `research.md`. Run 2 accepts it against live evidence, but run 3 validates that stored report only against the origin baseline, rejects it and launches the successful seat again. The three-run regression uses scripted reports that do not exercise this case. [Criterion 2] | Codex | fixed — tests/test_stage2_swarm.py::test_reused_report_accepts_live_publication_heading | — |
| F-2 | MAJOR | SPEC | base | `scripts/stage2_research_run.py:1646` | A newly launched topic-6 report can cite both an origin-only reference from its prompt and the later publication commit visible in the live worktree. Neither complete validation pass supports both citations, so a report whose only claim uses both is rejected even though each citation is supported by one of the required baselines. [Criterion 2] | Codex | fixed — tests/test_stage2_swarm.py::test_resumed_report_combines_origin_and_live_citations | — |

Phase 6 verdict: codex 01a21ab9-c01c-7a52-b5bd-f688f27981fa, 2026-11-27
Reviewer session: codex 01a21ab9-c01c-7a52-b5bd-f688f27981fa — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|

No loop row was reported.

Rounds run: 1

Record digest: sha256:c64a69aef0660eaa4ab6177d260732791142d51905c4f0957d8db389b824c7de

Record identity: sha256:e0430db126ccec6484c1fed4ce464329ee42dea6e6a8ba930fd530996da796c9

Loop state: {"availability": {"checked_at": "2026-11-27T00:53:20+00:00", "failed": {"deepseek-v4-pro": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "glm-5.3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "grok-4.7": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "hy3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "hy4-preview": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "kimi-k3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated.\"}", "qwen3.8-max": "pi call failed: exit 1: 403 {\"type\":\"error\",\"error\":{\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/go.\"}}"}, "reachable": ["hy4-flash-free", "deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "glm-5.2": "absent from the fresh provider catalog", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "qwen4-max": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": ["the data terms of deepseek-v4.1-flash expire on 2026-11-30 (3 days left)", "the data terms of deepseek-v4-pro expire on 2026-11-30 (3 days left)"]}, "consumed": ["free"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-fable-5-2", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "gemini-4-carbon", "provider": "opencode"}, {"model": "gemini-4-hydrogen", "provider": "opencode"}, {"model": "gemini-4-neon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "gpt-6.2-astra", "provider": "opencode"}, {"model": "gpt-6.2-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "hy4-flash-free", "provider": "opencode"}, {"model": "iceman-free", "provider": "opencode"}, {"model": "inkling-2-small-free", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "longcat-2.5-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-ember-1.0", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "tidepool-alpha-free", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-flash-free", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "qwen4-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-27T00:47:08+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1795740428026, "etag": "W/\"cc2f04cbfe8260c9f7e1aa3de29586be\"", "lastModified": 1795094589000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash 1017", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "hy4-flash-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4 flash Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "LongCat 2.5 Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.075, "cacheWrite": 1.875, "input": 1.5, "output": 4.5}, "id": "qwen4-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Qwen4 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": ["opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-flash-free", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "longcat-2.5-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "qwen4-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-11-13", "id": "longcat-2.5-free", "reason": "The maintainer took the longcat models out for good on 2026-11-13 (\"das scheint ein sehr langsames modell zu sein\"): longcat-2.0 timed out on all three online topics of that day's research swarm run; the free longcat id goes with it (bead coding-harness-363r.2)."}, {"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["hy4-flash-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "rungs": ["qwen3.8-flash", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor, qwen4-max.
> Notice: the data terms of deepseek-v4.1-flash expire on 2026-11-30 (3 days left).
> Notice: the data terms of deepseek-v4-pro expire on 2026-11-30 (3 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> hy4-flash-free reported no finding.
> From hy4-flash-free:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> No finding.

<!-- End of released loop record -->

Stage-2 call, 2026-11-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6078 commits, 12 rules.

Runner restoration, 2026-11-27: repair · attempt 1 · route codex — lifecycle fields: plans/changes/research-swarm-resume/plan.md, plans/changes/research-swarm-resume/spec.md — unchanged

Stage-2 call, 2026-11-27: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6083 commits, 12 rules.

## Phase 6 — Codex, 2026-11-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | base | `scripts/stage2_research_run.py`, `validate_topic`; `scripts/stage2_research_report.py`, `_evidence` | A seat launched in run 2 can cite a `research.md` heading whose section contains run 1’s appended publication. When run 3 reuses that seat, the same heading also resolves in the origin file, so validation accepts the shorter origin excerpt and never checks the live excerpt the seat cited. The reused report can therefore reach the judge with evidence that omits the cited publication. [Criterion 2] | Codex | fixed — tests/test_stage2_swarm.py::test_reused_heading_evidence_includes_live_publication | — |
| F6-2 | MAJOR | SPEC | base | `scripts/stage2_research_run.py`, `stage_history` and `validate_topic`; `scripts/stage2_research_history.py`, `build_research_history` | A topic-6 seat launched on a resumed run can validly cite that run’s publication commit. After enough matching resumes commit further publications, that commit falls outside the live history’s ten-commit limit and is absent from the origin history. The next resume rejects and relaunches the previously valid seat instead of carrying it forward. [Criteria 2 and 5] | Codex | fixed — tests/test_stage2_swarm.py::test_resumed_history_carries_aged_out_commit | — |

Phase 6 verdict: codex 01a21b0f-71b0-7910-88d9-e6adf7268527, 2026-11-27
Reviewer session: codex 01a21b0f-71b0-7910-88d9-e6adf7268527 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-11-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6085 commits, 12 rules.

Runner restoration, 2026-11-27: repair · attempt 1 · route codex — lifecycle fields: plans/changes/research-swarm-resume/plan.md, plans/changes/research-swarm-resume/spec.md — unchanged

Stage-2 call, 2026-11-27: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6089 commits, 12 rules.

## Phase 6 — Codex, 2026-11-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R-1 | MAJOR | SPEC | fix-r2 | scripts/stage2_research_run.py:1642 | A reused repository report is validated against the live sources first even when `reused=True`; that argument never changes the selected baseline. If a citation points to a heading in `research.md` whose section grew after publication, the reused report’s resolved excerpt includes the new publication instead of the origin-run evidence shown to the seat. The judge therefore receives evidence different from the replayed origin baseline. Reused reports must be validated against that baseline. [Criterion 2] | Codex | fixed — tests/test_stage2_swarm.py::test_origin_launched_reused_heading_uses_origin_evidence | — |

Phase 6 verdict: codex 01a21b61-b141-7c21-b86b-4f1264f0e058, 2026-11-27
Reviewer session: codex 01a21b61-b141-7c21-b86b-4f1264f0e058 — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-11-27: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6092 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2_research_run.py` +13 -1
> - `tests/test_stage2_swarm.py` +16 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/research-swarm-resume/plan.md, plans/changes/research-swarm-resume/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: red; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_standin_call_counter.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); a fresh full `make verify` is still required before phase 6
> - Runner targeted checks: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> ........................................................................ [ 70%]
> .......................................................................F [ 77%]
> F....................................................................... [ 84%]
> ........................................................................ [ 91%]
> ........................................................................ [ 98%]
> ...................                                                      [100%]
> =================================== FAILURES ===================================
> _ test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete _
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/popen-gw4/test_a_failed_store_write_keep0/home'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x109212840>
>
>     def test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete(
>         sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
>     ) -> None:
>         # Criteria 18, 57 (phase-6 F-15). Planted fault: after the first failed terminal write the siblings'
>         # outcomes are dropped from the record, or a failed binding write loses the incomplete publication.
>         def broken(*_args, **_kwargs):
>             raise stage2_research_store.StoreWriteError("disk full")
>     
>         monkeypatch.setattr(stage2_research_store.Store, "write_result", broken)
>         monkeypatch.setattr(stage2_research_store.Store, "set_append", broken)
>         sworld.complete()
>         assert sworld.run() == 1
>         text = sworld.research.read_text(encoding="utf-8")
> >       slots = {s["slot_id"]: s for s in manifest_of(sworld)["slots"]}
>
> tests/test_stage2_swarm.py:3900: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> world = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/popen-gw4/test_a_failed_store_write_keep0/home'))
>
>     def manifest_of(world: SwarmWorld) -> dict:
>         text = world.research.read_text(encoding="utf-8")
>         blocks = re.findall(r"```research-swarm/v2 manifest\n(.*?)\n```", text, re.S)
> >       return json.loads(blocks[-1])
> E       IndexError: list index out of range
>
> tests/test_stage2_swarm.py:2198: IndexError
> ----------------------------- Captured stderr call -----------------------------
> failed: the research state store is unusable (disk full)
> _______ test_a_failed_append_binding_write_ends_incomplete_with_exit_one _______
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/popen-gw4/test_a_failed_append_binding_w0/home'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1091ba3c0>
>
>     def test_a_failed_append_binding_write_ends_incomplete_with_exit_one(
>         sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
>     ) -> None:
>         # Criterion 57 (phase-6 F-20). Planted fault: a failure writing only the research-append binding is
>         # suppressed, so the run publishes complete and exits 0 with no storage failure on record.
>         def broken(*_args, **_kwargs):
>             raise stage2_research_store.StoreWriteError("disk full")
>     
>         monkeypatch.setattr(stage2_research_store.Store, "set_append", broken)
>         sworld.complete()
>         assert sworld.run() == 1
>         text = sworld.research.read_text(encoding="utf-8")
> >       assert manifest_of(sworld)["status"].startswith("incomplete"), "the record must not read complete"
>
> tests/test_stage2_swarm.py:3918: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> world = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-4170/popen-gw4/test_a_failed_append_binding_w0/home'))
>
>     def manifest_of(world: SwarmWorld) -> dict:
>         text = world.research.read_text(encoding="utf-8")
>         blocks = re.findall(r"```research-swarm/v2 manifest\n(.*?)\n```", text, re.S)
> >       return json.loads(blocks[-1])
> E       IndexError: list index out of range
>
> tests/test_stage2_swarm.py:2198: IndexError
> ----------------------------- Captured stderr call -----------------------------
> failed: the research state store is unusable (disk full)
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete
> FAILED tests/test_stage2_swarm.py::test_a_failed_append_binding_write_ends_incomplete_with_exit_one
> 2 failed, 1025 passed in 209.35s (0:03:29)
>
> Standard error, last lines:
> Exception ignored in atexit callback: <function cleanup_numbered_dir at 0x107d054e0>
> Traceback (most recent call last):
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/lib/python3.12/site-packages/_pytest/pathlib.py", line 372, in cleanup_numbered_dir
>     try_cleanup(path, consider_lock_dead_if_created_before)
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/lib/python3.12/site-packages/_pytest/pathlib.py", line 341, in try_cleanup
>     maybe_delete_a_numbered_dir(path)
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/lib/python3.12/site-packages/_pytest/pathlib.py", line 293, in maybe_delete_a_numbered_dir
>     rm_rf(garbage)
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/lib/python3.12/site-packages/_pytest/pathlib.py", line 168, in rm_rf
>     shutil.rmtree(str(path), onexc=onerror)
>   File "/opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/shutil.py", line 759, in rmtree
>     _rmtree_safe_fd(stack, onexc)
>   File "/opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/shutil.py", line 674, in _rmtree_safe_fd
>     topfd = os.open(name, os.O_RDONLY | os.O_NONBLOCK, dir_fd=dirfd)
>             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/tests/stand_in_log_guard.py", line 134, in os_open
>     check(path, "os.open")
>   File "/Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/tests/stand_in_log_guard.py", line 119, in check
>     raise RawStandInLogAccess(message)
> stand_in_log_guard.RawStandInLogAccess: raw os.open of the declared stand-in counter calls.jsonl.counts.json at /Users/mikypiky/coding-harness/.claude/worktrees/research-swarm-resume/.venv/lib/python3.12/site-packages/_pytest/pathlib.py:168: use atomic_test_log.append_counted
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/research-swarm-resume/stage2/attempts/research-swarm-resume/attempt-1-20261127T051007897872Z-4d2c4b31.md
> ````

Stage-2 call, 2026-11-27: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1290 files, 6094 commits, 12 rules.

Runner restoration, 2026-11-27: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/research-swarm-resume/plan.md, plans/changes/research-swarm-resume/spec.md — unchanged

Stage-2 call, 2026-11-27: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1290 files, 6097 commits, 12 rules.

## Phase 6 — Codex, 2026-11-27

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | fix-r3 | `scripts/stage2_research_run.py:1655` | A report launched in the origin run can contain a claim whose citation did not resolve at that baseline. If a later publication adds that heading, revalidation falls back to the live file and marks the formerly unsupported claim as valid. The judge then receives evidence the original seat did not cite from its baseline. Reused origin-run results must be validated against that baseline. [Criteria 2 and 5] | Codex | taken — Criteria 2 and 5: for an origin-launched reused report (launched_in == origin_run_id), validate strictly against origin only (alternate=None) so a heading added only in a later publication never retroactively validates a claim from the origin run, with regression test | — |
| F-2 | MAJOR | SPEC | fix-r3 | `scripts/stage2_research_run.py:1586` and `scripts/stage2_research_run.py:2025` | In a long resume chain, a topic-6 report can cite a publication commit that later ages out of the ten-commit live history packet. If an intermediate run is interrupted after adopting that report but before publication, its stored binding still has an empty `history_commits` field. The next resume cannot validate the citation and relaunches the previously successful seat. The accumulated history must survive an interrupted run as well as a published one. [Criterion 2] | Codex | taken — Criterion 2: persist accumulated history_commits into the stored run record as soon as stage_history completes (before topic reuse/publication) so an interrupted intermediate run still carries accumulated commits forward to the next resume, with regression test | — |

Phase 6 verdict: codex 01a21bb0-fdda-7933-97b7-c12635a5e2be, 2026-11-27
Reviewer session: codex 01a21bb0-fdda-7933-97b7-c12635a5e2be — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
