<!--
Kit template: a section for the AGENTS.md of a repository that adopts this
workflow. Copy it into that file and fill the placeholders. It is the
portable form of the working-pace rules in this repository's
docs/WORKFLOW.md (maintainer, 2026-10-26 and 2026-10-27).
-->

## Working pace

- **One entry point and one writer per action — no side routes.** Every
  recurring action has one entry point and one writer, carried by code at
  one choke point. Decided variants (fallback models, routing by class) are
  declared parameters inside it, never a second route; no caller reaches
  around it and nothing a tool produces is written by hand. An existing
  side route becomes a tracked item, folded in by its own change; the rule
  holds through a check that goes red (maintainer, 2026-11-16).
- **One decision block a day.** Questions and merge requests for the
  maintainer are collected for one block at `<time, default 15:00>` local
  time, each with its context and a recommendation; work that does not
  depend on the answer goes on meanwhile. A security question, a leak-check
  block or a stop that blocks every lane is asked at once.
- **Lanes stay busy.** By day up to `<number, default 3>` foreign-model calls
  run at once from a visible queue; when a lane frees, the next item starts.
- **The second finding of one mechanism ends case-by-case repair.** When a
  re-check finds a further case of a mechanism a repair already addressed,
  the agent proposes a structural remedy — one choke point every path goes
  through, a fail-closed rule, or a tracked structural item — with the
  rounds so far, and the maintainer chooses. By day the session stops and
  asks.
- **Night runs.** A night run works its queue alone, in at most two lanes
  that change disjoint files. When the primary reviewer or repairer is at
  capacity it waits `<minutes, default 4>` minutes and retries once, then
  hands that one step to the fallback model with a note and continues. A
  further case of the same mechanism at a re-check is recorded, its pull
  request parked, and the run continues; the maintainer decides in the
  morning.
