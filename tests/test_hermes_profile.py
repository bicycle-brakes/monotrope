"""Coding Harness's Hermes profile is held offline (plans/changes/hermes-runner, slice 5, criteria 45-56).

The profile is `tools/hermes/`: a Hermes configuration, an env template, a wrapper, a sudo rule, a LaunchAgent and a
runbook. Nothing here installs or runs Hermes, sudo or launchd. The files are read with PyYAML, `plistlib` and text, and
the wrapper is run with a stub in place of Hermes (its install, run-root and home paths are the first lines of the
file, so a test can point them at a temporary directory).

Every check is a function of the profile directory. The real test calls it on `tools/hermes/`; `FAULTS` below plants
one fault at a time in a copy and expects the same check to go red. Where the config names a Hermes key, the source is
named in `KEY_SOURCES`; a key with no source there fails, so none is invented.
"""

from __future__ import annotations

import fnmatch
import plistlib
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
PROFILE = REPO / "tools" / "hermes"
MISSING = object()

# ---------------------------------------------------------------------------
# What the checks hold the files to, and where it comes from
# ---------------------------------------------------------------------------

# Every core toolset of Hermes's toolsets reference at tag v2026.9.21 (commit d337b73), website/docs/reference/
# toolsets-reference.md, table "Core Toolsets" (read 2026-10-06). The composites `safe`, `coding` and `debugging` and the
# platform toolsets are not core. A toolset new in a later tag must be added here, and to the config, in one change.
CORE_TOOLSETS = frozenset(
    {
        "browser",
        "clarify",
        "code_execution",
        "computer_use",
        "connections",
        "context_engine",
        "cronjob",
        "delegation",
        "desktop_ui",
        "discord",
        "discord_admin",
        "feishu_doc",
        "feishu_drive",
        "file",
        "homeassistant",
        "image_gen",
        "kanban",
        "memory",
        "project",
        "search",
        "session_search",
        "skills",
        "spotify",
        "terminal",
        "todo",
        "tts",
        "video",
        "video_gen",
        "vision",
        "web",
        "x_search",
        "yuanbao",
    }
)
KEPT_TOOLSETS = frozenset({"web", "file", "search"})  # criterion 45

# Where each key of tools/hermes/config.yaml comes from. "baseline" is adhd-relief's spike kit at bdce8dc
# (infra/macbook/spike-hermes/config.yaml); "docs:<page>" is Hermes's documentation at tag v2026.9.21 (website/docs/);
# "baseline-only" is a key the baseline names and no page read at the tag lists. NOT_READ_AT_TAG is the list the
# runbook (section 2) and the config file mark "not read".
KEY_SOURCES = {
    "model.provider": "baseline; docs:integrations/providers.md",
    "model.default": "baseline; docs:integrations/providers.md",
    "model.base_url": "baseline; docs:integrations/providers.md",
    "fallback_providers": "baseline; docs:integrations/providers.md",
    "auxiliary.free_only": "baseline-only",
    "auxiliary.openrouter_model": "baseline-only",
    "auxiliary.compression.provider": "docs:user-guide/configuration.md (Context Compression)",
    "auxiliary.compression.model": "docs:user-guide/configuration.md (Context Compression)",
    "auxiliary.title_generation.enabled": "docs:user-guide/configuration.md (Full auxiliary config reference)",
    "auxiliary.background_review.enabled": "docs:user-guide/features/memory.md",
    "agent.disabled_toolsets": "baseline; docs:user-guide/configuration.md (Global Toolset Disable)",
    "memory.memory_enabled": "docs:user-guide/features/memory.md",
    "memory.user_profile_enabled": "docs:user-guide/features/memory.md",
    "curator.enabled": "docs:user-guide/features/curator.md",
    "approvals.mode": "docs:user-guide/security.md",
    "approvals.cron_mode": "docs:user-guide/security.md",
    "approvals.single_query_mode": "docs:user-guide/security.md",
    "approvals.unattended_mode": "docs:user-guide/security.md",
    "approvals.deny": "docs:user-guide/security.md (User-Defined Deny Rules)",
    "web.backend": "baseline; docs:user-guide/features/web-search.md",
    "web.keyless_fallback": "baseline; docs:user-guide/features/web-search.md",
    "cron.allow_agent_scheduling": "baseline; docs:user-guide/features/cron.md",
    "security.tirith_enabled": "baseline; docs:user-guide/configuration.md",
    "updates.check": "baseline-only",
}
NOT_READ_AT_TAG = frozenset({"auxiliary.free_only", "auxiliary.openrouter_model", "updates.check"})

# Commands the deny globs must catch (criterion 47). Hermes matches `approvals.deny` case-insensitively against the
# whole command text and against the command with its executable reduced to the basename (security.md at the tag,
# "User-Defined Deny Rules"); `denied` below emulates exactly that, not Hermes's code.
DENIED_COMMANDS = (
    "git",
    "git status",
    "git push origin main",
    "/usr/bin/git push --force",
    "gh",
    "gh pr merge 12 --squash",
    "gh api repos/MPAdesso/coding-harness/rules/branches/main",
    "bd",
    "bd list",
    "bd update coding-harness-i3y --claim",
    "tools/bd ready",
    "./tools/bd dolt push",
    "/Users/someone/coding-harness/tools/bd create x",
)

