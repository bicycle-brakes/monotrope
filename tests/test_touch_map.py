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
    base.update({f"scripts/imp_{i}.py": f"import mod_{i}\n" for i in range(8)})
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


def test_a_runner_names_no_runner(tmp_path: Path) -> None:
    """Criterion 4 (the maintainer's decision, Amendment 1): a runner or shell script that names a runner makes no link."""
    base = {
        "Makefile": "all:\n\tcat decisions/gates.yaml\n\tcat .github/workflows/ci.yml\n\tcat data/config.yaml\n",
        "scripts/launch.sh": "#!/bin/sh\ncat .github/workflows/ci.yml\ncat decisions/gates.yaml\n",
        ".github/workflows/ci.yml": "steps: []\n",
        "decisions/gates.yaml": "steps: []\n",
    }
    feat = {
        ".github/workflows/ci.yml": "steps: [a]\n",
        "decisions/gates.yaml": "steps: [a]\n",
        "data/config.yaml": "a: 1\n",  # the control: the same Makefile names an "other" file, and that is a link
    }
    out = _run(_fixture(tmp_path, base, feat))
    boxes = _boxes(out)
    assert boxes["data/config.yaml"]["read by"] == ["Makefile"], "the control: a runner reads an other file"
    for runner in (".github/workflows/ci.yml", "decisions/gates.yaml"):
        assert set(boxes[runner]) == {"status"}, f"a runner or shell script names {runner}, and that is no link"
    assert "scripts/launch.sh" not in boxes, "a shell script that names only runners is no neighbour"


def test_a_trailing_comment_makes_no_link(tmp_path: Path) -> None:
    """Criterion 4: a name after a `#` that starts a comment in a shell script, a Makefile or YAML makes no link."""
    base = {
        "scripts/run_all.sh": "#!/bin/sh\n"
        "echo hi  # see scripts/subject_tool.py\n"  # a trailing comment: no link
        'echo "a # scripts/quoted_tool.py"\n'  # inside double quotes: code
        "echo 'b # scripts/single_tool.py'\n"  # inside single quotes: code
        "echo $# scripts/count_tool.py\n"  # `$#` is the argument count, not a comment
        "echo a#scripts/glued_tool.py\n"  # no blank before the `#`
        "curl https://example.org/#scripts/frag_tool.py\n"  # the fragment of a URL
        "echo \\# scripts/escaped_tool.py\n"  # an escaped `#`
        "echo $# # scripts/hidden_tool.py\n",  # `$#`, then a comment
        "Makefile": "all:\n\techo build # scripts/other_tool.py\n",
        "decisions/gates.yaml": 'steps: [] # data/config.yaml\nname: "x # data/quoted.yaml"\n',
    }
    names = ["subject", "other", "hidden", "quoted", "single", "count", "glued", "frag", "escaped"]
    feat = {f"scripts/{n}_tool.py": "V = 1\n" for n in names}
    feat.update({"data/config.yaml": "a: 1\n", "data/quoted.yaml": "a: 1\n"})
    out = _run(_fixture(tmp_path, base, feat))
    boxes = _boxes(out)
    for gone in ("subject", "other", "hidden"):
        assert "run by" not in boxes[f"scripts/{gone}_tool.py"], f"a name in a trailing comment makes a link: {gone}"
    for kept in ("quoted", "single", "count", "glued", "frag", "escaped"):
        assert boxes[f"scripts/{kept}_tool.py"]["run by"] == ["scripts/run_all.sh"], f"a name in code is lost: {kept}"
    assert "data/config.yaml" not in boxes and "- Not linked: `data/config.yaml`" in out
    assert boxes["data/quoted.yaml"]["read by"] == ["decisions/gates.yaml"]
    assert "run by" not in boxes["scripts/other_tool.py"]


def test_where_a_comment_starts() -> None:
    """Criterion 4: the rule of `_strip_comment` on its edges: first or after a blank, outside quotes, one line at a time."""
    cases = {
        "# whole line": "",
        "   # indented": "   ",
        "echo hi  # x": "echo hi  ",
        "echo hi\t# x": "echo hi\t",
        "echo $# args": "echo $# args",
        "echo ${#list[@]} # x": "echo ${#list[@]} ",
        "a#b": "a#b",
        "curl https://h/#top": "curl https://h/#top",
        'echo "a # b" # c': 'echo "a # b" ',
        "echo 'a # b' # c": "echo 'a # b' ",
        'echo "it\'s" # c': 'echo "it\'s" ',  # a quote inside the other kind of quote
        'echo \\" # c': 'echo \\" ',  # an escaped quote opens nothing
        "echo \\# x": "echo \\# x",  # an escaped `#` is code
        "echo 'a # b": "echo 'a # b",  # an unclosed quote hides the rest of its line
        "no hash": "no hash",
    }
    for line, kept in cases.items():
        assert tm._strip_comment(line) == kept, line


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


