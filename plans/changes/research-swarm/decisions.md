---
title: "Decisions — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-19
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, phase-1, swarm, opencode-go]
---

# Phase 1 as a research swarm — Decisions

Phase 1a for bead coding-harness-icw. Q-1 and Q-2 were answered by the
maintainer in the conversation on 2026-10-13 and 2026-10-14 before this file
was written (recorded in the bead's notes); this file records them. Later
questions were asked on 2026-10-14 with their context first.

## Q-1 · Who researches, and on which models

asked: 2026-10-13
answer: phase 1 runs as a swarm of OpenCode Go models with different tasks and models; each research topic is worked by one free model and one Flash model; the first stage always uses all free models automatically.
answered_by: maintainer
status: answered

Free models seen in `pi --list-models` on 2026-10-13: longcat-2.5-preview-free,
space-bunny, hy4-preview; Flash: deepseek-v4.1-flash, mimo-v2.6-flash (bead
notes, coding-harness-km1).

In the context of one exploring model that misses what a second view would
find, facing the choice between one explorer and a swarm, we decided on a
swarm of free and Flash OpenCode Go models to achieve two independent views
per topic at low cost, accepting more calls per change. — 2026-10-13

Addendum 2026-10-15: `space-bunny` and `hy4-preview` turned out to be paid
OpenCode Go models (OpenCode Go and Zen documentation and the pinned Pi
1.1.0 registry, read 2026-10-15); the free seats are now
`longcat-2.5-preview-free`, `space-bunny-free` and `big-pickle`. Big Pickle
may use what it receives to improve the model. Asked whether that is
acceptable, the maintainer said: "Es ist für mich okay wenn es nur anhand des
Opus Satzes ist und die Modelle nicht in die repo schauen". The maintainer
also noted that the free models change constantly and the list must keep
being adjusted.

## Q-2 · The research topics

asked: 2026-10-14
answer: six topics, each worked by one free and one Flash model, then a judge reconciles the pair — (1) code today, (2) rules and decisions, (3) history, (4) tests and gates, (5) risks and edge cases, (6) outside world and neighbours.
answered_by: maintainer
status: answered

The maintainer agreed to the six proposed topics with "Ja" on 2026-10-14
(bead notes hold each topic's scope).

In the context of a research that must cover code, rules, history, tests,
risks and neighbours, facing the choice between free-form research and fixed
topics, we decided on six fixed topics to achieve that no area is skipped,
accepting twelve research calls per change. — 2026-10-14

## Q-3 · What the free models may see

asked: 2026-10-14
answer: the free models do the kind of research that needs no repository content — finding best practice, what already exists outside; they are not given repository content. The swarm follows set patterns: the search for best practice, the comparison with the overall architecture, and the comparison with the nearby specs.
answered_by: maintainer
status: answered

Context given with the question: the repository is private (checked
2026-10-14); the data terms of the three paid OpenCode Go models were read
(retention 0 days, no training), those of the free models were not. The
maintainer's words: "nutzte die kostenlosen modelle für die art recherche, für
die die repo nicht gelesen werden muss. sowas wie best practice finden, was
gibt es da draußen schon. der schwarm soll ja auch gewissen mustern folgen,
wie die such nach best practice, den abgleich mit der gesamtarchitektur und
den naheliegenden specs". How the patterns map onto the six topics of Q-2,
and which model takes a repository-bound topic's second seat, is left to the
spec.

In the context of free models whose data terms are unread and a private
repository, facing the choice between waiting for their terms and giving them
no repository content, we decided to give them only outward research to
achieve the free first stage without exposing the repository, accepting that
repository-bound topics need another model for their second view. —
2026-10-14

## Q-4 · Which changes get the swarm

asked: 2026-10-14
answer: changes of class `feature` and `architectural`; a `bounded` change keeps the single exploration.
answered_by: maintainer
status: answered

In the context of twelve research calls and a judge per change, facing the
choice between every change and the larger classes, we decided on feature and
architectural changes to achieve depth where it pays, accepting that a small
change gets one view. — 2026-10-14

## Q-5 · Who judges

asked: 2026-10-14
answer: Opus 5.5 reconciles the pair of each topic into `research.md`.
answered_by: maintainer
status: answered

Options shown: MiMo-V2.6-Pro (recommended by the session: cheap, spares Codex
and Claude quota), Codex Sol (five-hour limit), Opus 5.5 (Claude quota; the
orchestrating session itself, outside the runner's leak check). The
maintainer chose Opus 5.5.

In the context of two views per topic that may contradict each other, facing
the choice between an OpenCode Go model, Codex and Opus as the judge, we
decided on Opus 5.5 to achieve the strongest reconciliation, accepting the
Claude quota it uses. — 2026-10-14

## Q-6 · What the free models learn about the change

asked: 2026-10-14
answer: "Kurzes Thema mitgeben: Die freien Modelle bekommen eine von Opus geschriebene Ein-Satz-Beschreibung ohne Datei- und Codenamen (zum Beispiel „Container-Isolation für KI-Agenten-Läufe“). Die Spec wird vor der Nacht angepasst."
answered_by: maintainer
status: answered

Asked after the first draft (`01ff6d9`), whose spec gave the free models only
fixed generic questions. Context shown: with the topic they find practice that
fits this change; without it the private repository stays entirely local.
Options shown: keep generic questions (recommended by the session while the
free models' data terms are unread), or pass a short topic. The maintainer
chose the short topic. This narrows Q-3: the one-sentence topic is the only
change-derived text a free model receives.

In the context of free researchers whose generic questions yield generic
practice, facing the choice between no change information and a one-sentence
topic, we decided on an Opus-written sentence without file or code names to
achieve best practice that fits the change, accepting that the free providers
learn what the change is about. — 2026-10-14

## Q-7 · How the topics are cut and who works each

asked: 2026-10-15
answer: "ja, finder als schritt 0, ich möchte für jedes thema drei agenten, einmal deepseek, einmal mimo, einmal haiku, jeweils auch eigener blickwinkel, es soll immer einen template gefolgt werden. bei der online recherche möchte ich, dass alle verfügbaren freien modelle zu diesen thema recherchieren, also 1 bis x modelle"
answered_by: maintainer
status: answered
context: |
  Topic: how the research topics are cut and which agents work each.
  Intention: walking through the six topics of Q-2 after the phase-6 repairs, the maintainer asked for smaller topics with one model each; an online search on multi-agent research design followed.
  Today: six broad topics; topics 1 to 5 by a DeepSeek and a MiMo Flash pair, topic 6 by a free model and DeepSeek Flash; a fixed free roster with focuses; neighbouring specs found in passing in topics 2 and 6.
  Repository change: a step 0 finder that maps files, ADRs, tests and neighbouring specs (`neighbours:` in the header of `research.md`); smaller topics, each with its own agents; spec, design, ADR draft, `model-endpoints.yaml`, runner and tests change; Q-1 and Q-2 are amended.
  Architecture change: phase 1 gains a finder stage before the topic stage; the topic assignment becomes one brief per topic instead of two models sharing a broad topic.

Asked after phase 6 and the F-2 to F-10 repairs, while walking through the
six topics of Q-2. The maintainer first asked for smaller topics; the session
proposed thirteen (ten repository topics, three online topics) and, after an
online search on multi-agent research design (Anthropic's multi-agent
research system, locator-then-analyzer code research, STORM, studies on
model diversity), a step 0 "finder" that maps files, ADRs, tests and
neighbouring specs (`neighbours:` in the header of `research.md`, later the
spec's) for every repository topic. The maintainer had also said, on the
free roster, that the free models change constantly and the list must keep
being adjusted; "all available free models" replaces a fixed roster.

This amends Q-1 (one free and one Flash model per topic) and Q-2 (six
topics): each repository topic is worked by three agents — DeepSeek Flash,
MiMo Flash and Haiku 5.5 — each from its own perspective and on one fixed
template; each online topic is worked by every free model available at run
time. The exact topic list, the perspectives and the template are settled
in the following questions and then in the spec.

In the context of six broad topics shared by two models and a fixed free
roster that goes stale, facing the choice between keeping that cut and
smaller topics with a finder step, we decided on a finder, three agents with
distinct perspectives per repository topic on one template, and every
available free model on each online topic to achieve clear assignments and
independent views, accepting many more calls per run. — 2026-10-15

Addendum 2026-10-15: on where the neighbouring specs are kept, the
maintainer said: "die nachbar specs sollen auch im specs header festgehalten
werden." The finder's neighbours (the ones given in the header of
`research.md` plus its marked suggestions, once accepted) are carried into a
`neighbours:` field in the header of `spec.md`; the exact field form and
its check are settled in the spec.

Addendum 2026-10-15: on the perspectives, the session proposed one fixed
perspective per model (DeepSeek existing state, MiMo critique, Haiku
impact). The maintainer said instead: "ich möchte, das jedes model die
gleichen blcikwinkel am anfang bekommt um deren ergebnisse evaluieren zu
könenn." At the start every model receives the same brief and perspectives
for a topic, so that their results can be compared and evaluated; per-model
perspectives are a later decision on that evidence.

Addendum 2026-10-15: on how the research is used, the maintainer said: "die
recherce ergebnisse sollen dann klar in die interview phase und die spec
definition eingehen. es dürfen gegenfalls auch mehr interview fragen
gestellt werden". The reconciled findings feed phase 1a and phase 2
traceably, and the interview may ask more questions than the class
minimum where the research raises them.

Addendum 2026-10-15: the maintainer accepted ("ja") the report template —
one fixed template; at most seven key claims, each with an id, one-sentence
statement, evidence (`path::symbol` or URL), kind (fact, assumption,
judgement) and confidence with its basis; counter-evidence; what was not
read; relation to the neighbouring specs; questions for the spec — and the
judge's per-model scoring (supported, refuted, unique, off-brief), recorded
in `research.md`. Also accepted: interview questions derive from the
reports' `[DECISION]` claims and from disagreements between models, naming
the claim ids; spec criteria name the claims or answers they rest on; a gate
checks that no research `[DECISION]` is lost.

### Topic walk-through (2026-10-15)

- Topic 0, finder — guiding questions: which files and functions the change
  touches; which ADRs and rules apply; which tests and gates check those
  places; which specs are neighbours (those in `neighbours:` are given,
  further ones are marked suggestions). Boundary: it locates and lists,
  it does not judge. Output: one list per question, each entry
  `path::symbol` with one sentence why. The maintainer chose option A:
  DeepSeek Flash, MiMo Flash and Haiku 5.5 each search, and Opus 5.5 merges
  the three lists into one map (answer: "A").
- Topic 1, code and reuse — guiding questions: which existing functions or
  modules already do part of what the change needs; which pattern in the
  repository serves as a model (a similar script or test); what would have
  to change in existing code to reuse it, and what speaks against it.
  Boundary: only existing code on the finder's map plus what it imports
  directly; no judgement whether the change is sensible; no proposals for
  new code. Three agents on the same brief; template report with every key
  claim backed by `path::symbol` (answer: "ja").
- Topic 2, callers and interfaces — guiding questions: who calls the
  affected functions, scripts or commands (code, tests, Makefile, CI, hooks,
  prompts); which interfaces are affected (signatures, options, file and
  header formats, configuration keys); which callers would have to change
  with an interface and which only read; which interfaces other
  repositories use (lakeswitch, the kit). Boundary: only connections to the
  finder's map; no judgement whether an interface is good (topic 4). Three
  agents on the same brief; every key claim names caller and callee as
  `path::symbol` (answer: "ja").
- Topic 3, rules and ADRs — guiding questions: which ADRs and house rules
  bear on the change and what exactly they require, quoting the place;
  whether the change touches a file `provenance.yaml` reserves for the
  maintainer and so becomes a decision PR; whether a rule or ADR must be
  amended, superseded or written, and which ADR number is free; whether two
  applicable rules contradict each other. Boundary: only rules written in
  the repository; no judgement of a rule; no new rules. Three agents on the
  same brief; evidence `path::section` or ADR number and point (answer:
  "ja"). The maintainer added: "evtl. macht hier die frage auch sinn ob es
  ein spike, bound, feature oder adr ist?" — the form of that question is
  settled next.
  Accepted form (answer: "ja"): topic 3 gets a fifth guiding question —
  does the declared class fit what was found? Each agent names the class
  it holds right, with evidence; any disagreement with the declared class
  becomes an interview question and is always a `[DECISION]` for the lost-
  decision gate; the class never changes by itself.
- Topic 4, fit with the overall architecture — guiding questions: which
  layer or building block the change belongs to per `docs/architecture/`
  and `docs/WORKFLOW.md`; whether it uses the intended paths (models only
  through `stage2.py`, tracker only through `tools/bd`, gates through
  `make verify`) or builds a second one; whether it shifts responsibility
  between framework, kit and instances; what in the architecture documents
  would no longer hold after it. Boundary: only the documented
  architecture and the code on the finder's map; no new target
  architecture; neighbouring specs belong to topic 5. Three agents on the
  same brief; evidence `path::section` or `path::symbol` (answer: "ja").
- Topic 5, neighbouring specs — input: the neighbours in the header of
  `research.md` are given, the finder's suggestions added. Guiding
  questions: what each neighbouring spec fixes that this change touches
  (a criterion, interface or decision); where the two specs contradict or
  this change would break a neighbour's criterion; where they overlap so
  that work doubles or an order is needed; which resources both claim
  (ADR numbers, files, configuration keys, gate names); which of the
  finder's suggestions really is a neighbour, with a reason. Boundary:
  only the neighbours' spec, design, plan and `decisions.md` (their code
  belongs to topics 1 and 2); no judgement which spec is right. Three
  agents on the same brief; evidence `path::section` or criterion number;
  confirmed neighbours go into `neighbours:` in the spec header; every
  contradiction becomes an interview `[DECISION]` (answer: "5 passt").
- Topic 6, history and stale assumptions — guiding questions: when and why
  the affected places last changed (commit, PR, reason from the message or
  body); what was tried before and reverted or superseded; which
  assumption in code, docs or rules no longer holds (a model name, a
  number, a reference); which beads, handovers or maintainer decisions
  explain why something is deliberately so. Boundary: only the history of
  the places on the finder's map; no judgement of earlier decisions; no
  proposals for new code. Three agents on the same brief; evidence commit
  hash, PR number, bead id or `path::section` (answer: "ja"). The
  maintainer added: "bei themen wie haiku 5.5 sollte auch generelle
  abgeleitet werden, ob das nicht themen sind, die sich dauerhaft öndern und
  wie das in der repo geregelt werden kann" — the form is settled next.
  Accepted form (answer: "ja"): topic 6 gets a fifth guiding question —
  which stale facts found are of a kind that keeps changing, and how the
  repository should govern them. Each agent assigns each such fact one of
  three ways: one central place (changes rarely but regularly — model ids
  and efforts, cf. bead coding-harness-ylu), looked up at run time (changes
  constantly — the free models from Pi's list), or written down with a
  read-on date and a gate that warns after a period (must stay fixed). A
  finding becomes a proposal for the spec, or a follow-up bead when it
  reaches beyond the change; the maintainer decides each.
- Topic 7, tests and gates — guiding questions: which tests
  (`tests/…::test_…`) and gates check the affected places and what each
  checks; which behaviour no test or gate checks; which tests drive only
  stand-ins, so real evidence is missing; which tests or gates the change
  would turn red, and why; how each new behaviour can be tested red-first,
  and where that is hard. Boundary: only tests and gates of the places on
  the finder's map; describe, write no tests; no `make verify` run. Three
  agents on the same brief; evidence `tests/…::test_…` or the gate name
  from `decisions/gates.yaml` (answer: "ja").
- Topic 8, risks and edge cases — guiding questions: which failure paths
  exist (aborts, timeouts, missing files, unreachable services) and what
  happens today; which unusual inputs are conceivable (empty or broken
  headers, date boundaries, duplicate ids, special characters); which
  security boundaries the change touches (leak check, secrets, what
  foreign models see, maintainer-only files); how the system recovers
  after an abort (resume, partial state, clean-up); what happens when two
  sessions or worktrees work on it at once. Boundary: only risks of the
  places on the finder's map; name, do not design solutions; others'
  public failure reports belong to topic 11. Three agents on the same
  brief; evidence `path::symbol` plus the trigger (answer: "ja").
- Topic 9, best practice (online) — input: only the Opus sentence and the
  fixed guiding questions, nothing from the repository. Guiding questions:
  which proven approaches exist for the problem, each with a source; which
  reasons the sources give and under which conditions they hold; where the
  sources disagree; what they explicitly advise against. Boundary: only
  public pages the model actually retrieved (no retrieval, no claim —
  F-3); ready-made tools belong to topic 10, failure reports to topic 11.
  Source quality: search broad, then narrow; official documentation,
  papers and known projects before SEO pages; each source with its date
  where given. Every free model available at run time on the same brief;
  evidence a URL with a retrieval receipt (answer: "ja").
- Topic 10, existing tools and standards (online) — input: only the Opus
  sentence and the fixed guiding questions. Guiding questions: which tools,
  libraries or services solve the problem fully or in part; how mature
  each is (version, last release, licence, maintained); which standards or
  formats exist for it; what each costs and whether it runs locally or
  sends data out. Boundary: only public pages with a retrieval receipt; no
  recommendation whether to adopt (spec and interview decide); general
  approaches belong to topic 9. Source quality: the tool's project page,
  repository and docs before comparison portals; versions and licence only
  with source and date. Every free model available at run time on the same
  brief; evidence a URL with a retrieval receipt (answer: "ja").
- Topic 11, known risks and failure reports (online) — input: only the
  Opus sentence and the fixed guiding questions. Guiding questions: which
  failures or incidents with similar solutions are publicly reported, and
  their cause; which security vulnerabilities or advisories exist for
  tools in the area; which non-obvious traps experience reports describe;
  how others fixed or prevented them. Boundary: only public pages with a
  retrieval receipt; no transfer to our code (the judge does that with
  topic 8); tool overviews belong to topic 10. Source quality: issue
  trackers, vendor advisories, CVE databases and postmortems before forum
  opinions; each report with its date. Every free model available at run
  time on the same brief; evidence a URL with a retrieval receipt (answer:
  "ja").

Addendum 2026-10-15, run time: with the new cut a run holds about 52 calls
(topic sentence 1; finder 3 plus an Opus merge; topics 1–8 24; topics 9–11
21 with today's seven free models; judge 1). The earlier spec ran every
call in sequence ([DETAIL]). Options shown: A — each stage runs its calls
concurrently, at most four at once per provider (rough estimate 1–1.5 h,
not measured; a queue in the runner, the leak check still before every
call, logs that keep concurrent calls apart); B — all in sequence (rough
estimate 4–8 h); C — in sequence with fewer topics for `feature`. The
maintainer chose A (answer: "A").

## Q-8 · What runs the online topics now that Zen's free tier refuses Pi

asked: 2026-10-15
answer: "Mache A, stelle B für später an" — the online topics 9 to 11 run on OpenCode Go models through Pi; the free models through the OpenCode CLI are deferred to a later bead.
answered_by: maintainer
status: answered
context: |
  Topic: what runs the online research (topics 9 to 11 of the swarm).
  Intention: a call to a free OpenCode Zen model from the maintainer's own Pi answered 403 FreeTierError, "OpenCode's free tier can only be used from within OpenCode" (2026-10-15); without a replacement all three online topics fail.
  Today: spec and code send the free models through Pi; every call would fail with 403. Disguising Pi as OpenCode would break the terms and is not an option.
  Repository change: A — topics 9 to 11 take OpenCode Go models through Pi instead of free models, still with only the Opus sentence and no repository content; B — free models through the OpenCode CLI (`opencode run`), a second program with its own isolation, measurement and pin; C — online topics by Haiku 5.5 only.
  Architecture change: A keeps one path to foreign models (Pi, pinned by coding-harness-agx) and costs subscription quota instead of nothing; B adds a second path whose isolation must be measured anew and whose terms for automated use were not read; C gives up the model comparison on topics 9 to 11.

In the context of a free tier that refuses every client but OpenCode,
facing the choice between Go models through Pi, a second client and Claude
alone, we decided on OpenCode Go models through Pi for the online topics,
to achieve one measured path to foreign models, accepting that the online
research uses subscription quota; the OpenCode CLI path is deferred. — 2026-10-15

This supersedes, for the online topics, the free-model part of Q-1 and of
its addendum of 2026-10-15 (the free roster and Big Pickle's training
terms): no free model is called while this holds. Which Go models take the
online topics is settled next.

## Q-9 · Which Go models take the online topics

asked: 2026-10-15
answer: "A" — DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash (`deepseek-v4.1-flash`, `mimo-v2.6-flash`, `qwen3.8-flash` on OpenCode Go) work topics 9 to 11, three agents per topic.
answered_by: maintainer
status: answered
context: |
  Topic: which OpenCode Go models work the online topics 9 to 11.
  Intention: "all free models" fell away with Q-8; the Go subscription lists 33 models, each with its own monthly limit inside the subscription, and running all of them would spend it fast.
  Today: the spec still names free models; the repository topics 1 to 8 run on DeepSeek Flash, MiMo Flash and Haiku 5.5.
  Repository change: A — DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash, cheap and from three vendors, three agents per topic like topics 1 to 8, 9 calls instead of 21, all through Pi with retrieval receipts; B — the same trio as topics 1 to 8 including Haiku, which runs through Claude Code and lacks the retrieval receipt; C — a fixed list the maintainer picks. In each case `model-endpoints.yaml` turns the free roster into a list of Go models for the online topics.
  Architecture change: none beyond Q-8 — one path through Pi.

In the context of online topics that must leave the free tier, facing the
choice between three cheap Go Flash models, the repository trio with Haiku
and a hand-picked list, we decided on DeepSeek, MiMo and Qwen Flash through
Pi, to achieve three comparable agents per topic with retrieval receipts at
low quota, accepting a third vendor that sees only the Opus sentence. — 2026-10-15

## Q-10 · Whether the free OpenCode Go models return to the online topics

asked: 2026-10-16
answer: "Ja, nur Online-Themen" — the free OpenCode Go models work the online topics 9 to 11 in addition to the three Flash models of Q-9; they see only the Opus sentence and the public web, never repository content (Q-3 stands).
answered_by: maintainer
status: answered
context: |
  Topic: whether the free models that OpenCode Go offers come back into the research swarm, beside the three Flash models.
  Intention: Q-8 dropped the free models because OpenCode Zen's free tier refuses Pi (403); on 2026-10-16 the pinned Pi 1.2.0 listed free models under provider `opencode-go` itself (cat-jam-free, longcat-2.5-preview-free, step-5-preview-free), and the maintainer ruled the same night that the swarms take only Go's free models, never Zen's, checked before every run.
  Today: the spec has the three Flash models alone on topics 9 to 11; the branch's code still carries the older Zen `opencode-free` path.
  Repository change: Options: A — the free Go models join the online topics only; B — they join every topic, so models with unread data terms would see repository content, which Q-3 excluded; C — no change, three Flash models. With A the spec, the ADR 0020 draft and the code change, with the rule of coding-harness-4fk: Pi's catalog refreshed live before the run, provider `opencode-go`, ids ending `-free`, include and exclude lists in `model-endpoints.yaml`.
  Architecture change: part of ADR 0020 (draft): which models work the online topics.

In the context of free models offered by OpenCode Go itself, facing the
choice between adding them to the online topics, adding them everywhere and
leaving them out, we decided to add them to the online topics only, to
achieve more independent public views at no cost, accepting more calls per
run and more work for the judge. — 2026-10-16

## Phase 2a rulings — 2026-10-16, orchestrator (Q-10 redraft)

These are `[DETAIL]` rulings on Opus 5.5's phase-2a rows (`findings.md`, S-1 to S-20). Each stays within the maintainer's answers Q-1 to Q-10 and the research. Each picks the reading that fails closed, keeps the bounded cost and time (`39 + 3N` invocations, 150 minutes, no retries) and can be tested red. The redraft carries them into `spec.md`, with matching changes to `design.md` and `plan.md` where named. No row changes intent, cost or what data leaves the machine, so none is deferred to the maintainer.

(Written by an Opus 5.5 sub-agent and committed unchanged by the orchestrator; the harness's two-space indentation removed. Findings rows stay unchanged; the redraft carries the rulings into the spec.)

- S-1: Reading B. Selected Go free seats add to the run but are not required. A free slot that fails, times out, is refused by the provider or returns no receipt keeps one terminal outcome in the manifest. The judge names it as missing. It does not make the run incomplete. The required contributions are the 39 fixed slots (criterion 37 calls them "mandatory"). Leak-check and declaration refusals still stop the whole run with exit 2 (criterion 12), whichever seat they hit. Reason: the Terms say catalog presence "is eligibility, not proof a model call will succeed". Q-10 adds the free models "in addition to" the trio, and the free list is looked up at run time, not curated. If free seats were required, the maintainer would have to keep excluding dead preview models by hand, which Q-10's runtime rule was meant to avoid. Redraft: define "Required contribution" in Terms as the 39 fixed slots; criteria 18, 39 and the `39 + 3N` [DETAIL] say a failed free slot is recorded and named, never silently dropped, and never makes the run incomplete. New refutation: a failed free slot is missing from the manifest or recorded as successful. Design "Catalog → frozen seats" ("Runtime removals fail their slots") and ADR 0020's consequence on large rosters are worded to match.
- S-2: Reading B. Only `-free` ids in this run's freshly fetched `opencode-go` overlay are eligible. A free id that appears only in Pi's shipped baseline is excluded and recorded as `baseline-only`. Reason: criterion 38 forbids a shipped list standing in for a refresh. The design already says "never reintroduce a removed free id from the shipped baseline". Redraft: Terms «Selected Go free models» and criterion 38 add the refutation "a baseline-only `-free` id is selected or dispatched".
- S-3: An eligible id meets four tests. Its provider is `opencode-go`. Its id ends exactly `-free`. The pinned Pi catalog lists it as a text-input chat model. That catalog also lists it as supporting tool calls, which the `public_search`/`public_fetch` receipts need. The design names the exact pinned-Pi catalog fields from the source it read. A model that fails a test is excluded with its reason recorded (`no-tool-support`, `not-chat`). Reason: without tool calls a seat can only write a report without receipts, which fails anyway (criterion 10). Filtering at preflight spends no invocation on it. Redraft: Terms «Selected Go free models» define "chat id" by these properties; criterion 39 adds the refutation "a model without declared tool support is selected".
- S-4: The character rule follows Q-6's own example. A word is one or more Unicode letters, optionally joined by single internal hyphens or apostrophes ("KI-Agenten-Läufe", "multi-agent" pass). The sentence has at most 20 words, an optional final period, and no digits, underscores, slashes, backticks, dots other than the final one, colons or a lower-to-upper case change inside a hyphen segment. A name list sits on top of this rule. It holds the change name, the bead id, and every tracked path component and file stem in the frozen state that contains a hyphen, underscore, dot or digit. A token on that list is refused, compared whole and case-insensitively. Letters-only words are not compared against symbol names. The exact-prompt leak check stays the second layer. Reason: refusing every hyphen would reject the maintainer's own example. Comparing plain words against every symbol would refuse ordinary language with no source the spec could name. Identifiers with hyphens or other identifier syntax are what carries leakage. Redraft: Terms «Public topic» and criterion 23 state both rules; refutations add "`research-swarm` or a bead id passes" and "the Q-6 example sentence is refused".
- S-5: The run fails fast at the preparatory stages. If any finder, the map merge or the topic sentence fails, or the topic filter rejects the sentence, no further call is dispatched. The run ends incomplete with exit 1, and the judge is not called. In the topic stage, a failed required slot does not stop sibling slots that are already queued or running. The judge, however, runs only if every required topic slot holds a valid report; otherwise the run ends incomplete with exit 1 and no judge. Free-seat failures (S-1) do not block the judge. A filter rejection is a failed structured result (exit 1), not a security refusal. Exit 2 stays reserved for leak-check BLOCKs and declaration/permission refusals, because nothing was sent and the filter worked as designed. Reason: an incomplete run cannot carry a handoff (S-13), so further calls after a dependency failure only spend quota. Redraft: [DETAIL] stage order and criteria 18, 23 and 36 state the stop points, the judge condition and the exit code for a filter rejection; plan step 4 changes "Ordinary call failure permits remaining slots" to cover topic-stage siblings only.
- S-6: On a security refusal, queued slots are cancelled and running children are stopped and reaped, never awaited. Their available partial output and receipts are kept as partial evidence, with outcome `cancelled`, and never count as contributions. Exit 2 takes precedence over exit 1. Reason: this is the design's behaviour ("stop/reap active children … Preserve its available partial output"). The spec must state it so criterion 12 can go red on an awaited child or on exit 1 after a BLOCK. Redraft: criteria 12 and 36 add "running children are stopped; their partial output is retained as `cancelled`; exit 2 wins over 1".
- S-7: The judge's 15 minutes are reserved. A topic slot launches only if the time left on the run, minus the judge reserve, still covers it. Its allowance is the lesser of its role allowance and that remainder. Required slots are dispatched first: repository topics 1–8, then Flash online topics 9–11, by topic number, then by declared seat order. Free seats follow, by topic, then by sorted id. Slots never launched get outcome `not-started-deadline`: incomplete if required, a named missing free seat otherwise (S-1). Reason: worst-case arithmetic gives 26 minutes before the topic stage and 70 minutes for the 25 required Go slots at four permits. So with the reserve, the required graph fits 150 minutes with time left. The 150-minute total is unchanged, and a large free list can only shorten its own share. Redraft: criterion 19 and the deadlines [DETAIL] state the judge reserve and dispatch order; new refutation "a free seat launches before a required one, or the judge has under 15 minutes because topic slots ran into its reserve".
- S-8: The frozen input state is the HEAD commit plus a digest of the working-tree bytes. It covers every tracked file and every untracked, non-ignored file under the change's own folder, recorded in the manifest. The runner keeps a copy of those bytes for the run, and local references resolve against that copy. Before publishing, the runner recomputes the digest and ignores only its own research appends and `updated:` restamp. Any other difference marks the run incomplete with exit 1 and names the changed paths. The outputs are kept. Reason: a HEAD-only state could not resolve uncommitted change inputs. The design already says "a changed frozen input invalidates complete publication". Redraft: criterion 16 defines the state and adds the refutation "a mid-run edit to a frozen file yields a complete run"; Data model "Run manifest" names the digest scope.
- S-9: The check works claim by claim, with a floor for the whole report. A breach of the template or structure rejects the report, and the slot fails (criterion 27). A claim whose local reference does not resolve, or whose URL has no successful page receipt, is kept but marked `unsupported` by the runner. It is not counted as evidence, cannot be scored supported, and does not fail the report on its own. A report fails its slot only if it has no evidence-backed claim. For an online report that means no successful page retrieval at all. Criterion 18's "required retrieval" means that one successful retrieval per online report; single failed fetches are recorded in receipts, not slot failures. Reason: failing a whole slot over one dead link would make complete runs rare without adding safety. A report with no evidence at all must still fail (the "URL-free online report" refutation). Redraft: criteria 10, 16 and 18 state the `unsupported` claim status and the floor for the whole report.
- S-10: Models write report-local ids: `C1`–`C7` for claims and `Q1`… for questions, each unique within its report. A duplicate is a template breach (criterion 27). Each question carries a `claims:` list of one or more local claim ids from the same report. The runner forms global ids `<run>/<topic>/<seat>/<local>`, where the seat id names the endpoint and model. Models never coordinate ids. Handoff items are `H-<n>`, unique per run, each with a list of global source-claim ids. The Q-record fields `research_items:` (run-qualified item ids) and `research_claims:` (global claim ids) sit in the Q-record header beside `answer:`. Criterion 33's "duplicate claim id" means a duplicate global id within a run, or a duplicate local id within a report. Reason: this is the design's data model ("Claim ids combine run, topic, model seat and local id"). It is moved into the spec so criteria 31–33 can be tested. Redraft: Terms «Claim» and «Handoff item», the template under Topic contract (question `claims:`), and criteria 27, 31 and 33.
- S-11: Reading A, with grouping. Coverage is measured against raw reports. Every `[DECISION]` question in every report the runner accepted as valid must be covered by a handoff item. The same goes for every unresolved disagreement in the judge's reconciliation and every class or neighbour item derived under S-16 and S-18. This includes reports or claims the judge scored off-brief or refuted. The judge may group duplicates into one item, keeping every source id. A dropped item can only be resolved by a maintainer answer, and an explicit rejection counts as one (the [DETAIL] already says so). Reason: measuring against the judge's own inventory would hide exactly the loss criterion 31 targets. Grouping limits the number of extra questions, and the maintainer allowed more interview questions in the Q-7 addendum. Redraft: criteria 31 and 32 name raw accepted reports plus judge disagreements as the coverage source; the [DETAIL] "Retain all raw claims…" says so.
- S-12: Reading A. In a change whose v2 run is complete, open handoff items fail the gate (exit 1) only once `spec.md` exists in that change folder. Before then the gate reports them as pending, listed with exit 0. Reason: under Reading B, `make verify` and the stop hook ("blocks on a red tree") would be red between phase 1 and the interview. That blocks an ordinary session end, such as an overnight run waiting for morning answers, without protecting anything more. Once a spec exists, no spec can pass with a lost decision. Redraft: criterion 32 states "once `spec.md` exists" and adds the refutation "a pre-spec change turns verification red"; design "Handoff gate" replaces "research-complete but verification-red" with the pending state.
- S-13: Only complete v2 runs carry obligations and can serve as a basis. A complete run's items remain obligations even after a later run. One answered Q-record may link items from several runs. An incomplete run carries no obligations. A spec criterion that names a claim from an incomplete run fails (criterion 34). If `spec.md` exists and the change has v2 runs, none of them complete, the gate exits 1 ("no complete research run"). Phase 1a and phase 2 start only from a complete run, and the remedy is a new complete run. Reason: this fails closed without asking for an inventory an incomplete run has none of. Accumulating obligations costs one linking step, not new answers. Redraft: criteria 30–32 and 34 and the [DETAIL] "the gate checks every such run" state the rule for complete and incomplete runs.
- S-14: Disposition and the `unique` mark are separate. The runner marks each claim `valid` or `unsupported` (S-9). The judge gives each valid claim exactly one disposition, in this order of precedence: `off-brief` (outside the topic's scope, whether or not true), `supported`, `refuted`, or `unresolved` (a sourced disagreement kept under criterion 15). `unique` is an extra mark, only on supported claims that no peer on the topic shares. Per model and topic, the reconciliation reports the counts and claim-id lists the maintainer asked for (supported, refuted, unique, off-brief), plus unresolved and unsupported. Reason: an exclusive set without `unresolved` would contradict criterion 15. The design already defines unique as "a supported contribution absent from peers". The four requested numbers stay, so Q-7's comparison is unchanged. Redraft: criterion 28 and Terms (new «Disposition»); refutation "a claim has two dispositions, or a unique claim is not supported".
- S-15: Reading A. Once a complete v2 run exists and `spec.md` exists, the gate also resolves two things. First, every criterion's `*Basis:*` line names at least one resolvable global claim id from a complete run, or a Q-record id in the change's `decisions.md`; free text may follow. Second, `neighbours:` contains every confirmed and every header-given neighbour, and no unconfirmed suggestion. The review still judges whether a criterion's rationale fits its basis. A change without a v2 run, such as this redraft, is an exempt case the gate still reports. Reason: the design already has the gate check "neighbour parity and criterion bases". Without that, criteria 30 and 34 cannot go red. Redraft: the review/gate [DETAIL] spells out "identities" as these checks; criteria 30 and 34 name the gate.
- S-16: Two fields are added to the fixed template for these topics. Topic 3 reports must carry `class_assessment: {class, claims}`. When a report's class differs from the declared class, the runner itself derives a `class` handoff item as a `[DECISION]`, without relying on the judge. Topic 6 claims carry `volatile: true|false`. Every volatile claim must carry `governance: central|runtime|dated`, and if one is missing the report fails the template. Whether a model rightly marks a fact as volatile stays a review duty. Reason: these fields carry the fifth guiding questions the maintainer accepted for topics 3 and 6, so a mismatched class or an ungoverned volatile fact can be detected mechanically. Redraft: template under Topic contract, criteria 27, 31 and 35, with refutations "a topic-3 report without `class_assessment` is accepted" and "a differing class yields no handoff item".
- S-17: Refutations get a structural form, and semantic quality is named as a review duty. Criterion 7: the reconciliation lacks one of the sections public practice, architecture or neighbours, or an unread neighbour has no gap entry. Criterion 15: an unresolved disagreement whose opposing claim ids are missing from the published reconciliation, or judge output containing an answer field. Criterion 24: a finder output with fields beyond the four locator lists, or an empty category without an unread marker. Criterion 25: a seat's packet differs from the checked-in prompt for its topic. Whether a finder judges in its prose, whether topic 1 proposes new code, or whether an online report judges local applicability is decided by the judge's `off-brief` disposition and the phase-6 review, stated as such. Reason: a stand-in test can only produce structure, and a refutation that cannot go red is not a criterion. Redraft: rewrite those refutations; add one review-duty sentence under Definition of Done.
- S-18: (1) Every `neighbours:` header entry is checked at preflight. An entry is invalid if it is not a repository-relative `spec.md` path, escapes the repository, is duplicated, or names a file missing from the frozen state. An invalid entry refuses before any model call with exit 2, like a malformed class (criterion 4). A seat's failed read during the run is a named gap, and the run stays complete (criterion 7). (2) A header-given neighbour that topic 5 or the judge finds unrelated becomes a `neighbour` handoff item (`[DECISION]`). It stays in `neighbours:` unless the maintainer answers to drop it. Reason: catching header errors before spending calls fails closed. Keeping a given neighbour until a human answers respects criterion 29. Redraft: the `neighbours:` [DETAIL] and criteria 4, 29 and 30.
- S-19: The private change brief is the same for all three finders and the topic author. It holds the frozen `research.md` (header and body), plus the change's `decisions.md` and `spec.md` when present. The bead is named by id only, and its tracker text is marked not read. The runner embeds `AGENTS.md` identically for all three repository seats. Runtime auto-loading of instruction files is disabled for every seat, so the three contexts are the same (criterion 26). Reason: the existing explore already embeds `AGENTS.md`. The design delegates no tracker reads. Identical packets need one fixed source. Redraft: [DETAIL] stage order and criteria 24 and 26 name the brief's contents; refutation "seats' embedded instructions differ, or a seat auto-loads an instruction file".
- S-20: Reading A. An included id missing from the fresh eligible set makes the catalog preflight exit 1 before any model call. Reason: this fails before any spend, matches the design ("Every explicit include must occur in the fresh eligible snapshot, otherwise exit 1", before dispatch), and avoids 39 or more calls on a run already known to be incomplete. An included model that fails later at call time is handled as a free seat under S-1. Redraft: the include/exclude [DETAIL] says "exits 1 at preflight, before any model call"; criterion 39 adds that refutation.

### Questions for the maintainer

None. Every row is decided within Q-1 to Q-10 and the research.

## Phase 2a rulings, round 2 — 2026-10-16, orchestrator (S-21 to S-30)

These are `[DETAIL]` rulings on Opus 5.5's second phase-2a round (`findings.md`, S-21 to S-30). Each stays within the maintainer's answers Q-1 to Q-10, the research and the round-1 rulings S-1 to S-20. Each picks the reading that fails closed, keeps the bounded cost and time (`39 + 3N` invocations, 150 minutes, no retries) and can be tested red. The redraft carries them into `spec.md`, with matching changes to `design.md`, `plan.md` and the ADR 0020 draft where named. No row is left to the maintainer. One question follows from S-21: what should happen if phase 4 finds that the live catalog has no field for tool support at all. It is listed below. It does not hold up the redraft, because the ruling already fails closed.

(Written by an Opus 5.5 sub-agent and committed unchanged by the orchestrator. Findings rows stay unchanged; the redraft carries the rulings into the spec.)

- S-21: Reading B. Tool support is judged per catalog entry, but only through one declared field. The runner holds one named raw catalog field (and its value) that counts as proof of tool-call support. Phase 4 qualifies that field against real pinned Pi and records the source it read. A fresh overlay entry that lacks the field, or carries a negative value, is excluded as `no-tool-support`. If no field is declared yet, or no entry in the fresh `opencode-go` overlay carries the declared field at all, the catalog's tool support cannot be measured. That is criterion 41's case: preflight keeps the diagnostics and exits 1 (see S-28) before any model call. It is not a measured empty selection under criterion 42. The `compat` flags `supportsAdditionalTools` and `supportsMidConvoToolAdditions` do not count as proof. They describe adding tools in the middle of a conversation, and they appear on only three shipped entries, none of them `-free`. Reason: under Reading A, Q-10 would never take effect, and every run would still report success. Criterion 41 already forbids treating a catalog that cannot be measured as a valid zero selection or as a Flash-only fallback. Read for this ruling, in `tools/pi/node_modules`, pinned Pi 1.2.0 (`@earendil-works/pi-coding-agent/package.json`). First, `pi-ai/dist/types.d.ts`: `BaseModel` and `Model` have no tool-support field, and absent `type` means chat. Second, `pi-coding-agent/dist/core/remote-catalog-provider.js`: `parseCatalog` keeps each entry's raw fields and checks none of them for tool support. Third, the shipped baseline `pi-ai/dist/providers/data/opencode-go.json`: no entry carries a tool-support field, and it lists two `-free` ids (`longcat-2.5-preview-free`, `step-5-preview-free`), which S-2 already excludes as `baseline-only`. Not read: a live remote overlay. So whether the remote catalog has such a field is unknown. Redraft: Terms «Selected Go free models» name the declared field as the only proof. Criterion 41 adds the refutation "an overlay without the declared tool-support field, or with no field declared, yields a valid `N=0` instead of preflight exit 1". Criterion 42 says a measured empty selection needs a tool-support field that was measured. Design «Catalog → frozen seats» replaces "inspect raw catalog capability metadata" with this one declared field and says that the `compat` tool flags are not proof. Plan, catalog step: fixtures for a declared field that is present and true, absent on one entry, false on one entry, absent from every entry, and not declared.
- S-22: Reading A, made explicit. The retained copy lives in the run's scratch directory outside the repository. It is made before the first model call, used to resolve every local reference and to recompute the digest (S-8), and deleted after publication or abort, together with the other scratch files. The durable record is the manifest: HEAD, one digest over all frozen bytes, and for the untracked change-folder files a list of paths with one digest per path. No copy of a file goes into `research.md`, into the change folder or into any brief. If the copy cannot be made, preflight exits 1 before any model call. Reason: a durable copy inside the change folder would make every run incomplete. Appending it to `research.md` would add the whole tracked tree on each run and carry it to the finders and the topic author through the next brief. Tracked bytes can be checked again later from HEAD. The per-path digests let a reader check the uncommitted inputs once they are committed. Redraft: Terms «Frozen input state» say "kept in run scratch for the run, then deleted; HEAD and digests persist". Criterion 16's refutation "the retained bytes/reports are absent" becomes "a local reference resolves against the live working tree instead of the run's copy, or a report is absent". It adds the refutation "research.md or the change folder contains a copy of a frozen file". Data model «Run manifest» lists the per-path digests. Design «Finder → map» names scratch as the copy's place.
- S-23: Reading B, narrowed to `supported`. Every global claim id that a criterion's `*Basis:*` line names must belong to a complete run and carry the judge disposition `supported`. A Basis naming any claim that is `unsupported`, `refuted`, `off-brief` or `unresolved` fails the gate with exit 1, even if another named id is supported. A criterion that rests on such a claim needs a maintainer-answered Q-record as its basis. The maintainer can link that claim through `research_claims:`. Reason: the Terms say unsupported claims are never evidence. A refuted claim is contradicted, and an off-brief claim lies outside its topic. An unresolved disagreement is a human decision (S-11), so its answer is the right origin. Refusing a mixed Basis keeps a weak id from riding along with a strong one. Redraft: criterion 34 says "a supported global claim from a complete run" and adds the refutation "a Basis naming an unsupported, refuted, off-brief or unresolved claim passes". The gate [DETAIL] (review/gate identities) says the same.
- S-24: A field is added for topic 5, built the same way as the S-16 fields. Every repository topic-5 report must carry `neighbour_relations`. This is a list with exactly one entry per neighbour in that seat's packet, given or suggested. Each entry has `path`, `relation` (`related`, `unrelated` or `contradicts`) and a nonempty local `claims` list. A packet neighbour with no entry, a path outside the packet, a duplicate path or an empty `claims` list is a template breach (criterion 27). From these fields alone, the runner derives a `neighbour` handoff item marked `[DECISION]` in two cases: any `contradicts` entry, and an `unrelated` entry for a header-given neighbour. It does not depend on the judge. The judge's own structured neighbour findings can add items (S-18), but they can never remove one. The free-prose section «relation to neighbouring specs» stays for the other topics. Online reports still mark neighbour relations as not assessable. Reason: the [DETAIL] requires a derivation that does not depend on the judge, and only a fixed field makes it mechanical. One entry per packet neighbour also makes a silent omission visible. Redraft: the template under Topic contract adds `neighbour_relations` for topic 5. Criteria 27, 29 and 31 add the refutations "a topic-5 report without an entry for a packet neighbour is accepted" and "a `contradicts` entry, or an `unrelated` entry for a given neighbour, yields no handoff item". Data model «Topic report» names the field.
- S-25: The merge keeps every finder entry. An entry's key is its category plus its exact `path::symbol` or `path::section`. The merged map must hold exactly the set of keys the three finders listed, without duplicates. Entries with the same key become one entry that lists every originating finder and every reason. A merge that omits a finder key or adds a key no finder listed is not a valid result. Under S-5 that is a preparatory failure: no topic is dispatched, and the run ends incomplete with exit 1. The runner, not Opus, resolves every entry against the frozen state, as under criterion 16. An entry that does not resolve stays in the map with the mark `unresolved`, does not count as mapped scope for topics 1 to 8, and does not fail its finder. The runner itself enters every header-given neighbour into the map's neighbour list with status `given`, whatever the finders or the merge listed. A merge entry that lists a given path as a suggestion is recorded as `given`. Reason: topics 1 to 8 are bounded to the map, so a drop or an addition by the merge would silently change every topic's scope. Resolving entries in the runner keeps the frozen-state check the same for map and claims. Given neighbours are validated inputs (S-18), not merge output. Redraft: criterion 5 defines "valid merge" as this exact union. Criterion 24 adds that the runner resolves entries. New refutations: "a merge that drops or adds a key lets a topic start", "an unresolved entry is handed to a topic as mapped scope" and "a given neighbour is missing from the map". Design «Finder → map» and Data model «Map» state the key, the `unresolved` mark and the runner-inserted `given` entries.
- S-26: An allow-list, closer to Reading B. The sentence may contain only Unicode letters, whitespace, and these separators: comma, semicolon, parentheses, straight and typographic double quotation marks, guillemets, a stand-alone en or em dash between spaces, and one final period or question mark. A straight apostrophe or the typographic apostrophe ’ joins a word only when a letter stands on both sides. At the edge of a word it counts as a quotation mark. Words are the letter runs left once the separators are removed. The S-4 rules apply to each word, and the 20-word limit counts only words. Every other character is refused, including digits, underscores, slashes, backticks, colons, other dots, `@`, `#`, `=`, `<`, `>`, brackets and braces. The name list (S-4) and the exact-prompt leak check are unchanged. Reason: an allow-list fails closed for every character the spec did not foresee. The allowed separators cannot carry a path or an identifier. Refusing a comma would end ordinary German sentences with exit 1 after five model calls, and gain no safety. Redraft: Terms «Public topic» list the allowed separators and the apostrophe rule. Criterion 23 adds the refutations "«Isolation, Prüfung und Wiederherstellung für Agentenläufe» is refused" and "a sentence containing `[`, `{`, `@`, `=` or a digit passes".
- S-27: Reading A (parity), with one addition that mirrors the drop rule. Once a spec exists for a change with a complete v2 run, `neighbours:` must equal the confirmed and given neighbours, plus any neighbour a linked maintainer-answered Q-record adds, minus any given neighbour such a record drops. A path that is in none of these sets fails with exit 1. That includes a path the phase-2 author found while drafting. The author records it as a `[DECISION]` for the maintainer, or starts a new complete run that confirms it. Reason: S-15 already reads "identities" as parity. Under the criterion's list alone, an unreviewed path could enter the header simply because no finder ever named it. A maintainer answer is the same authority that may already drop a given neighbour. Redraft: criterion 30 states the parity sets and adds the refutation "a header path that is neither confirmed, given nor added by a linked maintainer answer passes". The gate [DETAIL] and design «Handoff gate» say the same. The Q-record header link uses the existing `research_items:` field.
- S-28: Exit 1. Every case under criterion 41 (timeout, refresh error, a stale-only, malformed or ambiguous catalog, and the tool-support case of S-21) keeps the diagnostics and exits 1 before any model call. Reason: the design already says "fails before model dispatch (exit 1)", and S-20 gives a missing explicit include the same code. In the runner, exit 2 means it refused a call it would not send, and exit 1 means a failed result (`scripts/stage2.py`, the refusal and failure classes near lines 435 and 439, read). Exit 3, "not measured", is the convention of the gates (criterion 33), not of the runner. Redraft: criterion 41 replaces "exits nonzero" with "exits 1", and its refutation adds "a catalog failure exits 0, 2 or 3". ADR 0020's consequence line "exit nonzero" is worded to match.
- S-29: The three Opus roles (map merge, topic author and judge) run with no tools. Their Claude Code launch passes an empty tool list, with the restricted, safe-mode and strict MCP flags the runner already uses (`scripts/stage2.py`, the `--tools` launch arguments near line 1744, read). Each role sees only its packet. To let the judge check content without tools, the runner adds to each valid claim the evidence it resolved: the cited symbol or section text from the run's frozen copy for a local claim, and the receipt excerpt for a public claim. Each excerpt is capped at a fixed size, and a truncated excerpt is marked as truncated. The design fixes the cap. So `supported` means "the attached evidence supports the statement and no peer claim with evidence contradicts it". Reason: a role with file tools would read the live working tree, not the frozen state. The topic author could read past the brief, and that text could reach the public sentence that goes to outside models (Q-3, Q-6). Without tools, the judge's inputs can be listed in full and tested. The attached excerpts add no invocation, and they go only to Opus, which already receives these reports. Redraft: criteria 14, 23 and 28 state that the Opus roles have no tools and that excerpts are attached. New refutations: "an Opus role launches with any file, shell, web or MCP tool" and "the judge packet lacks a valid claim's resolved excerpt". Terms «Evidence status and disposition» define `supported` as above. Design «Reports → judge» names the excerpt cap.
- S-30: The 12-hour stop counts phase-4 time as `prompts/04-implement.md` defines it. Time used is the sum of the measured historical spans under «Earlier implementation time» in `plan.md` plus every span appended later under `## Time used`. The 2026-10-15 "repair attempt 3" span was not measured. Before any phase-4 work, the first phase-4 session tries to establish that span from recorded times: the start and end of that attempt's runner audit record, or failing that, its commits' timestamps. It writes the result and its source as a new line. If no record bounds the span, the session raises the appetite stop at once (`found:` "time used not measurable"). Only the maintainer can answer it with *continue* and a new total. Drafting work in phases 2 and 3 does not count. Reason: the prompt forbids estimating time. Counting the unmeasured span as zero would let phase 4 run past its stop, so the fail-closed outcome is the stop itself, which the maintainer answers. Measured on 2026-10-16 from `plan.md` at `42e5975`: the three measured entries sum to about 78 minutes (about 16, 11 and about 51 minutes); the fourth is unmeasured. Redraft: the spec's [DETAIL] «Keep the architectural class, ADR 0020 and 12-hour phase-4 stop» states this computation. The plan's «Earlier implementation time» names the evidence sources to try and the stop that applies if none bounds the span.

### Questions for the maintainer

- Topic: what happens if the live catalog has no field for tool support (follows from ruling S-21).
Intention: with S-21, a free Go model joins the online topics only if the fresh catalog shows that it supports tool calls. Without tool calls it cannot fetch web pages or produce receipts. If phase 4 finds that the live catalog has no such field at all, no run could pass the catalog check.
Today: pinned Pi 1.2.0 has no tool-support field in its model interface. The shipped Go catalog has none on any entry. The live remote catalog was not read, so this is not yet known.
Repository change: A — keep S-21. Until a field exists, every swarm run stops before any model call with exit 1, including the 39 fixed slots. B — if the catalog has no such field, record it, run the 39 fixed slots, and start no free seat (a recorded `N=0` with the reason "tool support not measurable"). C — if the catalog has no such field, admit chat models with text input anyway. A free seat that cannot make tool calls then fails as a best-effort slot (S-1) and costs at most three free calls.
Architecture change: none. All three stay within the `39 + 3N` invocations and 150 minutes, and send no new data. A blocks the whole research swarm on a missing catalog field. B quietly makes Q-10 depend on the catalog. C reverses part of ruling S-3. Recommendation: B, because the swarm keeps running and the missing free models stay visible in every run's record.
Should a run without a catalog tool-support field stop entirely (A), run without free models and record why (B), or let free models try anyway (C)?

## Q-11 · Where tool support for a free Go model is read

asked: 2026-10-17
answer: "D" — a free Go model is eligible when it is in this run's fresh Pi catalog for `opencode-go`, and models.dev lists it under `opencode-go` with `tool_call: true` and without `status: deprecated`. A model missing from models.dev, or every free model when models.dev cannot be reached, is excluded with its reason recorded; the 39 fixed slots still run (option B as the fallback).
answered_by: maintainer
status: answered
context: |
  Topic: how the runner knows that a free Go model can make tool calls, which the online topics need for retrieval receipts (follows from ruling S-21).
  Intention: ruling S-21 admits a free model only on a declared catalog field for tool support; if no catalog has one, no run passes the catalog check.
  Today (measured 2026-10-17 by the orchestrator, both public GETs without credentials): Pi's live catalog (`https://pi.dev/api/models/providers/opencode-go?types=chat,image,classifier`, the URL pinned Pi 1.2.0 requests; Last-Modified 2026-10-16 12:41 GMT) holds 29 models, two of them `-free` (`cat-jam-free`, `longcat-2.5-preview-free`), and no entry has a tool-support field (fields: api, baseUrl, compat, contextWindow, cost, id, input, inputLimits, maxTokens, name, provider, reasoning, thinkingLevelMap, type). models.dev (`https://models.dev/api.json`, the model database OpenCode builds on) lists four `-free` ids under `opencode-go`, each with `tool_call: true`; `cat-jam-free` and `step-5-preview-free` carry `status: deprecated`. Under D only `longcat-2.5-preview-free` would be eligible on that day.
  Repository change: A — keep S-21 as ruled: with no field anywhere, every swarm run stops at preflight, the 39 fixed slots included; B — without a field, run the 39 fixed slots, start no free seat, record `N=0` with the reason; C — admit text-input chat models anyway and let a seat without tool calls fail as a best-effort slot; D — read tool support and deprecation from models.dev, cross-checked against the fresh Pi catalog, with B as the fallback when models.dev is missing or unreachable.
  Architecture change: D adds a second public read (models.dev) to the catalog preflight; it sends no repository data and keeps `39 + 3N` invocations and 150 minutes.

In the context of free Go models that need tool calls for retrieval
receipts, facing a Pi catalog without a tool-support field, we decided to
read tool support and deprecation from models.dev, cross-checked against
the fresh Pi catalog, to achieve an automatic filter of dead preview models,
accepting a second public source in the preflight and the fixed slots alone
when it fails. This answer replaces the single-field rule of ruling S-21;
the rest of S-21 (fail closed, a reason recorded per excluded model) stands.
— 2026-10-17

## Phase 2a rulings, round 3 — 2026-10-17, orchestrator (S-31 to S-39)

These are `[DETAIL]` rulings on Opus 5.5's third phase-2a round (`findings.md`, S-31 to S-39). Each stays within the maintainer's answers Q-1 to Q-11 and the earlier rulings S-1 to S-30. Each picks the reading that fails closed, keeps the bounded cost and time (`39 + 3N` invocations, 150 minutes, no retries) and can be tested red. The redraft carries them into `spec.md`, with matching changes to `design.md`, `plan.md` and the ADR 0020 draft where named. No row is left to the maintainer. Read for these rulings: the round-3 rows in `findings.md`; `spec.md` in full; in `decisions.md`, Q-7 with its topic-6 walk-through, Q-11, and the rulings S-2 to S-30; `design.md`, section «Interfaces»; `plan.md`, steps 2 to 4; the ADR 0020 draft by search only; `scripts/stage2.py`, `declared_class` and `explore`; and the two catalog files measured on 2026-10-17 (Pi's live `opencode-go` catalog and models.dev's `api.json`). Not read: `research.md` beyond a search, Q-1 to Q-6 and Q-8 to Q-10 in full, the earlier findings rows, the design's «Data model» in full, the pinned Pi sources in `tools/pi/node_modules` (this round relies on S-21's reading of them), and any credential file.

(Written by an Opus 5.5 sub-agent and committed unchanged by the orchestrator. Findings rows stay unchanged; the redraft carries the rulings into the spec.)

- S-31: Reading A, the union, with a human item for every conflict between runs. The required neighbour set is built from every complete v2 run of the change, not only the latest. A path is required if any complete run confirmed it, or if any complete run's manifest lists it as given. Two cases create a `neighbour` handoff item marked `[DECISION]`, derived by the runner and not by the judge. First, one complete run confirms a path and another rejects it. Second, a path given in an earlier run's header is missing from a later run's header. Such a path stays required until a linked maintainer-answered Q-record drops it. The existing drop rule therefore covers confirmed paths as well as given ones. Reason: S-13 keeps every complete run's obligations across later runs, and S-18 keeps a given neighbour until a human answers. Under Reading B, a later run could silently remove a path that an earlier run made required. Test: run 1 confirms suggestion P and run 2 rejects it. Without a linked answer, the gate exits 1 whether or not the header contains P, because the item is open. With an answer that keeps P, only a header with P passes. With an answer that drops P, only a header without P passes. Redraft: criterion 30 says "confirmed or given in any complete run, plus linked maintainer additions, minus linked maintainer drops of given or confirmed paths". It adds the refutations "a path confirmed in an earlier complete run and rejected in a later one yields no handoff item" and "a given path removed from a later header leaves the required set without a linked maintainer drop". Criteria 29 and 31 name the two cross-run items. The [DETAIL]s «Version manifests research-swarm/v2» and «exact neighbour parity», and design «Handoff gate», say the same.
- S-32: Reading B, bounded. After the map merge and before topic dispatch, the runner collects topic 6's history itself. It reads git read-only, against the frozen HEAD, with no network and no tracker. For each resolved mapped path it takes at most the ten most recent commits that reach that path from frozen HEAD. For each commit it records the full hash, the UTC author date, the subject, the body capped at 4,000 characters with a truncation flag, and the mapped paths the commit touches. Older commits are listed as not read for that path. All three topic-6 seats receive this history in the same packet (criterion 26). No other topic receives it, and nothing from it goes online (criterion 8 already names history canaries). A topic-6 claim may cite a full commit hash as evidence. It resolves only if that hash appears in the seat's packet history, and the runner attaches the commit's record as the excerpt. A hash that is reachable but not in the packet is `unsupported`, because topic 6 is limited to mapped history. PR numbers and bead ids are not evidence sources, because neither GitHub nor the tracker is read (S-19). They may appear in a statement, and a commit that names them (for example "(#104)" or a `Closes-Bead:` trailer) carries them. A claim citing only a PR number or bead id is `unsupported`. Handover files and other repository records remain `path::section` evidence. If the history cannot be collected, that is a preparatory failure under S-5: no topic is dispatched, and the run ends incomplete with exit 1. Reason: the design already says "History is collected by the runner because read-only Pi tools cannot execute git" and "Tracker-backed history not already in the worktree is marked not read". Without a packet, Reading A would leave topic 6 with nothing it could cite. The collection adds no model invocation. Test: a topic-6 claim citing a commit hash from the packet is valid and carries that commit's excerpt. A reachable hash outside the packet, or a claim citing only `#104` or a bead id, is `unsupported`. A failed git read starts no topic and exits 1. Redraft: Topic contract row 6 names the runner-collected history and the commit-hash evidence form. Terms «Claim» list the evidence forms: `path::symbol`, `path::section`, a packet commit hash for topic 6, and a receipt-backed URL. Criterion 16 adds the refutations "a commit hash absent from the topic-6 packet, or a PR number or bead id alone, is valid evidence" and "a history-collection failure lets a topic start". The excerpt [DETAIL] names the commit record as an excerpt. Design «Map → topic contexts» states the bound of ten commits per path and the 4,000-character body cap. The plan, step 3, adds fixtures for these cases.
- S-33: Reading A, with the document-level faults named. The whole models.dev result is `capability-unavailable`, and every free candidate is excluded, in exactly these cases: the request fails or times out; the response is not HTTP 200; the body is not JSON, or its top level is not an object; `opencode-go` is missing or is not an object; or its `models` is missing or is not an object. Two entries under `opencode-go.models` that claim the same id are also this case, as identity ambiguity. Every other fault is judged per candidate, and only that id is excluded. A missing entry is `metadata-missing`. An entry that is not an object, a `tool_call` that is not a boolean (a string, null or a number), a present `status` that is not a string, or an entry `id` that differs from its key, is a new reason, `metadata-malformed`. The raw value is recorded. `tool_call: false` stays `no-tool-support`, and `status: "deprecated"` stays `deprecated`. Entries of other providers are not inspected. Reason: only a boolean `true` admits a candidate, so a malformed entry can never admit itself. Its fault says nothing about another candidate's valid entry. A missing `opencode-go` key is document-level, because otherwise every candidate would be recorded as "missing", which would read as a measured empty selection. Criterion 42 keeps that apart from capability-unavailable. Test: candidate X has `tool_call: "true"` and candidate Y has `tool_call: true`. N is 1, Y is selected and X is excluded as `metadata-malformed` with the value `"true"`. Without the `opencode-go` key, N is 0 with the reason capability-unavailable. Redraft: the [DETAIL] «Preflight validates class and given neighbours» replaces "malformed/unreachable metadata excludes all" with this list. Terms «Selected Go free models» add `metadata-malformed`. Criterion 42 adds the refutations "a non-boolean `tool_call` admits a seat" and "one malformed candidate entry excludes a validly marked candidate". Design «Catalog → frozen seats» adds the reason to its list. The plan's catalog fixtures cover each document-level and each per-entry case.
- S-34: One 60-second deadline for both reads, judged by which source is unfinished. The runner starts the Pi refresh and the models.dev request at the same time, and both share the deadline that starts with preflight. When the deadline passes, both requests are aborted, with no retry. If Pi has not returned a successful fresh snapshot by then, that is criterion 41's case: diagnostics are kept and preflight exits 1 before any model call, whatever models.dev did. If Pi succeeded and models.dev did not finish, models.dev is `capability-unavailable` with the reason "timeout". N is 0, the 39 fixed slots run, and a missing explicit include still exits 1 (S-20). Reason: Q-11 says that when models.dev "cannot be reached", every free model is excluded and the 39 fixed slots still run. Under Reading B, a slow models.dev would block the whole run and so reverse that answer. Running the two reads at the same time keeps models.dev from using Pi's time. The deadline stays within the 150 minutes. Test: Pi answers in 5 seconds and models.dev never answers. At 60 seconds the request is aborted, N is 0 with "timeout", and the 39 fixed slots are dispatched. Pi never answers and models.dev answers in 1 second: exit 1 with no model call. Redraft: the budget [DETAIL] says "catalog 60 seconds, both reads started together; at the deadline an unfinished Pi read exits 1 and an unfinished models.dev read is capability-unavailable". Criterion 41 adds the refutation "a successful Pi refresh with an unfinished models.dev read exits 1". Criterion 42 adds the refutation "a models.dev timeout delays the fixed slots beyond the 60-second deadline or exits nonzero by itself". Design «Catalog → frozen seats» and ADR 0020 («Both catalog reads share 60 seconds») say the same.
- S-35: Reading A, widened to the neighbour's change folder. A packet neighbour is always a change, named by its `spec.md` path, as a given neighbour already is (S-18). A resolved entry in the neighbour category counts as a suggestion for `plans/changes/<name>/spec.md` when its path lies in that change folder and that `spec.md` exists in the frozen state. This covers `spec.md`, `design.md`, `plan.md`, `decisions.md` and `research.md`. All entries for the same change merge into one packet neighbour, keeping every key. A neighbour-category entry outside a change folder, or in a folder without `spec.md`, gets no neighbour status. It stays a map entry marked `no-spec`, and the reconciliation's neighbour section lists it as a gap. Unresolved entries confer no status (S-25). Reason: topic 5's boundary already reads the neighbours' spec, design, plan and decisions. A finder that cites `design.md` therefore names that change. Under Reading B, a `design.md` path would enter the spec's `neighbours:` header, which takes only `spec.md` paths. Under pure Reading A, the suggestion would be lost without notice. Test: an entry `plans/changes/foo/design.md::Data model` with `foo/spec.md` present yields the packet neighbour `plans/changes/foo/spec.md`. A topic-5 report without a relation for that path is rejected. Without `foo/spec.md`, the entry is marked `no-spec` and listed as a gap, and no relation is required. Redraft: the finder paragraph of the Topic contract states this mapping and the `no-spec` mark. Criterion 29 adds the refutation "a neighbour suggestion outside any change with a spec becomes a packet neighbour, or one inside such a change is dropped without a gap entry". Criterion 27's topic-5 rule refers to these packet neighbours. Design «Finder → map» and Data model «Map» name the `no-spec` mark.
- S-36: Reading B, with an explicit empty list allowed. `research.md`'s header must carry `neighbours:`. An empty list, `neighbours: []`, means no given neighbours, and the run goes on with finder suggestions only. A missing key, `null`, or any value that is not a list refuses before any model call with exit 2. The refusal message says to add `neighbours: []` or the list of neighbour specs. Reason: Q-7's addendum puts the given neighbours in that header. A forgotten header would otherwise read as "none" without notice, and the maintainer's knowledge of a neighbour would be lost. The refusal costs no invocation, and the fix is one header line. This matches a missing class, which also refuses with exit 2 (`declared_class` in `scripts/stage2.py`, read). `explore` already requires `research.md` to exist with a bead in its header (`preflight` with `bead_file="research.md"`, read), so the key has a place on every swarm run. Test: a feature change without the key exits 2 before any call, and the same change with `neighbours: []` dispatches the finders. Redraft: criterion 4 says "a missing or non-list `neighbours:` key" and adds the refutations "a missing `neighbours:` key starts a call" and "`neighbours: []` is refused". The [DETAIL] «Preflight validates class and given neighbours» says the same. The plan adds the key to `docs/WORKFLOW.md`'s phase-1 description and to the kit's phase-1 instructions, so a new change can find it.
- S-37: Preflight exit 1. Every fixed `opencode-go` model of a required role must be in this run's freshly fetched overlay as a text-input chat model. These are `deepseek-v4.1-flash`, `mimo-v2.6-flash` (finder, repository and online) and `qwen3.8-flash` (online). A fixed id that is absent, present only in the shipped baseline, or not a text-input chat model, keeps the diagnostics and exits 1 before any model call. The reason is `fixed-model-unavailable`, and the id is named. models.dev is not consulted for fixed models, so a models.dev failure still never blocks them (Q-11). Haiku 5.5 runs through Claude Code and is outside this check. Reason: a required slot known to fail would spend up to `36 + 3N` other calls on a run that cannot complete. S-20 already stops for a missing explicit include on the same ground. Measured 2026-10-17 from Pi's live `opencode-go` catalog file (29 entries, Last-Modified 2026-10-16 per Q-11): all three fixed ids are present, so this rule would not have stopped a run that day. Test: a fresh overlay without `qwen3.8-flash`, or with it only in the shipped baseline, exits 1 with no model call. Redraft: criterion 38 adds "and every fixed Go model of a required role appears in the fresh overlay as a text-input chat model". It adds the refutation "a fixed Go model absent from the fresh overlay, or present only in the baseline, lets any model call start". Criterion 41 lists `fixed-model-unavailable` among its exit-1 cases. Design «Catalog → frozen seats» and the plan's catalog step add the check and its fixture.
- S-38: A size limit on the whole judge packet, checked before the call, with no shortening. The excerpt cap of 4,000 characters applies per claim, not per cited source. A claim with several sources gets their excerpts joined in citation order and cut at 4,000 characters in total, with the truncation flag set. The design fixes one packet limit in characters. Phase 4 derives it from the context size that pinned Claude Code documents or reports for Opus 5.5, minus a fixed share for the judge's output, and records the source and date. Before the judge call, the runner measures the assembled packet. If it exceeds the limit, the judge is not called. The run ends incomplete with exit 1 and the reason `judge-packet-over-limit`, and every report and excerpt is kept. Excerpts are never shortened to fit, N is never reduced, and no second judge call is added. Reason: the design already says "If reports exceed the actual context capacity, retain them and mark the run incomplete rather than truncating evidence or adding undeclared judge calls". The ADR draft says the same ("no silent truncation of models/reports to fit the deadline or judge context"). A cap per claim makes the excerpt share predictable: at most 28,000 characters per report. Not read: the actual context size of Opus 5.5. This ruling therefore names no number for the limit. Test: a fixture packet one character over the limit makes no judge call and exits 1 with that reason. At exactly the limit, the judge is called. A claim with three 4,000-character sources gets one excerpt of 4,000 characters, marked truncated. Redraft: the [DETAIL] «Opus map merge, topic author and judge have empty tool lists» says "capped at 4,000 Unicode characters per claim" and names the packet limit and its outcome. Criterion 14 adds the refutation "a packet over the recorded limit reaches the judge, or its excerpts are shortened beyond the per-claim cap to fit". Criterion 18 names `judge-packet-over-limit` as an incomplete outcome. Design «Reports → judge» states the limit, its recorded source and the per-claim cap. Data model «Run manifest» records the limit and the measured packet size.
- S-39: The models.dev record becomes refutable at every N. Criterion 38 records, beside the Pi refresh, the models.dev outcome: the source URL, UTC time and response digest, or the failure and its reason. It also records each free candidate from the fresh Pi overlay with its id, whether it was selected, and for each excluded one its reason and the source field and value. Reason: Q-11 says an excluded model keeps its recorded reason, and the [DETAIL] already asks for the source, time and digest. Neither can go red today unless N is 0. Measured 2026-10-17 from the two catalog files: the row's case is that day's case. Pi lists `cat-jam-free` and `longcat-2.5-preview-free`, and models.dev marks `cat-jam-free` as `status: deprecated` with `tool_call: true`. Test: with that input, N is 1, and a manifest that lacks models.dev's source, time or digest, or lacks `cat-jam-free` with `deprecated` and its field value, fails. Redraft: criterion 38 names the models.dev source, time and digest or failure, and the per-candidate outcome and reason. It adds the refutation "the manifest lacks the models.dev source, time and digest or failure, or any excluded candidate lacks its reason and source value, at any N". Criterion 39's test list and the plan's catalog fixtures add this case. Design «Catalog → frozen seats» already lists these fields and needs no change.

## Phase 2a rulings, round 4 — 2026-10-17, orchestrator (S-40 to S-46)

These are `[DETAIL]` rulings on Opus 5.5's fourth phase-2a round (`findings.md`, S-40 to S-46). Each stays within the maintainer's answers Q-1 to Q-11 and the earlier rulings S-1 to S-39. Each picks the reading that fails closed, keeps the bounded cost and time (`39 + 3N` invocations, 150 minutes, no retries) and can be tested red. The redraft carries them into `spec.md`, with matching changes to `design.md`, `plan.md` and the ADR 0020 draft where named. No row is left to the maintainer.

The neighbour rules are now the main source of new ambiguity: five of this round's seven rows, after three of nine in round 3 (S-31, S-35, S-36). The gaps are in the mechanics, not in the intent, and one simpler rule within Q-7 closes them: the runner alone derives a suggestion's status from the three topic-5 relations, every split between seats goes to the maintainer (Q-7 already sends disagreements between models to the interview), a maintainer answer carries its keep, drop or add in a structured field, and only three named spec path forms count. A further simplification, letting the maintainer accept every suggestion by hand, would change who decides and would replace only S-40, which can be ruled without it, so it is not asked.

Read for these rulings: the round-4 rows in `findings.md`; `spec.md` in full; `decisions.md` in full (Q-1 to Q-11 and S-1 to S-39); `design.md`, «Interfaces» (caller → router, finder → map, reports → judge, research → interview → spec, handoff gate) and «Data model»; `plan.md`, steps 3 and 9 by excerpt, the file table and the criterion ledger by search; the ADR 0020 draft by search only; `scripts/stage2_swarm.py`, `symbol_problem` and `citation_problems`; `docs/WORKFLOW.md`, «Artefact lifecycle»; and the folder listing under `plans/` and the `spec.md` files in the tree at `c0687a7`. Not read: `research.md`, the earlier findings rows, the other plan steps, the ADR draft in full, the pinned Pi sources, the live Pi and models.dev catalogs (S-44 needs no new measurement; S-33's reading stands), and any credential file.

(Written by an Opus 5.5 sub-agent and committed unchanged by the orchestrator. Findings rows stay unchanged; the redraft carries the rulings into the spec.)

- S-40: Reading B, by unanimity, with every split going to the maintainer. In each complete run, the runner alone sets the status of each suggested packet neighbour from the three topic-5 relations. All three topic-5 seats are required, so a complete run always holds three relations per packet neighbour. `confirmed` means all three seats say `related` or `contradicts`. `rejected` means all three say `unrelated`. Any other mix is `split`. A split derives a `neighbour` handoff item marked `[DECISION]`, independently of the judge. A `contradicts` counts toward confirmation and still derives its own item (S-24). The judge's reconciliation describes relevance, but it never sets or changes a status. It can add a neighbour item but cannot close one (S-24). A split path is not required and may not enter the header until a maintainer answer keeps it (S-41). Header-given paths keep the status `given`; their relations only derive items, as S-24 already rules. Reason: Q-7's addendum turns disagreements between models into interview questions. A status taken from the judge would let one model's prose overrule three seat fields, which S-24 forbids for removals. "Any seat confirms" would let a single seat make a path required. Unanimity also gives S-31's cross-run conflict a defined meaning: one complete run `confirmed` and another `rejected`. Test: P gets `related`, `unrelated`, `related`, and the judge calls P confirmed. P is `split` and an open item exists. Once `spec.md` exists, the gate exits 1 with or without P in the header. After a maintainer record keeps P, only a header with P passes. Redraft: Terms add «Neighbour status» (`given`, `confirmed`, `rejected`, `split`, derived by the runner from topic-5 relations only). Criterion 29 adds the refutations "a suggestion with any `unrelated` seat counts as confirmed", "a split yields no human item" and "a judge verdict sets or changes a neighbour status". Criterion 30's "confirmed" refers to this status. Criterion 31 lists the split item. The [DETAIL]s «Version manifests research-swarm/v2» and «exact neighbour parity», design «Research → interview → spec» and «Handoff gate», Data model «Handoff» (reason `neighbour`, kind `split`) and the plan's step-9 fixtures say the same.
- S-41: A structured field, never the answer text. A Q-record that settles neighbours carries a header field `research_neighbours:` with up to three lists of spec paths: `keep`, `drop` and `add`. The recording session writes it from the maintainer's stated answer, beside the free-text answer, as it already writes `research_items:`. The gate reads only this field. Five rules. First, a neighbour item (contradiction, unrelated given path, split, or either cross-run conflict) closes only through a maintainer-answered record that links it in `research_items:` and names its path in `keep` or `drop`. A linked record that names the path in neither list leaves the item open, and the gate exits 1. Second, `keep` and `add` put a path into the required set; `drop` takes it out, whether it was given, confirmed or split. Third, `add` needs no item link. It covers a path found while drafting, and it must stand in a maintainer-answered record of this change. Fourth, a path in two lists of one record, or kept in one answered record and dropped in another, is ambiguous and exits 3 (criterion 33). Fifth, every path in the field must have one of the three neighbour forms of S-43, otherwise exit 1. The gate checks the form, not the file's existence, so a neighbour that is archived later does not turn a finished spec red. Reason: reading the answer text would be the automatic semantic grading the Non-goals exclude. Reading B would let any linked answer close an item while the header ignores it, which fails open. Q-7's addendum leaves "the exact field form and its check" to the spec, so a structured field stays within it. Whether the field matches the answer stays a phase-6 review duty, as for `research_items:`. Test: given path P gets `unrelated` from one seat, and the linked answer says "P bleibt Nachbar" with no field: exit 1. With `keep: [P]`, only a header with P passes. With `drop: [P]`, only a header without P passes. A maintainer-answered record with `add: [X]` lets X pass; X without such a record exits 1. `keep: [P]` and `drop: [P]` in one record exit 3. Redraft: Terms «Handoff item» name `research_neighbours: {keep, drop, add}` beside `research_items:` and `research_claims:`. Criterion 30 reads "plus `keep` and `add` paths, minus `drop` paths, of maintainer-answered Q-records" and adds the refutations "a linked record without the path in `keep` or `drop` closes a neighbour item", "a path added only in answer text passes" and "conflicting keep and drop pass instead of exit 3". Criterion 33 names that conflict. The [DETAIL] «exact neighbour parity», design «Research → interview → spec» and «Handoff gate», the Data model's Q-record link fields, `prompts/01a-interview.md` and `prompts/02-spec.md` (plan file table) and the plan's step-9 fixtures say the same.
- S-42: Reading B, with a closed set of rules by file type; anything else is `unsupported`. The citation `path::X` has the same form for a symbol and a section, so the file type decides. First, Markdown (`.md`): X equals the text of exactly one heading, after removing the leading `#` marks and the outer whitespace, compared exactly and case-sensitively; formatting such as backticks stays part of the text. The excerpt runs from that heading to the line before the next heading of the same or a higher level, or to the end of the file. In Markdown, `criterion <n>` also resolves, to item `<n>.` under the file's one `## Acceptance criteria` heading, up to the next item or heading. This carries Q-7's "criterion number" evidence for topic 5. Second, Python (`.py`): X names a `def`, `async def`, `class` or module-level assignment target, found with Python's `ast` module on the frozen bytes; a dotted X names a nested definition such as `Class.method`. The excerpt is that node's lines. Third, YAML and JSON: X is a dotted key path found by the parser, and the excerpt is the value written out as canonical JSON. Fourth, every other file (shell, Makefile, JavaScript, TOML, text): X resolves when it occurs as a whole word, and the excerpt starts at the first matching line. Two or more matching headings, definitions or key paths make the citation ambiguous, and the claim is `unsupported`. All excerpts keep the 4,000-character claim cap with the truncation mark (S-38). The same resolution decides map entries, topic scope (S-25), the evidence floor and criterion bases. Reason: the judge has no tools and judges only the excerpt (S-29), so an excerpt without a defined extent cannot be tested. Reading A would let any prose word in a document count as evidence. A closed list fails closed: what it does not cover is unsupported, not guessed. The fallback for other files keeps Makefile, CI and hook files citable for topics 2 and 7, with a bounded excerpt. The earlier slice's `symbol_problem` (read) follows Reading A and is replaced in phase 4. Test: `docs/WORKFLOW.md::routing table`, prose only, is unsupported. `docs/WORKFLOW.md::Artefact lifecycle` is valid, with that section as its excerpt. `scripts/stage2_swarm.py::symbol_problem` yields the function's lines. A Markdown file with two equal headings makes a citation of that heading unsupported. Redraft: Terms «Claim» add «Resolves» with these four rules. Criterion 16 adds the refutations "a reference that matches only prose in a Markdown or Python file resolves" and "an ambiguous heading, definition or key path resolves". The excerpt [DETAIL] «Opus map merge, topic author and judge have empty tool lists» names the extents. Design «Reports → judge» and the plan's step-3 and step-7 fixtures cover each file type.
- S-43: Reading B, limited to three named path forms. A neighbour spec is exactly one of these: `plans/changes/<name>/spec.md`, an active change, where `<name>` is one path segment other than `archive`; `plans/changes/archive/<YYYY-MM-DD-name>/spec.md`, a closed change; or `plans/specs/<capability>/spec.md`, a living spec. The change's own `spec.md` is never its neighbour. A header-given path outside these forms, or the change's own spec, refuses with exit 2 before any model call, so `templates/spec.md` is refused. A resolved neighbour-category entry inside one of the three folder kinds suggests that folder's `spec.md` when it exists in frozen bytes (S-35, widened). An entry inside the change's own folder stays in the map marked `self`. It gets no neighbour status, needs no relation and is not a gap. Any other entry stays `no-spec` with a gap. Reason: `docs/WORKFLOW.md` («Artefact lifecycle», read) names exactly these three places for specs. A living spec states what holds today, and an archived change records closed decisions; topic 5 may need either. Marking them `no-spec` would hide a real neighbour behind a gap. A closed list fails closed for every other `spec.md`, such as the template. The own-change rule keeps topic 5 from comparing the change with itself. Measured at `c0687a7`: 20 active change folders with `spec.md`, this one included; 17 of 20 archived change folders with `spec.md`; one living spec, `plans/specs/implementation-verification/spec.md`; and `templates/spec.md`. Test: a given `templates/spec.md` exits 2, and so does the change's own spec. An entry under `plans/specs/implementation-verification/spec.md` yields a packet neighbour, and a topic-5 report without its relation is rejected. An entry in `plans/changes/archive/2026-10-08-interview-minimums/plan.md` yields that folder's spec as a packet neighbour. An entry in the change's own `design.md` is `self` and needs no relation. Redraft: the Topic contract's finder paragraph and the [DETAIL] «Preflight validates class and given neighbours» list the three forms and the own-spec rule. Criterion 4 adds the refutation "a given path outside the three forms, or the change's own spec, starts a call". Criterion 29 gains the refutation of S-46. Design «Caller → router» and «Finder → map», Data model «Map» (the `self` mark), the ADR 0020 draft's line on neighbour-category artifacts and the plan's step-3 fixtures say the same.
- S-44: The key is the identity, and every doubt about identity is document-level. A candidate is the entry whose key under `opencode-go.models` equals the Pi id. That entry's `id` field must be present and equal to its key. An absent `id` counts as different, so the entry is `metadata-malformed` with the raw value recorded as absent. S-33's "duplicate claimed ids" covers two forms: a key repeated in the raw JSON text, and two entries under different keys whose `id` fields are equal. Either makes the whole result `capability-unavailable` with the reason `duplicate-id`, and every free candidate is excluded. The runner parses with a parser that reports repeated keys, because a default parser keeps one of them without notice. Only `opencode-go.models` is inspected. Reason: S-33 already calls two entries that claim the same id an identity ambiguity. Under the per-entry reading, `a-free` could be selected from one of two conflicting entries. Treating an absent `id` as malformed admits nothing on a guess. Both choices exclude more, never less, and the fixed slots still run (Q-11). Test: keys `a-free` and `b-free`, each with `id: "a-free"` and `tool_call: true`, give N=0 with capability-unavailable and `duplicate-id`. A repeated raw key gives the same. `x-free` with `tool_call: true` and no `id` is excluded as `metadata-malformed` with the value absent, while another valid candidate is still selected. Redraft: Terms «Selected Go free models» say "the entry keyed by the exact Pi id, whose `id` field is present and equal to the key". The [DETAIL] «Preflight validates class and given neighbours» names both duplicate forms and the absent-id case. Criterion 42 adds the refutations "a repeated raw key, or one `id` value under two keys, leaves any candidate selectable" and "an entry without `id` admits a seat". Design «Catalog → frozen seats» and the plan's catalog fixtures add the three cases.
- S-45: Topic 5 still runs, and its evidence floor is waived only when its packet holds no neighbour. If the packet has no given and no suggested packet neighbour (only `self` or `no-spec` entries, or none), the runner still dispatches all three topic-5 seats with the same packet, which states "no packet neighbour". A valid report then carries `neighbour_relations: []` and a `not read` entry that names the empty packet. In this one case the one-evidence-backed-claim floor does not apply. Any claim the report makes is still checked and can be scored off-brief. A report that lists any relation in this case has an extra path and fails the template. With one or more packet neighbours the floor applies unchanged. The reconciliation's neighbour section records "no neighbour given or found" as a named gap (criterion 7). Reason: S-36 makes `neighbours: []` valid and says the run goes on with finder suggestions only. Under the floor, every change without neighbours could never complete a run. Skipping topic 5 would change the 39 required slots and Q-7's three agents for every topic, so it would need the maintainer. Passing only by citing outside the scope must not be the way through. The bound stays `39 + 3N`, with no extra call; the three topic-5 calls stay within it. Test: a feature change with `neighbours: []` and no neighbour-category entry gets three empty topic-5 reports accepted, and the run is complete. The same change with one packet neighbour rejects a zero-claim topic-5 report. An empty packet with a report that lists a relation is rejected. Redraft: the Topic contract's topic-5 row and its floor sentence state the exception. Criterion 18's refutation "a report with zero evidence-backed claims passes" adds "except a topic-5 report whose packet holds no neighbour". Criterion 27 adds the refutations "a topic-5 report with an empty packet lists a relation or lacks the empty-packet not-read entry" and "a topic-5 report with a nonempty packet and no evidence-backed claim passes". Criterion 7 names the gap. Design «Map → topic contexts» and the plan's step-7 fixtures say the same.
- S-46: The refutation compares with an independent derivation. Criterion 29 adds the refutation "a resolved neighbour-category entry inside one of the three neighbour folder kinds (S-43) whose `spec.md` exists in frozen bytes is marked `no-spec` or `self` wrongly, or yields no packet neighbour". Criterion 24 adds the refutation "topic 5's packet-neighbour list differs from the list derived from the resolved map and the given header". The test derives the expected packet-neighbour list from the map fixture by the rules of S-35 and S-43. It then compares that list with topic 5's packet and with the manifest. Reason: criterion 27 checks relations against the runner's own packet, so a wrong packet passes it. Only a comparison with a list derived independently can go red. Test: the row's input, `plans/changes/foo/design.md::Data model` with `foo/spec.md` present in frozen bytes. A runner that marks it `no-spec` and lists a gap fails criterion 29 even though a gap entry exists. Redraft: criteria 24 and 29 carry the two refutations. The plan's step-3 fixtures and the criterion ledger lines for 24 and 29 name the derived-list comparison.

## Phase 2a rulings, round 5 — 2026-10-17, orchestrator (S-47 to S-52)

These are `[DETAIL]` rulings on Opus 5.5's fifth phase-2a round (`findings.md`, S-47 to S-52, six MINOR rows, no MAJOR). Each stays within the maintainer's answers Q-1 to Q-11 and the earlier rulings S-1 to S-46. Each picks the reading that fails closed, keeps the bounded cost and time (`39 + 3N` invocations, 150 minutes, no retries) and can be tested red. The redraft carries them into `spec.md`, with matching changes to `design.md` and `plan.md` where named; none touches the ADR 0020 draft. No row changes intent, scope, cost or a data boundary, so no row is left to the maintainer.

Three of the six rows refine the resolver of S-42 (Markdown structure, YAML/JSON key paths, claims with several citations); the other three close edges of rules already settled (neighbour status, the Pi catalog, the `--stage2-off` route). I see no concrete reason for another phase-2a round after this redraft: the rows have shrunk from 30 to 6 over five rounds, all are MINOR, none reopens intent, and the remaining risk sits in resolver and catalog mechanics that phase 3's fixtures and phase 4's red-first tests measure more cheaply than another spec review would.

Read for these rulings: the round-5 rows in `findings.md`; the round-4 rulings file (format); `spec.md` in full; `decisions.md` Q-4 and Q-10 in full and the opening lines of every ruling S-1 to S-46, with S-9, S-28, S-37 and S-38 in full; `design.md`, the explore/class lines near line 50, «Catalog → frozen seats» (lines 96 to 145) and the resolver paragraph (lines 318 to 332); `scripts/stage2.py`, `explore` (lines 2798 to 2830); the headings and fences of `prompts/03-plan.md`; `model-endpoints.yaml` lines 250 to 256; `decisions/adoption.yaml` lines 1 to 8; the package names in `requirements-ci.txt`, all at `d862bc2`. Not read: `research.md`, the earlier findings rows, the plan beyond two search hits, the ADR 0020 draft, Q-1 to Q-3 and Q-5 to Q-9 and Q-11 beyond what the spec cites, the pinned Pi sources and its behaviour on a malformed overlay entry, the live Pi and models.dev catalogs, and any credential file.

(Written by an Opus 5.5 sub-agent and committed unchanged by the orchestrator. Findings rows stay unchanged; the redraft carries the rulings into the spec.)

- S-47: Reading B, as a small fixed subset of CommonMark that needs no new library (`requirements-ci.txt` at `d862bc2` holds no Markdown parser). The resolver scans the file once. A front-matter block (a first line `---` through the next `---` line) is not scanned for headings. A fenced code block opens with a line of at least three backticks or tildes, indented by at most three spaces, and closes with a line of the same character at least as long; an unclosed fence runs to the end of the file. A heading is a line outside front matter and fences with at most three spaces of indentation, one to six `#` marks, then a space, a tab or the line end. The heading's text drops the marks, an optional closing run of `#` marks and outer whitespace. Setext headings and HTML blocks are not recognised. The same scan decides heading uniqueness, the end of an excerpt, the one `## Acceptance criteria` heading and the numbered items under it, so a fenced copy is never a heading, a duplicate or a criterion item. Reason: a fenced example is quoted text, not structure; reading it as a heading cuts real excerpts short and lets an example act as evidence. Unrecognised forms make a citation unsupported, never guessed. Test (from `prompts/03-plan.md` at `d862bc2`): `prompts/03-plan.md::The criterion ledger` yields lines 65 to 94; `prompts/03-plan.md::Criterion ledger` is unsupported; a fixture with a real `## X` and a fenced `## X` resolves `X` to the real one; a fixture whose only `## Acceptance criteria` sits in a fence makes `criterion 1` unsupported; a `# comment` line inside front matter is no heading. Redraft: Terms «Resolves», Markdown rule, add the scan in one sentence ("headings are ATX lines outside front matter and fenced code blocks; setext and HTML forms are not recognised"). Criterion 16 adds the refutation "a line inside a fenced block or front matter counts as a heading, a duplicate or a criterion item". Design's resolver paragraph says the same; the plan's resolver fixtures add the five cases.
- S-48: Split at every dot, no index segments, dates as ISO text, one fixed JSON form. First, X is split at every `.`; each segment must equal a string key of the current mapping exactly. A key that contains a dot, a non-string key, or a path that passes through a list cannot be named by a path; the claim cites the nearest citable parent instead, whose excerpt holds it. Second, YAML parses with a safe loader that reports duplicate keys, and JSON with duplicate-key reporting and NaN or infinity refused; a duplicate is ambiguous and unsupported (as S-42 already rules). Third, dates and timestamps convert to their ISO 8601 text (`2026-10-08`); any other value without a JSON form (binary, sets, NaN, infinity, a non-string key anywhere in the value) makes the reference unsupported. Fourth, canonical JSON means sorted keys, non-ASCII kept unescaped, two-space indentation, separators `,` and `: `, and no trailing newline; the excerpt is that text before the per-claim cap. Reason: one split rule has no second match to arbitrate, so no ambiguity rule is needed; rejecting what it cannot name fails closed while the parent stays citable. Turning dates into text keeps the governance files citable for topic 3 (`decisions/adoption.yaml` line 5 holds an unquoted date) without guessing. A fixed JSON form makes "the excerpt differs from the extent" testable. Test: `model-endpoints.yaml::research_swarm.free_focuses.longcat-2.5-preview-free` is unsupported and `model-endpoints.yaml::research_swarm.free_focuses` resolves with the key in its excerpt (both measured on the file at `d862bc2`; this change later replaces that key); `decisions/adoption.yaml::adopted.interview-minimums` yields `"2026-10-08"`; `a.0` on a list is unsupported; a YAML file with a repeated key makes a citation of it unsupported; a JSON fixture yields byte-exact canonical text. Redraft: Terms «Resolves», YAML/JSON rule, state the split, the date rule, the refusals and the JSON form. Criterion 16 adds the refutation "a dotted key, list index or value without a JSON form resolves, a date excerpt is not its ISO text, or the excerpt is not the canonical form". Design's resolver paragraph and the plan's resolver fixtures say the same.
- S-49: Reading A. A claim is `valid` only when every one of its citations resolves (local) or has a successful page receipt (online); one failing citation marks the whole claim `unsupported`. An unsupported claim gets no excerpt, no disposition and cannot name a criterion Basis (S-9, S-23). Reason: the statement may rest on the source that failed, and the judge cannot tell which part each source supports; partial acceptance would let a claim be scored supported on evidence it does not fully carry. It matches the [DETAIL] «Template breaches reject a report» and S-9 as written. The floor stays per report, so a report with another valid claim still passes; a model can avoid the loss by citing only what it has read. «Unsupported references confer no evidence» keeps its meaning for map scope, where each entry has one reference. Test: a topic-1 claim citing `scripts/stage2.py::explore` and `scripts/stage2.py::no_such_symbol` is unsupported and carries no excerpt; as a report's only claim, the report fails the floor; an online claim with one receipted and one unreceipted URL is unsupported. Redraft: Terms «Evidence status and disposition» add "a claim is valid only if all its citations resolve or have receipts". Criterion 16 adds the refutation "a claim with any unresolved citation or unreceipted URL is valid". The [DETAIL] «Opus map merge, topic author and judge have empty tool lists» keeps "joined in citation order", now for valid claims whose every source resolved. Design «Reports → judge» and the plan's step-7 fixtures say the same.
- S-50: Repeated ids are document-level and exit 1; a bad entry is excluded by itself. First, a failed or timed-out refresh, a response pinned Pi itself rejects, an unparseable body, or a repeated id anywhere in the fresh `opencode-go` overlay (a repeated raw key, or one id under two entries) is a malformed or ambiguous Pi result: diagnostics kept, exit 1 before any model call (criterion 41, S-28). "Sort and deduplicate selected identities" in the design never merges two catalog entries. Second, otherwise each entry is judged alone. A `-free` candidate whose `input` or `type` field does not have Pi's typed form is excluded as `pi-malformed`, with the raw value recorded, and never excludes a valid peer. A fixed Go id with a malformed entry exits 1 as `fixed-model-unavailable`, naming the id and the raw value (S-37). Other entries are not inspected beyond the repeated-id check. Reason: this mirrors the models.dev split of S-33 and S-44, while Q-11 keeps Pi as the blocking source: a duplicate leaves the identity in doubt, so no seat may be chosen from it, and Pi's doubt blocks the run, while one bad preview entry is no failed refresh and must not cost the 39 fixed slots. Not read: how pinned Pi itself treats a malformed entry; whatever it does, a rejection by Pi falls under the first rule. Test: an overlay valid except `cat-jam-free` with `"input": "text"` runs the 39 fixed slots and records `cat-jam-free` as `pi-malformed` with that value; `longcat-2.5-preview-free` listed twice exits 1 with no model call; `qwen3.8-flash` with a string `input` exits 1 as `fixed-model-unavailable` naming it. Redraft: Terms «Selected Go free models» add `pi-malformed` to the exclusion reasons and "a repeated overlay id is an ambiguous Pi result". Criterion 41 adds the refutation "a repeated overlay id lets any model call start"; criterion 42 adds "one malformed Pi candidate excludes a valid candidate or blocks the fixed slots". The [DETAIL] «Preflight validates class and given neighbours», design «Catalog → frozen seats» and the plan's catalog fixtures add the three cases.
- S-51: Reading B, closed by the existing split rule. A topic-5 relation counts toward a suggested neighbour's status only if at least one of its listed claims is `valid`. `confirmed` needs three counting relations, all `related` or `contradicts`; `rejected` needs three counting relations, all `unrelated`; every other case, including fewer than three counting relations, is `split`, with its human item. Human items are never filtered: every `contradicts` and every `unrelated` given path still derives its item, whether or not its claims are valid. Reason: an unsupported claim "is never evidence" (Terms), so a relation that rests only on one cannot help make a path required or drop it without a human; folding the gap into `split` keeps one status set and sends the doubt to the maintainer, as Q-7's addendum does for disagreements. The runner uses only its own valid/unsupported marks, never a judge disposition, so S-40's runner-only rule holds. Test: three `related` relations for P, one citing only an unresolved claim, make P `split` with an open item; once `spec.md` exists the gate exits 1 until a structured keep or drop. The same with three `unrelated` gives `split`, not `rejected`. A given path whose `unrelated` relation cites only unsupported claims still derives its item. Redraft: Terms «Neighbour status» add "a relation counts only if one of its claims is valid; fewer than three counting relations is split". Criterion 29 adds the refutation "a relation whose claims are all unsupported counts toward confirmed or rejected, or such an unrelated-given or contradicts relation yields no item". Design «Research → interview → spec» and the plan's step-9 fixtures say the same.
- S-52: Reading B, with `--class` refused beside `--stage2-off`. `--stage2-off [REASON]` skips class derivation and every class and neighbour header check, because it selects no class-dependent route; it makes one Haiku 5.5 call, as `scripts/stage2.py` `explore` already does (lines 2809 to 2812, read at `d862bc2`, whose comment cites criterion 20). An explicit `--class` together with `--stage2-off` refuses with exit 2 before any call, saying the class has no effect on that route. Reason: Q-4 decides which changes get the swarm, not whether the explicit fallback may run; requiring a class there would block the fallback for changes the swarm never applies to, with no safety gained, because Haiku is the route that already existed. Refusing the unused argument fails closed on the one input that could mislead the caller about what ran. Test: `research.md` with a bead and no class, `scripts/stage2.py explore <change> --stage2-off "quota"`, makes one Haiku call and records route, model and reason; `--class bounded --stage2-off "quota"` with header `feature` exits 2 before any call. Redraft: criterion 4 opens "When exploration runs without `--stage2-off`, …"; criterion 20 adds the refutations "it requires or validates a class or neighbours header" and "a `--class` argument beside it is accepted". The design's explore lines (near line 55) and the plan's explore fixtures say the same.

## Q-12 · How the research seats get their models when OpenCode Go changes its offer

asked: 2026-10-18
answer: "ja" — then "bei beiden": replace the fixed research trios with an ordered candidate list per seat in `model-endpoints.yaml` and a reachability check before each run, for both the repository trio (finders and topics 1 to 8) and the online trio (topics 9 to 11).
answered_by: maintainer
status: answered
supersedes_in_part: Q-9 (fixed online trio) and the fixed repository trio of the spec
context: |
  Topic: how the research swarm chooses the model for each of its required seats.
  Intention: OpenCode Go changes its offer often; the maintainer wants changing a research model to be a one-line edit, and one unavailable model should not make every run incomplete.
  Today (measured 2026-10-18 12:12 UTC through `stage2.py prepare-loop` on a scratch change, no repository content, no tools): `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `longcat-2.0` and `mimo-v2.6-pro` answered; `qwen3.8-flash`, a fixed online-trio member, was not called because its wire API is not measured; GLM through OpenCode Go works, only GLM through Z.ai is unavailable until 2026-10-21 20:34 Asia/Singapore (maintainer, 2026-10-18). The spec fixes both trios, so one missing member makes every run end incomplete with exit 1.
  Repository change: each required research seat gets an ordered candidate list in `model-endpoints.yaml`; before each run a reachability check without repository content or tools selects the first reachable admitted candidate per seat, the selection is reported in the main conversation, and a seat with no reachable candidate stops the run before any model call and names the seat. The same form as the review swarm's availability preparation (PR #157), so both swarms are changed the same way.
  Architecture change: yes — spec, design and the ADR 0020 draft replace "fixed trio" with "candidate list per seat plus reachability selection"; the `39 + 3N` budget, the public/private boundary, the leak checks and Opus as map merger, topic author and judge stay unchanged.

In the context of an OpenCode Go offer that changes often, facing fixed
research trios that end every run incomplete when one member is
unavailable, we decided on an ordered candidate list per seat with a
reachability check before each run, for the repository and the online
trio alike, to achieve model changes by a one-line edit and runs that
survive a single unavailable model, accepting one more preflight step and
a selection that is reported rather than fixed in the spec. — 2026-10-18

## Q-13 · Research results survive an aborted run

asked: 2026-10-18
answer: "bitte achte darauf, dass die zwischenergebnisse der recherche agenten gespeichert werden, damit bei abbruch wegen token limits nicht verloren geht" — every finished research contribution is stored durably as soon as it ends, so a run cut off by a token or quota limit loses no finished work.
answered_by: maintainer
status: answered
context: |
  Topic: what happens to finished research contributions when a run stops early.
  Intention: model quotas and token limits are tight (Codex, Claude and Z.ai budgets were all short on 2026-10-17/18); a run that dies after 30 of 42 calls should not have to pay for those 30 again.
  Today: the design buffers reports until a stage ends or aborts and appends research only at barriers; there is no resume, so an aborted run starts from zero.
  Repository change: each slot's terminal result (report, receipts, audit record) is written durably when it ends, into runner-owned state outside the repository bound to the frozen input digest; a later run with the same frozen input state reuses finished slots and launches only the missing ones, after the same preflight and leak checks.
  Architecture change: yes — a resumable run state beside the existing frozen-input snapshot; the research artifact is still written only by the runner, peers still cannot read each other's answers during a stage, and no slot is retried within a run.

In the context of tight model quotas, facing runs that lose every finished
contribution when a token limit stops them, we decided to store each
finished contribution durably at once and let a later run with the same
frozen input reuse it, to achieve no repeated spend on finished work,
accepting a runner-owned state store and an input-binding check on resume. — 2026-10-18

## Q-14 · How substitutes for the research seats are chosen, and the phase-4 time budget

asked: 2026-10-18
answer: "die ersatzmodelle müssen auch dynamsisch angepasst werden  - Ersatzmodelle sind LongCat 2.0, MiMo Pro und GLM 5.3 Flash über Go. erhöhe das zeizbudget" — the substitute for an unavailable seat model is chosen at each preparation from the admitted paid Go models in the live catalog, not from a declared list; the last clause raises the phase-4 appetite to 17 hours 20 minutes in total (recorded in plan.md, Time used).
answered_by: maintainer
status: answered
supersedes_in_part: Q-12 (the declared order of fallback candidates per seat)
context: |
  Topic: how the research swarm picks a substitute when a seat's model is unavailable, and how much phase-4 time the change may use.
  Intention: the Q-12 redraft proposed hand-kept fallbacks per seat (LongCat 2.0, MiMo Pro, GLM 5.3 Flash through Go); OpenCode Go changes its offer often, so a fixed fallback list goes stale like the fixed trios did. The same redraft showed that the remaining appetite falls 3 to 4 hours short and recommended 17 hours 20 minutes in total.
  Today: the redrafted spec (`4586c04`) gives each seat an ordered candidate list with fixed fallbacks in `model-endpoints.yaml`. The review swarm (pull request #157) admits a paid Go model only with a dated terms reading in `modelle_terms` and orders admitted models by the declared `anfragen_5h`, cheapest first, ties by id. The appetite is 13 hours 20 minutes, of which 4 hours 56 minutes were measured by 2026-10-18.
  Repository change: each seat declares one preferred model; when it cannot be used, preparation takes the cheapest reachable admitted paid Go model of the live catalog that no other seat of the same topic holds, and reports it as "substitute for <seat>". Admission stays one deliberate YAML entry, a dated terms reading in `modelle_terms`, because repository seats receive private content; a newly admitted model then serves as a substitute without any other edit. Spec, design, plan and the ADR 0020 draft change; plan.md records the new appetite.
  Architecture change: yes — seat selection draws substitutes from a live pool instead of a declared list. Admission, the public/private boundary, the `39 + 3N` budget, leak checks, the free-seat rules and the Opus roles stay unchanged.

In the context of research seats whose hand-kept fallbacks go stale as
OpenCode Go changes its offer, facing the choice between fixed fallback
lists and substitutes chosen from the live catalog, we decided on live
substitutes among the admitted paid Go models, cheapest first, to achieve
that newly admitted models serve without a list edit, accepting that a dated
terms reading stays a deliberate manual step and that the phase-4 appetite
rises to 17 hours 20 minutes in total. — 2026-10-18

## Q-15 · Where the research state store may live relative to a model's home directory

asked: 2026-10-19
answer: "Ja zu Option 1" — the runner guards the real home directory that Claude research processes inherit: a state store beneath it is refused with a clear message, and the store is used only when `XDG_STATE_HOME` points outside that home.
answered_by: maintainer
status: answered
context: |
  Topic: the default place of the resumable research state store.
  Intention: the phase-6 review (finding F-12) found that without `XDG_STATE_HOME` the store defaults beneath the user's home, which Claude research processes inherit, although the spec keeps stored peer results out of every model's home directory (criterion 52).
  Today: the design names `${XDG_STATE_HOME:-~/.local/state}` as the default; the placement guard checks only the worktree and its git directory.
  Repository change: the placement guard also refuses a store inside the real home directory, naming `XDG_STATE_HOME` in the message; the design line for the default path is amended; a test shows both the refusal and an accepted store outside the home.
  Architecture change: no — the store layout, locking, resume and the review loop record stay as they are; only the default location no longer works unless it lies outside the home.

In the context of a state store whose default lies in the home directory that
Claude research processes inherit, facing the choice between refusing, a scratch
home for Claude seats and a new default path, we decided to refuse a store inside
the real home with a clear message, to achieve that stored peer results never lie
within a model's home, accepting that `XDG_STATE_HOME` must be set outside the
home before a research run. — 2026-10-19

## Q-16 · How a repository seat is kept inside the worktree

asked: 2026-10-19
answer: "ja, mach das mit der Pfadsperre in Pi" — a path lock in Pi itself (an extension on the repository seats), cross-platform, instead of an operating-system sandbox.
answered_by: maintainer
status: answered
context: |
  Topic: how the swarm's repository seats are kept from reading files outside the worktree.
  Intention: the attended offline capture with the real pinned Pi (finding F-24) showed a repository seat reading absolute paths outside the worktree: the fake home directory's `.ssh` canary and the state-store peer-result canary reached the model, which spec criterion 52 forbids. The maintainer was told that `sandbox-exec` is macOS-only and Windows is unsupported.
  Today: a repository seat runs Pi with `--tools read,grep,find,ls`, the worktree as working directory and no extension; those tools accept absolute paths, `..` and symbolic links. The design recorded this as the accepted paid-Pi residual read risk.
  Repository change: a Pi extension (`scripts/stage2_repository_pathlock.mjs`), loaded on repository-seat launches as the one explicit `-e` beside `--no-extensions`, blocks a read, grep, find or ls call whose path, resolved with `..` collapsed and symbolic links followed, lies outside the worktree; tests drive it with an absolute path, a `..` escape and a symlink escape. The design line on the residual read risk is amended.
  Architecture change: no new component beyond the extension; public seats, probes and the merge, author and judge calls are unchanged. The lock works on every platform Pi runs on.

In the context of repository seats whose file tools accept paths anywhere on the machine, facing the choice between an operating-system sandbox (macOS only) and a lock inside Pi, we decided to confine the four file tools to the worktree with a Pi extension, to achieve that the state store, the home directory and the git directory outside the worktree never reach a model on any platform, accepting that the lock judges the path a tool is called with and not what a directory walk then visits. — 2026-10-19

## Q-17 · Whether review preparation shares the research swarm's rule validation and probe now

asked: 2026-10-19
answer: "lege zusdammen" (verbatim; "merge them") — option 1: unify now; review preparation uses the shared rule validation and the shared Go probe within this change.
answered_by: maintainer
status: answered
context: |
  Topic: one implementation of rule validation and model probing for both swarms' preparation.
  Intention: the phase-6 review, round 3 (finding F-27), found that review preparation kept its own rule validation and probed through `runner.run_reviewer()` instead of the shared `probe_go()` the research preparation uses, although spec criterion 50 requires one implementation.
  Today: the research preparation validates with `rule_problem` and probes with `probe_go`; the review preparation has a private validator and probe.
  Repository change: review preparation calls `rule_problem(flash_size=True)` and `probe_go` (which gains `admission` and `verb` keywords); the private validation leaves that path; the review rule now refuses an unknown key, as the research rule does; tests show both calls and a refusal.
  Architecture change: no — the review loop's behaviour, records and rounds stay as they are; only its preparation shares the research swarm's helpers.

In the context of two swarm preparations with separate rule validation and
probing, facing the choice between unifying now and a follow-up change, we
decided to unify them within this change, to achieve the single implementation
criterion 50 requires, accepting that the review rule now refuses unknown keys.
— 2026-10-19

## Q-18 · Who chooses the research seat models before a run, and on what evidence

asked: 2026-10-21
answer: "die flash modelle werden immer ändern, ich möchte, dass in stufe 2 oder der stufe in der die flash modelle alle verfügbaren aber maximal 3 modelle genutzt werden. am besten die günstigsten, und in der leiter gehen wir die preisreihe dann schrittweise nach oben." — then "ich möchte das man vor jeden lauf gefragt wird, welche modelle genutzt werden sollen, mit empfehlungen und warum, sowas wie intelligenz vs kosten" — then "A, artificial analysis als benchmark, nur für research" — then "der benchmark muss aktualisiert werden, regalmäßig" — then, asked whether live per run, a dated reading with a maximum age, or a dated reading with a weekly refresh job: "1" (live per run). Before every research run the maintainer is asked which models fill the seats, with a recommendation and its reason weighing intelligence against cost; the Go seats name no fixed models; the recommendation starts from the cheapest reachable admitted models, at most three per trio, and moves up the price order only with a reason; intelligence is the Artificial Analysis Intelligence Index, recorded with its reading date and source, for the research swarm only, read live from the Artificial Analysis API at every preparation.
answered_by: maintainer
status: answered
supersedes_in_part: Q-12 and Q-14 (one fixed preferred model per seat; the preparation alone choosing substitutes)
context: |
  Topic: how the six research seats get their models now that the Go Flash models change often.
  Intention: PR #205 (2026-10-21) removed `mimo-v2.6-flash` from the Go model list because OpenCode Go no longer answers it correctly, yet it was the preferred model of the second seat in both trios, so the declared seats no longer resolved.
  Today: each seat declares one preferred model; preparation keeps a reachable preferred model and fills the rest with the cheapest reachable admitted pool model, then prints the selection for the main conversation. No intelligence value is declared anywhere in `model-endpoints.yaml`.
  Repository change: the research block declares an intelligence reading per candidate model (Artificial Analysis Intelligence Index, dated, with its source); preparation prints every reachable admitted candidate with cost and intelligence plus a recommended selection, and the orchestrator asks the maintainer before the receipt is used; the maintainer's choice can replace the recommendation. Spec, design, ADR 0020 and the tests follow.
  Architecture change: the seat choice moves from a declared preferred model to a per-run maintainer choice on a recommendation. Admission through a dated terms record, the probe, the receipt, the public/private boundary and the `39 + 3N` budget stay unchanged. The review loop keeps its measured order (cheapest admitted first, Flash round of at most three, then upward) and gets no intelligence value.

In the context of research seats whose named Flash models go stale as OpenCode
Go changes its offer, facing the choice between fixed preferred models with
automatic substitutes and a per-run choice, we decided that the maintainer
chooses the seat models before each run on a recommendation that weighs the
Artificial Analysis Intelligence Index against the declared request cost, to
achieve that no stale model name blocks a run and that a harder change can buy
a stronger model deliberately, accepting one more question before every research
run and a live call to the Artificial Analysis API, with its key, at every
preparation. — 2026-10-21
