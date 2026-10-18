---
title: "Decisions — loop-until-clean"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-17
supersedes: null
superseded_by: null
bead: coding-harness-4fk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, review-loop, opencode-go, swarm]
---

# Review loop until clean, as a swarm and a ladder — Decisions

Phase 1a, asked by the orchestrating Claude Code session on 2026-10-14, each
question with its context first. The change began as bead coding-harness-dx0
(the review loop runs until a round finds nothing); by the maintainer's answer
Q-4 it merged into bead coding-harness-4fk (the implementation review as a
swarm of OpenCode Go models), which carries it from here.

## Q-1 · Which models review, in which order

asked: 2026-10-14
answer: first three Flash models of OpenCode Go — DeepSeek V4.1 Flash, MiMo-V2.6-Flash, LongCat-2.0; then GLM-5.3-Flash, then Qwen3.8 Flash, then GPT 6 Luna, then Claude Haiku 5.5, then MiniMax M2.7, then MiMo-V2.6-Pro.
answered_by: maintainer
status: answered

Asked as "where is the upper bound" (8 rounds, 5 rounds, or none); the
maintainer answered with the ladder itself: "ich möchte, dass am anfange drei
flash modelle von opencoe laufen, nämlich DeepSeek V4.1 Flash,
MiMo-V2.6-Flash, LongCat-2.0, danach soll GLM-5.3-Flash, dann Qwen3.8 Flash,
dann GPT 6 Luna, dann Claude Haiku 5.5, dann MiniMax M2.7, dann
MiMo-V2.6-Pro". The bead of 2026-10-11 had named MiMo-V2.6-Pro for every
round after the third; this ladder replaces it.

In the context of a loop capped at three rounds on three OpenCode Go models,
facing the choice between a fixed cap and a longer ladder, we decided on a
nine-model ladder across providers to achieve fresh eyes in every round,
accepting more providers to declare and more calls per change. — 2026-10-14

## Q-2 · What "nothing found" means

asked: 2026-10-14
answer: a round is clean when it leaves no taken finding; a round whose findings were all rejected counts as clean.
answered_by: maintainer
status: answered

In the context of rounds that may report only findings the orchestrator
rejects, facing the choice between "no taken finding" and "no finding at
all", we decided on no taken finding to achieve that a model reporting
trivia cannot keep the loop running, accepting that a rejected finding does
not earn another round. — 2026-10-14

## Q-3 · The repair-caused emergency brake

asked: 2026-10-14
answer: it stays — two consecutive rounds whose taken findings were caused by a repair (origin `fix-r`) stop the loop and go to the maintainer, also before the ladder ends.
answered_by: maintainer
status: answered

In the context of the fix-by-case pattern of PR #138, facing the choice
between keeping and dropping the brake in a longer loop, we decided to keep
it to achieve an early stop when repairs feed the reviews, accepting more
interruptions. — 2026-10-14

## Q-4 · The order against the review swarm

asked: 2026-10-14
answer: merged — the loop-until-clean change goes into bead coding-harness-4fk; one rebuild of the review loop instead of two.
answered_by: maintainer
status: answered

In the context of two beads that change the same loop, facing the choice
between this change first and one merged change, we decided to merge them to
achieve one rebuild, accepting that the longer loop arrives with the swarm.
— 2026-10-14

## Q-5 · How the first three Flash models run

asked: 2026-10-14
answer: at the same time, in round 1 — three reviews in parallel, their findings merged, then one repair; from round 2 on one model of the ladder per round.
answered_by: maintainer
status: answered

In the context of "first three Flash models", which could mean parallel or
consecutive rounds, facing that choice, we decided on parallel in round 1 to
achieve three independent views at once and a faster loop, accepting a
merge step for their findings. — 2026-10-14

## Q-6 · When the ladder runs out

