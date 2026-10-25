"""The counterexample matrix of plans/changes/archive/2026-10-08-interview-minimums/spec.md
and of plans/changes/adr-owning-change/spec.md (ADR 0014).

Each acceptance criterion gets the test that holds it and the fault that
would refute it (plan.md, "Per acceptance criterion, the test"). The tree
fixtures are real git repositories with a bare remote, because the gate
reads diff states — committed, staged, unstaged and untracked — and derives
its base per context (decisions.md Q-7). Counting fixtures are dated after
the adoption day their fixture repository records, so the gate measures
them; the stock tests use the adoption day and before.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import check_interview_minimums as gate  # noqa: E402


def _git_env() -> dict[str, str]:
    """Git configuration isolated from the maintainer's machine: no global or
    system config, so inherited commit signing cannot break the seed commits
    (phase-6 row F-19 — the review run lost 23 fixtures to a signer that was
    not available)."""
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    return env


SCRIPT = REPO / "scripts" / "check_interview_minimums.py"
FUTURE = "2026-10-09"  # later than the fixture's adoption day — measured
CUTOFF_DAY = "2026-10-08"  # the adoption day itself — exempt (Q-8)
BEFORE = "2026-10-07"  # older stock — exempt
ADR = "docs/adr/0099-test-decision.md"
ADOPTION = "schema_version: 1\nadopted:\n  interview-minimums: 2026-10-08\n"


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True, env=_git_env())
    return done.stdout.strip()


def _commit_all(cwd: Path, message: str) -> None:
    _git(cwd, "add", "-A")
    _git(cwd, "commit", "-m", message)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A clone of a bare origin, seeded on main with the adoption record, work
    continued on a branch."""
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
    (work / "decisions").mkdir()
    (work / "decisions" / "adoption.yaml").write_text(ADOPTION)
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
    adr_files: list[str] | None = None,
    extra_header: str = "",
) -> Path:
    folder = work / "plans" / "changes" / name
    folder.mkdir(parents=True, exist_ok=True)
    claim = "" if adr_files is None else f"adr_files: [{', '.join(adr_files)}]\n"
    (folder / "spec.md").write_text(
        "---\n"
        f'title: "Spec — {name}"\n'
        "status: draft\n"
        "implementation_status: none\n"
        f"date: {day}\n"
        f"last_reviewed: {day}\n"
        "bead: coding-harness-test\n"
        f"class: {klass}\n"
        f"{claim}"
        f"{extra_header}"
        "---\n"
        f"\n# Spec — {name}\n"
    )
    if decisions:
        (folder / "decisions.md").write_text(decisions)
    return folder


def write_answer(work: Path, name: str, answer: str, quoted: bool = True) -> None:
    folder = work / "decisions" / "answers" / name
    folder.mkdir(parents=True, exist_ok=True)
    value = f"'{answer}'" if quoted else answer
    (folder / "adr.yaml").write_text(
        "schema_version: 1\n"
        f"change: {name}\n"
        "question: adr\n"
        f"answer: {value}\n"
        "reason: Stated by the maintainer.\n"
        "shown:\n"
        f"  proposed: {value}\n"
        "  proposal_reason: Proposed.\n"
        "answered_by: framework-architect\n"
        "answered_at: 2026-10-12\n"
    )


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
    adr = work / ADR
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0099 — test\n")
    if commit:
        _commit_all(work, "docs: an adr")


