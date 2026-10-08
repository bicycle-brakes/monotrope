---
title: "Spec — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, opencode-go, pi, review-loop, model-endpoints, adr]
class: feature
appetite: 8
change: stage2-mimo
adr_question: {proposed: "yes", answered_by: null, reason: "it widens where framework content may flow, which ADR 0007 limits to Codex and GLM and nowhere else, to the three models OpenCode Go serves for the review loop, and takes GLM out of the reviewer roles ADR 0007 names"}
---

# Spec — stage2-mimo

After this change the review loop (4b) is called on OpenCode Go: each round
is started through Pi at OpenCode Go's OpenAI-compatible address, read-only
and isolated per call, and which model answers the round comes from one
ordered list in `model-endpoints.yaml` that a one-line pull request can
reorder without touching code. The spec review (2a) and the review (6) stay
with Codex exactly as on main; GLM is no longer a reviewer (bead
coding-harness-ymx).

Inputs: [`research.md`](research.md) — sections E to K (OpenCode Go, read
2026-10-07), L to R (Pi 1.1.0, read and measured 2026-10-08) and S (read for
this spec) — and [`decisions.md`](decisions.md): the reviewer decision of
2026-10-07 with its two answers (round 2 is MiMo-V2.6-Flash; the entry
declares `anbieter-erklaert`), the answer "1" on the probe, and the three
addenda of 2026-10-08 (the ladder runs the loop only; Pi is the launcher and
`…/chat/completions` the address; the terms risk is accepted). None of them
is reopened here.