asked: 2026-10-14
answer: the ladder is the upper bound — when MiMo-V2.6-Pro's round still leaves a taken finding, the loop stops and reports to the maintainer.
answered_by: maintainer
status: answered

In the context of a nine-step ladder, facing the choice between stopping and
repeating the last model, we decided to stop and report to achieve a bounded
loop, accepting that a hard case reaches the maintainer. — 2026-10-14

## Q-7 · How undeclared models enter

asked: 2026-10-14
answer: each new model (LongCat-2.0, Qwen3.8 Flash, GPT 6 Luna, MiniMax M2.7, and any other not yet in `model-endpoints.yaml`) is declared with its data terms read; a model whose terms show retention or training, or cannot be read, is skipped in the ladder and named in the handover.
answered_by: maintainer
status: answered

In the context of a private repository and models whose data terms are not
read, facing the choice between declaring with read terms and releasing all
at once, we decided on read terms to achieve that no provider keeps or trains
on framework content, accepting a ladder that may run shorter. — 2026-10-14

## Q-8 · Whether free models review

asked: 2026-10-14
answer: when the review reads only the implementation's code — one part of the repository — the free models run first, as a swarm; before each run the list of free models currently offered by OpenCode Go is checked.
answered_by: maintainer
status: answered

The maintainer's words: "wenn nur der code der implemntierung, als nur ein
teil der repo gelesen wird, dann sollten die freien modelle zu erst als
schwarm genutzt werden. dazu sollte vorher immer überprüft werden, welche
freien modelle es gerade bei opencode go gibt". This narrows the research
swarm's rule (change research-swarm, Q-3: free models see no repository
content) for the review: a review limited to the implementation's diff may
go to the free models. How the review's input is limited to the
implementation is left to the spec.

In the context of free models that change over time and whose data terms are
unread, facing the choice between leaving them out of the review and a free
first stage on the implementation only, we decided on the free first stage
with a fresh list each run to achieve many cheap views before the ladder,
accepting that part of the code reaches models without read terms. —
2026-10-14

## Addendum 2026-10-16 — the free stage's models

Two statements of the maintainer in the conversation of 2026-10-16 (night
run), added below the records above, which stay as written:

- "Achte dafür darauf nur die freien Modelle aus opencode go und nicht von
  Zen zu nehmen" — the free stage takes only OpenCode Go's free models,
  never OpenCode Zen's. Measured the same night with the pinned Pi 1.2.0
  (`tools/pi/pi --list-models`): under provider `opencode-go` the ids with
  `-free` in their name were `cat-jam-free`, `longcat-2.5-preview-free` and
  `step-5-preview-free`; `space-bunny-free` and `big-pickle` exist only under
  provider `opencode` (Zen). Whether the `-free` ids are billed as free was
  not measured.
- "Es muss vor jeden Review lauf gecheckt werden welche aktuell die free
  Models sind bei Open Code go" — restates Q-8's check, now for every review
  run.

## Q-9 · A free model the check finds that the entry does not declare

asked: 2026-10-16
answer: "Automatisch mitnehmen" — every model the check finds free under `opencode-go` runs in the free stage without a hand-written entry; the run records the check's date and the model list.
answered_by: maintainer
status: answered
context: |
  Topic: what the review run does with a free OpenCode Go model the check finds but `model-endpoints.yaml` does not list.
  Intention: Q-8 said the first stage always uses all free models; the spec's criterion 5 (bde7a7e) names such a model and does not call it.
  Today: the review loop is a ladder of three declared models; there is no free stage.
  Repository change: Options: A — take it automatically, record date and list in the run's record; B — name it, call it only once declared with read data terms; C — automatically only for repositories whose content may be public. Criterion 5 of the spec changes with A.
  Architecture change: part of this change's ADR (the review swarm); the free models see the implementation's diff, so repository content reaches models with unread data terms, as Q-8 accepted.

