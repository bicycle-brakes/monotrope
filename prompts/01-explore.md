# Phase 1 · Explore

**Model:** GLM 5.3 Flash — much input, little output, no deep reasoning needed;
through `python3 scripts/stage2.py explore <change>` and its leak check
(`docs/WORKFLOW.md` §4). When Stage 2 is off or Z.ai is unavailable, rerun as
`python3 scripts/stage2.py explore <change> --stage2-off [REASON]`; Haiku 5.5
explores and the reason is recorded. A leak-check BLOCK stops; it never falls
back.
**Result:** `plans/changes/<name>/research.md`
**Gate:** `research-handoff` (a complete swarm run is blocked until the research questions and neighbours are answered; see below).

**Routing by class (ADR 0020).** A `feature` or `architectural` change
explores through the research swarm; a `bounded` change or a `spike` through
the single GLM 5.3 Flash explorer. The runner reads the class wherever stated:
the explore-only `--class` argument and the headers of `research.md` and
`spec.md`. All available declarations must agree; missing, invalid or
disagreeing declarations refuse before any model call. `--stage2-off [REASON]`
keeps the Haiku 5.5 route and skips the class.

**The swarm in one pass.** A finder trio (three seats, the same input) lists
where things are: files and functions, applicable rules and ADRs, tests and
gates, neighbouring specs. An Opus map merge keeps the exact union of those
lists. Then eleven topics follow: the repository seats work eight (1-8) on that
map and the online seats three public ones (9-11), each model on the same brief
and the same perspectives; a fresh Opus 5.5 context judges. The online topics see one
filtered public sentence and no repository content. That makes at most
`39 + 3N` calls for `N` selected free models; the free models work the online
topics only and are best-effort. The judge holds evidence authority only: it
exposes support, dissent, gaps and human questions, and decides no design and
no workflow question. Only the runner writes `research.md`.

**Required header: `neighbours:`.** The header of `research.md` carries a
`neighbours:` list of the neighbouring specs you already know (paths to a
`spec.md` of an active change, an archived change or a living spec). An empty
list is stated as `neighbours: []`; a missing header refuses the swarm. The
runner adds the neighbours the finders suggest; topic 5 reports on both kinds.

**Steps, in this order, in the main conversation.**

1. `python3 scripts/stage2.py prepare-explore <change> [--class CLASS]` refreshes
   the Go model catalog, probes reachability, fills the six seats (a substitute
   is named as such) and prints the selection report with a receipt id.
2. Show that report to the maintainer unchanged. The receipt is single-use and
   expires.
3. `python3 scripts/stage2.py explore <change> --availability-reported <id>`
   consumes the receipt and runs the swarm.

If a run is cut off (a quota or token limit, a kill), start steps 1 to 3 again:
the runner resumes — a finished contribution with the same inputs and prompt is
reused, only the missing ones are called again. Do not edit tracked files
between the runs. Only a complete run feeds phase 1a and phase 2; the gate
`research-handoff` checks that the research questions and neighbours reached
the interview and the spec (`docs/WORKFLOW.md`).

You collect facts about what exists today. You design nothing, you recommend
nothing, you judge nothing.

Before writing anything: `rg` through `plans/specs/` and `plans/changes/` for the
topic. If a matching artefact exists, it is updated rather than created again.

**Every statement names where it came from** — file and symbol, never a line
number alone; line numbers age within the hour. What you have not read is
written down as an open question, not as a guess. "Not found" and "not there"
are two different statements and are written as two.

Structure of `research.md`: what exists today · where it lives · what is unclear
about it · which files a change would have to touch.
