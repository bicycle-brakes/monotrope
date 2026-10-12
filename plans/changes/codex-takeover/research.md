---
title: "Research — codex-takeover"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-nsm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, codex, cost]
---

# Which workflow tasks Codex can take over — Research

Phase 1 for bead coding-harness-nsm, read against `origin/main` on
2026-10-12. The maintainer asked (2026-10-12) which tasks of the seven-phase
workflow, and of the orchestration around it, can move from Claude to Codex
to save Claude tokens. Today Codex runs only spec-review (phase 2a) and
review (phase 6) through `scripts/stage2.py`. The maintainer wanted Codex to
research this; the runner has no Codex research verb (ADR 0007), so GLM
explores through the explore verb and the answer is checked by the
orchestrating session. A related feature bead covers a repair verb for GLM
(coding-harness-g2f).

## Questions for the exploration

1. Which tasks does Claude do today, per phase and around the phases, as the
   repository records them (`docs/WORKFLOW.md`, `prompts/`, `AGENTS.md`,
   `model-endpoints.yaml`, `scripts/stage2.py`): spec and plan writing,
   orchestration, repairs of review findings, pull-request review, tracker
   hygiene, handover drafts, commit and PR text.
2. For each: could Codex do it under the repository's rules (ADR 0007 leak
   check and runner-only start, ADR 0008 maintainer decisions, ADR 0011
   review loop, house rules in `AGENTS.md`)? What would the runner need (a
   new verb, a write scope, a session), and what must stay with Claude or the
   maintainer (interviews, ADR answers, merges, tracker writes)?
3. What does the repository say about Codex's limits and cost today (the
   `openai-codex` entry in `model-endpoints.yaml`, data residency, plan
   limits, measured runs in findings files and `scripts/stage2_runs.py`)?
4. Which candidates give the largest saving for the smallest rule change,
   ranked, with the files each would touch.

This file stops at the findings; a decision on any candidate is the
maintainer's.

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 347 files, 863 commits, 12 rules.

## Runner exploration — 2026-10-12

*Note by the orchestrating session (2026-10-12): GLM's answer opened with a German preamble and a rule, both removed (house rule 1). The text below is unchanged.*

### What exists today

**The seven phases and who runs them.** `docs/WORKFLOW.md` §3 ("Model routing") and §4 ("The routing") fix the allocation. On Anthropic today: phase 1a interview (Opus 5.5; only records with `answered_by: maintainer` count, `prompts/01a-interview.md`, gate `scripts/check_interview_minimums.py`), phase 2 spec, 2b design and 3 plan (each Opus 5.5 at effort `xhigh`, `prompts/02-spec.md`, `02b-design.md`, `03-plan.md`), phase 5 verify (deterministic, no model, `prompts/05-verify.md`), phase 7 commit (Haiku 4.5, `prompts/07-commit.md`, which also holds "The merge": merge only on the maintainer's request, restated, `gh pr merge --match-head-commit`). Already off Claude: phase 1 explore on GLM 5.3 Flash (`scripts/stage2.py` function `explore`, read-only tools `WORK_READ_TOOLS`, appends `## Runner exploration` to `research.md`), phase 2a on Codex (`spec_review` → `run_codex`, a fresh session), phase 4 implement on GLM Flash (`implement`: file tools but no shell; the runner itself runs `make verify`, checks the `## Time used` log and makes the checkpoint commit as `stage2-runner`), phase 4b on the ladder through Pi (`review_loop`, `ladder()` reading the `modelle` order of the `opencode-go` entry), phase 6 on Codex (`review`: resumes the 2a thread, writes the verdict, then `release()` and a resumed loop-marks call). A `spike` gets no stage-2 review at all (`docs/WORKFLOW.md` §4, "Which change gets what"); explore and implement are not routed by class.

**What Claude does around the phases**, as the repository records it: orchestration of the runner verbs and the loop-row decisions (`taken`/`rejected` under the evidence rule, `prompts/04b-review-loop.md` "For the implementer"); every `[DECISION]` and `[AMBIGUITY]` to the maintainer (question protocol, `docs/WORKFLOW.md` §2; the appetite answer *continue* only from the maintainer, `prompts/04-implement.md`); handover files at session end (`docs/WORKFLOW.md` §2 "The eighth movement", `templates/handover.md`); commit and pull-request text plus the generated touch map (`prompts/07-commit.md`, `scripts/touch_map.py`); tracker hygiene after a merge (`make close-merged ARGS=--write`, `prompts/07-commit.md`; one-writer rule, `AGENTS.md` house rule 4); ADR answers (`scripts/harness.py decide adr`, maintainer-only, `docs/WORKFLOW.md` §2). The maintainer's own display (status line, `/handover`) lives in `tools/claude-code/` (`README.md`, `statusline.sh`).

**The runner** (`scripts/stage2.py`): eight verbs (`VERBS` plus `session`). Every call passes `preflight` — change folder exists, the phase artefact carries a `bead`, `declaration_problem` clears `model-endpoints.yaml` — then `checked_prompt` runs `scripts/leakcheck.py` in-process immediately before the call, and `begin_call`/`begin_work_call` writes the audit line into the phase artefact. Codex is pinned in `CODEX = ("openai-codex", "gpt-6.1-sol", "max")` and launched by `run_codex` as `codex exec`, first or resumed, with `sandbox_mode="read-only"`, hooks and memories disabled, the session kept via the `thread.started` event and `exec resume`. The child environment is an allow-list (`ENV_ALLOW`, `foreign_env`); `.claude/settings.json` asks before a bare `codex` (`Bash(codex *)`, held by `codex_rule_problems`). `--stage2-off` exists for explore and implement only.

**Codex already works beyond the two reviews in one place:** the `session` verb (ADR 0012) starts an interactive Codex in the change's dedicated worktree with workspace-write and approval on request (`scripts/stage2_session.py` — not read in this session; facts from ADR 0012 and `docs/WORKFLOW.md` §4, "The interactive session"). And a Codex-authored draft already lives in the tree: `plans/changes/stage2-session/adr-0007-session-amendment.md` carries `produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}`, confirmed by ADR 0012's review line ("the first draft was written by Codex on 2026-10-07").

**What the repository measures about Codex.** `docs/research/2026-10-08-stage2-three-runs.md`: across the first four stage-2 runs, Codex's phase 6 produced 13 BLOCKERs the loop had not raised; one disagree mark per run (the fourth run marked all seven rows, each reason saying the row was resolved); 24 of 24 recorded calls ran behind a clean leak check. The same note states, twice, that tokens and cost per vendor are not recorded by the runner — as does the docstring of `scripts/stage2_runs.py`, which counts rows and calls, never tokens. The recorded reason the loop lost its reviewer role while Codex kept 2a and 6 stands in ADR 0011 (Context and decision 2: Codex's phase 6 found two real BLOCKERs in a change the loop had passed; maintainer, 2026-10-08). Why the expensive models sit where they sit is recorded in §3's table: spec, plan and review carry effort `xhigh`/`max` because "an error here is the most expensive", while the token-heavy phases moved to Flash.

