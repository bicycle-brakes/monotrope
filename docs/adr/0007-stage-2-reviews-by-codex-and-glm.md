---
title: "ADR 0007 — Codex and GLM work on framework content, and decision D-13 is amended"
category: adr
status: accepted
created: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-10-07
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---

# ADR 0007 — Codex and GLM work on framework content, and decision D-13 is amended

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open is
  proposed, closed is rejected. Amends decision D-13 of the 2026-09-16
  interview; supersedes no ADR.
* Review: the decisions the maintainer stated on 2026-09-30 while answering the
  interview of `plans/changes/stage-2-codex-glm/` (`decisions.md`, answers 1, 3,
  4, 5, 10, 11 and 14), and the routing decisions the maintainer stated on
  2026-10-06 in a Claude Code session (bead coding-harness-bib: no Fable,
  explore and implement on GLM 5.3 Flash, a bounded change's reviews to Codex,
  the leak check kept) · the acceptance is the merge commit and is written
  nowhere else, so the header's `review` stays empty (ADR 0008) · Decider:
  maintainer · prepared by a Claude Code session
* Date: 2026-09-30, widened on 2026-10-06 before the merge · takes effect on
  merge

## Context

Decision D-13 of the 2026-09-16 interview (`docs/architecture/target-architecture.md`
§9.1, carried forward as "Retain" by the current target document) sets four
measured criteria before any other vendor sees a change: at least three full
seven-phase runs with metrics in this repository; lakeswitch-ai's disclosure
decision written; a green leak check in every run; the foreign reviewer's
endpoint declared with its residency. The implementation plan adds that every
criterion holds "even in an optional trial".

On 2026-09-30 the four stood like this (`research.md` §4 of the change):

* **Three measured runs:** not met. The measurement (a tracker item) waits on
  a template bundle and on a metrics generator that does not exist.
* **lakeswitch-ai's disclosure decision:** not found and not read in that
  repository; by its wording it concerns lakeswitch-ai's own content.
* **A green leak check:** not possible. `make leakcheck` was a stub that printed
  a message and exited 1.
* **A declared endpoint with residency:** met for GLM, not for Codex.

The same day the maintainer decided the routing: Codex reviews the spec (2a)
and the code (6), the same agent for both; GLM reviews in a short loop between
implementation and phase 6; Sonnet 5.5 implements; Kimi is dropped; framework
content only. Without an amendment that routing would run against D-13.

**Widened on 2026-10-06, before the merge.** The maintainer then decided four
more things, in a Claude Code session (bead coding-harness-bib):

* **No Fable.** Opus 5.5 takes the places of Fable 5.1 — the interview, the
  escalation and the fallback below — and a `bounded` change's stage-2 reviews
  (the spec review where one is held, and the review) go to Codex.
* **Implementation runs on GLM 5.3 Flash** (`glm-5.3-flash`, the Z.ai endpoint
  already declared) once stage 2 is live, instead of Sonnet 5.5.
* **Exploration runs on GLM 5.3 Flash too**, instead of Haiku 4.5.
* **The leak check stays**, asked about and kept that day.

That changes what leaves Anthropic. A review reads one diff and one spec;
exploration reads the repository broadly, and implementation reads the tree
and writes its code. Both phases are therefore inside the scope below, and
this ADR no longer keeps phases 1 and 4 with Anthropic.

## Decision

1. **D-13 is amended for framework content.** Criteria 3 and 4 stay, and the
   runner (`scripts/stage2.py`) enforces them on every call: a green leak check
   immediately before the call, and a declaration in `model-endpoints.yaml`
   that clears the endpoint, the model and the data class — on a call of
   explore or implement as on a call of a review. Criterion 2
   governs lakeswitch-ai's content, which this repository never sends;
   lakeswitch-ai's disclosure decision stays that repository's to write.
   Criterion 1 is replaced by measuring the first three stage-2 runs, each
   finding recording its reviewer, whether it was taken and whether it broke a
   test, with a stop rule: after the third run, if at least one taken Codex or
   GLM finding broke a test, stage 2 falls back to Opus 5.5 — Opus 5.5 reviews
   every change, and phases 1 and 4 return to Haiku 4.5 and Sonnet 5.5 — until
   the maintainer decides again (`docs/WORKFLOW.md` §4). **The accepted loss is
   the measured stage-1 baseline** before the first foreign call.
2. **Where framework content may flow.** This repository's tree — the class
   `framework` of `model-endpoints.yaml`: rules, templates, process, tests —
   may go to `openai-codex` through the official Codex CLI, and to
   `glm-coding-plan` through Claude Code: the reviews to Codex and GLM, and,
   since 2026-10-06, exploration and implementation to GLM 5.3 Flash, which
   read the repository broadly and write code into the worktree. Far more of
   this repository goes to Z.ai than the review loop alone sends. Nothing else
   goes, and nowhere else. Customer code and rows go to neither endpoint.
   LakeSwitch and customer content never go, to any endpoint; the leak check
   before each call is what blocks them. lakeswitch-ai's own trees are not
   sent, and their disclosure decision (D-13, criterion 2) stays theirs.
