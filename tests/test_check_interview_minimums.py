"""The counterexample matrix of plans/changes/archive/2026-10-08-interview-minimums/spec.md.

Each acceptance criterion gets the test that holds it and the fault that
would refute it (plan.md, "Per acceptance criterion, the test"). The tree
fixtures are real git repositories with a bare remote, because the gate
reads diff states — committed, staged, unstaged and untracked — and derives
its base per context (decisions.md Q-7). Counting fixtures are dated after
the cut-off constant, so the gate measures them; the stock tests use the
cut-off day and before.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


def _git_env() -> dict[str, str]:
    """Git configuration isolated from the maintainer's machine: no global or
    system config, so inherited commit signing cannot break the seed commits
    (phase-6 row F-19 — the review run lost 23 fixtures to a signer that was
    not available)."""
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    return env


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_interview_minimums.py"
REPO = Path(__file__).resolve().parent.parent
FUTURE = "2026-10-09"  # later than CUTOFF in the gate — measured
CUTOFF_DAY = "2026-10-08"  # the cut-off day itself — exempt (Q-8)
BEFORE = "2026-10-07"  # older stock — exempt


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True, env=_git_env())
    return done.stdout.strip()


def _commit_all(cwd: Path, message: str) -> None:
    _git(cwd, "add", "-A")
    _git(cwd, "commit", "-m", message)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A clone of a bare origin, seeded on main, work continued on a branch."""
    origin = tmp_path / "origin.git"
    subprocess.run(
        ["git", "init", "--bare", "-b", "main", str(origin)],
        check=True,
        capture_output=True,
        env=_git_env(),
    )
    work = tmp_path / "work"
    subprocess.run(["git", "clone", str(origin), str(work)], check=True, capture_output=True, env=_git_env())
    _git(work, "config", "user.email", "test@example.com")
    _git(work, "config", "user.name", "Gate Tests")
    (work / "README.md").write_text("seed\n")
    _commit_all(work, "seed")
    _git(work, "push", "origin", "main")
    _git(work, "checkout", "-b", "feat/test")
    return work


def write_change(
    work: Path,
    name: str,
    klass: str,
    day: str = FUTURE,
    decisions: str = "",
) -> Path:
    folder = work / "plans" / "changes" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "spec.md").write_text(
        "---\n"
        f'title: "Spec — {name}"\n'
        "status: draft\n"
        "implementation_status: none\n"
        f"date: {day}\n"
        f"last_reviewed: {day}\n"
        "bead: coding-harness-test\n"
        f"class: {klass}\n"
        "---\n"
        f"\n# Spec — {name}\n"
    )
    if decisions:
        (folder / "decisions.md").write_text(decisions)
    return folder


def records(count: int, **overrides: str) -> str:
    """`count` distinct counted records; overrides apply to every block."""
    blocks = []
    for n in range(1, count + 1):
        fields = {
            "asked": FUTURE,
            "answer": "ok",
            "answered_by": "maintainer",
            "status": "answered",
            **overrides,
        }
        body = "\n".join(f"{key}: {value}" for key, value in fields.items())
        blocks.append(f"## Q-{n} · question {n}\n\n{body}\n\nY-statement. — {FUTURE}\n")
    return "\n".join(blocks)


SKIP = f"## SKIP · interview\n\nstatus: skipped\nreason: the assignment settles every open question. — {FUTURE}\n"


