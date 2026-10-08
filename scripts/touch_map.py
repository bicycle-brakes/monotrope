#!/usr/bin/env python3
"""touch_map.py - what a pull request touches, as a list and a collapsed Mermaid map.

Usage:
    python3 scripts/touch_map.py BASE HEAD [--repo PATH]

An agent runs it after the last push (`origin/main HEAD`) and pastes the output,
unchanged, under "What it touches" in the pull request body (prompts/07-commit.md).
Spec: plans/changes/touch-map/spec.md.

Nothing is read from the working tree or the network. The script asks git for
objects only (`rev-parse`, `merge-base`, `diff-tree`, `ls-tree`, `cat-file`), uses the
standard library only, and gives the same bytes for the same two commits.

The rules, in short:

  * Changed files are the difference between the merge base of BASE and HEAD and HEAD,
    without rename detection: a rename is one removed and one new file.
  * A code file is a `.py` or `.sh` file outside `tests/`; a test is a `.py` file under
    `tests/`; a runner is one of RUNNERS or a file under RUNNER_DIRS. These three kinds
    are the sources, the files whose text is read for links; the rest is "other".
  * The code text of a source is its text without comments and, for Python, without
    docstrings. In a shell script, `Makefile` or YAML file a comment runs from a `#` that
    is first on its line or follows a blank, outside quotes; quotes are followed across lines and
    a heredoc body is code (`_strip_comments`). A source names a tracked file by its full path,
    by its basename (when that is unique and longer than BASENAME_LONGER_THAN), or - in a test -
    by a chain of `/` joins whose trailing string segments end exactly one tracked path.
  * Links, each with a kind: `tests` (a test names or imports a file), `runs` (a runner
    or shell script names a code file or test), `reads` (a runner or shell script names
    an "other" file), `imports` (a Python code file imports a tracked `.py` file by its
    unique stem). A Python code file makes no link by naming a path, and a source that
    is not a runner and names REGISTRY_PATHS or more tracked files by full path (a
    registry) makes none.
  * Boxes: every changed code file, test and runner, and every changed "other" file a
    test, runner or shell script links to; one hop of unchanged neighbours (runners,
    shell scripts and Python code files that link to a changed box, code and runners a
    changed test links to); the unchanged tests of a changed box fold into one box.
    A link is drawn only between two boxes when at least one of them is changed.
  * A removed file's links are read at the merge base.
  * Without a changed box the output is one line when every changed file is prose, and the
    files that are neither boxes nor prose, named, when some are not. With SPLIT_FROM boxes
    it advises a split, above MAP_MAX boxes it draws no map, and without a link it draws none.

The constants below are the one place an instance changes these rules.

Exit: 0 = the output was printed; 2 = usage; 3 = not measured (not a git repository, a
      revision that does not resolve, no merge base) - a line beginning
      `touch-map: not measured` goes to standard error and nothing to standard output.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import NamedTuple

# What this repository means by runner, test, code and prose.
RUNNERS = ("Makefile", "decisions/gates.yaml")
RUNNER_DIRS = (".github/workflows/",)
TESTS = "tests/"
CODE = (".py", ".sh")
PROSE_DIRS = ("docs/", "plans/")
PROSE_SUFFIXES = (".md",)
# A source naming this many tracked files by full path is a registry and links to none.
REGISTRY_PATHS = 15
# A basename names a file only when it is unique and longer than this.
BASENAME_LONGER_THAN = 8
# From this many boxes the output advises a split; above MAP_MAX it draws no map.
SPLIT_FROM = 15
MAP_MAX = 30

KIND_ORDER = {"code": 0, "test": 1, "runner": 2, "other": 3}
STATUS_WORD = {"A": "new", "D": "removed"}
# The order of the groups in the line of a box: who reaches it, then what it reaches.
INBOUND = {"runs": "run by", "reads": "read by", "imports": "imported by", "tests": "tested by"}
GROUPS = ("run by", "read by", "imported by", "tested by", "runs", "reads", "imports", "tests", "still named by")
MAP_CLASS = {"new": "added", "changed": "changed", "removed": "removed"}
PROSE_ONLY = "Prose only: no code, runner or test changed."
# Said wherever links are printed: a link is a name found in text, so it can be missing or false.
LINKS_CAVEAT = (
    "Links are found by reading the code, so some may be missing "
    "and a shown one can be false (a name in text, not a dependency)."
)
# The colours of the map: status in colour, never in colour alone (the label says it in words).
CLASSES = (
    "  classDef added fill:#d9f2d9,stroke:#2e7d32,color:#000",
    "  classDef changed fill:#fff2cc,stroke:#b58900,color:#000",
    "  classDef removed fill:#f7d4d4,stroke:#a02a2a,color:#000",
    "  classDef same fill:#f2f2f2,stroke:#999,color:#000",
)


class CannotMeasure(Exception):
    """The two revisions cannot be compared; `main` turns this into exit 3."""


# --- git ------------------------------------------------------------------------------


def _git(repo: str, args: list[str], data: bytes | None = None) -> bytes:
    try:
        done = subprocess.run(["git", "-C", repo, *args], input=data, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        lines = err.stderr.decode("utf-8", "replace").strip().splitlines()
        raise CannotMeasure(lines[0] if lines else f"git {args[0]} failed") from err
    except OSError as err:
        raise CannotMeasure(f"cannot run git: {err}") from err
    return done.stdout


def git(repo: str, *args: str) -> str:
    """Run a git plumbing command in `repo`; raise `CannotMeasure` when it fails."""
    return _git(repo, list(args)).decode("utf-8", "replace")


class Revisions(NamedTuple):
    head: str
    merge_base: str
    head_short: str
    merge_base_short: str


def resolve(repo: str, base: str, head: str) -> Revisions:
    """Head and merge base as full and short hashes, or `CannotMeasure`."""
    try:
        git(repo, "rev-parse", "--git-dir")
    except CannotMeasure as err:
        raise CannotMeasure(f"{repo} is not a git repository ({err})") from err
    ids = []
    for rev in (base, head):
        try:
            ids.append(git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").strip())
        except CannotMeasure as err:
            raise CannotMeasure(f"the revision {rev!r} does not resolve to a commit") from err
    try:
        merge_base = git(repo, "merge-base", ids[0], ids[1]).strip()
    except CannotMeasure:
        merge_base = ""
    if not merge_base:
        raise CannotMeasure(f"{base!r} and {head!r} have no merge base")
    return Revisions(
        ids[1],
        merge_base,
        git(repo, "rev-parse", "--short", ids[1]).strip(),
        git(repo, "rev-parse", "--short", merge_base).strip(),
    )


def changed(repo: str, merge_base: str, head: str) -> dict[str, str]:
    """Every changed path between the merge base and head -> `new`, `changed` or `removed`.

    Plumbing with `-z` and no rename detection, so neither the user's `diff.renames`
    nor the quoting of odd names reaches the result.
    """
    raw = git(repo, "diff-tree", "-r", "-z", "--no-renames", "--name-status", merge_base, head)
    fields = raw.split("\0")
    out = {}
    for i in range(0, len(fields) - 1, 2):
        out[fields[i + 1]] = STATUS_WORD.get(fields[i][:1], "changed")
    return out


# --- what a path is -------------------------------------------------------------------


def kind(path: str) -> str:
    """`runner`, `test`, `code` or `other`."""
    if path in RUNNERS or path.startswith(RUNNER_DIRS):
        return "runner"
    if path.startswith(TESTS):
        return "test" if path.endswith(".py") else "other"
    return "code" if path.endswith(CODE) else "other"


def is_shell(path: str) -> bool:
    return kind(path) == "code" and path.endswith(".sh")


def is_prose(path: str) -> bool:
    return path.endswith(PROSE_SUFFIXES) or path.startswith(PROSE_DIRS)


def short(path: str) -> str:
    """Folder and file: `scripts/ci_gates.py`, `kit/probe.py`; `Makefile` alone at the root."""
    return "/".join(path.rsplit("/", 2)[-2:])


# --- reading the code -----------------------------------------------------------------


@dataclass
class Source:
    text: str  # the code text: no comments, for Python no docstrings
    tree: ast.Module | None  # the Python tree of the code text, else None


def _is_docstring(node: ast.stmt) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


# A heredoc marker: `<<`, an optional `-`, a delimiter bare, quoted or escaped. `<<<` and `<< 3` are not one.
_HEREDOC = re.compile(r"<<-?[ \t]*(?:'([^']+)'|\"([^\"]+)\"|\\?([A-Za-z_][A-Za-z_0-9]*))")


# The scan state across lines: one entry per open command substitution `$( … )`, the outermost first. Each
# holds the quote open in that context ("" none, `'`, `"`, or `$'` for an ANSI-C string) and its count of
# unquoted `(` still to close.
State = tuple[tuple[str, int], ...]
OUTSIDE: State = (("", 0),)


def _scan(line: str, state: State, yaml: bool = False) -> tuple[str, State, list[str]]:
    """One line up to its comment, the state still open at its end, the delimiters of the heredocs it starts.

    A `$(` opens a context of its own, so the quotes of `"$(echo "$x" | sed 's/"//')"` nest as the shell
    nests them, and `$'…'` lets a backslash escape its quote (bead coding-harness-cff). In a YAML file an
    apostrophe between two letters (`Don't`) is a letter, not a quote.
    """
    stack = [list(context) for context in state]
    heredocs: list[str] = []
    blank = True  # the first character of a line counts as following a blank
    i = 0
    while i < len(line):
        char = line[i]
        quote = stack[-1][0]
        if char == "\\" and quote != "'":
            i += 2  # the escaped character is neither a quote, a `#` nor a blank
            blank = False
            continue
        if quote in ("'", "$'"):
            if char == "'":
                stack[-1][0] = ""
        elif line.startswith("$(", i):
            stack.append(["", 0])  # inside double quotes too: a substitution starts its own quoting
            i += 2
            blank = False
            continue
        elif quote == '"':
            if char == '"':
                stack[-1][0] = ""
        elif char == '"':
            stack[-1][0] = char
        elif char == "'":
            letters = 0 < i < len(line) - 1 and line[i - 1].isalpha() and line[i + 1].isalpha()
            if not (yaml and letters):
                # `$'` opens an ANSI-C string only where the `$` starts a word: `\$'` and `$$'` are a plain quote
                ansi = i > 0 and line[i - 1] == "$" and (i < 2 or line[i - 2] in " \t=(;|&")
                stack[-1][0] = "$'" if ansi else "'"
        elif char == "(":
            stack[-1][1] += 1
        elif char == ")":
            if stack[-1][1]:
                stack[-1][1] -= 1
            elif len(stack) > 1:
                stack.pop()
        elif char == "#" and blank:
            return line[:i], tuple(tuple(context) for context in stack), heredocs
        elif char == "<" and line.startswith("<<", i):
            found = _HEREDOC.match(line, i)  # `<<<` (a here-string) and `<< 3` are no marker
            if found:
                heredocs.append(found.group(1) or found.group(2) or found.group(3))
            i = found.end() if found else i + 2
            blank = False
            continue
        blank = char in " \t"
        i += 1
    return line, tuple(tuple(context) for context in stack), heredocs


def _strip_comments(body: str, yaml: bool = False) -> str:
    """The text of a shell script, `Makefile` or YAML file without its comments.

    A `#` starts a comment when it is the first character of a line or follows a blank that is
    not escaped, and stands outside quotes. So `$#`, `${#a}`, `a#b` and the
    fragment of a URL (`/#top`) are code, `"a # b"` is a string, and `echo hi  # x` keeps
    `echo hi`. A backslash outside single quotes escapes the next character. A quote is followed
    across lines, so an inner line of a quote that runs over several lines is code, and so is a
    heredoc body, up to its end line. Command substitutions nest their own quotes, `$'…'` takes
    escaped quotes, and in YAML an apostrophe inside a word is a letter (bead coding-harness-cff).
    It does not parse the shell: a quote it still misreads - an apostrophe in a shell script's
    plain text, an apostrophe in YAML that does not stand between two letters (`users'`), a quote
    in backticks, `<<$end` - flips the rest of the file, and the error runs
    both ways: a comment read as code can make a false link, and code read as a comment can lose
    one (finding F-10 of touch-map, a named limit).
    """
    kept = []
    state = OUTSIDE
    waiting: list[str] = []  # the delimiters of the heredocs opened above, whose bodies are still to be read
    for line in body.splitlines():
        if waiting:
            if line.strip() == waiting[0]:  # an indented end line counts: YAML takes the indent off first
                waiting.pop(0)
            kept.append(line)
            continue
        text, state, waiting = _scan(line, state, yaml)
        kept.append(text)
    return "\n".join(kept)


def read_code(path: str, body: str) -> Source:
    """The text a file executes: comments removed, and for Python docstrings too."""
    if path.endswith(".py"):
        try:
            tree = ast.parse(body)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
                    and node.body
                    and _is_docstring(node.body[0])
                ):
                    node.body[0] = ast.Pass()
            return Source(ast.unparse(tree), tree)  # unparse drops the comments
        except (SyntaxError, ValueError, RecursionError):
            pass  # a file that does not parse is read like a shell script
    return Source(_strip_comments(body, path.endswith((".yml", ".yaml"))), None)


class Snapshot:
    """The tracked files of one revision; source texts are read from git objects on first use."""

    def __init__(self, repo: str, rev: str) -> None:
        self.repo = repo
        self.rev = rev
        self._blobs: dict[str, str] = {}  # path -> object id, regular files only
        paths = []
        for record in git(repo, "ls-tree", "-r", "-z", "--full-tree", rev).split("\0"):
            if not record:
                continue
            meta, _, path = record.partition("\t")
            mode, otype, oid = meta.split()
            paths.append(path)
            if otype == "blob" and mode != "120000":
                self._blobs[path] = oid
        self.paths = sorted(paths)
        names = Counter(p.rsplit("/", 1)[-1] for p in self.paths)
        # Basename -> path, for the basenames that name one file and are long enough to mean it.
        self.long_unique = {
            p.rsplit("/", 1)[-1]: p
            for p in self.paths
            if names[p.rsplit("/", 1)[-1]] == 1 and len(p.rsplit("/", 1)[-1]) > BASENAME_LONGER_THAN
        }
        stems = Counter(p.rsplit("/", 1)[-1][:-3] for p in self.paths if p.endswith(".py"))
        # Stem -> path, for the `.py` stems that no second file shares.
        self.stems = {
            p.rsplit("/", 1)[-1][:-3]: p
            for p in self.paths
            if p.endswith(".py") and stems[p.rsplit("/", 1)[-1][:-3]] == 1
        }
        # Every `.py` stem, shared or not: an import of one of them is not dangling.
        self.py_stems = set(stems)
        # Every tail of a path after a `/` (and the whole path) -> the paths that end so.
        self.suffixes: dict[str, list[str]] = {}
        for p in self.paths:
            parts = p.split("/")
            for i in range(len(parts)):
                self.suffixes.setdefault("/".join(parts[i:]), []).append(p)
        self.sources = [p for p in self.paths if kind(p) != "other" and p in self._blobs]
        self._read: dict[str, Source] | None = None

    def source(self, path: str) -> Source:
        if self._read is None:
            self._read = self._load()
        return self._read[path]

    def _load(self) -> dict[str, Source]:
        wanted = sorted({self._blobs[p] for p in self.sources})
        blobs: dict[str, bytes] = {}
        if wanted:
            data = _git(self.repo, ["cat-file", "--batch"], ("\n".join(wanted) + "\n").encode())
            pos = 0
            while pos < len(data):
                end = data.index(b"\n", pos)
                header = data[pos:end].split()
                pos = end + 1
                if len(header) == 3 and header[1] == b"blob":
                    size = int(header[2])
                    blobs[header[0].decode()] = data[pos : pos + size]
                    pos += size + 1
        return {p: read_code(p, blobs.get(self._blobs[p], b"").decode("utf-8", "replace")) for p in self.sources}


def _full_paths(snap: Snapshot, src: str) -> set[str]:
    text = snap.source(src).text
    return {p for p in snap.paths if p != src and p in text}


def _joins(snap: Snapshot, tree: ast.Module) -> set[str]:
    """Tracked paths named by a chain of `/` joins that ends in string constants."""

    def operands(node: ast.expr) -> list[ast.expr]:
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return operands(node.left) + operands(node.right)
        return [node]

    divs = [n for n in ast.walk(tree) if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)]
    inner = {id(c) for n in divs for c in (n.left, n.right)}
    found: set[str] = set()
    for top in (n for n in divs if id(n) not in inner):
        try:
            parts = operands(top)
        except RecursionError:
            continue
        tail: list[str] = []
        for part in reversed(parts):
            if not (isinstance(part, ast.Constant) and isinstance(part.value, str)):
                break
            tail.append(part.value.strip("/"))
        joined = "/".join(s for s in reversed(tail) if s)
        hits = snap.suffixes.get(joined, [])
        if joined and len(hits) == 1:
            found.add(hits[0])
    return found


def names(snap: Snapshot, src: str, full: set[str] | None = None) -> set[str]:
    """The tracked files a source names: full path, unique long basename, and in Python a `/` join."""
    source = snap.source(src)
    found = set(_full_paths(snap, src) if full is None else full)
    found |= {p for name, p in snap.long_unique.items() if p != src and name in source.text}
    if source.tree is not None:
        found |= _joins(snap, source.tree)
    found.discard(src)
    return found


def _import_roots(tree: ast.Module) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def imported(snap: Snapshot, src: str) -> set[str]:
    """The tracked `.py` files a Python source imports (absolute imports, a unique stem)."""
    tree = snap.source(src).tree
    if tree is None:
        return set()
    return {snap.stems[r] for r in _import_roots(tree) if r in snap.stems} - {src}


Link = tuple[str, str, str]  # source, target, kind


def links(snap: Snapshot) -> set[Link]:
    """Every link of the revision, by the rules in the module docstring."""
    out: set[Link] = set()
    for src in snap.sources:
        src_kind = kind(src)
        full = _full_paths(snap, src)
        if src_kind != "runner" and len(full) >= REGISTRY_PATHS:
            continue  # a registry mentions, it does not depend
        if src_kind == "test":
            out |= {(src, t, "tests") for t in names(snap, src, full) | imported(snap, src)}
        elif src_kind == "code" and src.endswith(".py"):
            out |= {(src, t, "imports") for t in imported(snap, src)}
        else:  # a runner or a shell script
            for t in names(snap, src, full):
                target = kind(t)
                if target in ("code", "test"):
                    out.add((src, t, "runs"))
                elif target == "other":
                    out.add((src, t, "reads"))
    return out


def still_named(snap: Snapshot, path: str) -> list[str]:
    """The sources at this revision that still hold a removed file's path or import its stem.

    An import counts only while its stem resolves to no tracked `.py` file: when the module
    moved to another folder, the import now reaches the moved file and dangles nowhere.
    """
    stem = path.rsplit("/", 1)[-1][:-3] if path.endswith(".py") else None
    dangling = stem is not None and stem not in snap.py_stems
    out = []
    for src in snap.sources:
        source = snap.source(src)
        if path in source.text or (dangling and source.tree is not None and stem in _import_roots(source.tree)):
            out.append(src)
    return out


# --- what the pull request touches ----------------------------------------------------


@dataclass
class Touch:
    head: str  # short hash
    base: str  # short hash of the merge base
    status: dict[str, str]  # every changed file -> new | changed | removed
    boxes: list[str]  # the changed boxes, in list order
    unchanged: list[str]  # the unchanged boxes, by path
    links: list[Link]  # the drawn links, sorted
    folds: dict[str, int]  # a changed box -> how many unchanged tests link to it
    still_named: dict[str, list[str]]  # a removed box -> the sources at head that still name it
    not_linked: list[str]  # changed files that are neither boxes nor prose
    prose: int  # changed files that are prose and not boxes
    imports_added: list[tuple[str, str]] = field(default_factory=list)
    imports_dropped: list[tuple[str, str]] = field(default_factory=list)

    @property
    def size(self) -> int:
        """The box count, fold boxes included."""
        return len(self.boxes) + len(self.unchanged) + len(self.folds)


def _order(paths) -> list[str]:
    return sorted(paths, key=lambda p: (KIND_ORDER[kind(p)], p))


def build(repo: str, base: str, head: str) -> Touch:
    revs = resolve(repo, base, head)
    status = changed(repo, revs.merge_base, revs.head)
    snap = Snapshot(repo, revs.head)
    head_links = links(snap)
    removed = {p for p, s in status.items() if s == "removed"}
    code_py = {p for p in status if kind(p) == "code" and p.endswith(".py")}
    old_links: set[Link] = set()
    if removed or code_py:
        old_links = links(Snapshot(repo, revs.merge_base))
    # A removed file's links are read at the merge base.
    edges = head_links | {e for e in old_links if e[0] in removed or e[1] in removed}

    boxes = {p for p in status if kind(p) != "other"}
    for src, dst, _ in edges:  # a changed "other" file is a box when a test, runner or shell script links to it
        if dst in status and kind(dst) == "other" and (kind(src) in ("test", "runner") or is_shell(src)):
            boxes.add(dst)
    unchanged = set()
    for src, dst, _ in edges:
        if src not in status and kind(src) in ("code", "runner") and dst in boxes:
            unchanged.add(src)
        if src in status and kind(src) == "test" and dst not in status and kind(dst) in ("code", "runner"):
            unchanged.add(dst)
    folds = Counter(dst for src, dst, k in edges if k == "tests" and src not in status and dst in boxes)
    drawn = sorted(
        e
        for e in edges
        if e[0] in boxes | unchanged and e[1] in boxes | unchanged and (e[0] in status or e[1] in status)
    )

    rest = [p for p in status if p not in boxes]
    in_head = {(s, d) for s, d, k in head_links if k == "imports" and s in code_py}
    in_base = {(s, d) for s, d, k in old_links if k == "imports" and s in code_py}
    return Touch(
        head=revs.head_short,
        base=revs.merge_base_short,
        status=status,
        boxes=_order(boxes),
        unchanged=sorted(unchanged),
        links=drawn,
        folds=dict(sorted(folds.items())),
        still_named={p: still_named(snap, p) for p in sorted(removed & boxes)},
        not_linked=sorted(p for p in rest if not is_prose(p)),
        prose=sum(1 for p in rest if is_prose(p)),
        imports_added=sorted(in_head - in_base),
        imports_dropped=sorted(in_base - in_head),
    )


# --- the output -----------------------------------------------------------------------


def _flat(text: str) -> str:
    """No control character: a name with a newline would break its line."""
    return re.sub(r"[\x00-\x1f\x7f]", "?", text)


def _span(text: str) -> str:
    """`text` as a Markdown code span, whatever backticks it holds."""
    text = _flat(text)
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * (longest + 1)
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def _files(n: int) -> str:
    return "1 file" if n == 1 else f"{n} files"


def render_list(touch: Touch) -> list[str]:
    """One line per changed box, then the changed files that are not boxes."""
    lines = []
    for path in touch.boxes:
        groups: dict[str, list[str]] = {name: [] for name in GROUPS}
        for src, dst, k in touch.links:
            if dst == path:
                groups[INBOUND[k]].append(src)
            if src == path:
                groups[k].append(dst)
        groups["still named by"] = touch.still_named.get(path, [])
        parts = [f"- {_span(path)} ({touch.status[path]})"]
        for name in GROUPS:
            shown = [_span(short(p)) for p in sorted(groups[name], key=short)]
            if name == "tested by" and touch.folds.get(path):
                shown.append(f"+{touch.folds[path]} unchanged")
            if shown:
                parts.append(f"{name} {', '.join(shown)}")
        lines.append(" · ".join(parts))
    if touch.not_linked:
        lines.append("- Not linked: " + ", ".join(_span(p) for p in touch.not_linked))
    if touch.prose:
        lines.append(f"- Prose, not drawn: {_files(touch.prose)}")
    return lines


def _label(text: str) -> str:
    """A Mermaid label: one line, and no `"` or backtick whatever the file is called."""
    return _flat(text).replace('"', "'").replace("`", "'")


def render_map(touch: Touch) -> list[str]:
    """The lines of the `flowchart LR`: boxes, links, class definitions.

    Ids are `n1`, `n2`, ... in box order and never come from a file name: `a-b.py` and
    `a_b.py` would collide, and `end` closes a block in Mermaid.
    """
    order = touch.boxes + touch.unchanged
    folded = [p for p in touch.boxes if p in touch.folds]  # fold boxes follow their target's order
    number = {p: i for i, p in enumerate(order, 1)}
    fold_number = {p: len(order) + i for i, p in enumerate(folded, 1)}
    ident = {p: f"n{i}" for p, i in number.items()}
    fold_ident = {p: f"n{i}" for p, i in fold_number.items()}
    lines = ["flowchart LR"]
    for path in order:
        status = touch.status.get(path)
        text = f"code: {short(path)}" + (f" ({status})" if status else "")
        lines.append(f'  {ident[path]}["{_label(text)}"]:::{MAP_CLASS.get(status, "same")}')
    for path in folded:
        lines.append(f'  {fold_ident[path]}(["code: +{touch.folds[path]} unchanged tests"]):::same')
    links = [(number[s], number[d], k, "-->", ident[s], ident[d]) for s, d, k in touch.links]
    links += [(fold_number[p], number[p], "tests", "-.->", fold_ident[p], ident[p]) for p in folded]
    for *_, k, arrow, src, dst in sorted(links, key=lambda e: e[:3]):
        lines.append(f"  {src} {arrow}|{k}| {dst}")
    lines.extend(CLASSES)
    return lines


def _pairs(pairs: list[tuple[str, str]]) -> str:
    return ", ".join(f"{_span(a)} \u2192 {_span(b)}" for a, b in pairs) or "none"


def render_lists(touch: Touch) -> list[str]:
    """Added, changed and removed boxes, with the imports gained and dropped."""

    def paths(status: str) -> str:
        return ", ".join(_span(p) for p in touch.boxes if touch.status[p] == status) or "none"

    return [
        f"- **Added:** {paths('new')}. New imports: {_pairs(touch.imports_added)}.",
        f"- **Changed:** {paths('changed')}.",
        f"- **Removed:** {paths('removed')}. Imports dropped: {_pairs(touch.imports_dropped)}.",
    ]


def render(touch: Touch) -> str:
    """The whole section, ending in a newline.

    Without a box the section is one line when every changed file is prose; a changed file
    that is neither prose nor a box is named, so "Prose only" is never said of it.
    """
    if not touch.boxes and not touch.not_linked:
        return PROSE_ONLY + "\n"
    lines = [f"Touched at `{touch.head}`, against the merge base `{touch.base}`:", ""]
    lines += render_list(touch)
    notes = []
    if touch.size >= SPLIT_FROM:
        notes.append("Large change: consider splitting it.")
    has_links = bool(touch.links or touch.folds)
    if touch.size > MAP_MAX:
        notes.append(f"Map left out: {touch.size} boxes, more than {MAP_MAX}.")
        if has_links:  # the list prints links and no caption follows
            notes.append(LINKS_CAVEAT)
    if notes:
        lines += ["", *notes]
    if has_links and touch.size <= MAP_MAX:
        caption = (
            f"<sub>Generated by scripts/touch_map.py from the commit {touch.head} and the merge base {touch.base}; "
            f"nothing drawn by hand. {LINKS_CAVEAT} "
            "A box is a file at C4 level code; new, changed and removed show in words and in colour.</sub>"
        )
        lines += [
            "",
            f"<details><summary>Map at {touch.head}</summary>",
            "",
            "```mermaid",
            *render_map(touch),
            "```",
            "",
        ]
        lines += [*render_lists(touch), "", caption, "</details>"]
    return "\n".join(lines) + "\n"


def _write(text: str) -> None:
    """Standard output as UTF-8 whatever the locale (the list uses `·` and `→`)."""
    data = text.encode("utf-8")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        sys.stdout.flush()
        buffer.write(data)
        buffer.flush()
    else:
        sys.stdout.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="touch_map.py",
        description="What a pull request touches: a list and a collapsed Mermaid map, from git objects only.",
        allow_abbrev=False,
    )
    parser.add_argument("base", help="the revision the pull request merges into, e.g. origin/main")
    parser.add_argument("head", help="the revision of the pull request, e.g. HEAD")
    parser.add_argument("--repo", default=".", help="the repository (default: the current directory)")
    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code if isinstance(err.code, int) else 2
    try:
        text = render(build(args.repo, args.base, args.head))
    except CannotMeasure as err:
        print(f"touch-map: not measured: {err}", file=sys.stderr)
        return 3
    _write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