def test_adr_change_demands_five_regardless_of_class(repo: Path) -> None:
    write_change(repo, "bounded-adr", "bounded", decisions=records(4), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")  # staged only — never committed
    done = run_gate(repo)
    assert done.returncode == 1
    assert "bounded-adr (ADR change): 4 of 5" in done.stdout


def test_adr_change_with_five_counted_passes(repo: Path) -> None:
    write_change(repo, "bounded-adr-five", "bounded", decisions=records(5), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_untracked_adr_path_is_seen(repo: Path) -> None:
    other = "docs/adr/0098-untracked.md"
    write_change(repo, "untracked-adr", "bounded", decisions=records(4), adr_files=[other])
    adr = repo / other
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0098\n")  # neither staged nor committed
    done = run_gate(repo)
    assert done.returncode == 1
    assert "untracked-adr (ADR change): 4 of 5" in done.stdout


def test_unstaged_adr_path_is_seen(repo: Path) -> None:
    write_change(repo, "unstaged-adr", "bounded", decisions=records(4), adr_files=[ADR])
    _stage_adr(repo, commit=False)
    _git(repo, "add", ADR)
    (repo / ADR).write_text("# ADR 0099 — edited\n")
    done = run_gate(repo)  # the edit is neither staged nor committed
    assert done.returncode == 1
    assert "unstaged-adr (ADR change): 4 of 5" in done.stdout


def test_committed_adr_path_is_seen(repo: Path) -> None:
    write_change(repo, "committed-adr", "bounded", decisions=records(4), adr_files=[ADR])
    _stage_adr(repo, commit=True)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "committed-adr (ADR change): 4 of 5" in done.stdout


def test_adr_outside_any_change_is_a_finding(repo: Path) -> None:
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert ADR in done.stdout
    assert "no change in this diff claims it" in done.stdout
    assert "adr_files" in done.stdout


def test_adr_with_two_owning_changes_is_a_finding(repo: Path) -> None:
    write_change(repo, "owner-a", "bounded", decisions=records(5), adr_files=[ADR])
    write_change(repo, "owner-b", "feature", decisions=records(5), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert f"{ADR} is claimed by owner-a, owner-b" in done.stdout
    assert "split the pull request" in done.stdout
    assert "the amendment in one" in done.stdout
    assert "drop the other claims" not in done.stdout
    assert "retire" not in done.stdout


def test_an_unreadable_claim_does_not_also_report_a_missing_one(repo: Path) -> None:
    # L2-4: one fault, one finding — the agreement check skips a feature whose
    # claim cannot be read.
    write_change(repo, "broken", "feature", decisions=records(3), extra_header="adr_files: docs/adr/0099-x.md\n")
    write_answer(repo, "broken", "yes")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "adr_files cannot be read" in done.stdout
    assert "claims no ADR file" not in done.stdout


@pytest.mark.parametrize("key", ['"adr_files"', "'adr_files'", "adr_files "])
def test_a_claim_key_in_any_yaml_spelling_is_seen(repo: Path, key: str) -> None:
    # F-2: a quoted key or a blank before the colon is the same key — a
    # malformed claim in an archived stock spec is reported, a valid one claims.
    write_change(repo, "fine", "bounded", decisions=records(1))
    write_change(repo, "stock", "feature", day=BEFORE, extra_header=f"{key}: [plans/x.md]\n")
    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "stock").rename(archive / f"{BEFORE}-stock")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout
    assert "adr_files cannot be read" in done.stdout


@pytest.mark.parametrize("key", ['"adr_files"', "adr_files "])
def test_a_claim_in_another_spelling_attributes_the_edit(repo: Path, key: str) -> None:
    write_change(repo, "spelled", "bounded", decisions=records(4), extra_header=f"{key}: [{ADR}]\n")
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "spelled (ADR change): 4 of 5" in done.stdout


def test_an_impossible_date_in_a_claiming_header_is_a_finding(repo: Path) -> None:
    # F-3: the YAML loader raises ValueError on 2026-02-30; the gate reports.
    write_change(repo, "dated", "bounded", decisions=records(1), extra_header="adr_files: []\nwhen: 2026-02-30\n")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout
    assert "adr_files cannot be read" in done.stdout
    assert "Traceback" not in done.stderr


# --- AC 3 · feature with ADR: five in total, never the sum -----------------


def test_feature_with_adr_needs_five_not_eight(repo: Path) -> None:
    write_change(repo, "feature-adr", "feature", decisions=records(5), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    write_change(repo, "feature-adr", "feature", decisions=records(4), adr_files=[ADR])
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
    write_change(repo, "on-branch", "bounded", decisions=records(4), adr_files=[ADR])
    _stage_adr(repo, commit=True)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "on-branch" in done.stdout


def test_main_checkout_uses_first_parent(repo: Path) -> None:
    # main's landfall: the branch itself says main, so the first parent is
    # the base and the merged change is measured.
    write_change(repo, "merged-in", "bounded", decisions=records(4), adr_files=[ADR])
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
    write_change(repo, "merged-detached", "bounded", decisions=records(4), adr_files=[ADR])
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
    write_change(repo, "detached-work", "bounded", decisions=records(4), adr_files=[ADR])
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
    write_change(repo, "landfall", "bounded", decisions=records(5), adr_files=[ADR])
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
    (lonely / "decisions").mkdir()
    (lonely / "decisions" / "adoption.yaml").write_text(ADOPTION)
    write_change(lonely, "unmeasured", "feature", decisions=records(1))
    _commit_all(lonely, "a change without an origin")
    done = run_gate(lonely)  # no origin/main: no merge base, not on main
    assert done.returncode == 3
    assert "NOT MEASURED" in done.stdout
    assert "merge-base" in done.stdout  # the base is what failed, not the record
    assert "adoption.yaml" not in done.stdout


# --- AC 8 · the adoption day ------------------------------------------------


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
    # minimum — the adoption day decides, not the folder's place.
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
    earlier = "docs/adr/0097-earlier.md"
    _git(repo, "checkout", "main")
    adr = repo / earlier
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0097 — original\n")
    _commit_all(repo, "docs: an adr on main")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "feat/test")
    _git(repo, "merge", "main", "-m", "sync main into the branch")
    write_change(repo, "index-adr", "bounded", decisions=records(4), adr_files=[earlier])
    adr.write_text("# ADR 0097 — changed\n")
    _git(repo, "add", earlier)
    adr.write_text("# ADR 0097 — original\n")  # the working file matches the base
    done = run_gate(repo)
    assert done.returncode == 1
    assert "index-adr (ADR change): 4 of 5" in done.stdout


def test_change_flag_typo_is_red_even_when_another_change_passes(repo: Path) -> None:
    # F-17: a passing unrelated measurement must not answer for the named
    # change — a typo stays red whatever else the run measured.
    write_change(repo, "owner-ok", "bounded", decisions=records(5), adr_files=[ADR])
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
    moved = "docs/adr/0096-moved.md"
    _git(repo, "checkout", "main")
    adr = repo / moved
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text("# ADR 0096\n")
    _commit_all(repo, "docs: an adr on main")
    _git(repo, "push", "origin", "main")
    _git(repo, "checkout", "feat/test")
    _git(repo, "merge", "main", "-m", "sync main into the branch")
    write_change(repo, "moved-adr", "bounded", decisions=records(1), adr_files=[moved])
    _git(repo, "mv", moved, "docs/notes-0096.md")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "moved-adr (ADR change): 1 of 5" in done.stdout


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
    # not evidence of the duty. AGENTS.md stays in its repository: that half
    # skips where the file does not travel.
    workflow = (REPO / "docs" / "WORKFLOW.md").read_text(encoding="utf-8")
    assert "interview-minimums" in workflow
    assert "2026-10-08" in workflow  # the adoption day, dated
    agents_path = REPO / "AGENTS.md"
    if not agents_path.is_file():
        return
    agents = agents_path.read_text(encoding="utf-8")
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
    write_change(repo, "merged-detached", "bounded", decisions=records(4), adr_files=[ADR])
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
    # L1-3: the adoption day exempts a folder's own class minimums, never a
    # new ADR edit — the claimant owes five whatever its spec date.
    write_change(repo, "old-folder", "bounded", day=BEFORE, decisions=records(4), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "old-folder (ADR change): 4 of 5" in done.stdout


def test_change_flag_with_unknown_name_is_found(repo: Path) -> None:
    # L1-6: the spec gate must not pass on a typo.
    write_change(repo, "real", "feature", decisions=records(3))
    done = run_gate(repo, "--change", "real-typo")
    assert done.returncode == 1
    assert "no change folder" in done.stdout


# --- ADR 0014 · the claim, the owner, the agreement, the adoption day -------


def _land_on_main(work: Path, message: str) -> None:
    """Commit what the working tree holds on main, push it, and come back to
    the branch with main merged in — the change then is part of the base."""
    _git(work, "checkout", "main")
    _commit_all(work, message)
    _git(work, "push", "origin", "main")
    _git(work, "checkout", "feat/test")
    _git(work, "merge", "main", "-m", "sync main into the branch")


def test_a_claim_in_flow_or_block_form_names_the_owner(repo: Path) -> None:
    # Criterion 1: the claim in either YAML form owns the edit; a path under
    # another key claims nothing.
    _stage_adr(repo)
    write_change(repo, "flow", "bounded", decisions=records(4), adr_files=[ADR])
    done = run_gate(repo)
    assert done.returncode == 1
    assert "flow (ADR change): 4 of 5" in done.stdout

    write_change(repo, "flow", "bounded", decisions=records(1), extra_header=f"adr_files:\n  - {ADR}\n")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "flow (ADR change): 1 of 5" in done.stdout
    assert "no change in this diff claims it" not in done.stdout

    write_change(repo, "flow", "bounded", decisions=records(5), extra_header=f"notes:\n  - {ADR}\n")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "no change in this diff claims it" in done.stdout


@pytest.mark.parametrize(
    "line",
    [
        "adr_files: docs/adr/0099-x.md",
        "adr_files: [plans/x.md]",
        "adr_files: [docs/adr/../x.md]",
        "adr_files: [docs/adr/]",
        "adr_files: [docs/adr/0099-x.md, docs/adr/0099-x.md]",
        "adr_files: [7]",
        "adr_files: [docs/adr/0099-x.md",
        "adr_files: []\nadr_files: []",
        '"adr\\u005ffiles": [plans/x.md]',  # F-6: an escaped key
        "? adr_files\n: [plans/x.md]",  # F-6: the explicit-key form
    ],
)
def test_an_unreadable_claim_is_reported(repo: Path, line: str) -> None:
    # Criterion 2: a claim that cannot be read is reported in every spec,
    # an archived stock spec included, with and without --change.
    write_change(repo, "fine", "bounded", decisions=records(1))
    write_change(repo, "stock", "feature", day=BEFORE, extra_header=f"{line}\n")
    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "stock").rename(archive / f"{BEFORE}-stock")
    for args in ((), ("--change", "fine")):
        done = run_gate(repo, *args)
        assert done.returncode == 1, (line, done.stdout)
        assert "adr_files cannot be read" in done.stdout
        assert f"archive/{BEFORE}-stock/spec.md" in done.stdout
        assert "adr_files: [docs/adr/<file>" in done.stdout


def test_a_spec_that_is_not_utf8_is_reported_not_a_traceback(repo: Path) -> None:
    # F-7: a spec the gate cannot decode is one finding naming it; the second
    # read for its class and date must not abort the run and lose the findings.
    write_change(repo, "fine", "bounded", decisions=records(1))
    write_change(repo, "stock", "feature", day=BEFORE, extra_header="adr_files: []\n")
    spec = repo / "plans" / "changes" / "stock" / "spec.md"
    spec.write_bytes(spec.read_bytes() + "café\n".encode("latin-1"))
    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "stock").rename(archive / f"{BEFORE}-stock")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout + done.stderr
    assert "Traceback" not in done.stderr
    assert f"archive/{BEFORE}-stock/spec.md: adr_files cannot be read" in done.stdout
    assert "adr_files: [docs/adr/<file>" in done.stdout


def test_the_gate_goes_red_when_an_adr_edit_is_unclaimed(repo: Path) -> None:
    """Mutation evidence for scripts/check_interview_minimums.py: the inference
    of the old gate — the one touched change folder owns the edit — turns this
    run green, and a finding without the remedy loses its `adr_files`."""
    write_change(repo, "touched", "bounded", decisions=records(5))
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 1
    assert f"{ADR} changed, but no change in this diff claims it" in done.stdout
    assert "list it under adr_files in the spec header" in done.stdout


def test_a_claim_outside_the_diff_does_not_own_the_edit(repo: Path) -> None:
    # Criterion 4: only a change of the diff can claim; an active change the
    # diff does not touch, and an archived one, claim nothing for it.
    _git(repo, "checkout", "main")
    write_change(repo, "elsewhere", "bounded", decisions=records(5), adr_files=[ADR])
    _land_on_main(repo, "feat: a change that claims the file, already on main")
    write_change(repo, "unclaiming", "bounded", decisions=records(5))
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "no change in this diff claims it" in done.stdout
    assert "elsewhere (ADR change)" not in done.stdout


def test_an_archived_change_does_not_own_the_edit(repo: Path) -> None:
    write_change(repo, "late", "bounded", day=BEFORE, decisions=records(5), adr_files=[ADR])
    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "late").rename(archive / f"{BEFORE}-late")
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "no change in this diff claims it" in done.stdout


