---
title: "Findings — kit-probe-on-kit-change"
category: findings
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-w2ay
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — kit-probe-on-kit-change

Stage-2 call, 2026-11-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1045 files, 4136 commits, 12 rules.

Stage-2 call, 2026-11-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1048 files, 4143 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/kit-probe-on-kit-change/plan.md` +14 -14
> - `plans/changes/kit-probe-on-kit-change/spec.md` +1 -1
> - `scripts/ci_gates.py` +345 -3
> - `scripts/kit/probe.py` +51 -1
> - `scripts/verify_all.sh` +85 -21
> - `scripts/verify_duration.py` +61 -2
> - `tests/test_gate_catalog.py` +44 -0
> - `tests/test_kit.py` +89 -0
> - `tests/test_kit_probe_condition.py` +875 -0
> - `tests/test_verify_duration.py` +117 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/ci_gates.py`, `scripts/verify_duration.py`, `tests/test_kit_probe_condition.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E         
> E         [verify-lock] admitted
> E         [verify-lock] available memory 64% at or above the 0% floor; starting
> E         Traceback (most recent call last):
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw0/test_skip_preserves_early_stop0/vertraege/stopp/baum/scripts/ci_gates.py", line 1254, in <module>
> E             sys.exit(main())
> E                      ^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw0/test_skip_preserves_early_stop0/vertraege/stopp/baum/scripts/ci_gates.py", line 1224, in main
> E             entscheidungen = lokale_entscheidungen(auswahl)
> E                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw0/test_skip_preserves_early_stop0/vertraege/stopp/baum/scripts/ci_gates.py", line 845, in lokale_entscheidungen
> E             return {g["id"]: _entscheidung(g, aenderung) for g in auswahl}
> E                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw0/test_skip_preserves_early_stop0/vertraege/stopp/baum/scripts/ci_gates.py", line 809, in _entscheidung
> E             praefixe = list(dekl.get("paths") or [])
> E                             ^^^^^^^^
> E         AttributeError: 'NoneType' object has no attribute 'get'
> E         die Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates
> E         
> E       assert 2 == 1
> E        +  where 2 = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...Type\' object has no attribute \'get\'\ndie Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates\n').returncode
>
> tests/test_kit_probe_condition.py:841: AssertionError
> ____________ test_skip_output_and_history_name_reason_without_pass _____________
> [gw10] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/kit-probe-on-kit-change/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw10/test_skip_output_and_history_n0')
>
>     def test_skip_output_and_history_name_reason_without_pass(tmp_path: Path) -> None:
>         """The skip names its measured reason in output and history — no gate frame, no exit, no seconds.
>     
>         Planted faults: a missing skip line or base, a fabricated exit status or
>         test duration, a skip parsed as a green gate section, or a history report
>         counting the skip as an executed gate.
>         """
>         baum = _baum(tmp_path / "hinweis")
>         _verzweige(baum)
>         ergebnis = _lauf_laeufer(baum)
> >       assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
> E       AssertionError: exit 2
> E         {
> E           "job": "verify",
> E           "candidate": "11c403c662d69d15ee871cd0be516c25fed68f39",
> E           "base": "11c403c662d69d15ee871cd0be516c25fed68f39",
> E           "config_sha256": "b310652cbcf527635910712481409972d4bad41b0d81f767ca0d42f9741b875b",
> E           "gates_total": 3,
> E           "gates_job": 3
> E         }
> E         
> E         [verify-lock] admitted
> E         [verify-lock] available memory 64% at or above the 0% floor; starting
> E         Traceback (most recent call last):
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw10/test_skip_output_and_history_n0/hinweis/baum/scripts/ci_gates.py", line 1254, in <module>
> E             sys.exit(main())
> E                      ^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw10/test_skip_output_and_history_n0/hinweis/baum/scripts/ci_gates.py", line 1224, in main
> E             entscheidungen = lokale_entscheidungen(auswahl)
> E                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw10/test_skip_output_and_history_n0/hinweis/baum/scripts/ci_gates.py", line 845, in lokale_entscheidungen
> E             return {g["id"]: _entscheidung(g, aenderung) for g in auswahl}
> E                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E           File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-152/popen-gw10/test_skip_output_and_history_n0/hinweis/baum/scripts/ci_gates.py", line 809, in _entscheidung
> E             praefixe = list(dekl.get("paths") or [])
> E                             ^^^^^^^^
> E         AttributeError: 'NoneType' object has no attribute 'get'
> E         die Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates
> E         
> E       assert 2 == 0
> E        +  where 2 = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...Type\' object has no attribute \'get\'\ndie Gate-Liste liess sich nicht erzeugen — kein VERIFY ohne gemessene Gates\n').returncode
>
> tests/test_kit_probe_condition.py:703: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_duration.py::test_skip_history_is_separate_and_old_history_stays_readable
> FAILED tests/test_kit_probe_condition.py::test_only_nontravelling_content_or_no_changes_skip_probe
> FAILED tests/test_kit_probe_condition.py::test_manifest_changes_and_travelling_edits_run_probe
> FAILED tests/test_kit_probe_condition.py::test_condition_comes_from_declaration_for_any_gate_id
> FAILED tests/test_kit_probe_condition.py::test_transferred_kit_uses_recipient_manifest_and_condition
> FAILED tests/test_kit_probe_condition.py::test_skip_preserves_early_stop_parser_and_storage_failure_contracts
> FAILED tests/test_kit_probe_condition.py::test_skip_output_and_history_name_reason_without_pass
> 7 failed, 7 passed in 1.84s
> ```

