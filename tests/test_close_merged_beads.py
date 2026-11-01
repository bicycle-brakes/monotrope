"""The merged-trailer reconciler closes only what a merged commit declared.

`scripts/close_merged_beads.py` is the executor behind the `Closes-Bead: <id>`
trailer (`prompts/07-commit.md`): merged history decides, the tracker render
decides, and nothing writes before the preflight has read both. These tests
build disposable Git origins with real merge-parent history and stand a
recording fake in for the pinned `tools/bd` wrapper and the render boundary —
this repository's tracker is never touched and nothing reaches a network: the
fixture remote is a local path, the render is a fixture file.

The fake wrapper logs every argv it sees and is configured per run: which close
to refuse, whether `dolt push` fails, and what a fresh render contains. A
ledger row's refutation is the assertion: every test here fails on the fault it
names (a missed side-parent declaration, a second close, an invented PR
number, a publication reported as published).
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
MAKEFILE = REPO_ROOT / "Makefile"

# The script plus its import closure: the copies inside a fixture sandbox
# render through the sandbox's own fake wrapper, never through this repo's.
SCRIPTS = ("close_merged_beads.py", "bead_render.py", "render_beads_export.py", "check_bead_export.py")

MAIN = "coding-harness-main"
SIDE = "coding-harness-side"
PR = "coding-harness-pr"
DUP = "coding-harness-dup"
NONPR = "coding-harness-nonpr"
DONE = "coding-harness-done"
REAL_A = "coding-harness-real-a"
REAL_B = "coding-harness-real-b"
UNMERGED = "coding-harness-unmerged"

# The declared set of the standard origin history; the fixture render holds
# these plus beads that exist without a merged declaration. One line per bead,
# each with id and status — the shape check_bead_export.run validates.
DECLARED = (MAIN, SIDE, PR, DUP, NONPR)
RENDER_LINES = {
    MAIN: "open",
    SIDE: "open",
    PR: "open",
    DUP: "open",
    NONPR: "open",
    UNMERGED: "open",
    REAL_A: "open",
    REAL_B: "open",
    DONE: "closed",
}

STUB = """#!/bin/bash
# Recording stand-in for the pinned tools/bd (test fixture, never this repo's).
printf '%s\\n' "$*" >>"${BEADS_STUB_LOG:?}"
case "$1" in
  export)
    out=""
    while [ $# -gt 0 ]; do
      if [ "$1" = "-o" ]; then out=$2; fi
      shift
    done
    if [ -z "$out" ]; then echo "export: no -o target" >&2; exit 1; fi
    cp "${BEADS_STUB_RENDER:?}" "$out"
    ;;
  close)
    if [ "$2" = "${BEADS_STUB_REFUSE:-}" ]; then
      echo "assignee is worker-a, actor is the reconciler" >&2
      exit 1
    fi
    # A real close moves the tracker; the rerun must read it closed. The
    # fixture line shape is json.dumps({"id": ..., "status": ...}) — the swap
    # is an exact string match, so a refused close leaves the render alone.
    open_line='{"id": "'"$2"'", "status": "open"}'
    closed_line='{"id": "'"$2"'", "status": "closed"}'
    awk -v a="$open_line" -v b="$closed_line" '$0 == a {print b; next} {print}' "${BEADS_STUB_RENDER:?}" >"${BEADS_STUB_RENDER:?}.tmp" &&
      mv "${BEADS_STUB_RENDER:?}.tmp" "${BEADS_STUB_RENDER:?}"
    ;;
  dolt)
    if [ "${BEADS_STUB_PUSH_RC:-0}" != "0" ]; then
      echo "dolt push: the remote refused" >&2
      exit "${BEADS_STUB_PUSH_RC}"
    fi
    ;;
