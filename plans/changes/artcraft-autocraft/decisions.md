---
title: "Decisions — artcraft-autocraft"
class: feature
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-68kr
owner: Data Architect
provenance: ai-drafted-reviewed
review: {status: pending, approved_by: null, approved_at: null}
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-26"}
tags: [decisions, interview]
---

# artcraft autocraft — Decisions

Class: feature (bead coding-harness-68kr, the Artcraft and AutoCraft research). Phase 1a, held with the maintainer in the conversation, in German. The seven questions and the obligation items each one closes are listed in `interview-prep.md`; they close the 161 items of the complete runs e7be7d27 and cfcbfc1a in `research.md`.

## Q-1 · Keep the class feature, or re-declare it?

asked: 2026-11-26
answer: "Feature bleiben, Interview" — the change stays class feature and continues with the interview in this change; spec, plan and implementation follow here.
answered_by: maintainer
status: answered
research_items:
  - e7be7d272599ab4091231773cd532193/H-20
  - e7be7d272599ab4091231773cd532193/H-25
  - e7be7d272599ab4091231773cd532193/H-28
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-23
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-27
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-32
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-73
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-78
context: |
  Topic: the class of the change artcraft-autocraft.
  Intention: the swarm had finished (run cfcbfc1a, commit d16868cb); the interview comes next, and the class decides how much follows it.
  Today: the change is declared feature; one swarm seat reads it as a spike (it answers questions and yields a recommendation), two seats raise architectural.
  Repository change: as a spike, a research note with the candidates, and every candidate the maintainer picks becomes a bead of its own; as a feature, interview, spec, plan and implementation follow in this change.
  Architecture change: only through the candidates, not through this choice.
  Options shown: close as a spike (recommended; downside: each picked candidate waits for a change of its own); stay feature with the interview (downside: several topics are bound to one change); first redo the online part (downside: everything waits, and deepseek-v4.1-flash leaves on 2026-11-30).

In the context of a research change whose swarm has delivered its candidates, facing the choice between closing it as a spike and building in this change, we decided to keep the class feature and hold the interview here, to achieve that the chosen candidates are specified and built in one tracked change, accepting that several topics are bound to one change and that the interview must close the obligation items of both complete runs. — 2026-11-26
