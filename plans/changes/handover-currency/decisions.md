---
title: "Decisions — handover-currency"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, handover, architecture, currency]
---

# Every handover checks the architecture documentation and the front page — Decisions

Phase 1a for bead coding-harness-ni8, asked by the orchestrating Claude Code
session on 2026-10-14, each question with its context first (what it is
about, why, what happens today, what changes).

## Q-1 · What "checked" means

asked: 2026-10-14
answer: every handover carries a section that names each document as current or as stale with what is stale; small corrections go into the handover's pull request, larger ones become a bead. In addition, the status in the maintainer's ADHD vault, registered there as the management vault, is updated; later this moves to a kanban or another project-management board.
answered_by: maintainer
status: answered

The maintainer's words, 2026-10-14: "wie empfohlen, zusätzlich soll noch in
adhs vault das hier als management vault eingetragen ist ein update des status
gemacht. irgendwann geht das auf ein kanban board oder anderes
projektmanagement board über". Read on 2026-10-14: the vault lives at
`~/ADHS-Vault`; its note `_agent/Vault-Repo-Abgleich.md` registers this
repository with the notes `20-Projekte/Software/coding-harness.md` and others,
plus `Software-Board` and `00 Software`, and a daily reconciliation at 21:45
already compares them with the repositories. AGENTS.md ("Research about this
repository lives in docs/research/") makes a vault note a view that names its
source path and commit; how the handover's status update and the existing
daily reconciliation share the work is left to the spec.

In the context of documents that go stale while sessions change the code,
facing the choice between a section with small fixes, a section only, and an
automatic check, we decided on a section with small fixes plus a vault status
update to achieve that each handover leaves the front documents and the
maintainer's board current, accepting longer handovers. — 2026-10-14

## Q-2 · Which documents are checked

asked: 2026-10-14
answer: `docs/architecture/`, `AGENTS.md`, `ROADMAP.md`, `README.md`, and the ADHD vault's notes for this repository.
answered_by: maintainer
status: answered

In the context of five places where the state of the repository is described
for readers, facing the choice of which to include, we decided on all of them
to achieve one complete check, accepting a longer section. — 2026-10-14

## Q-3 · Whether a gate enforces the section

asked: 2026-10-14
answer: required from its adoption — the handover schema demands the section in every new handover and `make verify` goes red without it; older handovers stay as they are.
answered_by: maintainer
status: answered

In the context of a template rule a model can skip, facing the choice between
a required section and a report only, we decided on required from adoption to
achieve that no handover skips the check, accepting a schema change that
reaches the handover corpus's checker. — 2026-10-14

## Q-4 · Whether the rule travels with the kit

asked: 2026-10-14
answer: yes, configured per repository — each repository names its architecture documentation, its front page and its board or vault; the check runs the same everywhere.
answered_by: maintainer
status: answered

In the context of other repositories with their own documents (first
lakeswitch-ai), facing the choice between a per-repository setting and this
repository only, we decided on a per-repository setting to achieve one check
everywhere, accepting a setting the kit must carry. — 2026-10-14