def test_a_moved_module_is_not_still_named(tmp_path: Path) -> None:
    """Criterion 6: an import whose stem now resolves to a moved file does not name the removed one; a path in text still does."""
    base = {
        "scripts/helper_mod.py": "V = 1\n",
        "scripts/user_mod.py": "import helper_mod\n",
        "Makefile": "all:\n\tpython3 scripts/helper_mod.py\n",
    }
    repo = _fixture(tmp_path, base, {"scripts/helper_mod.py": None, "lib/helper_mod.py": "V = 1\n"})
    boxes = _boxes(_run(repo))
    assert boxes["scripts/helper_mod.py"]["status"] == ["removed"]
    assert boxes["scripts/helper_mod.py"]["still named by"] == ["Makefile"], "the old path in text, not the import"
    assert boxes["lib/helper_mod.py"]["imported by"] == ["scripts/user_mod.py"], "the import reaches the moved file"
    # Two files of one stem at head: the import is not unique, but it does not dangle either.
    other = tmp_path / "shared"
    other.mkdir()
    shared = {"scripts/helper_mod.py": None, "lib/helper_mod.py": "V = 1\n", "extra/helper_mod.py": "V = 2\n"}
    boxes = _boxes(_run(_fixture(other, base, shared)))
    assert boxes["scripts/helper_mod.py"]["still named by"] == ["Makefile"]


# ---------------------------------------------------------------------------
# criterion 7: prose only
# ---------------------------------------------------------------------------


def test_prose_only_is_one_line(tmp_path: Path) -> None:
    """Criterion 7: no changed box means exactly one line, and a tested Markdown file is a box."""
    base = {"data/x.json": "{}\n"}
    prose = {"docs/a.md": "a\n", "plans/b.md": "b\n", "README.md": "c\n", "docs/new.txt": "d\n"}
    assert _run(_fixture(tmp_path, base, prose)) == "Prose only: no code, runner or test changed.\n"
    other = tmp_path / "second"
    other.mkdir()
    assert _run(_fixture(other, base, {})) == "Prose only: no code, runner or test changed.\n", "no change at all"
    third = tmp_path / "third"
    third.mkdir()
    out = _run(_fixture(third, {"tests/test_n.py": 'N = "docs/a.md"\n'}, {"docs/a.md": "a\n"}))
    assert _paths(out) == ["docs/a.md"]


def test_prose_only_is_said_only_of_prose(tmp_path: Path) -> None:
    """Criteria 7 (amended), 8: a changed file that is neither prose nor a box is named, and the one line is not printed."""
    base = {"data/x.json": "{}\n"}
    feat = {"pyproject.toml": "a = 1\n", ".gitignore": "x\n", "docs/a.md": "a\n", "data/x.json": "[]\n"}
    out = _run(_fixture(tmp_path, base, feat))
    lines = out.splitlines()
    assert lines[0].startswith("Touched at `") and lines[0].endswith(":")
    assert "- Not linked: `.gitignore`, `data/x.json`, `pyproject.toml`" in lines
    assert "- Prose, not drawn: 1 file" in lines
    assert "Prose only" not in out and "<details>" not in out and not _boxes(out)
    # An ADR answer alone, the case of the row: a data file, no box, named.
    other = tmp_path / "adr"
    other.mkdir()
    out = _run(_fixture(other, {"README.md": "x\n"}, {"decisions/answers/c/adr.yaml": "answer: no\n"}))
    assert "- Not linked: `decisions/answers/c/adr.yaml`" in out.splitlines() and "Prose only" not in out
    assert "Prose, not drawn" not in out, "no prose changed, so no prose line"


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


# ---------------------------------------------------------------------------
# the map: helpers (slice S2)
# ---------------------------------------------------------------------------