In the context of a free-model offer that changes often, facing the choice
between taking every model the check finds and calling only declared ones,
we decided to take every free OpenCode Go model the check finds, to achieve
a free stage that always uses all free models, accepting that a new model
with unread data terms sees the implementation's diff at once. — 2026-10-16

## Q-10 · Where the three Flash models run beside the free swarm

asked: 2026-10-16
answer: "Erst frei, dann die drei Flash" — round 1 is the free swarm alone; round 2 is the three Flash models (DeepSeek V4.1 Flash, MiMo-V2.6-Flash, LongCat-2.0) in parallel; from round 3 on, one rung per round.
answered_by: maintainer
status: answered
context: |
  Topic: how Q-1 and Q-5 (three Flash models in parallel in round 1) fit with Q-8 (the free models first, as a swarm).
  Intention: the spec drafted on 2026-10-14 (bde7a7e) made round 1 the free swarm alone and put the three Flash models on the ladder one per round, which departs from Q-5.
  Today: the loop ends at the first clean round (Q-2), so whatever runs first can end the loop alone.
  Repository change: Options: A — round 1 = the free swarm and the three Flash models together, in parallel; B — round 1 the free swarm, round 2 the three Flash models in parallel, then one rung per round; C — the spec as drafted. With B the spec, plan, design and ADR draft change their round structure.
  Architecture change: part of this change's ADR (0021): the round structure of the review loop.

In the context of a free swarm and three paid Flash models that the
maintainer both placed at the start, facing the choice between one merged
first round and two parallel rounds in sequence, we decided on the free swarm
first and the three Flash models as a parallel round 2, to achieve the
maintainer's order as stated, accepting that a clean free-swarm round ends
the loop before any Flash model reviews. — 2026-10-16

## Details the orchestrating session decides, 2026-10-16

These are `[DETAIL]` items that follow from Q-9 and Q-10; none changes a
decision of record.

1. **The runner makes the free check itself.** Q-9 calls every free model
   the check finds, so the check cannot stay an orchestrator step that edits
   the yaml before the run. Before round 1 of every review-loop run, the
   runner reads the model list of the pinned Pi (`tools/pi/pi
   --list-models`, ADR 0019), keeps the ids of provider `opencode-go` whose
   id ends in `-free`, and never reads provider `opencode` (OpenCode Zen).
   The round's block names the check's date and the list. An empty list
   refuses the run by name. Reason: the maintainer's two statements of
   2026-10-16 and Q-9. Known limit: whether `--list-models` reads the
   network or only the pinned install's registry was not measured on
   2026-10-16; if it reads only the registry, the list is as fresh as the
   pin, and the spec must say so.
2. **The entry declares the free stage as a class.** The `opencode-go` entry
   of `model-endpoints.yaml` states that its `-free` models run in the free
   stage with the diff only and unread terms accepted (Q-8, Q-9); the
   declaration gate of ADR 0011 admits a model of that class without a
   per-model line, and nothing outside that class. Reason: Q-9 removes the
   per-model entry for the free stage, not the gate.
3. **Round 2 is the three Flash models in parallel (Q-10).** Rounds 3 and
   later call one rung each of the remaining ladder in Q-1's order:
   `glm-5.3-flash`, `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5`,
   `minimax-m2.7`, `mimo-v2.6-pro`. Round 2 keeps the ladder's read tools;
   only the free stage is diff-only.

## Addendum 2026-10-16 — after the redraft (a0d5bc8)

Two statements of the maintainer in the conversation of 2026-10-16, after
the redraft had started, and the reading behind the first. They revise the
orchestrator's detail 1 of 2026-10-16 and add detail 4; the text above stays
as it was written.