esac
exit 0
"""


def _git(cwd: Path, *args: str) -> str:
    erg = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=120, check=False)
    assert erg.returncode == 0, f"git {' '.join(args)} failed: {erg.stderr}"
    return erg.stdout.strip()


def _commit(cwd: Path, message: str) -> str:
    erg = subprocess.run(
        [
            "git",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "user.name=Test",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--allow-empty",
            "-m",
            message,
            "--quiet",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert erg.returncode == 0, erg.stderr
    return _git(cwd, "rev-parse", "HEAD")


def _merge(cwd: Path, branch: str, message: str) -> str:
    """A real merge commit: the second parent is what pulls a declared side
    branch into main, the way a person's merge on GitHub does. A plain
    `git commit -m "Merge pull request ..."` would have no second parent, and
    the side declaration would be unmerged history."""
    erg = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "merge", "--no-ff", "--quiet", "-m", message, branch],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert erg.returncode == 0, erg.stderr
    return _git(cwd, "rev-parse", "HEAD")


def _write_stub(klon: Path) -> None:
    (klon / "tools").mkdir(parents=True, exist_ok=True)
    stub = klon / "tools" / "bd"
    stub.write_text(STUB, encoding="utf-8")
    stub.chmod(0o755)


def _copy_scripts(klon: Path) -> None:
    (klon / "scripts").mkdir(parents=True, exist_ok=True)
    for name in SCRIPTS:
        (klon / "scripts" / name).write_bytes((REPO_ROOT / "scripts" / name).read_bytes())


def _render_file(pfad: Path, *, text: str | None = None) -> Path:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    if text is None:
        text = "".join(json.dumps({"id": bid, "status": status}) + "\n" for bid, status in RENDER_LINES.items())
    pfad.write_text(text, encoding="utf-8")
    return pfad


def _build(tmp_path: Path, *, name: str = "main", shallow: bool = False) -> SimpleNamespace:
    """An origin with real merge-parent history and a clone of it.

    The clone sits detached on the base commit: eligibility must come from the
    fetched origin/main, never from the local HEAD. All declaring commits sit
    on main or on the side branch, the merge commit carries the GitHub merge
    subject, and the side branch reaches main only through the merge's second
    parent — a real `git merge`, so a first-parent-only traversal misses it.
    """
    origin = tmp_path / f"origin-{name}"
    origin.mkdir()
    _git(origin, "init", "--initial-branch=main", "--quiet")
    _git(origin, "config", "user.email", "test@example.invalid")
    _git(origin, "config", "user.name", "Test")
    base = _commit(origin, "base of the fixture history")
    _git(origin, "checkout", "-b", "side", "--quiet")
    side = _commit(origin, f"expand the side map for ticket 42\n\nCloses-Bead: {SIDE}")
    _git(origin, "checkout", "main", "--quiet")
    main_sha = _commit(origin, f"feat(map): widen the main map (#294)\n\nCloses-Bead: {MAIN}")
    merge = _merge(origin, "side", f"Merge pull request #295 from bicycle-brakes/side\n\nCloses-Bead: {PR}")
    dup_old = _commit(origin, f"declare {DUP} the first time\n\nCloses-Bead: {DUP}")
    dup_new = _commit(origin, f"declare {DUP} the second time\n\nCloses-Bead: {DUP}")
    nonpr = _commit(origin, f"rename map for issue #77 and #88\n\nCloses-Bead: {NONPR}")

    klon = tmp_path / f"klon-{name}"
    if shallow:
        _git(tmp_path, "clone", "--depth", "1", "--quiet", f"file://{origin}", str(klon))
    else:
        _git(tmp_path, "clone", "--quiet", str(origin), str(klon))
    _copy_scripts(klon)
    (klon / "Makefile").write_bytes(MAKEFILE.read_bytes())
    _write_stub(klon)
    if not shallow:
        _git(klon, "checkout", "--quiet", "--detach", base)

    return SimpleNamespace(
        origin=origin,
        klon=klon,
        log=tmp_path / f"stub-{name}.log",
        render=_render_file(tmp_path / f"render-{name}.jsonl"),
        base=base,
        side=side,
        main=main_sha,
        merge=merge,
        dup_old=dup_old,
        dup_new=dup_new,
        nonpr=nonpr,
    )


def _env(
    ns: SimpleNamespace,
    *,
    push_rc: int = 0,
    refuse: str = "",
    preset: Path | None = None,
    render: Path | None = None,
) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key != "BEAD_RENDER"}
    env.update(
        BEADS_STUB_LOG=str(ns.log),
        BEADS_STUB_RENDER=str(render or ns.render),
        BEADS_STUB_PUSH_RC=str(push_rc),
        BEADS_STUB_REFUSE=refuse,
    )
    if preset is not None:
        env["BEAD_RENDER"] = str(preset)
    return env


def _run_script(ns: SimpleNamespace, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ns.klon / "scripts" / "close_merged_beads.py"), *args],
        cwd=ns.klon,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _run_make(ns: SimpleNamespace, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["make", "-f", str(ns.klon / "Makefile"), *args],
        cwd=ns.klon,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _calls(ns: SimpleNamespace) -> list[str]:
    if not ns.log.exists():
        return []
    return ns.log.read_text(encoding="utf-8").splitlines()


def _closes(ns: SimpleNamespace) -> list[str]:
    return [line for line in _calls(ns) if line.startswith("close ")]


def test_all_merged_declarations_are_closed(tmp_path: Path) -> None:
    """Criterion 1: every merged declaration closes, a side parent included.

    The side branch's trailer reaches main only through the merge's second
    parent, and the clone sits detached on the base commit: a traversal that
    follows first parents only, or reads the local HEAD, misses at least one
    declaration and this test goes red.
    """
    ns = _build(tmp_path)
    erg = _run_script(ns, _env(ns), "--write")
    assert erg.returncode == 0, erg.stderr
    assert _git(ns.klon, "rev-parse", "HEAD") == ns.base, "fixture: the clone must sit away from the merged tip"

    closes = _closes(ns)
    closed_ids = [line.split()[1] for line in closes]
    assert sorted(closed_ids) == sorted(DECLARED), closes
    assert len(closed_ids) == len(set(closed_ids)), "a bead was closed twice in one run"

    by_id = {line.split()[1]: line for line in closes}
    assert f"declared by commit {ns.side}" in by_id[SIDE], "the side-parent declaration was missed"
    assert "(PR #294)" in by_id[MAIN]
    assert f"declared by commit {ns.merge}" in by_id[PR] and "(PR #295)" in by_id[PR]


def test_only_valid_merged_trailers_close(tmp_path: Path) -> None:
    """Criterion 2: prose, an unmerged commit and a malformed value close nothing.

    Git decides where trailers end: a Closes-Bead line followed by more prose
    is a body mention, not a trailer. A declaration on a local-only branch is
    not merged history, whatever the local HEAD says. A list in the trailer
    value is malformed and is reported, never closed and never guessed apart.
    The declared set starts closed in this test's render, so a correct run has
    nothing left to close: anything in the close log is a non-declaration that
    closed a bead.
    """
    ns = _build(tmp_path)
    states = {**RENDER_LINES, **{bid: "closed" for bid in DECLARED}}
    preclosed = _render_file(
        tmp_path / "render-preclosed.jsonl",
        text="".join(json.dumps({"id": bid, "status": status}) + "\n" for bid, status in states.items()),
    )
    prose = "prose case, mention followed by prose\n\nThis closes coding-harness-prose in words.\n\nMore prose after the mention."
    hidden = "prose case, key line followed by prose\n\nCloses-Bead: coding-harness-midtrailer\n\nA closing sentence after the line."
    listed = "malformed case, a list\n\nCloses-Bead: coding-harness-alpha coding-harness-beta"
    empty = "malformed case, an empty value\n\nCloses-Bead:"
    for message in (prose, hidden, listed, empty):
        _commit(ns.origin, message)
    _git(ns.klon, "fetch", "origin", "main", "--quiet")
    _git(ns.klon, "checkout", "-b", "local-only", "--quiet")
    _commit(ns.klon, f"unmerged case\n\nCloses-Bead: {UNMERGED}")
    _git(ns.klon, "checkout", "--quiet", "--detach", ns.base)

    erg = _run_script(ns, _env(ns, render=preclosed), "--write")
    assert erg.returncode == 1, (erg.stdout, erg.stderr)
    assert _closes(ns) == [], f"a non-declaration closed something: {_closes(ns)}"
    assert "malformed Closes-Bead value" in erg.stderr
    assert "coding-harness-alpha coding-harness-beta" in erg.stderr, "the malformed value is not named"
    assert "unknown bead" not in erg.stderr, "prose mentions must not become declarations at all"


def test_duplicate_and_closed_beads_are_not_rewritten(tmp_path: Path) -> None:
    """Criterion 3: duplicates resolve newest-first; closed beads stay closed."""
    ns = _build(tmp_path)
    erg = _run_script(ns, _env(ns), "--write")
    assert erg.returncode == 0, erg.stderr

    closes = _closes(ns)
    dup_lines = [line for line in closes if line.startswith(f"close {DUP} ")]
    assert len(dup_lines) == 1, f"a duplicate declaration closed twice: {closes}"
    assert f"declared by commit {ns.dup_new}" in dup_lines[0], "the newest declaring commit did not win"
    assert ns.dup_old not in dup_lines[0]
    assert not any(line.startswith(f"close {DONE} ") for line in closes), "an already closed bead was rewritten"

    # A second run finds everything closed: no close again, and the recorded
    # reason of the first run stays the only one.
    erg2 = _run_script(ns, _env(ns), "--write")
    assert erg2.returncode == 0, erg2.stderr
    assert len(_closes(ns)) == len(closes), "a rerun closed an already closed bead"


def test_reasons_identify_commit_and_explicit_pr(tmp_path: Path) -> None:
    """Criterion 4: the reason names the declaring commit; the PR only when the
    commit message itself states one. A number that is not an explicit PR form
    (here: issue numbers mid-subject) never becomes a PR reference."""
    ns = _build(tmp_path)
    erg = _run_script(ns, _env(ns), "--write")
    assert erg.returncode == 0, erg.stderr

    by_id = {line.split()[1]: line for line in _closes(ns)}
    assert f"declared by commit {ns.side}" in by_id[SIDE]
    assert "(PR #" not in by_id[SIDE], "a plain subject invented a PR number"

    assert f"declared by commit {ns.main}" in by_id[MAIN] and "(PR #294)" in by_id[MAIN]
    assert f"declared by commit {ns.merge}" in by_id[PR] and "(PR #295)" in by_id[PR]
    assert f"declared by commit {ns.nonpr}" in by_id[NONPR]
    assert "#77" not in by_id[NONPR] and "#88" not in by_id[NONPR], "an unrelated number became a PR"


def test_reporting_and_make_default_do_not_write(tmp_path: Path) -> None:
    """Criterion 5: without --write — on the CLI and through the Make target —
    nothing is closed and nothing is published. The Make target refuses any
    ARGS value except empty and --write before a shell ever sees one, and its
    validated --write passes through as data."""
    ns = _build(tmp_path)

    erg = _run_script(ns, _env(ns))
    assert erg.returncode == 0, erg.stderr
    assert "would close" in erg.stdout and MAIN in erg.stdout
    assert _closes(ns) == [] and not any(line.startswith("dolt") for line in _calls(ns))

    make_erg = _run_make(ns, _env(ns), "close-merged")
    assert make_erg.returncode == 0, make_erg.stderr
    assert "would close" in make_erg.stdout
    assert _closes(ns) == [] and not any(line.startswith("dolt") for line in _calls(ns))

    bad = _run_make(ns, _env(ns), "close-merged", "ARGS=--yes-really")
    assert bad.returncode != 0, "an invalid ARGS value was accepted"
    assert "ARGS must be empty or --write" in bad.stderr
    assert _closes(ns) == [] and not any(line.startswith("dolt") for line in _calls(ns)), "the refusal still ran"

    good = _run_make(ns, _env(ns), "close-merged", "ARGS=--write")
    assert good.returncode == 0, good.stderr
    assert any(line.startswith(f"close {MAIN} ") for line in _closes(ns)), (
        "the validated --write never reached the script"
    )


def test_unreadable_preflight_never_closes(tmp_path: Path) -> None:
    """Criterion 6: a failed fetch, a missing remote ref, shallow history, an
    invalid render and a preset render on a write run all stop before any
    closure — and before the publication step."""
    fresh = _build(tmp_path, name="fetch")
    _git(fresh.klon, "remote", "set-url", "origin", str(tmp_path / "does-not-exist"))
    erg = _run_script(fresh, _env(fresh), "--write")
    assert erg.returncode == 1 and "preflight failed" in erg.stderr
    assert _calls(fresh) == [], "a failed fetch still reached the wrapper"

    shallow = _build(tmp_path, name="shallow", shallow=True)
    erg = _run_script(shallow, _env(shallow), "--write")
    assert erg.returncode == 1 and "preflight failed" in erg.stderr
    assert _closes(shallow) == [] and not any(line.startswith("dolt") for line in _calls(shallow))

    no_main = tmp_path / "origin-nomain"
    no_main.mkdir()
    _git(no_main, "init", "--initial-branch=master", "--quiet")
    _git(no_main, "config", "user.email", "test@example.invalid")
    _git(no_main, "config", "user.name", "Test")
    _commit(no_main, "a default branch that is not main")
    klon = tmp_path / "klon-nomain"
    _git(tmp_path, "clone", "--quiet", str(no_main), str(klon))
    _copy_scripts(klon)
    (klon / "Makefile").write_bytes(MAKEFILE.read_bytes())
    _write_stub(klon)
    no_ref = SimpleNamespace(
        klon=klon,
        log=tmp_path / "stub-noref.log",
        render=_render_file(tmp_path / "render-noref.jsonl"),
    )
    erg = _run_script(no_ref, _env(no_ref), "--write")
    assert erg.returncode == 1 and "preflight failed" in erg.stderr
    assert _calls(no_ref) == []

    broken = _build(tmp_path, name="preset")
    preset = tmp_path / "render-broken.jsonl"
    preset.write_text("not json at all\n", encoding="utf-8")
    erg = _run_script(broken, _env(broken, preset=preset))
    assert erg.returncode == 1 and "preflight failed" in erg.stderr
    assert _closes(broken) == []

    refused = _build(tmp_path, name="refusepreset")
    erg = _run_script(refused, _env(refused, preset=refused.render), "--write")
    assert erg.returncode == 1 and "refusing to write" in erg.stderr
    assert _calls(refused) == [], "the preset rejection rendered anyway"

    garbage = _build(tmp_path, name="garbage")
    garbage_env = _env(
        garbage,
        render=_render_file(tmp_path / "render-garbage.jsonl", text="}\n"),
    )
    erg = _run_script(garbage, garbage_env, "--write")
    assert erg.returncode == 1 and "preflight failed" in erg.stderr
    assert _closes(garbage) == [] and not any(line.startswith("dolt") for line in _calls(garbage))


def test_unknown_and_refused_closures_are_reported_without_force(tmp_path: Path) -> None:
    """Criterion 7: an unknown identifier is reported, never created; a refused
    closure is reported, never forced — and the independent candidate still
    closes, with the run ending unresolved."""
    ns = _build(tmp_path)
    _commit(ns.origin, "declare an unknown bead\n\nCloses-Bead: coding-harness-ghost")
    _commit(ns.origin, f"declare {REAL_A}\n\nCloses-Bead: {REAL_A}")
    _commit(ns.origin, f"declare {REAL_B}\n\nCloses-Bead: {REAL_B}")
    _git(ns.klon, "fetch", "origin", "main", "--quiet")

    erg = _run_script(ns, _env(ns, refuse=REAL_A), "--write")
    assert erg.returncode == 1, (erg.stdout, erg.stderr)
    assert "unknown bead (not created): coding-harness-ghost" in erg.stderr
    assert f"closed {REAL_B}" in erg.stdout, "a refused closure blocked the independent candidate"
    assert f"refused: {REAL_A}" in erg.stderr
    assert not any("--force" in line for line in _calls(ns)), "ownership was overridden"
    assert any(line.startswith("dolt") for line in _calls(ns)), "the partial batch was not published"

    # The refusal was the wrapper's stance, not the declaration's: a normal
    # run closes the bead — the unknown identifier stays unresolved and keeps
    # the run nonzero.
    erg2 = _run_script(ns, _env(ns), "--write")
    assert erg2.returncode == 1, erg2.stdout
    assert f"closed {REAL_A}" in erg2.stdout, "the refused closure never became closable"
    assert "unknown bead" in erg2.stderr, "the unknown identifier was silently dropped on the rerun"


def test_partial_and_retried_runs_publish(tmp_path: Path) -> None:
    """Criterion 8: an eligible write run publishes what it can and still
    publishes on the rerun after a failed publication — even with nothing left
    to close."""
    partial = _build(tmp_path, name="partial")
    _commit(partial.origin, f"declare {REAL_A}\n\nCloses-Bead: {REAL_A}")
    _commit(partial.origin, f"declare {REAL_B}\n\nCloses-Bead: {REAL_B}")
    _git(partial.klon, "fetch", "origin", "main", "--quiet")
    erg = _run_script(partial, _env(partial, refuse=REAL_A), "--write")
    assert erg.returncode == 1 and f"refused: {REAL_A}" in erg.stderr
    assert any(line.startswith("dolt") for line in _calls(partial)), "a partial batch was left unpublished"

    ns = _build(tmp_path, name="retry")
    failed = _run_script(ns, _env(ns, push_rc=1), "--write")
    assert failed.returncode == 1 and "publication failed" in failed.stderr
    first_closes = len(_closes(ns))
    assert first_closes == len(DECLARED) and any(line.startswith("dolt") for line in _calls(ns))

    retry = _run_script(ns, _env(ns), "--write")
    assert retry.returncode == 0, retry.stderr
    assert len(_closes(ns)) == first_closes, "the rerun closed again instead of only publishing"
    assert "published: yes" in retry.stdout
    push_calls = [line for line in _calls(ns) if line.startswith("dolt")]
    assert len(push_calls) == 2, f"the already-closed rerun skipped publication: {push_calls}"


def test_failed_publication_is_not_success(tmp_path: Path) -> None:
    """Criterion 9: a failed dolt push is reported and never reads as published."""
    ns = _build(tmp_path, name="publish")
    erg = _run_script(ns, _env(ns, push_rc=1), "--write")
    assert erg.returncode == 1, erg.stdout
    assert "publication failed" in erg.stderr
    assert "published: yes" not in erg.stdout
    assert "published: NO" in erg.stdout
    assert any(line.startswith(f"close {MAIN} ") for line in _closes(ns))


def test_make_arguments_remain_literal_and_command_line_only(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    env = _env(ns)
    env["ARGS"] = "--write"
    result = _run_make(ns, env, "close-merged")
    assert result.returncode == 0, result.stderr
    assert "would close" in result.stdout
    assert not _closes(ns) and "dolt push" not in _calls(ns)

    marker = tmp_path / "expanded"
    for raw in (f"$(shell touch {marker})--write", "--write\n", "--\twrite", "--write\t"):
        result = _run_make(ns, _env(ns), "close-merged", f"ARGS={raw}")
        assert result.returncode != 0, (raw, result.stdout, result.stderr)
        assert "ARGS must be empty or --write" in result.stderr
        assert not marker.exists(), "make expanded an argument as code"
        assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_make_uses_its_own_checkout_from_any_directory(tmp_path: Path) -> None:
    ns = _build(tmp_path, name="intended")
    other = _build(tmp_path, name="other")
    _commit(other.origin, f"other declaration\n\nCloses-Bead: {REAL_A}")
    nested = tmp_path / "linked"
    _git(other.klon, "worktree", "add", "--detach", str(nested), "HEAD")
    _copy_scripts(nested)
    _write_stub(nested)
    for cwd in (tmp_path, other.klon, nested):
        result = subprocess.run(
            ["make", "-f", str(ns.klon / "Makefile"), "close-merged"],
            cwd=cwd,
            env=_env(ns),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert ns.main in result.stdout, "make reconciled the caller's checkout"
        assert f"would close {REAL_A}" not in result.stdout
    assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_script_uses_its_own_checkout_from_another_worktree(tmp_path: Path) -> None:
    ns = _build(tmp_path, name="intended")
    other = _build(tmp_path, name="other")
    linked = tmp_path / "linked"
    _git(ns.klon, "worktree", "add", "--detach", str(linked), "HEAD")
    _copy_scripts(linked)
    _write_stub(linked)
    # Give the other checkout a different history, so using its cwd is visible.
    _commit(other.origin, f"other repository declaration\n\nCloses-Bead: {REAL_A}")
    result = subprocess.run(
        [sys.executable, str(linked / "scripts" / "close_merged_beads.py"), "--write"],
        cwd=other.klon,
        env=_env(ns),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert len(_closes(ns)) == len(DECLARED)
    assert ns.main in result.stdout
    assert not any(line.startswith(f"close {REAL_A} ") for line in _closes(ns))
    assert "dolt push" in _calls(ns)


def test_log_failure_is_preflight_failure(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    bindir = tmp_path / "bin"
    bindir.mkdir()
    real_git = shutil.which("git")
    wrapper = bindir / "git"
    wrapper.write_text(
        f'#!/bin/sh\nif [ "$1" = log ]; then echo "broken history" >&2; exit 2; fi\nexec "{real_git}" "$@"\n'
    )
    wrapper.chmod(0o755)
    env = _env(ns)
    env["PATH"] = str(bindir) + os.pathsep + env["PATH"]
    result = _run_script(ns, env, "--write")
    assert result.returncode == 1
    assert "preflight failed, nothing attempted" in result.stderr
    assert "broken history" in result.stderr and "Traceback" not in result.stderr
    assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_export_failure_is_preflight_failure(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    stub = ns.klon / "tools" / "bd"
    stub.write_text(STUB.replace("  export)", '  export)\n    echo "database unavailable" >&2; exit 3'))
    result = _run_script(ns, _env(ns), "--write")
    assert result.returncode == 1
    assert "preflight failed, nothing attempted" in result.stderr
    assert "Traceback" not in result.stderr
    assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_startup_budget_reserves_publication(tmp_path: Path) -> None:
    """Close part of a slow batch, then publish after the close budget runs out."""
    ns = _build(tmp_path)
    stub = ns.klon / "tools" / "bd"
    # Keep the per-close bound above the one-second admission floor. Five
    # slow closes cannot all start within this budget, but some must finish.
    stub.write_text(STUB.replace("  close)", "  close)\n    sleep 0.3"))
    result = _run_script(ns, {**_env(ns), "CLOSE_MERGED_BD_TIMEOUT": "1.5"}, "--write", "--budget-seconds", "2")
    assert result.returncode == 1
    assert "startup budget exhausted" in result.stderr
    assert "dolt push" in _calls(ns), (result.stdout, result.stderr)
    assert "published: yes" in result.stdout
    closed = [
        json.loads(line)["id"] for line in ns.render.read_text().splitlines() if json.loads(line)["status"] == "closed"
    ]
    completed = set(closed) & set(DECLARED)
    assert 0 < len(completed) < len(DECLARED), (result.stdout, result.stderr)
    assert len(_closes(ns)) == len(completed), "every attempted close must finish before publication"
    calls = _calls(ns)
    assert all(calls.index(close) < calls.index("dolt push") for close in _closes(ns))


def test_renderer_unexpected_exit_is_preflight_failure(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); import close_merged_beads as reconcile\n"
        "def failed_render():\n    raise SystemExit(3)\n"
        "reconcile.bead_render.render_pfad = failed_render\n"
        "sys.exit(reconcile.main(['--write']))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code, str(ns.klon / "scripts")],
        cwd=ns.klon,
        env=_env(ns),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "preflight failed, nothing attempted" in result.stderr
    assert "tracker render is not readable" in result.stderr
    assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_make_argument_whitespace_is_rejected(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    for raw in ("--write\n", "--write\t", "--\twrite"):
        result = _run_make(ns, _env(ns), "close-merged", f"ARGS={raw}")
        assert result.returncode != 0
        assert "ARGS must be empty or --write" in result.stderr
        assert not _closes(ns) and "dolt push" not in _calls(ns)


def test_short_startup_budget_allows_quick_closures(tmp_path: Path) -> None:
    """A budget below BD_TIMEOUT still allows quick closes and publication."""
    ns = _build(tmp_path)
    result = _run_script(ns, _env(ns), "--write", "--budget-seconds", "30")
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert len(_closes(ns)) == len(DECLARED)
    assert "dolt push" in _calls(ns)
    assert "published: yes" in result.stdout


def test_reporting_exit_contract_is_exposed_in_help(tmp_path: Path) -> None:
    """Report-only is read-only, but unresolved declarations still exit nonzero."""
    ns = _build(tmp_path)
    _commit(ns.origin, "unknown declaration\n\nCloses-Bead: coding-harness-ghost")
    _commit(ns.origin, "malformed declaration\n\nCloses-Bead: two beads")
    for result in (_run_script(ns, _env(ns)), _run_make(ns, _env(ns), "close-merged")):
        assert result.returncode != 0
        assert "unknown bead" in result.stderr
        assert "malformed Closes-Bead" in result.stderr
    assert not _closes(ns) and "dolt push" not in _calls(ns)
    cli_help = _run_script(ns, _env(ns), "--help")
    make_help = _run_make(ns, _env(ns), "help")
    assert cli_help.returncode == make_help.returncode == 0
    for result in (cli_help, make_help):
        assert "reporting also fails on unresolved declarations" in " ".join(result.stdout.split())


def test_miscased_trailers_are_reported_without_closing(tmp_path: Path) -> None:
    """Only the exact key closes; case mistakes are visible unresolved items."""
    ns = _build(tmp_path)
    for key, bid in (("closes-bead", REAL_A), ("CLOSES-BEAD", REAL_B), ("Closes-bead", UNMERGED)):
        _commit(ns.origin, f"mistyped key\n\n{key}: {bid}")
    result = _run_script(ns, _env(ns), "--write")
    assert result.returncode == 1, (result.stdout, result.stderr)
    assert len(_closes(ns)) == len(DECLARED), "valid declarations must still close"
    for bid in (REAL_A, REAL_B, UNMERGED):
        assert not any(line.startswith(f"close {bid} ") for line in _closes(ns))
        assert bid in result.stderr
    assert result.stderr.count("malformed Closes-Bead") == 3
    assert "dolt push" in _calls(ns)


def test_subsecond_startup_remainder_refuses_closures(monkeypatch, capsys) -> None:
    spec = importlib.util.spec_from_file_location("budget_reconciler", REPO_ROOT / "scripts/close_merged_beads.py")
    reconcile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reconcile)
    monkeypatch.delenv("BEAD_RENDER", raising=False)
    monkeypatch.setattr(reconcile, "resolve_checkout", lambda: (REPO_ROOT, REPO_ROOT / "tools" / "bd"))
    monkeypatch.setattr(reconcile, "fetch_and_pin", lambda _root: "a" * 40)
    monkeypatch.setattr(reconcile, "load_state", lambda: {MAIN: {"status": "open"}})
    monkeypatch.setattr(reconcile, "collect_declarations", lambda *_args: ({MAIN: ("a" * 40, "done")}, []))
    ticks = iter([0.0, 9.5, 9.5])
    monkeypatch.setattr(reconcile.time, "monotonic", lambda: next(ticks))
    calls = []

    def run(argv, **_kwargs):
        calls.append(argv[1:])
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(reconcile.subprocess, "run", run)
    assert reconcile.main(["--write", "--budget-seconds", "10"]) == 1
    assert calls == [["dolt", "push"]], "a sub-second remainder must not start a close"
    assert "startup budget exhausted" in capsys.readouterr().err


def test_make_rejects_ambiguous_makefile_list(tmp_path: Path) -> None:
    ns = _build(tmp_path)
    extra = tmp_path / "extra.mk"
    extra.write_text("# Extra make input\n")
    spaced = tmp_path / "space path"
    spaced.mkdir()
    (spaced / "Makefile").write_bytes(MAKEFILE.read_bytes())
    including = tmp_path / "including.mk"
    including.write_text(f"include {ns.klon / 'Makefile'}\n")
    for args, additions in (
        (["-f", str(ns.klon / "Makefile"), "-f", str(extra)], {}),
        (["-f", str(ns.klon / "Makefile")], {"MAKEFILES": str(extra)}),
        (["-f", str(including)], {}),
        (["-f", str(spaced / "Makefile")], {}),
    ):
        result = subprocess.run(
            ["make", *args, "close-merged"],
            cwd=tmp_path,
            env={**_env(ns), **additions},
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0
        assert "close-merged: expected exactly one Makefile path without whitespace" in result.stderr
        assert not _calls(ns), "an ambiguous makefile list reached the tracker"
