---
title: "Findings — pi-catalog-redirect"
category: findings
status: draft
implementation_status: none
date: 2026-10-30
created: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-j2wb
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — pi-catalog-redirect

Stage-2 call, 2026-10-30: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 774 files, 2732 commits, 12 rules.

Stage-2 call, 2026-10-30: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 777 files, 2736 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/pi-catalog-redirect/plan.md` +10 -10
> - `plans/changes/pi-catalog-redirect/spec.md` +1 -1
> - `scripts/stage2_research_catalog.mjs` +75 -7
> - `tests/test_stage2_research_catalog.py` +366 -9
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
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
>         assert bridge["exit_code"] == 0
> >       first_path = next(p for p, _ in sources.requests if p.startswith(f"/api/models/{GO}") and "pi-version=" not in p)
> E       StopIteration
>
> tests/test_stage2_research_catalog.py:1008: StopIteration
> _____ test_preflight_redirect_record_preserves_request_and_final_evidence ______
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-catalog-redirect/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5707/popen-gw6/test_preflight_redirect_record0')
> sources = <test_stage2_research_catalog.Sources object at 0x108d47560>
>
>     def test_preflight_redirect_record_preserves_request_and_final_evidence(tmp_path, sources):
>         # Criterion 4. Planted fault: the requested url is overwritten, a hop field is missing, the
>         # digest describes the redirect body, or selection drops the hop evidence.
>         def admitted(path: str) -> tuple[int, str]:
>             return 307, versioned_location(path)
>     
>         sources.pi_redirect = admitted
>         bridge = collect(tmp_path, sources)
> >       first_path = next(p for p, _ in sources.requests if p.startswith(f"/api/models/{GO}") and "pi-version=" not in p)
> E       StopIteration
>
> tests/test_stage2_research_catalog.py:1131: StopIteration
> _______ test_preflight_accepts_one_pinned_version_redirect[302-<lambda>] _______
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/pi-catalog-redirect/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-5707/popen-gw0/test_preflight_accepts_one_pin1')
> sources = <test_stage2_research_catalog.Sources object at 0x108f7eba0>
> status = 302, build = <function <lambda> at 0x10991f100>
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
>         assert bridge["exit_code"] == 0
> >       first_path = next(p for p, _ in sources.requests if p.startswith(f"/api/models/{GO}") and "pi-version=" not in p)
> E       StopIteration
>
> tests/test_stage2_research_catalog.py:1008: StopIteration
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[308-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[303-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[301-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[307-<lambda>]
> FAILED tests/test_stage2_research_catalog.py::test_preflight_redirect_record_preserves_request_and_final_evidence
> FAILED tests/test_stage2_research_catalog.py::test_preflight_accepts_one_pinned_version_redirect[302-<lambda>]
> 6 failed, 25 passed in 3.71s
> ```

Stage-2 call, 2026-10-30: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 777 files, 2739 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 777 files, 2747 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 777 files, 2762 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model hy3 · leak check clean over 777 files, 2772 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 777 files, 2775 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 777 files, 2778 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 777 files, 2784 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 777 files, 2786 commits, 12 rules.

Stage-2 call, 2026-10-30: review-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 777 files, 2790 commits, 12 rules.
