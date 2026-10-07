---
title: "Spec — stage2-flash-runner"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-qcp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, glm, runner]
class: bounded
---

# Spec — stage2-flash-runner

Add the two missing Stage-2 work verbs: GLM 5.3 Flash explores a change and
implements its accepted plan through the same declared endpoint and leak
barrier that already guard the GLM review loop. Inputs are
[`research.md`](research.md), [`decisions.md`](decisions.md), ADR 0007 and the
existing runner, read at `0dcf65a`.

The class is `bounded`: ADR 0007 already fixes the two models and phases, and
the maintainer's answers in `decisions.md` fix fallback and post-run checks.
This change extends the existing runner with that decided behaviour; it makes
no new external contract or architecture choice.

## Problem

Stage 2 is active for framework content, but its runner still starts only
Codex review and GLM review-loop calls. The routing table says that GLM 5.3
Flash explores and implements, while the operative text immediately below it
says those verbs are not built and sends both phases back to Stage 1. As a
result, an orchestrating session cannot lawfully give either phase to Flash:
calling `claude` directly would skip the endpoint declaration, the leak check,
the controlled environment and the audit line.

Implementation also needs a stronger completion boundary than a successful
model process. The maintainer requires the runner itself to show that the full
gate is green, the run produced a commit and the plan's time log moved. A
missing condition earns Flash one repair attempt; after that Sonnet 5.5 takes
over. A leak-check refusal is different: no model starts and no fallback may
hide it.

## Terms

- **Flash route** — Claude Code against endpoint `glm-coding-plan`, model
  `glm-5.3-flash`, using `GLM_KEY` and the Z.ai base URL.
- **Stage-1 route** — Haiku 4.5 for explore and Sonnet 5.5 at effort `medium`
  for implement, using the maintainer's normal Claude Code authentication.
- **Attempt** — one model process started by one verb invocation. A retry and
  a fallback are separate attempts and each gets its own leak check and audit
  line.
- **Implementation baseline** — `HEAD` and the bytes below `## Time used` in
  `plan.md` immediately before the first implementation attempt; implement
  refuses pre-existing changes outside its own `findings.md`, so every later
  implementation change belongs to the run.
- **Post-run checks** — `make verify`, a new commit, the time-log change and a
  clean worktree after the attempt.

## Acceptance criteria

Each criterion states one observable condition and what refutes it. A fixture
means a temporary repository and stand-in programs; no automated test contacts
a model endpoint.

1. **The two verbs exist.** `python3 scripts/stage2.py explore <change>` and
   `python3 scripts/stage2.py implement <change>` are accepted alongside the
   four existing verbs; the help and module documentation name their phases,
   models, result and exit meanings.
   *Refuted by:* either command being rejected by argument parsing, or an
   existing verb disappearing.

2. **Explore can precede the spec.** Its preflight reads the bead from
   `research.md` and requires no `spec.md` or `plan.md`. Implement requires a
   readable `spec.md` and `plan.md`, and gets the bead from `spec.md`. Both
   refuse an invalid change name, a missing change folder or a missing bead
   before any model call.
   *Refuted by:* a fixture with only a valid `research.md` being refused by
   explore, or implement starting without either accepted artefact.

3. **The declared Flash route is pinned.** A normal attempt uses endpoint
   `glm-coding-plan`, model `glm-5.3-flash`, effort `max`, the Z.ai Anthropic
   compatibility URL and `GLM_KEY`; every GLM model environment variable is
   the Flash model, while `review-loop` remains on `glm-5.3`.
   *Refuted by:* a stand-in observing another model, endpoint, effort or model
   environment variable, or review-loop changing model.

4. **The declaration still decides.** Before every Flash attempt the runner
   requires the endpoint to exist, list `glm-5.3-flash`, allow `framework` and
   state a residency. A missing `GLM_KEY` refuses only a Flash attempt; it is
   not needed for an explicitly selected Stage-1 route.
   *Refuted by:* a planted declaration fault reaching `claude`, or
   `--stage2-off` refusing only because `GLM_KEY` is absent.