Stage-2 call, 2026-11-13: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1049 files, 4154 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/kit-probe-on-kit-change/plan.md` +13 -13
> - `scripts/ci_gates.py` +8 -4
> - `scripts/verify_duration.py` +6 -1
> - `tests/test_kit_probe_condition.py` +6 -2
> - `tests/test_verify_duration.py` +2 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E           "gates_job": 3
> E         }
> E         
> E         ── gates: job=verify ──────────────────────────────────────────────
> E         
> E         [verify-lock] admitted
> E         [verify-lock] available memory 67% at or above the 0% floor; starting
> E         die Entscheidung von [aa-rot] ist weder run noch skip — die Gate-Liste liess sich nicht entscheiden
> E         
> E       assert 2 == 1
> E        +  where 2 = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...loor; starting\ndie Entscheidung von [aa-rot] ist weder run noch skip — die Gate-Liste liess sich nicht entscheiden\n').returncode
>
> tests/test_kit_probe_condition.py:845: AssertionError
> ___________ test_only_nontravelling_content_or_no_changes_skip_probe ___________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/kit-probe-on-kit-change/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-162/popen-gw4/test_only_nontravelling_conten0')
>
>     def test_only_nontravelling_content_or_no_changes_skip_probe(tmp_path: Path) -> None:
>         """A content-only edit to inventory, an empty change and ignored noise skip the expensive gate.
>     
>         Planted faults: a `bestand` edit launching the throwaway tests, an empty
>         measured change launching them, or an ignored file counting as a change.
>         """
>         basis = tmp_path / "vergessen"
>         dekl = dict(VOLLE_DEKLARATION)
>         baum = _baum(
>             basis / "baum",
>             gate_bauer=lambda b: [
>                 _gate(b, "aa-vor"),
>                 _gate(b, "zz", dekl=dekl, cost="minutes"),
>                 _gate(b, "mm-nach", cost="minutes"),
>             ],
>         )
>         _verzweige(baum)
>     
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "an empty measured change launched the probe"
>         assert grund.startswith("skip:") and "merge-base with origin/main" in grund, grund
>     
>         (baum / "rest" / "notiz.txt").write_text("nur Inventur geaendert\n", encoding="utf-8")
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "a content-only `bestand` edit launched the probe"
>         assert "merge-base with origin/main" in grund, grund
>     
>         (baum / "rauschen").mkdir()
>         (baum / "rauschen" / "x.txt").write_text("ignored\n", encoding="utf-8")
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "an ignored file counted as a change"
>     
>         # The runner executes the skip: the expensive marker never appears, the
>         # final wording acknowledges the declared skip.
>         ergebnis = _lauf_laeufer(baum)
> >       assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
> E       AssertionError: exit 2
> E         {
> E           "job": "verify",
> E           "candidate": "867ea2f3417595895f186b0b2c19b2ec87c6e37c",
> E           "base": "867ea2f3417595895f186b0b2c19b2ec87c6e37c",
> E           "config_sha256": "4187e5e775716425a4bf90c1fad1b898863bc01ede3c9e2fccc78feb36cd8e52",
> E           "gates_total": 3,
> E           "gates_job": 3
> E         }
> E         
> E         ── gates: job=verify ──────────────────────────────────────────────
> E         
> E         [verify-lock] admitted
> E         [verify-lock] available memory 67% at or above the 0% floor; starting
> E         die Entscheidung von [aa-vor] ist weder run noch skip — die Gate-Liste liess sich nicht entscheiden
> E         
> E       assert 2 == 0
> E        +  where 2 = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...loor; starting\ndie Entscheidung von [aa-vor] ist weder run noch skip — die Gate-Liste liess sich nicht entscheiden\n').returncode
>
> tests/test_kit_probe_condition.py:416: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_kit_probe_condition.py::test_transferred_kit_uses_recipient_manifest_and_condition
> FAILED tests/test_kit_probe_condition.py::test_skip_output_and_history_name_reason_without_pass
> FAILED tests/test_kit_probe_condition.py::test_skip_preserves_early_stop_parser_and_storage_failure_contracts
> FAILED tests/test_kit_probe_condition.py::test_only_nontravelling_content_or_no_changes_skip_probe
> 4 failed, 10 passed in 5.27s
> ```

