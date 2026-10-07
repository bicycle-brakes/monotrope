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
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, mimo, review-loop, model-endpoints, adr]
class: feature
change: stage2-mimo
adr_question: {proposed: "yes", answered_by: null, reason: "it widens where framework content may flow, which ADR 0007 limits to Codex and GLM and nowhere else, to a third vendor, Xiaomi, chosen over OpenRouter, and extends to that vendor the unconfined reads ADR 0007 accepted for its reviewers"}
---

# Spec — stage2-mimo

MiMo-V2.6-Pro, Xiaomi's model, reviews every change in the review loop
(phase 4b) beside GLM, on the same diff and without seeing GLM's findings;
where the two differ, `findings.md` says so (bead coding-harness-ymx).

Inputs: [`research.md`](research.md) — its section "Gaps closed in phase 2"
holds where it disagrees with the text above it — and
[`decisions.md`](decisions.md), whose addendum of 2026-10-07 carries the
maintainer's answers: Xiaomi's own platform, with the maintainer's account and
key; GLM and MiMo independent on the same diff, one repair for both lists.
Neither answer is reopened here.

Written against the head of `feat/stage2-mimo` (`3ef4c85`), which stands on
`feat/stage-2-codex-glm` — pull request #60, not merged on 2026-10-07. Every
file named below is meant as it stands there.

## Order of work

- Phase 4 starts after pull request #60 is merged and `origin/main` is merged
  into this branch, and after `[DECISION]` 1 and the ADR question below are
  answered.
- The spec review (2a) runs by the routing in force when it runs: Codex
  through the runner once #60 is merged, Opus 5.5 before.
- This change's own review loop runs GLM alone. No MiMo call can run before
  this pull request is merged and the maintainer has then filled the
  personal-use declaration (criteria 3 and 4); the first MiMo call is a loop
  round of a later change.

## Problem

- **Nothing can start MiMo.** `model-endpoints.yaml` declares no Xiaomi
  endpoint, and an endpoint that is not listed is refused (the file's header:
  "Nicht gelistet ist BLOCK"). `python3 scripts/stage2.py review-loop` knows
  one reviewer, GLM (`review_loop`, lines 789–852).
- **The decision in force forbids it.** ADR 0007, decision 2: framework
  content may go to `openai-codex` and `glm-coding-plan`; "Nothing else goes,
  and nowhere else."
- **Two reviewers leave no record of where they differ.** A loop row names its
  reviewer, but nothing says whether the other reviewer raised the same
  finding. "MiMo flagged it, GLM did not" — what the maintainer asked to be
  recorded — cannot be read from the loop record or from `findings.md`.
- **A second vendor is a second way to fail.** A failed GLM call ends the run
  with exit 1 and no round (line 837). If the additional reviewer failed the
  same way, MiMo would stop the loop it was added to strengthen.

## Terms

- **MiMo** — Xiaomi's model `mimo-v2.6-pro` (MiMo-V2.6-Pro), through Xiaomi's
  own MiMo API Platform at its Anthropic-compatible address, with the
  maintainer's account and key (`MIMO_KEY` in the secrets file).
- **Round** — a run of `review-loop` that is counted: GLM answered, whether
  MiMo answered or not.
- **Both reviewed**, **GLM alone** — a round in which MiMo answered, or did
  not.
- **Cleared** — the declaration lets the runner call an endpoint (criterion 4).
- **`Also raised`** — the cell of a loop row that says whether the other
  reviewer of the round raised the same finding (criteria 19–21).

## Acceptance criteria

Each holds one condition and names what refutes it. "A fixture" is a
repository a test builds in a temporary directory; "the stand-in" is the
recording program the tests put on `PATH` as `claude`.

1. **The entry.** `model-endpoints.yaml` declares the endpoint `xiaomi-mimo`:
   `betreiber` names Xiaomi Technologies Singapore Pte. Ltd. and, for the EEA,
   Xiaomi Technology Netherlands B.V.; `residenz: anbieter-erklaert`;
   `abrechnung: token` (`abonnement` if `[DECISION]` 1 is answered with
   option 2); `darf_sehen: [framework]`; `modelle: [mimo-v2.6-pro]`.
   *Refuted by:* another value; `kundencode` or `kundendaten` among what it
   may see; a second model.

