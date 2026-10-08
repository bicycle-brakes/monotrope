---
title: "Plan — rb-g7-merge-freshness"
status: draft
implementation_status: none
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-34z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, governance, ruleset, ramp-valves, decision-pr]
---

# Plan — rb-g7-merge-freshness

```text
For you:     a pull request merges only when its branch is up to date with main; you tick one ruleset checkbox by hand, and make verify on your machine goes red if it is ever unticked
Done when:   criteria 1–14 hold and make verify is green on your machine, after you answer the ADR question (proposed: no) and tick the checkbox
Appetite:    1.5 h of phase 4, one repair round included
Not now:     a merge queue or auto-update of branches; a ruleset check in hosted CI; MG-3's stale code-owner row
Pre-mortem:  suppose it failed: most likely because re-running CI on every open pull request after each merge felt like friction and the checkbox was unticked again
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–14; class `feature`, ADR question proposed
"no". Facts read at `eae78a3` (research addendum). Explore ran on Stage 2
(GLM 5.3 Flash), so there is no Stage-1 fallback to carry. The phase-2/3
validator the prompts name is not in this repository; `python3
scripts/plans_registry.py --check` holds the headers.

## Decided in phase 3

No `[DECISION]` is open.

- `[DETAIL]` **Names:** `_merge_ref_findings`, `PR_TRIGGER_FILTERS`,
  `_MOVES_THE_TREE` (tests/test_ci.py); `UP_TO_DATE`, `UP_TO_DATE_OPTION`,
  `_up_to_date_rules` (tests/test_repo_settings.py). The new names in
  `tests/test_ci.py` use `flags`, never a `MUTATIONS_NAMEN` token.
- `[DETAIL]` **Order:** steps 1, 3, 4 and 5 land in one commit — the valve
  falls due the moment the test exists, and `tests/test_regelwerk.py` needs
  the valve and its `Ramp:` gone together.
- `[DETAIL]` **Ask the maintainer to tick the checkbox before phase 4**
  (Phase 7 below): a stricter ruleset holds today's code, and phase 4's
  `make verify` is then red only on `adr-answers` until the ADR answer.

## Steps

0. **The ADR answer**, asked by the orchestrating session (proposed: no, the
   header's reason) and recorded only as stated: `python3 scripts/harness.py
   decide adr --change rb-g7-merge-freshness --answer <yes|no> --reason "…"
   --stated-in "…"`. A "yes" stops phase 4.

1. **`tests/test_ci.py`** (20 min). After
   `test_concurrency_group_carries_the_event`, a section `1a · The
   verification runs against the merge ref (RB-G7)` with a comment that its
   names avoid `MUTATIONS_NAMEN` (reason: research addendum). Then:
   - `PR_TRIGGER_FILTERS = ("branches", "branches-ignore", "paths",
     "paths-ignore", "types")`; `_MOVES_THE_TREE =
     re.compile(r"\bgit\s+(?:checkout|switch|reset)\b")`.
   - `_merge_ref_findings(doc: dict) -> list[str]`, docstring: on
     `pull_request`, `actions/checkout` without `ref:` checks out
     `refs/pull/<n>/merge` (RB-G7, MG-2); the ruleset's up-to-date
     requirement (`tests/test_repo_settings.py`) makes it the merge that
     happens. Trigger = `doc.get("on") or doc.get(True) or {}`. One finding
     each for: no `pull_request` key; a `pull_request` value that is a mapping
     with any key of `PR_TRIGGER_FILTERS`; a `pull_request_target` key; the
     job `ci_gates.MATRIX_JOB` whose `if` does not contain `pull_request`; no
     step with `uses` starting `actions/checkout@` among that job's steps
     before the first step whose `id` is a gate id (`{g["id"] for g in
     gates()}`); then, in every job, each checkout step whose `with` holds
     `ref` or `repository`, and each step whose `run` matches
     `_MOVES_THE_TREE`. A finding names job and step.
   - `test_the_verification_runs_against_the_merge_ref`: for
     `("ci.yml", CI_FILE.read_text(encoding="utf-8"))` and
     `("generate_ci()", ci_gates.generate_ci())`, `_merge_ref_findings(
     yaml.safe_load(text)) == []`, the source in the message.
   - `test_the_merge_ref_check_flags_a_planted_fault`, parametrized by id
     over the nine faults of criterion 2 (`head-sha-on-the-matrix-checkout`,
     `head-ref-on-the-drift-checkout`, `another-repository`,
     `no-pull-request-trigger`, `pull-request-target`, `branches-filter`,
     `matrix-job-off-pull-request`, `no-checkout`, `git-checkout-step`), each
     a function on a `copy.deepcopy(_ci_doc())`; asserts a non-empty result.
   - `test_the_merge_ref_check_flags_a_ref_the_generator_emits`: monkeypatch
     `ci_gates._checkout` to return `["      - uses: actions/checkout@v4",
     "        with:", "          ref: ${{ github.head_ref }}"]`; asserts a
     finding on `yaml.safe_load(ci_gates.generate_ci())`.

2. **`tests/test_repo_settings.py`** (25 min).
   - Docstring: title "…what rules RB-M6 and RB-G7 ask…"; after the
     second-approval paragraph, **What RB-G7 adds**: (6) branches up to date
     before merging — an active `required_status_checks` rule with at least
     one check sets `strict_required_status_checks_policy` to `true`; the CI
     checks the merge ref (`tests/test_ci.py`), and this makes it the merge
     that happens; GitHub applies the most restrictive version of aggregated
     rules, so any ruleset may supply it, and (5) then covers that ruleset;
     decided 2026-10-08. "more than the five" and "the five requirements were
     seen to hold" become "six".
   - `UP_TO_DATE = "branches up to date before merging"`,
     `UP_TO_DATE_OPTION = "Require branches to be up to date before
     merging"`; `_up_to_date_rules(rules)`: the rules of type
     `required_status_checks` whose `parameters` is a mapping with the flag
     `is True` and a non-empty list under `required_status_checks`.
   - `_suppliers` adds the ids of `_up_to_date_rules(rules)`. In
     `ruleset_findings`, after the loop over the four types: no such rule →
     `f'{UP_TO_DATE} is not asked for — tick "{UP_TO_DATE_OPTION}" in the
     ruleset (RB-G7)'`.
   - Stubs: the heading comment becomes "the live answers of 2026-10-05, only
     the keys read above, plus the one key RB-G7 reads, set as the floor asks
     (live: false on 2026-10-08)"; `_todays_rules()`'s required-check
     `parameters` gains `"strict_required_status_checks_policy": True` first.
   - `test_the_ruleset_check_goes_red_when_a_rule_is_removed`: the first
     finding stays `f"{RULE_TYPES[rule_type]} is not asked for"`; for
     `required_status_checks` a second one starts with `f"{UP_TO_DATE} is not
     asked for"`, for the others there is none.
   - New: `test_the_ruleset_check_goes_red_when_branches_need_not_be_up_to_date`
     (flag `False` id `live-2026-10-08`, key removed, `None`, `"true"`; exactly
     one finding, starting with `UP_TO_DATE`, naming `UP_TO_DATE_OPTION`);
     `test_the_ruleset_check_goes_red_when_only_a_rule_without_checks_asks_for_it`
     (today's flag `False`, a ruleset-7 rule with the flag and an empty list);
     `test_up_to_date_from_a_second_ruleset_holds` (today's flag `False`, a
     ruleset-7 rule with the flag and `[{"context": "floor"}]`, both bypass
     lists empty → `[]`);
     `test_the_ruleset_check_goes_red_when_the_up_to_date_ruleset_can_be_bypassed`
     (the same, ruleset 7 with a bypass actor → exactly
     `"ruleset 7 lets RepositoryRole 5 bypass it"`).

3. **`scripts/ramp_valves.py`** (2 min): the `"merge-freshness"` entry out;
   in its place:

   ```python
       # "merge-freshness" (RB-G7) closed on <DAY>: tests/test_ci.py asserts the
       # merge ref, the gate `ruleset` the up-to-date requirement; rule set 5.0.0.
   ```

4. **`tests/test_ramp_valves.py`** (3 min): import `REGEL_VENTILE` beside
   `valves`; replace the `"merge-freshness" in namen` line with
   `missing = sorted(set(REGEL_VENTILE) - namen)` and `assert not missing,
   f"rule valves missing from valves(): {missing} — was the list emptied?"`.
   The count assertion stays.

5. **`docs/governance/regelwerk.md`** (10 min). Header: `version: 5.0.0`,
   `updated: <DAY>`, nothing else. The RB-G7 row:

   ```markdown
   | **RB-G7** | Eine leere Menge ist kein Ergebnis: jedes Gate behauptet seine Schlüsselmenge als nicht leer. Geprüft wird der Merge-Stand, nicht der Branch-Kopf. Die CI prüft den Merge-Ref des Pull Requests, und das Ruleset verlangt, dass der Branch vor dem Merge auf dem Stand seines Ziels ist. Ob das Ruleset das verlangt, misst nur die Maschine des Maintainers (Gate `ruleset`, `placement: writer`): wird die Einstellung abgeschaltet, hält das einen Merge über GitHub nicht auf, nur den nächsten lokalen `make verify` | 4 | `tests/test_ramp_valves.py`::test_the_valve_list_is_not_empty · `tests/test_regelwerk.py`::test_the_list_is_not_empty · `tests/test_ci.py`::test_the_verification_runs_against_the_merge_ref · `tests/test_repo_settings.py`::test_master_has_a_ruleset_with_required_checks | P L I |
   ```

   In §7, above `### 4.0.0 — 2026-10-06`:

   ```markdown
   ### 5.0.0 — <DAY>

   **RB-G7** prüft den Merge-Stand jetzt ganz. Die CI prüft den Merge-Ref des
   Pull Requests (`refs/pull/N/merge`). Das allein reichte nicht: er wird
   berechnet, wenn die CI läuft, und bewegt sich `main` vorher, bleibt `verify`
   grün für einen Merge gegen ein älteres `main`. Darum verlangt das Ruleset
   jetzt, dass ein Branch vor dem Merge auf dem Stand seines Ziels ist.
   Entschieden vom Maintainer am 2026-10-08 (Änderung `rb-g7-merge-freshness`,
   Bead `coding-harness-34z`).

   MAJOR, weil §4 es so vorschreibt: die beiden Sätze der Regel bleiben, aber
   sie verlangt mehr als vorher — jedes Repository, in dem sie gilt, braucht
   die Ruleset-Einstellung „Require branches to be up to date before merging".

   - **Geändert:** RB-G7 — zwei Sätze angefügt (was CI und Ruleset prüfen, und dass nur die Maschine des Maintainers misst, ob das Ruleset es verlangt — §3, Stufe 4); Erzwinger um `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref` und `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks` ergänzt, `Ramp:merge-freshness` entfällt; Stufe (4) und Geltung unverändert. Keine ID geändert, keine entfernt
   - **Tests:** neu `tests/test_ci.py::test_the_verification_runs_against_the_merge_ref` samt eingepflanzten Fehlern; `tests/test_repo_settings.py` verlangt als sechste Anforderung den aktuellen Branch (`strict_required_status_checks_policy`), gemessen im Gate `ruleset` auf der Maschine des Maintainers, nicht in der gehosteten CI; `tests/test_ramp_valves.py` nennt kein einzelnes Ventil mehr. Das Ventil `merge-freshness` ist geschlossen, nicht still gestrichen
   - **Agents/Hooks/Templates:** `prompts/07-commit.md`, „The merge", hat einen Schritt für einen Branch, der hinter seiner Basis liegt; `docs/governance/quality-gates.md` sagt unter den Maschinen-Gates, warum der geprüfte Merge-Ref der gemergte ist
   - **lakeswitch-ai:** nichts — das Ruleset dort („lakeswitch floor", gelesen am 2026-10-08) verlangt den aktuellen Branch bereits, und seine Workflows checken ohne `ref:` aus
   ```

6. **`docs/governance/quality-gates.md`** (3 min): `updated: <DAY>`; after
   "…die CI baut, was nach dem Merge entsteht." in the same paragraph:
   "Dass dieser Merge-Ref auch der gemergte ist, sichert das Ruleset: es
   verlangt, dass der Branch vor dem Merge auf dem Stand seines Ziels ist
   (RB-G7). Bewegt sich `main`, wird der Pull Request aktualisiert und neu
   geprüft."

7. **`prompts/07-commit.md`** (2 min): under "The merge", after step 6:

   ```markdown
   7. If GitHub refuses the merge because the branch is behind its base — the
      ruleset requires branches to be up to date before merging (rule RB-G7)
      — the agent runs `gh pr update-branch <n>`, waits until CI is green on
      the new head and starts again at step 2: a new head needs a new
      restatement. If the update reports a conflict, the agent stops and says
      so.
   ```

8. **Artefacts** (2 min): `implementation_status: partial` in this folder's
   four files, then `python3 scripts/plans_registry.py --index`.

## Verification

```bash
python3 -m pytest tests/test_ci.py tests/test_repo_settings.py tests/test_ramp_valves.py tests/test_regelwerk.py tests/test_kit.py tests/test_gate_machinery.py -q
RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs
python3 scripts/ramp_valves.py --format=json | grep merge-freshness   # expect no output
git diff --exit-code eae78a3 -- .github/workflows/ci.yml scripts/ci_gates.py decisions/gates.yaml scripts/kit/
make verify
```

| Criterion | Held by | Goes red when |
|---|---|---|
| 1 | `test_ci.py::test_the_verification_runs_against_the_merge_ref` | a checkout gets `ref:`, or the trigger or job drifts |
| 2 | `::test_the_merge_ref_check_flags_a_planted_fault`, `::…_a_ref_the_generator_emits`; `::test_the_mutation_ratchet_only_turns_one_way` | the function misses a fault, or a new name counts as mutation evidence |
| 3 | `test_repo_settings.py::…_when_branches_need_not_be_up_to_date`, `::…_only_a_rule_without_checks_asks_for_it`, `::…_the_up_to_date_ruleset_can_be_bypassed` | any truthy value counts, an empty list counts, or the flag's ruleset escapes the bypass check |
| 4 | `::test_todays_ruleset_holds`, `::test_a_stricter_ruleset_still_holds`, `::test_the_measurement_holds_on_todays_answers`, `::test_up_to_date_from_a_second_ruleset_holds` | the flag is demanded on the `verify` rule only, or the stubs lack it |
| 5 | `::test_an_unreachable_api_is_not_a_pass`, `::test_a_hidden_bypass_list_is_not_a_pass`, `::…_when_a_rule_is_removed` | a failed call reads as a pass, or one finding hides the other |
| 6 | `::test_master_has_a_ruleset_with_required_checks` in the gate `ruleset` | the live flag is `false` (expected until ticked) |
| 7 | the `grep` above; gate `ramp-valves`; `test_regelwerk.py` orphan check | the valve stays, or stays on one side |
| 8 | `test_ramp_valves.py::test_the_valve_list_is_not_empty` | `REGEL_VENTILE` emptied, or `valves()` drops it |
| 9 | `test_regelwerk.py::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-G7]`, `::test_every_named_ramp_exists_and_no_valve_is_orphaned`; phase 6 reading | an enforcer name is wrong, or a `Ramp:` stays |
| 10 | `::test_version_is_semver_and_history_is_monotone`, `::test_sync_impact_entry_exists_for_the_current_version`; gate `frontmatter-current`; `git diff` in phase 6 | version and entry disagree, a line is missing, another row moved |
| 11, 12 | gate `frontmatter-current`; phase 6 reading | a sentence missing, a row changed |
| 13 | the `git diff` above; gates `leerprobe`, `ci-drift` | a guarded file changed, or a new test is red in the kit copy |
| 14 | `make verify` | any other block gate red |

Phase 4 plants, besides criterion 2's faults, at least: the valve back in
`REGEL_VENTILE`; `Ramp:merge-freshness` back in the row; `version: 4.0.0`;
`is True` relaxed to truthiness; `_up_to_date_rules` without the non-empty
check; `_suppliers` without the flag's rules; `REGEL_VENTILE` emptied — each
red, restored with `git checkout`, recorded as in rb-m6-one-account.

## Not touched

GitHub (agents only `GET`); `ci.yml`, `ci_gates.py`, `gates.yaml`,
`scripts/kit/` (no gate is added); `docs/WORKFLOW.md` (it states no merge
mechanics); the rule set beyond step 5; the MG rows; `docs/journal/`.

## Phase 7

A decision pull request from `decide/rb-g7-merge-freshness`, two decisions
that stand together (the gate `adr-answers` needs this feature's answer):
title `decide(governance): RB-G7 checks the merge that happens — merge ref
and up-to-date branches`, label `decision`, body in the multi-decision form
of `prompts/07-commit.md` from `.github/PULL_REQUEST_TEMPLATE/decision.md` —
(1) RB-G7 amended, rule set 5.0.0, with the MG-2 sentence and merge step 7;
(2) no ADR for this change. It names bead "RB-G7 merge-freshness valve"
(coding-harness-34z) as closed.

"What could break": every open pull request needs an update and a new CI run
after each merge; `make verify` on the maintainer's machine is red on the gate
`ruleset` until the checkbox is ticked.

"Your move" adds the maintainer's step, best before the merge:

1. GitHub → `MPAdesso/coding-harness` → Settings → Rules → Rulesets → `main`
   → under "Require status checks to pass", tick "Require branches to be up
   to date before merging" → Save changes.
2. Or, the same in one command (no agent runs it; the read half was checked
   on 2026-10-08):

   ```bash
   gh api repos/MPAdesso/coding-harness/rulesets/24528176 \
     --jq '{rules: [.rules[] | if .type == "required_status_checks" then .parameters.strict_required_status_checks_policy = true else . end]}' \
     | gh api --method PUT repos/MPAdesso/coding-harness/rulesets/24528176 --input -
   ```

3. Check: `gh api 'repos/{owner}/{repo}/rules/branches/main' --jq '.[] |
   select(.type == "required_status_checks") |
   .parameters.strict_required_status_checks_policy'` prints `true`, and
   `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs`
   passes.

"After the merge": `make close-merged ARGS=--write` (maintainer's machine).

## Time used

Phase 4 appends its spans here (`prompts/04-implement.md`).