# criterion 53: what is adhd-relief's, and so never in the profile's operating files (the runbook may name them)
ADHD_RELIEF = ("_hspike", "/users/_hspike", "spike-vault")
OPERATING_FILES = (
    "config.yaml",
    "recheck-agent.sh",
    "ai.coding-harness.research-recheck.plist",
    "sudoers",
    "env.example",
)
ENV_NAMES = frozenset({"OPENCODE_GO_API_KEY", "OPENCODE_GO_BASE_URL", "FIRECRAWL_API_KEY", "FIRECRAWL_API_URL"})
WRAPPER_PATH = "/usr/local/libexec/coding-harness/recheck-agent"
RUNBOOK_BUDGET = 300  # lines; plans/changes/hermes-runner/plan.md, "Decided in phase 3"

# ---------------------------------------------------------------------------
# Reading helpers
# ---------------------------------------------------------------------------


def config_of(p: Path) -> dict:
    return yaml.safe_load((p / "config.yaml").read_text())


def get(cfg: dict, dotted: str):
    cur = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return MISSING
        cur = cur[part]
    return cur


def leaves(node, prefix: str = "") -> dict:
    """Dotted path of every key that holds a scalar or a list."""
    if isinstance(node, dict):
        out: dict = {}
        for key, val in node.items():
            out |= leaves(val, f"{prefix}.{key}" if prefix else str(key))
        return out
    return {prefix: node}


def named_models(node, path: tuple = ()) -> list[str]:
    """Every model the config names: `model.default`, any `model:` value, any non-empty `openrouter_model`."""
    out: list[str] = []
    if isinstance(node, dict):
        for key, val in node.items():
            if (
                isinstance(val, str)
                and val
                and (key in {"model", "openrouter_model"} or (path == ("model",) and key == "default"))
            ):
                out.append(val)
            out += named_models(val, (*path, key))
    elif isinstance(node, list):
        for item in node:
            out += named_models(item, path)
    return out


def values_of(node, wanted: str) -> list[str]:
    """Every non-empty string a key called `wanted` holds, at any depth."""
    out: list[str] = []
    if isinstance(node, dict):
        for key, val in node.items():
            if key == wanted and isinstance(val, str) and val:
                out.append(val)
            out += values_of(val, wanted)
    elif isinstance(node, list):
        for item in node:
            out += values_of(item, wanted)
    return out


def denied(command: str, patterns: list[str]) -> bool:
    candidates = {command.lower()}
    head, _, rest = command.partition(" ")
    candidates.add((head.rsplit("/", 1)[-1] + (" " + rest if rest else "")).lower())
    return any(fnmatch.fnmatchcase(c, pat.lower()) for pat in patterns for c in candidates)


def sections(text: str) -> dict[str, str]:
    """Heading line -> body, for the `## ` headings (a `### ` heading stays in the body of its `## ` section)."""
    out: dict[str, str] = {}
    cur = None
    for line in text.split("\n"):
        if line.startswith("## "):
            cur = line
            out[cur] = ""
        elif cur is not None:
            out[cur] += line + "\n"
    return out


def section(text: str, heading_pattern: str) -> str:
    found = [body for head, body in sections(text).items() if re.search(heading_pattern, head)]
    assert len(found) == 1, f"{len(found)} sections match {heading_pattern!r}"
    return found[0]


# ---------------------------------------------------------------------------
# The checks, one per criterion. Each takes the profile directory and raises AssertionError.
# ---------------------------------------------------------------------------


def check_toolsets(p: Path) -> None:  # 45
    disabled = get(config_of(p), "agent.disabled_toolsets")
    assert isinstance(disabled, list), "agent.disabled_toolsets is not a list"
    assert len(disabled) == len(set(disabled)), "a toolset is listed twice"
    wanted = CORE_TOOLSETS - KEPT_TOOLSETS
    assert wanted <= set(disabled), f"core toolsets not disabled: {sorted(wanted - set(disabled))}"
    assert not (KEPT_TOOLSETS & set(disabled)), f"a kept toolset is disabled: {sorted(KEPT_TOOLSETS & set(disabled))}"
    assert set(disabled) <= CORE_TOOLSETS, f"names that are no core toolset: {sorted(set(disabled) - CORE_TOOLSETS)}"


def check_learning_off(p: Path) -> None:  # 46
    cfg = config_of(p)
    for key in (
        "memory.memory_enabled",
        "memory.user_profile_enabled",
        "auxiliary.background_review.enabled",
        "auxiliary.title_generation.enabled",
        "curator.enabled",
    ):
        assert get(cfg, key) is False, f"{key} is {get(cfg, key)!r}, not false"


def check_approvals(p: Path) -> None:  # 47
    cfg = config_of(p)
    assert get(cfg, "approvals.mode") in {"manual", "smart"}, f"approvals.mode is {get(cfg, 'approvals.mode')!r}"
    for key in ("cron_mode", "single_query_mode", "unattended_mode"):
        assert get(cfg, f"approvals.{key}") == "deny", f"approvals.{key} is not deny"
    patterns = get(cfg, "approvals.deny")
    assert isinstance(patterns, list)
    assert all(isinstance(x, str) for x in patterns)
    for command in DENIED_COMMANDS:
        assert denied(command, patterns), f"no approvals.deny pattern matches {command!r}"


