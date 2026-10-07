---
title: "Spec — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: opencode, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, opencode-go, review-loop, model-endpoints, adr]
class: feature
appetite: 8
change: stage2-mimo
adr_question: {proposed: "yes", answered_by: null, reason: "it widens where framework content may flow, which ADR 0007 limits to Codex and GLM and nowhere else, to the three models OpenCode Go serves for reviews, and takes Codex and GLM out of the reviewer roles ADR 0007 names"}
---

# Spec — stage2-mimo

After this change every stage-2 review — the spec review (2a), the review
loop (4b) and the review (6) — is called on OpenCode Go, and which model
answers each round comes from one ordered list in `model-endpoints.yaml` that
a one-line pull request can reorder without touching code. Codex and GLM are
no longer reviewers (bead coding-harness-ymx).

Inputs: [`research.md`](research.md) — sections E to K hold everything read
about OpenCode Go on 2026-10-07 — and [`decisions.md`](decisions.md), whose
addendum of 2026-10-07 carries the maintainer's decision verbatim and both
answers to it: round 2 is MiMo-V2.6-Flash, and the entry declares
`anbieter-erklaert`. Neither answer is reopened here.

Written against the head of `feat/stage2-mimo` (`4e54967`), which stands on
`origin/main` of 2026-10-07 including pull request #60 (ADR 0007) and pull
request #89 (the flash runner's `explore` and `implement` verbs). Every file
named below is meant as it stands there.

## Order of work

- Implementation starts: pull requests #60 and #89 are merged, which was the
  start condition of the decision (bead coding-harness-ymx), and this branch
  holds `origin/main`.
- This change's own spec review (2a), review loop (4b) and review (6) run on
  the routing in force when they run — Codex for 2a and 6, GLM for 4b —
  because the code that routes them is the code this change replaces. The
  first OpenCode Go call of any kind happens after this pull request is
  merged: the entry it needs is added by this change.
- **Merge order.** The ADR amendment travels as its own decision pull
  request (`decide(stage2): …`, label `decision`), and it merges before this
  change's pull request does; until then the entry is declared here and
  nothing calls it (house rule 8). This change's pull request names that
  decision pull request in its body.
- **The compatibility probe comes first in phase 4** (the maintainer's answer
  to row S1 of the phase-2a review): three calls through the runner, one per
  rung, each with the declaration and the leak check in front of it, before
  any step of phase 4 builds on the Anthropic address. It is one special run
  and its commits are named in the pull request body. If an address refuses
  a rung, that is criterion 17: the run stops and is reported.
- The key is already in the secrets file (`OPENCODE_GO_KEY`, name checked
  2026-10-07, value never read by an agent). Nothing in this change reads,
  writes or names its value.

## Problem