def run_gate(work: Path, *args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.pop("GITHUB_REF", None)  # a test sets the main-line env explicitly
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(work), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


# --- AC 1 · the feature minimum -------------------------------------------


def test_feature_with_too_few_answers_is_found(repo: Path) -> None:
    write_change(repo, "thin", "feature", decisions=records(2))
    done = run_gate(repo)
    assert done.returncode == 1
    assert "thin" in done.stdout


def test_feature_with_three_answers_passes(repo: Path) -> None:
    write_change(repo, "enough", "feature", decisions=records(3))
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_the_gate_goes_red_when_a_feature_skips_its_interview(repo: Path) -> None:
    """Mutation evidence for scripts/check_interview_minimums.py: a fault that
    stopped counting the maintainer's answers — dropping a record, accepting an
    agent's answer as a human's, merging duplicate ids — silences this run."""
    write_change(repo, "mutation", "feature", decisions=records(2))
    done = run_gate(repo)
    assert done.returncode == 1
    assert "mutation" in done.stdout
    assert "2 of 3" in done.stdout


# --- AC 4 · what does not count -------------------------------------------


def test_agent_open_and_duplicate_records_do_not_count(repo: Path) -> None:
    body = (
        records(1)
        + records(1, answered_by="agent").replace("Q-1", "Q-2")
        + records(1, status="open").replace("Q-1", "Q-3")
        + records(1)  # an exact repeat of the first id (Q-5: ignored)
    )
    write_change(repo, "gamed", "feature", decisions=body)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "1 of 3" in done.stdout


# --- AC 2 · the ADR minimum, in every diff state ---------------------------


def _stage_adr(work: Path, commit: bool = False) -> None:
    adr = work / "docs" / "adr" / "0099-test-decision.md"
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0099 — test\n")
    if commit:
        _commit_all(work, "docs: an adr")


def test_adr_change_demands_five_regardless_of_class(repo: Path) -> None:
    write_change(repo, "bounded-adr", "bounded", decisions=records(4))
    _stage_adr(repo)
    _git(repo, "add", "-A")  # staged only — never committed
    done = run_gate(repo)
    assert done.returncode == 1
    assert "bounded-adr" in done.stdout and "5" in done.stdout


def test_adr_change_with_five_counted_passes(repo: Path) -> None:
    write_change(repo, "bounded-adr-five", "bounded", decisions=records(5))
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_untracked_adr_path_is_seen(repo: Path) -> None:
    write_change(repo, "untracked-adr", "bounded", decisions=records(4))
    adr = repo / "docs" / "adr" / "0098-untracked.md"
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0098\n")  # neither staged nor committed
    done = run_gate(repo)
    assert done.returncode == 1
    assert "untracked-adr" in done.stdout


def test_unstaged_adr_path_is_seen(repo: Path) -> None:
    write_change(repo, "unstaged-adr", "bounded", decisions=records(4))
    _stage_adr(repo, commit=False)
    _git(repo, "add", "docs/adr/0099-test-decision.md")
    (repo / "docs" / "adr" / "0099-test-decision.md").write_text("# ADR 0099 — edited\n")
    done = run_gate(repo)  # the edit is neither staged nor committed
    assert done.returncode == 1


def test_committed_adr_path_is_seen(repo: Path) -> None:
    write_change(repo, "committed-adr", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    done = run_gate(repo)
    assert done.returncode == 1


def test_adr_outside_any_change_is_a_finding(repo: Path) -> None:
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "owns 0 change folder(s)" in done.stdout


def test_adr_with_two_owning_changes_is_a_finding(repo: Path) -> None:
    write_change(repo, "owner-a", "bounded", decisions=records(5))
    write_change(repo, "owner-b", "feature", decisions=records(3))
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "owns 2 change folder(s)" in done.stdout


# --- AC 3 · feature with ADR: five in total, never the sum -----------------


def test_feature_with_adr_needs_five_not_eight(repo: Path) -> None:
    write_change(repo, "feature-adr", "feature", decisions=records(5))
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    write_change(repo, "feature-adr", "feature", decisions=records(4))
    done = run_gate(repo)
    assert done.returncode == 1


# --- AC 5 · bounded one-or-skip, spike three-or-skip -----------------------


def test_bounded_empty_file_is_found(repo: Path) -> None:
    write_change(repo, "silent", "bounded")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "silent" in done.stdout


def test_bounded_with_one_record_or_reasoned_skip_passes(repo: Path) -> None:
    write_change(repo, "one-answer", "bounded", decisions=records(1))
    assert run_gate(repo).returncode == 0
    write_change(repo, "one-answer", "bounded", decisions=SKIP)
    assert run_gate(repo).returncode == 0


def test_bounded_skip_without_reason_is_no_skip(repo: Path) -> None:
    write_change(
        repo,
        "hollow-skip",
        "bounded",
        decisions=SKIP.replace(
            "reason: the assignment settles every open question. — " + FUTURE,
            "reason:",
        ),
    )
    done = run_gate(repo)
    assert done.returncode == 1


def test_spike_three_topics_or_skip(repo: Path) -> None:
    write_change(repo, "spike-full", "spike", decisions=records(3))
    assert run_gate(repo).returncode == 0
    write_change(repo, "spike-full", "spike", decisions=records(2))
    assert run_gate(repo).returncode == 1
    write_change(repo, "spike-full", "spike", decisions=SKIP)
    assert run_gate(repo).returncode == 0


# --- AC 7 · the base rule per context --------------------------------------


def test_worktree_branch_uses_merge_base(repo: Path) -> None:
    # Committed on a feature branch: only a merge-base diff sees the ADR.
    write_change(repo, "on-branch", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "on-branch" in done.stdout


def test_main_checkout_uses_first_parent(repo: Path) -> None:
    # main's landfall: the branch itself says main, so the first parent is
    # the base and the merged change is measured.
    write_change(repo, "merged-in", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    _git(repo, "checkout", "main")
    (repo / "README.md").write_text("unrelated main work\n")
    _commit_all(repo, "docs: main moves on")
    _git(repo, "merge", "--no-ff", "feat/test", "-m", "merge the feature")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "merged-in" in done.stdout


def test_hosted_main_line_run_uses_first_parent(repo: Path) -> None:
    # Loop row L1-2: the hosted run that pushed main checks out a detached
    # HEAD — the branch name cannot speak, the main-line env does.
    write_change(repo, "merged-detached", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    _git(repo, "checkout", "main")
    (repo / "README.md").write_text("unrelated main work\n")
    _commit_all(repo, "docs: main moves on")
    _git(repo, "merge", "--no-ff", "feat/test", "-m", "merge the feature")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "--detach", "origin/main")
    done = run_gate(repo, env_extra={"GITHUB_REF": "refs/heads/main"})
    assert done.returncode == 1
    assert "merged-detached" in done.stdout


def test_detached_at_tip_without_main_line_env_is_not_measured(repo: Path) -> None:
    # Phase-6 rows F-13/F-14: detached at origin/main — the committed delta
    # since the base cannot be delimited, so the gate refuses (exit 3)
    # instead of guessing green or replaying an older landfall.
    write_change(repo, "detached-work", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    _git(repo, "checkout", "main")
    _git(repo, "merge", "--no-ff", "feat/test", "-m", "merge the feature")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "--detach", "origin/main")
    done = run_gate(repo)
    assert done.returncode == 3
    assert "NOT MEASURED" in done.stdout


def test_new_branch_at_tip_is_not_charged_main_landfall(repo: Path) -> None:
    # Phase-6 row F-15: main's previous landfall carried an ADR; a newly
    # begun branch at that tip with its own three answers and no ADR edits
    # must stay green — no replay of the old landfall.
    write_change(repo, "landfall", "bounded", decisions=records(5))
    _stage_adr(repo, commit=True)
    _git(repo, "checkout", "main")
    _git(repo, "merge", "--no-ff", "feat/test", "-m", "landfall")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "-b", "feat/fresh")
    write_change(repo, "fresh", "feature", decisions=records(3))
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


# --- AC 6 · unmeasurable is exit 3, never green ----------------------------


def test_unmeasurable_tree_exits_three(tmp_path: Path) -> None:
    lonely = tmp_path / "lonely"
    lonely.mkdir()
    _git(lonely, "init", "-b", "feature/nowhere")
    _git(lonely, "config", "user.email", "test@example.com")
    _git(lonely, "config", "user.name", "Gate Tests")
    write_change(lonely, "unmeasured", "feature", decisions=records(1))
    _commit_all(lonely, "a change without an origin")
    done = run_gate(lonely)  # no origin/main: no merge base, not on main
    assert done.returncode == 3
    assert "NOT MEASURED" in done.stdout


# --- AC 8 · the cut-off -----------------------------------------------------


def test_cutoff_excludes_same_day_and_older(repo: Path) -> None:
    write_change(repo, "same-day", "feature", day=CUTOFF_DAY)  # no decisions at all
    write_change(repo, "older", "feature", day=BEFORE)
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    write_change(repo, "next-day", "feature", day=FUTURE)  # empty decisions
    done = run_gate(repo)
    assert done.returncode == 1
    assert "next-day" in done.stdout
    assert "same-day" not in done.stdout and "older" not in done.stdout


# --- phase 6 · the counterexamples of rows F-10 to F-18 ---------------------


def test_quoted_date_does_not_exempt(repo: Path) -> None:
    # F-10: a quoted or commented date is valid YAML — it must not silently
    # exempt a subject change.
    folder = write_change(repo, "quoted", "feature")  # empty decisions
    spec = folder / "spec.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace(f"date: {FUTURE}", f'date: "{FUTURE}"  # noted'))
    done = run_gate(repo)
    assert done.returncode == 1
    assert "quoted" in done.stdout


def test_archived_post_cutoff_feature_is_measured(repo: Path) -> None:
    # F-11: normal completion and archival must not bypass the feature
    # minimum — the cut-off decides, not the folder's place.
    write_change(repo, "archived-late", "feature")  # empty decisions
    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "archived-late").rename(archive / f"{FUTURE}-archived-late")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "archived-late" in done.stdout


def test_minimal_blocks_are_not_interview_records(repo: Path) -> None:
    # F-12: blocks that carry only answered_by and status — no question, no
    # answer — count for nothing.
    body = (
        "## Q-1 · a\n\nanswered_by: maintainer\nstatus: answered\n\n"
        "## Q-2 · b\n\nanswered_by: maintainer\nstatus: answered\n\n"
        "## Q-3 · c\n\nanswered_by: maintainer\nstatus: answered\n"
    )
    write_change(repo, "hollow", "feature", decisions=body)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "hollow" in done.stdout


def test_index_only_staged_adr_is_seen(repo: Path) -> None:
    # F-16, fixture per PR review P2-3: the original ADR must live in the
    # comparison base — committed on main, pushed, then merged into this
    # branch — so the staged edit (working file restored to the base) is
    # visible to the index diff alone. Building it on the branch would make
    # the ADR an addition of the working-tree diff and the test vacuous.
    _git(repo, "checkout", "main")
    adr = repo / "docs" / "adr" / "0097-earlier.md"
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0097 — original\n")
    _commit_all(repo, "docs: an adr on main")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "feat/test")
    _git(repo, "merge", "main", "-m", "sync main into the branch")
    write_change(repo, "index-adr", "bounded", decisions=records(4))
    adr.write_text("# ADR 0097 — changed\n")
    _git(repo, "add", "docs/adr/0097-earlier.md")
    adr.write_text("# ADR 0097 — original\n")  # the working file matches the base
    done = run_gate(repo)
    assert done.returncode == 1
    assert "index-adr" in done.stdout


def test_change_flag_typo_is_red_even_when_another_change_passes(repo: Path) -> None:
    # F-17: a passing unrelated measurement must not answer for the named
    # change — a typo stays red whatever else the run measured.
    write_change(repo, "owner-ok", "bounded", decisions=records(5))
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo, "--change", "owner-ok-typo")
    assert done.returncode == 1
    assert "no change folder" in done.stdout


