---
title: "ADR 0011 — The review loop runs through OpenCode Go, and ADR 0007's reviewer list is amended"
category: adr
status: accepted
created: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, opencode-go, pi, reviews]
---

# ADR 0011 — The review loop runs through OpenCode Go, and ADR 0007's reviewer list is amended

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0007 (decisions 2 and 3);
  supersedes no ADR. Decision D-13 stands as ADR 0007 set it — no criterion
  of D-13 changes here.
* Review: the decisions the maintainer stated on 2026-10-07 in a Claude Code
  session (bead coding-harness-ymx: the review loop through OpenCode Go;
  round 2 on `mimo-v2.6-flash`; the entry declares `anbieter-erklaert`; the
  compatibility probe runs in phase 4 before the merge), and on 2026-10-08:
  the ladder runs the review loop alone — the spec review and the review stay
  with Codex, after Codex's phase 6 found two real BLOCKERs in a change the
  loop had passed; Pi starts the loop's rounds; the address is OpenCode Go's
  OpenAI-compatible one; the residual risk of OpenCode's terms is accepted ·
  the acceptance is the merge commit and is written nowhere else, so the
  header's `review` stays empty (ADR 0008) · Decider: maintainer · prepared
  by an opencode session, revised for Pi by a Claude Code session
* Date: 2026-10-07; narrowed to the review loop and given Pi as its launcher
  on 2026-10-08 · takes effect on merge

## Context