def test_a_claimant_beside_unclaiming_folders_is_decided_by_its_own_records(repo: Path) -> None:
    # Criterion 6, the shape of criterion-test-ledger: one claimant that
    # changes its spec, decisions and plan beside four folders touched
    # through plan.md alone.
    claimant = write_change(repo, "claimant", "bounded", decisions=records(4), adr_files=[ADR])
    (claimant / "plan.md").write_text("# Plan\n")
    for n in range(4):
        migrated = repo / "plans" / "changes" / f"migrated-{n}"
        migrated.mkdir(parents=True)
        (migrated / "plan.md").write_text("# Plan\n\n## Criterion ledger\n\n- 1: not a test — review\n")
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == 1
    assert "claimant (ADR change): 4 of 5" in done.stdout
    assert "migrated-" not in done.stdout
    write_change(repo, "claimant", "bounded", decisions=records(5), adr_files=[ADR])
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


@pytest.mark.parametrize(("count", "code"), [(4, 1), (5, 0)])
def test_a_claimant_touched_through_plan_md_alone_owns_its_edit(repo: Path, count: int, code: int) -> None:
    write_change(repo, "solo", "bounded", decisions=records(count), adr_files=[ADR])
    _land_on_main(repo, "feat: solo change with its answers")
    (repo / "plans" / "changes" / "solo" / "plan.md").write_text("# Plan\n")
    _stage_adr(repo)
    done = run_gate(repo)
    assert done.returncode == code, done.stdout
    if code:
        assert "solo (ADR change): 4 of 5" in done.stdout
        assert "no change in this diff claims it" not in done.stdout


