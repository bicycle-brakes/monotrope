---
title: "ADR 0011 — The review loop runs through OpenCode Go, and ADR 0007's reviewer list is amended"
category: adr
status: accepted
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: opencode, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, opencode-go, reviews]
---

# ADR 0011 — The review loop runs through OpenCode Go, and ADR 0007's reviewer list is amended

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0007 (decisions 2 and 3);
  supersedes no ADR. Decision D-13 stands as ADR 0007 set it — no criterion
  of D-13 changes here.
* Review: the decisions the maintainer stated on 2026-10-07 in a Claude Code
  session (bead coding-harness-ymx: the review loop through OpenCode
  Go; round 2 on `mimo-v2.6-flash`; the entry declares `anbieter-erklaert`;
  the compatibility probe runs in phase 4 before the merge), narrowed on
  2026-10-08 to the review loop alone — the spec review and the review stay
  with Codex, after Codex's phase 6 found two real BLOCKERs in a change the
  loop had passed · the acceptance
  is the merge commit and is written nowhere else, so the header's `review`
  stays empty (ADR 0008) · Decider: maintainer · prepared by an opencode
  session
* Date: 2026-10-07, narrowed to the review loop on 2026-10-08 · takes effect on merge

## Context

* **ADR 0007** (accepted by the merge of pull request #60) sets where
  framework content may flow: to `openai-codex` through the official Codex
  CLI, and to `glm-coding-plan` through Claude Code — "Nothing else goes,
  and nowhere else". It gives the reviews to Codex and GLM: the spec review
  and the review to Codex, the loop between implementation and phase 6 to
  GLM, and, since 2026-10-06, exploration and implementation to GLM 5.3
  Flash.
* **The maintainer decided otherwise on 2026-10-07** (bead
  coding-harness-ymx): the review loop (4b) runs on
  OpenCode Go with a fixed ladder of three models for its rounds; on
  2026-10-08 the maintainer put the ladder to the loop alone — the spec
  review and the review stay with Codex, because Codex's phase 6 found two
  real BLOCKERs in a change the loop had passed, as on every change of the
  night run. Without this record the
  runner's declaration of `opencode-go` would run against ADR 0007's
  decision 2, which is a decision nobody made.
* **What OpenCode Go is** (research §E to §K, read 2026-10-07): OpenCode
  (Operator Anomaly Innovations, Inc.) sells OpenCode Go by subscription
  with a Go key; the vendor documents Claude Code as the way in and says no
  custom-header wrapper is needed for it; three model ids are served —
  `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`. The Go page
  lists them under `https://opencode.ai/zen/go/v1/chat/completions` only,
  while the Anthropic-compatible address
  `https://opencode.ai/zen/go/v1/messages` is the one Claude Code needs —
  whether it accepts the three ids is measured, not assumed (below).
* **The class does not change.** What may be sent stays the `framework`
  class of `model-endpoints.yaml`: rules, templates, process, tests.
  Customer code and customer rows go to neither endpoint, and the leak check
  before every call is what blocks them (unchanged from ADR 0007).

## Decision

1. **Framework content may also go to `opencode-go`** — through Claude Code,
   which the vendor lists as a supported tool, with the three ids below.
   The review loop (4b) only. The sentence of ADR 0007 decision 2 that closes with "Nothing else
   goes, and nowhere else" now closes with Codex, Z.ai's GLM and OpenCode
   Go; nothing else goes, and nowhere else. Customer code and rows go to
   none of the three.
2. **The loop's reviewer role moves.** The loop leaves GLM for the ladder;
   the spec review and the review stay with Codex exactly as ADR 0007 set
   them (the maintainer, 2026-10-08), and phase 6 keeps resuming the
   phase-2a session. Codex and GLM remain declared endpoints for what still
   routes to them — explore and implement stay on GLM 5.3 Flash.
3. **The ladder is data, not code.** Round *n* of the loop calls
   `modelle[n-1]` of the `opencode-go` entry: round 1
   `deepseek-v4.1-flash`, round 2 `mimo-v2.6-flash`, round 3
   `mimo-v2.6-pro`. Rounds 1 and 2 both run, each still held by an undecided
   row; round 3 starts only when round 2 wrote at least one row whose status
   begins `taken`. The loop runs at most three rounds. Reordering the list is
   a one-line pull request that touches `model-endpoints.yaml` and nothing
   else.
4. **The unconfined reads accepted for ADR 0007's reviewers extend to the
   rungs.** The prompts ask the model to read nothing outside the worktree
   and the repository's git directory — a request, not a lock — and the
   maintainer accepted that residual risk for reviewers on 2026-09-30.
   It reaches the three rungs by this record.
5. **The key stays in the runner.** It is read from the secrets file at call
   time, reaches the call only in its environment as `ANTHROPIC_AUTH_TOKEN`
   and `ANTHROPIC_API_KEY`, never appears in an argument, and an OpenCode Go
   call carries no other endpoint's key.
6. **The address is measured before anything builds on it.** Three calls, one
   per rung, run through the runner in phase 4 of the change that carries
   this record — declaration and leak check in front of each, as one special
   run whose commits are named in the pull request body. That is the only
   content leaving before the merge, and the maintainer accepted it on
   2026-10-07. If the address refuses an id, the run stops and reports it:
   no second address, no second design, no substituted model.

## Options considered

* **Keep Codex and GLM in every review role (chosen against for the
  loop).** The maintainer kept Codex for the spec review and the review on
  2026-10-08, but the loop runs the ladder his decision names; keeping GLM
  there would not meet it.
* **An OpenCode product other than Go.** Zen serves other models over its
  own addresses, and Go Plus is the second Go plan with higher monthly
  caps; either keeps the launcher and changes only the billing. Chosen
  against: the maintainer named Go, and the entry's billing and limits are
  the Go plan's — another product needs its own entry and its own terms.
* **OpenCode's own CLI as the launcher.** Symmetric with today's Codex CLI —
  a binary, an ask rule, a resumable thread — but the vendor documents
  Claude Code, and an own integration reopens the subscription-coverage
  question `model-endpoints.yaml` records for Z.ai.
* **The model of round 2.** `mimo-v2.6-pro` in round 2 and again in round 3
  would give the third round nothing new over the second; the maintainer
  answered "runde 2 flash" on 2026-10-07 (`decisions.md`, `[DECISION] 1`),
  so round 2 is `mimo-v2.6-flash`.
* **The OpenAI address instead of the Anthropic one.** The vendor lists it
  too; it is kept as a remark and measured, never as a path, because a
  fallback is what criterion 17 forbids.
* **Reviewer per phase written as code.** A model id as a literal in
  `scripts/stage2.py` would make every reordering a code change with tests
  to match — the opposite of what the decision asks for.

## Consequences

* **Nothing leaves before the merge except the probe.** The three probe calls
  of phase 4 are the only foreign calls of the change, and the maintainer
  accepted them explicitly on 2026-10-07; every other call is a stage-2 run
  after the merge. Until then `main` routes as ADR 0007 says: spec review and
  review on Codex, the loop on GLM, exploration and implementation on GLM 5.3
  Flash, and this change's own review runs on Opus 5.5.
* **A rule, not proof, at two places.** The address accepting the three ids
  is measured once, in phase 4; a refusal found later stops that run
  (criterion 17) instead of opening a second design. And which model a round
  calls is held by a test that reorders a fixture's list — a review of the
  list itself is what keeps a wrong order from shipping.
* **The continuity chain stops at ADR 0007.** This record amends ADR 0007,
  not decision D-13: D-13's criteria (three measured stage-2 runs,
  lakeswitch-ai's disclosure decision, a green leak check in every run, a
  declared endpoint with its residency) are untouched here, and the endpoint
  list is ADR 0007's text. The map in `scripts/check_decision_continuity.py`
  therefore gains nothing, and the D-13 row of the target document says the
  same thing it said. This is a `[DETAIL]` of this design; the reason is in
  this sentence's first half and is reversible.
