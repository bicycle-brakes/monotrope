---
title: "Spec — codex-drafts"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, codex, draft, spec-review]
class: feature
appetite: 8
change: codex-drafts
adr_question: {proposed: "yes", reason: "It moves the spec review from Codex to Opus 5.5 and lets Codex write unattended, which amends the reviewer roles of ADR 0007 and ADR 0011, a maintainer decision."}
adr_files: [docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md]
---

# Spec — `codex-drafts`

After this change, one runner verb lets Codex (`gpt-6.1-sol`) draft a
change's spec, design and plan with the guards of `implement`, GLM 5.3 takes
over after two failed Codex attempts, and Opus 5.5 instead of Codex reviews
the spec (bead coding-harness-rhq). Research: [`research.md`](research.md).
Decisions: [`decisions.md`](decisions.md) — Q-1 to Q-5, answered by the
maintainer on 2026-10-12, and the stated reading of Q-5.

## Problem

Read on 2026-10-12 against `origin/main` (`research.md`, "Runner exploration
— 2026-10-12"; the branch's merge base is `02bf4b3`), and `codex exec --help`
of the installed codex-cli 0.162.0, read the same day.

- Phases 2, 2b and 3 run only in an interactive Claude session on Opus 5.5 at
  effort `xhigh` (`docs/WORKFLOW.md` §3): the most expensive phases cost
  Claude tokens, and no runner verb drafts them (`VERBS` in
  `scripts/stage2.py`).
- No headless Codex call can write: `run_codex` pins
  `sandbox_mode="read-only"` on every call. The one writing Codex path is the
  interactive `session` verb (ADR 0012), which needs a person at a terminal
  and cannot run in the night run.
- The spec review (phase 2a) is Codex's (`spec_review` passes `CODEX` to
  `preflight`, `begin_call` and `run_codex`; ADR 0011 decision 2). If Codex
  drafts the spec, Codex would review its own draft — what Q-1 rules out.
- Phase 6 resumes the Codex session of phase 2a (`SESSION_LINE` matches
  `Reviewer session: codex <id>` only; `docs/WORKFLOW.md` §3, "One reviewer
  for both"). With 2a on Opus, no Codex 2a session exists to resume.
- The gate `adr-answers` holds every `feature` to an answer file that only the
  maintainer's stated answer may create (`scripts/check_adr_answers.py`;
  `decisions.md`, second agent detail). A drafted feature therefore meets a
  red `make verify` that no drafter can repair (criterion 13 gives the gate
  one exception for it).
- `begin_call` writes a new `findings.md` header with producer `codex` or
  `pi` only; a Claude reviewer would be recorded as `pi`.

## Terms

- **Draft**: one run of `python3 scripts/stage2.py draft <change>` — up to
  three attempts, at most one commit.
- **Attempt**: one route of the draft — the model call, the put-back of paths
  outside what a draft may write, then the post-run checks.
- **Baseline**: `HEAD` when the draft starts.
- **New ADR file**: a path `docs/adr/<NNNN>-<slug>.md` (four digits, a slug of
  lowercase letters, digits and hyphens) that the merge base of the baseline
  and `origin/main` does not hold — so an ADR an earlier draft of the same
  change committed stays the change's one new ADR file, and a later draft
  may edit it.
- **Audit line**: the `Stage-2 call, …` line the runner writes into
  `findings.md` before each call.

## Acceptance criteria

1. When `draft` starts a Codex attempt, the call is `codex exec` with
   `-m gpt-6.1-sol`, `model_reasoning_effort="max"`,
   `sandbox_mode="workspace-write"`, hooks and memories disabled, and none of
   `--add-dir`, `--approve-for-me`,
   `--dangerously-bypass-approvals-and-sandbox`, `-s`, `--sandbox`,
   `--ephemeral`.
   *Refuted by:* a draft call whose argv carries `read-only` or
   `danger-full-access`, one of the named flags, another model or effort, or
   hooks or memories left on.
2. When the runner calls Codex for the phase-6 review or its loop marks, the
   sandbox stays `read-only`.
   *Refuted by:* a `review` call with `workspace-write` in its argv.