def check_model_route(p: Path) -> None:  # 48
    cfg = config_of(p)
    assert get(cfg, "model.provider") == "opencode-go", "model.provider is not opencode-go"
    assert get(cfg, "model.default") == "glm-5.3", "model.default is not glm-5.3"
    assert urlparse(get(cfg, "model.base_url")).hostname == "127.0.0.1", "model.base_url is not on 127.0.0.1"
    assert get(cfg, "fallback_providers") == [], "fallback_providers is not empty"
    for url in values_of(cfg, "base_url"):
        assert urlparse(url).hostname == "127.0.0.1", f"a base_url off the proxy: {url}"
    for provider in values_of(cfg, "provider"):  # `main` is the main model's provider, valid inside `auxiliary`
        assert provider in {"opencode-go", "main"}, f"a provider other than opencode-go: {provider}"
    endpoints = {e["name"]: e for e in yaml.safe_load((REPO / "model-endpoints.yaml").read_text())["endpunkte"]}
    declared = set(endpoints["opencode-go"]["modelle"])
    for model in named_models(cfg):
        assert model in declared, f"{model} is not declared for opencode-go in model-endpoints.yaml"


def check_web(p: Path) -> None:  # 49
    cfg = config_of(p)
    assert get(cfg, "web.backend") == "firecrawl", "web.backend is not firecrawl"
    for key in ("web.keyless_fallback", "cron.allow_agent_scheduling", "updates.check"):
        assert get(cfg, key) is False, f"{key} is {get(cfg, key)!r}, not false"


def check_key_sources(p: Path) -> None:  # every key has a source; what no page at the tag lists is marked
    cfg_text = (p / "config.yaml").read_text()
    unknown = sorted(set(leaves(config_of(p))) - set(KEY_SOURCES))
    assert not unknown, f"keys with no named source (not read, so not written): {unknown}"
    assert {k for k, v in KEY_SOURCES.items() if v == "baseline-only"} == NOT_READ_AT_TAG, (
        "KEY_SOURCES and NOT_READ_AT_TAG differ"
    )
    for key in NOT_READ_AT_TAG:
        leaf = key.rsplit(".", 1)[-1]
        assert re.search(rf"^\s+{leaf}:.*not read at the tag", cfg_text, re.M), (
            f"{key} is not marked 'not read at the tag'"
        )
    facts = section((p / "README.md").read_text(), r"Facts, and what was not read")
    for key in NOT_READ_AT_TAG:
        assert f"`{key}`" in facts, f"{key} is not in the runbook's list of what was not read"


def check_wrapper_text(p: Path) -> None:  # 50
    text = (p / "recheck-agent.sh").read_text()
    for fragment in (
        "chat --oneshot",
        "--query-file",
        "--ignore-rules",
        "--format stream-json",
        "--max-turns",
        "env -i",
        "perl -e 'alarm shift; exec @ARGV'",
    ):
        assert fragment in text, f"wrapper lacks {fragment!r}"
    for forbidden in ("--yolo", "--worktree", "GH_TOKEN", "GITHUB_TOKEN"):
        assert forbidden not in text, f"wrapper names {forbidden}"
    assert re.search(r"--toolsets web,file\s", text), "the toolsets are not exactly web and file"
    assert re.search(r"^SERVICE_HOME=/Users/_chhermes$", text, re.M), "SERVICE_HOME is not the service user's home"
    assert 'HERMES_HOME="$SERVICE_HOME/.hermes"' in text, "HERMES_HOME is not the service user's"
    assert 'HERMES_WRITE_SAFE_ROOT="$run_dir/work"' in text, "HERMES_WRITE_SAFE_ROOT is not the run's work directory"
    assert re.search(r"^RUNS_ROOT=/Users/Shared/coding-harness-hermes/runs$", text, re.M), (
        "RUNS_ROOT is not the runs directory"
    )
    assert len(re.findall(r"^HERMES_BIN=", text, re.M)) == 1, "HERMES_BIN is not set exactly once"
    assert text.index("HERMES_BIN=") < text.index("exec env"), "HERMES_BIN is not set at the top"
    cap = re.search(r"^CAP_SECONDS=(\d+)", text, re.M)
    assert cap and 0 < int(cap.group(1)) <= 2700, "the wrapper's alarm is missing or longer than 45 minutes"
    assert '"$CAP_SECONDS"' in text, "the alarm does not use CAP_SECONDS"
    assert subprocess.run(["sh", "-n", str(p / "recheck-agent.sh")], check=False).returncode == 0, "sh -n fails"


def _wrapper_copy(p: Path, tmp: Path, stub_body: str, cap: int | None = None) -> tuple[Path, Path]:
    """The wrapper with its three paths (and optionally the cap) pointed into `tmp`, and a stub for Hermes."""
    stub = tmp / "stub-hermes"
    stub.write_text("#!/bin/sh\n" + stub_body)
    stub.chmod(0o755)
    run_dir = tmp / "runs" / "r1"
    (run_dir / "in").mkdir(parents=True)
    (run_dir / "work").mkdir()
    (run_dir / "in" / "query.md").write_text("q\n")
    text = (p / "recheck-agent.sh").read_text()
    for name, value in (("HERMES_BIN", stub), ("SERVICE_HOME", tmp / "home"), ("RUNS_ROOT", tmp / "runs")):
        text, n = re.subn(rf"^{name}=.*$", f"{name}={value}", text, flags=re.M)
        assert n == 1
    if cap is not None:
        text = re.sub(r"^CAP_SECONDS=\d+", f"CAP_SECONDS={cap}", text, flags=re.M)
    wrapper = tmp / "wrapper.sh"
    wrapper.write_text(text)
    return wrapper, run_dir