**Codex cost and limits as declared.** The `openai-codex` entry of `model-endpoints.yaml`: the ChatGPT subscription, official Codex CLI only ("any other way in is not covered"), `darf_sehen: [framework]`, `residenz: anbieter-erklaert`, personal-plan data processed and stored in the US with no region choice (read 2026-09-30), personal-use declaration of 2026-09-30 with three renewal conditions, and the account's "Improve the model for everyone" switched off. The entry records no price and no usage ceiling; a grep over `plans/` for cost, token and USD terms found no Codex figure anywhere — the only price list in the tree is the `opencode-go` entry.

**The rules a wider Codex role runs into.** ADR 0007 decisions 1–5 (runner-only start; leak check and declaration on every call; the `framework` data class only; unconfined reads accepted as residual risk; the three-run stop rule that can send reviews back to Opus 5.5). ADR 0011 decision 2 fixes today's allocation as a maintainer decision ("the spec review and the review stay with Codex"), so moving them is a new decision, not a build step. ADR 0012 covers interactive sessions and states the runner does not verify Codex's sandbox. ADR 0008 with `provenance.yaml`: `docs/adr/`, `decisions/answers/`, `.claude/rules/`, `docs/governance/quality-gates.md` and `regelwerk.md` are `human-decided` — a change there is a decision pull request (`decide(<scope>): …`, label `decision`). `AGENTS.md` house rules 4 and 8 bound tracker writes and merges. Each prompt carries its own `**Model:**` line, so any re-route edits `prompts/` too.