2. **The remark says what Xiaomi states.** The entry's `bemerkung` names: the
   Anthropic-compatible address, through Claude Code, for phase 4b only; data
   hosted in the Netherlands and Singapore — for an EEA account stored in the
   Netherlands, transferable to Singapore and to affiliates and service
   providers elsewhere; Xiaomi's statement that it does not use the content
   for model training; that no retention period is stated; that these terms
   hold for an account outside China, while an account in China falls under
   terms that store data in China; and that this was read on 2026-10-07 in
   Xiaomi's privacy policy and service agreement.
   *Refuted by:* a point missing, or a residency, retention period or promise
   that the sources (research, "Gaps closed in phase 2", C) do not state.

3. **The personal-use declaration is a field the maintainer fills.** The entry
   carries `personal_use_declaration` with the keys `declared_on` and
   `statement`. A comment above it says that only the maintainer fills it,
   after this change is merged, and that the statement covers: personal use,
   to be obtained again on the three conditions the file names for GLM and
   Codex; an account registered outside China; and that the address in
   `scripts/stage2.py` is the one the account's console shows. This change
   leaves both values `null`.
   *Refuted by:* the field, a key or one of the comment's points missing; a
   value set in this change's diff.

4. **MiMo is called only when cleared.** The runner calls MiMo only when the
   declaration clears `xiaomi-mimo` as it clears GLM — the entry present,
   `mimo-v2.6-pro` listed, `framework` among what it may see, a residency
   other than `nicht-erklaert` — and `personal_use_declaration` holds a
   `YYYY-MM-DD` date in `declared_on` and a non-blank `statement`.
   *Refuted by:* a fixture lacking any one of these in which the stand-in is
   started as MiMo.

5. **Two reviewers, one prompt.** When a round runs, MiMo is cleared and
   `MIMO_KEY` is in the secrets file, the runner makes exactly one GLM call
   and one MiMo call, and the two prompts are byte-identical: the text of
   `prompts/04b-review-loop.md`, the answer format, the read request and the
   diff, built as the GLM prompt is built today.
   *Refuted by:* one call or three; two prompts that differ in a byte.

6. **Neither sees the other.** Each call of a round starts before any part of
   the other call's answer of that round is written — to the loop record, to
   `findings.md` or into the worktree.
   *Refuted by:* a stand-in that finds, when it starts, a marker from the
   other call's answer of the same round in any of the three.

7. **MiMo's call is GLM's call, at Xiaomi.** The MiMo call starts Claude Code
   with every setting the GLM call has — tools `Read`, `Grep` and `Glob`, a
   fresh empty configuration directory, `--restricted`,
   `--strict-mcp-config`, permission mode `dontAsk`, no session persistence,
   an empty standard input, the runner's allow-listed environment — and with
   Xiaomi's Anthropic-compatible address as `ANTHROPIC_BASE_URL`,
   `mimo-v2.6-pro` as `--model` and in every model variable, and effort `max`.
   *Refuted by:* another address, model or effort; one setting of the GLM
   call missing.

8. **No key on a command line.** No eight consecutive characters of the GLM
   key or of the MiMo key appear in the arguments of any call.
   *Refuted by:* a stand-in's recorded arguments that hold them.

9. **Each call carries its own key.** The MiMo call's environment holds the
   MiMo key, as `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`, and not the
   GLM key; the GLM call's environment holds the GLM key and not the MiMo key.
   *Refuted by:* either key in the other call's environment.

10. **The MiMo key stays in the runner.** No eight consecutive characters of
    the MiMo key appear in what the runner prints, in the loop record or in
    `findings.md`.
    *Refuted by:* a stand-in that prints its key on standard output and on
    standard error, with exit 0 and with exit 1, and the key found.

11. **A leak check of its own before every MiMo call.** Each MiMo call follows
    a clean leak check over its own prompt, run in the same invocation after
    GLM's check and before either call starts.
    *Refuted by:* a MiMo call with one leak check for both calls, or with its
    check after a call has started.

12. **A check that is not clean stops the round.** If any leak check of a
    round is not clean, neither call starts, nothing is written to the loop
    record or to `findings.md`, and the runner exits 2.
    *Refuted by:* a planted match in the second check, after which a stand-in
    starts, a call line is written, or the exit is not 2.

