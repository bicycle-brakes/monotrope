"""The touch map: what a pull request touches (plans/changes/touch-map/spec.md, criteria 1-18).

Every test builds its own git repository in a temporary directory and reads nothing of
this repository's history or files, so the file holds in the kit probe's copy too. The
one thing read from here is the kit manifest, through the probe, for the kit-role test.

Each rule stands next to the fault that turns it red (docs/WORKFLOW.md, phase 5: a gate
that has never been red measures nothing). The faults planted for these tests, with the
test each one turned red, are recorded in plans/changes/touch-map/plan.md.
"""

from __future__ import annotations

import ast
import contextlib
import io
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "touch_map.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import probe  # noqa: E402
import touch_map as tm  # noqa: E402

# ---------------------------------------------------------------------------
# helpers: a repository of the test's own, committed through plumbing-safe git
# ---------------------------------------------------------------------------


def _env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
        env=_env(),
    )
    return done.stdout.strip()


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    return repo


def _commit(repo: Path, files: dict[str, str | None], message: str = "c") -> None:
    """Write the files (a `None` deletes one) and commit everything."""
    for rel, text in files.items():
        path = repo / rel
        if text is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--allow-empty", "-m", message)


def _branch(repo: Path, name: str = "feat") -> None:
    _git(repo, "checkout", "-q", "-b", name)


def _fixture(tmp_path: Path, base: dict[str, str | None], feat: dict[str, str | None]) -> Path:
    """`main` holds `base`; `feat` forks from it and commits `feat`."""
    repo = _repo(tmp_path)
    _commit(repo, base)
    _branch(repo)
    _commit(repo, feat)
    return repo


def _cli(*argv: str) -> tuple[int, str, str]:
    """`main` in this process: exit code, standard output as UTF-8 text, standard error."""
    out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="")
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tm.main(list(argv))
    out.flush()
    return code, out.buffer.getvalue().decode("utf-8"), err.getvalue()  # type: ignore[attr-defined]


def _run(repo: Path, base: str = "main", head: str = "feat") -> str:
    code, out, err = _cli(base, head, "--repo", str(repo))
    assert code == 0, err
    assert err == ""
    return out


def _build(repo: Path) -> tm.Touch:
    return tm.build(str(repo), "main", "feat")


_BOX = re.compile(r"^- `([^`]+)` \((new|changed|removed)\)$")
_GROUP = re.compile(r"^(run by|read by|imported by|tested by|runs|reads|imports|tests|still named by) (.+)$")


def _boxes(out: str) -> dict[str, dict[str, list[str]]]:
    """The box lines of the list -> path -> {"status": [..], group: [names]}."""
    found: dict[str, dict[str, list[str]]] = {}
    for line in out.splitlines():
        parts = line.split(" · ")
        head = _BOX.match(parts[0])
        if not head:
            continue
        groups: dict[str, list[str]] = {"status": [head.group(2)]}
        for part in parts[1:]:
            match = _GROUP.match(part)
            assert match, f"unreadable group {part!r} in {line!r}"
            groups[match.group(1)] = [n.strip("`") for n in match.group(2).split(", ")]
        found[head.group(1)] = groups
    return found


def _paths(out: str) -> list[str]:
    return list(_boxes(out))


# ---------------------------------------------------------------------------
# criterion 1: only the two commits count
# ---------------------------------------------------------------------------


def test_the_working_tree_does_not_count(tmp_path: Path) -> None:
    """Criterion 1: an uncommitted edit that would add a link changes nothing."""
    repo = _fixture(
        tmp_path,
        {"scripts/a_module.py": "V = 1\n", "scripts/b_module.py": "V = 1\n", "tests/test_a.py": "import a_module\n"},
        {"scripts/a_module.py": "V = 2\n", "scripts/b_module.py": "V = 2\n"},
    )
    before = _run(repo)
    assert _boxes(before)["scripts/a_module.py"]["tested by"] == ["+1 unchanged"]
    assert "tested by" not in _boxes(before)["scripts/b_module.py"]
    # The edits stay in the working tree: a test that now imports b_module too, a runner that
    # names both scripts, and a changed file that was never committed.
    (repo / "tests" / "test_a.py").write_text("import a_module\nimport b_module\n", encoding="utf-8")
    (repo / "Makefile").write_text("all:\n\tpython3 scripts/a_module.py scripts/b_module.py\n", encoding="utf-8")
    (repo / "scripts" / "new_only_here.py").write_text("V = 1\n", encoding="utf-8")
    assert _run(repo) == before


