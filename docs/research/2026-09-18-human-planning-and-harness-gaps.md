---
title: "Human planning, attention support and remaining harness gaps"
category: research
status: proposed
created: 2026-09-18
last_reviewed: 2026-09-18
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex
  version: "2026-09-18"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [planning, accessibility, adhd, obsidian, evaluation, recovery]
---

# Human planning and remaining harness gaps

This research addendum responds to the maintainer's request for easier human
planning, particularly with ADHD. It supplements the four original sources
in the [index](_INDEX.md); it proposes an optional planning surface and stronger
execution contracts. No application, plugin or runtime was installed for this
review. The [target](../architecture/2026-09-17-omnigent-first-target.md) defines
authority; the [implementation plan](../architecture/2026-09-17-implementation-plan.md)
assigns delivery and acceptance. Preferences remain configurable and need a
trial with the maintainer; the proposals do not establish clinical efficacy.

## What the existing research already provides

The [Lake Switch architecture](Lake-Switch-Architektur-arc42.md), sections
5.2.2–5.2.3, already places Obsidian above local Markdown and Beads, with an
inbox and a Now/Next/Later roadmap. Its backup and context sections also supply
useful constraints. Carry the separation of authorities forward. Replace a
rigid inbox-cleanup deadline with an agreed review rhythm and optional archive;
capturing an idea must not automatically create assigned work.

The [ADW architecture](arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md),
especially its enforcement discussion, and the
[migration plan](Migrationsplan_Omnigent_Referenzarchitektur.md) establish
protected controls, policy probes and staged adoption. The remaining gaps are
the concrete adapters, acceptance evidence and the human-facing interaction.

## Largest remaining gaps

| Priority | Missing contract | Proposed response and evidence |
|---|---|---|
| P0 | A worker can appear successful after changing its own checker | Protect active gates, policies and expected outcomes; use an approved verifier to assess harness-maintenance changes; prove a harmless bypass is rejected. |
| P0 | Separate worktrees do not prove isolation | Probe shell, child-process, symlink and shared-Git writes, then constrain or mediate those operations. An isolation failure blocks the pilot. |
| P0 | Per-worker limits omit coordination, retries and cancellation | Use a total-run ledger, finite attempts and process-group cancellation; reject stale results after ownership changes. |
| P1 | Green schemas do not measure agent correctness | Keep independently checked faulty, clean and ambiguous fixtures; compare repeated runs and gate critical regressions before upgrades. |
| P1 | Resume promises conflate a process crash and disk loss | Add startup checks and compact context packets; rehearse local restart separately from remote checkpoint/full-store restoration. |
| P1 | Humans must reconstruct the next action from many tools | Provide one small, portable start page with source freshness, a next action, pending decisions and a resume point. Keep task status in Beads. |

These are implementation recommendations derived from the corpus and the
following primary-source checks, accessed on 2026-09-18:

- Git documents shared configuration and repository data across worktrees.
  This supports treating isolation as a separate control to test.
  [Git worktree reference](https://git-scm.com/docs/git-worktree)
- Omnigent documents terminal sandbox configuration. The pilot must check the
  selected version's terminal and subagent settings and effective permissions.
  [OS sandbox documentation](https://omnigent.ai/docs/reference/configuration/os-sandbox)
- Anthropic distinguishes tasks, trials, graders and observed outcomes, and
  discusses balanced evaluations and grader calibration. The proposed small
  evaluation set applies those ideas to this harness; its numerical thresholds
  are local pilot choices.
  [Agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Its long-running-agent guidance describes environment initialization and
  durable artifacts for later sessions. Here those artifacts remain the
  existing specs, Git evidence and Beads rather than another progress tracker.
  [Long-running harness guidance](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Client choice

| Client | Verified basis | Suggested role and limitation |
|---|---|---|
| Obsidian | Local Markdown; Bases can view **and edit** note properties. The application uses its own license; open file formats do not make the application open source. | Suggested first optional client if the maintainer likes it. Begin with core features, a bookmarked start page and templates. Do not expose authoritative task state through editable Bases rows. [Storage](https://obsidian.md/help/data-storage), [Bases](https://obsidian.md/help/bases), [license](https://obsidian.md/license) |
| Foam | Open-source knowledge tooling for VS Code, with templates and linked Markdown notes. | Alternative for planning in the coding editor. Keep portable Markdown links; evaluate the exact editor/extension combination before standardizing it. [Official repository](https://github.com/foambubble/foam) |
| Zettlr | Open-source Markdown writing application. | Alternative for a quieter document-oriented workflow. Use the same start page; do not assume it supplies a live Beads board. [Official repository](https://github.com/Zettlr/Zettlr) |
| Any Markdown editor | The proposed view is ordinary Markdown with relative links. | Required fallback. Essential direction, decisions and resume information remain readable without any client plugin. |

Recommendation: build the portable files and projection contract first; trial
one client. Adding another task database or installing a large plugin set is
not a prerequisite for better planning. Private knowledge and personal client
preferences remain outside the reusable kit.

## A small start page

The initial page has these sections, in this order:

1. **Continue:** current change, last completed checkpoint, one concrete next
   action and the link that opens it. For example: “Review the two options in
   the data-retention decision.” A missing next action is shown explicitly.
2. **Needs your decision:** concise options, recommendation, consequence and
   the exact contract/PR revision the answer would approve. Show blocking
   decisions first; answering a draft note does not itself grant permission.
3. **Now:** one primary focus and up to three visible themes by default.
   This is an adjustable display limit, not an agent concurrency limit.
4. **Waiting:** a short explanation, owner and next review point. Blocked work
   must not look ready. Next/Later and detailed agent activity are collapsed
   or linked from the main view.
5. **Capture:** one shortcut to add an idea without mandatory classification.
   Triage can later link it to an existing change, promote it once, or archive it.

Every generated page shows the Git revision and tracker snapshot time/revision.
An unavailable or old snapshot says **unknown/stale**, never “nothing to do.”
The renderer records when it took the snapshot, the Beads/Dolt revision it
read, and the Git commit used for linked contracts. At render time it checks
both against the current checkout; on mismatch it shows a stale banner and
suppresses any claim that a task is ready. A page opened later cannot prove
live freshness, so it displays its capture time and a link to refresh through
the authorized coordinator. The next-action line may be authored by the human;
it is labelled as guidance, not as a Beads status or a new approval.
Generated content is not manually edited or synchronized back to Beads. The
projection is read-only by contract; an integrity check must catch manual edits
before regeneration, with a recoverable copy rather than silent data loss.

## Attention and interruption defaults

W3C cognitive-accessibility guidance recommends helping users reorient and
limiting interruptions. Those principles support the following design choices;
they do not prescribe this particular layout or a universal ADHD workflow.
[Focus guidance](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o5-user-focus/),
[interruption guidance](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o5p01-minimal-interruptions/)

| Need | Proposed default | User control |
|---|---|---|
| Start without rebuilding the whole plan | One next action with a visible done condition and effort range where useful | Change or hide estimates; select another focus |
| Resume after interruption | Persistent “last done / next / waiting on” breadcrumb derived from the handover and change | Open detail without losing the start page |
| Avoid competing signals | Batch routine agent updates; interrupt only for an actionable blocker, decision or configured urgent event | Quiet period and notification preferences |
| Capture a thought cheaply | Plain text inbox entry with automatic date; no required tags | Optional template or later classification |
| Avoid backlog pressure | Hide Later by default; no mandatory streaks, red overdue wall or productivity score | Show the full backlog deliberately; optional timers |
| Understand state | Short labels, text alongside color, consistent links and keyboard navigation | Adjust density; use any compatible editor |

The inbox is idea capture, not another work queue. Accepted work is linked to
one existing or new Bead through the authorized coordinator. The captured note
then points to that authority; it does not keep a parallel task status.

## Proposed setup

1. Create a dedicated planning checkout/worktree through the selected adapter.
   The human edits there; active worker worktrees keep their assigned owners.
   Worktree separation prevents accidental file collisions, not unauthorized
   access by itself. The planning checkout has its own branch; a human edit
   becomes canonical only through the normal reviewed merge. Do not write the
   same branch from a parallel session or overwrite a renderer's output.
2. Ship templates for an authored `ROADMAP.md`, human-owned
   `docs/planning/inbox/`, and generated `docs/planning/HOME.md`. These are
   proposed paths, not files created by this research PR. Read decisions and
   resume information from their canonical change artifacts and handovers.
3. Let the authorized coordinator render a bounded Beads snapshot under its
   ownership protocol. The UI never opens the Dolt store or invokes live
   tracker writes. Until such a renderer exists, show a dated static snapshot
   and links; the session-end JSONL export is not a real-time feed.
4. For Obsidian, open the planning checkout as the vault, bookmark HOME and
   begin with core Properties/Templates/Bookmarks. Bases is optional for
   **human-owned** idea metadata. Use normal Markdown links for new content.
   Exclude tracker internals, worker trees, dependencies and execution logs
   from navigation. UI exclusions are not access controls.
   A plain-editor setup needs only `ROADMAP.md`, `docs/planning/HOME.md`, and
   dated `docs/planning/inbox/<date>-<short-title>.md` notes. Keep HOME's
   generated region separate from any human notes; if the renderer is absent,
   write a dated static HOME with links and an explicit stale status.
5. Keep reusable client settings optional and reviewed. Ignore volatile
   workspace files and personal settings; do not vendor plugin binaries or
   credentials. Do not run automatic Git push plugins in the initial trial.
6. Use the reviewed Git workflow to publish canonical planning changes. Never
   synchronize a live `.git`, `.beads` or worker directory through a general
   file-sync service. Optional mobile capture starts as a separate inbox;
   mobile approvals need the same identity/revision binding as desktop ones.
7. Define metadata ownership before views: document approval status,
   roadmap theme and Beads task status have different meanings. The view
   references them; it must not repurpose a `status` property across them.

## Acceptance before routine use

With the maintainer, trial: start the next action; capture an unrelated idea;
return after interruption; identify a blocker; decide from a concise request;
and recover when the tracker snapshot is stale. Repeat with the client closed
using only Markdown. Record confusion, missing context and unnecessary steps.
Optional timing evaluates the interface, not personal productivity. Tune the
visible work limit and notifications from that feedback.

The portable kit contains templates, a projection schema/renderer and its
freshness/integrity checks. Obsidian/Foam settings are optional adapter
examples. Removing them must leave core verification, planning files and the
single Beads authority intact.