3. **Kimi is dropped, and so is Fable.** Kimi leaves the declared endpoints and
   stands under `ausgeschlossen` with the date of 2026-09-30. Fable 5.1 leaves
   the routing (2026-10-06); Opus 5.5 takes its places, the fallback of
   decision 1 included.
4. **The reads of the foreign models are not confined.** They can read the
   whole disk, the customer instance's checkout included. The prompts ask them
   to read nothing outside the worktree and the repository's git directory — a
   request, not a lock, and the doctrine says so in those words. The
   maintainer accepted this as a residual risk on 2026-09-30, choosing it over
   a proof of about one hour's work, for the reviewers. Explore and implement
   widen what is read and add writes; whether that acceptance reaches them is
   for the maintainer to confirm by merging this pull request.
5. **Explore and implement run on GLM 5.3 Flash — decided, not built.** They
   run there for every change, whatever its class: the class is stated in the
   spec, after exploration. The runner (`scripts/stage2.py`) has no verb for
   either phase yet, no plan marking assigns a step to Flash, and no effort is
   set for it. Until that is built, `docs/WORKFLOW.md` §3 runs the two phases:
   Haiku 4.5 explores and Sonnet 5.5 implements. This is an open item of the
   change, not a claim that it works.

## Options considered

* **Amend D-13 (chosen).** The two criteria that protect data stay hard and are
  enforced rather than written; the two that measure readiness are answered in
  substance by the maintainer's routing. Real calls start after the merge; the
  cost is the missing baseline.
* **Build now, switch on later.** Everything built and tested offline; no real
  call until three measured runs and the disclosure decision exist. The
  capability would then wait on the template bundle and on a metrics generator
  that has no date.
* **Reviews only, as this ADR first stood.** Nothing but specs and diffs go to
  Z.ai, and exploration and implementation stay with Anthropic. Set aside by
  the maintainer on 2026-10-06, who widened the routing.
* **Run without touching D-13.** The architecture documents and the practice
  would contradict each other, which is a `[DIVERGENT]` finding at review and a
  decision nobody made.

## Consequences

* **Nothing leaves before the merge.** Until this pull request is merged, D-13
  stands unamended and no call runs with content from its worktree. The first
  real call is the first stage-2 run after the merge, which is also run 1 of
  the three; a runner fault found there is a follow-up fix, not a reason this
  ADR did not hold. While the pull request is open the routing on `main` stays:
  spec review and review on Opus 5.5, exploration on Haiku 4.5 and
  implementation on Sonnet 5.5; this change's own review runs on Opus 5.5.
* **A rule, not proof, in two places.** The ask rule on a bare `codex` is a
  brake that another spelling passes. Which change class a change has is
  checked by nobody: a `feature` stated as a `spike` skips every stage-2
  review, and one stated as `bounded` may skip the spec review, which is
  optional there; the review before the merge is what catches either.
* **More leaves than reviews.** Explore and implement send the repository's
  tree and code to Z.ai, and a model there writes code that this repository
  then merges after Codex and GLM have read it. The leak check, the declared
  endpoint, `make verify` after each repair and the review before the merge
  are what stand between that and a customer's content or a wrong change; none
  of them measures what Flash does to the code; the rule of decision 1 sees it
  only through the findings the reviewers raise.
* **Data use and use terms.** The ChatGPT subscription behind Codex is declared
  personal use on 2026-09-30 with the same three expiry conditions as GLM's,
  and the account's setting "Improve the model for everyone" is off, as the
  maintainer stated that day (`model-endpoints.yaml`). OpenAI states that it
  processes and stores personal-plan data in the United States and wherever its
  affiliates and service providers are, and personal plans get no region
  choice.
* **The continuity chain.** The gate `decision-continuity` maps D-13 to this
  ADR; the D-13 row of the target document now reads "Amend" and points here,
  and both architecture documents that set D-13's criteria carry a dated note.
* **It does not enter M2.** M2, the Omnigent milestone for cross-vendor
  operation, has further entry conditions — the Omnigent topology, lakeswitch-ai's
  adoption — that nobody was asked about. The runner is not wired into
  Omnigent; the reviewers run as separate command-line processes.
* **Beyond D-13.** The same pull request carries changes that follow from other
  answers of the maintainer and need no ADR of their own: Sonnet 5.5 for
  implementation until Flash can be started (the interim, in every change), the
  evidence rule for foreign findings, and one condition per acceptance
  criterion. Opus 5.5 in place of Fable 5.1 outside stage 2 is on `main`
  already (pull request #87).

## Validation

* `python3 scripts/check_decision_continuity.py` is green with `"D-13"` in its
  map and this ADR naming D-13.
* `tests/test_stage2.py` and `tests/test_leakcheck.py` are green: the runner
  refuses without a clean leak check and a clearing declaration, and the leak
  check reports the place of a match and never the match. The same tests hold
  the routing of this amendment: GLM 5.3 Flash on phases 1 and 4, a `bounded`
  change's reviews on Codex, no Fable in a routing row or a prompt, and the
  statement that the two Flash rows are not built.
* After the third stage-2 run, the evaluation under `docs/research/` is written
  and read by the maintainer.
