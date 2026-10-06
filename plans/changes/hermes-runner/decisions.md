---
title: "Decisions — hermes-runner"
status: accepted
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-i3y
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# hermes-runner — Decisions

**Questions only, prepared for the phase 1a interview; nothing is answered
yet.** Each question comes from [`research.md`](research.md) and carries
options, a recommendation and what the recommendation costs. The order puts
first what unblocks the most work. Answers are recorded below each question
as a dated Y-statement once the maintainer gives them
([`prompts/01a-interview.md`](../../../prompts/01a-interview.md)).

Given, not asked again: the maintainer wants Hermes Agent as the runner for
Coding Harness's recurring jobs (2026-10-05, "Ich würde gerne Hermes
forcieren, lege die Grundlage dafür"); the first job is the weekly re-check
of research notes (bead coding-harness-pu9, part 2); the class is
`architectural`.

## Q1 · Does adhd-relief's spike run first, as the proof for both repositories?

**Why now:** every slice that needs Hermes running waits for proof that its
guards hold, and that proof needs the maintainer at the laptop for an
afternoon (research 4.4, 4.6). Nothing of it has run yet.

If the guards are proven once on this laptop, should that one afternoon
serve both repositories, or should Coding Harness prove them on its own?

- **(a) One afternoon for both.** The maintainer runs adhd-relief's runbook
  (S-2 to S-6, the write boundary in §7, S-7), and adds a short Coding
  Harness part the same afternoon: S-2, S-4 and the write boundary again for
  the Coding Harness user with its toolsets `web` and `file` and learning
  off. Results stay in adhd-relief; Coding Harness cites them by commit.
- **(b) A spike of Coding Harness's own.** Its own throwaway user and kit;
  independent of adhd-relief's timing and PR #2, but a second afternoon and
  a second copy of a 446-line runbook.
- **(c) No spike.** Install the Coding Harness profile directly and treat the
  first runs as the proof; no evidence before an agent that writes is live.

**Recommendation: (a).** One install, one proxy and one guard baseline are
shared anyway (research 8), so one proof covers them; the short addendum
covers what differs.

**Consequence:** Coding Harness's Hermes-dependent slices (profile install,
first run) wait for that afternoon; slices that do not need Hermes (ruleset,
prompt, endpoint entry, publish script, ADR draft) go ahead meanwhile. The
spike's results and adhd-relief's PR #2 remain adhd-relief's business.

## Q2 · Which model does the job use, and so where does its text go?

**Why now:** every model must resolve to a declared endpoint (rule RB-A6,
"not listed is BLOCK"), and the answer decides whether a leak check is
needed before each run (Q5).

If the job sends a research note and its search results to a model every
week, should that model be a flat-rate open model shared with the personal
agent, or a first-party model paid by use?

- **(a) GLM-5.3 on OpenCode Go, through the shared proxy.** A new endpoint
  entry (operator Anomaly Innovations, Inc., USA; subscription; sees
  `framework` only). Flat cost if the existing subscription is shared, with
  one quota for both agents (GLM-5.3 about 220 requests per five hours). Its
  terms forbid software that runs "while you are not logged into the
  Services" — whether a scheduled job falls under it is open, and a block
  would stop both agents. A foreign endpoint, so the leak check applies.
- **(b) Claude through the Anthropic API key.** Already declared
  (`anthropic-api`); a first-party endpoint, so no leak check and no new
  entry; about $0.7–1.1 a run by the assessment's estimate; a key to place on
  the host. Spends Anthropic money, not the Claude subscription.
- **(c) GLM-5.3 through Z.ai's API key.** A new token-billed entry; about
  $0.3–0.8 a run (assessment); a second foreign vendor; the leak check
  applies. Z.ai's coding plan itself is excluded for this use by its own
  entry ("only through Claude Code").

**Recommendation: (a)**, with a key of its own for the Coding Harness user
on the same subscription. It keeps the cost flat and the model route the
spike tests (S-5), and spares the Claude budget, which bead
coding-harness-6hx named as a reason.

**Consequence:** a new entry in `model-endpoints.yaml`; the leak check
before every run (Q5); a block or a throttle by opencode hits adhd-relief's
agent too, with ADR-0025's fall-back to OpenCode Zen for both. Whether one
OpenCode Go subscription allows a second key was not read.

## Q3 · One service user with two Hermes profiles, or two service users?

**Why now:** it shapes the profile slice and the Coding Harness part of the
spike (Q1).

If two Hermes agents run on the same laptop — the personal one with your
journal and Telegram, and the Coding Harness job reading the open web —
should the operating system keep them apart, or Hermes's own code?