_ID = r"[A-Za-z0-9_]+"
_BOX_LINE = re.compile(rf'^  ({_ID})(?:\["([^"`]*)"\]|\(\["([^"`]*)"\]\)):::({_ID})$')
_LINK_LINE = re.compile(rf"^  ({_ID}) (-->|-\.->)\|([a-z]+)\| ({_ID})$")
_CLASS_LINE = re.compile(rf"^  classDef ({_ID}) \S.*$")


def _map_block(out: str) -> str:
    match = re.search(r"```mermaid\n(.*?)\n```", out, re.S)
    assert match, out
    return match.group(1)


def _mermaid_problems(block: str) -> list[str]:
    """The structure check of the spec's criterion 11, standard library only.

    Every line is `flowchart LR`, a box, a link or a class definition; box ids are unique,
    match `[A-Za-z0-9_]+` and none is `end`; every label is in double quotes without a `"` or
    a backtick (the regular expression admits none); both ends of every link are declared
    boxes. Whether GitHub renders the block stays the maintainer's look on the phone.
    """
    lines = block.split("\n")
    problems = []
    if lines[0] != "flowchart LR":
        problems.append(f"the first line is {lines[0]!r}, not 'flowchart LR'")
    ids: list[str] = []
    ends: list[tuple[str, str]] = []
    used: set[str] = set()
    defined: set[str] = set()
    for line in lines[1:]:
        if match := _BOX_LINE.match(line):
            ids.append(match.group(1))
            used.add(match.group(4))
        elif match := _LINK_LINE.match(line):
            ends.append((match.group(1), match.group(4)))
        elif match := _CLASS_LINE.match(line):
            defined.add(match.group(1))
        else:
            problems.append(f"not a box, a link or a class definition: {line!r}")
    problems += [f"duplicate id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    if "end" in ids:
        problems.append("a box is called end")
    for end in (e for pair in ends for e in pair):
        if end not in ids:
            problems.append(f"undeclared link end {end}")
    problems += [f"undefined class {c}" for c in sorted(used - defined)]
    return problems


def _map_links(block: str) -> set[tuple[str, str, str]]:
    """The links of a map as (source label, target label, kind)."""
    labels = {}
    for line in block.split("\n"):
        if match := _BOX_LINE.match(line):
            text = (match.group(2) or match.group(3)).removeprefix("code: ")
            labels[match.group(1)] = re.sub(r" \((new|changed|removed)\)$", "", text)
    out = set()
    for line in block.split("\n"):
        if match := _LINK_LINE.match(line):
            out.add((labels[match.group(1)], labels[match.group(4)], match.group(3)))
    return out


def _list_links(out: str) -> set[tuple[str, str, str]]:
    """The links the list lines name, as (source label, target label, kind)."""
    inbound = {"run by": "runs", "read by": "reads", "imported by": "imports", "tested by": "tests"}
    found = set()
    for path, groups in _boxes(out).items():
        me = tm.short(path)
        for group, names in groups.items():
            for name in names:
                other = f"{name} tests" if name.startswith("+") else name
                if group in inbound:
                    found.add((other, me, inbound[group]))
                elif group not in ("status", "still named by"):
                    found.add((me, other, group))
    return found


def _rich(tmp_path: Path) -> Path:
    """A pull request with every kind of box: new, changed, removed, unchanged, folded, linked outward."""
    base = {
        "scripts/target_one.py": "V = 0\n",
        "scripts/gone.py": "G = 1\n",
        "data/config.yaml": "a: 0\n",
        "scripts/importer.py": "import target_one\n",
        "scripts/launch.sh": "#!/bin/sh\npython3 scripts/target_one.py\n",
        "Makefile": "all:\n\tpython3 scripts/target_one.py\n\tcat data/config.yaml\n\tpython3 scripts/gone.py\n",
        "tests/test_unch_a.py": "import target_one\n",
        "tests/test_unch_b.py": "import target_one\n",
        "other/dup.py": "D = 1\n",
    }
    feat = {
        "scripts/target_one.py": "V = 1\n",
        "scripts/gone.py": None,
        "data/config.yaml": "a: 1\n",
        "scripts/new_tool.py": "N = 1\n",
        "scripts/importer_new.py": "import new_tool\nimport target_one\n",
        "tests/test_path.py": 'P = "scripts/target_one.py"\nQ = "scripts/launch.sh"\n',
        "data/unnamed.yaml": "a: 1\n",
        "docs/n.md": "text\n",
    }
    return _fixture(tmp_path, base, feat)


# ---------------------------------------------------------------------------
# criterion 8: the list, and the map holds the same links
# ---------------------------------------------------------------------------


def test_the_list_and_the_map_hold_the_same_links(tmp_path: Path) -> None:
    """Criterion 8: every link of the map is in the list and the other way round; every changed file is in a line."""
    out = _run(_rich(tmp_path))
    listed, drawn = _list_links(out), _map_links(_map_block(out))
    assert listed == drawn
    assert len(drawn) >= 9, "the fixture draws too little to prove anything"
    assert ("+2 unchanged tests", "scripts/target_one.py", "tests") in drawn
    assert ("Makefile", "scripts/gone.py", "runs") in drawn, "a removed file keeps the link it had at the merge base"
    lines = out.splitlines()
    boxes = _paths(out)
    changed = {
        "scripts/target_one.py",
        "scripts/gone.py",
        "data/config.yaml",
        "scripts/new_tool.py",
        "scripts/importer_new.py",
        "tests/test_path.py",
    }
    assert set(boxes) == changed
    assert "- Not linked: `data/unnamed.yaml`" in lines
    assert "- Prose, not drawn: 1 file" in lines


def test_no_table_or_checkbox(tmp_path: Path) -> None:
    """Criterion 8: no line of the output starts with `|`, and none is a checkbox."""
    out = _run(_rich(tmp_path))
    assert "<details>" in out and "- Prose, not drawn" in out, "the fixture must print every kind of line"
    for line in out.splitlines():
        assert not line.lstrip().startswith("|"), line
        assert not re.match(r"^\s*[-*] \[[ xX]\]", line), line


# ---------------------------------------------------------------------------
# criterion 9: when the map is drawn
# ---------------------------------------------------------------------------


def _star(tmp_path: Path, importers: int) -> str:
    """One changed module and `importers` unchanged importers: `importers + 1` boxes."""
    where = tmp_path / f"star{importers}"
    where.mkdir()
    base = {"scripts/core.py": "V = 1\n", **{f"scripts/user_{i:02d}.py": "import core\n" for i in range(importers)}}
    return _run(_fixture(where, base, {"scripts/core.py": "V = 2\n"}))


def test_the_size_lines(tmp_path: Path) -> None:
    """Criterion 9: the map from one link on and up to 30 boxes; the hint from 15; the list only above 30."""
    split = "Large change: consider splitting it."
    one = _star(tmp_path, 0)
    assert "<details>" not in one and split not in one, "one box and no link: no map"
    for boxes, hint, left_out in ((14, False, False), (15, True, False), (30, True, False), (31, True, True)):
        out = _star(tmp_path, boxes - 1)
        assert (split in out) is hint, f"{boxes} boxes: the hint"
        assert ("<details>" in out) is (not left_out), f"{boxes} boxes: the map"
        assert (f"Map left out: {boxes} boxes, more than 30." in out) is left_out, f"{boxes} boxes: the left-out line"
        assert ("- **Added:**" in out) is (not left_out), f"{boxes} boxes: the three lists go with the map"
    # A fold box counts: 14 changed files and one fold box are 15 boxes.
    where = tmp_path / "folded"
    where.mkdir()
    mods = {f"scripts/m_{i:02d}.py": "V = 1\n" for i in range(14)}
    out = _run(_fixture(where, {**mods, "tests/test_m.py": "import m_00\n"}, {m: "V = 2\n" for m in mods}))
    assert "+1 unchanged tests" in out and split in out


def test_links_may_be_false_wherever_they_are_printed(tmp_path: Path) -> None:
    """Criteria 9, 12 (amended): the caption and, without a map, the list say a link can be false as well as missing."""
    false = "a shown one can be false (a name in text, not a dependency)"
    missing = "some may be missing"
    # A map: the caption says both, and no other line repeats it.
    out = _star(tmp_path, 3)
    caption = [line for line in out.splitlines() if line.startswith("<sub>")]
    assert len(caption) == 1 and false in caption[0] and missing in caption[0] and caption[0].endswith("</sub>")
    assert [line for line in out.splitlines() if "can be false" in line] == caption
    # The map left out: the list prints links and no caption follows, so a line of its own says both.
    out = _star(tmp_path, 30)
    assert "<details>" not in out and "Map left out: 31 boxes, more than 30." in out
    said = [line for line in out.splitlines() if "can be false" in line]
    assert len(said) == 1 and false in said[0] and missing in said[0]
    assert not said[0].startswith("<sub>") and out.index("Map left out") < out.index(said[0])
    # No link, nothing printed that could be false: no caveat.
    assert "can be false" not in _star(tmp_path, 0)
    # More than 30 boxes and no link: the map is left out, the list prints no link, and no caveat follows (Amendment 2).
    where = tmp_path / "unlinked"
    where.mkdir()
    out = _run(_fixture(where, {}, {f"scripts/m_{i:02d}.py": "V = 1\n" for i in range(31)}))
    assert "Map left out: 31 boxes, more than 30." in out and "<details>" not in out
    assert not any(" · " in line for line in out.splitlines()), "the fixture draws no link"
    assert "can be false" not in out and "some may be missing" not in out


# ---------------------------------------------------------------------------
# criterion 10: the map's form
# ---------------------------------------------------------------------------


def test_boxes_carry_level_and_status_in_words(tmp_path: Path) -> None:
    """Criterion 10: `code:` on every box, the status in words as well as colour, the kind on every link, inside `<details>`."""
    out = _run(_rich(tmp_path))
    head = _git(tmp_path / "repo", "rev-parse", "--short", "feat")
    lines = out.splitlines()
    assert lines.count(f"<details><summary>Map at {head}</summary>") == 1 and lines.count("</details>") == 1
    assert out.index("<details>") < out.index("```mermaid") < out.index("```\n\n- **Added:**") < out.index("</details>")
    block = _map_block(out).split("\n")
    assert block[0] == "flowchart LR"
    expected = {
        "scripts/target_one.py": ("changed", "changed"),
        "scripts/new_tool.py": ("new", "added"),
        "scripts/gone.py": ("removed", "removed"),
    }
    seen = set()
    for line in block:
        if match := _BOX_LINE.match(line):
            label = match.group(2) or match.group(3)
            assert label.startswith("code: "), line
            text = label.removeprefix("code: ")
            word = re.search(r" \((new|changed|removed)\)$", text)
            colour = match.group(4)
            if word:  # a changed box: the word and the colour agree
                assert colour == {"new": "added", "changed": "changed", "removed": "removed"}[word.group(1)], line
                seen.add((text.removesuffix(word.group(0)), word.group(1), colour))
            else:  # an unchanged box or a fold box: neither word nor changed colour
                assert colour == "same", line
        elif match := _LINK_LINE.match(line):
            assert match.group(3) in {"runs", "reads", "imports", "tests"}, line
    assert {(tm.short(p), w, c) for p, (w, c) in expected.items()} <= seen
    assert any(re.match(r'^  n\d+\(\["code: \+2 unchanged tests"\]\):::same$', line) for line in block)


# ---------------------------------------------------------------------------
# criterion 11: the block holds by structure
# ---------------------------------------------------------------------------


def test_the_block_holds_by_structure(tmp_path: Path) -> None:
    """Criterion 11: odd file names break no rule: a `"`, a backtick, a newline, `end.sh`, `a-b.py` beside `a_b.py`."""
    odd = ['scripts/a"b.py', "scripts/back`tick.py", "scripts/end.sh", "scripts/a-b.py", "scripts/a_b.py"]
    base = {"Makefile": "all:\n" + "".join(f"\tpython3 {p}\n" for p in odd)}
    feat = {p: "V = 1\n" for p in [*odd, "scripts/new\nline.py"]}
    out = _run(_fixture(tmp_path, base, feat))
    block = _map_block(out)
    assert _mermaid_problems(block) == [], block
    ids = [m.group(1) for line in block.split("\n") if (m := _BOX_LINE.match(line))]
    assert len(ids) == len(set(ids)) >= 7
    assert block.count("-->") >= 5, "the odd files must be linked, or the check proves nothing"
    assert "a'b.py" in block and "back'tick.py" in block, "the labels are cleaned, not dropped"
    assert out.count("\n```") == 2, "a backtick in a name must not break the fenced block"


def test_the_structure_check_can_go_red() -> None:
    """Criterion 11: the structure check itself fails on each rule it states."""
    good = 'flowchart LR\n  n1["code: a.py (new)"]:::added\n  n2["code: b.py"]:::same\n  n2 -->|runs| n1\n  classDef added fill:#fff\n  classDef same fill:#eee'
    assert _mermaid_problems(good) == []
    # Each bad block breaks one rule and the problem it raises must name that rule.
    bad = {
        "an undeclared link end": (good.replace("n2 -->|runs| n1", "n2 -->|runs| n9"), "undeclared link end n9"),
        "a duplicate id": (good.replace("n2", "n1"), "duplicate id n1"),
        "an id called end": (good.replace("n2", "end"), "a box is called end"),
        "an unquoted label": (good.replace('n2["code: b.py"]', "n2[code: b.py]"), "not a box"),
        "a quote inside a label": (good.replace('"code: b.py"', '"code: b".py"'), "not a box"),
        "a backtick inside a label": (good.replace('"code: b.py"', '"code: b`.py"'), "not a box"),
        "a stray line": (good + "\n  subgraph x", "not a box"),
        "a wrong header": (good.replace("flowchart LR", "flowchart TD"), "not 'flowchart LR'"),
        "an undefined class": (good.replace(":::same", ":::nowhere"), "undefined class nowhere"),
        "an id with a dash": (good.replace("n2", "n-2"), "not a box"),
    }
    for what, (block, expected) in bad.items():
        problems = _mermaid_problems(block)
        assert any(expected in p for p in problems), f"the check passes {what}: {problems}"


# ---------------------------------------------------------------------------


def test_imports_added_and_dropped(tmp_path: Path) -> None:
    """Criterion 12: imports of changed code files gained and dropped since the merge base."""
    base = {
        "scripts/mod_a.py": "import dep_one\nimport dep_two\n",
        "scripts/mod_gone.py": "import dep_two\n",
        "scripts/dep_one.py": "V = 1\n",
        "scripts/dep_two.py": "V = 1\n",
        "scripts/dep_three.py": "V = 1\n",
        "Makefile": "all:\n\tpython3 scripts/mod_a.py\n",
    }
    feat = {
        "scripts/mod_a.py": "import dep_one\nimport dep_three\n",
        "scripts/mod_gone.py": None,
        "scripts/mod_new.py": "import dep_one\n",
    }
    out = _run(_fixture(tmp_path, base, feat))
    lines = out.splitlines()
    assert (
        "- **Added:** `scripts/mod_new.py`. New imports: `scripts/mod_a.py` → `scripts/dep_three.py`, `scripts/mod_new.py` → `scripts/dep_one.py`."
        in lines
    )
    assert "- **Changed:** `scripts/mod_a.py`." in lines
    assert (
        "- **Removed:** `scripts/mod_gone.py`. Imports dropped: `scripts/mod_a.py` → `scripts/dep_two.py`, "
        "`scripts/mod_gone.py` → `scripts/dep_two.py`." in lines
    )
    # Nothing gained, nothing dropped: both say none.
    other = tmp_path / "quiet"
    other.mkdir()
    quiet = _run(
        _fixture(
            other, {"scripts/x_mod.py": "V = 1\n", "Makefile": "scripts/x_mod.py\n"}, {"scripts/x_mod.py": "V = 2\n"}
        )
    )
    assert "- **Added:** none. New imports: none." in quiet.splitlines()
    assert "- **Removed:** none. Imports dropped: none." in quiet.splitlines()


def test_the_caption_names_both_commits(tmp_path: Path) -> None:
    """Criterion 12: the line under the lists names head and merge base, says nothing is drawn by hand and links may be missing."""
    repo = _repo(tmp_path)
    _commit(repo, {"scripts/core.py": "V = 1\n", "Makefile": "all:\n\tpython3 scripts/core.py\n"})
    _branch(repo)
    _commit(repo, {"scripts/core.py": "V = 2\n"})
    _git(repo, "checkout", "-q", "main")
    _commit(repo, {"README.md": "later on main\n"})
    out = _run(repo)
    head = _git(repo, "rev-parse", "--short", "feat")
    fork = _git(repo, "rev-parse", "--short", _git(repo, "merge-base", "main", "feat"))
    assert head != fork != _git(repo, "rev-parse", "--short", "main")
    caption = [line for line in out.splitlines() if line.startswith("<sub>")]
    assert len(caption) == 1
    assert f"from the commit {head} and the merge base {fork}" in caption[0]
    assert "scripts/touch_map.py" in caption[0] and "nothing drawn by hand" in caption[0]
    assert "some may be missing" in caption[0] and caption[0].endswith("</sub>")
    assert out.splitlines()[0] == f"Touched at `{head}`, against the merge base `{fork}`:"