Stage-2 call, 2026-11-14: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1049 files, 4161 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_all.sh` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         assert len(ende) == 1 and ende[0]["verdict"] == "red"
>         rot = stage2.red_sections(ergebnis.stdout)
>         assert rot is not None and "aa-rot" in rot and "block-rot-diagnostik" in rot, rot
>         assert "zz-leerprobe" not in rot and "mm-nach" not in rot, rot
>     
>         # Broken measurement storage: the runner warns, the gates and the skip
>         # keep their verdicts, and nothing is written through the substituted file.
>         baum = _baum(
>             basis / "lager",
>             gate_bauer=lambda b: [
>                 _gate(b, "aa-vor"),
>                 _gate(b, "zz", dekl=dict(VOLLE_DEKLARATION), cost="minutes"),
>             ],
>         )
>         _verzweige(baum)
>         lager = baum.parent / "state" / "coding-harness"
>         lager.mkdir(parents=True)
>         (lager / verify_duration.HISTORY_NAME).mkdir()
>         ergebnis = _lauf_laeufer(baum)
>         assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
>         assert "measurement storage unusable" in ergebnis.stderr, ergebnis.stderr
> >       assert "VERIFY GREEN" in ergebnis.stdout and "1 declared local skip" in ergebnis.stdout
> E       assert ('VERIFY GREEN' in '{\n  "job": "verify",\n  "candidate": "497616f94552d766da4e3092ede9f4354dc2f6cc",\n  "base": "497616f94552d766da4e309...rtraege/lager/baum/order.txt\'; true\n── [zz] gruen\n\nVERIFY GREEN — every local gate of the \'verify\' job passed.\n' and '1 declared local skip' in '{\n  "job": "verify",\n  "candidate": "497616f94552d766da4e3092ede9f4354dc2f6cc",\n  "base": "497616f94552d766da4e309...rtraege/lager/baum/order.txt\'; true\n── [zz] gruen\n\nVERIFY GREEN — eve [… 47 characters left out …]
> E        +  where '{\n  "job": "verify",\n  "candidate": "497616f94552d766da4e3092ede9f4354dc2f6cc",\n  "base": "497616f94552d766da4e309...rtraege/lager/baum/order.txt\'; true\n── [zz] gruen\n\nVERIFY GREEN — every local gate of the \'verify\' job passed.\n' = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...ry\nverify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged\n' [… 8 characters left out …]
> E        +  and   '{\n  "job": "verify",\n  "candidate": "497616f94552d766da4e3092ede9f4354dc2f6cc",\n  "base": "497616f94552d766da4e309...rtraege/lager/baum/order.txt\'; true\n── [zz] gruen\n\nVERIFY GREEN — every local gate of the \'verify\' job passed.\n' = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...ry\nverify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged\n' [… 8 characters left out …]
>
> tests/test_kit_probe_condition.py:874: AssertionError
> ___________ test_only_nontravelling_content_or_no_changes_skip_probe ___________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/kit-probe-on-kit-change/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-167/popen-gw4/test_only_nontravelling_conten0')
>
>     def test_only_nontravelling_content_or_no_changes_skip_probe(tmp_path: Path) -> None:
>         """A content-only edit to inventory, an empty change and ignored noise skip the expensive gate.
>     
>         Planted faults: a `bestand` edit launching the throwaway tests, an empty
>         measured change launching them, or an ignored file counting as a change.
>         """
>         basis = tmp_path / "vergessen"
>         dekl = dict(VOLLE_DEKLARATION)
>         baum = _baum(
>             basis / "baum",
>             gate_bauer=lambda b: [
>                 _gate(b, "aa-vor"),
>                 _gate(b, "zz", dekl=dekl, cost="minutes"),
>                 _gate(b, "mm-nach", cost="minutes"),
>             ],
>         )
>         _verzweige(baum)
>     
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "an empty measured change launched the probe"
>         assert grund.startswith("skip:") and "merge-base with origin/main" in grund, grund
>     
>         (baum / "rest" / "notiz.txt").write_text("nur Inventur geaendert\n", encoding="utf-8")
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "a content-only `bestand` edit launched the probe"
>         assert "merge-base with origin/main" in grund, grund
>     
>         (baum / "rauschen").mkdir()
>         (baum / "rauschen" / "x.txt").write_text("ignored\n", encoding="utf-8")
>         entscheidung, grund, _ = _entscheidungen(baum)["zz"]
>         assert entscheidung == "skip", "an ignored file counted as a change"
>     
>         # The runner executes the skip: the expensive marker never appears, the
>         # final wording acknowledges the declared skip.
>         ergebnis = _lauf_laeufer(baum)
>         assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
>         assert "VERIFY GREEN" in ergebnis.stdout
> >       assert "1 declared local skip" in ergebnis.stdout
> E       assert '1 declared local skip' in '{\n  "job": "verify",\n  "candidate": "f16c0f6aaa069a0c6c573586946475798be4c6d7",\n  "base": "f16c0f6aaa069a0c6c57358...h] 0.094s\nexecution 1.559s · admission wait 0.008s\n\nVERIFY GREEN — every local gate of the \'verify\' job passed.\n'
> E        +  where '{\n  "job": "verify",\n  "candidate": "f16c0f6aaa069a0c6c573586946475798be4c6d7",\n  "base": "f16c0f6aaa069a0c6c57358...h] 0.094s\nexecution 1.559s · admission wait 0.008s\n\nVERIFY GREEN — every local gate of the \'verify\' job passed.\n' = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...b passed.\n', stderr='[verify-lock] admitted\n[verify-lock] available memory 62% at or above the 0% floor; starting\n' [… 8 characters left out …]
>
> tests/test_kit_probe_condition.py:418: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_kit_probe_condition.py::test_transferred_kit_uses_recipient_manifest_and_condition
> FAILED tests/test_kit_probe_condition.py::test_skip_output_and_history_name_reason_without_pass
> FAILED tests/test_kit_probe_condition.py::test_skip_preserves_early_stop_parser_and_storage_failure_contracts
> FAILED tests/test_kit_probe_condition.py::test_only_nontravelling_content_or_no_changes_skip_probe
> 4 failed, 10 passed in 5.87s
> ```
