# Phase 1 · Explore

**Model:** GLM 5.3 Flash — much input, little output, no deep reasoning needed;
through `python3 scripts/stage2.py explore <change>` and its leak check
(`docs/WORKFLOW.md` §4). When Stage 2 is off or Z.ai is unavailable, rerun as
`python3 scripts/stage2.py explore <change> --stage2-off [REASON]`; Haiku 4.5
explores and the reason is recorded. A leak-check BLOCK stops; it never falls
back.
**Result:** `plans/changes/<name>/research.md`
**Gate:** none.

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