3. When a draft attempt's prompt is built, it holds `prompts/02-spec.md`,
   `prompts/02b-design.md` and `prompts/03-plan.md` in full, the rules of
   `AGENTS.md`, the change's folder, the runner's drafting rules (what to
   write, what is put back, that open phase-2a rows are worked in, that no
   answer is written for the maintainer) and the read request.
   *Refuted by:* a prompt, on the Codex or the GLM route, that lacks one of
   the three prompt texts or the drafting rules, or names another change.
4. If the change's `research.md` has no bead in its header, or `research.md`
   or `decisions.md` cannot be read, `draft` refuses with exit 2 before any
   call.
   *Refuted by:* a Codex call for a change folder without `decisions.md`.
5. If the worktree has changes outside the change's `findings.md` before the
   first attempt, `draft` refuses with exit 2 before any call.
   *Refuted by:* an uncommitted edit of `src/app.py` followed by a Codex call.
6. When a draft attempt starts, the declaration and the leak check run for
   that attempt's endpoint and exact prompt immediately before its call, and
   `findings.md` gains its audit line with the verb `draft`, the attempt's
   number, route, endpoint and model, and — for attempts 2 and 3 — the reason
   it started.
   *Refuted by:* an attempt without its own audit line, one leak check for
   the whole run, or a fallback's line without its reason.
7. If the leak check of an attempt is not clean, the run stops with exit 2 and
   starts no later attempt.
   *Refuted by:* a second Codex call or a GLM call after a leak refusal.
8. When an attempt's call has returned, every path git reports as changed
   outside `plans/changes/<change>/` is put back at the baseline, a new ADR
   file excepted, and `findings.md` names each path put back.
   *Refuted by:* an edited `src/app.py`, a new `src/new.py`, an edited
   existing ADR or a written `decisions/answers/<change>/adr.yaml` in the
   commit, or a path put back without being named.
9. When an attempt's call has returned, an edit of the change's
   `decisions.md` is put back at the baseline too.
   *Refuted by:* an answered record the model added to `decisions.md`
   reaching the commit.
10. If more than one new ADR file is left after an attempt's call, the
    attempt fails its post-run checks with a diagnostic naming them.
    *Refuted by:* a commit that adds two files under `docs/adr/`.
11. If `HEAD` is not the baseline after an attempt's call, the runner stops
    with exit 1, says that `HEAD` moved, and makes no put-back, no commit and
    no later attempt.
    *Refuted by:* a stand-in that commits, followed by a restore, a runner
    commit or another call.
12. When an attempt's call has returned and the put-back is done, the runner
    stamps the changed held documents, renders `plans/INDEX.md` and runs
    `make verify`, and a red `make verify` fails the attempt's post-run
    checks.
    *Refuted by:* an attempt that passes with `make verify` red for a reason
    criterion 13 does not name, or that never runs `make verify`.
13. The gate `adr-answers` itself checks the one exception: the runner sets
    `ADR_ANSWERS_TOLERATE_CHANGE=<change>` for its own `make verify` only, and
    the gate then tolerates exactly that change's missing answer file. The
    runner reads no gate output for this; the exit code of `make verify`
    decides. When the answer was tolerated, `findings.md` says the ADR answer
    is owed to the maintainer; the checks of criteria 14 to 16 still apply.
    Any other red gate, another change's missing answer and a refused answer
    file still fail the gate, and so the attempt.
    *Refuted by:* a draft failing on that alone; or one passing when the gate
    reports another change or a refused answer file, when a second gate
    blocks, or when `plan.md` lacks `## Time used`; or a gate that tolerates
    a missing answer without the variable set to that change.
14. If `spec.md` or `plan.md` is missing in the change folder after an
    attempt, the attempt fails its post-run checks with a diagnostic naming
    the file.
    *Refuted by:* a commit of a change folder without `plan.md`.
15. If `plan.md` does not open with the plan card — a fenced block before its
    first level-two heading whose lines begin `For you:`, `Done when:`,
    `Appetite:`, `Not now:` and `Pre-mortem:`, in this order — the attempt
    fails its post-run checks with a diagnostic saying so.
    *Refuted by:* a commit of a `plan.md` whose card lacks `Pre-mortem:` or
    stands after `## Criterion ledger`.
16. If `plan.md` has no `## Time used` heading after an attempt, the attempt
    fails its post-run checks with a diagnostic saying so.
    *Refuted by:* a commit of a `plan.md` without the heading.