5. **Every attempt has a fresh leak barrier.** Immediately before each model
   process, `scripts/leakcheck.py` checks the change, tree, history and exact
   prompt. Exit other than clean refuses the verb with exit 2; that invocation
   starts neither its intended model nor a fallback, and writes no model
   output.
   *Refuted by:* a planted marker reaching a model, a retry reusing an earlier
   verdict, or any model call after a blocked check.

6. **Explore receives the phase, not review instructions.** Its prompt is
   `prompts/01-explore.md`, the change name, the current `AGENTS.md`, and a
   request to report repository facts with source paths for `research.md`; it
   contains neither the six-cell finding format nor implementation powers.
   The process has only `Read`, `Grep` and `Glob`, restricted to the worktree
   as the current review-loop call is.
   *Refuted by:* a stand-in seeing `ANSWER_FORMAT`, `Edit`, `Write` or `Bash`,
   or not seeing the phase prompt and agent rules.

7. **Explore preserves the artefact.** A non-empty answer is appended under a
   dated `## Runner exploration` heading in `research.md`, after an audit line
   naming verb, route, model and clean leak-check counts; existing research and
   YAML frontmatter remain byte-for-byte except `updated:`. An empty answer or
   failed process exits 1 and appends no answer.
   *Refuted by:* prior research being replaced, output going to `findings.md`,
   a blank answer succeeding, or a credential fragment appearing in the file.

8. **Implement receives the accepted job.** Its prompt includes
   `prompts/04-implement.md`, `AGENTS.md`, the complete `spec.md` and
   `plan.md`, the change name, the implementation baseline and the read
   boundary. It tells the model to implement only that plan, update
   `## Time used`, and leave verification, staging and the local checkpoint
   commit to the runner.
   *Refuted by:* any of these inputs or instructions absent from the stand-in's
   prompt.

9. **Implement has bounded write powers.** Claude Code starts restricted and
   in safe mode, with no project/user customisations or MCP servers, and only
   `Read`, `Grep`, `Glob`, `Edit` and `Write` in the worktree. It gets no
   `Bash`, other code-running tool, WebFetch, git operation or permission
   bypass; standard input is empty. The runner, outside the model process,
   owns every command: exactly `make verify` for testing and `git status`,
   `git diff`, `git add -A` and `git -c commit.gpgsign=false commit` for the
   baseline and checkpoint. There is no plan-dependent shell allow-list.
   *Refuted by:* the model argv naming a shell, network, MCP, git or bypass
   power; Edit or Write being absent; or the runner executing another
   plan-derived command.

10. **Success means the post-run checks hold.** Implement first refuses a
    worktree with a tracked or untracked change outside this change's
    `findings.md`; a previous attempt's audit line may remain there. After a
    model process exits zero with a non-empty answer, the runner itself runs
    exactly `make verify` with git signing disabled and requires exit 0 and
    changed bytes below the plan's `## Time used` heading.
    It then stages the run's changes, creates one local checkpoint commit
    `feat(<change>): implement accepted plan` with signing disabled, and
    requires: `HEAD` is a descendant of the baseline with exactly one new
    runner commit, and the worktree is clean. Only then does implement exit 0.
    *Refuted by:* any one condition planted false while the verb succeeds, or
    `make verify` being trusted only because the model said it ran it.

11. **One Flash repair, then Sonnet.** If the first Flash process succeeds but
    a post-run check fails, the runner gives the failure evidence to one fresh
    Flash attempt. If the checks still fail, one Sonnet 5.5 attempt at effort
    `medium` receives the same job plus both diagnostics. The verb succeeds
    only if a later attempt satisfies criterion 10; there is never a third
    Flash attempt or a second Sonnet fallback.
    *Refuted by:* no repair, more attempts, a repair without the diagnostic,
    or fallback success bypassing a post-run check.

12. **A failed model process is visible.** A non-zero process or empty answer
    exits the verb with 1 and its scrubbed error; it does not silently become a
    repair or fallback in the same invocation. The orchestrating session may
    diagnose Z.ai as unavailable and invoke the explicit Stage-1 route.
    *Refuted by:* a stand-in process failing and another model starting, or the
    verb returning 0.

