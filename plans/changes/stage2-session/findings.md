---
title: "Findings — stage2-session"
category: findings
status: draft
implementation_status: partial
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-09
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-session

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 607 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md:44–51,74–85,113–117`; `research.md:58–61` | [GAP] No accepted OpenCode model or provider/model mapping is identified. Research reports no OpenCode declaration; undeclared transports must be refused, and new endpoint approvals are excluded. Only PR #89 is a prerequisite. Implementing the OpenCode path therefore requires an unstated declaration dependency or an invented supported-model contract; no permitted positive OpenCode invocation is specified. | Codex | in spec — Supported models and prerequisites: existing Codex positive path; OpenCode Go activation depends on the separately approved declaration, with fixture-only positive tests until then | — |
| F-2 | MAJOR | SPEC | base | `spec.md:37–38,66–77` | [AMBIGUITY] Consider Terminal accepting the command while its shell cannot find the CLI. Reading “Dispatch” as terminal acceptance produces success and a successful-dispatch audit. Reading AC8’s missing-executable refutation as requiring executable startup produces failure and a failed-dispatch audit. The spec gives these different outcomes for the same launch state without defining which boundary determines success. | Codex | in spec — maintainer said "mach weiter" to the recommendation on 2026-10-07; Terms and criterion 8 distinguish prerequisite refusal from Terminal acceptance and subsequent GUI-window failures | — |
| F-3 | MAJOR | SPEC | base | `spec.md:44–47` | [GAP] The association between a change and its dedicated worktree is undefined. Two attached, non-main linked worktrees can contain the same tracked change directory, so resolving that directory within the current root does not identify which worktree belongs to the change. For an invocation from the other change’s worktree, the implementer must invent the association that determines acceptance or refusal. | Codex | in spec — Supported models and prerequisites fixes the canonical main-checkout/.claude/worktrees/change association and attached-branch requirement | — |

Reviewer session: codex 01a116cd-d624-7ee0-9e14-3db0027c8eff

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 274 files, 612 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: operator terminated the known
GLM CLI process after more than 15 minutes without an answer or code changes.
CLI exit 143, runner exit 1; the worktree needed no restore. This is not a
completed implementation or review. Claude Code also reported that its local
catalog did not describe glm-5.3-flash; that warning alone does not establish
the cause of the missing response. No credentials were read by the orchestrator.

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 274 files, 614 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: the second GLM Flash attempt ran
as a file-tool worker and wrote the session verb: `scripts/stage2_session.py`
(the dispatch helper), `scripts/stage2.py` (session wiring, the required
`--model` and optional `--handover`, and the refusals for other verbs),
`tests/test_stage2_session.py` (refusal and dispatch tests over temporary
linked worktrees with fake CLI, effective-policy and Terminal stand-ins), the
`.stage2-sessions/` ignore entry, the workflow section "The interactive
session (`session`)", and this record. No command ran in the worker session:
`make verify`, the registry check and any repair belong to the runner step
that follows. The GUI/model smoke test is unrun. Review loop and final review
have not started.

Stage-2 call, 2026-10-07: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 276 files, 614 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: the repair attempt reviewed the
attempt-2 code against the block gates and repaired three defects, all in
`tests/test_stage2_session.py`: the denylist refusal is now asserted against
the rendered verdict on standard output instead of standard error, and the two
OpenCode dispatch tests now script the `osascript` stand-in step that runs the
launch command, so the recorded interactive `opencode` call exists and is
asserted exactly once. `scripts/stage2_session.py`, the session wiring in
`scripts/stage2.py`, the workflow section and the ignore entry stood the
review unchanged. No command ran in the worker session: `make verify`, the
registry check, the review loop and the final review belong to the runner
steps that follow. The GUI/model smoke test is unrun.

Stage-2 call, 2026-10-07: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 276 files, 615 commits, 12 rules.

Implementation attempt outcome, 2026-10-07: the Sonnet 5.5 fallback (Claude
Code with Anthropic) ran, and the runner's post-run checks stayed red; it
ended with exit 1 and "implementation post-run checks failed after the
allowed attempts". No checkpoint commit was made; the code stayed in the
worktree. The orchestrator (Claude Code with Anthropic, Opus 5.5) then
repaired it by hand: the Terminal command (absolute `/usr/bin/env`, the CLI
named once) and the effective-policy check rebuilt on OpenCode 1.18.35's
source, with tests and fixtures to match. `make verify` went green (1,199
passed, 16 skipped) and the checkpoint is `fb01133` on
`feat/stage2-session`. Details: the handover addendum of the same date.

Stage-2 call, 2026-10-07: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 276 files, 619 commits, 12 rules.

Stage-2 call, 2026-10-07: review-loop · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 276 files, 621 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 276 files, 623 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-4 | BLOCKER | SPEC | base | `scripts/stage2_session.py:123–183`; `scripts/stage2.py:441–449` | With `darf_sehen: not-framework` as a YAML string, substring membership incorrectly grants framework access. An empty `residenz` also passes validation. Both cases reproduced exit 0 and a Terminal call with fake launchers. Malformed permissions and missing residency must refuse before dispatch. [Acceptance criterion 2] | Codex | closed — c73d259; test_a_malformed_permission_or_residency_refuses | no |
| F-5 | BLOCKER | SPEC | base | `scripts/stage2_session.py:110–120` | If `.claude/worktrees/<change>` is a symlink to the main checkout, comparing both paths through `realpath` accepts that checkout. With worktree directories ignored, the complete invocation reproduced exit 0 and a Terminal call from branch `main`. The main checkout must remain forbidden regardless of a symlink alias. [Acceptance criterion 1] | Codex | closed — c73d259; test_a_link_that_aliases_the_main_checkout_refuses | no |
| F-6 | BLOCKER | SPEC | base | `scripts/stage2_session.py:549–553`; `tests/test_stage2_session.py:656–670` | Finalizing an accepted dispatch rewrites the entire findings file through a truncating write. A simulated disk-full error after truncation erased earlier findings and the pending audit, although the error claimed that pending evidence remained. The existing test raises before truncation and misses this loss. A failed update must preserve the existing record. [Acceptance criterion 7; design, Data model] | Codex | closed — c73d259; test_an_update_that_fails_mid_write_keeps_the_record_whole | no |
| F-7 | BLOCKER | SPEC | base | `scripts/stage2_session.py:543–547` | For a handover named `dispatch pending.md`, finalization replaces the status phrase inside the handover filename first. The resulting audit records `dispatch accepted.md` as its source while its actual dispatch status remains pending; finalization succeeds. This reproduced directly against the helper. Status updates must preserve the handover source and update the dispatch outcome. [Acceptance criterion 7] | Codex | closed — c73d259; test_a_handover_named_like_the_status_keeps_its_source | no |

Phase 6 verdict: codex 01a116cd-d624-7ee0-9e14-3db0027c8eff, 2026-10-08

## Phase 4b — GLM loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | SPEC | base | `plans/changes/stage2-session/spec.md:4` (likewise the other six artifact headers and their rows at `plans/INDEX.md:69–75`) | Every artifact of this change still declares `implementation_status: none`, and the regenerated index prints `none` beside each one, although the branch already carries the implemented session verb with a green full-verification record in its journal. The workflow defines this field as the one that moves when the code moves, so the registry view tells a maintainer scanning it that no code exists where the code is the point of the change; the honest value at this state is at least `partial`. | GLM | taken — all seven artefacts now `implementation_status: partial`; plans registry green | no | agree |
| L1-2 | MINOR | MAINT | base | `plans/changes/stage2-session/findings.md:71` | The audit trail stops mid-record: the third implement call line (the fallback route after the two failed primary-route attempts) has no outcome paragraph, unlike the two before it, and nothing in this file records the successful hand repair and green verification that produced the current head — that history lives only in the journal handover. A maintainer reading the change's findings sees an unanswered attempt as the last word on how the code got here. | GLM | taken — attempt-3 outcome and the hand repair recorded in findings.md | no | agree |
| L1-3 | MINOR | MAINT | base | `scripts/stage2_session.py:189` | An explicitly empty `--handover` value is treated as if the flag were absent: the change's own default handover is selected and dispatched without a refusal. Every other defect of a named handover (missing file, empty content, blank content) refuses, so the same operator mistake — an unset shell variable expanding to an empty string — silently starts the session on a different prompt than the one asked for. | GLM | taken — test_an_empty_handover_value_refuses_instead_of_taking_the_default | no | agree |
| L1-4 | MINOR | MAINT | base | `scripts/stage2_session.py:118–143` | The session module parses and validates `model-endpoints.yaml` with its own second reader (shape, names, duplicates) beside the runner's existing declaration check that the same code path also calls, so one file now has two parsers that must agree; a future change to the declaration's shape has to be made in both places, and the tests exercise only their agreement on today's shape. | GLM | rejected — the runner's shared declaration check refuses neither duplicates nor malformed shapes, which spec criterion 2 requires of a session; moving them into it changes every verb's refusals and is outside this change |  | disagree — The session reader adds structural checks absent from the shared checker; duplicate parsing alone does not demonstrate a correctness fault. |
| L2-1 | MAJOR | MAINT | round 2 | `scripts/stage2_session.py:445-460` (`cli_argv`) | The Codex launch passes the whole prompt as a trailing positional argument with no `--` end-of-options separator before it. The prompt begins with the handover text, and every journal handover in `docs/journal/handover/` — the handover source the change's own decisions explicitly bless for `--handover` — begins with YAML frontmatter, so the first token handed to the CLI is `---`. A CLI that treats a leading-dash token as an unknown option rejects the entire launch inside the new window, while the runner has already recorded `dispatch accepted.` — exactly the dead-launch state the audit cannot distinguish. The OpenCode path is immune (`--prompt` takes the text as a value); only the Codex form is exposed. Add a `--` separator (or refuse a prompt whose first line is option-like) so the one transport usable today survives the canonical handover format. | GLM | taken — test_a_handover_that_starts_like_an_option_stays_the_prompt (Codex after `--`, OpenCode `--prompt=`) | no | agree |
| L2-2 | MINOR | SPEC | round 2 | `plans/changes/stage2-session/design.md:74` (Data model) | The design says of the retained policy directory "Remove it after that session exits", but the runner returns the moment Terminal accepts the command (the settled dispatch boundary) and nothing ever observes the session ending, so no code path removes an accepted directory. Directories under the gitignored runtime root accumulate without bound across accepted sessions, and the sentence contradicts both the module docs and the workflow section, which say an accepted attempt keeps the directory. Either drop the sentence or add the cleanup on the next invocation; as written the design promises removal that the accepted architecture cannot perform. | GLM | taken — design.md data model: an accepted directory is never removed by the runner | no | agree |
| L2-3 | MINOR | MAINT | round 2 | `scripts/stage2_session.py:66,245-255` (`GUARDED`, `policy_config`) | The runner-supplied OpenCode policy writes a `webfetch` denial in addition to the guarded permissions, but the effective-policy verification (`GUARDED`) checks only `external_directory`, `task` and `bash`. A global or agent override that flips `webfetch` — or any other rule written into the config but outside the guarded set — to `allow` passes `verify_policy` silently, so the config file shows a denial that nothing confirms holds in the effective agent. A maintainer reading the policy file assumes every written rule is verified; either guard what is written or write only what is guarded. | GLM | taken — webfetch guarded; override case webfetch-allow in test_an_override_the_runner_did_not_write_refuses | no | agree |

Rounds run: 2

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 276 files, 623 commits, 12 rules.

## Addendum — re-pointed to Pi, 2026-10-09

No review ran. The rows above are the first build's record and stay as
written; they name OpenCode where the code then used it. On 2026-10-09 the
maintainer answered the phase-1a interview for the Pi move (`decisions.md`,
Q-1 to Q-6) and approved the plan
`docs/research/2026-10-09-session-verb-on-pi-plan.md`. Work package 2
re-pointed `spec.md`, `design.md`, `plan.md` and the ADR 0007 amendment draft
from the OpenCode CLI to Pi. The code in `scripts/stage2_session.py` still
starts OpenCode; nothing is implemented or tested for Pi, and the Mac smoke
test is unrun. Review of the Pi code (phases 4b and 6) has not started.