13. **Each MiMo call leaves its line.** Each MiMo call adds to `findings.md`
    the line every stage-2 call leaves, naming the endpoint `xiaomi-mimo` and
    the model `mimo-v2.6-pro`.
    *Refuted by:* a MiMo call without its line.

14. **The rows of a round.** A round lands in the loop record, outside the
    worktree, as GLM's block and then MiMo's, each under a heading that names
    its reviewer. Its rows are numbered `L<round>-<k>` on through both lists
    and carry the reviewer `GLM` or `MiMo`.
    *Refuted by:* a MiMo row with the reviewer GLM; an id twice in one round;
    a row in the worktree.

15. **A round counts once.** A round both reviewed counts as one of the two
    rounds the loop allows.
    *Refuted by:* a second round refused after one round both reviewed; a
    third round started.

16. **If MiMo is not asked or does not answer, the round runs with GLM alone
    and says so.** The causes: the declaration does not clear MiMo (criterion
    4); `MIMO_KEY` is missing; the call cannot start; it ends with a non-zero
    exit; its answer is empty; it has not ended within its time limit
    (criterion 17). In each case the round is written with GLM's rows and
    counts, MiMo's block in the loop record is the line `MiMo did not review
    this round: <cause>.`, the runner's output names the cause, and the exit
    is 0.
    *Refuted by:* one cause after which the run exits non-zero, the round is
    not written or not counted, or the cause is not named in the record or in
    the output.

17. **A time limit for MiMo.** A MiMo call that has not ended 30 minutes
    after it started is stopped, and that is a cause of criterion 16. The 30
    minutes are one named constant. GLM's call keeps no limit, as today.
    *Refuted by:* a stand-in that outlasts a shortened limit, and a run that
    waits for it or exits non-zero.

18. **GLM is still required.** If the GLM call fails or answers nothing, the
    attempt is no round, as today: the loop record is unchanged — MiMo's
    answer of that attempt is not kept, and the output says so — and the
    runner exits 1.
    *Refuted by:* a record written, or exit 0.

19. **Every loop row has `Also raised`.** It is the last cell of a loop row.
    In a round both reviewed the runner leaves it empty, or writes `no` where
    the other reviewer reported no row in that round; in a round GLM reviewed
    alone it writes `—`.
    *Refuted by:* a loop row without the cell; `—` in a round both reviewed;
    an empty cell in a round GLM reviewed alone.

20. **The implementer says where the two met.** A loop row is undecided — and,
    like a row without `Status`, holds the next round and the release — while
    its `Also raised` is empty or holds anything other than: `no`; `—` in a
    round GLM reviewed alone; or the ids of rows the other reviewer raised in
    the same round, each of which names this row back.
    *Refuted by:* a next round or a release with such a row; a well-formed row
    refused.

21. **`findings.md` records the disagreement.** When the loop rows are
    released, each carries its `Also raised`, and one line counts: the rows
    only GLM raised, the rows only MiMo raised, the rows of each reviewer that
    the other raised too, and the rounds MiMo did not review. The line `MiMo
    did not review this round: <cause>.` of each such round is carried too.
    *Refuted by:* a released row without the cell; a count that differs from
    the rows; a cause line lost.

22. **No live call.** Every test that runs a MiMo call starts the stand-in;
    no test reads the maintainer's secrets file, denylist or loop record, or
    needs the network.
    *Refuted by:* `test_the_runner_finds_only_stand_ins` or
    `test_the_suite_never_reaches_the_real_denylist_or_secrets` red with MiMo
    in the run; a test that passes only with a real key.

23. **The doctrine names MiMo in phase 4b, and nowhere else.**
    `docs/WORKFLOW.md` §4, `prompts/04b-review-loop.md`,
    `prompts/06-review.md` and `AGENTS.md` name MiMo as the second reviewer of
    the review loop, with its fallback and `Also raised`; no text routes MiMo
    to phase 1, 2a, 4 or 6.
    *Refuted by:* one of these files without MiMo; MiMo routed to another
    phase.

24. **The evidence rule covers MiMo.** Wherever the evidence rule stands —
    `docs/WORKFLOW.md` §2, `prompts/04-implement.md`,
    `prompts/04b-review-loop.md` — it names a MiMo finding beside Codex's and
    GLM's.
    *Refuted by:* one of these texts naming Codex and GLM only.

25. **The stop rule covers MiMo.** The measurement of the first stage-2 runs
    (`docs/WORKFLOW.md` §4) counts a taken MiMo finding that broke a test like
    a Codex or GLM finding.
    *Refuted by:* the rule naming Codex and GLM only.

26. **The ADR.** The ADR the maintainer's answer names records that framework
    content may also go to `xiaomi-mimo` through Claude Code, for the review
    loop only; that the unconfined reads ADR 0007 accepted for its reviewers
    extend to MiMo; that the stop rule counts MiMo; that GLM stays required and
    MiMo falls back; the options weighed — OpenRouter pinned to a US provider,
    OpenRouter with free provider choice, GLM first and MiMo after GLM's
    repair, a direct API call by the runner, a Token Plan; and Xiaomi's data
    terms as read.
    *Refuted by:* ADR 0007's "Nothing else goes, and nowhere else" standing
    unamended while `xiaomi-mimo` is declared; one of these points missing.

27. **Green.** `make verify` is green on the last commit.
    *Refuted by:* a gate red.

## Non-goals

In this change, not now:

- **MiMo anywhere but phase 4b** — no spec review, review, exploration or
  implementation by MiMo; neither `mimo-v2.6-flash` nor
  `mimo-v2.6-pro-ultraspeed`.
- **Any other way to Xiaomi** — OpenRouter or another aggregator, the
  OpenAI-compatible address, a direct API call by the runner, a second Xiaomi
  address.
- **Changes to GLM's or Codex's calls**, to the limit of two rounds, to the
  phase-6 marks, or to the order verdict first, release after.
- **What only the maintainer does** — the Xiaomi account, the top-up or
  subscription, `MIMO_KEY` in the secrets file, the personal-use declaration.
- **A live call, or a measurement of MiMo's cost, time or findings** — the
  first live rounds measure them.
- **Matching findings by machine** — the implementer says where two rows meet;
  the runner checks the form, not the meaning.
- **The German keys and comments of `model-endpoints.yaml`** — translated in a
  pull request of their own (house rule 1).
- **The interview decision D-13, its row in the target document and the
  continuity map** — see the `[DETAIL]`s.
- `ROADMAP.md`, `docs/architecture/`, the Omnigent wiring.

## Open decisions

### `[DECISION]` 1 — how Xiaomi is paid

```text
Goal in one sentence:  How you pay Xiaomi decides which address the reviews
                       go to and which of Xiaomi's terms apply.