# --- PR review · the maintainer's three P2 rows -----------------------------


def test_renamed_away_adr_is_seen(repo: Path) -> None:
    # P2-1: `git mv` out of docs/adr/ names only the destination when rename
    # detection is on — the abandoned ADR path must still count, and the
    # bounded change with one answer must not pass.
    _git(repo, "checkout", "main")
    adr = repo / "docs" / "adr" / "0096-moved.md"
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0096\n")
    _commit_all(repo, "docs: an adr on main")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "feat/test")
    _git(repo, "merge", "main", "-m", "sync main into the branch")
    write_change(repo, "moved-adr", "bounded", decisions=records(1))
    _git(repo, "mv", "docs/adr/0096-moved.md", "docs/notes-0096.md")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "moved-adr" in done.stdout


def test_date_with_inline_comment_keeps_the_stock_exempt(repo: Path) -> None:
    # P2-2: `date: 2026-10-07 # existing stock` is valid YAML — the stock
    # change stays exempt instead of becoming interview duty.
    folder = write_change(repo, "noted-stock", "feature", day=BEFORE)  # empty decisions
    spec = folder / "spec.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace(f"date: {BEFORE}", f"date: {BEFORE}  # existing stock"))
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


# --- AC 9, 10, 11 · the spec gate, the declaration, the docs ----------------


