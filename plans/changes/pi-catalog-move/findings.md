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

Stage-2 call, 2026-11-04: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 891 files, 3270 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-catalog-move/plan.md` +1 -1
> - `scripts/stage2.py` +6 -2
> - `tests/test_stage2_availability.py` +31 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>             if refresh.returncode != 0:
>                 raise Refused(
>                     f"`{PI_WRAPPER} update --models` ended {refresh.returncode}; the free stage is not filled "
>                     "from a stale cache."
>                 )
>             store = overlay_store(agent, rule["provider"])
>             stripped, notices = activate_overlay(agent, store, policy)
>             if stripped:
>                 listing = dropped_notice({model: ", ".join(fields) for model, fields in sorted(stripped.items())})
>                 print(f"review-loop: catalog fields not activated: {listing}", file=sys.stderr)
>             for notice in notices:
>                 print(f"Address notice: {notice}", file=sys.stderr)
>             fresh = {
>                 str(model["id"])
>                 for model in store.get(rule["provider"], {}).get("models", [])
>                 if isinstance(model, dict) and model.get("id")
>             }
>             invalid = {model for model in fresh if not MODEL_ID.fullmatch(model)}
>             if invalid:
>                 # Pi restores its remote cache before listing. Use a separate, validated cache for
>                 # that command; the fetched store and the snapshot remain unchanged as evidence.
>                 listing_agent = scratch / "listing-agent"
>                 listing_agent.mkdir()
>                 (listing_agent / "settings.json").write_bytes((agent / "settings.json").read_bytes())
>                 safe_store = {
>                     provider: {
>                         **entry,
>                         "models": [
>                             model
>                             for model in entry.get("models", [])
>                             if isinstance(model, dict)
>                             and isinstance(model.get("id"), str)
>                             and MODEL_ID.fullmatch(model["id"])
>                         ],
>                     }
>                     for provider, entry in store.items()
>                 }
>                 (listing_agent / "models-store.json").write_text(json.dumps(safe_store), encoding="utf-8")
>                 activate_overlay(listing_agent, safe_store, policy)
>                 env = {**env, "PI_CODING_AGENT_DIR": str(listing_agent)}
>             check_overlay(Path(env["PI_CODING_AGENT_DIR"]), home, policy=policy)
>             try:
>                 listing = launch(
>                     [str(PI_WRAPPER), "--list-models"], scratch, env, timeout=PI_DISCOVERY_SECONDS, limit=limit
>                 )
>             except CallFailed as error:
>                 raise Refused(
>                     f"the model listing did not end within {PI_DISCOVERY_SECONDS} seconds; the free stage is not entered. ({error})"
>                 ) from None
>         if listing.returncode != 0:
>             raise Refused(f"`{PI_WRAPPER} --list-models` ended {listing.returncode}; the free stage stays unentered.")
>         catalog = parse_catalog(listing.stdout or "")
>         # Only ids the fresh overlay carries: an id that only Pi's shipped list holds is not selected (Q-13).
>         dropped = free_drops(
>             root, rule, [*catalog, *({"provider": rule["provider"], "model": model} for model in sorted(invalid))], fresh
>         )
>         # Only assessed definitions become selectable: a fresh catalog row whose
>         # destination the record refuses is named as a drop and never reaches a
>         # launch, however the rule filters (criterion 5).
>         for definition in store.get(rule["provider"], {}).get("models", []):
>             if not isinstance(definition, dict) or not isinstance(definition.get("id"), str):
>                 continue
>             verdict = stage2_go.assess(policy, definition["id"], definition)
>             if not verdict.admitted:
>                 dropped.setdefault(definition["id"], verdict.problem)
>         selected = [model for model in select_free(rule, catalog) if model in fresh and model not in dropped]
>         if dropped:
>             print(f"review-loop: free ids dropped: {dropped_notice(dropped)}", file=sys.stderr)
>         if not selected and not allow_empty:
> >           raise Refused("the live catalog holds no free model for the configured rule; the free stage is not entered.")
> E           stage2.Refused: the live catalog holds no free model for the configured rule; the free stage is not entered.
>
> scripts/stage2.py:2334: Refused
> ----------------------------- Captured stderr call -----------------------------
> Address notice: opencode-go/deepseek-v4.1-flash: the recorded base path is /zen/go/v1, the definition names /inference/go/v1; running on with this same-host move
> review-loop: free ids dropped: deepseek-v4.1-flash (a paid model; the free class does not admit it)
> =========================== short test summary info ============================
> FAILED tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> FAILED tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> 2 failed, 39 passed in 35.11s
> ```

