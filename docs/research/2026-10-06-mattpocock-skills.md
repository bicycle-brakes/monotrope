---
title: "mattpocock/skills against Coding Harness — what is covered, what to adopt, whether to install"
category: research
status: proposed
created: 2026-10-06
last_reviewed: 2026-10-06
updated: 2026-10-06
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-06"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, skills, claude-code, plugins, interview, glossary, testing, debugging, architecture, recurring-jobs]
---

# mattpocock/skills against Coding Harness

## Result first

**Do not install the plugin for work in these repositories. Adopt four
pieces as prompt text, in our own words with credit, and add a
`GLOSSARY.md`.**

- **Most of it is here already.** Of 22 skills, mapped in 19 rows (§3),
  9 rows are covered or done better here, 5 partly, 2 are missing, and 3
  are left out on purpose. Phase 1a already credits the set's
  `grill-me` → `to-spec` pattern.
- **Two real gaps.** Coding Harness has **no debugging discipline** at all
  (no guidance on it in `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/`,
  `templates/` or `tools/claude-code/` at `d5813ec`), and **no place for
  design friction**: the phase 6 review forbids suggestions the spec does
  not ask for, and nothing else picks them up.
- **The glossary is overdue.** About 26 coined terms (gate, valve,
  Leerprobe, kit role, class, appetite, plan card …) are defined across 13
  files, two of them in German. Phase 1a points to a glossary folder and a
  term-discipline page that do not exist in this repository (§4.1).
- **The plugin is the wrong carrier.** 11 of its 27 skills fire on their
  own, and at least five of those collide with rules here: pull request
  bodies, ADRs, research notes, review findings and the one-question rule
  (§5).
- **The criticism lands in part** (§4.6). Coding Harness is the
  maintainer's own process, in his repository, changed only by pull
  requests he merges. But default-proceed plan cards, agent-decided
  mechanics, more process text than he can read, and named mechanisms
  that do not exist do move control away from him.

**Top three adoptions, by value for effort:**

1. A debugging prompt, `prompts/debug.md`: a failing command before any
   theory, ranked hypotheses, the regression test as the planted fault
   (about 2 hours).
2. `GLOSSARY.md` at the root, one pointer in `AGENTS.md`, the broken
   phase 1a pointer fixed, and a report-only check (about half a day).
3. Sharper prompt lines: ask from the frontier, test an answer on an edge
   case, independent expected values in tests, three criteria for "yes,
   an ADR" (about 1 hour).

A second recurring job, the architecture survey, comes later: after the
research re-check job has run (§4.5).

**Next step for the maintainer:** say which of the three to start. Nothing
here needs an install, and nothing is decided until a pull request merges.

## 1 · Question and scope