def check_wrapper_environment(p: Path) -> None:  # 50, run with a stub: flags, environment, directory
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d).resolve()
        wrapper, run_dir = _wrapper_copy(
            p, tmp, 'echo "ARGS: $*"; echo "PWD: $(pwd -P)"; echo "UMASK: $(umask)"; env | sort\n'
        )
        env = {"PATH": "/usr/bin:/bin", "GH_TOKEN": "secret", "GITHUB_TOKEN": "secret", "FOO": "bar"}
        done = subprocess.run(["sh", str(wrapper), str(run_dir)], env=env, capture_output=True, text=True, check=False)
        out = done.stdout
        assert done.returncode == 0, done.stderr
        assert (
            f"ARGS: chat --oneshot --query-file {run_dir}/in/query.md --toolsets web,file --ignore-rules "
            "--format stream-json --max-turns 60 --source tool"
        ) in out
        assert f"PWD: {run_dir}/work" in out, "Hermes does not start in the work directory"
        assert f"HERMES_HOME={tmp}/home/.hermes" in out, "HERMES_HOME is not the service user's"
        assert f"HERMES_WRITE_SAFE_ROOT={run_dir}/work" in out, "HERMES_WRITE_SAFE_ROOT is not the work directory"
        assert f"HOME={tmp}/home" in out, "HOME is not the service user's"
        assert "PATH=/usr/bin:/bin" in out, "PATH is not the fixed one"
        assert re.search(r"^UMASK: 0*2$", out, re.M), "umask is not 002: the maintainer could not read the agent's note"
        for leaked in ("GH_TOKEN", "GITHUB_TOKEN", "FOO="):
            assert leaked not in out, f"{leaked} reached Hermes"


def check_wrapper_alarm(p: Path) -> None:  # 50, the alarm of its own
    with tempfile.TemporaryDirectory() as d:
        wrapper, run_dir = _wrapper_copy(p, Path(d).resolve(), "exec sleep 3\n", cap=1)
        done = subprocess.run(
            ["sh", str(wrapper), str(run_dir)],
            env={"PATH": "/usr/bin:/bin"},
            capture_output=True,
            check=False,
            timeout=30,
        )
        assert done.returncode in {-14, 142}, f"Hermes was not ended by the alarm (exit {done.returncode})"


def check_wrapper_refusals(p: Path) -> None:  # 50, the real wrapper refuses before it starts anything
    wrapper = str(p / "recheck-agent.sh")
    root = "/Users/Shared/coding-harness-hermes/runs"
    cases = (
        ([], "usage"),
        (["a", "b"], "usage"),
        (["/tmp/x"], "outside"),
        ([root + "/"], "outside"),
        ([root + "/../x"], "'..'"),
        ([root + "/no-such-run"], "query.md"),
    )
    for args, reason in cases:
        done = subprocess.run(["sh", wrapper, *args], capture_output=True, text=True, check=False)
        assert done.returncode == 2, f"wrapper did not refuse {args}: exit {done.returncode}"
        assert reason in done.stderr, f"{args}: refused for another reason than {reason!r}: {done.stderr.strip()}"


def check_launchd(p: Path) -> None:  # 51
    plist = plistlib.loads((p / "ai.coding-harness.research-recheck.plist").read_bytes())
    assert "KeepAlive" not in plist, "KeepAlive is set"
    assert not plist.get("RunAtLoad", False), "RunAtLoad is set"
    assert "StartInterval" not in plist, "StartInterval is set"
    assert "UserName" not in plist, "UserName is set: a LaunchAgent of the maintainer, not a daemon"
    interval = plist["StartCalendarInterval"]
    assert isinstance(interval, dict), "one calendar interval expected"
    assert set(interval) == {"Weekday", "Hour", "Minute"}, "the schedule is not weekly"
    assert interval["Weekday"] in {0, 7}, "not Sunday"
    assert (interval["Hour"], interval["Minute"]) == (3, 0), "not 03:00"
    args = plist["ProgramArguments"]
    assert plist["WorkingDirectory"] + "/scripts/research_recheck.py" == args[1], "the job does not run from the clone"
    assert args[1].endswith("scripts/research_recheck.py") and args[2:] == ["run", "--notify"], args
    for name in (
        "ai.coding-harness.research-recheck.plist",
        "recheck-agent.sh",
        "sudoers",
        "config.yaml",
        "env.example",
    ):
        assert "gateway" not in (p / name).read_text().lower(), f"{name} names a gateway"


def check_sudoers(p: Path) -> None:  # 52
    rules = [x for x in (p / "sudoers").read_text().split("\n") if x.strip() and not x.lstrip().startswith("#")]
    assert len(rules) == 1, f"{len(rules)} rules"
    assert re.fullmatch(rf"@MAINTAINER@ ALL=\(_chhermes\) NOPASSWD: {re.escape(WRAPPER_PATH)}", rules[0]), rules[0]
    assert WRAPPER_PATH in (p / "README.md").read_text(), (
        "the runbook does not install the wrapper at the sudo rule's path"
    )
    assert WRAPPER_PATH in (p / "recheck-agent.sh").read_text(), "the wrapper does not name its installed path"


