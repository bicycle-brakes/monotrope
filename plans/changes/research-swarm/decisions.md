---
title: "Decisions — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-16
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
