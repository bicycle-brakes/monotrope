---
title: "Findings — pi-catalog-move"
category: findings
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-vku6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — pi-catalog-move

Stage-2 call, 2026-11-04: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 888 files, 3252 commits, 12 rules.

Stage-2 call, 2026-11-04: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 891 files, 3257 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +2 -2
> - `tests/test_pi_contract.py` +123 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_pi_contract.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     def test_real_catalog_move_contains_new_go_models() -> None:
>         """Ledger 2: the shipped opencode-go catalog carries the 2026-11-04 Go models on the moved base.
>     
>         The evidence is the installed package's own data file - no live store, no overlay, no
>         refresh; a catalog entry alone grants no permission to call its model (spec criterion 2).
>         """
>         catalog = {
>             model["id"]: model
>             for model in provider_data("opencode-go").get("openai-completions", {}).values()
>             if isinstance(model, dict)
>         }
>         for model_id in ("kimi-k3.1-pro", "minimax-m3.1-flash", "step-5-preview"):
>             model = catalog.get(model_id)
> >           assert model is not None, (
>                 f"{model_id}: absent from the installed Pi's shipped opencode-go catalog (openai-completions)"
>             )
> E           AssertionError: kimi-k3.1-pro: absent from the installed Pi's shipped opencode-go catalog (openai-completions)
> E           assert None is not None
>
> tests/test_pi_contract.py:611: AssertionError
> _________________ test_real_catalog_move_uses_locked_pi_1_5_0 __________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-catalog-move/.venv/bin/python3
>
>     @pytest.mark.usefixtures("installed_pi")
>     def test_real_catalog_move_uses_locked_pi_1_5_0() -> None:
>         """Ledger 1: manifest, lock graph, lock entry and running wrapper agree on exactly Pi 1.5.0.
>     
>         Every point is anchored to the literal version, so a floating pin, a lock the manifest
>         outgrew, a stale install or a wrapper reporting another version fails this contract
>         instead of passing the move.
>         """
>         pin = _manifest_pin()
> >       assert pin == PI_MOVED_PIN, f"tools/pi/package.json pins {pin!r}, not the moved {PI_MOVED_PIN}"
> E       AssertionError: tools/pi/package.json pins '1.2.0', not the moved 1.5.0
> E       assert '1.2.0' == '1.5.0'
> E         
> E         - 1.5.0
> E         ?   ^
> E         + 1.2.0
> E         ?   ^
>
> tests/test_pi_contract.py:544: AssertionError
> ______________ test_real_catalog_move_keeps_messages_catalog_base ______________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-catalog-move/.venv/bin/python3
>
>     @pytest.mark.usefixtures("installed_pi")
>     def test_real_catalog_move_keeps_messages_catalog_base() -> None:
>         """Ledger 3: the shipped opencode-go Messages entries carry anthropic-messages on the moved base.
>     
>         Catalog evidence for the separate Messages follow-up - no wire exchange is measured or
>         admitted here (spec criterion 3).
>         """
>         catalog = {
>             model["id"]: model
>             for model in provider_data("opencode-go").get("anthropic-messages", {}).values()
>             if isinstance(model, dict)
>         }
>         for model_id in ("qwen3.8-flash", "qwen3.8-max", "qwen3.7-plus", "minimax-m3"):
>             model = catalog.get(model_id)
>             assert model is not None, (
>                 f"{model_id}: absent from the installed Pi's shipped opencode-go catalog (anthropic-messages)"
>             )
>             assert model.get("api") == "anthropic-messages", (
>                 f"{model_id}: the shipped catalog files it under {model.get('api')!r}, not anthropic-messages"
>             )
> >           assert model.get("baseUrl") == GO_SHIPPED_MESSAGES, (
>                 f"{model_id}: the shipped base is {model.get('baseUrl')!r}, not {GO_SHIPPED_MESSAGES}"
>             )
> E           AssertionError: qwen3.8-flash: the shipped base is 'https://opencode.ai/zen/go', not https://opencode.ai/inference/go/anthropic
> E           assert 'https://opencode.ai/zen/go' == 'https://open.../go/anthropic'
> E             
> E             - https://opencode.ai/inference/go/anthropic
> E             + https://opencode.ai/zen/go
>
> tests/test_pi_contract.py:642: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_pi_contract.py::test_real_catalog_move_contains_new_go_models
> FAILED tests/test_pi_contract.py::test_real_catalog_move_uses_locked_pi_1_5_0
> FAILED tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base
> 3 failed, 37 passed in 30.16s
> ```

Stage-2 call, 2026-11-04: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 891 files, 3262 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-catalog-move/plan.md` +3 -3
> - `tests/test_pi_contract.py` +6 -4
> - `tools/pi/package.json` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                 admitted = f"{path}&pi-version={PIN}"
>                 if fault == "foreign-origin":
>                     location = f"{foreign_url}{admitted}"
>                 elif fault == "other-path":
>                     location = f"/api/models/providers/other?{query}&pi-version={PIN}"
>                 elif fault == "altered-original-value":
>                     location = f"{base}?{query.split('=', 1)[0]}=altered&pi-version={PIN}"
>                 elif fault == "duplicated-original-pair":
>                     location = f"{path}&{query}&pi-version={PIN}"
>                 elif fault == "comma-collision":
>                     # Row L1-6: `types=chat,image` and `types,chat=image` joined to the same string.
>                     name, value = next((n, v) for n, v in urllib.parse.parse_qsl(query) if "," in v)
>                     head, _, rest = value.partition(",")
>                     moved = urllib.parse.urlencode([(f"{name},{head}", rest)])
>                     others = [(n, v) for n, v in urllib.parse.parse_qsl(query) if n != name]
>                     tail = f"&{urllib.parse.urlencode(others)}" if others else ""
>                     location = f"{base}?{moved}{tail}&pi-version={PIN}"
>                 elif fault == "wrong-version":
>                     location = f"{path}&pi-version=0"
>                 elif fault == "duplicate-version":
>                     location = f"{admitted}&pi-version={PIN}"
>                 elif fault == "extra-parameter":
>                     location = f"{admitted}&extra=1"
>                 elif fault == "credentials":
>                     location = f"{sources.url.replace('http://', 'http://catalog-user@')}{admitted}"
>                 elif fault == "fragment":
>                     location = f"{admitted}#catalog"
>                 elif fault == "empty-fragment":
>                     # Phase-6 row F6-1: a bare `#` leaves `URL.hash` empty, so the raw Location is checked.
>                     location = f"{admitted}#"
>                 elif fault == "missing-location":
>                     location = None
>                 else:
>                     location = "http://"
>                 chosen["location"] = location
>                 return 307, location
>     
>             sources.pi_redirect = refused
>             bridge = collect(tmp_path, sources)
>     
>         evidence = bridge["sources"]["pi"]
> >       assert evidence["outcome"] == "redirect-refused"
> E       AssertionError: assert 'request-failed' == 'redirect-refused'
> E         
> E         - redirect-refused
> E         + request-failed
>
> tests/test_stage2_research_catalog.py:1138: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[307-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[303-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[301-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[302-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[duplicated-original-pair]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refreshes_despite_fresh_store_and_never_revives_cached_ids
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[comma-collision]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[308-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[other-path]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[altered-original-value]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[foreign-origin]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[duplicate-version]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[wrong-version]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[extra-parameter]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[empty-fragment]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[credentials]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[fragment]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[missing-location]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[unparsable-location]
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> ERROR tests/test_pi_contract.py::test_real_catalog_move_contains_new_go_models
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_catalog_move_uses_locked_pi_1_5_0
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-946684800000]
> ERROR tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> 19 failed, 10 passed, 11 errors in 10.04s
> ```

Stage-2 call, 2026-11-04: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 891 files, 3264 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>                     location = f"{admitted}#"
>                 elif fault == "missing-location":
>                     location = None
>                 else:
>                     location = "http://"
>                 chosen["location"] = location
>                 return 307, location
>     
>             sources.pi_redirect = refused
>             bridge = collect(tmp_path, sources)
>     
>         evidence = bridge["sources"]["pi"]
> >       assert evidence["outcome"] == "redirect-refused"
> E       AssertionError: assert 'request-failed' == 'redirect-refused'
> E         
> E         - redirect-refused
> E         + request-failed
>
> tests/test_stage2_research_catalog.py:1138: AssertionError
> _______ test_preflight_accepts_one_pinned_version_redirect[307-<lambda>] _______
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-catalog-move/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-697/popen-gw5/test_preflight_accepts_one_pin0')
> sources = <test_stage2_research_catalog.Sources object at 0x10b204ec0>
> status = 307, build = <function <lambda> at 0x10b63a020>
>
>     @pytest.mark.parametrize(
>         "status,build",
>         [
>             (301, lambda _url, path: versioned_location(path)),
>             (302, lambda _url, path: versioned_location(path, prefix=True)),
>             (303, lambda _url, path: versioned_location(path).replace("%2C", ",")),
>             (307, lambda url, path: f"{url}{versioned_location(path)}"),
>             (308, lambda _url, path: versioned_location(path, prefix=True)),
>         ],
>     )
>     def test_preflight_accepts_one_pinned_version_redirect(tmp_path, sources, status, build):
>         # Criterion 1. Planted fault: the admitted version hop fails preflight, hard-codes the version
>         # independently of the pin, or loses fresh catalog entries on the way.
>         def admitted(path: str) -> tuple[int, str]:
>             return status, build(sources.url, path)
>     
>         sources.pi_redirect = admitted
>         bridge = collect(tmp_path, sources)
> >       assert bridge["exit_code"] == 0
> E       assert 1 == 0
>
> tests/test_stage2_research_catalog.py:1047: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[303-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[301-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[302-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[308-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[foreign-origin]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[altered-original-value]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[duplicated-original-pair]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[comma-collision]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[other-path]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refreshes_despite_fresh_store_and_never_revives_cached_ids
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[duplicate-version]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[wrong-version]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[credentials]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[missing-location]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[extra-parameter]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[empty-fragment]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[fragment]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_refuses_unapproved_catalog_redirect[unparsable-location]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[307-<lambda>]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_catalog_move_contains_new_go_models
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> ERROR tests/test_pi_contract.py::test_real_catalog_move_uses_locked_pi_1_5_0
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-946684800000]
> ERROR tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> 19 failed, 10 passed, 11 errors in 8.66s
> ```