def check_no_adhd_identity(p: Path) -> None:  # 53
    for name in OPERATING_FILES:
        text = (p / name).read_text().lower()
        for needle in ADHD_RELIEF:
            assert needle not in text, f"{name} names {needle}"


def check_env_example(p: Path) -> None:  # 54
    text = (p / "env.example").read_text()
    seen = {}
    for line in text.split("\n"):
        if line.strip() and not line.lstrip().startswith("#"):
            m = re.fullmatch(r"([A-Z][A-Z0-9_]*)=(.*)", line)
            assert m, f"not a variable line: {line!r}"
            assert m.group(2) == "", f"{m.group(1)} has a value"
            seen[m.group(1)] = m.group(2)
    assert set(seen) == ENV_NAMES, f"names: {sorted(seen)}"
    for forbidden in ("GH_TOKEN", "GITHUB_TOKEN"):
        assert forbidden not in text, f"env.example names {forbidden}"


def check_runbook(p: Path) -> None:  # 55
    text = (p / "README.md").read_text()
    assert len(text.rstrip("\n").split("\n")) <= RUNBOOK_BUDGET, "the runbook is over its line budget"
    parts = {
        r"service user": ("staff", "_chhermes", "dscl"),
        r"Directories, owners and modes": ("Owner:group", "2750", "2770", "1770", "640"),
        r"Install": ("visudo -cf", "install -o root", "config.yaml", ".env", "LaunchAgent", "gh repo clone"),
        r"publish token": ("366", "600", "one repository", "Contents", "Pull requests"),
        r"ruleset": ("restrict deletions", "block force pushes", "require a pull request", "`verify`"),
        r"Coding Harness spike part": ("CH-1", "CH-8"),
        r"first run by hand": ("--dry-run", "check-ruleset"),
        r"After a tag change": ("CORE_TOOLSETS",),
        r"Removal": ("dscl . -delete",),
        r"What is shared": ("Never shared",),
    }
    for heading, needles in parts.items():
        body = section(text, heading)
        for needle in needles:
            assert needle in body, f"the section on {heading!r} lacks {needle!r}"


SPIKE_ITEMS = {
    "1": ("execute_code", "Delegate", "memory", "skill", "web_search", "patch"),
    "2": ("HERMES_WRITE_SAFE_ROOT", "outside", "note.md"),
    "3": ("$HOME", "_hspike", "spike-vault", "Permission denied"),
    "4": ("config.yaml", ".env", "mv", "rm"),
    "5": ("glm-5.3", "llm", "proxy", "netz.log"),
    "6": ("web_search", "web_extract", "route: web"),
    "7": ("MEMORY.md", "USER.md", "skills"),
    "8": ("dry-run", "ls-remote"),
}


def check_spike_part(p: Path) -> None:  # 56
    text = (p / "README.md").read_text()
    spike = section(text, r"Coding Harness spike part")
    heads = re.findall(r"^### CH-(\d+) · ", spike, re.M)
    assert heads == [str(n) for n in range(1, 9)], f"CH tests found: {heads}"
    for number, body in zip(heads, re.split(r"^### CH-\d+ · .*$", spike, flags=re.M)[1:], strict=True):
        assert "**Green when:**" in body, f"CH-{number} has no green condition"
        for needle in SPIKE_ITEMS[number]:
            assert needle in body, f"CH-{number} lacks {needle!r}"
    results = section(text, r"Spike results")
    rows = [r for r in results.split("\n") if r.startswith("|")]
    assert rows[0].replace(" ", "") == "|Test|Source|Date|Result|", rows[:1]
    for row in rows[2:]:
        assert [c.strip() for c in row.strip("|").split("|")][-1] in {"green", "red", "open"}, row


# ---------------------------------------------------------------------------
# The real tests, one per criterion
# ---------------------------------------------------------------------------


def test_every_core_toolset_but_web_file_search_is_disabled():
    check_toolsets(PROFILE)


def test_learning_is_off():
    check_learning_off(PROFILE)


def test_approvals_deny_and_block_git_gh_bd():
    check_approvals(PROFILE)


def test_model_route_and_every_named_model_is_declared():
    check_model_route(PROFILE)


def test_web_backend_and_switches():
    check_web(PROFILE)


def test_every_config_key_has_a_named_source_and_the_unread_ones_are_marked():
    check_key_sources(PROFILE)


def test_wrapper_flags_environment_and_alarm():
    check_wrapper_text(PROFILE)
    check_wrapper_environment(PROFILE)
    check_wrapper_alarm(PROFILE)
    check_wrapper_refusals(PROFILE)


def test_launch_agent_is_weekly_and_nothing_starts_a_gateway():
    check_launchd(PROFILE)


def test_sudo_rule_allows_one_command():
    check_sudoers(PROFILE)


def test_no_adhd_relief_identity_in_the_profile_files():
    check_no_adhd_identity(PROFILE)


def test_env_example_names_only():
    check_env_example(PROFILE)


def test_runbook_has_its_parts():
    check_runbook(PROFILE)


def test_spike_part_has_eight_tests():
    check_spike_part(PROFILE)


# ---------------------------------------------------------------------------
# The counterparts: one fault planted at a time in a copy, and the check that holds it goes red
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Fault:
    name: str
    file: str
    mutate: Callable[[str], str]
    check: Callable[[Path], None]