def test_each_claimant_owes_its_own_five(repo: Path) -> None:
    # Criterion 7: two edits with different claimants.
    other = "docs/adr/0098-other.md"
    write_change(repo, "claimant-a", "bounded", decisions=records(5), adr_files=[ADR])
    write_change(repo, "claimant-b", "feature", decisions=records(4), adr_files=[other])
    _stage_adr(repo)
    (repo / other).write_text("# ADR 0098\n")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "claimant-b (ADR change): 4 of 5" in done.stdout
    assert "claimant-a (ADR change)" not in done.stdout
    write_change(repo, "claimant-b", "feature", decisions=records(5), adr_files=[other])
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_the_adr_text_does_not_decide_the_owner(repo: Path) -> None:
    # Criterion 8: the text of an ADR that names an unclaiming folder changes
    # no verdict, and the interim machinery is gone from the gate.
    write_change(repo, "real", "bounded", decisions=records(5), adr_files=[ADR])
    migrated = repo / "plans" / "changes" / "migrated"
    migrated.mkdir(parents=True)
    (migrated / "plan.md").write_text("# Plan\n")
    _stage_adr(repo)
    (repo / ADR).write_text("# ADR 0099 — test\n\nChange: migrated\n")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    source = SCRIPT.read_text(encoding="utf-8")
    assert "_folders_named_by_adrs" not in source
    assert "plan_only" not in source