* **ADR 0007** (accepted by the merge of pull request #60) sets where
  framework content may flow: to `openai-codex` through the official Codex
  CLI, and to `glm-coding-plan` through Claude Code — "Nothing else goes,
  and nowhere else". It gives the reviews to Codex and GLM: the spec review
  and the review to Codex, the loop between implementation and phase 6 to
  GLM, and, since 2026-10-06, exploration and implementation to GLM 5.3
  Flash.
* **The maintainer decided otherwise on 2026-10-07** (bead
  coding-harness-ymx): the review loop (4b) runs on OpenCode Go with a fixed
  ladder of three models for its rounds. On 2026-10-08 the maintainer put
  the ladder to the loop alone — the spec review and the review stay with
  Codex, because Codex's phase 6 found two real BLOCKERs in a change the
  loop had passed, as on every change of the night run — and, the same day,
  named Pi as the program that starts each round ("ich möchte pi nutzen"),
  the OpenAI-compatible address as its path, and accepted the residual risk
  of OpenCode's terms. Without this record the runner's declaration of
  `opencode-go` would run against ADR 0007's decision 2, which is a decision
  nobody made.
* **What OpenCode Go is** (`plans/changes/stage2-mimo/research.md` §E to
  §K, read 2026-10-07; §Q, read 2026-10-08): OpenCode (Operator Anomaly
  Innovations, Inc.) sells OpenCode Go by subscription with a Go key; three
  of the model ids it serves are `deepseek-v4.1-flash`, `mimo-v2.6-flash`
  and `mimo-v2.6-pro`. The Go page lists them under
  `https://opencode.ai/zen/go/v1/chat/completions`, the OpenAI-compatible
  address, and lists Pi among the clients it has validated ("Current builds
  send session information for OpenCode"). Its terms of service (effective
  2026-08-15) name no third-party client and forbid processes that
  "automatically or programmatically extracts data or Output" and that run
  "while you are not logged into the Services".
* **Why the launcher changed twice on 2026-10-08.** Three calls through
  Claude Code at the Anthropic-compatible address
  `https://opencode.ai/zen/go/v1/messages` were refused, and Claude Code
  speaks only that format. The maintainer then named OpenCode's own CLI; the
  installed version 2.0.24 did not load the policy file the runner supplies,
  which 1.18.35 loads (measured), so a read-only reviewer could not be shown.
* **What Pi is, measured** (research §L to §P; Pi 1.1.0, 2026-10-08):
  `@earendil-works/pi-coding-agent`, a coding-agent CLI. Its built-in
  `opencode-go` provider sends the three ids to `…/chat/completions` with
  Pi's own user agent and the `x-opencode-session` header the Go page asks
  for. `--tools read,grep,find,ls` declares exactly those four tools, and a
  call for any other tool is refused — but extension code, MCP servers,
  project files and the configuration directory still load unless each is
  switched off, and an extension can shadow a built-in tool's name. `read`
  returned a file outside the working directory when asked.
* **The class does not change.** What may be sent stays the `framework`
  class of `model-endpoints.yaml`: rules, templates, process, tests.
  Customer code and customer rows go to no endpoint, and the leak check
  before every call is what blocks them (unchanged from ADR 0007).

## Decision

1. **Framework content may also go to `opencode-go`** — at
   `https://opencode.ai/zen/go/v1/chat/completions`, through Pi
   (`@earendil-works/pi-coding-agent`, at the version the runner pins), with
   the three ids below. Of the stage-2 phases, the review loop (4b) only,
   with the runner's `probe` that measures its rungs. The
   sentence of ADR 0007 decision 2 that closes with "Nothing else goes, and
   nowhere else" now closes with Codex, Z.ai's GLM and OpenCode Go; nothing
   else goes, and nowhere else. Customer code and rows go to none of the
   three. The interactive `session` verb reaches a declared endpoint under
   its own amendment (bead coding-harness-amp); this declaration is what that
   verb waits for before it opens its OpenCode path to the three ids.
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
   rungs — measured, not assumed.** A round has `read`, `grep`, `find` and
   `ls` and nothing that writes or runs a command; but `read` reaches files
   outside the worktree, and Pi has no switch that confines it. A rung can
   therefore read what the maintainer's user can read — the secrets file and
   the customer instance's checkout included — and send it to OpenCode Go.
   What bounds it is the prompt's request to read nothing outside the
   worktree and the repository's git directory: a request, not a lock. The
   leak check scans what this repository presents, not what a rung reads.
   The maintainer accepted this residual risk for reviewers on 2026-09-30;
   it reaches the three rungs by this record.
5. **The key stays in the runner.** It is read from the secrets file at call
   time, reaches the call only in its environment as `OPENCODE_API_KEY`,
   never appears in an argument or in a file the runner writes, and an
   OpenCode Go call carries no other endpoint's key.
6. **Each round is isolated, and Pi is pinned.** Each call gets a fresh,
   empty Pi configuration directory whose one file switches Pi's own retries
   off, a scratch home directory, and the switches that keep extensions, MCP
   servers, skills, context files, prompt templates, themes, project trust,
   sessions and every network request but the model call off. The isolation
   was measured on Pi 1.1.0; the runner refuses any other version, and
   raising the pin means measuring it again. The effort is Pi's `max`, which
   Pi clamps to each model's ceiling — `max` for DeepSeek, `high` for both
   MiMo rungs: a known limit, not a failure.
7. **The address is measured before anything builds on it.** Three calls,
   one per rung, run through the runner and Pi in phase 4 of the change that
   carries this record — declaration and leak check in front of each, as one
   special run whose commits are named in the pull request body. After the
   probe, the change's own review loop runs on the ladder, at most three
   rounds. The probe and that loop are the only content leaving before the
   merge: the maintainer accepted the probe on 2026-10-07 and the loop on
   2026-10-08. If OpenCode Go refuses an id, the run stops and reports it:
   no second address, no second launcher, no substituted model.
8. **The terms risk is accepted.** The Go page invites "other coding agents"
   and lists Pi as validated; the terms of service do not address
   third-party clients and forbid automated extraction of output and
   processes that run while the user is not logged in. The maintainer
   accepted the residual risk on 2026-10-08. The reading and its date stand
   in the entry's remark, so a later change of the terms can be held against
   it, and the loop makes at most three calls per change.

## Options considered

* **Keep Codex and GLM in every review role (chosen against for the
  loop).** The maintainer kept Codex for the spec review and the review on
  2026-10-08, but the loop runs the ladder his decision names; keeping GLM
  there would not meet it.
* **An OpenCode product other than Go.** Zen serves other models over its
  own addresses, and Go Plus is the second Go plan with higher monthly
  caps; either changes only the billing. Chosen against: the maintainer
  named Go, and the entry's billing and limits are the Go plan's — another
  product needs its own entry and its own terms.
* **Claude Code at the Anthropic-compatible address.** The launcher this
  record first named: the program ADR 0007 already starts, and a validated
  client on the Go page. Chosen against on 2026-10-08: three calls through
  it at `…/v1/messages` were refused, and the Go page lists the three ids
  under the OpenAI-compatible address only.
* **OpenCode's own CLI.** The vendor's own client, named by the maintainer
  on the morning of 2026-10-08 and replaced the same day: the installed
  2.0.24 did not load the runner-supplied policy file, so a read-only
  reviewer could not be shown.
* **A round without tools.** Pi with `--no-tools` sends no tool at all
  (measured), which would close decision 4's reach entirely. Chosen against:
  a round that cannot open the code around a hunk misses the contracts the
  loop prompt asks about, and the loop's reviewer has had read and search
  tools since ADR 0007.
* **The model of round 2.** `mimo-v2.6-pro` in round 2 and again in round 3
  would give the third round nothing new over the second; the maintainer
  answered "runde 2 flash" on 2026-10-07, so round 2 is `mimo-v2.6-flash`.
* **Reviewer per phase written as code.** A model id as a literal in
  `scripts/stage2.py` would make every reordering a code change with tests
  to match — the opposite of what the decision asks for.

## Consequences

* **Nothing leaves before the merge except the probe and this change's own
  loop.** The three probe calls of phase 4 and this change's own review loop
  (at most three rounds) are the only foreign calls to OpenCode Go before the
  merge; the maintainer accepted the probe on 2026-10-07 and the loop on
  2026-10-08. Every other call is a stage-2 run after the merge. Until then `main` routes as ADR 0007 says:
  spec review and review on Codex, the loop on GLM, exploration and
  implementation on GLM 5.3 Flash.
* **A rule, not proof, at three places.** The address accepting the three
  ids is measured once, in phase 4; a refusal found later stops that run
  instead of opening a second design. The isolation of a round is measured
  by hand on one version and held to it by the pin; the test suite checks
  that the flags are passed, not that Pi obeys them. And which model a round
  calls is held by a test that reorders a fixture's list — a review of the
  list itself is what keeps a wrong order from shipping.
* **The continuity chain stops at ADR 0007.** This record amends ADR 0007,
  not decision D-13: D-13's criteria (three measured stage-2 runs,
  lakeswitch-ai's disclosure decision, a green leak check in every run, a
  declared endpoint with its residency) are untouched here, and the endpoint
  list is ADR 0007's text. The map in `scripts/check_decision_continuity.py`
  therefore gains nothing, and the D-13 row of the target document says the
  same thing it said.