- **(a) One user, two profiles, one gateway.** Hermes's default
  ("Multiplexing is on by default"); per-profile secrets kept apart by
  Hermes's code inside one process. Less to set up. Under one OS user the
  job, fed by the open web, could read the personal vault, and the personal
  agent could read the job's key (derived from Hermes's documentation and
  ADR-0022; not tried).
- **(b) Two users, shared install and proxy.** Each its own LaunchDaemon,
  `HERMES_HOME`, write root and keys; the OS keeps them apart, as ADR-0022
  already relies on for the vault. A second service user to create and a
  second short spike part.

**Recommendation: (b).** Hermes itself advises one process per profile "when
you want hard process-level isolation", and the job's input is the open web.

**Consequence:** a second user (`sudo`) and a second LaunchDaemon on the
laptop; whether Coding Harness runs a gateway or a one-shot Hermes run from
launchd is left to the design phase (research 11).

## Q4 · Which ruleset does `main` get?

**Why now:** `main` has no protection and no ruleset (measured 2026-10-05).
The publish token needs `contents: write`, and that permission also merges a
pull request (GitHub's permission data, research 3.4). The ruleset can be
set this week; it needs GitHub Pro or higher for this private repository,
and the plan could not be read (research 3.2).

If anything — a token, an agent or a slip — tries to push straight to
`main` or merge a pull request whose CI is red, should GitHub refuse it, and
for whom?

- **(a) No direct pushes.** Require a pull request (no approval), block force
  pushes and deletion of `main`, no bypass. Nothing pushed straight to `main`
  since 2026-09-22, so today's flow does not change.
- **(b) As (a), plus CI must be green.** Add the required status check
  `verify` (loose: the branch need not be up to date). A merge while CI is
  red or still running is refused for everyone; `--admin` has no bypass to
  use. This is what `prompts/07-commit.md` already asks of agents, now held
  by GitHub.
- **(c) As (b), plus a separate identity for publishing.** "Restrict
  updates" on `main` with the repository admin as the only bypass, for pull
  requests only, and the publish step under a GitHub App. Then the publish
  identity cannot merge or push `main` at all. Costs an App and its private
  key — a bot identity, which ADR 0008 put on the not-now list for agents.
- **(d) Require one approval.** Cannot be met: the maintainer and every agent
  act as one account, and nobody else can approve.

**Recommendation: (b).** It turns two rules already followed by hand into
GitHub's refusal and costs nothing in today's flow. (c) stays the upgrade if
a second runner arrives.

**Consequence:** a red or hanging CI blocks every merge until it is fixed or
the ruleset is switched off by the owner; the tracker-first push order
(house rule 4) becomes binding through CI. No ruleset can tell the
maintainer from a token of the same account, and none reaches the tracker
ref `refs/dolt/data`.

## Q5 · May the job run on its schedule before PR #60 brings the leak check?

**Why now:** applies only if Q2 picks a foreign endpoint. The leak check
exists only on PR #60's branch, needs a change folder the job does not have,
and its denylist lives on the laptop (research 2.3). PR #60 waits for the
maintainer at the laptop (ROADMAP, "Next").

If the job is ready before PR #60 is merged, should it wait, run with a
smaller check of its own, or run without one?

- **(a) Wait.** Scheduled runs start after PR #60 merges and after a small
  change lets the leak check scan a job's prompt and its staged note without
  a change folder. Runs by hand in a Claude Code session (first-party, no
  foreign call) can start now.
- **(b) Run with a check of the job's own.** The prepare step scans the
  staged note and the prompt against the denylist before the run. A second
  copy of the leak-check logic, to retire when PR #60 lands.
- **(c) Run without a check.** The note is framework text meant to become
  public, and house rule 6 is reviewed when the note is merged. Nothing then
  stops a slip before it leaves for a US endpoint and a search vendor.

**Recommendation: (a).** The spike (Q1) needs the laptop anyway, and PR #60
waits for the same; one session can serve both.

**Consequence:** the first scheduled run waits for PR #60 and one small
follow-up change; until then the job runs only by hand.

## Q6 · Does Hermes take a Now place in `ROADMAP.md`?

**Why now:** the roadmap trial allows at most three Now themes, and all
three are taken: forms and their checker, LakeSwitch reads Coding Harness,
the repository in English (`ROADMAP.md`, checked 2026-10-05).

If Hermes is pushed now, which theme waits?

- **(a) Hermes replaces "The repository in English"**, which moves to Next.
  English has no date; LakeSwitch has one (its pilot expires 2026-12-15); the
  forms carry the design template this change needs for phase 2b.
- **(b) Hermes replaces "Forms and their checker".** The design template
  (bead coding-harness-9qo) would then wait, though this change needs it.
- **(c) Hermes goes to Next.** The groundwork runs only where Now leaves
  room; the maintainer's "forcieren" is not reflected.
- **(d) Four Now themes.** Breaks the trial's own rule.

**Recommendation: (a).**

**Consequence:** German stays longer in `scripts/`, `tests/`,
`docs/governance/` and `model-endpoints.yaml`; the new endpoint entry (Q2)
uses that file's existing German keys.

## Not asked here

- **Whether the job waits for M3 or is scoped out of it** (unattended runs:
  budgets, cancellation, restore; research 2.4). The assessment places it in
  the ADR that brings the first scheduled agent; the ADR draft proposes, the
  maintainer's merge decides (ADR 0008).
- **`[GAP]`s for the spec and design phases** (research 11): due notes only
  or the oldest; the ordering of prepare, agent and publish; gateway or
  one-shot; the web backend; the write root's content; token lifetime;
  delivery beyond the pull request; whether the job prompt travels with the
  kit.

## Addendum 2026-10-05: the maintainer's answers

The maintainer answered the six questions one at a time in the Claude Code
session on 2026-10-05. The questions were asked in German, shortened; the
answer is recorded as the option the maintainer chose.

1. **Q1 — (a) yes, plus a Coding Harness part.** adhd-relief's spike is the
   shared proof for both repositories; the same afternoon at the laptop adds
   a short Coding Harness part (its own user, the write boundary, web through
   the proxy). No real job runs before it.
2. **Q2 — GLM-5.3 through OpenCode Go**, through the shared proxy, with its
   own entry in `model-endpoints.yaml` and its own key.
3. **Q3 — two service users**, sharing only the pinned install and the
   proxy; separate Hermes home, write root and keys.
4. **Q4 — pull request required plus a green CI** on `main`: no direct push,
   no force-push, no deletion, merge only through a pull request with a
   green `verify`, no bypass. The maintainer sets it up in GitHub (if the
   plan offers rulesets for a private repository; not verified).
5. **Q5 — (c) run before PR #60, without a leak check.** Asked as "May the
   scheduled job run before PR #60? Yes, before: faster, but repository text
   would go to GLM unchecked; low residual risk because house rule 6 keeps
   customer data out of Coding Harness, but unchecked." The maintainer chose
   this against the recommendation (a). Consequence: the scheduled run does
   not wait for PR #60; house rule 6 is checked when the note's pull request
   is reviewed and merged, not before the text leaves.
6. **Q6 — Hermes replaces "The repository in English" as a Now theme** in
   `ROADMAP.md`; the translation moves to Next.

All six questions are answered; phase 1a is closed.

## Addendum 2026-10-05: repair round 1 of slice 1

After the phase-6 review of slice 1 (`findings.md`, on `a4ff61c`) the
maintainer decided on 2026-10-05 to repair six of its rows in one round. The
answer is recorded as he gave it, in German: "Alle sechs reparieren".

1. **Slice-1 rows.** F-1 (the unbounded re-check),
   F-2 (`notes[0]` is not "the oldest" and a header with zero or two
   `last_reviewed:` lines has no rule), F-3 (the "Never" list does not forbid
   adding a line), F-4 (the language of the addendum), F-6 (checks 6 and 8
   stay silent while their criteria are broken) and F-7 (the kit rule is not
   held by a test) are repaired in one round, on the branch of slice 1.
2. **Rows that stay open.** F-5, F-8 and F-9 concern the orchestrator's
   contract; they stay open and are for slice 4's phase 2a.

## Addendum 2026-10-06: what holds the agent's own keys (F-14)

The phase-6 review of slices 2 and 5 found that the service user can read its
own OpenCode Go and Firecrawl keys in `$HERMES_HOME/.env`, and that only
Hermes's own file guard stands between a fetched page and those keys
(`findings.md`, F-14 and F-26). The maintainer was asked in the Claude Code
session on 2026-10-06, in German, shortened: "Hermes F-14: what holds the
agent's own API keys?" The answer is recorded as the maintainer gave it:

1. **A real barrier in slice 4.** The publish/orchestrator script passes the
   OpenCode Go and Firecrawl keys to Hermes only at start, on the wrapper's
   standard input, from a key file in the maintainer's home that the Hermes
   service user (`_chhermes`) cannot read. `.env` under `$HERMES_HOME` keeps
   only non-secret settings (the URLs).
2. **Before the merge of ADR 0010.** Spec, design and ADR 0010 are amended
   before the maintainer merges ADR 0010 (pull request #77).
3. **Not chosen:** accepting the risk with Hermes's own guard — which Hermes
   itself calls "not a security boundary" — plus the spike check CH-4.

Consequence: slice 4 builds the key handover together with the profile's side
of it (wrapper, `env.example`, runbook, test); `spec.md` gains criteria 60–70,
and F-14 stays open until slice 4 is built.