17. When an attempt passes its post-run checks, the runner makes exactly one
    commit on the baseline holding the attempt's result, and the worktree is
    clean afterwards.
    *Refuted by:* no commit, two commits, a changed file left out of the
    commit, or a dirty worktree.
18. If the first attempt fails — its call or its post-run checks — the second
    attempt is Codex again, with the first attempt's diagnostics in its
    prompt.
    *Refuted by:* GLM as the second attempt, or a second prompt without the
    first attempt's diagnostics.
19. If the second attempt fails, the third and last attempt runs `glm-5.3` on
    `glm-coding-plan` through Claude Code with the tools
    `Read,Grep,Glob,Edit,Write`, with both earlier attempts' diagnostics in its
    prompt.
    *Refuted by:* a third Codex call, `glm-5.3-flash`, a shell tool, or a
    fourth attempt.
20. If an attempt's call fails, every path except `findings.md` is put back
    at the baseline before the next attempt starts, and `findings.md` holds a
    quoted block below that attempt's audit line saying why the call failed.
    *Refuted by:* a `spec.md` half-written by a dead Codex call that the next
    attempt finds, or no block.
21. If an attempt fails its post-run checks, `findings.md` holds that
    attempt's quoted block — the files its model changed and its diagnostics —
    below its audit line, and the next attempt starts on the tree it left.
    *Refuted by:* a missing block, or a tree put back after a post-run
    failure.
22. If all three attempts fail, the runner exits 1 with a message that names
    `findings.md`, and makes no commit.
    *Refuted by:* exit 0 or 2, a commit, or a message without `findings.md`.
23. While the Codex attempts run, the runner has not read the GLM key.
    *Refuted by:* the secrets file read during a draft whose first attempt
    passes.
24. If the GLM key is missing when the GLM attempt is due, the run refuses
    with exit 2 and makes no GLM call.
    *Refuted by:* a Claude Code call against Z.ai without the key.
25. If the GLM attempt leaves the GLM key, whole or as a fragment of eight or
    more characters, in a changed file, the runner removes it and refuses with
    exit 2 without a commit.
    *Refuted by:* a commit or a `findings.md` holding an eight-character
    fragment of the planted key.
26. If `--stage2-off` is given with `draft`, the runner refuses with exit 2
    before any call.
    *Refuted by:* any call after `draft demo --stage2-off`.
27. When `spec-review` runs, it starts Claude Code on `claude-opus-5-5` at
    effort `xhigh` with the tools `Read,Grep,Glob`, `--restricted` and no
    session kept, without a GLM or OpenCode Go variable, and starts no Codex.
    *Refuted by:* a `codex` call, another model or effort, `Edit` or `Write`
    among the tools, or `ANTHROPIC_BASE_URL` in the call's environment.
28. When the Opus spec review answers, `findings.md` gains a block headed
    `## Phase 2a — Opus 5.5, <date>` whose rows carry Reviewer `Opus`, Status
    `open` and Broke a test `—`, and no `Reviewer session:` line.
    *Refuted by:* rows marked `Codex`, or a session line after the block.
29. If `findings.md` does not exist when the Opus spec review starts, the
    header the runner writes names `claude-code` as its producer.
    *Refuted by:* `name: pi` or `name: codex` in that header.
30. When `review` runs on a change whose `findings.md` holds no
    `Reviewer session: codex <id>` line, or whose last `## Phase 2a` block is
    headed `Opus 5.5`, Codex starts a fresh session and
    `findings.md` says that no phase-2a session was recorded.
    *Refuted by:* a `codex exec resume` call, or no such statement.
31. When `review` runs on a change whose last `## Phase 2a` block is Codex's
    and holds a `Reviewer session: codex <id>` line (a change reviewed before
    this change), it resumes that session as today.
    *Refuted by:* a fresh session although that block and line stand, or a
    resumed session after an Opus block that follows the line.
32. When `docs/WORKFLOW.md` is read, its routing rows and its class table send
    phases 2, 2b and 3 to Codex through `draft` with GLM 5.3 after two failed
    attempts, phase 2a to Opus 5.5 through `spec-review`, and phase 6 to
    Codex in a fresh session.
    *Refuted by:* a routing row or a class-table cell that still sends 2a to
    Codex or calls the phase-6 reviewer "the same Codex agent, resumed".