- "Pi soll live abrufen" — the free check reads the model list live. Read in
  the pinned Pi 1.2.0 source on 2026-10-16 (not run): the model list comes
  from a remote catalog on `pi.dev` (`core/remote-catalog-provider.js`),
  cached in the agent directory and refetched only after four hours;
  `pi update models` forces a refresh over the network
  (`package-manager-cli.js`, `refreshModelCatalogs`, `force: true`). The
  installed package does not contain `cat-jam-free`, so the list measured at
  01:50 already came from that catalog — the redraft's sentence "its
  freshness is limited by the Pi pin" is wrong.
  **Detail 1, revised:** before `--list-models`, the runner forces the
  catalog refresh (`tools/pi/pi update models`) in the call's scratch agent
  directory; a failed or timed-out refresh refuses the run instead of using
  an older list. Known limit: the live source is Pi's catalog on `pi.dev`,
  not OpenCode Go's own model endpoint (the maintainer kept Pi's catalog on
  2026-10-16 after the trade-off was put to them).
- "Das mit den free Modellen muss ich nachträglich leicht anpassen lassen,
  da sich das immer wieder ändert" — the free-stage rule is configuration.
  **Detail 4:** the rule lives in `model-endpoints.yaml`, not in
  `scripts/stage2.py`: the provider (`opencode-go`), the match rule (ids
  ending `-free`), an `include` list (ids treated as free though the rule
  misses them) and an `exclude` list (ids never called), each entry with a
  date and a reason. The runner and the tests read the rule from the yaml;
  no free model id or suffix stands as a literal in the runner. Adjusting
  the free models is a yaml edit carried by an ordinary pull request
  (`model-endpoints.yaml` has no `human-decided` entry in `provenance.yaml`,
  read 2026-10-16).

## Q-11 · Which ladder models with unread terms are admitted

asked: 2026-10-17
answer: "B" — the five ladder ids whose terms were unread get a dated reading and are admitted, the two that retain 30 days included; then "Passe minimax auf die neue Version an" — `minimax-m2.7` is replaced by `minimax-m3`
answered_by: maintainer
status: answered
context: |
  Topic: which of the six skipped paid ladder ids may review.
  Intention: after the two swarms only `mimo-v2.6-pro` was admitted, so the ladder was spent after one rung and the loop stopped for the maintainer.
  Today: `modelle_terms` skipped `longcat-2.0`, `glm-5.3-flash`, `qwen3.8-flash`, `gpt-6-luna`, `claude-haiku-5.5` and `minimax-m2.7` with the reason "terms not read". The Go page's privacy table, read 2026-10-17 (raw page, fetched 2026-10-16 23:24 GMT): the first three retain 0 days, `gpt-6-luna` (abuse-monitoring logs) and Claude Haiku 5.5 retain 30 days, training "Not used" for all five; the page lists Haiku as `claude-haiku-5-5` and has no `minimax-m2.7`, only `minimax-m3` (0 days, "Not used"). Pi's live `opencode-go` catalog of 2026-10-16 likewise holds `minimax-m3` and not `minimax-m2.7`.
  Repository change: Options: A — admit the three 0-day ids, keep the 30-day ones skipped; B — admit all five; C — change nothing. Recommendation was A.
  Architecture change: none; only which providers see the change's diff. The ladder grows from one admitted rung to all nine.

In the context of a review ladder whose paid rungs were mostly skipped for
unread terms, facing a loop that stopped after one paid rung, we decided to
admit every rung with a dated reading of the Go page's privacy table, the
30-day ones included, and to replace the retired `minimax-m2.7` by
`minimax-m3`, to achieve a ladder long enough for an until-clean loop,
accepting that `gpt-6-luna` and `claude-haiku-5-5` keep requests for up to
30 days. — 2026-10-17

The ladder id `claude-haiku-5.5` is corrected to `claude-haiku-5-5`, the id
the Go page and Pi's catalog use; with the old spelling the rung could never
have been called.

## Q-12 · Whether models that train on the data may review

