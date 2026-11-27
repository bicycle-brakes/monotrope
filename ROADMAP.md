# Roadmap

What Monotrope (`coding-harness`) works on now, next and later. Themes, not
tasks: task status stays in Beads (`tools/bd ready`). At most three themes are
**Now**.

**A trial** (maintainer, 2026-10-05; research note
`docs/research/2026-10-05-likec4-roadmap-arc42.md`, part B). Every handover
checks whether Now is still true. This file becomes a kit template only after
it stays true through two handovers; if a handover finds it stale twice, it is
removed.

Last checked: `2026-11-26`, `origin/main` at `b3391f6d`.

## Now

1. **Security boundaries and ramp-valve enforcers.** With the `2026-11-30`
   valves re-dated to `2026-12-31` (`coding-harness-5ane.1`, PR #463) and
   DeepSeek's terms re-read (`coding-harness-hw7w`), deliver the six
   enforcer tests (`coding-harness-5ane.20`–`5ane.25`) and harden the local
   and runner trust boundaries surfaced by the `2026-11-24` audit
   (`coding-harness-5ane.2`–`5ane.6`, `coding-harness-s9r`).
2. **State-first machine state, single kit manifest, and shared primitives.**
   Move mutable loop, lane, job, and attempt state onto locked JSON/JSONL with
   rendered Markdown views (`coding-harness-5ane.11`, aligned with
   `coding-harness-oebl`), unify the kit and export manifests while driving
   `DECKEL` from 44 to 0 (`coding-harness-5ane.7`, `coding-harness-5ane.10`),
   and consolidate YAML, atomic-write, and git primitives
   (`coding-harness-5ane.12`).
3. **Verification speed, runner modularization, and harness-neutral lanes.**
   Split `scripts/stage2.py` and `tests/test_stage2.py` to unlock targeted
   verification (`coding-harness-vg9`), prune accumulated worktrees
   (`coding-harness-bxxt.4`), and advance harness-neutral detached job and lane
   orchestration (`coding-harness-a6ns`, `coding-harness-bxxt`).

## Next

- **Unified model registry and route resilience:** Consolidate phase-to-model
  declarations into one registry (`coding-harness-wq1m`) and ensure fallback
  coverage when individual providers are unavailable.
- **Repository in English:** Translate remaining German identifiers, messages,
  and governance texts in dedicated pull requests (`coding-harness-yim`).
- **Missing standard entry files and gate hygiene:** Add `SECURITY.md` and
  `CONTRIBUTING.md` (`coding-harness-5ane.15`), enforce ADR claims on
  `architectural` changes (`coding-harness-5ane.8`, reconciled with
  `coding-harness-6slq`), and align CI/local `interview-minimums` history
  declarations (`coding-harness-5ane.9`).

## Later

- **Runner containment and sandboxing:** Evaluate OS-level/container isolation
  around foreign model and test runs (`coding-harness-nevd`).
- **Empirical evals and telemetry:** Build standing pass^k / defect-detection
  evals and structured cycle-time reports over the JSONL event log
  (`coding-harness-phcy`, `coding-harness-zaqf`).
- **External multi-stack transfer:** Apply the unified central-config and
  state-first kit cleanly to upcoming TypeScript, Rust, SQL, and PySpark
  projects.