def test_two_runs_give_the_same_bytes(tmp_path: Path) -> None:
    """Criterion 1: the same two commits give the same bytes, whatever the hash seed."""
    base = {f"scripts/mod_{i}.py": "V = 1\n" for i in range(8)}
    base.update({f"tests/test_mod_{i}.py": f"import mod_{i}\n" for i in range(8)})
    base["Makefile"] = "all:\n" + "".join(f"\tpython3 scripts/mod_{i}.py\n" for i in range(8))
    feat = {f"scripts/mod_{i}.py": "V = 2\n" for i in range(8)}
    feat.update({f"tests/test_mod_{i}.py": f"import mod_{i}\nX = 2\n" for i in range(4)})
    repo = _fixture(tmp_path, base, feat)
    outputs = set()
    for seed in ("0", "1", "2", "3"):
        done = subprocess.run(
            [sys.executable, str(SCRIPT), "main", "feat", "--repo", str(repo)],
            capture_output=True,
            check=True,
            env={**_env(), "PYTHONHASHSEED": seed},
        )
        outputs.add(done.stdout)
    assert len(outputs) == 1, "the output changes with the hash seed"
    assert outputs == {_run(repo).encode("utf-8")}


def test_only_the_standard_library() -> None:
    """Criterion 1: every import of the script is the standard library's (or `__future__`)."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    assert roots, "the script imports nothing at all: the check reads nothing"
    assert not [r for r in roots if r != "__future__" and r not in sys.stdlib_module_names]


def test_standard_output_is_utf8_whatever_the_locale(tmp_path: Path) -> None:
    """The list uses `·`; a run under the C locale must still write UTF-8 bytes."""
    repo = _fixture(
        tmp_path,
        {"scripts/tool_x.py": "V = 1\n"},
        {"scripts/tool_x.py": "V = 2\n", "tests/test_x.py": "import tool_x\n"},
    )
    env = {**_env(), "LC_ALL": "C", "PYTHONIOENCODING": "ascii", "PYTHONUTF8": "0"}
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "main", "feat", "--repo", str(repo)], capture_output=True, check=True, env=env
    )
    assert " · ".encode() in done.stdout


# ---------------------------------------------------------------------------
# criterion 2: the changed files
# ---------------------------------------------------------------------------


def test_the_merge_base_is_the_start(tmp_path: Path) -> None:
    """Criterion 2: a commit on base after the fork is not a change."""
    repo = _repo(tmp_path)
    _commit(repo, {"scripts/shared_tool.py": "V = 1\n"})
    _branch(repo)
    _commit(repo, {"scripts/on_feat_only.py": "V = 1\n"})
    _git(repo, "checkout", "-q", "main")
    _commit(repo, {"scripts/on_main_only.py": "V = 1\n", "scripts/shared_tool.py": "V = 2\n"})
    out = _run(repo)
    assert _paths(out) == ["scripts/on_feat_only.py"]
    fork = _git(repo, "rev-parse", "--short", _git(repo, "merge-base", "main", "feat"))
    assert f"against the merge base `{fork}`" in out


def test_a_rename_is_removed_and_new(tmp_path: Path) -> None:
    """Criterion 2: no rename detection, whatever the repository's configuration says."""
    repo = _repo(tmp_path)
    _git(repo, "config", "diff.renames", "copies")
    body = "".join(f"LINE_{i} = {i}\n" for i in range(40))
    _commit(repo, {"scripts/old_name.py": body})
    _branch(repo)
    (repo / "scripts" / "old_name.py").rename(repo / "scripts" / "new_name.py")
    _commit(repo, {})
    boxes = _boxes(_run(repo))
    assert {p: g["status"] for p, g in boxes.items()} == {
        "scripts/new_name.py": ["new"],
        "scripts/old_name.py": ["removed"],
    }


# ---------------------------------------------------------------------------
# criterion 3: which changed files are boxes
# ---------------------------------------------------------------------------