asked: 2026-10-17
answer: "Lasse a" — option A: the three Go models that train on prompts stay out of the ladder
answered_by: maintainer
status: answered
context: |
  Topic: whether Gemini 4 Argon Contributor, Muse Spark 1.3 Contributor and Muse Spark 1.2 Contributor may review.
  Intention: more ladder rungs give more distinct readers of a change.
  Today: none of the three is on the ladder. The Go page's privacy table, read 2026-10-17, marks all three "Yes" for training (future Google or Meta models) and "Not ZDR" with no period; the Muse Spark rows are discounted for that permission and limited to some regions.
  Repository change: Options: A — change nothing, the three stay out; B — add them at the end of the ladder, dated and marked as training. Recommendation was A.
  Architecture change: B would let a model that trains on prompts see code for the first time, a new data boundary in ADR 0021.

In the context of three Go models that may train future models on what they
read, facing a longer ladder against a diff that could not be taken back, we
decided to keep them off the ladder, to achieve that no reviewer keeps the
change's code beyond 30 days or trains on it, accepting nine rungs as the
ladder's length. — 2026-10-17

## Q-13 · How the ladder is ordered, and what replaces a failed Flash member

asked: 2026-10-17
answer: "B, es werden immer wieder neue Modelle kommen, der Flash Schwarm wird aber Manuell festgelegt. Sollte ein Modell im Flash Schwarm ausfallen, automatisch ein günstiges nachziehen, was noch nicht dabei ist , und melden" — option B: the runner orders the ladder by a declared cost value; the Flash swarm stays a hand-kept list; a Flash member that fails is replaced automatically by a cheap admitted model not yet in the round, and the replacement is reported
answered_by: maintainer
status: answered
context: |
  Topic: the order of the review ladder by cost.
  Intention: cheap models review first, expensive ones only when earlier rounds were not clean.
  Today: the order is the hand-kept `modelle` list (ADR 0021, decision 4); by the Go page's "Estimated requests" table (Go plan, requests per 5 hours, read 2026-10-17) it is already in cost order except that `minimax-m3` (3,200) stands before `mimo-v2.6-pro` (3,250).
  Repository change: Options: A — swap the two last rungs, one line; B — the runner reads a declared cost value per model and orders the ladder itself, new code and tests; C — change nothing. Recommendation was A.
  Architecture change: B replaces ADR 0021 decision 4's hand-ordered list by a declared cost value the runner sorts by.

In the context of a Go catalog that keeps gaining models, facing a hand-kept
ladder order that drifts from cost, we decided that the runner orders the
paid ladder by a declared, dated cost value, keeps the Flash swarm as a
hand-kept list, and replaces a failed Flash member by the cheapest admitted
model not yet in the round, reporting it, to achieve cheap-first rounds that
stay complete when one member fails, accepting new runner code and a cost
value that must be read and dated for every model. — 2026-10-17

## Details the orchestrating session decides for Q-13, 2026-10-17

- **Cost value:** each ladder model's `modelle_terms` record carries
  `anfragen_5h` (the Go page's "Estimated requests", Go column, requests per
  5 hours), with the reading date and source it already has. More requests
  is cheaper; the ladder is ordered by `anfragen_5h` descending, ties by id.
  A model without the value is not dropped silently: it goes after every
  valued model and is named on stderr and in the loop record. Reason: the Go
  page states the value per model and it folds token price and quota into
  one number; a declared value keeps the run offline and testable.
- **`modelle` becomes a set:** its order no longer counts. Flash-swarm
  members are not ladder rungs while they are in the swarm.
- **Replacement:** when a Flash member fails (nonzero exit, timeout, empty
  answer), the runner calls the cheapest admitted ladder model that is not
  in this round and not yet consumed, with the same paid-round prompt; if
  that one fails too, the next, each model at most once, until one answers
  or the ladder is spent. A replacement is consumed: it is no later rung.
  Each failure and each replacement is written in the loop record
  (`<model> failed: <reason>; replaced by <model>`) and printed on stderr.
- **Failure reason:** every failed member names the last line of Pi's
  standard error, scrubbed, beside its exit, e.g. "Model is unavailable".