def sub(old: str, new: str) -> Callable[[str], str]:
    def mutate(text: str) -> str:
        assert old in text, f"{old!r} is not in the file"
        return text.replace(old, new, 1)

    return mutate


def cfg(change: Callable[[dict], None]) -> Callable[[str], str]:
    def mutate(text: str) -> str:
        data = yaml.safe_load(text)
        change(data)
        return yaml.safe_dump(data, sort_keys=False)

    return mutate


def drop_patterns(*patterns: str) -> Callable[[dict], None]:
    def change(data: dict) -> None:
        data["approvals"]["deny"] = [x for x in data["approvals"]["deny"] if x not in patterns]

    return change


def set_key(dotted: str, value) -> Callable[[dict], None]:
    def change(data: dict) -> None:
        *path, last = dotted.split(".")
        node = data
        for part in path:
            node = node.setdefault(part, {})
        if value is MISSING:
            node.pop(last)
        else:
            node[last] = value

    return change


def drop_toolset(name: str) -> Callable[[dict], None]:
    return lambda data: data["agent"]["disabled_toolsets"].remove(name)


def add_toolset(name: str) -> Callable[[dict], None]:
    return lambda data: data["agent"]["disabled_toolsets"].append(name)


CFG, WRAP, PLIST, SUDO, ENV, README = (
    "config.yaml",
    "recheck-agent.sh",
    "ai.coding-harness.research-recheck.plist",
    "sudoers",
    "env.example",
    "README.md",
)