Stage-2 call, 2026-11-04: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 891 files, 3274 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model iceman-contributor-free · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model iceman-contributor-free · leak check clean over 891 files, 3276 commits, 12 rules.

Stage-2 call, 2026-11-04: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 891 files, 3278 commits, 12 rules.

## Phase 6 — Codex, 2026-11-04

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | BLOCKER | SPEC | phase-6 | plans/changes/pi-catalog-move/spec.md:65,84-85,100-101; scripts/stage2.py:1992-2006 | [DIVERGENT] For a refreshed catalog containing declared-paid `beam-free`, criterion 5 requires excluding it while preparation continues. The implementation adds that filter in `scripts/stage2.py`, but Protected areas forbids changes under `scripts/`, and Definition of Done requires protected areas untouched. The spec therefore requires the behavior change while prohibiting its implementation; completion cannot satisfy both requirements. [Acceptance criterion 5; Protected areas; Definition of Done] | Codex | fixed — orchestrator spec amendment: Protected areas and Definition of Done now carry the scripts/stage2.py exception the maintainer's answer decisions.md#Q-2 decided (2026-11-04) | — |

Phase 6 verdict: codex 01a1a858-e592-7b43-a893-1aa1ed9ff80a, 2026-11-04
Reviewer session: codex 01a1a858-e592-7b43-a893-1aa1ed9ff80a — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-04

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | Correctness | scripts/stage2.py::free_drops | `if not MODEL_ID.fullmatch(model): dropped[model] = "not a plain model id"` before `elif model in paid:` | A candidate selected by suffix/include that is declared paid in `modelle` but fails `MODEL_ID.fullmatch` hits the first branch and is reported as `"not a plain model id"` rather than `"a paid model; the free class does not admit it"`, so the newly added paid exclusion is shadowed by precedence with no fallback visible in the diff. | iceman-contributor-free | rejected — no failure: an id that fails MODEL_ID is dropped either way and never selected; only the reason text differs, and the ids in `modelle` are plain ids |  | disagree — The candidate is excluded in either branch. Criterion 5 requires exclusion, not precedence of the paid-model diagnostic over an invalid-ID diagnostic. |
| L1-2 | MINOR | Consistency | tests/test_pi_contract.py::test_real_opencode_provider_contracts | comment claims `GO_NATIVE`/synthetic fixtures keep their start vs `assert native_base_urls("opencode-go","openai-completions")=={GO_SHIPPED}`, `assert native_base_urls("opencode","openai-completions")=={ZEN_SHIPPED}` and ladder `baseUrl == GO_SHIPPED` | The changed assertions require the shipped bases while the adjacent changed comment still states the synthetic `GO_NATIVE` keeps its fixture starting point; the two claims about the same providers directly contradict one another with no reconciler visible in the diff. | iceman-contributor-free | rejected — false: the assertions read the installed (shipped) catalog, the comment speaks of the synthetic GO_NATIVE loopback fixtures; two different objects, both statements hold |  | disagree — The assertions inspect the installed package’s shipped catalog; GO_NATIVE and ZEN_NATIVE remain starting addresses for separate synthetic fixtures. These describe different data and do not contradict each other. |

Rounds run: 1

Record digest: sha256:d0e26379788963b62d14a305b174c32d3a537f69a12e7727528c251b118c568d

Record identity: sha256:d05cbee35212db5d6e88680c0011e79377acf631233d53d4a1811b7e73924c7d

Loop state: {"availability": {"checked_at": "2026-11-04T20:53:18+00:00", "failed": {"glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"server_error\",\"message\":\"Upstream request failed: Model access is disabled\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["iceman-contributor-free", "deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)", "grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["free"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "crouton-alpha-free", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "pulse-alpha-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-04T20:49:56+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1793825395046, "etag": "W/\"1bd64b7a4e5ceecb344acfe7686c20fc\"", "lastModified": 1793798534000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": [], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["iceman-contributor-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "rungs": ["glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured); grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: muse-spark-1.2-contributor, muse-spark-1.3-contributor.

<!-- End of released loop record -->

Stage-2 call, 2026-11-04: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 891 files, 3278 commits, 12 rules.