- **Free swarm from the fresh catalog only:** the free stage selects only
  ids in Pi's freshly fetched `opencode-go` overlay; an id that only Pi's
  shipped list carries is not selected (measured 2026-10-17: Pi's
  `mergeModels(baseline, dynamic)` in `core/remote-catalog-provider.js`
  keeps baseline ids that pi.dev no longer lists, which is how
  `step-5-preview-free` reached round 1 and failed with "Model is
  unavailable").
- **Flash swarm tends to the three cheapest:** maintainer, 2026-10-17, "Tendenziell soll der Schwarm aber aus den drei günstigsten Modellen bestehen" — the list stays hand-kept; when it differs from the three admitted models with the highest anfragen_5h, the runner prints a notice and writes one line in the loop record naming both sets; exit unchanged.
- **[DETAIL] Overlay read, 2026-10-17 (implementation session):** read Pi 1.2.0 `core/remote-catalog-provider.js` (`withRemoteCatalog.refreshModels` persists the fetched pi.dev entry `{models, lastModified, etag, checkedAt}` through `context.publish({persist})`), `core/models-store.js` (`FileModelsStore` writes it under the provider id into `models-store.json` beside `models.json`, i.e. in `PI_CODING_AGENT_DIR`) and `core/model-runtime.js` (the path). `pi --list-models` shows `mergeModels(baseline, overlay)`. Chosen: after the forced refresh the runner reads `<scratch agent dir>/models-store.json`, takes `opencode-go.models[].id` as the overlay, and selects only free ids in both the listing and the overlay; a missing or unreadable store refuses the free stage. The overlay ids are pinned in the run state (`free.overlay`). Not measured against the live network (no real Pi call was made).
- **[DETAIL] Unread catalog ids, 2026-10-17 (maintainer addition):** when the run's overlay holds a non-free id with no `modelle_terms` record, the runner names it on stderr and in one record line ("in the live catalog without a terms reading: …") at the run's first round. It never admits it: a paid model still needs a dated terms reading and `anfragen_5h`.
- **[DETAIL] Replacement details, 2026-10-17 (implementation session):** a failed replacement is consumed too (each model at most once per run); replacements are chosen per failed member in member order; the replacement's name joins the round heading and its rows; with no replacement left the failure is named ("no replacement is left on the ladder"); the swap statements replace the plain "failed:" line for a replaced member; the failure reason ends with the last scrubbed Pi stderr line in parentheses, and a swarm member's printed stderr tail is prefixed `<model>: `. `anfragen_gelesen` and `anfragen_quelle` sit beside `anfragen_5h` in each terms record.

## Q-14 · How the change goes on after its loop is spent

asked: 2026-10-17
answer: "mach a" — option A: the pull request is finished as it stands; the five-rung ladder runs first on the next change
answered_by: maintainer
status: answered
context: |
  Topic: the review-swarm change after its loop run could not start again.
  Intention: the maintainer had chosen (answer "B", 2026-10-17) a fresh loop run with the current ladder before the pull request.
  Today: the release refused nothing, but the next `review-loop` call refused ("every stage of this run is consumed"); ADR 0021 decision 9 keeps consumed stages across a release, so no fresh run exists for this change. Phase 6 has no open BLOCKER.
  Repository change: Options: A — finish the pull request as it stands; B — amend decision 9 so the maintainer can order a fresh run, then run it here. Recommendation was A.
  Architecture change: none for A; B would change ADR 0021 decision 9.

In the context of a loop run whose snapshot predates the admission of more
paid models, facing a design that keeps consumed stages across a release,
we decided to finish the change as it stands, to achieve a reviewed change
without growing it further, accepting that the full ladder is first
measured on the next change. — 2026-10-17

## Q-15 · Whether the probe goes on after a failed member

asked: 2026-10-17
answer: "Ja" — the probe names a failed member and goes on to the next; it never substitutes a model
answered_by: maintainer
status: answered
context: |
  Topic: the compatibility probe (`stage2.py probe`) of the review loop.
  Intention: the maintainer asked which models are reachable through Pi; two probe runs on 2026-10-17 each stopped at their first failed free member (`step-5-preview-free` "Model is unavailable", then `cat-jam-free` with an empty answer), so no paid model was measured.
  Today: the first failed call ends the probe; spec criterion 14 asks for every discovered free and eligible paid member to be checked once.
  Repository change: Recommendation was yes — each failure is printed with its reason, the probe continues, and ends with a list of answered and failed members; no second address and no substituted model.
  Architecture change: none; ADR 0021 is unchanged.

In the context of a live free catalog that changes within the hour, facing a
probe that stopped at the first unreachable member, we decided to let the
probe name every failure and go on, to achieve one complete reachability
list per run, accepting that a probe with failures exits nonzero only after
all members were called. — 2026-10-17

## Q-16 · Reachability before each fresh review run

asked: 2026-10-17
answer: "ja" — direct PR #157 toward general availability preflight and defer the individual MiMo replacement
answered_by: maintainer
status: answered
context: |
  Topic: dynamic availability checking for the review loop.
  Intention: detect failures such as MiMo Flash before starting the review ladder.
  Today: the free catalog is refreshed live; paid membership remains configured. Actual reachability probes consume additional requests.
  Repository change: PR #157 selects reachable, already admitted models, reports the selection and pins it for the run.
  Architecture change: yes, stage2.py changes its review behavior; data-terms and cost admission remain.
  Recommendation: yes, a general availability check instead of a single MiMo exception.
  Question: Should PR #157 implement that general check and defer the individual MiMo replacement?
stated_in: "Codex conversation, 2026-10-17; maintainer answered ja immediately after this question"

In the context of models listed but not served, facing a ladder that can
start with unreachable reviewers, we decided to check the actual availability
of admitted candidates before every fresh review run and report the resulting
selection in the main Claude Code or Codex conversation, to achieve a ladder
built from reachable models, accepting additional probe calls and a pinned
point-in-time selection rather than a promise of continuing availability.
— 2026-10-17

### Implementation details for Q-16

- A separate `prepare-loop` invocation performs static, tool-free probes
  through the existing runner and pinned Pi. It sends no repository content;
  declaration and leak checks still run before each call. Each probe has
  a 60-second timeout. Only ordinary call failures permit continuing.
- The paid pool remains the declared, terms-admitted set. Require a known
  cost value and presence in the fresh provider overlay. Select up to three
  cheapest reachable paid models for the Flash swarm; the rest form the
  cheap-first ladder. This supersedes Q-13's hand-kept Flash membership for
  new availability-enabled runs. Old snapshots are preserved.
- Print reachable, failed and skipped ids and the resulting stages. The
  orchestrator relays that report in the main conversation, then supplies
  its report id to `review-loop --availability-reported <id>`. This is an
  orchestration acknowledgment, not a measurement of what the UI displayed.
- Store the preparation receipt outside the repository. Bind it to the
  worktree, endpoint configuration and diff; reject it after 15 minutes or
  any input change. Preparing never resets existing or released run history.
  Failed preparation invalidates an older receipt. No answering candidate
  means refusal, never a clean review result.
- Production configuration enables this protocol. A declaration without
  the new rule retains legacy behavior for compatibility; the repository's
  declaration and its tests require the new rule.
- Honor the maintainer-declared GLM outage without probing GLM before
  2026-10-21T20:34+08:00. Expiry permits a check, not automatic admission.
  Timed model-family prefixes match both the full id and its final component,
  so an id namespace cannot bypass the exclusion.
- The runner refactor is independent work (coding-harness-vg9, split the
  runner into cohesive modules); this change introduces only its bounded
  availability helper. The old MiMo-only configuration question is deferred.
