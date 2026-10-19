---
title: "Prompts for the README graphics"
category: presentation
created: 2026-10-20
updated: 2026-10-20
status: draft
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [readme, graphics, brand, prompts]
---

# Prompts for the README graphics

Prompts for an AI design tool that draws the three README diagrams as
illustrations in the bicycle-brakes style. The Mermaid diagrams in
`README.md` stay the source: they are searchable, versioned and change with
the workflow. An illustration is the first impression next to them, never a
replacement.

## Brand in short

- **Attitude:** calm, close to nature, reduced — mid-century modern outdoor
  posters, grounded rather than loud.
- **Colours:** warm white `#F3EBDD` (background), slate blue `#34566A`
  (primary), sage `#788773` (secondary), terracotta `#CE663B` (the only
  strong accent), anthracite `#292F2D` (text). For illustrations also ochre
  `#DDA344`, dust blue `#7896A3`, forest green `#394B43`.
- **Text on colour:** terracotta and sage are too weak for body text on warm
  white; use `#A84A22` and `#5C6B57` for text. Terracotta as a fill reaches at
  most about 3.6 : 1 with any text colour, so labels sit on light tints
  (`#F6D9C8`, `#DCE4E8`) with a terracotta or slate border instead.
- **Type:** Inter, lowercase, geometric.
- **Symbols:** brake rotor = control and one's own pace; path = progress
  without a straight line; waves = different ways of thinking.
- **Principle:** categories differ by pattern as well as colour, never by
  colour alone.
- **Avoid:** photorealism, 3D, gloss, drop shadows, hard gradients, clutter,
  puzzle symbols, circuit boards, neon.

## Shared style block

Put this in front of every prompt below.

```text
Style: clean technical infographic in a mid-century modern poster language,
inspired by Patagonia — flat shapes, no gradients, no shadows, no 3D, no
gloss, no circuit boards, no neon, no puzzle pieces. Warm off-white paper
(#F3EBDD) with a very light paper grain. Palette: slate blue #34566A, sage
#788773, forest green #394B43, dust blue #7896A3, ochre #DDA344, terracotta
#CE663B as the only strong accent (person moments only). All text in Inter,
lowercase, anthracite #292F2D; file paths and commands in a monospace face.
Landscape is reduced to ONE thin band of layered flat hills along the bottom
edge (max 10 % of the height) and a small terracotta sun in one corner —
nothing else decorative. Categories differ by pattern as well as colour
(diagonal stripes, dots, waves, cross-hatch). Every text exactly as given,
legible at 900 px width.
```

## 1. How a change runs

Portrait, 1600 × 2200.

```text
Subject: a vertical swimlane diagram titled "how a change runs".
Three narrow lanes, left to right: "you" (terracotta, diagonal stripes),
"agents" (sage outline cards), "machine checks" (dust blue, dotted pattern).
A single solid anthracite flow line runs top to bottom through the phases.
Each phase card shows: number · name, one line of what happens, and the
file it writes in monospace.

agents lane:
1 · explore — reads the code and the history — plans/changes/<name>/research.md
1a · interview — asks only [DECISION] points — decisions.md
2 · spec — what changes, acceptance criteria, each names its proving test — spec.md
2a · spec review (optional) — a second reader from another vendor
2b · design (by class) — structure, adr draft if architectural — design.md
3 · plan — steps, appetite as a hard stop, pre-mortem — plan.md
4 · implement — code and tests, test first
7 · commit — pull request, beads named in the body

machine checks lane:
5 · verify — make verify: tests, lint and process checks from decisions/gates.yaml
4b · review loop — free model swarm → fast paid swarm → one stronger model per round, cheapest first — until a round is clean
6 · review — fresh read-only session of another vendor — findings.md
guard (small shield icon beside 2a, 4b and 6) — leak check before every external model call
ci — workflow generated from the same gate file

you lane (terracotta flags with stripes):
"you: state the goal" → before 1
"you: answer" → after 1a, minimum set by the change class
"you: read the plan card — silence means go" → after 3
"you: merge — the merge is the decision" → after 7

Return arrows, dashed sage, labelled in small text:
5 → 4 "red gate"
4b → 4 "finding backed by a test or the spec — repair, its test must fail first"
6 → 4 "blocker or divergent view"
A small brake-rotor icon sits on the 4b → 4 arrow with the note
"repair brake: two rounds of only repair-caused findings → a person decides".

Bottom right, a small file-stack icon:
"session end → docs/journal/handover/<date>.md".
```

## 2. Who decides what

Landscape, 1600 × 1000.

```text
Subject: a technical decision-routing diagram titled "who decides what".
Left: a card "open point" with the note "raised in any phase".
It enters a hexagonal router "classify". Three output rails:

rail 1 — terracotta, diagonal stripes — tag [DECISION]
  trigger: "intent · irreversible · risky · external"
  handler: "you"
  record: plans/changes/<name>/decisions.md — "your words, date, the question asked"
  check: gate "question-context" — "every question carries topic, why now, today, change"

rail 2 — dust blue, dots — tag [GAP]
  trigger: "a missing fact"
  handler: "agent explores, never asks"
  record: research.md

rail 3 — sage, waves — tag [DETAIL]
  trigger: "a name · an order · a format · a library"
  handler: "agent decides"
  record: marked line with its reason in spec.md · design.md · plan.md

Below the rails, a separate strip "architecture":
  question "does this change need an adr?" → decisions/answers/<change>/adr.yaml
  (answer, reason, proposal shown, who, when) → gate "adr-answers"
  → docs/adr/NNNN-*.md → "takes effect on merge"

Right edge, a slim panel "guardrails":
  provenance.yaml — "files only a person may change"
  "a pull request touching them is a decision pull request"

Landscape band along the bottom only.
```

## 3. Not every change is the same size

Landscape, 1600 × 1000.

```text
Subject: a technical comparison matrix titled "not every change is the same size".
Top: a small code-like card showing the spec header line in monospace:
  class: spike | bounded | feature | architectural
with the note "declared by the change, read by the gates".

Four columns, each headed by a pattern swatch and a simple line icon:
spike (dots, question mark) · bounded (horizontal lines, short straight path) ·
feature (waves, footbridge) · architectural (cross-hatch, small building).

Rows, as a clean table with thin sage rules:
what it is | answers a question → recommendation | changes an existing flow, decides nothing new | new deliverable: what the system must do or how it is checked | new subsystem or broken interface
interview minimum (gate interview-minimums) | 3 topics or reasoned skip | 1 or reasoned skip | ≥ 3 | 5 when an adr is created or changed
design 2b | never | never | yes, or one sentence why not | always + adr draft
spec review 2a (other vendor) | no | where one is held | yes | yes
review loop 4b | no | yes | yes | yes
review 6 (fresh read-only, other vendor) | no | yes | yes | yes
adr question | — | — | answered in decisions/answers/ | already carries its adr

The "interview minimum" row gets a terracotta stripe marker, because it is
the row that reaches a person.

Footer note in small text with a dust-blue warning triangle:
"no tool checks the class yet — a feature declared as a spike skips the
other-vendor reviews; the review before the merge catches it".

Landscape band along the bottom only.
```

## Before an image goes into the README

1. Read every label against the prompt, word by word; image tools misspell.
2. Check every statement against `docs/WORKFLOW.md` at the current commit —
   the prompts reflect it as of 2026-10-20 (phases, the review routing table
   "Which change gets what", change classes).
3. Leave model names out: they change faster than the workflow, and a role
   ("another vendor") stays true.
4. Store the image under `docs/assets/` and embed it beside, not instead of,
   the Mermaid diagram.