def test_which_changed_files_are_boxes(tmp_path: Path) -> None:
    """Criterion 3: every changed code file, test and runner; an "other" file only when a test, runner or shell script links to it."""
    base = {
        "tests/test_named.py": 'X = "data/named.yaml"\nY = "docs/tested.md"\n',
        "scripts/py_names.py": 'P = "data/py_named.yaml"\n',
        "Makefile": "all:\n",
    }
    feat = {
        "scripts/lonely.py": "V = 1\n",  # a code file with no link at all
        "tests/test_lonely.py": "def test_x():\n    pass\n",
        "Makefile": "all:\n\techo changed\n",
        "data/named.yaml": "a: 1\n",  # named by an unchanged test
        "data/unnamed.yaml": "a: 1\n",
        "data/py_named.yaml": "a: 1\n",  # named only by a Python code file
        "docs/tested.md": "text\n",  # Markdown that a test names is a box, not prose
        "docs/note.md": "text\n",
        "README.md": "text\n",
    }
    out = _run(_fixture(tmp_path, base, feat))
    assert _paths(out) == ["scripts/lonely.py", "tests/test_lonely.py", "Makefile", "data/named.yaml", "docs/tested.md"]
    assert "- Not linked: `data/py_named.yaml`, `data/unnamed.yaml`" in out.splitlines()
    assert "- Prose, not drawn: 2 files" in out.splitlines()


# ---------------------------------------------------------------------------
# criterion 4: the links
# ---------------------------------------------------------------------------


def test_each_kind_of_link(tmp_path: Path) -> None:
    """Criterion 4: each kind of link, found by each way a source can name a file."""
    base = {
        "scripts/importer.py": "import target_one\n",
        "Makefile": "all:\n\tpython3 scripts/target_one.py\n\tcat data/config.yaml\n",
        "scripts/launch.sh": "#!/bin/sh\npython3 scripts/target_one.py\n",
        "other/dup.py": "D = 1\n",
    }
    feat = {
        "scripts/target_one.py": "V = 1\n",
        "scripts/target_long_name.py": "V = 1\n",
        "scripts/jt.py": "V = 1\n",
        "scripts/dup.py": "V = 1\n",
        "data/config.yaml": "a: 1\n",
        "scripts/importer_changed.py": "import target_one\n",
        "tests/test_path.py": 'P = "scripts/target_one.py"\n',  # a full path
        "tests/test_base.py": 'N = "target_long_name.py"\n',  # a unique basename over eight characters
        "tests/test_join.py": 'from pathlib import Path\nX = Path(".") / "scripts" / "dup.py"\n',  # a join; the basename is not unique
        "tests/test_imp.py": "import jt\n",  # an import
    }
    boxes = _boxes(_run(_fixture(tmp_path, base, feat)))
    one = boxes["scripts/target_one.py"]
    assert one["run by"] == ["Makefile", "scripts/launch.sh"]  # a runner and a shell script run it
    assert one["imported by"] == ["scripts/importer.py", "scripts/importer_changed.py"]
    assert one["tested by"] == ["tests/test_path.py"]
    assert boxes["scripts/target_long_name.py"]["tested by"] == ["tests/test_base.py"]
    assert boxes["scripts/jt.py"]["tested by"] == ["tests/test_imp.py"]
    assert boxes["scripts/dup.py"]["tested by"] == ["tests/test_join.py"]
    assert boxes["data/config.yaml"]["read by"] == ["Makefile"]
    assert boxes["scripts/importer_changed.py"]["imports"] == ["scripts/target_one.py"]
    assert boxes["tests/test_path.py"]["tests"] == ["scripts/target_one.py"]


def _registry(names: list[str]) -> str:
    return "FILES = [\n" + "".join(f'    "{n}",\n' for n in names) + "]\n"


def test_what_makes_no_link(tmp_path: Path) -> None:
    """Criterion 4: a comment, a docstring, a script's naming, a short or shared basename, an ambiguous join, a registry."""
    data = [f"data/f{i:02d}.txt" for i in range(1, 15)]  # 14 tracked files to name
    base = {
        "scripts/commented.sh": "#!/bin/sh\n# runs scripts/subject_tool.py\n   # and scripts/subject_tool.py\necho hi\n",
        "decisions/gates.yaml": "# scripts/subject_tool.py\nsteps: []\n",
        "tests/test_doc.py": '"""Tests scripts/subject_tool.py."""\n# scripts/subject_tool.py\n\n\ndef test_x():\n    """Also scripts/subject_tool.py."""\n',
        "scripts/names_it.py": 'PATH = "scripts/subject_tool.py"\n',
        "scripts/bare.sh": "#!/bin/sh\nabcde.py\nshared_name.py\n",  # eight characters; two files of that name
        "scripts/bare9.sh": "#!/bin/sh\nabcdef.py\n",  # nine characters: a link
        "other/shared_name.py": "S = 1\n",
        "a/dup_name.py": "D = 1\n",
        "b/dup_name.py": "D = 1\n",
        "tests/test_reg14.py": _registry(["scripts/subject_tool.py", *data[:13]]),  # 14 paths: not a registry
        "tests/test_reg15.py": _registry(["scripts/subject_tool.py", *data[:14]]),  # 15 paths: a registry
        ".github/workflows/ci.yml": "steps:\n"
        + "".join(f"  - {n}\n" for n in ["scripts/subject_tool.py", *data]),  # a runner is exempt
        **{d: "x\n" for d in data},
    }
    feat = {
        "scripts/subject_tool.py": "V = 1\n",
        "scripts/abcde.py": "V = 1\n",
        "scripts/abcdef.py": "V = 1\n",
        "scripts/shared_name.py": "V = 1\n",
        "tests/test_two.py": 'from pathlib import Path\nX = Path(".") / "dup_name.py"\n',  # the join ends two files
    }
    boxes = _boxes(_run(_fixture(tmp_path, base, feat)))
    assert boxes["scripts/subject_tool.py"] == {
        "status": ["new"],
        "run by": ["workflows/ci.yml"],
        "tested by": ["+1 unchanged"],
    }
    assert "run by" not in boxes["scripts/abcde.py"], "eight characters are not enough"
    assert boxes["scripts/abcdef.py"]["run by"] == ["scripts/bare9.sh"], "nine characters are"
    assert "run by" not in boxes["scripts/shared_name.py"], "a basename that two files share names neither"
    assert "tests" not in boxes["tests/test_two.py"], "a join that ends two files names neither"


