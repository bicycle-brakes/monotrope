# coding-harness

The home of the coding workflow: **seven phases, three stages**, the session
handover, the kit that carries the process into new repositories, and the
research corpus behind it.

- **Doctrine:** `docs/WORKFLOW.md` (migrating step by step from
  `portfolio-agentic-engineering`)
- **Tracker:** beads with the `coding-harness-` prefix, pinned via `tools/bd`,
  transported through `refs/dolt/data` on origin — `.beads/issues.jsonl` is a
  rendered export, not the source of truth
- **Status:** bootstrapping — see
  [`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`](docs/journal/handover/2026-09-16-coding-harness-bootstrap.md)
- **Current target (2026-09-17):**
  [Omnigent-first target](docs/architecture/2026-09-17-omnigent-first-target.md),
  [gap analysis](docs/architecture/2026-09-17-gap-analysis.md), and
  [implementation plan](docs/architecture/2026-09-17-implementation-plan.md)

## The three-repo topology

| Repo | Role |
|---|---|
| `coding-harness` (here) | process source of truth: doctrine, prompts, templates, kit, model routing, research |
| `portfolio-agentic-engineering` | framework governance (rule set, gates, ADRs, lessons), OSI→lakeswitch transfer logistics, domain content |
| `lakeswitch-ai` | product repo running a clean-room instance of the workflow |

## The workflow in one line

Explore → Interview → Spec → Spec-Review → Plan → Implement → Verify →
Review → Commit — every phase leaves a **file**, never a chat transcript;
between the files stand gates that are not negotiated with. The full doctrine
arrives with migration step 3.6.

## Quick start

```bash
git clone https://github.com/MPAdesso/coding-harness.git
cd coding-harness
tools/bd ready              # open, unblocked work
tools/bd prime              # full tracker context
```