* **Data use and terms.** The Go key sits in the secrets file and reaches the
  child process's environment only. The entry declares `anbieter-erklaert`
  because the Go page gives no region, `opencode.ai/privacy` returned 404 on
  2026-10-07 and the vendor's Zen page states US and EU for its models — the
  provider explains the residency, and the measurement stays open as a
  `[GAP]` of `spec.md`.
* **The runner's shape.** `run_codex` and the Codex tuple stay for the spec
  review and the review, and the loop's calls are Claude Code launches; the
  ask rule on a directly typed `codex` and `.claude/settings.json` stay as
  they are — a non-goal of this change and the subject of bead
  coding-harness-amp.
* **The resume stays where it was.** Phase 6 resumes the Codex thread of
  phase 2a; a thread that cannot be resumed starts a fresh session and says
  so in `findings.md` (criterion 9).

## Validation

* `python3 -m pytest tests/test_stage2.py tests/test_model_endpoints.py -q`
  green: the runner launches `claude` with the address, the rung and effort
  `max` and the settings of criterion 8 for the loop's rounds, and `codex
  exec` pinned as on main for the spec review and the review; the
  ladder round *n* → `modelle[n-1]` holds in a reordered fixture; three
  rounds are the limit and round 3 only after a taken row; the 30-minute
  limit is one constant and a stand-in that outlasts it is stopped; the key
  is in no argv, no print and no record; a red leak check exits 2 with
  nothing written.
* `make verify` green, and `scripts/touch_map.py origin/main HEAD` naming no
  protected area: `docs/adr/` gains only this file, `scripts/leakcheck.py`,
  `scripts/harness.py`, `scripts/touch_map.py`,
  `scripts/check_decision_continuity.py`, `scripts/new_change.py`,
  `docs/architecture/`, `ROADMAP.md`, `.claude/settings.json` and
  `model-endpoints.yaml`'s German keys are untouched.
* The three probe commits named in the pull request body, each with its
  rung's id and the answer's first line.
