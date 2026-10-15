# Phase 1 · Explore

**Model:** GLM 5.3 Flash — much input, little output, no deep reasoning needed;
through `python3 scripts/stage2.py explore <change>` and its leak check
(`docs/WORKFLOW.md` §4). When Stage 2 is off or Z.ai is unavailable, rerun as
`python3 scripts/stage2.py explore <change> --stage2-off [REASON]`; Haiku 5.5
explores and the reason is recorded. A leak-check BLOCK stops; it never falls
back.
**Result:** `plans/changes/<name>/research.md`
**Gate:** none.

**Routing by class (ADR 0020).** A `feature` or `architectural` change explores
through the research swarm; a `bounded` change or a `spike` through the single
GLM 5.3 Flash explorer. The runner reads the class wherever stated in the
explore-only `--class` argument and the headers of `research.md` and `spec.md`.
All available declarations must agree; missing, invalid or disagreeing
declarations refuse before any model call. `--stage2-off [REASON]`
keeps the Haiku 5.5 route and skips the class. In the swarm, free researchers
see public sources only — one filtered topic sentence, no repository content;
the Flash pair compares the repository on six topics; a fresh Opus 5.5 context
reconciles the six pairs. The judge holds evidence authority only: it exposes
support, dissent, gaps and human questions, and decides no design and no
workflow question.

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
