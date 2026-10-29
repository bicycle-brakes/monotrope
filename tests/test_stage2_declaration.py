"""The shared model declaration reader stays current while reusing parses (bead coding-harness-dca4).

`stage2_availability.read_declaration` sits on every swarm call boundary, so it
may reuse a successful YAML parse of unchanged contents in a bounded
process-local cache only while the current file bytes still decide every read:
an edit at the same size and modification time, another repository's file and
every read, decode or parse failure must be seen, no refusal may go stale, and
no caller may receive another caller's object. Admission itself stays live:
the research send guard re-evaluates terms and the declaration on each launch
even when the parse is warm. The tests compare the reader against the baseline
contract (`yaml.safe_load(...) or {}` over the UTF-8 text) and count real YAML
parses through `yaml.load`, never timing.

The parse cache is process-local and survives between tests in one worker, so
every parse-counting test writes its own distinct declaration contents.

Each behavioral test's fault is the planted mutation that removes the guarantee
it names: reuse of a stale parse (criterion 2), a path or stat shortcut
(criterion 3), a cached refusal (criterion 4), a shared mutable result
(criterion 5), or admission decided from cached data at the send guard
(criterion 6).
"""

from __future__ import annotations

import datetime as dt
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402
import stage2_availability as availability  # noqa: E402
import stage2_research_run as research  # noqa: E402
from stage2_research_dispatch import GateVerdict, Slot  # noqa: E402
from terms_fixtures import admissible_terms  # noqa: E402

REFUSAL = "model-endpoints.yaml cannot be read"

NESTED = """\
endpunkte:
  - name: opencode-go
    residenz: "München — EU-Rechenzentrum ✓"
    darf_sehen: [framework, public-web]
    modelle_terms:
      m:
        gelesen: 2026-10-25
        valid_until: "2026-10-31"
        anfragen_5h: 100
        ratio: 0.5
        flags: [true, false, null, ~]
        counts: {a: 1, b: 2}
        note: |
          mehrere Zeilen
          mit Umlauten
anchored: &anchor
  key: value
  keep: [1, 2]
alias_user: *anchor
"""

# Documents whose full contract result must not differ from the baseline
# reader's, whatever it is: a value, the empty normalisation or the refusal.
CONTRACT_CASES = [
    ("nested", NESTED),
    ("empty file", ""),
    ("only comments", "# nothing here\n"),
    ("empty flow mapping", "{}\n"),
    ("empty flow sequence", "[]\n"),
    ("null document", "~\n"),
    ("zero document", "0\n"),
    ("false document", "false\n"),
    ("empty string document", '""\n'),
    ("positive number document", "5\n"),
    ("true document", "true\n"),
    ("plain text document", "hello\n"),
    ("sequence document", "- a\n- b\n"),
    ("date document", "2026-10-31\n"),
    ("unsafe python tag", '!!python/object/apply:os.system ["echo no"]\n'),
    ("unbalanced flow mapping", "a: {b: c\n"),
    ("tab indentation", "a:\n\tb: 1\n"),
    ("crlf line endings", "a: 1\r\nlist:\r\n  - x\r\n  - y\r\n"),
]


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """One repository root with no declaration yet."""
    directory = tmp_path / "repo"
    directory.mkdir()
    return directory