def test_a_yes_answer_without_a_claim_is_reported(repo: Path) -> None:
    # Criterion 9: no `adr_files` line, and `adr_files: []`, both claim nothing.
    write_change(repo, "yes-feature", "feature", decisions=records(3))
    write_answer(repo, "yes-feature", "yes")
    for header in ("", "adr_files: []\n"):
        write_change(repo, "yes-feature", "feature", decisions=records(3), extra_header=header)
        done = run_gate(repo)
        assert done.returncode == 1, done.stdout
        assert "yes-feature: answers yes to the ADR question but claims no ADR file" in done.stdout
        assert "correct the answer in a decision pull request" in done.stdout
    write_change(repo, "yes-feature", "feature", decisions=records(3), adr_files=[ADR])
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_each_clash_message_names_its_own_remedy(repo: Path) -> None:
    # F-5: two claimants -> split the pull request, never "remove the claim";
    # a "no" answer with a claim -> remove the erroneous claim.
    write_change(repo, "owner-a", "bounded", decisions=records(5), adr_files=[ADR])
    write_change(repo, "owner-b", "bounded", decisions=records(5), adr_files=[ADR])
    _stage_adr(repo)
    _git(repo, "add", "-A")
    clash = run_gate(repo).stdout
    assert "split the pull request" in clash
    assert "remove the claim" not in clash
    assert "a correct claim is never removed" in clash
    _git(repo, "reset", "-q", "--hard")
    _git(repo, "clean", "-fdq")
    write_change(repo, "no-feature", "feature", decisions=records(3), adr_files=["docs/adr/0099-x.md"])
    write_answer(repo, "no-feature", "no")
    wrong = run_gate(repo).stdout
    assert "remove the claim" in wrong
    assert "split the pull request" not in wrong