13. **Stage 2 can be turned off explicitly.** `--stage2-off` on either new
    verb selects Haiku 4.5 for explore or Sonnet 5.5 at effort `medium` for
    implement on the first attempt; it performs the same prompt, leak, audit,
    output and post-run checks, but neither reads `GLM_KEY` nor sets the Z.ai
    URL. Existing verbs reject the flag rather than changing route.
    *Refuted by:* a Stage-1 stand-in seeing GLM credentials/base URL, the wrong
    model, or weaker checks.

14. **Fallback is recorded where the phase has an artefact.** Every Stage-1
    attempt records its reason and model. Implement writes the route line in
    `plan.md`. Explore writes it in `research.md`, because `plan.md` does not
    exist in phase 1; the plan prompt and documentation require that line to
    be copied into `plan.md` when phase 3 creates it. This is the concrete,
    phase-valid form of the maintainer's “record it in plan.md” decision.
    *Refuted by:* an explicit fallback leaving no durable line, or a generated
    plan after such an explore omitting the line.

15. **The runner owns credentials and output.** Both routes receive only the
    existing environment allow-list plus their route variables. GLM gets an
    empty configuration directory; Stage 1 gets normal Claude Code auth but
    safe mode and neither reads nor is expected to recognise `GLM_KEY`.
    On the Flash route, the full key and therefore every eight-character
    fragment of it are absent from stdout, stderr and runner-written audit or
    answer artefacts on success and failure. If the exact key nevertheless
    occurs in a regular file changed by the attempt, the runner replaces it
    with `[credential]`, refuses with exit 2 and starts no repair or fallback.
    Implementation files otherwise are not output-scrubbing targets; the
    model's no-shell tool boundary keeps the credential unavailable to them.
    *Refuted by:* an unrelated planted environment variable reaching a
    stand-in, configuration files loaded, a Flash stream or runner artefact
    retaining a key fragment, a changed file retaining the exact key, or a
    Stage-1 attempt reading the GLM secrets file.

16. **The audit tells attempts apart.** Each attempt has one line that names
    date, verb, attempt number, route, endpoint where applicable, model and
    clean leak counts. Explore keeps it in `research.md`; implement keeps it in
    `findings.md`. Existing Codex and review-loop audit lines remain readable.
    *Refuted by:* a retry/fallback not distinguishable from the preceding call,
    or an attempt without its line.

17. **The operative texts agree that the verbs are live.** `docs/WORKFLOW.md`,
    `prompts/01-explore.md`, `prompts/03-plan.md`,
    `prompts/04-implement.md` and `AGENTS.md` name the exact commands, Flash
    route, explicit Stage-1 fallback and leak-stop rule; the plan prompt says
    how an explore fallback reaches `plan.md`, and none says the two verbs are
    unbuilt. The phase-routing doctrine tests check these facts on planted
    copies.
    *Refuted by:* any operative text retaining the temporary Stage-1-only
    wording, or a planted model/command/fallback surviving its test.

18. **The existing runner is unchanged in meaning.** Spec review and review
    remain Codex `gpt-6.1-sol`; review-loop remains GLM `glm-5.3`, read-only and
    limited to two rounds; release-loop keeps its records. Their existing
    tests stay green, and the new tests contact no endpoint.
    *Refuted by:* an old `tests/test_stage2.py` case failing, an existing argv
    changing outside shared model-parameterisation, or a test call log naming
    a real executable.

19. **The repository is green and the live review route is exercised.** The
    phase gate named by the prompts, `scripts/validate_change_artefacts.py`,
    is not in this repository; its present stand-in
    `python3 scripts/plans_registry.py --check`, the Stage-2 unit tests and
    `make verify` pass. After implementation, one real Codex phase-6
    review and at least one real GLM review-loop attempt run through this
    runner; their audit lines and scrubbed outcomes are evidence in
    `findings.md`.
    *Refuted by:* a red command, either reviewer not called through the runner,
    or a credential in the evidence.

## Non-goals

- No unattended change orchestrator, spend cap or general retry framework.
- No change to the endpoint declaration, ADR 0007, the leak rules, the Codex
  session-resume protocol or the phase-4b loop record.
- No implementation on GLM 5.3 (non-Flash), no review on Flash, and no use of
  a direct model API outside Claude Code.
- No fallback from a leak refusal and no inference of “Stage 2 off” from an
  undeclared environment variable or a failed leak check.
- No migration of older change artefacts or retroactive model calls.