def baseline_reader(root: Path) -> dict | str:
    """The baseline reader verbatim: the contract `read_declaration` must keep."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return REFUSAL
    return data if isinstance(data, dict) else REFUSAL


def assert_same_value(left: object, right: object) -> None:
    """Equality with exact scalar types: 0 and False, or 1 and True, stand in for each other in `==`."""
    assert left == right, (left, right)
    assert type(left) is type(right), (left, right)
    if isinstance(left, dict):
        assert isinstance(right, dict)
        assert set(left) == set(right)
        for key in left:
            assert_same_value(left[key], right[key])
    if isinstance(left, list):
        assert isinstance(right, list)
        assert len(left) == len(right)
        for one, two in zip(left, right, strict=True):
            assert_same_value(one, two)


def patch_load_counter(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, object]]:
    """Count real YAML parses through `yaml.load`, recording each request's loader.

    `yaml.safe_load` resolves `load` in the yaml module at call time, so the
    baseline reader's parses are counted here too.
    """
    real_load = yaml.load
    calls: list[tuple[str, object]] = []

    def counting_load(text: str, *args: object, **kwargs: object) -> object:
        loader = kwargs.get("Loader", args[0] if args else None)
        calls.append((text, loader))
        return real_load(text, *args, **kwargs)

    monkeypatch.setattr(yaml, "load", counting_load)
    return calls


def write(root: Path, text: str) -> Path:
    """Write one declaration into the root and return its path."""
    path = root / "model-endpoints.yaml"
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Criterion 1: the reader keeps the baseline contract of the pure safe loader
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("label,text", CONTRACT_CASES, ids=[label for label, _ in CONTRACT_CASES])
def test_reader_matches_safe_load_contract(root: Path, label: str, text: str) -> None:
    """Criterion 1: values, scalar types, empty normalisation and refusals match the old reader."""
    write(root, text)
    expected = baseline_reader(root)
    got = availability.read_declaration(root)
    assert_same_value(got, expected)
    if label == "nested":
        entry = got["endpunkte"][0]
        assert entry["name"] == "opencode-go"
        assert entry["residenz"] == "München — EU-Rechenzentrum ✓"
        assert entry["darf_sehen"] == ["framework", "public-web"]
        terms = entry["modelle_terms"]["m"]
        assert type(terms["gelesen"]) is dt.date and terms["gelesen"] == dt.date(2026, 10, 25)
        assert type(terms["valid_until"]) is str and terms["valid_until"] == "2026-10-31"
        assert terms["flags"] == [True, False, None, None]
        assert terms["counts"] == {"a": 1, "b": 2}
        assert terms["note"] == "mehrere Zeilen\nmit Umlauten\n"
        assert got["alias_user"] == {"key": "value", "keep": [1, 2]}
    if isinstance(expected, str):
        assert got == REFUSAL


@pytest.mark.parametrize(
    "text",
    [
        "endpunkte: []\t# ordinary inline comment\n",
        "endpunkte: [] \t# spaced inline comment\n",
        "endpunkte:\t[]\n",
        "endpunkte: []\n\t# comment on its own line\n",
        'note: "a\tb"\n',
        "note: 'a\tb'\n",
        "note: |\n  a\tb\n",
        "# comment containing\ta tab\nendpunkte: []\n",
        'note: "\\uD83D\\uDE00"\n',
    ],
)
def test_reader_preserves_safe_loader_contract(root: Path, text: str) -> None:
    """F6-1 and F6-3: the reader accepts and refuses exactly what the old pure-SafeLoader reader did.

    Planted faults: libyaml's C loader accepts the tab separators and refuses the escaped surrogate
    pair, so a reader that parses with it turns several of these cases red.
    """
    write(root, text)
    expected = baseline_reader(root)
    # Repeat to exercise both an uncached read and any successful cached read.
    for _ in range(2):
        assert_same_value(availability.read_declaration(root), expected)


def test_reader_parses_with_the_pure_safe_loader(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 1: the pure safe loader parses whether or not libyaml is built in, and an unsafe tag is refused."""
    # Distinct contents: this test counts its own parses in the shared process-local cache.
    text = NESTED + "loader-test: unique\n"
    path = write(root, text)
    calls = patch_load_counter(monkeypatch)
    data = availability.read_declaration(root)
    assert isinstance(data, dict) and data["loader-test"] == "unique"
    assert len(calls) == 1
    assert calls[0][1] is yaml.SafeLoader, "the reader did not parse with the pure SafeLoader"

    # An unsafe tag is refused, not executed - planted fault: a full loader would return a mapping.
    path.write_text('!!python/object/apply:os.system ["echo no"]\n', encoding="utf-8")
    assert availability.read_declaration(root) == REFUSAL