def test_a_no_answer_with_a_claim_is_reported(repo: Path) -> None:
    # Criterion 10.
    write_change(repo, "no-feature", "feature", decisions=records(3), adr_files=["docs/adr/0099-x.md"])
    write_answer(repo, "no-feature", "no")
    done = run_gate(repo)
    assert done.returncode == 1, done.stdout
    assert "no-feature: answers no to the ADR question but claims docs/adr/0099-x.md" in done.stdout
    write_change(repo, "no-feature", "feature", decisions=records(3))
    assert run_gate(repo).returncode == 0


def test_the_agreement_holds_subject_features_alone(repo: Path) -> None:
    # Criterion 11: stock, other classes and other changes under --change are
    # not compared; an archived subject feature is.
    write_change(repo, "stock", "feature", day=CUTOFF_DAY)  # the adoption day itself
    write_answer(repo, "stock", "yes")
    write_change(repo, "plain", "bounded", decisions=records(1), adr_files=["docs/adr/0099-x.md"])
    write_answer(repo, "plain", "no")
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout

    write_change(repo, "bad", "feature", decisions=records(3))
    write_answer(repo, "bad", "yes")
    done = run_gate(repo, "--change", "plain")
    assert done.returncode == 0, done.stdout
    assert "bad:" not in done.stdout
    done = run_gate(repo)
    assert done.returncode == 1
    assert "bad: answers yes" in done.stdout

    archive = repo / "plans" / "changes" / "archive"
    archive.mkdir(exist_ok=True)
    (repo / "plans" / "changes" / "bad").rename(archive / f"{FUTURE}-bad")
    done = run_gate(repo)
    assert done.returncode == 1
    assert "bad: answers yes" in done.stdout


def test_a_missing_or_refused_answer_is_left_to_adr_answers(repo: Path) -> None:
    # Criterion 12: the gate adr-answers owns those findings, not this gate.
    write_change(repo, "no-file", "feature", decisions=records(3))
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    write_answer(repo, "no-file", "yes", quoted=False)  # a YAML boolean, refused
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout


def test_the_adoption_day_comes_from_the_record(repo: Path) -> None:
    # Criterion 13: the day moves with the record, the gate holds none.
    write_change(repo, "late-feature", "feature", day="2026-10-09")  # no records
    done = run_gate(repo)
    assert done.returncode == 1
    assert "late-feature" in done.stdout
    (repo / "decisions" / "adoption.yaml").write_text(ADOPTION.replace("2026-10-08", "2026-10-10"))
    done = run_gate(repo)
    assert done.returncode == 0, done.stdout
    assert "adoption day 2026-10-10" in done.stdout
    assert "CUTOFF" not in SCRIPT.read_text(encoding="utf-8")


def test_a_missing_adoption_record_is_not_measured(repo: Path) -> None:
    # Criterion 14: without the record the gate exits 3 and reports no finding.
    write_change(repo, "late-feature", "feature")  # would be a finding
    (repo / "decisions" / "adoption.yaml").unlink()
    done = run_gate(repo)
    assert done.returncode == 3
    assert "NOT MEASURED" in done.stdout
    assert "decisions/adoption.yaml" in done.stdout
    assert "interview-minimums: YYYY-MM-DD" in done.stdout
    assert "finding(s)" not in done.stdout


# --- ADR 0014 · the texts ---------------------------------------------------


