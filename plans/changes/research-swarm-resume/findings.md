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
