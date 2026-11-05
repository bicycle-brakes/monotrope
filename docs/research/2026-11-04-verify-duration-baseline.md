---
title: "make verify baseline — five serial runs on bc2fe411, and a warning-budget proposal"
category: research
created: 2026-11-05
updated: 2026-11-05
last_reviewed: 2026-11-05
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-1um6
tags: [verify, duration, baseline, spike, measurement]
---

# make verify baseline

**Result: a full local `make verify` took 1,215–1,261 s of execution on one
clean revision (median 1,223 s, about 20.4 minutes; five green runs,
2026-11-05). The pytest gate is 81 % of it and the kit probe (`leerprobe`)
16 %; everything else together is under 3 %.** Waiting at the machine-wide
verify lock is a separate quantity and varied from 2 s to 1,254 s in the
same five runs. Proposal: warn when execution exceeds **1,400 s**.

## How it was measured

- Revision `bc2fe411` of branch `spike/verify-duration`, clean tree (`dirty:
  false` in every record), the instrumentation this change adds.
- Command, five times serially, through ordinary lock admission (no bypass):
  `PYTEST_ADDOPTS=--durations=30 PYTHON=.venv/bin/python3 make verify`.
- Same job (`verify`), placement (`local`), gate configuration
  (`config_sha256` prefix `afaec60c0743`) and worker setting (4 configured).
  The actually started worker count is not printed in the retained output —
  not read.
- Source: the run records in `~/.local/state/coding-harness/verify-duration.jsonl`
  (`run_start`, `gate`, `run_end` events) and each run's stdout for the
  30 slowest pytest durations. No foreign model call.
- Other lanes were running on the same machine (review loops, repairs); the
  lock admits one verification at a time, so no two full runs overlapped, but
  model calls and editors did. Free memory at admission: 55–67 %.

## The five runs

| Run | Admitted (UTC) | Execution s | pytest s | leerprobe s | Lock wait s | Free memory % | Workers |
|---|---|---|---|---|---|---|---|
| 765c156b | 2026-11-05T00:08:32Z | 1261 | 1031 | 194 | 960 | 61 | 4 |
| c695e555 | 2026-11-05T00:49:21Z | 1218 | 981 | 200 | 1188 | 55 | 4 |
| 0864a0f1 | 2026-11-05T01:30:34Z | 1215 | 984 | 195 | 1254 | 59 | 4 |
| 414ab592 | 2026-11-05T01:50:55Z | 1233 | 999 | 198 | 5 | 66 | 4 |
| 4d648f85 | 2026-11-05T02:11:30Z | 1223 | 991 | 196 | 2 | 67 | 4 |

All five ended green; none was excluded (no failed, incomplete or dirty run).
Range of execution: 46 s (3.8 % of the median).

## Where the time goes

Median seconds per gate over the five runs (20 gates):

| Gate | Median s | Range s | Share of median run |
|---|---|---|---|
| pytest | 991 | 981–1031 | 81 % |
| leerprobe (kit probe) | 196 | 194–200 | 16 % |
| markdownlint | 10 | 10–10 | 1 % |
| ruleset | 9 | 9–9 | 1 % |
| frontmatter-current | 6 | 6–6 | <1 % |
| the other 15 gates | ≤ 2 each | — | <1 % together |

Slowest single tests (call phase, median over the runs that listed them;
every one below appeared in all five unless noted):

| s | Test |
|---|---|
| 26.3 | `tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours` |
| 24.8 | `tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps` |
| 20.5 | `tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts` |
| 19.9 | `tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons` |
| 16.2 | `tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection` |
| 15.7 | `tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence` |
| 15.0 | `tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims` |
| 13.8 | `tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence` |
| 13.8 | `tests/test_stage2_swarm.py::test_a_foreign_edit_breaks_the_binding_and_reuses_nothing` |
| 13.6 | `tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map` |
| 13.5 | `tests/test_stage2_swarm.py::test_a_staged_run_whose_record_was_published_is_not_resurrected` |
| 13.5 (4 of 5) | `tests/test_stage2_swarm.py::test_only_the_runner_appends_research` |

Eleven of the twelve slowest tests are research-swarm tests. The first run's
pytest suite reported 4,710 passed and 17 skipped in 1,030.87 s.

## Warning-budget proposal

Warn when one run's **execution** (lock wait excluded) exceeds **1,400 s**:
the median 1,223 s plus about 15 %. The margin is four times the observed
spread (3.8 %), because these five runs come from one night on one machine
with other lanes active, and a quieter or busier machine was not measured.
The budget is a warning, not a timeout: this note makes no speed-up claim and
changes no timeout.

The lock wait needs its own reading: on this night it was up to 1,254 s
(about 21 minutes), as long as a run itself — the dominant cost for a lane
was queueing, not execution.

## Limits

- One night, one machine, one revision; five runs. Variance across machines,
  times of day and a quiet machine is not measured.
- Each gate reading includes the start of a small helper interpreter
  (`python -m scripts.verify_duration clock`), estimated at 0.1–0.3 s per
  reading (review-loop row L2-2, not measured here) — below the precision of
  the table.
- The started worker count is not printed in the retained output (not read);
  only the configured 4 is recorded.