def test_spec_prompt_names_the_interview_check() -> None:
    text = (REPO / "prompts" / "02-spec.md").read_text(encoding="utf-8")
    assert "check_interview_minimums.py" in text


def test_interview_prompt_defines_the_records() -> None:
    text = (REPO / "prompts" / "01a-interview.md").read_text(encoding="utf-8")
    assert "answered_by" in text and "status: skipped" in text
    assert "## SKIP · interview" in text


def test_workflow_and_agents_state_the_duty() -> None:
    # F-20: the assertions must fail against the original AGENTS.md that
    # called the interview optional — "three stages" in the introduction is
    # not evidence of the duty.
    workflow = (REPO / "docs" / "WORKFLOW.md").read_text(encoding="utf-8")
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "interview-minimums" in workflow
    assert "2026-10-08" in workflow  # the cut-off, dated
    assert "interview-minimums" in agents
    assert "optional, human-called" not in agents
    assert "≥ 3" in agents and "≥ 5" in agents


def test_gates_yaml_declares_interview_minimums() -> None:
    """Deleting the gate entry from decisions/gates.yaml turns this red —
    the refutation AC 10 demands beside `ci-drift`."""
    gates = yaml.safe_load((REPO / "decisions" / "gates.yaml").read_text(encoding="utf-8"))
    entries = [g for g in gates["gates"] if g.get("id") == "interview-minimums"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["job"] == "verify"
    assert entry["enforcement"] == "block"
    assert entry["placement"] == "both"
    assert entry["command"] == "python3 scripts/check_interview_minimums.py"


# --- review-loop round 1 ----------------------------------------------------


def test_earlier_uncounted_record_does_not_spend_the_id(repo: Path) -> None:
    # L1-1: Q-1 answered by the agent first, by the maintainer second — the
    # maintainer's answer counts; an uncounted earlier record spends nothing.
    body = (
        records(1, answered_by="agent")
        + records(1)
        + records(1).replace("Q-1", "Q-2")
        + records(1).replace("Q-1", "Q-3")
    )
    write_change(repo, "l11", "feature", decisions=body)
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_detached_at_merged_tip_uses_first_parent(repo: Path) -> None:
    # L1-2: hosted CI checks out a detached HEAD; on the post-merge push the
    # merge base equals HEAD and an empty diff would silence the ADR duty.
    write_change(repo, "merged-detached", "bounded", decisions=records(4))
    _stage_adr(repo, commit=True)
    _git(repo, "checkout", "main")
    (repo / "README.md").write_text("unrelated main work\n")
    _commit_all(repo, "docs: main moves on")
    _git(repo, "merge", "--no-ff", "feat/test", "-m", "merge the feature")
    _git(repo, "checkout", "--detach", "HEAD")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "merged-detached" in done.stdout


def test_adr_edit_in_a_stock_folder_still_owes_five(repo: Path) -> None:
    # L1-3: the cut-off exempts a folder's own class minimums, never a new
    # ADR edit — the owner owes five whatever its spec date.
    write_change(repo, "old-folder", "bounded", day=BEFORE, decisions=records(4))
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "old-folder" in done.stdout and "ADR change" in done.stdout


def test_change_flag_with_unknown_name_is_found(repo: Path) -> None:
    # L1-6: the spec gate must not pass on a typo.
    write_change(repo, "real", "feature", decisions=records(3))
    done = run_gate(repo, "--change", "real-typo")
    assert done.returncode == 1
    assert "no change folder" in done.stdout


# --- the ADR owner: a plan-only folder is a migration, not an owner ---------


def test_a_folder_whose_diff_touches_only_plan_md_is_no_owner(repo: Path) -> None:
    """The ledger migration of change criterion-test-ledger (2026-10-11): one
    ADR draft lands beside four migrated plans, and the diff then touches five
    change folders. Only a folder that carries more than plan.md counts as the
    owner, so the five answers answer for exactly one. Mutation evidence for
    scripts/check_interview_minimums.py: counting the plan-only folder again
    turns this run red with "owns 2 change folder(s)"."""
    write_change(repo, "real", "bounded", decisions=records(5))
    _stage_adr(repo)
    # the ADR names its owner, the one means the interim rule reads (row L3-1)
    (repo / "docs" / "adr" / "0099-test-decision.md").write_text("# ADR 0099 — test\n\nChange: real\n")
    migrated = repo / "plans" / "changes" / "migrated"
    migrated.mkdir(parents=True)
    (migrated / "plan.md").write_text("# Plan\n\n## Criterion ledger\n\n- 1: not a test — review\n")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    assert "owns 2 change folder(s)" not in done.stdout


def test_an_adr_with_only_its_own_plan_md_still_has_that_one_owner(repo: Path) -> None:
    """Review-loop row L2-1: the plan-only narrowing must not leave an ADR
    without an owner. A diff touching docs/adr/** and only the plan.md of its
    own change folder still owns exactly that folder, which then owes the five
    answers (here it has them, so the run is green). Fault: dropping the
    fall-back to plan-only folders in scripts/check_interview_minimums.py
    ("owns 0 change folder(s)") turns this red. The heuristic is interim; bead
    coding-harness-afa replaces it with an explicit owner statement."""
    _git(repo, "checkout", "main")
    write_change(repo, "solo", "bounded", decisions=records(5))
    _commit_all(repo, "feat: solo change with its answers")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "feat/test")
    _git(repo, "merge", "main")
    (repo / "plans" / "changes" / "solo" / "plan.md").write_text("# Plan\n")
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    assert "owns 0 change folder(s)" not in done.stdout, done.stdout


