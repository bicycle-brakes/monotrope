---
title: "Evaluation — a shared model wiki and the Elephant-Goldfish Model, against the harness"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-g4iq
tags: [evaluation, memory, knowledge, review, outside-practice]
---

# A shared model wiki and the Elephant-Goldfish Model, against the harness

The maintainer asked on 2026-11-02 for an evaluation of two outside sources
for this repository's approach. This is a first reading by the orchestrating
session, not the research swarm: the swarm route that evaluations take
(maintainer, 2026-10-27) was blocked that day by the full disk of the machine
and by the open Pi path leak (bead coding-harness-xul8). A swarm pass can
re-check it.

## Sources and what was read

- **"Less memory, more wiki"**, Siim Tolk, dated 2026-10-31
  (<https://siimtolk.github.io/articles/model-wiki/>): the whole article, read
  2026-11-02. The projects it cites (Karpathy's LLM wiki, ai-memory, Basic
  Memory, OpenWiki, agent-wiki) were not opened.
- **google/elephant-goldfish-model** ("EGM",
  <https://github.com/google/elephant-goldfish-model>, Apache-2.0, created
  2026-09-13, last push 2026-11-01, 9,976 stars on 2026-11-02): the README,
  `TESTING.md`, the skills `egm-review`, `egm-review-loop` and
  `egm-drift-report`, and the reviewer personas `zoom_out` and
  `comprehension`, read 2026-11-02 through the GitHub API. Not read: the
  architecture document, `docs/designs/`, the other five personas, the
  document standards, and Dave Rensin's essay the ideas come from.

## Evidence quality

- **Model wiki:** one author, a home setup with two agents, one measured
  night of 22 questions checked against the live system; six runs excluded.
  With the wiki both agents answered 22 of 22; without it Claude Code answered
  18 of 21 and the local agent 13 of 17, slower and with three to four times
  the tokens. The author names the limits himself. The design is plausible and
  cheap; the numbers are an anecdote, not a measurement this repository can
  lean on.
- **EGM:** no measurement. The README says "Thousands of Google engineers use
  EGM" and that it "is not an officially supported Google product".
  `TESTING.md` covers offline checks of frontmatter, links and plugin
  manifests, plus an opt-in reviewer probe; nothing measures review quality.
  The star count after seven weeks shows attention, not effect.

## Where each idea meets the harness

### The model wiki (knowledge across sessions)

| Idea | The harness on 2026-11-02 | Verdict |
|---|---|---|
| Agents never edit pages; they drop short, sourced notes in an inbox; one steward merges, disputes, asks or discards, and treats notes as data | One writer exists for the tracker (house rule 4, ADR 0006) and for handovers (append-only). The other knowledge stores — `AGENTS.md`, `docs/WORKFLOW.md`, bead notes, the maintainer's Claude Code memory and user instructions — have no inbox and no steward; they are condensed by hand at session end | **Adopt as the design candidate of the consolidation run (bead coding-harness-g4iq).** The bead already names the problem; inbox plus one steward fits the one-writer rule and the "propose, never write" rule for human-decided files better than a pass that rewrites stores directly |
| Private memory holds working preferences only; a setup fact in memory becomes a pointer to its page | The repository already says a standing rule belongs in `AGENTS.md`, not in memory. The memory index still carries setup facts that expire (2026-11-02: a Codex budget window of 2026-10-20, a runner fallback "until bead eao", the `/usr/bin/grep` waiter fact). The two personal instruction files `~/.claude/CLAUDE.md` and `~/AGENTS.md` are near-copies, and both still state the model-availability window that ended 2026-10-21 | **Adopt the rule; the sweeper later.** The pointer rule costs nothing to state; an automated sweeper only after the rule fails twice, as the author himself advises |
| Facts about the machine (ports, timers, services) are regenerated from the machine every night, not remembered | The tracker view, `plans/INDEX.md` and the run report are regenerated. Nothing records the machine's state: on 2026-11-02 the night ran into a full disk, 22 worktrees and 22 GB of swap that no page showed (handover of 2026-11-02) | **Adopt, narrowly:** a machine-facts block (free disk, swap, worktree count, running jobs) generated at night-run start and in the morning status. It feeds the disk floor of the verify admission (bead coding-harness-87b0) and the clean-up after merge (bead coding-harness-kpaq) |
| A short brief of the most-asked facts is loaded at every session start | The start hook loads the latest handover's "Resume here" and `tools/bd prime` | **Have it.** Not measured here; the article reports it roughly halved answer time |
| An outcome test: fixed questions, expected answers read from the live system, run nightly | Nothing measures whether a fresh session knows the harness's current rules and state; gates measure artefacts, not knowledge | **Adopt as the acceptance test of bead coding-harness-g4iq:** a small question set (which model repairs, what the verify admission's floor is, where run plans live) answered by a fresh session before and after consolidation |
| "Enforce, don't ask"; "add machinery only when something fails twice" | `docs/WORKFLOW.md` §4 ends case repair at the second finding of one mechanism; several rules are still "stated, not enforced" (the one-writer guard D-60) | **Convergent.** No change; it confirms the existing direction |
| Pages go stale after 60 days; a page is marked stale when a cited source changes | Artefacts carry `last_reviewed`, and the plans registry checks age | **Partly have it.** Source-change staleness needs pinned sources; most of the harness's sources are files with commits, so it is feasible later |