# ---------------------------------------------------------------------------
# criterion 5: one hop from the change
# ---------------------------------------------------------------------------


def test_a_tests_only_change_shows_the_code_it_tests(tmp_path: Path) -> None:
    """Criterion 5: a change of tests alone still shows the code and runners they name."""
    base = {"scripts/module_a.py": "V = 1\n", "Makefile": "all:\n", "scripts/far.py": "import module_a\n"}
    feat = {"tests/test_a.py": 'import module_a\nM = "Makefile"\n'}
    repo = _fixture(tmp_path, base, feat)
    out = _run(repo)
    assert _boxes(out)["tests/test_a.py"]["tests"] == ["Makefile", "scripts/module_a.py"]
    assert _build(repo).unchanged == ["Makefile", "scripts/module_a.py"]


def test_unchanged_tests_fold(tmp_path: Path) -> None:
    """Criterion 5: the unchanged tests that link to a changed box fold into one count, never boxes of their own."""
    base = {"scripts/subject.py": "V = 1\n", **{f"tests/test_{i}.py": "import subject\n" for i in range(3)}}
    repo = _fixture(tmp_path, base, {"scripts/subject.py": "V = 2\n"})
    touch = _build(repo)
    assert touch.folds == {"scripts/subject.py": 3}
    assert touch.unchanged == []
    assert _boxes(_run(repo))["scripts/subject.py"]["tested by"] == ["+3 unchanged"]


def test_a_fixture_path_is_not_a_box(tmp_path: Path) -> None:
    """Criterion 5: an unchanged file other than code or a runner that a changed test names is no box."""
    base = {"AGENTS.md": "x\n", "docs/fixture_note.md": "x\n", "scripts/real_code.py": "V = 1\n"}
    feat = {"tests/test_fixture.py": 'A = "AGENTS.md"\nB = "docs/fixture_note.md"\nimport real_code\n'}
    repo = _fixture(tmp_path, base, feat)
    assert _build(repo).unchanged == ["scripts/real_code.py"]
    assert _boxes(_run(repo))["tests/test_fixture.py"]["tests"] == ["scripts/real_code.py"]


def test_one_hop_only(tmp_path: Path) -> None:
    """Criterion 5: a file two links away from every changed file is no box."""
    base = {
        "scripts/outer.py": "import middle\n",
        "scripts/middle.py": "import inner\n",
        "scripts/inner.py": "V = 1\n",
        "Makefile": "all:\n\tpython3 scripts/outer.py\n",
    }
    repo = _fixture(tmp_path, base, {"scripts/inner.py": "V = 2\n"})
    assert _build(repo).unchanged == ["scripts/middle.py"]
    assert _boxes(_run(repo))["scripts/inner.py"]["imported by"] == ["scripts/middle.py"]


def test_no_link_between_two_unchanged_boxes(tmp_path: Path) -> None:
    """Criterion 5: a link is drawn only when at least one end is a changed file."""
    base = {
        "scripts/core.py": "V = 1\n",
        "scripts/user_a.py": "import core\n",
        "Makefile": "all:\n\tpython3 scripts/core.py scripts/user_a.py\n",
    }
    touch = _build(_fixture(tmp_path, base, {"scripts/core.py": "V = 2\n"}))
    assert touch.unchanged == ["Makefile", "scripts/user_a.py"]
    assert touch.links == [("Makefile", "scripts/core.py", "runs"), ("scripts/user_a.py", "scripts/core.py", "imports")]