On 2026-10-06 the maintainer asked how
[mattpocock/skills](https://github.com/mattpocock/skills) can be used in
Coding Harness. It is an MIT-licensed set of agent skills by Matt Pocock;
277,048 stars when read.

Read on 2026-10-06, all as data, none as instructions:

- **The skill set**, `main` at `4588b32` (committed 2026-10-05):
  `README.md`, `LICENSE`, `AGENTS.md`, `CLAUDE.md` (the same text as
  `AGENTS.md`),
  `GLOSSARY.md`, `.agents/adr/0001` and `0002`, `.agents/invocation.md`,
  `.out-of-scope/question-limits.md` and
  `mainstream-issue-trackers-only.md`, `.claude-plugin/plugin.json`
  (version 1.3.1), and the `SKILL.md` of `grill-me`, `grilling`,
  `grill-with-docs`, `domain-modeling` (with its glossary and ADR formats),
  `to-spec`, `to-tickets`, `implement`, `implement-spec`, `tdd` (with
  `tests.md` and `mocking.md`), `diagnosing-bugs` (with its loop script),
  `improve-codebase-architecture`, `codebase-design` (with
  `DEEPENING.md`), `triage`, `ask-matt` (with `PHASE-BOUNDARIES.md`),
  `setup-matt-pocock-skills` (with `domain.md`), `code-review`, `retro`,
  `research`, `handoff` and `wait-what`.
- **This repository** at `d5813ec` (`origin/main`): `AGENTS.md`,
  [`docs/WORKFLOW.md`](../WORKFLOW.md), `prompts/01` to `07` with `01a`
  and `02a`, `decisions/gates.yaml`, `provenance.yaml`,
  `scripts/kit/manifest.yaml`, the docstrings of `scripts/ramp_valves.py`
  and `scripts/kit/probe.py`, the mutation ratchet in `tests/test_ci.py`,
  the change folders under `plans/changes/`, the
  [Agent Skills assessment](2026-09-18-agent-skills-assessment.md) and the
  [Hermes runner note](2026-10-05-hermes-agent-runner.md).
- **Branch `feat/hermes-runner`** at `7beed6b`:
  `prompts/research-recheck.md`.
- **Sibling repositories**, read only: `portfolio-agentic-engineering`
  (`docs/governance/begriffs-disziplin.md`, `docs/glossar/_INDEX.md`);
  `lakeswitch-ai` at `09c9d62` (decisions D-57 "Terms that mean one thing"
  and D-63 "Agent messages fit working memory" in
  `plans/changes/unified-research-and-work-management/decision-interview.md`).

Nothing was installed and no skill was run.

## 2 · What the skill set is

27 skills ship in the Claude Code plugin; 11 are **model-invoked** (the
agent may start them on its own) and 16 **user-invoked** (only a typed
command starts them). The main flow, as its router `ask-matt` describes it:

1. `grill-with-docs` interviews the user and writes `GLOSSARY.md` and ADRs
   as it goes.
2. `to-spec` turns the conversation into a spec on the issue tracker.
3. `to-tickets` cuts it into tracer-bullet tickets with blocking edges.
4. `implement` or `implement-spec` builds them through `tdd` and closes
   with `code-review`.
5. `retro` suggests changes to the agent's environment.

Two side roads: `diagnosing-bugs` for hard bugs and `triage` for incoming
issues. One upkeep job: `improve-codebase-architecture`, "every few days".

Its README sets it against frameworks that "own the process" (GSD, BMAD,
Spec-Kit): they "take away your control and make bugs in the process hard to
resolve". The skills are meant to be small, composable and edited by their
user.

## 3 · Mapping

Verdicts: **covered**, **better here** (this repository does more, or
the same with a stronger check), **partly**, **missing**, **left out**
(not wanted here, with the reason).

| Skill | Here | Verdict |
| --- | --- | --- |
| `grilling`, `grill-me` | phase 1a interview | better here |
| `grill-with-docs` + `domain-modeling` | 1a, ADRs, decision PRs | partly |
| `to-spec` | phase 2 spec, 2a review | better here |
| `to-tickets` | phase 3 plan, beads with blocking deps | partly |
| `implement` | phase 4 (plan as contract, appetite stop) | better here |
| `implement-spec` | stage 3, not active | left out |
| `tdd` | planted faults, mutation ratchet | partly |
| `diagnosing-bugs` | nothing | **missing** |
| `improve-codebase-architecture` + `codebase-design` | nothing | **missing** |
| `triage` | `tools/bd ready`, priorities | left out |
| `ask-matt` | "The workflow in one screen" | covered |
| `setup-matt-pocock-skills` | change folder script, kit, Leerprobe | covered |
| `code-review` | phase 6, findings table | better here |
| `handoff` | handover file and pull request | better here |
| `research` | `docs/research/`, re-check job | better here |
| `retro` | lessons into `AGENTS.md` and gates | partly |
| `wait-what` | rule 7, maintainer's rules | partly |
| `wayfinder` | 1a, research notes | left out |
| `pr` | the two pull request templates | covered |

Why the "better here" rows are better, one line each:

- **Interview:** only a `[DECISION]` reaches the person; a `[GAP]` is read,
  a `[DETAIL]` decided. `grilling` puts every design decision to the user.
- **Spec:** every acceptance criterion names what would refute it, and a
  fresh-context reviewer (2a) reads the spec before anything is built.
  `to-spec` has user stories and no refutation.
- **Implement:** the plan is a contract with a four-line stop, an appetite
  and a `done:` line with evidence. `implement` is five lines.
- **Review:** a findings table with origin (`base`, `fix-r<N>`), escalation
  after two repair rounds, and a rejected finding returns only with new
  evidence. `code-review` has two axes, much like `SPEC` and `MAINT`.
- **Handover and research:** files in the repository, through a pull
  request, with frontmatter and a re-check. `handoff` writes to the
  operating system's temporary folder.

Why the "left out" rows stay out:

- **`implement-spec`** runs implementer subagents in parallel across a task
  graph. Here that waits for stage 3 and the M0 isolation evidence, and
  house rule 4 allows one tracker writer.
- **`triage`** serves a public issue queue. Coding Harness has one
  maintainer and no outside reporters.
- **`wayfinder`** charts multi-session decision maps on the issue tracker.
  Research notes and the 1a interview carry that here; not read in detail.

## 4 · The six questions

### 4.1 · A project glossary

**Recommendation: one `GLOSSARY.md` at the repository root, English,
process terms only, kept current by the change that coins a term and by a
report-only check.**

**The need is measured, not guessed.** A list of the coined terms an agent
meets in the phase prompts and gates gives 26: gate, enforcement
(advisory / report / block), floor, valve, ratchet, planted fault and its
counterpart, Leerprobe, kit, kit role (`mechanismus`, `bestand`), change,
change class, ADR question, decision pull request, appetite, plan card,
acceptance card, `done:` and `Resume:` lines, the question tags, the review
markers `[AMBIGUITY]` and `[DIVERGENT]`, finding, dimension, origin,
handover, writer session, stage, and provenance class. Their definitions
sit in 13 files: `decisions/gates.yaml` (header), `scripts/ramp_valves.py`
and `scripts/kit/probe.py` (docstrings, the second in German),
`scripts/kit/manifest.yaml` (German), `tests/test_ci.py` (comments),
`docs/WORKFLOW.md`, the prompts of phases 3, 4, 6 and 7, `AGENTS.md`,
`provenance.yaml` and the research index.

**Three words already mean two or more things:**

- **class:** change class (`spike` … `architectural`) and provenance class
  (`human-decided` …). LakeSwitch had the same clash and settled it in
  D-57, adding a third, "claim class".
- **stage:** model routing (stage 1–3) beside M0–M4, S0–S7 and T0–T2. The
  research index carries a one-line key for this, which is a glossary
  entry in the wrong place.
- **drift:** the `ci-drift` gate (the generated workflow differs from the
  gate list) and the scheduled `drift` job.

**A broken pointer.** `prompts/01a-interview.md` ("Terms count") sends a
settled term to `docs/glossar/` and to
`docs/governance/begriffs-disziplin.md`. Neither exists here at `d5813ec`.
Both came over from `portfolio-agentic-engineering`, where they hold the
data-domain vocabulary of that repository, in German.

**Would it help?**

- **Agents: yes.** One file to read before writing a prompt, a gate or a
  finding; one spelling per concept; the German identifiers explained in
  English until house rule 1's translation reaches them. Pocock's claim
  that a shared language makes agents shorter is plausible but not
  measured; his evidence is one example.
- **The maintainer: as a lookup, not as reading.** LakeSwitch decided
  that a person is not asked to learn its glossary, and that a term is
  explained where a person first meets it (D-57, D-63). The same holds
  here through house rule 7 and the maintainer's own rule against
  shorthand without context. A glossary must not license jargon in
  messages to him; it gives the agent the one sentence to explain it with.

**Where it would live**, four places weighed:

| Place | For | Against |
| --- | --- | --- |
| `GLOSSARY.md` at the root | one file, found by agents and by tools that follow this convention; reads on a phone | one more root file |
| `docs/glossar/`, one note per term | the pointer already names it; `provenance.yaml` reserves it | 26 files to keep; a German name against house rule 1 |
| a section of `docs/WORKFLOW.md` | no new file | 649 lines already; not found |
| `AGENTS.md` | always loaded | 181 of 200 lines used |

The root file wins. It travels with the kit (role `mechanismus`): an
instance runs the same process and meets the same words, and adds its own
section where it has its own terms.

**How it stays current:**

1. **The change that coins or sharpens a term updates the file**, in the
   same pull request. Phase 1a and `AGENTS.md` say so (§6.2).
2. **A report-only check**, `glossary` in `decisions/gates.yaml`, each
   rule with a planted-fault test as `tests/test_ci.py` requires:
   - every defined term still occurs in at least one other tracked file
     (a term renamed away everywhere else is reported);
   - no word on the file's `Retired` list occurs in `AGENTS.md`,
     `docs/WORKFLOW.md`, `prompts/` or `templates/`.
3. **What no check catches:** a new coined word without an entry. That
   stays stated, not enforced, as in LakeSwitch D-57; the phase 6 review
   may name it.

A new gate changes how the repository is checked, so the change is a
`feature` and owes the ADR question.

### 4.2 · `grill-with-docs` against phase 1a

**Phase 1a is better at who is asked and how often; `grill-with-docs` is
better at words, edge cases and the code. Take those three.**

| Aspect | `grill-with-docs` | Phase 1a |
| --- | --- | --- |
| Called by | the user, "every time" | the maintainer, optional; a skip has a reason |
| Per turn | the whole frontier, numbered | one question |
| What goes to the person | every decision | `[DECISION]` only |
| Facts | a subagent looks them up | `[GAP]`: read, extend `research.md` |
| Record | `GLOSSARY.md` and ADRs, inline | `decisions.md`, Y-statements |
| ADR | offered when hard to reverse, surprising, a real trade-off | a feature's ADR question, answered by the maintainer, merged as a decision PR |
| Terms | challenged against the glossary | pointer to a folder that is missing |
| Edge cases | invents scenarios to force precision | not asked for |
| Code | names where the code contradicts an answer | not asked for |

Two points of `grilling` do not fit here:

- **The whole frontier per round** breaks the maintainer's rule of one
  question at a time. Its maintainers refuse any cap on questions (their
  out-of-scope note cites a user who was asked 200).
- **Every decision to the user** breaks the question protocol: a question
  about mechanics put to the owner of the intent is a protocol violation
  here, not thoroughness.

What to take, in our words (§6.3): **the frontier as the rule for which
question comes next**, one concrete edge case before a decision is
recorded, a named contradiction with the code, and the glossary update.
Its three-part ADR test fits phase 2's ADR question (§6.5).

### 4.3 · `tdd` against planted faults

**Keep planted faults; they prove more. Take two of `tdd`'s test rules.**

| | `tdd` | Here |
| --- | --- | --- |
| Order | red first, then the least code, one slice at a time | the test with the change; order free |
| Proof a test can fail | it failed before the code existed | a fault planted in finished code turns it red, then is taken back; recorded in `plan.md` |
| Gates | — | every gate has a mutation test or a reason in a list that may only shrink (bound 12; 7 entries at `d5813ec`) |
| Where tests go | at seams agreed with the user | per criterion in the plan, seam not named |
| Test quality | through the interface; expected value from an independent source; mocks only at system boundaries | not stated |

What each proves:

- **Red first** shows a test can fail once — possibly for the wrong reason
  (a missing import is red too). It adds design pressure: the interface is
  written before the body.
- **A planted fault** shows the test catches a named wrong behaviour in
  the real code. That is the stronger evidence, and this repository
  applies it to its gates as well (`tests/test_ci.py`, the mutation
  ratchet).

What planted faults miss:

- **A brittle test.** A test coupled to internals goes red on a planted
  fault, and also on a harmless refactor. Planted faults measure
  sensitivity, not robustness.
- **A tautology.** A test whose expected value is computed the way the
  code computes it stays green when the fault sits in the shared source,
  and is caught only if the fault is planted there.

So: add "through the interface its callers use" and "expected value from a
source the code does not use" to phase 4, and name the seam per criterion
in phase 3 (§6.4). Do not ask the maintainer to agree seams, as `to-spec`
and `tdd` do: a seam is mechanics, a `[DETAIL]` here. Red first may stay
an allowed order, not a rule.

### 4.4 · `diagnosing-bugs`: the missing debug discipline

**Missing, and worth adopting as a prompt of its own.**

What exists here: nothing named. The appetite stop bounds time inside a
change, and two failed repair rounds escalate (`docs/WORKFLOW.md`, the
findings process). Neither says how to find a cause.

The skill's core, in six steps:

1. **A loop before a theory.** One command, already run once, that is
   red on this bug, gives the same verdict every run, finishes in seconds
   and runs without a person. No hypothesis before it exists.
2. **Shrink** the case until every remaining part is needed for red.
3. **Three to five ranked hypotheses**, each with the prediction that
   would refute it, shown to the user before testing (without waiting).
4. **One variable per probe**; every debug print carries one tag, so one
   search removes them all.
5. **The regression test at the seam where the bug occurs**, red before
   the fix; where no seam reaches the bug, that is the finding.
6. **Clean up**, and state the hypothesis that held in the commit message.

It fits this repository unusually well. Step 5 is the planted-fault rule
with the fault supplied by the bug: revert the fix and the test must go
red. Step 1 is "claim nothing unread" applied to causes.

**Where it lives:** `prompts/debug.md`, a discipline prompt beside the
phases (like the research re-check, "not one of the seven phases"), with
one pointer from phase 4 and one from `AGENTS.md`, because most debugging
happens outside a change (§6.1).

### 4.5 · `improve-codebase-architecture` as a second recurring job

**Yes, as job two, after job one has run. Lower exposure than job one,
real targets, and it fills a gap the review leaves on purpose.**

**The gap.** Phase 6 reports correctness faults, gaps against the spec and
gates that cannot bite — "no suggestions the spec does not ask for".
That keeps reviews sharp, and it means design friction found on the way
has nowhere to go.

**Targets exist.** In the 30 days to 2026-10-06, `scripts/kit/probe.py` and
`scripts/kit/manifest.yaml` changed in 18 commits each and
`scripts/ci_gates.py` in 17; `tests/test_ci.py` holds 1,181 lines. That
is the hot-spot signal the skill starts from.

**What the job would be**, in the form of `prompts/research-recheck.md`:

- **Input:** the repository at one commit, the last 30 days of history,
  the ADRs.
- **Work:** find the hot spots; read them; apply the deletion test
  ("would deleting this module concentrate complexity, or just move it?").
- **Output:** one new note under `docs/research/`, at most three
  candidates, each with files, the friction in one sentence, the deepening
  in plain words, which tests would move to the interface, a strength
  (strong / worth exploring / speculative), and any ADR it would reopen,
  with the reason.
- **Never:** code, interfaces, tracker commands, git or GitHub actions.

**Against job one:** it needs no web access, so no fetched page can steer
it. It creates one new file instead of appending to one, so the runner's
post-check must allow exactly one new path under `docs/research/`.

**Cadence:** monthly, or after a set number of merged pull requests. The
skill's "every few days" fits a product codebase; this repository holds
about 5,700 lines of scripts (19 at the top level) and 7,900 of tests at
`d5813ec`.

**Order:** the Hermes runner note's first slice comes first — the
research re-check by hand, two or three times. Then the survey runs once
by hand; the vocabulary it needs (module, interface, depth, seam, adapter,
leverage, locality) goes into `GLOSSARY.md` when it is adopted. The
maintainer picks a candidate; the tracker writer opens a bead; the change
runs through the seven phases.

### 4.6 · "Process-owning frameworks take away your control"

**The criticism lands in part.** Honest list, numbers at `d5813ec`:

**Where it misses:**

- **It is his process, not a vendor's.** Every rule is a plain file in his
  repository; nothing updates behind his back; a decision takes effect
  only when he merges its pull request (ADR 0008).
- **Bugs in the process are visible.** Gates are one list
  (`decisions/gates.yaml`), each with a reason; an exception is a valve
  whose switch-up condition a test checks.

**Where it hits:**

1. **Control is a veto he has to catch.** A plan card starts phase 4
   "unless you say stop"; `[DETAIL]` and mechanics are decided by agents
   and written into artefacts. Only a card that widens the scope waits
   for his "ok". That is the design (low friction), and it means a card
   he did not see is consent.
2. **More process text than he can read.** `AGENTS.md`,
   `docs/WORKFLOW.md` and the phase prompts hold 1,375 lines. The
   research-currency change (pull request #73) carried 1,334 lines of
   change artefacts for 1,146 lines of code and tests, over 16 commits;
   one plan (`harness-decide-adr`) has 799 lines. A process whose
   artefacts the owner cannot read is steered by whoever writes them —
   the agents.
3. **A bug in the process is fixed through the process.** A wrong gate
   needs spec, plan and review rounds; research-currency, a report-only
   date check, took a repair round and a second review round. Ratchets
   bind him too. The escape hatch, "never plan what one sentence
   describes", has no size.
4. **Named mechanisms that do not exist.** `docs/WORKFLOW.md`'s header
   honestly lists 13 pieces it names that are not in the tree (still
   absent at `d5813ec`: the artefact validator, the explorer and reviewer
   subagents, the stop hook, `templates/findings.md` …). The phase
   prompts name them as gates without that caveat: phase 2's gate is a
   validator that is not here. A reader can believe a protection exists
   that does not.
5. **His own words need a translator.** The coined terms of §4.1 have no
   single place to look up, so he depends on agents to explain his own
   process.

None of this argues for dropping the process. Items 4 and 5 are cheap to
close; items 1 to 3 are trade-offs the maintainer chose. §6 adds about 60
lines of prompt text, a glossary file and one report-only gate: that is
item 2's cost, and the reason each piece is kept short.

## 5 · Options

| Option | Consequence | Verdict |
| --- | --- | --- |
| (a) Install the plugin | 27 skills in every repository on the machine; collisions below; updates without review here | not for repository work |
| (b) Adopt four pieces as prompt text, in our words, with credit | reaches every harness; reviewed like any change; about 3–4 hours | **recommended** |
| (c) `GLOSSARY.md` and its check | one file to keep; a `feature` with an ADR question; about half a day | **recommended**, as its own change |
| (d) Nothing | no debug rule; phase 1a's pointer stays broken; terms stay scattered | not recommended |

**Why not (a), concretely.** Installing is the maintainer's decision;
agents never install into `~/.claude`. If he does, these collide:

1. **`pr`** (model-invoked) shapes every pull request body its own way;
   here both templates carry the acceptance card, and decision pull
   requests a block of their own (ADR 0008).
2. **`domain-modeling`** (model-invoked) offers ADRs and writes them into
   `docs/adr/` as one paragraph without frontmatter; ADRs here are
   `human-decided`, carry frontmatter and take effect through a decision
   pull request.
3. **`research`** (model-invoked) writes a cited note "where the repo
   keeps such notes" — `docs/research/` — and nothing in it asks for the
   frontmatter, index row or provenance class a note here needs.
4. **`code-review`** (model-invoked) adds a baseline of code-smell
   findings unless a standards file it finds says otherwise; phase 6
   allows no style findings.
5. **`grilling`** asks the whole frontier at once; the maintainer's rule
   is one question at a time.
6. **`to-spec`, `to-tickets`, `triage`** need a configured tracker; Beads
   is not one they support (their out-of-scope rule takes mainstream
   trackers only), and a ticket written from a second session breaks the
   one-writer rule.
7. **Updates arrive when the official listing's pinned commit moves**
   (their ADR 0002), so third-party text changes inside sessions without
   a review here.
8. **A user-level install reaches every repository**, the customer
   instance included. Whether a plugin can be enabled for one project
   only was not verified.

If he wants to feel `grill-me` or `wait-what`, trying them outside these
repositories is his call.

**Credit and license.** The adopted text is ours; each prompt names its
source skill and the repository, as phase 1a already does. Copying
substantial text verbatim would carry the MIT notice ("Copyright (c)
2026 Matt Pocock", `LICENSE`); none is proposed.

## 6 · Proposed changes

Proposed, not implemented, not tested.

### 6.1 · Debug discipline (adoption 1)

New file `prompts/debug.md`, about 40 lines. Its core:

```markdown
# Debug · a discipline, not one of the seven phases

**When:** a test, a gate or a run fails and the cause is not clear after
one look — in phase 4, in a repair round, or outside any change.
**Result:** a fix, a test that is red without it, and the cause in the
commit body.
The loop follows `diagnosing-bugs` in
[mattpocock/skills](https://github.com/mattpocock/skills), in this
repository's words.

1. **A command before a theory.** Build one command that shows the
   failure and run it: a test, a script with a fixture, a bisect run. It
   hits the reported symptom, not a nearby one; it gives the same verdict
   every run; it takes seconds. No hypothesis before it exists. If none
   can be built, stop: say what you tried and what you need.
2. **Shrink the case** one part at a time, until every remaining part is
   needed for red.
3. **Three to five hypotheses, ranked.** Each says what would refute it:
   "if X is the cause, changing Y makes it green." Show the list, then
   test without waiting for an answer.
4. **One variable per probe.** Tag every debug print `[DEBUG-<4 hex>]`.
5. **The regression test is the planted fault.** Write it where the bug
   occurs; see it red on the unfixed code; fix; see it green. Where no
   test can reach the bug there, write that down: it is a finding.
6. **Done:** the command of step 1 is green on the original case,
   `make verify` is green, `rg '\[DEBUG-'` finds nothing, and the commit
   body names the hypothesis that held.

After three failed fixes for the same symptom, make no fourth: name the
assumption that may be wrong. A cause no evidence shows yet is "cause not
yet known".
```

`prompts/04-implement.md`, after its last paragraph:

```markdown
When a test or a gate goes red and the cause is not clear after one look,
follow `prompts/debug.md` before changing code.
```

### 6.2 · `GLOSSARY.md` (adoption 2)

New file `GLOSSARY.md`; the form, with three of about 26 entries:

```markdown
# Glossary

The words this workflow coined, one meaning each. Process terms only; a
term an instance adds goes under a heading of its own. In a message to a
person, a term is still explained where it is first used.

**Gate**:
A check listed in `decisions/gates.yaml`, the one list that `make verify`
and CI run; its enforcement is advisory, report or block.
_Avoid_: check (for a gate), guard

**Valve**:
An exception that lets a gate report lower than its target until a
stated, measured condition holds; listed in `scripts/ramp_valves.py`, and a
test turns red when the condition holds and the valve is still open.
_Avoid_: waiver, exception

**Kit role**:
Whether a file travels to another repository: `mechanismus` carries the
workflow and runs there unchanged; `bestand` describes this repository
and stays.
_Avoid_: kit type

## Retired

- Stufe: say stage (model routing), or name the M-, S- or T-step
```

`AGENTS.md`, after "Full doctrine: `docs/WORKFLOW.md` …" (3 lines; 181 →
184 of 200):

```markdown
Coined terms (gate, valve, appetite …) are defined once, in `GLOSSARY.md`;
a change that coins or sharpens one updates it. Debugging follows
`prompts/debug.md`: a failing command first, then hypotheses.
```

`prompts/01a-interview.md`, the paragraph "Terms count" replaced:

```markdown
**Terms count.** Where the interview settles what a word means in this
repository, add or sharpen its entry in `GLOSSARY.md` in the same change.
Where an answer uses a word against its entry, say so and ask which holds.
```

Also, in the same change: a `GLOSSARY.md` rule in `provenance.yaml` beside
`ROADMAP.md` (`human-written`, `ai-drafted-reviewed`; no frontmatter); a
kit rule with role `mechanismus` in `scripts/kit/manifest.yaml`;
`scripts/check_glossary.py` with its gate entry (`enforcement: report`)
and tests named so the mutation ratchet sees them
(`test_the_check_notices_a_term_no_other_file_uses`,
`test_the_check_notices_a_retired_word_in_a_prompt`, and the counterpart
`test_a_term_a_prompt_uses_is_not_reported`).

If (c) is declined, the broken pointer in phase 1a still goes: delete the
"Terms count" paragraph.

### 6.3 · Interview lines (adoption 3)

`prompts/01a-interview.md`, under "How you ask", after "One question at a
time.":

```markdown
**Ask from the frontier.** The next question is one whose prerequisites
are already answered; a question that depends on an open one waits. (The
frontier is `grilling`'s idea, in mattpocock/skills.)

**Try an answer on one case.** Before recording a decision, apply it to
one concrete edge case; ask again only if the case shows two readings.

**Name a contradiction with the code.** When an answer and the code
disagree, say which file does what; the person decides which is right.
```

### 6.4 · Test lines (adoption 4)

`prompts/04-implement.md`, after "…which plants the fault and goes red.":

```markdown
The test reaches the code through the interface its callers use, so a
change that keeps the behaviour keeps it green. Its expected value comes
from a source the code does not use — a literal, a worked example, the
spec; a value computed the way the code computes it passes by
construction.
```

`prompts/03-plan.md`, the required item on tests:

```markdown
- **Per acceptance criterion the test** that holds it, the seam it tests
  at, and the fault that test would have to meet to go red.
```

### 6.5 · The ADR question (adoption 5)

`prompts/02-spec.md`, after "The proposal only proposes;":

```markdown
Propose `"yes"` only when all three hold: the choice is hard to undo, a
later reader would be surprised by it without this change's context, and
a real alternative was turned down. (The three-part test is from
`domain-modeling` in mattpocock/skills.)
```

### 6.6 · Later: the architecture survey job

`prompts/architecture-survey.md`, in the form of
`prompts/research-recheck.md`, with the input, work, output and "never"
of §4.5. Written once the research re-check has run by hand; about 1–2
hours, then one manual run.

### Left out on purpose

- Expand–contract for wide refactors (`to-tickets`): useful, but no change
  here has needed one yet.
- User stories in the spec, seams agreed with the maintainer, the HTML
  report, `handoff` to a temporary folder, `implement-spec`'s parallel
  implementers, `triage`.

## 7 · Overlap with the parallel notes

- **i-have-adhd** (draft `docs/research/2026-10-06-i-have-adhd-skill.md`,
  uncommitted in its worktree when read, branch not on origin): the same
  verdict on plugins — unreviewed third-party text in every session, one
  harness only. Its proposed `AGENTS.md` block already holds the
  three-failed-fixes rule and "cause not yet known"; whichever lands first,
  `prompts/debug.md` points to it rather than repeating it. Its block adds
  13 lines to `AGENTS.md`, this note 3: 197 of 200 together. `wait-what`
  overlaps its rules on plain re-explanation; nothing is proposed for it
  here. Both notes add a row to the research index; the second merge
  resolves one line.
- **ponytail:** not read. Its worktree held no draft and its branch was
  not on origin when checked (2026-10-06).
- **The Agent Skills assessment** (2026-09-18) reached the same shape for
  another skill pack: adapt techniques as repository text, do not install
  the pack.

## 8 · Not read or not verified

- **Not read:** the `SKILL.md` of `prototype`, `wayfinder`, `pr`, `wizard`,
  `teach`, `to-questionnaire` and `writing-for-agents` (`pr` is judged
  from `ask-matt`'s description); the `docs/` pages, `CHANGELOG.md`, and
  the `misc/` and `in-progress/` buckets.
- **Not verified:** whether a plugin can be enabled for one project only;
  how much context the 11 model-invoked descriptions cost per session;
  whether the official listing's pinned commit equals `4588b32`.
- **Not measured:** that a glossary shortens agent output (Pocock's claim);
  the token cost of one architecture survey run.

## Sources

- **skills:** <https://github.com/mattpocock/skills> at `4588b32`
  (2026-10-05) — the author's own repository, read 2026-10-06 through the
  GitHub contents API; the files listed in §1
- **skills-adr-0002:**
  <https://github.com/mattpocock/skills/blob/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d/.agents/adr/0002-ship-as-a-claude-code-plugin.md>
  — official listing, pinned commit, update path
- **skills-out-of-scope:**
  <https://github.com/mattpocock/skills/tree/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d/.out-of-scope>
  — question limits, mainstream trackers only
- **agent-skills:** [2026-09-18-agent-skills-assessment.md](2026-09-18-agent-skills-assessment.md)
  — this repository's earlier note on another skill pack
- **hermes:** [2026-10-05-hermes-agent-runner.md](2026-10-05-hermes-agent-runner.md)
  — the runner and the first job's order
- **lakeswitch D-57, D-63:** `lakeswitch-ai` at `09c9d62`,
  `plans/changes/unified-research-and-work-management/decision-interview.md`
  — read 2026-10-06
- **portfolio glossary:** `portfolio-agentic-engineering`,
  `docs/governance/begriffs-disziplin.md`, `docs/glossar/_INDEX.md` — read
  2026-10-06
- **Repository reads and counts:** §1, §4.1, §4.5, §4.6 — measured
  2026-10-06 at `d5813ec`