Rejected by the author, and not proposed here either: every agent writing
pages directly, filing whole session logs (they carry keys and private
messages), and a database-backed memory. The last matches bead
coding-harness-g4iq's "no product adoption: the repository stays file-based".

### The Elephant-Goldfish Model (design review with fresh contexts)

| Idea | The harness on 2026-11-02 | Verdict |
|---|---|---|
| "Goldfish" reviewers see only the document and its referenced sources, never the conversation; a review in the author's own context "is not a Goldfish review" | Spec review (phase 2a) runs Opus in a fresh, read-only context; the review loop (4b) gives other model families the diff alone, without tools; phase 6 is a fresh read-only Codex session that never repairs | **Have it, stricter:** the harness also changes model family, which EGM does not |
| The "Elephant" keeps the context, sorts findings into contest or fix, and applies fixes | The orchestrator marks loop rows taken or rejected with a reason; a separate Codex session repairs | **Have it** |
| A reviewer that fails or returns nothing is "not run", never a reviewer with zero findings; retry once | Failed members are written into the loop record, a replacement is started, and a clean answer over a cut diff does not end the loop | **Have it** |
| Comprehension reviewer, "paraphrase first": restate what the document proposes; a section that cannot be paraphrased is a blocker — "a list of undefined terms does not find a document whose terms are all defined but whose parts do not connect" | Spec review answers three fixed questions (two readings, missing decisions, criteria that cannot go red). House rule 7 and ADR 0018 demand self-contained text, but no reviewer tests it | **Adapt — the one new mechanism worth taking.** A paraphrase step in the spec review would test house rule 7 where it matters, before anything is built. A bounded change to `prompts/02a-spec-review.md`; it widens "three questions and nothing else", so the maintainer decides |
| Zoom-out reviewer: YAGNI, and a code search for existing helpers before new ones are written | The worth of a goal is settled by the maintainer in the interview (phase 1a) and kept out of the spec review on purpose. Reuse is not checked: in the 2026-11-02 review loop of the red-first change, two rounds found the same duplication between two proofs (rows L4-3 and L5-4) | **Reuse search: consider for phase 6**, which has tools. **YAGNI: keep with the maintainer** |
| Drift report: design documents against current code, differences only | The plans registry reports structural drift (status, frontmatter, age). Whether living specs still match the code was not checked in this reading | **Open:** worth a spike only after the living-spec layout settles |
| One question per gate, artefacts in files rather than chat, plain English, no flattery | ADR 0018 and the maintainer's ADHD rules require the same | **Convergent,** with one deliberate difference: EGM forbids a "(Recommended)" option; the harness requires a recommendation with its consequence |
| Install as a plugin for Claude Code and Codex | — | **Do not install.** EGM writes its own drafts and specs (`design_draft.md`, `docs/designs/`) beside `plans/changes/`, with its own phases and no gates; it would run a second workflow in parallel to this one |

## Recommendation

1. **The model wiki's design goes into the consolidation run (bead
   coding-harness-g4iq) as its leading candidate:** an inbox per writer, one
   steward, memory as pointers, and an outcome question test as the
   acceptance measure. This is the highest fit: the bead exists, and the drift
   it describes is visible today in the two personal instruction files.
2. **A bounded change adds EGM's paraphrase step to the spec review**
   (`prompts/02a-spec-review.md`). Cheap; needs the maintainer's word because
   it changes the prompt's fixed three questions.
3. **A machine-facts block at night-run start and in the morning status**
   joins the disk-floor bead (coding-harness-87b0).
4. **Not adopted:** the EGM plugin, a database memory, YAGNI judgements by a
   reviewer.

## Not done in this reading

No experiment ran: neither the outcome test nor EGM's reviewers were tried on
this repository. The EGM architecture document, five personas and its
document standards, and the projects the article cites were not read.