# ---------------------------------------------------------------------------
# criterion 6: removed files
# ---------------------------------------------------------------------------


def test_a_removed_script_still_named(tmp_path: Path) -> None:
    """Criterion 6: a removed file's links come from the merge base; what still names it at head is said."""
    base = {
        "scripts/old_tool.py": "V = 1\n",
        "Makefile": "all:\n\tpython3 scripts/old_tool.py\n",
        "tests/test_x.py": "import old_tool\n",
    }
    repo = _fixture(tmp_path, base, {"scripts/old_tool.py": None})
    line = _boxes(_run(repo))["scripts/old_tool.py"]
    assert line["status"] == ["removed"]
    assert line["run by"] == ["Makefile"]
    assert line["still named by"] == ["Makefile", "tests/test_x.py"]
    # When the runner drops the line in the same pull request, the old link is still read at the
    # merge base, and nothing at head names the file any more.
    other = tmp_path / "second"
    other.mkdir()
    repo = _fixture(other, base, {"scripts/old_tool.py": None, "Makefile": "all:\n", "tests/test_x.py": "X = 1\n"})
    line = _boxes(_run(repo))["scripts/old_tool.py"]
    assert line["run by"] == ["Makefile"]
    assert "still named by" not in line


# ---------------------------------------------------------------------------
# criterion 7: prose only
# ---------------------------------------------------------------------------


def test_prose_only_is_one_line(tmp_path: Path) -> None:
    """Criterion 7: no changed box means exactly one line, and a tested Markdown file is a box."""
    base = {"data/x.json": "{}\n"}
    prose = {"docs/a.md": "a\n", "plans/b.md": "b\n", "README.md": "c\n", "data/x.json": "[]\n", "docs/new.txt": "d\n"}
    assert _run(_fixture(tmp_path, base, prose)) == "Prose only: no code, runner or test changed.\n"
    other = tmp_path / "second"
    other.mkdir()
    assert _run(_fixture(other, base, {})) == "Prose only: no code, runner or test changed.\n", "no change at all"
    third = tmp_path / "third"
    third.mkdir()
    out = _run(_fixture(third, {"tests/test_n.py": 'N = "docs/a.md"\n'}, {"docs/a.md": "a\n"}))
    assert _paths(out) == ["docs/a.md"]


# ---------------------------------------------------------------------------
# criterion 13: exit codes
# ---------------------------------------------------------------------------


def test_not_measured(tmp_path: Path) -> None:
    """Criterion 13: a directory without a repository, an unknown revision, unrelated histories."""
    plain = tmp_path / "plain"
    plain.mkdir()
    repo = _fixture(tmp_path, {"scripts/tool_y.py": "V = 1\n"}, {"scripts/tool_y.py": "V = 2\n"})
    _git(repo, "checkout", "-q", "--orphan", "other")
    _git(repo, "rm", "-rfq", ".")
    _commit(repo, {"x.txt": "x\n"})
    cases = [
        (("main", "feat", "--repo", str(plain)), "is not a git repository"),
        (("main", "feat", "--repo", str(tmp_path / "missing")), "is not a git repository"),
        (("main", "nope", "--repo", str(repo)), "does not resolve"),
        (("nope", "feat", "--repo", str(repo)), "does not resolve"),
        (("main", "other", "--repo", str(repo)), "no merge base"),
    ]
    for argv, reason in cases:
        code, out, err = _cli(*argv)
        assert code == 3, argv
        assert out == "", f"output on standard output for {argv}"
        assert err.startswith("touch-map: not measured"), err
        assert reason in err, err


def test_a_usage_error_is_2() -> None:
    """Criterion 13: a usage error is exit 2 and prints nothing on standard output."""
    for argv in ([], ["main"], ["main", "feat", "--bogus"], ["a", "b", "c"]):
        code, out, _ = _cli(*argv)
        assert code == 2, argv
        assert out == ""


# ---------------------------------------------------------------------------
# criterion 16: the kit carries it
# ---------------------------------------------------------------------------


def test_the_kit_carries_the_script_and_its_test() -> None:
    """Criterion 16: both files have the kit role `mechanismus`, so the templates never name a script the kit lacks."""
    for path in ("scripts/touch_map.py", "tests/test_touch_map.py"):
        found = probe.rolle(path)
        assert found is not None, f"{path} has no role in scripts/kit/manifest.yaml"
        assert found[0] == "mechanismus", path