def test_a_plan_md_only_folder_does_not_hide_the_adr_owner_among_other_folders(repo: Path) -> None:
    """Review-loop row L3-1: folder A touched through decisions.md, folder B
    through plan.md alone and one ADR that names neither. The paths cannot say
    whether the ADR belongs to A or to B, so the run must not go green by
    silently picking A: it reports both candidates. Fault: dropping the
    plan-only folder whenever another folder owns (the L2-1 rule) reports one
    owner and exits 0. When the ADR text names exactly one candidate, that
    one owns it and the run is decided by its answers."""
    write_change(repo, "folder-a", "bounded", decisions=records(5))
    _stage_adr(repo)
    other = repo / "plans" / "changes" / "folder-b"
    other.mkdir(parents=True)
    (other / "plan.md").write_text("# Plan\n\nA real plan edit, not a ledger migration.\n")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout
    assert "folder-a" in done.stdout and "folder-b" in done.stdout
    assert "name the owning change folder" in done.stdout

    # the ADR names folder-b, which has no decisions.md: the owner owes five
    (repo / "docs" / "adr" / "0099-test-decision.md").write_text("# ADR 0099\n\nChange: folder-b\n")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout
    assert "folder-b" in done.stdout and "5" in done.stdout


def test_a_folder_touched_beyond_plan_md_is_never_also_plan_only(repo: Path) -> None:
    """Review-loop row F-3 (phase 6, Codex): one feature changes its spec.md,
    decisions.md and plan.md, and the ADR does not spell the folder name. The
    folder owns the ADR through spec.md and decisions.md; its plan.md must not
    also enter the plan-only set, or the ambiguity branch rejects a diff with
    five valid answers and exactly one candidate owner. Fault: leaving the
    folder in plan_only reports "cannot say which of" and exits 1."""
    folder = write_change(repo, "solo-feature", "bounded", decisions=records(5))
    (folder / "plan.md").write_text("# Plan\n\nA real plan edit.\n")
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    assert "cannot say which" not in done.stdout, done.stdout
