---
title: "Findings — rb-m6-one-account"
category: findings
created: 2026-10-06
updated: 2026-10-06
status: draft
implementation_status: partial
date: 2026-10-06
last_reviewed: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, governance, ruleset, ramp-valves, decision-pr]
---

# Findings — rb-m6-one-account

Phase 6, round 1, on commit `b5f8631` (branch `decide/rb-m6-one-account`,
eight commits over `origin/main` at `d5813ec`), 2026-10-06. The reviewer ran
on Opus 5.5 in a fresh context, wrote nothing but this file and the
regenerated `plans/INDEX.md`, opened no pull request, wrote nothing to the
tracker, recorded no ADR answer and changed nothing at GitHub: every call to
GitHub was a `gh api` GET, through the real `gh` or through a shim in the
session's scratchpad that refuses anything but `gh api <path>`. Measured
against `spec.md` (criteria 1–12, the non-goals and the `[DETAIL]`s) and
`decisions.md` (the maintainer's answer of 2026-10-05); `plan.md` was read
for its deviations, its planted faults and its evidence, not as the
yardstick. `templates/findings.md` does not exist on `origin/main`; the
columns are those of `plans/changes/research-currency/findings.md`.

**Verdict: two BLOCKER, both `[DIVERGENT]`; five MINOR; no `[AMBIGUITY]`.**
The code does what the spec asks, and every criterion that a test can hold
is held. Both blockers are places that now say the opposite of what the
change makes true — that hosted CI runs what `make verify` runs (F-1), and
that RB-M6 at level 4 blocks the merge in CI (F-2). F-1 is two comment lines
and one list marker; F-2 is the maintainer's call, since the rule set is
`human-decided`. The five MINOR are a weakening of the ruleset the check
does not see (F-3), a check that can measure another repository (F-4), a
gate tie that holds only the prefix of the command (F-5), the detection
deviation D1 gave up (F-6), and a test that cannot fail for the hint it
asserts (F-7). The ADR answer is still missing, so `make verify` is red on
`adr-answers`, as `decisions.md` expects; it is no row here.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `docs/WORKFLOW.md` lines 338–339; `prompts/05-verify.md` lines 9–10; `scripts/ci_gates.py --list` (`make gates`) | `[DIVERGENT]` Three places say that hosted CI runs what `make verify` runs, and this change makes that false for the first time. `docs/WORKFLOW.md` and `prompts/05-verify.md` both annotate `make verify` as "every locally runnable gate — the same the CI runs" and `make gates` as "what the CI runs"; `make gates` (measured on `b5f8631`) lists `[ruleset]` as an ordinary gate, while it marks the hosted-only `lychee` with "laeuft nur in der CI". Against that, `decisions/gates.yaml` gives `ruleset` `placement: writer`, `ci.yml` has no such step (byte-identical to `origin/main`, measured), and the 4.0.0 entry of the rule set says "misst `make verify` auf der Maschine des Maintainers, nicht die gehostete CI". The case it breaks: a reader who sees `ruleset` red in a local run — offline, say — is told CI runs the same and expects the pull request's check to go red too, or trusts hosted CI to notice a weakened ruleset when the maintainer works from another machine; neither happens. Before this change no gate was `writer`, so the local set was a subset of the hosted one and the sentences held loosely. What should hold: the two annotations and the list say that a `writer` gate runs in `make verify` only. The plan's "Not touched: `scripts/ci_gates.py` … a `writer` gate needs no generator change" missed the list, as it missed `tests/test_ci.py` (D1). [criterion 11, "the workflow text stays true"] | fixed in `8524800` — reviewed at `b9ee999`, closed: both annotations now say the CI runs what `make verify` runs "minus a `writer` gate (here only)" and that `make gates` marks such a gate; `make gates` on `b9ee999` prints "— laeuft nur lokal (make verify), nicht in der CI" on `[ruleset]` and on no other gate, in agreement with the gate's `reason` and the 4.0.0 entry. `tests/test_ci.py::test_the_list_marks_a_writer_gate_as_local_only` holds the mark; replayed, R1-1 to R1-5 each turn it red. See "Phase 6, round 2" |
| F-2 | BLOCKER | SPEC | base | `docs/governance/regelwerk.md`, §3 "Die Leiter" row 4, the RB-M6 row (Stufe 4) and the 4.0.0 entry, line `Tests:` | `[DIVERGENT]` The rule set answers "does a broken RB-M6 fail the CI run?" both ways. §3 defines level 4 as "CI blockierend — der Lauf schlägt fehl (BLOCK); ohne Fix kein Merge", and RB-M6 now stands at 4; the same document's 4.0.0 entry says the ruleset is measured by `make verify` on the maintainer's machine, "nicht die gehostete CI". The case: the maintainer removes the `deletion` rule in the web interface on a Monday; on Tuesday an agent's pull request passes the hosted `verify` check (the `ruleset` gate is not in it) and is merged on GitHub without a local `make verify` in between — nothing blocks, although level 4 promises "ohne Fix kein Merge". The spec chose level 4 as a `[DETAIL]` ("the gate blocks the run that phase 4 requires to be green"), reading "der Lauf" as the local run; §3's heading says CI, and no rung of the ladder describes a gate that blocks only on a writer machine. Before this change no level-4 rule rested on a writer-only gate. The rule set is `human-decided`, so which answer stands — level 4 with §3 amended to cover a blocking writer-machine gate, another level, or the divergence rejected with a reason — is the maintainer's, in this decision pull request. [criteria 2 and 3] | decided 2026-10-06 (level 4, ladder amended) — fixed in `a9f55a8`, reviewed at `c69015c`, closed: §3 row 4 and the RB-M6 row now say that a `placement: writer` gate blocks only the run on the maintainer's machine and that a merge on GitHub without that run is not stopped — the maintainer's choice in `decisions.md` (addendum 2026-10-06, answer 2), nothing beyond it; the 4.0.0 entry's `Geändert:` line names §3; `version:` stays 4.0.0. See "Phase 6, round 3"; what the fix left in `spec.md` is F-9 |
| F-3 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `_lists_required_check`; the RB-M6 row, "(der Job, der die Gate-Liste fährt)" | The check accepts a `verify` check from any source, so a ruleset that unpins it stays green. Today's ruleset (read 2026-10-06, `gh api repos/MPAdesso/coding-harness/rulesets/24528176`) requires `{"context": "verify", "integration_id": 15368}` — the check must come from GitHub Actions, the job that runs the gate list, as the amended row says in its parenthesis. Replayed end to end through the shim on `b5f8631`: the same answer with `integration_id` removed — the live test passes. Under one account that is the weakening that matters: unpinned, a commit status `verify: success` posted with the maintainer's token — which every agent holds — satisfies the rule without the job ever running (GitHub's documented meaning of `integration_id`; not measured, it would write). The spec's definition (b) asks for the context only, so the code meets the spec; the maintainer's words were "exactly today's ruleset", and the row promises the job. What should hold: an unpinned `verify` entry is a finding, or the row drops the parenthesis. [criterion 5, spec term (b)] | fixed in `8f9b11e`, reviewed at `c69015c`, closed in the code: an unpinned or other-app `verify` is the finding "not pinned to GitHub Actions"; R2-1, R2-3, R2-5 and E2-2 replayed red. What the pin does to the spec and to LakeSwitch is F-8 |
| F-4 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `measure` and `gh_api` (`repos/{owner}/{repo}`) | The check never asserts which repository it measured. `gh` fills `{owner}/{repo}` from `GH_REPO` when that variable is set, else from the repository's default (`gh repo set-default`), else from the remote. Measured on 2026-10-06 on `b5f8631`: `GH_REPO=MPAdesso/lakeswitch-ai` with the variable `RULESET_ASSERT=1` makes the live test pass against lakeswitch-ai's ruleset 22305982, which happens to hold the five; `gh api 'repos/{owner}/{repo}' --jq .full_name` answers `MPAdesso/lakeswitch-ai` there and `MPAdesso/coding-harness` without it. The case: a shell or an agent harness that exports `GH_REPO` for other work, or an instance cloned as a fork whose default points to its upstream (reasoned, not measured), gets a green gate for a repository other than the one it guards. What should hold: the measured `full_name` is compared with the repository the gate runs in, and a mismatch is `not measured`. [criterion 7, "reads the default branch, its active rules and each supplying ruleset"] | fixed in `fba000d`, reviewed at `c69015c`, closed: `measure` compares `full_name` with the checkout's `origin` before it reads any rule; E2-1 (`GH_REPO=MPAdesso/lakeswitch-ai`) replayed red with the cause named, R2-6 and R2-8 red; D9's reds fail closed and name the cause |
| F-5 | MINOR | SPEC | base | `tests/test_repo_settings.py`, `_gate_findings` (`startswith(prefix)`) | The test that ties the gate to the live check holds only the start of the command, so a suffix can switch the live check off with every test green. Planted on `b5f8631`: the gate command becomes `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs -k "not master"` — `tests/test_repo_settings.py`, `tests/test_ci.py` and `tests/test_gate_machinery.py` pass, `--check-schema` and `--check-ci` pass, and the gate itself runs green with "38 passed, 1 deselected": nothing reads GitHub. A deselection is not a skip, so `-rs` prints nothing about it. Deleting the gate or dropping the variable is caught (planted faults F14, F15, F19); this is the pre-mortem's "the gate got switched off" by a quieter route. What should hold: the tie fails for any command that does not run `test_master_has_a_ruleset_with_required_checks`. [criterion 8, "a test holds the command to the variable the test file reads"] | fixed in `8078d0e` and `21251a2`, reviewed at `c69015c`, closed: the tie asks a pytest started with the gate's arguments and variables whether the live test runs; E2-3 (`-k "not master"`) replayed red on `test_the_ruleset_gate_turns_the_live_check_on` alone, R2-12 to R2-15 and R2-17 red; cost measured in round 3 |
| F-6 | MINOR | MAINT | base | `tests/test_ci.py`, `test_every_gate_step_runs_even_after_a_failing_gate` (deviation D1, commit `ba7d17f`) | D1 gives up one detection the old count had by accident: a gate that moves to `writer` now leaves hosted CI with no test red, floor gates included. Planted on `b5f8631`: the floor gate `pytest` set to `placement: writer` and `ci.yml` regenerated — `tests/test_ci.py`, `tests/test_gate_machinery.py`, `--check-schema` and `--check-ci` all pass, and the hosted run would no longer run the test suite. On `origin/main` the same edit turns this test red (17 steps for 18 gates). The verdict on D1 itself: not a weakening of what the test guards — every hosted gate step still needs `if: ${{ !cancelled() }}`, the count still proves the test saw every hosted gate, and D1 reverted is red (planted fault F28, replayed); the old count contradicted the schema, which has allowed `writer` since bead 1jg.2, and would have made any `writer` gate impossible. MINOR, not MAJOR: the move takes two deliberate edits that both show in the diff (`decisions/gates.yaml` and the regenerated `ci.yml`), and no gate but `ruleset` is `writer` today. What should hold: which gates may be `writer` — at least never a `floor: true` gate — is held by a test of its own. [criterion 10, "no ratchet grows"; plan, D1] | fixed in `f010de1` and `bd1904d`, reviewed at `c69015c`, closed: R2-18 (the floor gate `pytest` moved to `writer`, `ci.yml` regenerated) replayed red on `test_only_the_named_gates_are_writer_only` alone with `--check-schema` and `--check-ci` green; R2-21 and R2-22 red; D8's naming is honest (round 3) |
| F-7 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `test_the_live_check_goes_red_without_gh_when_the_gate_turns_it_on` (deviation D6) | The test asserts the hint "needs network and a `gh` login" in the output, but pytest prints the hint's source line in every traceback, so the assertion holds without the hint. Planted on `b5f8631`: the condition that appends the hint becomes `if False and any(...)` — the three live-check tests pass, and the failure message no longer carries the hint (measured: the `E` lines show only `not measured: … exit 127: gh is not installed`; the hint text appears once, as source, line 19 of the output). The hint itself works today (measured with the shim's exit 1: the `E` lines read the finding and then "The gate `ruleset` needs network and a `gh` login on this machine; not measured is red, never green (RB-M6)."). What should hold: the test reads the assertion message — an `E` line, or `--tb=line` — not the whole output. [plan, D6] | fixed in `d2f27f8`, reviewed at `c69015c`, closed: the test reads the `E` lines; R2-24 replayed red, and so is a variant that prints the hint instead of putting it in the assertion message |
| F-8 | BLOCKER | SPEC | fix-r2 | `spec.md`, term (b) and criterion 5; `docs/governance/regelwerk.md`, 4.0.0 entry, line `lakeswitch-ai:`; `tests/test_repo_settings.py`, `_lists_required_check` (commit `8f9b11e`, deviation D7) | `[DIVERGENT]` Since `8f9b11e` the check answers "does a required `verify` without the GitHub Actions pin meet RB-M6?" with no; two places of this change still answer yes. Spec term (b) defines the requirement as "an entry with `context: verify`", and the 4.0.0 entry says LakeSwitch has nothing to pull through because its ruleset "fordert bereits … `verify`". Measured on 2026-10-06 through the read-only shim: LakeSwitch's ruleset 22305982 requires `[{"context": "verify"}, {"context": "floor"}]` with no `integration_id`, and `measure` of `c69015c` on it returns exactly one finding, "required check verify is not pinned to GitHub Actions (integration_id 15368)" — the ruleset the check before the pin passed (F-4's measurement). The case: LakeSwitch adopts `tests/test_repo_settings.py` (the kit carries it as `mechanismus`, and RB-M6 applies in P L I), and its gate is red on a ruleset the rule set says needs nothing. So D7 is not only a tightening of a spec term: it changes the verdict on a sibling repository's live ruleset and the history entry the decision pull request asks the maintainer to confirm. The choice is the maintainer's — the rule set is `human-decided` and the change lands in LakeSwitch. Either the pin stands (recommended: the RB-M6 row promises "der Job, der die Gate-Liste fährt", research 1.4 records today's ruleset with the pin, and the unpinned hole is the one F-3 named): then spec term (b) and criterion 5 name `integration_id` 15368, and the 4.0.0 `lakeswitch-ai:` line says that LakeSwitch's `verify` must be pinned to GitHub Actions, a change at GitHub that the maintainer makes. Or the pin goes: `8f9b11e` is reverted and F-3 stays a named limit. No code change in the first case. [spec term (b), criteria 1 and 5; plan, D7] | decided 2026-10-06 (maintainer) — fixed in `938ebd8`, not reviewed |
| F-9 | BLOCKER | SPEC | fix-r2 | `spec.md`, criterion 3; `docs/governance/regelwerk.md`, §3 row 4 and the heading `### 4.0.0 — 2026-10-05` (commit `a9f55a8`) | `[DIVERGENT]` The spec and the maintainer's decision of 2026-10-06 answer "may this change edit the rule set beyond the RB-M6 row, the two header keys and the new entry?" oppositely. Criterion 3 says no and names its own refutation — "a diff of the rule set outside the RB-M6 row, the two header keys and the new entry" — and ties the entry's heading to the day in `updated:`. Since `a9f55a8`, `git diff origin/main...HEAD -- docs/governance/regelwerk.md` changes §3 row 4 as well, as `decisions.md` (addendum 2026-10-06, answer 2) asks, and `updated:` reads 2026-10-06 while the heading still reads 2026-10-05; for 3.0.0 both were the same day. The case: whoever holds the change against criterion 3 — the next review, or the maintainer before the merge — finds it refuted twice by the very change it describes. Nothing in the rule-set text is wrong in substance; `spec.md` was not revised after the maintainer's answer. What should hold: criterion 3 admits §3 row 4 under the decision of 2026-10-06, and the entry's heading carries the day of its last edit, 2026-10-06, as `updated:` does. No code change. [criterion 3] | decided 2026-10-06 (maintainer) — fixed in `938ebd8`, not reviewed |
| 2a-1 | — | SPEC | base | `decisions.md` (the maintainer's words); `spec.md`, `[DETAIL]` "The five are a floor" | *Where does the spec admit two plausible readings?* The maintainer said "pull request required, required check verify, no force push, no deletion, no bypass — exactly today's ruleset". The spec reads the five as a floor (a stricter ruleset holds) and says why: turning red on a stricter one would punish the upgrade the decision expects. The other reading — today's ruleset exactly, the `integration_id` pin included — is plausible; its one consequence that matters is F-3. Not an `[AMBIGUITY]`: the spec decides it in the open, reversibly, and the decision pull request lets the maintainer confirm it — provided its decision block says "a floor, not an exact match" in so many words. | answered |
| 2a-2 | — | SPEC | base | `plan.md`, "Not touched" and "Deviations" | *What is missing that would have to be decided while building?* The plan held that a `writer` gate needs no change outside the new files; the build met two places that assumed no `writer` gate exists — `tests/test_ci.py` (D1, recorded) and `ci_gates.py --list` with the two annotations (F-1, not recorded). Everything else the build met is written down in D2–D6. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 1, 11 and 12 | *Which acceptance criterion cannot go red?* Criteria 1 and 11 are prose, read here (F-1, F-3). Criterion 12 is one measurement and waits on the ADR answer. Criterion 7's "at the commit of this change, it passes" is one measurement, re-measured here green. Every other criterion has a test that a planted fault turns red, except the holes F-5 and F-7. | answered |

Reviewer session: none — no phase 2a ran for this change (`spec.md` names
none, and `decisions.md` records phase 1a as skipped); this review ran in a
fresh session.

## Checked without a finding

- **The amended RB-M6 row (criterion 1).** It names the five requirements,
  the return trigger ("sobald eine zweite Identität existiert, etwa eine
  GitHub App") and keeps "Eine unerreichbare Verwaltungs-Schnittstelle ist
  BLOCK, nicht grün"; code-owner review and the last-pusher approval appear
  only as what returns. Nothing in it goes beyond the maintainer's words but
  the parenthesis on `verify`, which is F-3. No other row of the rule set
  changed (`git diff origin/main...HEAD -- docs/governance/regelwerk.md`:
  the row, `version:`, `updated:` and the new entry only).
- **The precedent of pull request #55 (criterion 3).** Merge `e490772`
  changed `version:` 2.0.0 → 3.0.0, `updated:`, one row and added the entry
  above the previous one, leaving `last_reviewed:` and `review:` alone; this
  change does the same with 3.0.0 → 4.0.0. MAJOR follows §4's semver ("ihre
  Bedeutung geändert"). The entry has the prose, the MAJOR sentence and the
  four mandatory lines; it names the decision of 2026-10-05, the closed
  valve, the writer-machine measurement and LakeSwitch. Its LakeSwitch line
  was re-read on 2026-10-06: ruleset 22305982 "lakeswitch floor" on
  `MPAdesso/lakeswitch-ai` supplies `pull_request`, `required_status_checks`
  (`verify`, `floor`), `non_fast_forward` and `deletion` with an empty
  bypass list.
- **The live check against the real ruleset (criteria 4, 7).** Read on
  2026-10-06: ruleset 24528176, `enforcement: active`, target
  `~DEFAULT_BRANCH`, the four rule types, `bypass_actors: []`,
  `current_user_can_bypass: never`; the branch-rules answer carries the same
  four with `ruleset_id` 24528176. The stubs copy exactly the keys the code
  reads. Through the shim passing everything through, the live test passes
  with three calls (repository, branch rules, ruleset); without
  `RULESET_ASSERT` it is skipped, names the gate `ruleset`, and calls `gh`
  zero times.
- **"Unreachable is BLOCK, not green" (criterion 6).** Measured end to end:
  `gh` exit 1, `gh` not on `PATH`, an empty answer with exit 0, and a
  supplying ruleset that answers 404 each fail the live test with one
  `not measured:` finding naming the step; the gate is `enforcement: block`.
- **Agents and hosted CI.** `.github/workflows/ci.yml` is byte-identical to
  `origin/main` and `--check-ci` is green, so the pull request's `verify`
  check and the floor gate `pytest` there are unaffected: the live test is
  skipped without the variable, and the two tests that run it in a
  subprocess put an empty or fake `gh` on `PATH`. An agent's `make verify`
  without network or login is red on the one gate `ruleset`, and the
  failure reads the cause and the way out (F-7 is only about the test of
  that line). `prompts/05-verify.md` already tells an agent that "a red run
  is reported, not worked around". That only the maintainer's machine
  measures is stated in the gate's `reason`, the module docstring and the
  4.0.0 entry; F-1 is where it is contradicted.
- **The valves (criteria 9, 10).** `ruleset-assert` is gone from
  `REGEL_VENTILE`, a comment stands in its place, and no valve names RB-M6;
  `ramp_valves.py --format=json` lists 26 valves, none due. With the date
  forced: on 2026-10-30 none is due, on 2026-10-31 exactly
  `merge-freshness` (RB-G7, bead coding-harness-34z), which this change does
  not touch (its entry is unchanged in the diff). `commit-identity` and
  `codeowners-here` stay closed because they wait for functions, not for
  the file, and the file defines neither.
- **Kit and ratchets (criterion 10).** `tests/test_repo_settings.py` has the
  role `mechanismus`; `OHNE_MUTATIONSTEST`, `OHNE_AUFRUFER`, `OHNE_TEST`
  and `REIST_NICHT` are not in the diff. The gate's mutation evidence is in
  the file it runs (`*_goes_red_when_*`).
- **The workflow note (criterion 11).** The sentence is appended inside the
  quote paragraph, the dated list is unchanged, and `updated:` moved.
- **The suite (criterion 12, as far as it can be measured now).**
  `make verify` on `b5f8631`, 2026-10-06, commit signing off: `pytest` 638
  passed and 16 skipped; `ruleset` green ("39 passed"); every other block
  gate green except `adr-answers` ("rb-m6-one-account: no answer");
  `docs-links` and `markdownlint` red but report-only. The plan's records
  match. A first run of this review wrote its log under a name another
  session in the same scratchpad also used, and showed `d5813ec` numbers;
  the run quoted here wrote to a name of its own and reports candidate
  `b5f8631`, 19 gates.
- **Planted faults.** Thirteen of the plan's 41 replayed on `b5f8631`, each
  alone, the file restored with `git checkout` (the tree clean after each):
  F01 → 2 of the 4 hidden-bypass cases red; F04 →
  `…_goes_red_when_verify_is_not_required` red; F11 →
  `[rules-exit-1-with-a-valid-answer]` red; F12 →
  `…_goes_red_without_gh_when_the_gate_turns_it_on` red; F14 →
  `test_the_ruleset_gate_turns_the_live_check_on` red; F20 →
  `test_every_named_ramp_exists_and_no_valve_is_orphaned` red; F26 →
  `leerprobe` BLOCK (the RB-M6 enforcer among the red cases); F28 →
  `test_every_gate_step_runs_even_after_a_failing_gate` red; and end to end
  through the shim E01 (bypass actor), E03 (pull-request rule removed), E07
  (`verify` replaced by `lint`), E10 (`gh` exit 1) and E12 (`gh` not on
  `PATH`) → the live test red with the finding named. Every result as
  `plan.md` records it. Own variants: a bypass actor with
  `bypass_mode: pull_request` (red); an empty answer with exit 0 (red); a
  supplying ruleset that cannot be read (red); the `integration_id` removed
  (green — F-3); `GH_REPO` pointing at another repository (green — F-4); a
  `-k "not master"` suffix on the gate command (green — F-5); the floor
  gate `pytest` moved to `writer` (green — F-6); the D6 hint switched off
  (green — F-7).

## Not checked

No hosted run: there is no pull request yet, so the `verify` check on this
branch was not seen. What GitHub returns to a token without write access to
the ruleset (no `bypass_actors` key, research 1.6) was not measured — no
such token was used; the stub case holds the code's answer. Organisation
rulesets, a fork with `gh repo set-default` (F-4 reasons it) and a Claude
Code sandbox that blocks `api.github.com` were not tried. A commit status
posted by hand (F-3) was not tried, since it writes. The plan's other 28
planted faults were not re-run. `research.md` was read only where the spec
cites it.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. Phase 7 waits on three things:

1. **F-1** — a repair round: the two annotations and `make gates` say that
   a `writer` gate runs locally only.
2. **F-2** — the maintainer's decision on level 4 and §3, in this decision
   pull request; the rule set is `human-decided`, so no agent closes it.
3. **The ADR answer** — recorded with `scripts/harness.py decide adr` as
   the maintainer states it; until then `adr-answers` keeps `make verify`
   red.

F-3 to F-7 can be fixed in the same round or closed as named limits, the
maintainer's choice. The pull request is a decision pull request
(`decide(governance): …`, label `decision`), names bead coding-harness-bma
in its body (house rule 4), says in its decision block that the five are a
floor (2a-1), and says under "after the merge" that the valve
`merge-freshness` still falls due on 2026-10-31.

## Phase 6, round 2 (2026-10-06)

Repair round 1 read, on commit `b9ee999`, 2026-10-06, by a reviewer on
Opus 5.5 in a fresh context that wrote nothing but this file, opened no pull
request, wrote nothing to the tracker, called no external model and changed
nothing at GitHub. It read the repair diff `48f69e9..b9ee999` — the two
annotations, the list mark in `scripts/ci_gates.py`, the new test, the
`updated:` stamps and "Repair round 1" of `plan.md`, where the repair and its
planted faults are recorded — against row F-1 only. F-2 stays the
maintainer's decision; F-3 to F-7 were not re-read. Above this section only
the Status column of F-1 changed.

**Verdict: F-1 is closed; no new row, so nothing of origin `fix-r1`.** What
still stops phase 7 is F-2 and the missing ADR answer.

- **The three places are true now.** `make verify` runs the verify job's
  gates with `--placement lokal`, everything but `hosted`
  (`scripts/verify_all.sh`); the derived `ci.yml` holds everything but
  `writer` (`misst_in`, `generate_ci`). "The CI runs the same, minus a
  `writer` gate (here only)" names exactly that difference, and `make gates`
  now marks `[ruleset]`, the one `writer` gate, and no other line. The words
  agree with the gate's `reason` ("measures it on the writer machine") and
  the 4.0.0 entry ("misst `make verify` auf der Maschine des Maintainers,
  nicht die gehostete CI"). Searched on `b9ee999`: no other sentence in the
  tree says the CI and `make verify` run the same set. The nearest, the
  `verify_all.sh` entry of `OHNE_AUFRUFER` ("Die CI faehrt jedes Gate als
  eigenen Schritt"), says how the CI runs gates — one step each, not through
  the runner — not which.
- **Minimal.** Two comment lines in each of `docs/WORKFLOW.md` and
  `prompts/05-verify.md`, two lines in the `--list` branch of `main`, one test
  with its helper, the `updated:` stamps and the plan record. No generator,
  schema or runner change; `ci.yml` is untouched and `--check-ci` green.
- **Replays.** All five planted faults, R1-1 to R1-5, each alone on a clean
  export of `b9ee999` (`git archive`), `tests/test_ci.py` run, the file
  restored: each turns `test_the_list_marks_a_writer_gate_as_local_only`
  red, R1-4 at the synthetic `writer` gate as `plan.md` says. The export has
  no `.git` and no tracker, so four other tests of the file are red there
  with and without a fault (measured); they are not counted. Own variants:
  the mark keyed on `misst_in(g, "lokal")` (red); the mark moved from the
  command line to the gate's title line (red); `not misst_in(g, "ci")`
  (green, an equivalent rewrite, as it should be); `placement != "both"` and
  `placement == "writer" and not via_local_equivalent` (green — see below).
- **The suite.** `make verify` on `b9ee999`, 2026-10-06, commit signing
  off: `pytest` 639 passed and 16 skipped (one more than round 1, the new
  test); `ruleset` green ("39 passed"); every block gate green except
  `adr-answers` ("rb-m6-one-account: no answer"); `docs-links` and
  `markdownlint` red but report-only, as in round 1.

Seen, and no row:

- The two green variants differ from the code only on gates the file does
  not hold: a `hosted` gate with a command, and a `writer` gate run through
  an action's local equivalent. For the first, the list prints no mark at
  all — measured on `b9ee999` by moving `ruff-check` to `hosted` in a
  scratch copy; at `48f69e9` the list had no placement branch (read) —
  although `make verify` skips such a gate. That is F-1's shape for a gate
  that does not exist, older than this round.
- The longer annotations add three `MD013` line-length hits
  (`docs/WORKFLOW.md` lines 338 and 339, `prompts/05-verify.md` line 9: 103,
  93 and 102 characters, up from 68, 66 and 72). `markdownlint` is
  report-only by its reason.
- The new mark is German, like its neighbour "laeuft nur in der CI" and the
  rest of the `--list` output; house rule 1 translates that output in a pull
  request of its own (bead coding-harness-yim), not in passing.
- `prompts/05-verify.md` still says `make gates` reads "from ci.yml"; it
  reads `decisions/gates.yaml`, as `docs/WORKFLOW.md` says. The words were
  the same at `48f69e9`; the repair kept them.

Not checked: a hosted run (still no pull request); a planted revert of the
two annotations, since no test holds prose — criterion 11 is read.

For phase 7: F-1 no longer stops the pull request. Two things still do —
F-2, the maintainer's decision on level 4 and §3, and the ADR answer,
recorded as the maintainer states it.

## Phase 6, round 3 (2026-10-06)

The F-2 fix and repair round 2 read, on commit `c69015c`, 2026-10-06, by a
reviewer on Opus 5.5 in a fresh context that wrote nothing but this file,
opened no pull request, wrote nothing to the tracker, called no external model
and changed nothing at GitHub. Every call to GitHub was a `gh api <path>` GET —
through the real `gh` in the gate, otherwise through a shim in the session's
scratchpad that refuses anything else (`gh api -X DELETE …` measured refused).
It read `git diff b9ee999..9730444` (§3, the RB-M6 row, the 4.0.0 entry, the
ADR answer, the decisions addendum) and `git diff 9730444..c69015c` (rows F-3
to F-7, deviations D7–D10, the planted faults) against `spec.md` and
`decisions.md`. Above this section only the Status column of F-2 to F-7
changed, and rows F-8 and F-9 were added.

**Verdict: F-2 to F-7 are closed; two new BLOCKER rows, both `[DIVERGENT]`,
both of origin `fix-r2`: F-8 (the pin against spec term (b) and the
LakeSwitch line) and F-9 (criterion 3 against the §3 amendment). Round 2 is
the second consecutive repair round, so the two go to the maintainer, not to
a third round.** Neither needs a code change unless the maintainer drops the
pin. `docs/WORKFLOW.md` words the rule as "two consecutive rounds of `fix-r`
origin"; round 1 produced none, so read literally one more round would be
open — the dispatching session's rule, escalate now, is followed here.

- **F-2: the maintainer's choice, and nothing more.** §3 row 4 adds: a
  `placement: writer` gate blocks only the run on the maintainer's machine
  (`make verify`), a merge on GitHub without that run is not stopped, and the
  rule's row says so. The RB-M6 row adds: measured only on the maintainer's
  machine (gate `ruleset`, `placement: writer`), a merge on GitHub without a
  local `make verify` is not blocked. Both are answer 2 of the addendum;
  "die Regelzeile sagt das" is the general form §3 needs of "the RB-M6 row
  says so". No other ladder row and no other rule row changed. "The
  maintainer's machine" is the spec's term *writer machine*; an agent's
  `make verify` elsewhere is red on `not measured`, which blocks too, so
  "nur" is about where the gate measures, and that holds.
- **The version stays 4.0.0.** §4: "jede Änderung erhöht `version:`" — this
  change reaches `main` once, 3.0.0 → 4.0.0, with one entry that now names
  §3 in its `Geändert:` line. A further number for an amendment inside the
  unmerged pull request would name a version that never stood on `main`.
  The 1.1.0 lesson (an edit that left the version standing) concerns a
  merged edit, not this. The heading's day is F-9.
- **The ADR answer.** `decisions/answers/rb-m6-one-account/adr.yaml` records
  `answer: 'no'` with the reason of the recommended option the maintainer
  chose ("It applies ADR 0008 and the maintainer's decision of 2026-10-05;
  the one-account exception of RB-M2 (PR #55) set the precedent without an
  ADR."), as the addendum (answer 1) says; commit `d9e7648` carries "Stated
  by the maintainer in: Claude Code session 2026-10-06, interview: … — Nein
  (recommended option)". `adr-answers` is green.
- **D7: `[DIVERGENT]`, not an acceptable tightening.** Had the pin only made
  the check stricter than a spec term, aligning the term would be a detail.
  It also flips the verdict on LakeSwitch's live ruleset from green to red
  while the 4.0.0 entry says LakeSwitch needs nothing (measured, F-8). That
  is an answer the rule set gives to a sibling repository, so it is the
  maintainer's. Recommended: keep the pin; amend spec term (b) and
  criterion 5; rewrite the `lakeswitch-ai:` line.
- **F-4 and D9.** The comparison runs after the repository answer and before
  any rule is read (`calls == [REPO_PATH]`). Every red D9 names — a renamed
  repository, a `gh` default other than `origin`, a fork pointing at its
  upstream — fails closed with the cause in the message; so does an
  `origin` that is a local path (`local_repository` names it
  `mikypiky/coding-harness`, which matches nothing at GitHub; measured on a
  scratch repository).
- **F-5: robust, and what it costs.** The tie no longer reads words: it asks
  pytest itself, with the gate's own arguments and variables, which tests
  would run. `-k`, `-m`, `--deselect`, `PYTEST_ADDOPTS`, `--co` and an
  unknown option all fail closed. `--lf` reads as "does not run" because
  the probe turns the cache provider off, which also fails closed. Cost,
  three runs each on 2026-10-06: `tests/test_repo_settings.py` takes
  1.38–1.40 s at `9730444` and 3.52–3.64 s at `c69015c`. That is +2.1 s per
  run of the file, and `make verify` runs the file twice (the gates `pytest`
  and `ruleset`), so about +4 s per run rather than D10's two. Not a row.
- **F-6 and D8: honest.** Renamed back to
  `test_the_writer_only_list_goes_red_when_a_gate_moves`, the test turns
  `test_the_mutation_ratchet_only_turns_one_way` red with "long since
  covered, but still in the ratchet: ['plans-registry',
  'plans-registry-strict']". A `*_goes_red_*` name in `tests/test_ci.py`
  would count as mutation evidence for every script the file mentions,
  though nothing here mutates them. `…_flags_…` avoids a false claim of
  coverage and hides no real one. The schema knows `both`, `writer` and
  `hosted`, and only `writer` leaves hosted CI, so keying the list on
  `writer` misses no route.
- **Replays.** Fourteen of R2-1 to R2-26 were planted each alone in the
  worktree, the named file run and the file restored with `git checkout`
  (the tree was clean after each): R2-1, R2-3, R2-6, R2-8, R2-12, R2-13,
  R2-14, R2-15, R2-17, R2-18, R2-21, R2-22 and R2-24 red as `plan.md`
  records. R2-5 was planted in a form of my own (an unpinned `verify` builds
  no finding at all) and is red on the four `…not_pinned…` cases. The
  three end-to-end faults ran through the shim: E2-1 red ("it answers for
  'MPAdesso/lakeswitch-ai', but this checkout is of
  'MPAdesso/coding-harness'"), E2-2 red ("not pinned to GitHub Actions")
  and green without the distortion, E2-3 red on the tie alone with
  `--check-schema` and `--check-ci` green. Own variants:
  - the hint printed instead of put in the assertion message: red (F-7);
  - the pin only in a ruleset with a bypass and an unpinned `verify` in a
    clean one: "ruleset 7 lets RepositoryRole 5 bypass it" (F-3);
  - `GH_REPO` set inside the gate command: the tie is green, as it should
    be, and the live check is red on F-4's finding, so the two fixes
    compose;
  - the pinned check on LakeSwitch's live ruleset: "not pinned" (F-8).
- **The suite.** `make verify` on `c69015c`, 2026-10-06 15:26–15:27,
  commit signing off: `pytest` 688 passed and 16 skipped. `ruleset` is green
  ("82 passed") and read the real ruleset. Every block gate is green,
  `adr-answers` included, so criterion 12 holds as measured. `docs-links` and
  `markdownlint` are red but report-only, as before.

Seen, and no row:

- After F-4's mismatch, the live test's hint line still reads "needs network
  and a `gh` login"; the line above names the real cause (`GH_REPO` or the
  `gh` default). This is generic, not false.
- The chain check reads a newline as whitespace (`shlex`). A gate command
  whose second line is an executable `.py` path (`scripts/kit/probe.py`)
  keeps the tie green; measured with `decisions/gates.yaml` planted and
  restored. It cannot swallow the exit code: `ci_gates.py --commands --tsv`
  prints the second line as a line of its own, and the runner's `read` loop
  skips a line without a command, so the pytest part alone decides the gate.
- `GITHUB_ACTIONS_APP_ID` 15368 is the id on github.com. An instance on
  GitHub Enterprise Server would read red (reasoned, not measured); all
  three repositories named here are on github.com.

Not checked: a hosted run (still no pull request). A real `gh repo
set-default` was not tried, because it writes the shared git config. The
other twelve planted faults were not replayed. Portfolio's ruleset was not
read further: the rule set claims nothing about it in 4.0.0.

For phase 7: not ready. F-8 and F-9 are open BLOCKERs of origin `fix-r2`
and go to the maintainer, one question at a time — first F-8 (does RB-M6's
`verify` require the GitHub Actions pin?), then F-9 (`spec.md` criterion 3
and the 4.0.0 heading). Everything else holds: F-1 to F-7 closed, the ADR
answer recorded, `make verify` green on `c69015c`.