FAULTS = [
    # 45
    Fault("45 terminal is not disabled", CFG, cfg(drop_toolset("terminal")), check_toolsets),
    Fault("45 the last core toolset is not disabled", CFG, cfg(drop_toolset("yuanbao")), check_toolsets),
    Fault("45 web is disabled", CFG, cfg(add_toolset("web")), check_toolsets),
    Fault("45 search is disabled", CFG, cfg(add_toolset("search")), check_toolsets),
    Fault("45 a name that is no toolset", CFG, cfg(add_toolset("terminl")), check_toolsets),
    # 46
    Fault("46 memory on", CFG, cfg(set_key("memory.memory_enabled", True)), check_learning_off),
    Fault("46 user profile on", CFG, cfg(set_key("memory.user_profile_enabled", True)), check_learning_off),
    Fault(
        "46 background review on", CFG, cfg(set_key("auxiliary.background_review.enabled", True)), check_learning_off
    ),
    Fault(
        "46 title generation absent",
        CFG,
        cfg(set_key("auxiliary.title_generation.enabled", MISSING)),
        check_learning_off,
    ),
    Fault("46 curator on", CFG, cfg(set_key("curator.enabled", True)), check_learning_off),
    # 47
    Fault("47 approvals off", CFG, cfg(set_key("approvals.mode", "off")), check_approvals),
    Fault("47 cron mode approve", CFG, cfg(set_key("approvals.cron_mode", "approve")), check_approvals),
    Fault("47 single query mode approve", CFG, cfg(set_key("approvals.single_query_mode", "approve")), check_approvals),
    Fault("47 unattended mode absent", CFG, cfg(set_key("approvals.unattended_mode", MISSING)), check_approvals),
    Fault("47 no gh pattern", CFG, cfg(drop_patterns("gh", "gh *")), check_approvals),
    Fault("47 git arguments not denied", CFG, cfg(drop_patterns("git *")), check_approvals),
    Fault("47 no bd pattern", CFG, cfg(drop_patterns("bd", "bd *", "*tools/bd*")), check_approvals),
    Fault("47 tools/bd by path not denied", CFG, cfg(drop_patterns("bd *", "*tools/bd*")), check_approvals),
    # 48
    Fault("48 provider custom", CFG, cfg(set_key("model.provider", "custom")), check_model_route),
    Fault("48 another model", CFG, cfg(set_key("model.default", "glm-5.2")), check_model_route),
    Fault(
        "48 base url off the proxy",
        CFG,
        cfg(set_key("model.base_url", "https://opencode.ai/zen/go/v1")),
        check_model_route,
    ),
    Fault("48 a fallback provider", CFG, cfg(set_key("fallback_providers", ["openrouter"])), check_model_route),
    Fault(
        "48 compression on an undeclared model",
        CFG,
        cfg(set_key("auxiliary.compression.model", "glm-5")),
        check_model_route,
    ),
    Fault("48 an undeclared delegation model", CFG, cfg(set_key("delegation.model", "kimi-k2.5")), check_model_route),
    Fault(
        "48 compression on another provider",
        CFG,
        cfg(set_key("auxiliary.compression.provider", "openrouter")),
        check_model_route,
    ),
    Fault(
        "48 an auxiliary base url off the proxy",
        CFG,
        cfg(set_key("auxiliary.compression.base_url", "https://example.org/v1")),
        check_model_route,
    ),
    # 49
    Fault("49 web backend exa", CFG, cfg(set_key("web.backend", "exa")), check_web),
    Fault("49 keyless fallback on", CFG, cfg(set_key("web.keyless_fallback", True)), check_web),
    Fault("49 agent scheduling on", CFG, cfg(set_key("cron.allow_agent_scheduling", True)), check_web),
    Fault("49 update check on", CFG, cfg(set_key("updates.check", True)), check_web),
    Fault("49 update check absent", CFG, cfg(set_key("updates.check", MISSING)), check_web),
    # sources
    Fault("src a key with no source", CFG, sub("memory:\n", "memory:\n  nudge_interval: 10\n"), check_key_sources),
    Fault(
        "src a baseline-only key not marked",
        CFG,
        sub("check: false                               # not read at the tag (baseline only)", "check: false"),
        check_key_sources,
    ),
    Fault("src the runbook does not list a key", README, sub("`updates.check`", "`updates.checks`"), check_key_sources),
    # 50
    Fault("50 no --ignore-rules", WRAP, sub(" --ignore-rules", ""), check_wrapper_text),
    Fault("50 a third toolset", WRAP, sub("--toolsets web,file", "--toolsets web,file,terminal"), check_wrapper_text),
    Fault("50 --yolo", WRAP, sub("--ignore-rules", "--ignore-rules --yolo"), check_wrapper_text),
    Fault("50 --worktree", WRAP, sub("--ignore-rules", "--ignore-rules --worktree"), check_wrapper_text),
    Fault(
        "50 no --max-turns",
        WRAP,
        sub('    --max-turns "$MAX_TURNS" --source tool', "    --source tool"),
        check_wrapper_text,
    ),
    Fault("50 no stream-json", WRAP, sub(" --format stream-json", ""), check_wrapper_text),
    Fault("50 no --query-file", WRAP, sub("--query-file", "--query"), check_wrapper_text),
    Fault("50 no --oneshot", WRAP, sub("chat --oneshot", "chat"), check_wrapper_text),
    Fault(
        "50 another HERMES_HOME",
        WRAP,
        sub('HERMES_HOME="$SERVICE_HOME/.hermes"', 'HERMES_HOME="$HOME/.hermes"'),
        check_wrapper_text,
    ),
    Fault("50 no write root", WRAP, sub('    HERMES_WRITE_SAFE_ROOT="$run_dir/work" \\\n', ""), check_wrapper_text),
    Fault(
        "50 no alarm", WRAP, sub("perl -e 'alarm shift; exec @ARGV' \"$CAP_SECONDS\" \\\n    ", ""), check_wrapper_text
    ),
    Fault("50 alarm of two hours", WRAP, sub("CAP_SECONDS=2700", "CAP_SECONDS=7200"), check_wrapper_text),
    Fault(
        "50 HERMES_BIN set twice",
        WRAP,
        sub("MAX_TURNS=60", "MAX_TURNS=60\nHERMES_BIN=/usr/local/bin/hermes"),
        check_wrapper_text,
    ),
    Fault("50 environment not scrubbed", WRAP, sub("exec env -i", "exec env"), check_wrapper_environment),
    Fault("50 no umask", WRAP, sub("umask 002", "true"), check_wrapper_environment),
    Fault("50 not in the work directory", WRAP, sub('cd "$run_dir/work"', "true"), check_wrapper_environment),
    Fault(
        "50 no write root (run)",
        WRAP,
        sub('    HERMES_WRITE_SAFE_ROOT="$run_dir/work" \\\n', ""),
        check_wrapper_environment,
    ),
    Fault("50 alarm never fires", WRAP, sub("alarm shift", "alarm 0*shift"), check_wrapper_alarm),
    Fault(
        "50 any run directory accepted",
        WRAP,
        sub('*) echo "recheck-agent: refusing a run directory outside $RUNS_ROOT" >&2; exit 2 ;;', "*) ;;"),
        check_wrapper_refusals,
    ),
    Fault("50 '..' accepted", WRAP, sub("*..*)", "*XX*)"), check_wrapper_refusals),
    # 51
    Fault("51 KeepAlive", PLIST, sub("<key>Label</key>", "<key>KeepAlive</key><true/><key>Label</key>"), check_launchd),
    Fault("51 daily, no weekday", PLIST, sub("    <key>Weekday</key>\n    <integer>0</integer>\n", ""), check_launchd),
    Fault(
        "51 Monday",
        PLIST,
        sub("<key>Weekday</key>\n    <integer>0</integer>", "<key>Weekday</key>\n    <integer>1</integer>"),
        check_launchd,
    ),
    Fault(
        "51 monthly",
        PLIST,
        sub("<key>Hour</key>", "<key>Day</key>\n    <integer>1</integer>\n    <key>Hour</key>"),
        check_launchd,
    ),
    Fault(
        "51 run at load", PLIST, sub("<key>Label</key>", "<key>RunAtLoad</key><true/><key>Label</key>"), check_launchd
    ),
    Fault(
        "51 every hour",
        PLIST,
        sub("<key>Label</key>", "<key>StartInterval</key><integer>3600</integer><key>Label</key>"),
        check_launchd,
    ),
    Fault("51 a gateway", PLIST, sub("<string>run</string>", "<string>gateway</string>"), check_launchd),
    Fault("51 no --notify", PLIST, sub("    <string>--notify</string>\n", ""), check_launchd),
    Fault(
        "51 another working directory",
        PLIST,
        sub(
            "<key>WorkingDirectory</key>\n  <string>@HOME@/Library/Application Support/coding-harness-recheck/clone</string>",
            "<key>WorkingDirectory</key>\n  <string>/tmp</string>",
        ),
        check_launchd,
    ),
    Fault("51 a gateway in the wrapper", WRAP, sub("# Standard output", "# gateway\n# Standard output"), check_launchd),
    # 52
    Fault("52 a second command", SUDO, sub("recheck-agent\n", "recheck-agent, /bin/sh\n"), check_sudoers),
    Fault(
        "52 ALL as the command",
        SUDO,
        sub("NOPASSWD: /usr/local/libexec/coding-harness/recheck-agent", "NOPASSWD: ALL"),
        check_sudoers,
    ),
    Fault("52 target root", SUDO, sub("(_chhermes)", "(root)"), check_sudoers),
    Fault("52 target ALL", SUDO, sub("(_chhermes)", "(ALL)"), check_sudoers),
    Fault("52 a password is asked", SUDO, sub("NOPASSWD: ", ""), check_sudoers),
    Fault("52 a second rule", SUDO, lambda t: t + "@MAINTAINER@ ALL=(ALL) ALL\n", check_sudoers),
    # 53
    Fault(
        "53 adhd-relief's user in the config",
        CFG,
        sub("# No secret belongs", "# user _hspike\n# No secret belongs"),
        check_no_adhd_identity,
    ),
    Fault(
        "53 adhd-relief's home in the wrapper",
        WRAP,
        sub("# The service user may not", "# /Users/_hspike/.hermes\n# The service user may not"),
        check_no_adhd_identity,
    ),
    Fault(
        "53 adhd-relief's write root in the plist",
        PLIST,
        sub("<key>Label</key>", "<key>Spike</key><string>/Users/Shared/spike-vault</string><key>Label</key>"),
        check_no_adhd_identity,
    ),
    Fault(
        "53 adhd-relief's user in the sudo rule",
        SUDO,
        sub("# @MAINTAINER@ stands for", "# _hspike\n# @MAINTAINER@ stands for"),
        check_no_adhd_identity,
    ),
    Fault(
        "53 adhd-relief's home in the env template",
        ENV,
        sub("# Template", "# /Users/_hspike\n# Template"),
        check_no_adhd_identity,
    ),
    # 54
    Fault("54 a value", ENV, sub("OPENCODE_GO_API_KEY=", "OPENCODE_GO_API_KEY=sk-123"), check_env_example),
    Fault("54 a missing name", ENV, sub("FIRECRAWL_API_URL=", "# FIRECRAWL_API_URL"), check_env_example),
    Fault("54 GH_TOKEN", ENV, lambda t: t + "GH_TOKEN=\n", check_env_example),
    Fault("54 GITHUB_TOKEN in a comment", ENV, lambda t: t + "# GITHUB_TOKEN\n", check_env_example),
    Fault("54 a fifth variable", ENV, lambda t: t + "OPENROUTER_API_KEY=\n", check_env_example),
    # 55
    Fault("55 no staff", README, lambda t: t.replace("staff", "wheel"), check_runbook),
    Fault("55 no modes", README, lambda t: t.replace("2770", "x"), check_runbook),
    Fault("55 no expiry", README, lambda t: t.replace("366", "x"), check_runbook),
    Fault("55 no token mode", README, lambda t: t.replace("chmod 600", "chmod"), check_runbook),
    Fault("55 no ruleset rule", README, lambda t: t.replace("block force pushes", "x"), check_runbook),
    Fault("55 no visudo", README, lambda t: t.replace("visudo -cf", "visudo"), check_runbook),
    Fault("55 no dry run", README, lambda t: t.replace("--dry-run", "x"), check_runbook),
    Fault(
        "55 no shared section",
        README,
        lambda t: t.replace("## 1 · What is shared with adhd-relief, and what never is", "## 1 · x"),
        check_runbook,
    ),
    Fault("55 no removal", README, lambda t: t.replace("## 11 · Removal", "## 11 · x"), check_runbook),
    Fault("55 over its line budget", README, lambda t: t + "x\n" * 5, check_runbook),
    # 56
    Fault("56 no CH-5", README, lambda t: t.replace("### CH-5 · ", "### CH-x · "), check_spike_part),
    Fault(
        "56 a ninth",
        README,
        lambda t: t.replace("## 9 · The first", "### CH-9 · x\n\n## 9 · The first"),
        check_spike_part,
    ),
    Fault(
        "56 CH-3 has no green condition",
        README,
        sub("**Green when:** the four denied", "the four denied"),
        check_spike_part,
    ),
    Fault("56 CH-2 forgets the boundary", README, lambda t: t.replace("outside", "x"), check_spike_part),
    Fault("56 CH-6 forgets the route", README, sub("`route: web`", "`x`"), check_spike_part),
    Fault("56 a result of maybe", README, lambda t: t + "| CH-1 | x | 2026-10-06 | maybe |\n", check_spike_part),
    Fault(
        "56 the table lost a column",
        README,
        sub("| Test | Source | Date | Result |", "| Test | Source | Date |"),
        check_spike_part,
    ),
]


@pytest.mark.parametrize("fault", FAULTS, ids=[f.name for f in FAULTS])
def test_a_planted_fault_goes_red(fault: Fault, tmp_path: Path):
    copy = tmp_path / "hermes"
    shutil.copytree(PROFILE, copy)
    fault.check(copy)  # silent before the fault
    target = copy / fault.file
    before = target.read_text()
    after = fault.mutate(before)
    assert after != before, "the fault changed nothing"
    target.write_text(after)
    with pytest.raises(AssertionError):
        fault.check(copy)