33. When `docs/WORKFLOW.md` §4 is read, it states the order of a drafted
    change: `draft`; the orchestrating session reads the whole draft;
    `spec-review` on Opus 5.5; a second `draft` that works the 2a rows in; the
    plan card shown to the maintainer unchanged.
    *Refuted by:* one of the five steps missing from the section.
34. When the phase prompts are read, the `**Model:**` lines of
    `02-spec.md`, `02b-design.md` and `03-plan.md` name Codex and
    `stage2.py draft <change>`, the one of `02a-spec-review.md` names Opus 5.5
    and `stage2.py spec-review <change>` and no Codex, and `06-review.md` says
    the Codex session starts fresh where phase 2a ran on Opus.
    *Refuted by:* a prompt whose Model line still routes its phase as before.
35. When `AGENTS.md` is read, its stage-2 paragraph names `draft`, Opus 5.5
    for 2a and Codex for 6, and the file has at most 200 lines.
    *Refuted by:* "Codex reviews 2a and 6" still standing, or 201 lines.
36. When `model-endpoints.yaml` is read, the `openai-codex` remark names the
    draft and the phase-6 review and no longer the spec review, the
    `opencode-go` remark no longer says that phase 2a stays with Codex, and
    the `glm-coding-plan` remark names `glm-5.3` drafting after two failed
    Codex attempts.
    *Refuted by:* any of the three remarks routing as before.
37. When the change is proposed for merge, its pull request adds ADR 0016 as
    a new file under `docs/adr/` and edits no existing ADR.
    *Refuted by:* a changed `docs/adr/0007-…`, `0011-…` or `0012-…` file in
    the pull request's file list.

## Non-goals

- **Phase 6 moving off Codex.** Q-1 keeps the code review with Codex.
- **A Stage-1 route inside `draft`.** Where Stage 2 is off, Opus 5.5 drafts
  as §3 says, by hand; `draft` takes no `--stage2-off` (criterion 26).