def test_the_spec_template_and_prompt_name_the_claim(tmp_path: Path) -> None:
    # Criterion 20: the template line passes the gate's claim reading.
    template = (REPO / "templates" / "spec.md").read_text(encoding="utf-8")
    lines = [line for line in template.splitlines() if line.startswith("adr_files:")]
    assert len(lines) == 1
    assert "every class" in lines[0]
    spec = tmp_path / "spec.md"
    spec.write_text(f"---\ntitle: x\nclass: bounded\n{lines[0]}\n---\n\n# Spec\n")
    assert gate._claim(spec) == ([], None)
    prompt = (REPO / "prompts" / "02-spec.md").read_text(encoding="utf-8")
    assert "adr_files" in prompt


def test_the_workflow_states_the_claim_and_the_adoption_record() -> None:
    # Criterion 21.
    workflow = (REPO / "docs" / "WORKFLOW.md").read_text(encoding="utf-8")
    assert "adr_files" in workflow
    assert "decisions/adoption.yaml" in workflow
    assert "ADR 0014" in workflow
    assert "2026-10-08" in workflow
    assert 'that a "yes" is followed by an ADR' not in workflow


# ---------------------------------------------------------------------------
# A fenced example is no record (bead coding-harness-k2r)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("fence", "closing"), [("```", "```"), ("~~~", "~~~"), ("````markdown", "````")])
def test_a_fenced_record_or_skip_is_not_counted(fence: str, closing: str) -> None:
    example = (
        "# Decisions\n\nAn example of the form:\n\n"
        f'{fence}\n## Q-1 · An example question\n\nanswer: "yes"\nanswered_by: maintainer\nstatus: answered\n'
        f"\n## SKIP · interview\n\nstatus: skipped\nreason: an example reason\n{closing}\n"
    )
    records, skips = gate._parse_records(example)
    assert records == [] and skips == [], "a fenced example was counted"


def test_a_record_after_a_closed_fence_still_counts() -> None:
    text = (
        "# Decisions\n\n```\n## Q-9 · fenced\n```\n\n"
        '## Q-1 · A real question\n\nanswer: "yes"\nanswered_by: maintainer\nstatus: answered\n'
    )
    records, _ = gate._parse_records(text)
    assert [ident for ident, _ in records] == ["Q-1"]
    assert records[0][1]["status"] == "answered"


_REAL_Q1 = '## Q-1 · A real question\n\nanswer: "yes"\nanswered_by: maintainer\nstatus: answered\n'
_HIDDEN_Q9 = '## Q-9 · hidden\n\nanswer: "yes"\nanswered_by: maintainer\nstatus: answered\n'


def _ids(text: str) -> list[str]:
    records, _ = gate._parse_records(text)
    return [ident for ident, _ in records]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # a shorter closer inside a four-backtick fence does not close it
        (f"````\n```\n{_HIDDEN_Q9}````\n\n{_REAL_Q1}", ["Q-1"]),
        # a tilde line inside a backtick fence does not close it
        (f"```\n~~~\n{_HIDDEN_Q9}```\n\n{_REAL_Q1}", ["Q-1"]),
        # a closer carrying an info string is no closer: the fence stays open
        (f"```\n{_HIDDEN_Q9}```js\n\n{_REAL_Q1}", []),
        # a one-line "```a```" is no fence (a backtick in a backtick fence's info string)
        (f"```a```\n\n{_REAL_Q1}", ["Q-1"]),
        # four spaces of indent make a code block, not a fence
        (f"    ```\n\n{_REAL_Q1}", ["Q-1"]),
    ],
    ids=["shorter-closer", "tilde-in-backtick", "closer-with-info", "one-line-fence", "indented-four"],
)
def test_the_commonmark_fence_rules_decide_what_is_hidden(text: str, expected: list[str]) -> None:
    assert _ids(text) == expected


def test_an_unclosed_fence_before_the_records_hides_them() -> None:
    text = f"# Decisions\n\n```\nnever closed\n\n{_REAL_Q1}"
    records, skips = gate._parse_records(text)
    assert records == [] and skips == [], "an unclosed fence must hide what follows (fails safe, red)"


def test_a_crlf_file_with_a_closed_fence_still_counts_the_real_record() -> None:
    text = f"# Decisions\n\n```\n{_HIDDEN_Q9}```\n\n{_REAL_Q1}".replace("\n", "\r\n")
    assert _ids(text) == ["Q-1"]
