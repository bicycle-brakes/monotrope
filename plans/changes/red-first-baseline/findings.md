---
title: "Findings — red-first-baseline"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — red-first-baseline

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1149 files, 5013 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1152 files, 5014 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | BLOCKER | SPEC | base | spec.md:27,31; decisions.md:29 | [AMBIGUITY] It is unclear which two runs make up "the mismatch" that criterion 1 must demonstrate using "its baseline and attempted test". Reading A: `red_first` is compared with a direct pytest run on the same inputs, meaning the refused attempt's saved `tests/` tree on the HEAD the runner captured before round 3's first call. A mismatch exists only if those two disagree. Reading B: the runner's round-3 refusal (the attempt's test bytes on the runner's baseline) is compared with the hand check in `5121a00c` (the hand-written tests against "the old scripts", possibly a different commit). Under A, an attempt test that really is green on that baseline gives no mismatch and nothing to fix in the runner. Under B, a weaker attempt test set against a stronger hand test "demonstrates" a mismatch, and the "fix" would make `red_first` accept a run that pytest itself passes, which criterion 2 forbids. The Problem cites `ca493614` and `5121a00c` as one discrepancy. It never says the hand check ran the attempt's bytes on the runner's baseline, and it names no baseline commit. | Opus | open | — |
| S-2 | BLOCKER | SPEC | base | spec.md:23,31-32,35,45; decisions.md:23 | [AMBIGUITY] It is unclear what the fix must achieve for the round-3 test. Reading A (spec line 23 and the bug as filed in decisions.md): the proof must report what pytest actually reports. A refusal that names the true baseline outcome satisfies this, for example a crash, a non-AssertionError failure or a skip, instead of "pytest ended 0". Reading B (criterion 1): the fixed proof must accept the round-3 run as a qualifying red. The two diverge whenever the true baseline outcome is red but not qualifying. For example, the name `…_is_invalid_without_crashing` suggests the old code crashes with an uncaught exception. Criterion 3 and the non-goal on the qualifying-failure definition require that case refused, so under B criteria 1 and 3 conflict, and under A the word "accepts" in criterion 1 is wrong. | Opus | open | — |
| S-3 | MAJOR | SPEC | base | spec.md:31,44-46,57,62 | The spec defines no outcome for three cases: the reproduction finds no runner fault (exit 0 was correct for the attempt's bytes), the saved attempt evidence cannot be found (research.md:63 could not locate it), or the measured cause falls under a non-goal. The non-goals that could apply are: code under test outside `tests/` (bf9m), an environment or interpreter difference (dependency provisioning), and the qualifying-failure definition. In each case criterion 1 cannot be met, yet the Definition of Done still requires the PR to close bead `coding-harness-7aso`. The spec does not say whether the change then ships only criterion 5 plus the evidence record, keeps the bead open, files a successor, or stops without a PR. The rule "stop and report if evidence or scope exceeds it" (line 62) is tied to the appetite and names no deliverable, so the implementer would have to decide. | Opus | open | — |
| S-4 | MAJOR | SPEC | base | spec.md:27,31,57; decisions.md:29 | The Problem names two finder-partial-report tests misjudged as green, but criterion 1 reproduces only the round-3 one (L3-1), and the second test is never named. The PR closes bead `coding-harness-7aso`, which covers both. The spec does not say whether the second case must also be reproduced and covered by the fix, or whether it may be closed on the assumption that it shares round 3's mechanism. If its mechanism differs, it is dropped without anyone deciding to drop it. | Opus | open | — |
| S-5 | MAJOR | SPEC | base | spec.md:31,54,58 | The spec does not say where criterion 1's regression gets its inputs. Option A: it replays the recorded objects (the round-3 baseline commit, the saved attempt tree, the unmerged `fix/finder-partial-report` test bytes) from the repository's own Git store. Then `make verify` depends on objects that may exist only in this local store, such as saved-attempt refs in a lane worktree's git directory or an unpushed branch, and those may be missing in CI clones or kit instances. Option B: it builds a self-contained disposable repository that distils the measured mechanism. Then nothing ties it to "the recorded refusal reproduced". The implementer has to pick one, and the choice decides whether the criterion is about the incident or about a mechanism. | Opus | open | — |
| S-6 | MAJOR | SPEC | base | spec.md:31-32 | Criterion 1's refutation is narrower than its claim. The claim is that the fixed proof "accepts the qualifying red". It is refuted only if the fixed proof "still reports exit 0". A fixed proof that now refuses the same run in another way is not caught: pytest exit 2, a collection error, a nonqualifying-failure diagnostic, a missing outcome record, or a ref fault. That proof neither accepts nor reports exit 0, so the criterion stays green while unmet. Separately, the half "demonstrates the mismatch before the fix" can only go red once, before the fix lands. After merge, no test or input can refute it, and it rests on the PR record alone (Definition of Done, line 58). | Opus | open | — |
| S-7 | MAJOR | SPEC | base | spec.md:33-36; research.md:36 | No criterion covers a baseline run whose selected cases end skipped, xfailed or XPASS. Criterion 2 covers runs where the test "actually passes" and criterion 3 covers runs where it "fails", so neither applies. pytest exits 0 for an all-skipped or xfailed selection, which is the incident's exit code, so a fix to the exit-0 path is exactly where such a run could start being accepted. The current contract refuses these outcomes (research.md:36), and the non-goal on the qualifying-failure definition forbids changing that. But a fix that accepts a skipped or xfailed baseline as red refutes no criterion, so nothing goes red. | Opus | open | — |