Written against the head of `feat/stage2-mimo` (`1d22f28`), which holds
`origin/main` of 2026-10-08 and the first implementation of this change
(with Claude Code as the loop's launcher). Every file named below is meant
as it stands there.

## Order of work

- **What stands.** The entry, the ladder, the three-round loop, the record,
  the doctrine and the ADR file were built at `3af0c9c` with Claude Code as
  the launcher. This revision changes the launcher, the address and what
  follows from them; criteria that do not mention either hold as built.
- **One pull request decides and carries.** `docs/adr/0011-stage-2-reviews-through-opencode-go.md`
  and `decisions/answers/stage2-mimo/adr.yaml` are reserved for
  `human-decided` (`provenance.yaml`), so this change's pull request is a
  decision pull request: title `decide(stage2): …`, label `decision`, body
  from `.github/PULL_REQUEST_TEMPLATE/decision.md` (house rule 8). The merge
  makes the amendment effective and lands the code at the same moment.
- **The compatibility probe comes first** once the Pi launch is built: three
  calls through the runner, one per rung, each with the declaration and the
  leak check in front of it (the maintainer's answer "1", 2026-10-07). The
  three calls of 2026-10-08 went through Claude Code to the Anthropic
  address and were refused; the probe is run again through Pi. If OpenCode
  Go refuses a rung, that is criterion 17: the run stops and is reported.
- **This change's own spec review (2a) and review (6) run on Codex.** Where
  its own review loop (4b) runs before the merge is the open `[DECISION]`
  below; no step before the loop depends on it.
- The key is already in the secrets file (`OPENCODE_GO_KEY`, name checked
  2026-10-07, value never read by an agent). Nothing in this change reads,
  writes or names its value.

## Problem

- **Nothing can call OpenCode Go** on `main`. `model-endpoints.yaml`
  declares no `opencode-go` entry, and an endpoint that is not listed is
  refused (the file's header: "Nicht gelistet ist BLOCK").
- **The decision in force forbids it.** ADR 0007, decision 2: framework
  content may go to `openai-codex` and `glm-coding-plan`; "Nothing else goes,
  and nowhere else."
- **Which model reviews is a code change** on `main`: every reviewer's model
  and effort is a constant, and `MAX_ROUNDS = 2` is another. The maintainer
  asked for an ordered list whose order is the round, changeable by a
  one-line pull request (`decisions.md`, addendum of 2026-10-07).
- **The loop stops at two rounds** on `main`, and the decision names three,
  the third "only when needed".
- **The launcher this branch built does not reach the rungs.** Three calls
  through Claude Code at `https://opencode.ai/zen/go/v1/messages` were
  refused on 2026-10-08 (`decisions/answers/stage2-mimo/adr.yaml`;
  `findings.md`, lines 41–45); the Go page lists the three ids under
  `…/chat/completions` only (research §F), and Claude Code speaks only the
  Anthropic format. The installed OpenCode CLI 2.0.24 does not load the
  runner-supplied policy file (measured 2026-10-08, `decisions.md`), so it
  cannot be shown to run a read-only reviewer.

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
  that is neither absent nor `nicht-erklaert` (`declaration_problem`,
  `scripts/stage2.py`).
- **Pi** — the coding-agent CLI `@earendil-works/pi-coding-agent`, pinned at
  1.1.0; it starts each round. **Agent directory** — Pi's configuration
  directory, named by `PI_CODING_AGENT_DIR` (research §L).

## Acceptance criteria

Each criterion holds one condition and names what refutes it. "A fixture" is
a repository a test builds in a temporary directory; "the stand-in" is the
recording program the tests put on `PATH` in the callee's place (`pi`,
`codex`, `claude`).

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
   `bemerkung` names: that the review loop (4b) alone runs here, through
   `python3 scripts/stage2.py` and Pi at the version the runner pins; the
   address `https://opencode.ai/zen/go/v1/chat/completions`, under which the
   Go page lists the three ids (research §F, §M), and that the
   Anthropic-compatible `…/v1/messages` is not used — three calls there were
   refused on 2026-10-08; that the Go page lists Pi among its validated
   clients and that Pi sends the `x-opencode-session` header the page asks
   for (research §G, §M, §Q); the Go plan at USD 10 a month; each rung's
   price and monthly limit (research §G); retention `0 days` and training
   "Not used" for all three, with DeepSeek's ZDR footnote valid through
   2026-10-31; that the Go page states no region and that
   `anbieter-erklaert` rests on the Zen page's "All our models are hosted in
   the US and EU.", both read 2026-10-07; and the terms reading of
   2026-10-08 — the terms of service (effective 2026-08-15) name no
   third-party client and forbid processes that "automatically or
   programmatically extracts data or Output" and that run "while you are not
   logged into the Services", a residual risk the maintainer accepted on
   2026-10-08 (research §Q; `decisions.md`).
   *Refuted by:* one of these points missing; one the sources do not state;
   Claude Code named as the loop's launcher or the Anthropic address as its
   path.

3. **The old reviewers' entries tell the truth.** The `glm-coding-plan`
   entry no longer says `glm-5.3` runs the review loop, and the
   `openai-codex` entry names the spec review and the review as its phases
   and not the loop; each says which phases still route to it.
   *Refuted by:* either remark claiming the review loop, or the Codex remark
   no longer naming 2a and 6.

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

8. **The loop's call is Pi, read-only and isolated.** `review-loop` and
   `probe` start `pi` with exactly `--print --no-session --no-approve
   --no-extensions --no-mcp --no-skills --no-context-files
   --no-prompt-templates --no-themes --offline --tools read,grep,find,ls
   --thinking max --model opencode-go/<rung>`, the prompt through
   `--append-system-prompt <file>` and a one-line message, an empty standard
   input and the worktree as its directory; its environment is the runner's
   allow-list plus `OPENCODE_API_KEY`, `HOME` set to a scratch directory of
   this call, and `PI_CODING_AGENT_DIR` set to a fresh directory of this call
   whose only file is `settings.json` = `{"retry": {"enabled": false}}`.
   `spec-review` and `review` start the Codex CLI exactly as on main: `codex
   exec` with `gpt-6.1-sol` pinned, the read-only sandbox, hooks and memories
   off.
   *Refuted by:* a loop call missing one of these flags or holding another
   tool, model or thinking level, `--mode json`, `--api-key` or `--approve`;
   an agent directory shared between two calls or holding another file;
   `HOME` the caller's; an `ANTHROPIC_*` or `CLAUDE_*` variable in its
   environment; its argv starting `claude` or `codex`; a `spec-review` or
   `review` call that does not go through `codex exec` with those pins.

9. **Phase 2a's session is what phase 6 resumes.** `spec-review` records the
   session it held as `Reviewer session: codex <thread id>`; `review` resumes
   that session with `codex exec resume` when one was recorded and otherwise
   starts a fresh one and says so in `findings.md`, with the wording it uses
   today.
   *Refuted by:* a recorded session phase 6 does not resume; a fresh session
   without the sentence that says so; a session line that names no reviewer.

10. **Every call is checked for itself.** Immediately before each of the
    four verbs' calls (`spec-review`, `review-loop`, `review`, `probe`): the
    declaration again, then the leak check over the change, the tree and the
    call's own prompt, then the call line in `findings.md` — one check per
    call, in that order.
    *Refuted by:* a call without its own check; the check after the call
    started; one check standing for two calls.

### The key

11. **The key stays in the runner.** The OpenCode Go key is read from the
    secrets file at call time and reaches the call only in its environment,
    as `OPENCODE_API_KEY`; it never appears in the arguments of a call or in
    a file the runner writes for it.
    *Refuted by:* eight consecutive characters of it in any recorded argv or
    in the agent directory the call saw; the key under another variable.

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
    on standard error, and the exit is 1. Pi's `--print` ends non-zero on a
    provider's 401, 404, 429 or 5xx answer (research §N), which is what makes
    a refused rung a failed call.
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

17. **A refused rung stops the run; it is not worked around.** If OpenCode
    Go refuses a rung's id at `…/chat/completions` — the probe's open
    question — the run stops and reports it (criterion 14). No second
    address, no second launcher, no other rung and no other endpoint is
    tried.
    *Refuted by:* a second call after the refused one — to the Anthropic
    address, through Claude Code or OpenCode's CLI, to another rung, or to
    another endpoint.

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

20. **No live call.** Every test that starts a reviewer starts a stand-in —
    `pi`, `codex` or `claude`; no test starts the real Pi, reads the
    maintainer's secrets file, the denylist or the loop record of a real
    change, and none needs the network.
    *Refuted by:* `test_the_runner_finds_only_stand_ins` or
    `test_the_suite_never_reaches_the_real_denylist_or_secrets` red with an
    OpenCode Go call in the run; a test that passes only with a real key or
    an installed Pi.

### The doctrine

21. **§4 routes the review loop to OpenCode Go and the spec review and the
    review to Codex.** `docs/WORKFLOW.md` §4's routing table gives 4b the
    ladder with the round-to-rung mapping, keeps 2a and 6 on Codex, keeps 1
    and 4 on GLM 5.3 Flash, and keeps "no stage 2" for a `spike` and a
    one-sentence change; §3's model table keeps its rows for wherever the
    runner does not start a phase.
    *Refuted by:* a table routing 4b to GLM or to a single rung, or 2a or 6
    to the ladder, or a `spike` given a stage-2 review.

22. **The reason for reviewing across vendors still holds, and now says
    what the ladder records.** §4 keeps the argument that lineages see
    different errors and that disagreements are recorded rather than resolved
    automatically, and names the three rungs' lineages instead of "Codex
    flagged it, GLM did not".
    *Refuted by:* the argument gone; or the sentence still naming two
    reviewers of the same round.

23. **The prompts and the instruction file follow.**
    `prompts/04b-review-loop.md` names the ladder, its round-to-rung mapping
    and Pi as the program that starts each round; `prompts/02a-spec-review.md`
    and `prompts/06-review.md` name Codex as their reviewer and the loop's
    round limit of three with the round-3 condition; the stage-2 paragraph
    of `AGENTS.md` sends 2a and 6 to Codex and the loop to the ladder through
    Pi; `prompts/01-explore.md` and `prompts/04-implement.md` still name GLM
    5.3 Flash.
    *Refuted by:* the loop prompt without the ladder or Pi; any of these
    texts naming Claude Code as the loop's launcher; a review prompt naming a
    rung as its reviewer; the instruction file sending 2a or 6 to the ladder;
    one of the last two prompts without GLM.

24. **The stop rule counts the new reviewers.** Where §4 measures the first
    stage-2 runs, a taken finding of a rung counts like a Codex or GLM
    finding counts today.
    *Refuted by:* the measurement naming only the two former reviewers.

25. **The ADR.** ADR 0011 records: that framework content may go to
    `opencode-go` at `…/chat/completions` through Pi, pinned, for phase 4b
    only — and that the `session` verb reaches the entry under its own
    amendment; that GLM leaves the reviewer roles while Codex keeps the spec
    review and the review and explore and implement stay on GLM 5.3 Flash;
    that the ladder is an ordered list a one-line pull request changes; that
    the loop runs at most three rounds; that the unconfined reads ADR 0007
    accepted for its reviewers extend to the rungs, with Pi's `read` measured
    reaching outside the worktree; the key as `OPENCODE_API_KEY`; the
    isolation per call and the version pin; the effort `max` clamped to
    `high` for both MiMo rungs; the accepted terms risk; and the options
    weighed — keeping Codex and GLM, an OpenCode product other than Go,
    Claude Code at the Anthropic address, OpenCode's own CLI, a round without
    tools, and the model of round 2. **It is a file of this change's own pull
    request, which is therefore a decision pull request** (title
    `decide(stage2): …`, label `decision`, decision body): the merge confirms
    it and lands the code together with it.
    *Refuted by:* ADR 0007's "Nothing else goes, and nowhere else" standing
    unamended while `opencode-go` is declared; one of these points missing
    from the ADR or from its draft in `design.md`; the pull request merged
    without its decision title, label or body.

26. **Green.** `make verify` is green on the last commit.
    *Refuted by:* a gate red.

### Added with the launcher (2026-10-08)

27. **The pinned Pi or none.** Before the leak check of a `review-loop` or
    `probe` call, the runner runs `pi --version`; if it cannot start, ends
    non-zero, takes longer than 30 seconds or prints anything but the pinned
    version (`1.1.0`, one named constant), the runner refuses with exit 2:
    no leak check, no call line, no call.
    *Refuted by:* a stand-in answering `1.1.1`, failing `--version` or not
    present, and a call that starts, a line in `findings.md`, or an exit
    other than 2.

28. **§4 says what a round can read.** `docs/WORKFLOW.md` §4 and the
    runner's module docstring say that a round's `read` reaches files outside
    the worktree (measured with Pi 1.1.0, research §L), that the secrets file
    is among them, that only the prompt's request bounds it, and that the
    isolation flags are configured on every call and were measured once by
    hand on the pinned version; neither counts the loop's calls among the
    `--restricted` Claude Code calls.
    *Refuted by:* a text that calls every runner call confined, or counts the
    loop's calls among the Claude Code ones.

29. **§4's caveat names each subscription's client.** The caveat on
    subscription coverage says Claude Code for Z.ai, the Codex CLI for
    OpenAI and Pi for OpenCode Go — a client the Go page lists as validated,
    under terms that do not name third-party clients, a risk the maintainer
    accepted on 2026-10-08.
    *Refuted by:* the caveat naming Claude Code as the covered program for
    every subscription, or OpenCode Go without its accepted risk.

## Non-goals

In this change, not now:

- **Explore and implement** — the `explore` and `implement` verbs, GLM 5.3
  Flash, and §3's rows for them; neither is routed by class and neither moves
  to OpenCode Go. Their Claude Code environment returns to main's.
- **Any launcher but Pi for the loop** — Claude Code (refused at the
  Anthropic address), OpenCode's own CLI, the Codex CLI, a direct HTTP call
  by the runner.
- **The `session` verb** (bead coding-harness-amp) — this change's
  declaration opens its OpenCode path for the three ids, as that verb's spec
  expects (research §S); its launcher, policy and amendment are its own.
- **The Anthropic-compatible address** — not used and not measured further.
- **A real Pi in the test suite** — the suite starts stand-ins only
  (criterion 20); the isolation flags were measured by hand on the pinned
  version (research §L), and the pin holds that measurement to it.
- **Confining Pi's reads below the tool level** — no operating-system
  sandbox; the residual risk is ADR 0011's decision 4.
- **Checking a rung against Pi's own catalog** — the declaration check
  stands (see the `[DETAIL]`s).
- **Any OpenCode product but Go** — Zen, the Zen addresses, a second plan.
- **A measurement of a rung's cost, time or findings** — the first live
  rounds measure them.
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
- **`.claude/settings.json` and the ask rule on `codex`** — the `session`
  verb's business (bead coding-harness-amp).
- **The German keys and comments of `model-endpoints.yaml`** — translated in
  a pull request of their own (house rule 1).
- **The interview decision D-13, its row in the target document and the
  continuity map** — see the `[DETAIL]`s.
- `ROADMAP.md`, `docs/architecture/`, the Omnigent wiring.

## Protected areas

- `docs/adr/` other than ADR 0011 — `human-decided`; ADR 0007 is amended by
  the new record, never edited in place (house rule 8).
- `scripts/leakcheck.py`, the denylist and where it lives — the check is
  reused, not changed.
- `scripts/harness.py`, `scripts/touch_map.py`, `scripts/new_change.py` — the
  machinery around a change, not the reviews.
- `~/.config/cc-routing/secrets.env` — never read, never written (its name is
  quoted, its value is not).
- `~/.pi` and the Pi install itself — the runner points Pi at a directory of
  its own and changes nothing of Pi's.
- The loop record's location outside the worktree and outside the git
  directory.

Beyond the non-goals: none.

## Known limits

- **A round can read outside the worktree.** Pi's `read` returned a file
  outside its working directory (measured, research §L), and nothing at the
  tool level confines it; the secrets file and the customer instance's
  checkout are within its reach. Only the prompt's request bounds it — the
  risk ADR 0007 accepted for its reviewers and ADR 0011 extends to the rungs.
- **MiMo answers at `high`, not `max`.** Pi clamps `--thinking max` to each
  model's ceiling: `max` for `deepseek-v4.1-flash`, `high` for both MiMo
  rungs (research §O). Whether OpenCode Go forwards the effort as sent is
  not readable.
- **The isolation is a measurement of one version.** The flags were measured
  by hand on Pi 1.1.0; the runner refuses any other version, and raising the
  pin means measuring them again — a rule, not proof.
- **A near-miss id is not measured.** Pi matches `--model` exactly or by a
  fuzzy match; an id close to another catalog id may be matched to that one
  (research §S). The ladder holds exact ids of OpenCode Go's list.

## Definition of Done

- `verify` green.
- Moved in the same pull request, each by name: `model-endpoints.yaml`;
  `scripts/stage2.py`; `tests/test_stage2.py`; `tests/test_model_endpoints.py`;
  `docs/WORKFLOW.md` §4; `prompts/02a-spec-review.md`;
  `prompts/04b-review-loop.md`; `prompts/06-review.md`; `AGENTS.md`;
  `scripts/kit/probe.py` where a test's travel list changes;
  `docs/adr/0011-stage-2-reviews-through-opencode-go.md`;
  `decisions/answers/stage2-mimo/adr.yaml` as the maintainer stated it
  (re-recorded at `fc76287`, Pi included).
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list and by its "What it touches" section
  (`scripts/touch_map.py origin/main HEAD`).
- Bead: the pull request closes `coding-harness-ymx`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-ymx`
  (`prompts/07-commit.md`).
- Special runs: the compatibility probe through Pi (three calls through the
  runner, one per rung, declaration and leak check in front of each), its
  commit and three lines in the pull request body — and this change's own
  loop only as the open `[DECISION]` below decides.

## Open decisions

### `[DECISION]` — where this change's own review loop runs before the merge

The spec said "GLM for 4b" until `3af0c9c`, which changed it to "the
ladder"; your answer "1" of 2026-10-07 and ADR 0011 say the probe is the only
content that leaves for OpenCode Go before the merge; one review-loop call
already went there on 2026-10-08 (research §S). No answer of yours covers
it.

```text
Goal in one sentence:  Before you merge this change, may its own review loop
                       send its diff to OpenCode Go, or only the probe?
Options:
  1. The ladder, through Pi, after the probe.
                       Up to three more calls carry this change's diff to
                       OpenCode Go before your merge makes ADR 0011
                       effective — beyond the probe you allowed; in return
                       the new loop is shown working end to end before you
                       decide on it.
  2. GLM, as main routes the loop today.
                       Only the probe goes to OpenCode Go before the merge,
                       as recorded; the diff goes to Z.ai, which ADR 0007
                       already allows; the round is started with main's
                       runner against this worktree; the new loop first runs
                       on the next change.
  3. No foreign loop for this change.
                       Nothing leaves but the probe; Opus 5.5 reviews in 4b
                       and Codex in phase 6; no lineage of the ladder sees
                       this change before the merge.
Recommendation:        Option 1 — the probe already sends to the same
                       endpoint under the same declaration and leak check,
                       and a loop shown working is the evidence the decision
                       pull request otherwise lacks.
If you say "ok":       the order of work and ADR 0011 (decision 7, the first
                       consequence) say "the probe and this change's own
                       loop, at most three rounds", and phase 4 runs
                       `review-loop stage2-mimo` from this branch after the
                       probe.
What is lost:          Option 2 keeps your rule of 2026-10-07 that only the
                       probe leaves before the merge, at the price of a GLM
                       round that shows nothing about the new launcher.
```

### `[GAP]`s

- **Closed: the Anthropic address.** It is not used: Pi's built-in
  `opencode-go` provider sends the three ids to `…/chat/completions`, the
  address the Go page lists for them (research §F, §M).
- **Open, measured in phase 4: whether `…/chat/completions` answers the
  three ids for a real Go key** — the probe, before any step builds on it;
  a refusal is criterion 17.
- **Open: where OpenCode hosts the Go models.** The Go page states no region;
  only Zen states "US and EU" (research §G). Re-read before phase 7; a
  statement found there corrects the entry's `residenz` in the same pull
  request.
- **Open, not measured in this change: whether OpenCode Go forwards the
  effort as Pi sends it** (research §O, §R) — `--print` shows no usage; a
  known limit.

### `[DETAIL]`s — decided here, with the reason

Reversible, and nothing beyond this change depends on them.

- **Phases 2a and 6 run Codex, exactly as on main** — the maintainer put the
  ladder to the review loop alone on 2026-10-08.
- **Rounds 1 and 2 unconditional, round 3 conditional on round 2's taken
  rows** — `decisions.md`, `[DETAIL]` 2. Undecided rows still hold the next
  round, unchanged.
- **The rounds are a ladder over repaired code**, one reviewer per round:
  round 2 sees round 1's repair.
- **The entry's remaining fields** — `name: opencode-go`, `betreiber`,
  `abrechnung: abonnement`, `darf_sehen: [framework]`, key `OPENCODE_GO_KEY`
  (`decisions.md`, `[DETAIL]` 4).
- **The request shape is Pi's built-in `opencode-go` provider**: the
  OpenAI-compatible format, `Bearer` authentication, Pi's own user agent and
  the `x-opencode-session` and `x-opencode-client` headers (research §M) —
  what the Go page asks of a client. Production writes no `models.json`, so
  no address but Pi's built-in one can be reached.
- **The launch flags are the measured set** (criterion 8): each one closes a
  path a hostile file could open — a shadowed `grep`, an extension's code,
  an MCP server, a project's settings or context, the agent directory's
  `SYSTEM.md` — and `--tools` alone closes none of them (research §L).
  `HOME` is the call's scratch directory because the set was measured in
  that environment (research §L, §P).
- **The read tools stay, and their unconfined reach is accepted, not
  closed.** `read,grep,find,ls` is the Read/Grep/Glob the loop's reviewer
  has had since ADR 0007; a round that cannot open the code around a hunk
  misses the contracts the loop prompt asks about. `--no-tools` would close
  the reach (measured, research §L) and is named in the ADR's options. This
  does not widen where framework content may flow: the destination stays
  `opencode-go`, and the reach is the "whole disk" ADR 0007's decision 4
  accepted for reviewers on 2026-09-30, which ADR 0011's decision 4 carries
  to the rungs in words that name Pi and the secrets file, so the merge
  decides with it in view.
- **`--print`, not `--mode json`** — `--print` ends non-zero on a provider
  error (criterion 14), JSON mode ends 0 and would need a parser of
  `stopReason`; the loop already consumes plain text (research §N).
- **Retries off** — Pi's own retry re-sends a 429 or 5xx call three times
  inside one round, which the runner neither sees nor counts (research §N).
- **The key as `OPENCODE_API_KEY`, never `--api-key`** — the variable is the
  one Pi's provider reads, and an argument would put it in argv (research
  §M; criterion 11).
- **The prompt through `--append-system-prompt <file>`** with a one-line
  message: no `ARG_MAX` limit, and the scratch path does not reach the model
  as `@file` would; the runner writes the file itself, so Pi never receives
  a path it would send as text (research §N).
- **The rung is checked against the declaration, not Pi's catalog.**
  `declaration_problem` refuses an id the entry does not list before any
  call; an id OpenCode Go does not serve is answered with an error status,
  which `--print` turns into exit 1 (criterion 14). `--list-models` is a
  fuzzy search whose output and key need were not measured (research §S).
- **Effort `--thinking max` for every rung** — Pi clamps it to each model's
  ceiling; a per-rung effort in code would undo "the ladder is data". The
  clamp is a known limit, not recorded per call: `--print` does not report
  the resolved level.
- **The version pin lives in the runner** (`1.1.0`, one constant) and its
  failure is a refusal before the leak check (criterion 27): the isolation
  was measured on that version, and a refusal sends nothing.
- **The tool set is held by the hand measurement and the pin, not by a test
  of the real Pi** — the suite starts no real foreign program (criterion
  20), and hosted CI has no Pi, so such a test would be skipped where
  `verify` gates the merge.
- **The window-enforcement variable goes.** Its one recorded reason was the
  rungs through Claude Code (`plan.md`, detail of 2026-10-08); GLM's
  environment returns to main's, which never carried it — explore and
  implement are a non-goal.
- **The class stays `feature`** — a new endpoint entry, a new launcher for
  one verb and a re-routing of the loop; no interface a caller outside this
  repository holds.
- **The `Reviewer` cell and the round heading carry the model id**, not a
  display name: the id is what the entry lists and what the round called.
- **The findings header's producer follows the endpoint** — `codex` for the
  Codex tuple, `pi` for `opencode-go`. The branch at `1d22f28` writes
  `claude-code` for every endpoint (research §S); main chose by endpoint.
- **The 30-minute limit is one constant with the reviewer's name in it** — a
  hung call would hold the loop open for ever, and 30 minutes is well above
  what a round should take; a guess until the first live rounds.
- **A failed rung does not fall through to the next one** — a round must
  name the model that reviewed it.
- **ADR 0011 names the `session` verb's path** instead of leaving it
  implicit: the declaration opens it as that verb's spec expects (research
  §S), and a decision record that says "the review loop only" would
  otherwise read as closing it.
- **`decisions/answers/stage2-mimo/adr.yaml` stands as recorded at
  `fc76287`** — its reason carries the maintainer's words up to Pi; a later
  answer of the maintainer's is recorded the same way, never one of an
  agent's.