**Adjacent work already in flight** (recorded, not this change): bead coding-harness-rwa — GLM 5.3 through Pi for explore and implement, with the exact file list a decision pull request would touch (`docs/research/2026-10-11-glm-through-pi.md`); bead coding-harness-g2f — a repair verb for GLM (named in this file's frame; the tracker itself was not readable in the exploring session).

**Verified absent in this tree** (as the header note of `docs/WORKFLOW.md` already records): `.claude/commands/`, `.claude/hooks/`, the sub-agent definitions `explorer.md`/`reviewer.md` (`.claude/agents/` holds seven unrelated definitions), the `make change` and `make index` targets (the entry is `python3 scripts/new_change.py`), and any runner script for job prompts — `prompts/research-recheck.md` expects one that picks its note from `scripts/check_research_currency.py --format json`, and no such script exists under `scripts/`.

### What is unclear (open questions, not guesses)

- The full text of bead coding-harness-nsm: not read — the tracker is a Dolt database and this session had no tracker access; only this file's frame and the `plans/INDEX.md` row (draft, 2026-10-12, bead coding-harness-nsm) describe the change.
- Usage limits or a cost ceiling of the ChatGPT plan behind `openai-codex`: not recorded anywhere in the tree.
- Whether a headless *writing* Codex phase is possible and safe: `run_codex` pins `sandbox_mode="read-only"`; ADR 0012 records workspace-write only for the interactive session verb and states the runner does not verify Codex's sandbox. Nothing in the repository measures a headless write run.
- Whether the Codex CLI can fetch the web, which a `prompts/research-recheck.md` run would need: not recorded in the repository.
- Files present but not read in this session: `scripts/stage2_session.py`, `scripts/check_interview_minimums.py`, `scripts/leakcheck.py`, `decisions/gates.yaml`, `docs/research/2026-10-08-explore-swarm-proposal.md`, `plans/changes/stage2-session/findings.md`. Statements about them above come from `docs/WORKFLOW.md`, the ADRs, or their listing in a glob.
- The working-tree modification of this file, as read here, is the frame plus this run's own audit line ("Stage-2 call, 2026-10-12: explore · attempt 1 · route flash …"), which `begin_work_call` writes before the call; no other text differs from the committed frame as far as this read shows.

### Which files a change would have to touch

- A new or changed Codex role: a verb or tuple in `scripts/stage2.py` (`VERBS`, `CODEX`, `run_codex`, `phase_prompt`/`work_prompt`), `tests/test_stage2.py`, the routing rows in `docs/WORKFLOW.md` §3/§4, and the `**Model:**` lines of the affected `prompts/*.md`.
- A wider Codex scope amends ADR 0007 (its decision 2 names what may flow where) as a new file under `docs/adr/` in a decision pull request, following the pattern of ADR 0011 and 0012; reviewer moves additionally touch the `openai-codex` remark in `model-endpoints.yaml`.
- A repair verb for the implementer's loop rows: no verb exists today (`VERBS` has none); the work is already framed as bead coding-harness-g2f.
- A job-prompt runner for `prompts/research-recheck.md` has no script to extend; it would start beside `scripts/check_research_currency.py`.
- A Codex-side surface for the maintainer's display has no counterpart in `tools/claude-code/`; that directory is Claude-Code-specific by construction.


*Note by the orchestrating session (2026-10-12): a German closing remark was removed (house rule 1). Question 4, a ranking of candidates by saving and rule change, is not answered above; it is open for the next session.*

## Ranking of candidates (question 4) — orchestrating session, 2026-10-12

Written by the orchestrating Claude Code session from the findings above, not
by the runner. No candidate can be ranked by measured saving: the runner
records no tokens for any vendor (`scripts/stage2_runs.py`,
`docs/research/2026-10-08-stage2-three-runs.md`), and no Claude figure per
phase is recorded either. The order below is by the size of the Claude work a
candidate removes, as the routing table describes it, against the size of the
rule change it needs. A decision on any of them is the maintainer's.

| # | Candidate | Claude work it removes | Rule change it needs | Files |
|---|---|---|---|---|
| 0 | Measure first: the runner records tokens per call, for every vendor | none by itself; it turns every row below from a guess into a figure | none (no routing moves) | `scripts/stage2.py` (call log), `scripts/stage2_runs.py`, `tests/test_stage2.py` |
| 1 | Repairs of taken review rows move off Claude | the Sonnet repair sub-agents of every review loop and phase 6 | a repair verb; GLM is already framed for it (bead coding-harness-g2f); Codex would need a writing headless call, which `run_codex` does not allow (`sandbox_mode="read-only"`) and an ADR 0007 amendment | `scripts/stage2.py`, `tests/test_stage2.py`, `prompts/04b-review-loop.md`, `docs/WORKFLOW.md` §4 |
| 2 | Draft spec and plan in a Codex interactive session, Claude checks | the largest single Claude cost per change (phases 2, 2b, 3 at effort `xhigh`) | none to start the session (ADR 0012); but Codex then reviews its own spec in phase 2a, which removes the independence ADR 0011 decision 2 relies on — a maintainer decision and a routing change in `docs/WORKFLOW.md` §3 | `prompts/02-spec.md`, `prompts/03-plan.md` (`**Model:**` lines), `docs/WORKFLOW.md` §3/§4, an ADR amending 0007/0011 |
| 3 | Commit and pull-request text, handover drafts | small: phase 7 already runs on Haiku 4.5 | a new Codex verb for a writing call | `scripts/stage2.py`, `prompts/07-commit.md` |
| — | Stays with Claude or the maintainer | orchestration (the session itself), the interview (1a), ADR answers, merges, tracker writes | — | — |

Reading: candidate 0 is the precondition for judging the others and changes no
rule; candidate 1 is the largest saving for the smallest rule change, and it
is already a bead (coding-harness-g2f) on GLM, without Codex; candidate 2
saves the most but trades away the independent spec review.