Options:
  1. Pay per use.      You top up a balance in US dollars; each review is
                       charged by its tokens — about 10 to 25 US cents a round
                       at Xiaomi's list price (USD 0.435 per million input and
                       0.87 per million output tokens). Xiaomi's terms put no
                       limit on the tools that use it; nothing is bought ahead.
  2. Token Plan.       A monthly subscription from USD 6, not refundable, with
                       an address in Amsterdam. Xiaomi limits it to
                       programming tools and forbids "automated scripts"; the
                       runner is a script that starts Claude Code, which
                       Xiaomi lists as supported — allowed by our reading, not
                       by Xiaomi's word.
Recommendation:        Option 1 — at two rounds per change it costs cents, and
                       Xiaomi's terms leave no doubt that the runner may use it.
If you say "ok":       the entry says `abrechnung: token`; the runner sends to
                       Xiaomi's pay-per-use address
                       (`https://api.xiaomimimo.com/anthropic`), which your
                       declaration confirms against your console; your key is
                       an `sk-` key, stored as `MIMO_KEY`.
What is lost:          a fixed monthly price, and an address that is itself in
                       Europe (with option 1 an account in the EEA is stored in
                       the Netherlands by Xiaomi's policy, not by its address).
```

### The ADR question — proposed "yes"

The header proposes **yes**: this change widens where framework content may
flow — ADR 0007 limits it to Codex and GLM, "nowhere else" — to a third
vendor, chosen over OpenRouter, and extends to that vendor the unconfined
reads ADR 0007 accepted for its reviewers.

**The vehicle this spec recommends:** a new ADR with the next free number —
0011 on 2026-10-07, since 0010 is held by the open decision branch
`decide/adr-0010-hermes` — that amends ADR 0007's decisions 1, 2 and 4.
Because ADR 0007 is accepted by the merge of #60, which comes before this
change lands, and in this repository an accepted decision is amended by a new
ADR (ADR 0007 amends D-13; ADR 0009 amends D-15 and O-3). **The alternative:**
ADR 0007's own text widened on this branch — one document would still list
every stage-2 vendor, but the text the maintainer confirmed by merging #60
would change after that merge. The maintainer answers both at once, with
`python3 scripts/harness.py decide adr` or in the conversation (recorded with
`--stated-in`); the reason names the vehicle. Either way the pull request is a
decision pull request (house rule 8).

### `[GAP]`s

- **Closed by reading** (research, "Gaps closed in phase 2"): the API shape
  (Anthropic- and OpenAI-compatible), the addresses, the model id
  `mimo-v2.6-pro`, the key in a header or `ANTHROPIC_AUTH_TOKEN`, Claude Code
  documented by Xiaomi for both ways of paying, the prices, the operator, the
  residency, the training statement, the retention, the next ADR number.
- **Not closable by reading:** the address Xiaomi shows for the maintainer's
  own account (the console is behind the login; Xiaomi gives addresses by the
  account's region). The runner pins Xiaomi's documented address; the
  maintainer's statement confirms it (criterion 3), and until it is filled
  MiMo does not run (criterion 4). If the console shows another address, the
  one constant changes in the same pull request as the declaration.

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change; the ADR states the
ones that touch what leaves the machine, and the maintainer's merge confirms
them.

- **The endpoint's name `xiaomi-mimo`** — operator and product, as
  `openai-codex`.
- **MiMo-V2.6-Pro, id `mimo-v2.6-pro`** — `decisions.md` (addendum) chose Pro;
  the id is Xiaomi's.
- **Through Claude Code, as GLM** — Xiaomi documents Claude Code for both ways
  of paying; the maintainer asked for both reviewers on the same state, and
  only the same launch gives MiMo what GLM has: the diff and the tools to read
  around it; the runner keeps one way to start a reviewer of the loop. The
  price: MiMo's reads are as unconfined as GLM's — a request, not a lock —
  which the ADR states and the merge accepts (criterion 26). A direct API call
  would confine MiMo to its prompt and give it less than GLM; it is a
  non-goal.
- **Effort `max`** — every stage-2 call pins it (`docs/WORKFLOW.md` §4).
  Xiaomi documents no effort parameter and has thinking on by default, so
  whether it takes effect is configured, not measured — as for GLM.
- **The two calls run at the same time** — they share nothing but the prompt;
  one after the other would double the wait.
- **GLM required, MiMo optional** — ADR 0007 names GLM for the loop and MiMo
  is the additional reviewer; a loop that stopped when the additional
  reviewer failed would lose GLM's finished round to it.
- **30 minutes for MiMo only** — "unreachable" includes a call that never
  ends, and without a limit GLM's finished round would wait for it. 30 minutes
  is well above what a round should take, a guess until the first live
  rounds; one constant. GLM keeps its behaviour (a non-goal).
- **`MIMO_KEY`** in the secrets file beside `GLM_KEY`, read at call time.
- **Numbering on through both lists** — the ids keep their form
  `L<round>-<k>`, so the phase-6 marks and every reader of ids stay as they
  are.
- **The implementer marks `Also raised`** — the implementer reads every row to
  decide it anyway, nobody else reads both lists before phase 6, and a machine
  cannot tell two wordings of one finding apart.
- **`no` prefilled where the other reviewer reported no row** — it is the only
  true value there; asking for it would be work without information.
- **The stop rule counts MiMo by name** — the maintainer asked for MiMo as a
  "Stufe 2 reviewer", and the stage-2 rule covers its reviewers. A rule for
  MiMo alone would be a new rule nobody asked for.
- **D-13 and the continuity map stay** — the new ADR changes which endpoints
  ADR 0007 clears, not what D-13 asks for; the D-13 row of the target document
  names no vendor.
- **The declaration is filled after the merge** — a decision takes effect when
  its pull request is merged (ADR 0008); a declaration filled in this pull
  request would let MiMo run on this change before Xiaomi is cleared.
- **New keys in English** (`personal_use_declaration`, `declared_on`,
  `statement`) — house rule 1; the file's German keys stay until their own
  pull request.