# ---------------------------------------------------------------------------
# Criterion 2: unchanged contents reuse one parse, and the cache stays bounded
# ---------------------------------------------------------------------------


def test_unchanged_contents_reuse_a_bounded_parse_cache(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 2: immediate repeats parse once; distinct inputs evict the oldest entries.

    Planted fault on the baseline reader: it parses on every read, so the first
    assertion fails against the old code.
    """
    text = "reuse: yes\nmarker: bounded-cache-test\n"
    write(root, text)
    calls = patch_load_counter(monkeypatch)
    first = availability.read_declaration(root)
    for _ in range(2):
        again = availability.read_declaration(root)
        assert again == first
        assert again is not first, "a caller received the cached object itself"
    assert len(calls) == 1, "an unchanged declaration was parsed again on an immediate repeat"

    bound = availability._DECLARATION_CACHE_SIZE
    for number in range(bound + 1):
        write(root, f"{text}extra: {number}\n")
        assert availability.read_declaration(root) == {
            "reuse": True,
            "marker": "bounded-cache-test",
            "extra": number,
        }
    assert len(calls) == 2 + bound, "a distinct declaration reused an existing parse"
    assert len(availability._DECLARATION_CACHE) <= bound, "the parse cache grew beyond its bound"

    # The first contents have been evicted by the distinct inputs: reading them parses again.
    write(root, text)
    availability.read_declaration(root)
    assert len(calls) == 3 + bound, "the oldest entry survived: the cache is unbounded"


# ---------------------------------------------------------------------------
# Criterion 3: changed contents are read, whatever their metadata says
# ---------------------------------------------------------------------------


def test_changed_contents_are_read_without_metadata_shortcuts(
    root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Criterion 3: same-size, same-mtime edits, atomic replacement and another root are all seen."""
    warm_text = "model: alpha\nmodelle: [one, two]\n"
    edited_text = "model: omega\nmodelle: [one, two]\n"
    replaced_text = "model: gamma\nmodelle: [one, two]\n"
    other_text = "model: delta\nmodelle: [one, two]\n"
    calls = patch_load_counter(monkeypatch)

    def rewrite_with_old_stat(path: Path, text: str) -> None:
        """Replace the contents and restore the previous size-preserving stat pair."""
        before = path.stat()
        path.write_text(text, encoding="utf-8")
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        after = path.stat()
        assert after.st_size == before.st_size and after.st_mtime_ns == before.st_mtime_ns

    path = write(root, warm_text)
    assert availability.read_declaration(root) == {"model": "alpha", "modelle": ["one", "two"]}
    assert len(calls) == 1

    # An in-place edit invisible to size and mtime - planted fault: a stat-keyed cache returns "alpha".
    rewrite_with_old_stat(path, edited_text)
    assert availability.read_declaration(root) == {"model": "omega", "modelle": ["one", "two"]}

    # An atomic replacement, equally invisible to size and mtime.
    temporary = root / "declaration.tmp"
    temporary.write_text(replaced_text, encoding="utf-8")
    before = path.stat()
    temporary.replace(path)
    os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
    after = path.stat()
    assert (after.st_size, after.st_mtime_ns) == (before.st_size, before.st_mtime_ns)
    assert availability.read_declaration(root) == {"model": "gamma", "modelle": ["one", "two"]}

    # Another repository's declaration, at another path: a path-keyed cache would return "gamma".
    other = tmp_path / "other-repo"
    other.mkdir()
    write(other, other_text)
    assert availability.read_declaration(other) == {"model": "delta", "modelle": ["one", "two"]}

    # Both roots keep serving their own current contents, each parsing only once.
    assert availability.read_declaration(root) == {"model": "gamma", "modelle": ["one", "two"]}
    assert availability.read_declaration(other) == {"model": "delta", "modelle": ["one", "two"]}
    assert len(calls) == 4, "an unchanged declaration was parsed again"


# ---------------------------------------------------------------------------
# Criterion 4: a failed read returns the refusal, never a cached declaration
# ---------------------------------------------------------------------------


def test_read_failure_never_returns_a_cached_declaration(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 4: deletion, bad UTF-8, malformed YAML and a read error refuse; recovery needs a valid file."""
    text = "failure-test: warm\n"
    path = write(root, text)
    warm = availability.read_declaration(root)
    assert warm == {"failure-test": "warm"}

    # Deletion - planted fault: a cache over failures would return the warm mapping.
    path.unlink()
    assert availability.read_declaration(root) == REFUSAL
    # Restoring the same valid contents serves the mapping again: no stale refusal.
    write(root, text)
    assert availability.read_declaration(root) == warm

    # Invalid UTF-8 bytes fail the decode, then a valid file recovers.
    path.write_bytes(b"\xff\xfe: broken\n")
    assert availability.read_declaration(root) == REFUSAL
    write(root, text)
    assert availability.read_declaration(root) == warm

    # Malformed YAML fails the parse, and the refusal itself is not cached.
    calls = patch_load_counter(monkeypatch)
    malformed = "malformed: {b: c\n"
    path.write_text(malformed, encoding="utf-8")
    assert availability.read_declaration(root) == REFUSAL
    assert len(calls) == 1 and calls[0][0] == malformed
    assert availability.read_declaration(root) == REFUSAL
    assert len(calls) == 2 and calls[1][0] == malformed, "the malformed declaration was not parsed again"
    write(root, text)
    assert availability.read_declaration(root) == warm

    # A read error between two otherwise identical reads is not papered over either.
    def broken(_self: Path) -> bytes:
        raise OSError("injected read failure")

    with pytest.MonkeyPatch.context() as injection:
        injection.setattr(Path, "read_bytes", broken)
        assert availability.read_declaration(root) == REFUSAL
    assert availability.read_declaration(root) == warm


# ---------------------------------------------------------------------------
# Criterion 5: every caller owns its result, on the miss and across threads
# ---------------------------------------------------------------------------


def test_returned_declarations_are_isolated_across_threads(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 5: mutating a returned declaration never reaches another caller or a later read."""
    text = "isolation: yes\nnested:\n  list: [1, 2]\n  map: {keep: me}\n"
    write(root, text)
    pristine = {"isolation": True, "nested": {"list": [1, 2], "map": {"keep": "me"}}}

    # The first caller's result is already a copy - planted fault: handing out
    # the cache's own object lets this mutation reach every later read.
    miss = availability.read_declaration(root)
    assert miss == pristine
    miss["nested"]["map"]["keep"] = "mutated"
    miss["nested"]["list"].append(3)
    assert availability.read_declaration(root) == pristine, "the first caller's mutation polluted the cache"

    workers = 4
    barrier = threading.Barrier(workers, timeout=10)
    parsing = threading.Barrier(workers + 1, timeout=10)
    release = threading.Event()
    # A distinct key has never been read: every worker must reach the parser
    # before any worker can store it. Keep the earlier initial-miss check too.
    cold_text = text + f"cold-key: {root.as_posix()}\n"
    write(root, cold_text)
    pristine["cold-key"] = root.as_posix()
    real_load = yaml.load
    parses: list[str] = []

    def held_load(document: str, *args: object, **kwargs: object) -> object:
        if document == cold_text:
            parses.append(document)
            parsing.wait()
            assert release.wait(timeout=10), "cold parses were not released"
        return real_load(document, *args, **kwargs)

    monkeypatch.setattr(yaml, "load", held_load)

    def mutate_and_reread() -> dict:
        mine = availability.read_declaration(root)
        assert mine == pristine
        barrier.wait()  # everyone holds a result before anyone mutates
        mine["isolation"] = f"mutated-{threading.get_ident()}"
        mine["nested"]["list"].append(threading.get_ident())
        barrier.wait()  # everyone has mutated before anyone re-reads
        return availability.read_declaration(root)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(mutate_and_reread) for _ in range(workers)]
        try:
            parsing.wait()  # all workers missed the same key and are parsing
            assert len(parses) == workers
            # Evict entries while the cold parses are in flight, without
            # changing the declaration those workers will later re-read.
            other = root / "eviction"
            other.mkdir()
            bound = availability._DECLARATION_CACHE_SIZE
            for number in range(bound + 1):
                write(other, f"concurrent-eviction: {number}\n")
                assert availability.read_declaration(other) == {"concurrent-eviction": number}
            assert len(availability._DECLARATION_CACHE) == bound
            assert cold_text not in availability._DECLARATION_CACHE
        finally:
            release.set()
        # Future.result propagates every worker exception to pytest; an empty
        # result collection must never make the isolation assertion pass.
        after = [future.result(timeout=15) for future in futures]
    assert len(after) == workers
    assert all(item == pristine for item in after), "a nested mutation reached another caller's read"
    assert len(parses) == workers, "concurrent stores failed to retain the shared key"
    assert len(availability._DECLARATION_CACHE) == bound, "concurrent stores broke the cache bound"
    assert availability.read_declaration(root) == pristine


# ---------------------------------------------------------------------------
# Criterion 6: a warm cache keeps the research send guard live
# ---------------------------------------------------------------------------


def guard_declaration(model: str = "m") -> str:
    """A minimal declaration admitting one Go model for framework data on the day its terms end."""
    data = {
        "endpunkte": [
            {
                "name": "opencode-go",
                "residenz": "eu",
                "darf_sehen": ["framework"],
                "modelle_terms": {model: admissible_terms(valid_until="2026-10-31")},
            }
        ]
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def test_warm_cache_preserves_live_research_admission(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Criterion 6: the production send guard sees a declaration edit, expiry and deletion over a warm cache."""

    def scan(*_args: object, **_kwargs: object) -> SimpleNamespace:
        return SimpleNamespace(
            verdict=SimpleNamespace(render=lambda: "clean", exit_code=lambda: 0),
            files=1,
            commits=0,
            rules=1,
        )

    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 10, 31))
    monkeypatch.setattr(stage2.leakcheck, "check", scan)
    calls = patch_load_counter(monkeypatch)
    text = guard_declaration()
    path = write(root, text)
    entry = {"role": "repository", "endpoint": availability.GO, "model": "m"}
    run = SimpleNamespace(root=root, runner=stage2, change="demo", free=[], entries={"saved": entry})
    slot = Slot("saved", availability.GO, True, (0,), 60, {}, "research prompt")

    def gate() -> GateVerdict:
        return research.Run.gate(run, slot)

    # Warm: the guard admits on the expiry day, parsing the declaration exactly once.
    verdict = gate()
    assert not verdict.blocked, verdict.record
    assert gate().blocked is False
    assert len(calls) == 1, "an unchanged declaration was parsed again at the guard"

    # An edit is seen - planted fault: a guard over the cache would keep admitting "m".
    path.write_text(guard_declaration(model="other"), encoding="utf-8")
    verdict = gate()
    assert verdict.blocked and "does not declare the model m" in verdict.record["refused"], verdict.record
    assert len(calls) == 2, "the edited declaration was not read"

    # Restored contents hit the cache, and terms are still evaluated live across the UTC cutoff.
    path.write_text(text, encoding="utf-8")
    assert gate().blocked is False
    assert len(calls) == 2, "the restored declaration was parsed again"
    monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(2026, 11, 1))
    verdict = gate()
    assert verdict.blocked and "expired on 2026-10-31" in verdict.record["refused"], verdict.record
    assert len(calls) == 2, "expiry was decided by a fresh parse, not the live terms check"

    # A missing current file refuses instead of falling back to the cached mapping.
    path.unlink()
    verdict = gate()
    assert verdict.blocked and verdict.record["refused"] == REFUSAL, verdict.record