- **Nothing can call OpenCode Go.** `model-endpoints.yaml` declares no
  `opencode-go` entry, and an endpoint that is not listed is refused (the
  file's header: "Nicht gelistet ist BLOCK"). The runner's endpoint tuples
  are `CODEX`, `GLM`, `GLM_FLASH`, `HAIKU` and `SONNET`
  (`scripts/stage2.py:90-94`); there is no tuple for OpenCode Go.
- **The decision in force forbids it.** ADR 0007, decision 2: framework
  content may go to `openai-codex` and `glm-coding-plan`; "Nothing else goes,
  and nowhere else."
- **Which model reviews is a code change.** Every reviewer's model and effort
  is a constant (`scripts/stage2.py:90-91`), and `MAX_ROUNDS = 2` is another
  (`scripts/stage2.py:134`). The maintainer asked for an ordered list whose
  order is the round, changeable by a one-line pull request
  (`decisions.md`, addendum of 2026-10-07); today `modelle` carries nothing
  but membership (`research.md` §J), and `declaration_problem` reads it that
  way.
- **Both reviewers are wired into the code and the doctrine by name.**
  `SESSION_LINE` matches `Reviewer session: codex` only
  (`scripts/stage2.py:147`), round headings are `## Round <n> — GLM, <date>`
  (`scripts/stage2.py:1296`), and `docs/WORKFLOW.md` §4 routes 2a and 6 to
  gpt-6.1-sol and 4b to GLM 5.3. A third reviewer cannot be named by a list
  the code does not read.
- **The loop stops at two rounds**, and the decision names three, the third
  "only when needed".

## Terms

- **Ladder** — the ordered `modelle` list of the `opencode-go` entry. Its
  position is the round: position 1 answers round 1.
- **Rung** — one model of the ladder.
- **Round** — one run of `review-loop` that wrote a block into the loop
  record.
- **Taken row** — a loop row whose `Status` begins `taken`, as the implementer
  writes it (`docs/WORKFLOW.md` §4).
- **Cleared** — the declaration lets the runner call an endpoint: the entry
  present, the model listed, `framework` among what it may see, a residency
  that is neither absent nor `nicht-erklaert`
  (`declaration_problem`, `scripts/stage2.py`).

## Acceptance criteria

Each criterion holds one condition and names what refutes it. "A fixture" is
a repository a test builds in a temporary directory; "the stand-in" is the
recording program the tests put on `PATH` in the callee's place.

### The entry

1. **The entry.** `model-endpoints.yaml` declares `opencode-go` with
   `betreiber: "OpenCode (Operator Anomaly Innovations, Inc.)"`,
   `residenz: anbieter-erklaert`, `abrechnung: abonnement`,
   `darf_sehen: [framework]`, and `modelle` in exactly this order:
   `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`.
   *Refuted by:* another value in any field; `kundencode` or `kundendaten`
   among what it may see; a fourth model; a different order; two of the three
   ids missing.

2. **The remark says what OpenCode states, with its source and date.** Its
   `bemerkung` names: the Anthropic-compatible address
   `https://opencode.ai/zen/go/v1/messages` and the OpenAI-compatible
   `…/chat/completions`; that the Go page lists these three ids under the
   OpenAI address only, and that whether the Anthropic address accepts them
   is measured in phase 4 (research §F); that Claude Code is a validated
   client there and its native session header needs no wrapper (research §G);
   the Go plan at USD 10 a month; each rung's price and monthly limit
   (research §G); retention `0 days` and training "Not used" for all three,
   with DeepSeek's ZDR footnote valid through 2026-10-31; that the Go page
   states no region and that `anbieter-erklaert` rests on the Zen page's
   "All our models are hosted in the US and EU.", both read 2026-10-07; and
   that the reviews are phases 2a, 4b and 6 through the runner only.
   *Refuted by:* one of these points missing, or one the sources do not state.

3. **The old reviewers' entries tell the truth.** The `openai-codex` entry no
   longer says it is used for the spec review and the review, and the
   `glm-coding-plan` entry no longer says `glm-5.3` runs the review loop
   before phase 6; each says instead which phases, if any, still route to it.
   *Refuted by:* either remark still claiming a reviewer phase this change
   takes away.

### The ladder

4. **The round reads its model from the ladder.** Round *n* of `review-loop`
   calls `modelle[n-1]` of the `opencode-go` entry: round 1
   `deepseek-v4.1-flash`, round 2 `mimo-v2.6-flash`, round 3
   `mimo-v2.6-pro`.
   *Refuted by:* a round calling another id; a reviewer model id standing as
   a literal in `scripts/stage2.py`.

5. **Reordering the list changes the reviews, not the code.** In a fixture
   whose `modelle` is reordered or whose ids are replaced, the rounds call
   the models the list now gives, and the diff of that change touches
   `model-endpoints.yaml` and nothing else.
   *Refuted by:* a change to the list that leaves the round calling the old
   model, or that needs a line in `scripts/stage2.py`.

6. **Three rounds.** The loop runs at most three; a fourth is refused with
   the refusal's present form (`<n> rounds have run; the loop stops at <n>.`)
   and exits as a refusal does today.
   *Refuted by:* a fourth round starting, or the loop still stopping at two
   rounds after three have run.

7. **Round 3 only when needed.** Rounds 1 and 2 both run, each still held by
   an undecided row as today; round 3 starts only when round 2 wrote at least
   one row whose `Status` begins `taken`.
   *Refuted by:* a round 3 after round 2 produced no taken row; no round 3
   after round 2 produced one.

### Who launches a call

8. **The runner starts every reviewer the same way.** `spec-review`,
   `review-loop` and `review` each launch Claude Code against
   `https://opencode.ai/zen/go/v1/messages` with the rung's id as the model
   and effort `max`, and the settings `review-loop` pins today (tools
   `Read,Grep,Glob`, a fresh empty `CLAUDE_CONFIG_DIR`, `--restricted`,
   `--strict-mcp-config`, permission mode `dontAsk`, `--output-format`, the
   runner's allow-listed environment). No verb of the runner starts the Codex
   CLI.
   *Refuted by:* a stand-in's recorded argv holding `codex`; a reviewer call
   with another base URL, model or effort; one of those settings missing.

9. **Phase 2a's session is what phase 6 resumes.** `spec-review` records the
   session it held with the rung's id and the session id; `review` resumes
   that session when one was recorded and otherwise starts a fresh one and
   says so in `findings.md`, with the wording it uses today.
   *Refuted by:* a recorded session phase 6 does not resume; a fresh session
   without the sentence that says so; a session line that names no model.

10. **Every call is checked for itself.** Immediately before each of the
    three verbs' calls: the declaration again, then the leak check over the
    change, the tree and the call's own prompt, then the call line in
    `findings.md` — one check per call, in that order.
    *Refuted by:* a call without its own check; the check after the call
    started; one check standing for two calls.

### The key

11. **The key stays in the runner.** The OpenCode Go key is read from the
    secrets file at call time, reaches the call only in its environment as
    `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`, and never appears in the
    arguments of a call.
    *Refuted by:* eight consecutive characters of it in any recorded argv.

12. **The key reaches nothing else.** No eight consecutive characters of it
    appear in what the runner prints, in the loop record or in
    `findings.md`.
    *Refuted by:* a stand-in that prints its key on standard output and on
    standard error, with exit 0 and with exit 1, and the key found.

13. **A call carries no other endpoint's key.** An OpenCode Go call's
    environment holds no GLM key and no Codex key; a GLM call's environment
    holds no OpenCode Go key.
    *Refuted by:* either in the other's environment.

### When a call fails

14. **A round that did not review is not a round.** If a round's call cannot
    start, ends non-zero, answers empty, or is stopped by the time limit
    (criterion 15), the loop record is unchanged, the runner names the cause
    on standard output, and the exit is 1.
    *Refuted by:* a block in the loop record, an exit of 0, or a cause not
    named.

15. **A time limit for every reviewer call.** A call that has not ended 30
    minutes after it started is stopped; the 30 minutes are one named
    constant. Stopping it is one of the causes of criterion 14.
    *Refuted by:* a stand-in that outlasts a shortened limit and a run that
    waits for it or exits 0.

16. **A leak check that is not clean stops everything.** If a check of the
    run is not clean, no call starts, nothing is written to the loop record,
    and the runner exits 2 — as today.
    *Refuted by:* a call after a red check, a written round, or another exit.

17. **A refused address stops the run; it is not worked around.** If the
    Anthropic address refuses a rung's id — the open question of research §F
    — the run stops and reports it. No second address, no second design and
    substituted is built in this change.
    *Refuted by:* an automatic fallback to the OpenAI address, to another
    rung, or to another endpoint.

### The record

18. **Each round is written as its own reviewer.** A round lands in the loop
    record outside the worktree under `## Round <n> — <rung>, <date>`, its
    rows numbered `L<n>-<k>` on through the list, and the row's `Reviewer`
    cell holds the rung's id.
    *Refuted by:* a heading naming a model no round called; a row whose
    reviewer is another rung; an id repeated in one round; a row in the
    worktree.

19. **Release carries the reviewer of each row.** `release-loop` writes every
    loop row into `findings.md` with the reviewer its round had — not one
    fixed name — and the phase-6 reviewer marks each row agree or disagree as
    it does today; the verdict is written before anything is released.
    *Refuted by:* a released row with another reviewer; the release before
    the verdict.

20. **No live call.** Every test that starts a reviewer starts the stand-in;
    no test reads the maintainer's secrets file, the denylist or the loop
    record of a real change, and none needs the network.
    *Refuted by:* `test_the_runner_finds_only_stand_ins` or
    `test_the_suite_never_reaches_the_real_denylist_or_secrets` red with an
    OpenCode Go call in the run; a test that passes only with a real key.

### The doctrine

21. **§4 routes the three reviews to OpenCode Go.** `docs/WORKFLOW.md` §4's
    routing table gives 2a, 4b and 6 the ladder with the round-to-rung
    mapping, keeps 1 and 4 on GLM 5.3 Flash, and keeps "no stage 2" for a
    `spike` and a one-sentence change; §3's model table keeps its rows for
    wherever the runner does not start a phase.
    *Refuted by:* a table still routing 2a or 6 to Codex, or 4b to GLM, or a
    `spike` given a stage-2 review.

22. **The reason for reviewing across vendors still holds, and now says
    what the ladder records.** §4 keeps the argument that lineages see
    different errors and that disagreements are recorded rather than resolved
    automatically, and names the three rungs' lineages instead of "Codex
    flagged it, GLM did not".
    *Refuted by:* the argument gone; or the sentence still naming two
    reviewers of the same round.

23. **The prompts and the instruction file follow.**
    `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
    `prompts/06-review.md` and the stage-2 paragraph of `AGENTS.md` name the
    ladder, the round limit of three and the round-3 condition instead of
    Codex and GLM as reviewers of those phases; `prompts/01-explore.md` and
    `prompts/04-implement.md` still name GLM 5.3 Flash.
    *Refuted by:* one of the first four without the ladder; one of the last
    two without GLM.

24. **The stop rule counts the new reviewers.** Where §4 measures the first
    stage-2 runs, a taken finding of a rung counts like a Codex or GLM
    finding counts today.
    *Refuted by:*     the measurement naming only the two former reviewers.

25. **The ADR.** The ADR the maintainer's answer names records that framework
    content may go to `opencode-go` through Claude Code for phases 2a, 4b and
    6 only; that Codex and GLM leave the reviewer roles while explore and
    implement stay on GLM 5.3 Flash; that the ladder is an ordered list a
    one-line pull request changes; that the loop runs at most three rounds;
    that the unconfined reads ADR 0007 accepted for its reviewers extend to
    the rungs; and the options weighed — keeping Codex and GLM, an OpenCode
    product other than Go, OpenCode's own CLI as the launcher, and the model
    of round 2. **It travels as a decision pull request and merges before
    this change's pull request**: house rule 8 — a decision takes effect when
    its pull request is merged — so the entry this change declares is never
    in force against an unamended ADR 0007, and this change's pull request
    names the decision pull request in its body.
    *Refuted by:* ADR 0007's "Nothing else goes, and nowhere else" standing
    unamended while `opencode-go` is declared; one of these points missing;
    this change's pull request merged while the amendment was not.

26. **Green.** `make verify` is green on the last commit.
    *Refuted by:* a gate red.

## Non-goals

In this change, not now:

- **Explore and implement** — the `explore` and `implement` verbs, GLM 5.3
  Flash, and §3's rows for them; neither is routed by class and neither moves
  to OpenCode Go.
- **Any launcher but Claude Code** — OpenCode's own CLI, the Codex CLI, a
  direct HTTP call by the runner, and the `session` verb the maintainer asked
  for separately (bead coding-harness-amp).
- **Any OpenCode product but Go** — Zen, the Zen addresses, a second plan.
- **The OpenAI-compatible address as the path** — it is named in the remark
  and measured in phase 4, not built around (criterion 17).
- **A live call, and any measurement of a rung's cost, time or findings** —
  the first live rounds measure them.
- **Removing the `openai-codex` or the `glm-coding-plan` entry** — their
  remarks are corrected (criterion 3); a removed entry cannot be called again
  without being re-declared, which is a bigger claim than a corrected remark.
- **The personal-use declaration for OpenCode Go** — the maintainer writes it
  with a date, as Codex's was written on 2026-09-30; this change does not
  write another person's declaration, and touches no entry but its own.
- **The secrets file** — `OPENCODE_GO_KEY` is already there; nothing in this
  change reads it, names its value or writes the file.
- **Matching rows across rounds by machine, and `Also raised`** — there is
  one reviewer per round, and the cell was never built.
- **The loop record's place, the evidence rule, and the order verdict first,
  release after** — unchanged.
- **`.claude/settings.json` and the ask rule on `codex`** — what a direct
  call must still be asked about is the `session` verb's business (bead
  coding-harness-amp).
- **The German keys and comments of `model-endpoints.yaml`** — translated in
  a pull request of their own (house rule 1).
- **The interview decision D-13, its row in the target document and the
  continuity map** — see the `[DETAIL]`s.
- `ROADMAP.md`, `docs/architecture/`, the Omnigent wiring.

## Protected areas

- `docs/adr/` — `human-decided`; the amendment text is drafted in this folder
  and never edited in place (house rule 8).
- `scripts/leakcheck.py`, the denylist and where it lives — the check is
  reused, not changed.
- `scripts/harness.py`, `scripts/touch_map.py`, `scripts/new_change.py` — the
  machinery around a change, not the reviews.
- `~/.config/cc-routing/secrets.env` — never read, never written (its name is
  quoted, its value is not).
- The loop record's location outside the worktree and outside the git
  directory.

Beyond the non-goals: none.

## Definition of Done

- `verify` green.
- Moved in the same pull request, each by name: `model-endpoints.yaml`;
  `scripts/stage2.py`; `tests/test_stage2.py`; `tests/test_model_endpoints.py`;
  `docs/WORKFLOW.md` §4; `prompts/02a-spec-review.md`;
  `prompts/04b-review-loop.md`; `prompts/06-review.md`; `AGENTS.md`; the ADR
  amendment drafted in this folder; `decisions/answers/stage2-mimo/adr.yaml`
  re-recorded from the maintainer's own words of 2026-10-07, whose present
  reason names the superseded Xiaomi wording.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list and by its "What it touches" section
  (`scripts/touch_map.py origin/main HEAD`).
- Bead: the pull request closes `coding-harness-ymx`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-ymx`
  (`prompts/07-commit.md`).
- Special runs: one — the compatibility probe of phase 4 (three calls
  through the runner, one per rung, declaration and leak check in front of
  each), each with its commit in the pull request body.

## Open decisions

None open. `[DECISION]` 1 (round 2's model) and `[DECISION]` 2 (the entry's
residency) were answered by the maintainer on 2026-10-07 and are recorded in
`decisions.md`.

### `[GAP]`s — measured, not asked

- **Does the Anthropic address accept the three ids?** The Go page lists
  them under `https://opencode.ai/zen/go/v1/chat/completions` only
  (research §F). Measured in phase 4 as the declared special run of the
  Definition of Done — one call per id through the runner, the leak check in
  front of it, before any step builds on the address; if an id is refused
  the run stops and is reported (criterion 17).
- **Where OpenCode hosts the Go models.** The Go page states no region; only
  Zen states "US and EU" (research §G). Re-read before phase 7; a statement
  found there corrects the entry's `residenz` in the same pull request.

### `[DETAIL]`s — decided here, with the reason

Reversible, and nothing beyond this change depends on them.

- **The rung for phases 2a and 6 is rung 1**, `deepseek-v4.1-flash` — the
  decision gives the escalation to the loop, whose limit it raises to three;
  a single call has no round to climb. Risk written down: rung 1 is the
  cheapest of the three, so phase 6's verdict comes from the weakest model of
  the ladder; a stronger rung for phase 6 takes one sentence from the
  maintainer (`decisions.md`, `[DETAIL]` 1).
- **Rounds 1 and 2 unconditional, round 3 conditional on round 2's taken
  rows** — see `decisions.md`, `[DETAIL]` 2. Undecided rows still hold the
  next round, unchanged.
- **The rounds are a ladder over repaired code**, one reviewer per round:
  round 2 sees round 1's repair. The superseded answer "Beide unabhängig,
  gleicher Diff" and its `Also raised` cell go with it.
- **The entry's remaining fields** — `name: opencode-go`, `betreiber`,
  `abrechnung: abonnement`, `darf_sehen: [framework]`, key `OPENCODE_GO_KEY`
  (`decisions.md`, `[DETAIL]` 4).
- **The request shape** — the Anthropic address first, Claude Code's own
  user agent and native session header, no wrapper, exactly as the Go page
  describes for Claude Code; the OpenAI address is measured, not built
  (`decisions.md`, `[DETAIL]` 5).
- **The class stays `feature`** — a new endpoint entry and a re-routing of
  three existing verbs; no new subsystem and no interface a caller outside
  this repository holds. The ADR question carries the rule change, and an
  `architectural` class would add a design phase that decides nothing this
  spec has not already said.
- **The `Reviewer` cell and the round heading carry the model id**, not a
  display name: two rungs are MiMo and would need a name invented for them,
  while the id is what the entry lists and what the round called.
- **The findings header's producer becomes `claude-code`** — every reviewer
  call is a Claude Code launch after this change, and the branch
  `producer = "codex" if endpoint == CODEX else "claude-code"` already has
  that value for a non-Codex endpoint.
- **The 30-minute limit is one constant with the reviewer's name in it**, the
  only time limit in the runner today being none: a hung call would hold the
  loop open for ever, and 30 minutes is well above what a round should take
  — a guess until the first live rounds.
- **A failed rung does not fall through to the next one** — a round must
  name the model that reviewed it, and a round that quietly used rung 3
  while rung 1 failed would report a reviewer that never saw the diff.
- **`decisions/answers/stage2-mimo/adr.yaml` is re-recorded at the pull
  request**, not here: its answer stands, its reason still names Xiaomi and
  the Token Plan, and an answer is recorded only as the maintainer stated it
  (house rule 8).