* **Data use and terms.** The Go key sits in the secrets file and reaches the
  child process's environment only. The entry declares `anbieter-erklaert`
  because the Go page gives no region and the vendor's Zen page states US
  and EU for its models; the measurement stays open as a `[GAP]` of the
  change's spec. The terms reading of 2026-10-08 stands in the entry's
  remark beside it.
* **The runner's shape.** `run_codex` and the Codex tuple stay for the spec
  review and the review; the loop's calls are Pi launches; explore and
  implement stay Claude Code launches against Z.ai. The ask rule on a
  directly typed `codex` and `.claude/settings.json` stay as they are — the
  subject of bead coding-harness-amp.
* **The resume stays where it was.** Phase 6 resumes the Codex thread of
  phase 2a; a thread that cannot be resumed starts a fresh session and says
  so in `findings.md`.

## Validation

* `python3 -m pytest tests/test_stage2.py tests/test_model_endpoints.py -q`
  green: the runner starts `pi` for the loop's rounds with the flags, the
  environment and the fresh configuration directory of decision 6, the rung
  as `opencode-go/<id>` and the key as `OPENCODE_API_KEY` only, and refuses
  a Pi off the pin before the leak check; `codex exec` is started pinned as
  on main for the spec review and the review; the ladder round *n* →
  `modelle[n-1]` holds in a reordered fixture; three rounds are the limit
  and round 3 only after a taken row; the 30-minute limit is one constant
  and a stand-in that outlasts it is stopped; the key is in no argv, no
  print and no record; a red leak check exits 2 with nothing written.
* `make verify` green, and `scripts/touch_map.py origin/main HEAD` naming no
  protected area: `docs/adr/` gains only this file, `scripts/leakcheck.py`,
  `scripts/harness.py`, `scripts/touch_map.py`,
  `scripts/check_decision_continuity.py`, `scripts/new_change.py`,
  `docs/architecture/`, `ROADMAP.md`, `.claude/settings.json` and
  `model-endpoints.yaml`'s German keys are untouched.
* The probe's commit named in the pull request body, with each rung's id and
  the first line of its answer through Pi.