- **Retiring the `spec-planner` agent.** It is a user-level definition
  outside the repository (`research.md`, orchestrator's note); nothing here
  edits it.
- **Resuming the drafting thread in phase 6.** Codex's drafting thread is not
  recorded; phase 6 starts fresh (criterion 30).
- **A runner check that every 2a row was worked in, or of a change's class.**
  The 2a gate stays the review's; the class check waits for the
  change-artefact validator (bead coding-harness-jc3).
- **A time limit on a Codex or Claude Code call**, as for `implement` today.
- **Reserving ADR numbers across open branches.** The drafter numbers after
  the highest file in its tree; the orchestrator renumbers before the
  decision pull request when an open branch holds the number.
- **Confining what Codex reads, verifying its sandbox, or putting back
  ignored files and paths outside the worktree.** The runner sees what git
  sees; the residual risk is the ADR's to state.
- **Measuring Codex's usage limits or cost.**
- **Changing `implement`, `review-loop`, `release-loop`, `probe` or
  `session`** beyond the shared helpers they already use.

The design phase 2b runs: the class is `feature` and the ADR question is
proposed "yes".

## Protected areas

- `provenance.yaml`, `decisions/` — maintainer-owned; the ADR answer of this
  change is recorded only from the maintainer's stated answer.
- `decisions/gates.yaml` — the gate list does not change. (The gate's script
  `scripts/check_adr_answers.py` is not protected: criterion 13 puts the
  exception there. Amended by the maintainer on 2026-10-13 after phase-6 row
  F-13: "Die ADR-Prüfung selbst" checks the exception.)
- `scripts/stage2_runs.py`, `scripts/stage2_session.py`,
  `scripts/leakcheck.py` — they read and scan what this change writes
  unchanged.
- `docs/adr/0007-…`, `0011-…`, `0012-…` — amended by the new record, never
  edited (criterion 37).
- `.claude/settings.json` — the ask rule on a typed `codex` stays.

## Definition of Done

- `verify` green, with the maintainer's ADR answer for this change recorded
  (`decisions/answers/codex-drafts/adr.yaml`).
- Moved in the same pull request: `docs/WORKFLOW.md` §3 and §4, `AGENTS.md`,
  the three remarks in `model-endpoints.yaml`, the `**Model:**` lines of
  `prompts/02-spec.md`, `02b-design.md`, `03-plan.md`, `02a-spec-review.md`
  and `06-review.md`, the Session lines of the last two, the runner-path
  sentences of `02-spec.md` ("After the spec review") and `03-plan.md` (the
  card), the module docstring of `scripts/stage2.py`, and the new
  `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-rhq, and its last commit
  carries the trailer `Closes-Bead: coding-harness-rhq`
  (`prompts/07-commit.md`). It is a decision pull request (ADR 0008).
- Special runs: none. No real Codex, Claude Code or GLM call runs in the
  tests; the first real draft is a later change's.

## Open decisions

None open. Q-1 to Q-5 are answered (`decisions.md`). The points below are
reversible and bind nothing beyond this change, so this phase decided them;
each carries its reason.

- `[DETAIL]` **Phase 2a moves to Opus 5.5 for every change, not only for a
  drafted one.** Q-1 asked which review phases move to a Claude model and
  answered "2a"; after this change every framework spec is drafted by Codex
  or GLM, and where Stage 2 is off no foreign reviewer runs anyway. A spec
  Opus wrote by hand is then reviewed by the same model in a fresh context —
  the cost §3 already records for a spike.
- `[DETAIL]` **Phase 6 starts a fresh Codex session.** It is the only reading
  of Q-1 left: the 2a session is Opus's, and resuming Codex's drafting thread
  would give the code reviewer its own draft's reasoning. The runner's
  existing path already starts fresh and says so (`review`, `recorded is
  None`); a change reviewed before this change still resumes (criterion 31).
- `[DETAIL]` **`spec-review` stays a runner verb, now on Opus 5.5 through
  Claude Code.** The prompt is then the 2a prompt in full and nothing the
  orchestrating session read while checking the draft (Q-4); the rows keep
  the runner's form, which `scripts/stage2_runs.py` counts, and the verb runs
  unattended.
- `[DETAIL]` **Effort `xhigh` for the Opus spec review.** It is the effort the
  repository gives its highest-demand phases (§3); Q-2 chose the strongest
  review.
- `[DETAIL]` **"GLM 5.3" is `glm-5.3`, not `glm-5.3-flash`.** The repository
  calls `glm-5.3-flash` "GLM 5.3 Flash" throughout, the declaration lists
  `glm-5.3` beside it, and the open change stage2-repair (bead
  coding-harness-g2f) names `glm-5.3` "GLM 5.3". One constant changes it.
- `[DETAIL]` **A failed call also gets the Codex repair attempt.** The stated
  reading of Q-5 is one Codex attempt, one Codex repair, then GLM 5.3; a
  failed call is one of Q-5's three failure kinds, so it moves along the same
  chain. Unlike `implement`, a dead call is not the end of the run, because
  Q-5 names "Codex unreachable" as a reason for the fallback.
- `[DETAIL]` **The one red `make verify` a draft accepts is this change's own
  missing ADR answer** (criterion 13). Only the maintainer's stated answer may
  create that file, and the orchestrating session records it after reading
  the spec's proposal (`decisions.md`, second agent detail); refusing every
  feature draft would stop the verb for the class it is most for. Every other
  red gate, and another change's missing answer, still fails the attempt.
- `[DETAIL]` **`decisions.md` is put back although it is in the change
  folder** (criterion 9). It holds the maintainer's answers, and the gate
  `interview-minimums` counts records it cannot attribute; a drafter's
  `[DECISION]` goes into the spec's "Open decisions" instead. This narrows
  Q-3's "the change folder", it does not widen it.
- `[DETAIL]` **The 2a rows are worked in by a second `draft` run.** The
  author works them in (`prompts/02-spec.md`, "After the spec review"), and
  the author is the drafting model; Q-1 accepted that Codex stands on both
  sides of the change. An `[AMBIGUITY]` row goes to the maintainer first, and
  the orchestrating session puts the answer into `decisions.md` before that
  run.
- `[DETAIL]` **The GLM key is read only when the GLM attempt is due**
  (criteria 23 and 24). A Codex draft that passes never needs it, and
  `implement`'s up-front refusal would stop a draft whose Codex attempts had
  not run yet.
- `[DETAIL]` **A moved `HEAD` stops the run without a rewrite** (criterion
  11). Resetting a commit Codex made rewrites history; stopping leaves the
  decision to a person.
