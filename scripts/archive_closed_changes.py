#!/usr/bin/env python3
"""archive_closed_changes.py — moves change folders with a closed bead into the archive.

A change is finished when its bead is closed in the tracker; its folder then
leaves the active tree (`plans/_README.md`, "Three states, three places") —
but moving alone is not enough: the plans-registry coupling wants the archived
artefacts to read `accepted`/`done`, the freshness gate wants the moving day
in `updated:`, and a stale `plans/INDEX.md` is BLOCK. This command does the
whole move in one invocation and leaves every other byte alone (bead
coding-harness-cqun; the maintainer's answer stands in the change's
decisions.md Q-1: a tool, applied once to the backlog, then after every merge
next to `make close-merged`).

How it decides:

- A folder is ELIGIBLE when it is an immediate real directory under
  `plans/changes/` (the `archive` folder itself excepted), every registry
  artefact inside names the same nonempty bead, and that bead reads exactly
  `closed` in the validated tracker render of this invocation. Nothing else
  selects a folder — not the artefacts' `implementation_status`.
- Everything else is reported with a reason: open or unknown beads, folders
  without artefacts or with mixed/beadless artefacts — skipped, because they
  are not completion candidates — and folders that WOULD be eligible but
  cannot be interpreted safely (unreadable front matter, invalid header
  fields, a conflicting destination, a symlink on the source or archive
  boundary). A blocked folder refuses a write run before the first byte
  moves; silently leaving a finished change in the drift backlog is exactly
  what this command exists to end.
- The tracker state is read only through `bead_render.render_pfad()` (bead
  1jg.3), validated line by line (`check_bead_export.run`), and duplicate
  identifiers are rejected on top. An unavailable render is a failure, never
  an empty backlog.

How it writes (`--write`; without it the command is a report that changes
nothing):

- The whole eligible batch is preflighted before the first move. The four
  lifecycle fields (`status`, `implementation_status`, `updated`,
  `last_reviewed`) are rebuilt in memory; every other header value and the
  whole body stay byte for byte. The folder then moves with plain filesystem
  operations — companions (non-Markdown files, nested folders, empty
  folders) travel untouched — and `plans/INDEX.md` is replaced by the
  existing registry generator's output (`plans_registry.render_index()`),
  only when it differs.
- An I/O or index failure stops the run, exits nonzero and lists completed
  moves and unfinished work separately. All-or-nothing recovery is not
  promised: before source removal a failed copy leaves the source intact;
  after source removal starts, a failure keeps the verified destination and
  reports both paths, because the source may be partially removed. A rerun
  resumes source removal when the destination still matches the complete
  source (with its archived headers); conflicting copies remain blocked. It
  verifies the index even when nothing remains eligible; after success,
  unchanged inputs leave the tree byte-identical.

Exit codes: 0 = report written, or the batch archived cleanly (a rerun with
nothing eligible included); 1 = nothing measurable, a blocked folder during a
write run, or an I/O or index failure. No tracker write, no Git, no shell, no
mutating subprocess. Without BEAD_RENDER the tracker reader runs a read-only
`tools/bd export` subprocess to create a temporary render; the checkout is
resolved from this script's location, linked worktrees included.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_SCRIPTS))

import bead_render  # noqa: E402 — the ONE tracker access point (bead 1jg.3)
import check_bead_export  # noqa: E402 — the render's line-by-line check
import plans_registry  # noqa: E402 — artefact selection and the index generator

REPO = Path(__file__).resolve().parent.parent
CHANGES = REPO / "plans" / "changes"
ARCHIVE = CHANGES / "archive"

# The registry's field vocabulary, reused — never restated here.
REQUIRED = plans_registry.REQUIRED
STATUS = plans_registry.STATUS
IMPLEMENTATION = plans_registry.IMPLEMENTATION

# The only four header fields archiving edits; every other header value and
# the whole body are preserved byte for byte (decisions.md, header
# normalisation detail). The archive day stamps the two dates.
LIFECYCLE = ("status", "implementation_status", "updated", "last_reviewed")
NEW_STATUS = "accepted"
NEW_IMPLEMENTATION = "done"

# A top-level header key opens at column 0; nested lines are indented and a
# plain value keeps its colon off the line end. Quoted keys never match —
# `_uneditable` refuses them instead of appending a duplicate.
_HEADER_KEY = re.compile(r"([A-Za-z0-9_.-]+):(?:\s|$)")


class PreflightError(RuntimeError):
    """A precondition failed — nothing may be attempted."""


class SourceRemovalError(OSError):
    """The verified destination must survive a failed source removal."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """A SafeLoader that refuses a mapping with the same key twice.

    The registry's own reader keeps the last of a duplicate pair silently;
    for a write run that is not readable enough — the header would be
    rewritten around a guess. Duplication is malformed evidence here.
    """


def _construct_unique_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    seen: set[object] = set()
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in seen
            if not duplicate:
                seen.add(key)
        except TypeError:
            duplicate = False  # an unhashable key fails on its own when built
        if duplicate:
            raise yaml.YAMLError(f"duplicate mapping key: {key!r}")
    # dict(): construct_pairs alone yields a list of pairs — an unconverted
    # return made yaml.load hand every header back as a non-mapping, and no
    # folder was ever selectable (attempt-1 post-run diagnosis).
    return dict(loader.construct_pairs(node, deep))


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


@dataclass
class Artefact:
    """One registry artefact of a change folder, with its split front matter."""

    path: Path
    text: str
    header: str  # the lines between the fences, without either fence
    tail: str  # from the closing fence onward, untouched
    meta: dict


@dataclass
class Eligible:
    """One folder the run may move, and everything known about the move."""

    name: str
    src: Path
    dst: Path
    bead: str
    artefacts: list[Artefact]


def _today() -> dt.date:
    """The archiving day, captured once per invocation (decisions.md detail)."""
    return dt.date.today()


def _display(path: Path) -> str:
    """Repository-relative where possible — the manifest names clickable paths."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def _first_line(text: str) -> str:
    lines = text.splitlines()
    return lines[0] if lines else text


def _split_front_matter(text: str) -> tuple[str, str] | None:
    """Locate the registry-readable header without normalizing original bytes.

    Path.read_text in the registry uses universal newlines (LF, CRLF, CR).
    Keep an offset map so its fence search also works on the original text;
    this splitter only locates editable spans, never decides metadata.
    """
    normalized: list[str] = []
    offsets: list[int] = []
    for match in re.finditer(r"\r\n|\r|[^\r]", text):
        offsets.append(match.start())
        normalized.append("\n" if match.group().startswith("\r") else match.group())
    offsets.append(len(text))
    view = "".join(normalized)
    if not view.startswith("---\n"):
        return None
    end = view.find("\n---", 4)
    if end == -1:
        return None
    return text[offsets[4] : offsets[end]], text[offsets[end] :]


def _load_artefact(path: Path) -> tuple[Artefact | None, str]:
    """Read and parse one artefact; (None, reason) when it cannot be interpreted."""
    try:
        meta = plans_registry._frontmatter(path)
        raw = path.read_bytes()
    except UnicodeDecodeError:
        return None, "is not valid UTF-8"
    except OSError as exc:
        return None, f"cannot be read ({exc.strerror or exc})"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "is not valid UTF-8"
    split = _split_front_matter(text)
    if meta is None or split is None:
        return None, "has no readable front-matter block"
    header, tail = split
    try:
        # Metadata comes from the registry; this additional load only refuses
        # duplicate keys that its read-only parser tolerates.
        yaml.load(header, Loader=_UniqueKeyLoader)
    except (yaml.YAMLError, TypeError) as exc:
        # TypeError: an unhashable mapping key — the header cannot become the
        # mapping the registry fields live in, so it is malformed evidence.
        return None, f"has unreadable front matter ({_first_line(str(exc))})"
    if not isinstance(meta, dict):
        return None, "front matter is not a mapping"
    return Artefact(path=path, text=text, header=header, tail=tail, meta=meta), ""


def _readable_date(value: object) -> dt.date | None:
    """A plain calendar date, as YAML or ISO text — nothing else."""
    if isinstance(value, dt.datetime):
        return None
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        with contextlib.suppress(ValueError):
            return dt.date.fromisoformat(value)
    return None


def _invalid_field(art: Artefact) -> str:
    """The first invalid required field, or '' when the header is fully valid."""
    meta = art.meta
    for name in REQUIRED:
        if name not in meta:
            return f"required field '{name}' is missing"
        if meta.get(name) in (None, ""):
            return f"required field '{name}' is empty"
    status = meta.get("status")
    if not isinstance(status, str) or status not in STATUS:
        return f"status {status!r} is none of {sorted(STATUS)}"
    implementation = meta.get("implementation_status")
    if not isinstance(implementation, str) or implementation not in IMPLEMENTATION:
        return f"implementation_status {implementation!r} is none of {sorted(IMPLEMENTATION)}"
    for name in ("date", "last_reviewed"):
        if _readable_date(meta.get(name)) is None:
            return f"{name} {meta.get(name)!r} is not a readable date"
    if not isinstance(meta.get("bead"), str):
        return "bead is not a string"
    return ""


def _uneditable(art: Artefact) -> str:
    """'' when every lifecycle field is a findable, single-line plain scalar.

    The edit is line surgery, so a quoted or otherwise unusual key spelling
    would be appended as a second mapping key. Non-plain or multiline values
    could leave continuation lines behind; anchors could leave dangling aliases.
    Refuse these forms and explicit tags before any move.
    """
    line_keys = {key for line in re.split(r"\r\n|\r|\n", art.header) if (key := _header_key(line))}
    for name in LIFECYCLE:
        if (name in art.meta) != (name in line_keys):
            return f"the '{name}' header line cannot be edited safely (quoted or indented key)"
    # Parsing preserves scalar style and source spans that the constructed
    # Python values lose (e.g. `|-\n  draft` also constructs the string draft).
    # The header has already passed the unique-key YAML loader.
    node = yaml.compose(art.header, Loader=_UniqueKeyLoader)
    # A composed scalar's style does not reveal anchors or explicit tags.
    # Require its entire source span to be exactly one plain scalar token:
    # properties such as &state or !!str extend the node beyond that token.
    # Aliases resolve to the original node, whose line fails the check below.
    plain_scalar_spans = {
        (token.start_mark.index, token.end_mark.index)
        for token in yaml.scan(art.header, Loader=_UniqueKeyLoader)
        if isinstance(token, yaml.ScalarToken) and token.plain
    }
    for key, value in node.value:
        if key.value in LIFECYCLE and (
            not isinstance(value, yaml.ScalarNode)
            or (value.start_mark.index, value.end_mark.index) not in plain_scalar_spans
            or value.style is not None
            or value.start_mark.line != key.start_mark.line
            or value.end_mark.line != key.start_mark.line
            or not value.value
        ):
            return f"the '{key.value}' header value must be a single-line plain scalar"
    return ""


def _header_key(line: str) -> str:
    """The top-level key a header line opens, or '' — nested lines never match."""
    matched = _HEADER_KEY.match(line)
    return matched.group(1) if matched else ""


def _artefact_bead(art: Artefact) -> str:
    """The artefact's bead, or '' when it names none."""
    bead = art.meta.get("bead")
    return bead if isinstance(bead, str) and bead else ""


def _folder_artefacts(folder: Path) -> list[Path]:
    """The registry's own artefact selection, restricted to one change folder."""
    return [p for p in plans_registry.artefacts() if folder in p.parents]


def _active_folders() -> list[Path]:
    """Immediate real directories under plans/changes, archive excluded, sorted.

    Symlinks are never followed — the same rule `run_report.active_changes`
    applies, so a link cannot pull a foreign folder into the batch.
    """
    if CHANGES.is_symlink():
        raise PreflightError("plans/changes is a symlink, not a real directory")
    try:
        entries = sorted(CHANGES.iterdir())
    except OSError as exc:
        raise PreflightError(f"plans/changes cannot be listed: {exc}") from None
    return [entry for entry in entries if entry.name != "archive" and entry.is_dir() and not entry.is_symlink()]


def _tracker_state() -> tuple[Path, dict[str, str]]:
    """The render path plus its validated `id -> status`, duplicate ids refused."""
    try:
        render = bead_render.render_pfad()
    except (OSError, bead_render.RendererNichtMoeglich, SystemExit) as exc:
        raise PreflightError(f"the tracker render is not readable: {exc}") from None
    findings = check_bead_export.run(render)
    if findings:
        raise PreflightError("the tracker render is not valid: " + "; ".join(findings))
    try:
        lines = render.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise PreflightError(f"the tracker render is not readable: {exc}") from None
    statuses: dict[str, str] = {}
    for line in lines:
        if not line.strip():
            continue
        row = json.loads(line)  # every line is a validated JSON object with id and status
        bead_id = row["id"]
        if bead_id in statuses:
            raise PreflightError(f"the tracker render names bead '{bead_id}' twice — duplicates cannot be told apart")
        statuses[bead_id] = row["status"]
    return render, statuses


def _walk_error(error: OSError) -> None:
    """Never let an unreadable subtree disappear from a walk."""
    raise OSError(f"cannot list {error.filename}: {error}") from error


def _tree_bytes(root: Path, artefacts: dict[Path, Artefact], day: dt.date) -> dict[Path, bytes | None]:
    """A complete tree, with expected archived headers when reading a source."""
    tree: dict[Path, bytes | None] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False, onerror=_walk_error):
        base = Path(directory)
        tree[base.relative_to(root)] = None
        for name in [*dirnames, *filenames]:
            member = base / name
            if member.is_symlink():
                raise OSError(f"symlink inside the folder: {_display(member)}")
        for name in filenames:
            member = base / name
            art = artefacts.get(member)
            tree[member.relative_to(root)] = _edited_text(art, day).encode("utf-8") if art else member.read_bytes()
    return tree


def _destination_block(dst: Path, src: Path, artefacts: list[Artefact], day: dt.date) -> str:
    """Preflight both trees; only an exact verified copy is resumable."""
    if CHANGES.is_symlink():
        return "plans/changes is a symlink, not a real directory"
    if ARCHIVE.is_symlink() or (ARCHIVE.exists() and not ARCHIVE.is_dir()):
        return "the archive is not a real directory (a file or a symlink)"
    if not ARCHIVE.exists():
        if not CHANGES.is_dir() or not os.access(CHANGES, os.W_OK):
            return "the archive directory cannot be created (plans/changes is not a writable directory)"
    elif not os.access(ARCHIVE, os.W_OK):
        return "the archive directory is not writable"
    expected = _tree_bytes(src, {art.path: art for art in artefacts}, day)
    if dst.exists() or dst.is_symlink():
        if not dst.is_symlink() and dst.is_dir() and _tree_bytes(dst, {}, day) == expected:
            return ""
        return f"the destination already exists: {_display(dst)}"
    return ""


def _classify(
    statuses: dict[str, str], day: dt.date
) -> tuple[list[Eligible], list[tuple[str, str]], list[tuple[str, str]]]:
    """The eligible folders plus a reason for every skipped or blocked one.

    A folder whose bead reads closed is "otherwise eligible": when its
    evidence cannot be interpreted safely it is blocked, not skipped, and a
    write run refuses (spec criterion 6). Bead state alone decides
    eligibility — the artefacts' implementation_status is never read here.
    """
    eligible: list[Eligible] = []
    blocked: list[tuple[str, str]] = []
    skipped: list[tuple[str, str]] = []
    for folder in _active_folders():
        where = _display(folder)
        artefact_paths = _folder_artefacts(folder)
        if not artefact_paths:
            skipped.append((where, "no registry artefacts (nothing to classify)"))
            continue
        loaded: list[Artefact] = []
        broken: list[tuple[str, str]] = []
        for path in artefact_paths:
            art, reason = _load_artefact(path)
            if art is None:
                broken.append((_display(path), reason))
            else:
                loaded.append(art)
        beads = sorted({_artefact_bead(art) for art in loaded} - {""})
        beadless = [art for art in loaded if not _artefact_bead(art)]
        otherwise_eligible = len(beads) == 1 and not beadless and statuses.get(beads[0]) == "closed"
        if broken:
            where_broken, reason = broken[0]
            finding = f"{where_broken} {reason}"
            if otherwise_eligible:
                blocked.append((where, finding))
            else:
                skipped.append((where, finding))
            continue
        if not beads:
            skipped.append((where, "no artefact names a bead"))
            continue
        if beadless:
            skipped.append((where, "artefacts do not all name the same bead (some name none)"))
            continue
        if len(beads) > 1:
            skipped.append((where, "artefacts name different beads: " + ", ".join(beads)))
            continue
        bead = beads[0]
        status = statuses.get(bead)
        if status is None:
            skipped.append((where, f"bead {bead} does not appear in the tracker render"))
            continue
        if status != "closed":
            skipped.append((where, f"bead {bead} is open (status: {status})"))
            continue
        malformed = [
            (art, why)
            for art in loaded
            if (why := _uneditable(art) or _invalid_field(art) or _round_trip_error(art, day))
        ]
        if malformed:
            art, why = malformed[0]
            blocked.append((where, f"{_display(art.path)}: {why}"))
            continue
        dst = ARCHIVE / f"{day.isoformat()}-{folder.name}"
        reason = _destination_block(dst, folder, loaded, day)
        if reason:
            blocked.append((where, reason))
            continue
        eligible.append(Eligible(name=folder.name, src=folder, dst=dst, bead=bead, artefacts=loaded))
    return eligible, blocked, skipped


def _edited_text(art: Artefact, day: dt.date) -> str:
    """The artefact's text with only the four lifecycle fields rewritten.

    Lines are edited in place and a missing field is appended at the end of
    the header; everything else — values, comments, fences, body — keeps its
    exact bytes.
    """
    values = {
        "status": NEW_STATUS,
        "implementation_status": NEW_IMPLEMENTATION,
        "updated": day.isoformat(),
        "last_reviewed": day.isoformat(),
    }
    prefix = art.text[: len(art.text) - len(art.header) - len(art.tail)]
    newline = prefix[3:]
    # Keep separators as tokens: mixed line endings and unrelated header
    # lines must survive too. Newly inserted lines use the opening newline.
    lines = re.split(r"(\r\n|\r|\n)", art.header)
    for key, value in values.items():
        target = f"{key}: {value}"
        for index in range(0, len(lines), 2):
            line = lines[index]
            if _header_key(line) == key:
                if line != target:
                    lines[index] = target
                break
        else:
            lines.extend([newline, target])
    return prefix + "".join(lines) + art.tail


def _round_trip_error(art: Artefact, day: dt.date) -> str:
    """Refuse any edit the registry cannot read back with exactly the expected metadata.

    Exercise the actual file reader on a temporary copy during whole-batch
    preflight. Never use a source or destination as the validation scratchpad:
    a later invalid header must leave even earlier eligible folders untouched.
    """
    expected = dict(art.meta)
    expected.update(
        status=NEW_STATUS,
        implementation_status=NEW_IMPLEMENTATION,
        updated=day,
        last_reviewed=day,
    )
    with tempfile.NamedTemporaryFile(prefix="archive-header-", suffix=".md") as scratch:
        scratch.write(_edited_text(art, day).encode("utf-8"))
        scratch.flush()
        reread, reason = _load_artefact(Path(scratch.name))
    if reread is None:
        return f"header round-trip failed: edited front matter {reason}"
    if reread.meta != expected:
        return (
            "header round-trip failed: edited metadata differs from the expected lifecycle fields and preserved values"
        )
    return ""


def _manifest(entry: Eligible) -> list[str]:
    """Every prospective directory and file, companions marked."""
    artefact_paths = {art.path for art in entry.artefacts}
    lines: list[str] = []
    for root, dirnames, filenames in os.walk(entry.src, followlinks=False, onerror=_walk_error):
        dirnames.sort()
        directory = Path(root)
        target_dir = entry.dst / directory.relative_to(entry.src)
        lines.append(f"{_display(directory)}/ -> {_display(target_dir)}/ (directory)")
        for filename in sorted(filenames):
            source = Path(root) / filename
            target = entry.dst / source.relative_to(entry.src)
            marker = "" if source in artefact_paths else " (companion)"
            lines.append(f"{_display(source)} -> {_display(target)}{marker}")
    return lines


def _print_entry(entry: Eligible, lead: str) -> None:
    print(f"{lead} {_display(entry.src)} (bead {entry.bead}, closed)")
    for line in _manifest(entry):
        print(f"  {line}")


def _relocate(src: Path, dst: Path, artefacts: dict[Path, Artefact], day: dt.date) -> None:
    """Move the whole folder: edited artefacts, untouched companions, then the source goes.

    Raises OSError on the first failing operation; the caller reports the
    folder as unfinished. Copy failures permit destination cleanup; source
    removal failures preserve the verified destination for recovery.
    """
    if dst.exists():
        if _tree_bytes(dst, {}, day) != _tree_bytes(src, artefacts, day):
            raise OSError(f"retained destination no longer matches source: {_display(dst)}")
        try:
            shutil.rmtree(src)
        except OSError as exc:
            raise SourceRemovalError(str(exc)) from exc
        return
    dst.mkdir(parents=True)
    edited: list[tuple[Path, bytes]] = []
    companions: list[tuple[Path, Path]] = []
    for root, dirnames, filenames in os.walk(src, followlinks=False, onerror=_walk_error):
        base = Path(root)
        dirnames.sort()
        (dst / base.relative_to(src)).mkdir(parents=True, exist_ok=True)
        for filename in sorted(filenames):
            source = base / filename
            target = dst / source.relative_to(src)
            art = artefacts.get(source)
            if art is None:
                companions.append((source, target))
            else:
                edited.append((target, _edited_text(art, day).encode("utf-8")))
    for target, payload in edited:
        target.write_bytes(payload)
    for source, target in companions:
        shutil.copy2(source, target)
    # Read back the entire copy before deleting even the first source byte.
    for target, payload in edited:
        if target.read_bytes() != payload:
            raise OSError(f"copy verification failed: {target}")
    for source, target in companions:
        if target.read_bytes() != source.read_bytes():
            raise OSError(f"copy verification failed: {target}")
    try:
        shutil.rmtree(src)
    except OSError as exc:
        raise SourceRemovalError(str(exc)) from exc


def _remove_partial(dst: Path) -> bool:
    """Best-effort removal of a half-written destination; True when it is gone."""
    if not (dst.exists() or dst.is_symlink()):
        return True
    try:
        shutil.rmtree(dst)
    except OSError:
        return False
    return True


def _regenerate_index() -> tuple[str, str | None]:
    """(summary, failure reason) of one index regeneration.

    The index comes from the existing registry generator — never from a
    second implementation of its format — and is replaced only when it
    differs, so a repeat run rewrites nothing.
    """
    index = plans_registry.INDEX
    try:
        rendered = plans_registry.render_index()
        current = index.read_text(encoding="utf-8") if index.exists() else None
        mode = index.stat().st_mode & 0o7777 if current is not None else None
    except Exception as exc:
        return "", f"not regenerated — the registry generator failed: {exc}"
    if current == rendered:
        return "already current", None
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=index.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(rendered)
        if mode is not None:
            temporary.chmod(mode)
        temporary.replace(index)
    except OSError as exc:
        return "", f"not regenerated — the write failed: {exc}"
    finally:
        if temporary is not None:
            with contextlib.suppress(OSError):
                temporary.unlink(missing_ok=True)
    return "regenerated from the registry generator", None


def _report_failure(completed: list[str], unfinished: list[str]) -> None:
    print("archive: FINISHED WITH FAILURES — the batch is not all-or-nothing:", file=sys.stderr)
    print("completed moves:", file=sys.stderr)
    for line in completed:
        print(f"  - {line}", file=sys.stderr)
    print("unfinished work:", file=sys.stderr)
    for line in unfinished:
        print(f"  - {line}", file=sys.stderr)


def _write_batch(eligible: list[Eligible], day: dt.date) -> int:
    """Archive every eligible folder, then the index; 0 only when all went well."""
    completed: list[str] = []
    unfinished: list[str] = []
    try:
        manifests = [_manifest(entry) for entry in eligible]
    except OSError as exc:
        _report_failure([], [f"manifest unreadable — nothing moved: {exc}"])
        return 1
    for position, entry in enumerate(eligible):
        print(f"archiving {_display(entry.src)} (bead {entry.bead}, closed)")
        for line in manifests[position]:
            print(f"  {line}")
        artefacts = {art.path: art for art in entry.artefacts}
        retained_destination = entry.dst.exists()
        try:
            _relocate(entry.src, entry.dst, artefacts, day)
        except SourceRemovalError as exc:
            unfinished.append(
                f"{_display(entry.src)}: source removal failed — {exc}; source may be partially removed; "
                f"complete verified destination retained at {_display(entry.dst)}; "
                "plans/INDEX.md not regenerated; rerun resumes removal only if both trees still match"
            )
        except OSError as exc:
            cleaned = False if retained_destination else _remove_partial(entry.dst)
            note = f"{_display(entry.src)}: not moved — {exc} (source left in place; "
            if cleaned:
                note += "partial destination removed)"
            else:
                note += f"PARTIAL DESTINATION REMAINS at {_display(entry.dst)})"
            unfinished.append(note)
        if unfinished:
            unfinished.extend(f"{_display(pending.src)}: not attempted" for pending in eligible[position + 1 :])
            break
        completed.append(f"{_display(entry.src)} -> {_display(entry.dst)}")
        print(f"archived {_display(entry.src)}")
    if unfinished:
        _report_failure(completed, unfinished)
        return 1
    if not completed:
        print("archive: nothing to archive — no eligible closed folder is left active")
    summary, failure = _regenerate_index()
    if failure is not None:
        _report_failure(completed, [f"plans/INDEX.md: {failure}"])
        return 1
    print(f"archive: {len(completed)} folder(s) archived; plans/INDEX.md {summary}")
    return 0


def _report(
    eligible: list[Eligible],
    blocked: list[tuple[str, str]],
    skipped: list[tuple[str, str]],
    day: dt.date,
    render: Path,
) -> None:
    source = "preset render" if bead_render.quelle(render) == bead_render.QUELLE_VORGESETZT else "fresh render"
    print(f"archive: report for {day.isoformat()} — tracker render: {_display(render)} ({source})")
    for entry in eligible:
        _print_entry(entry, "would archive")
    for where, reason in blocked:
        print(f"blocked {where}: {reason}")
    for where, reason in skipped:
        print(f"skipped {where}: {reason}")
    print(
        f"archive: {len(eligible)} eligible, {len(skipped)} skipped, {len(blocked)} blocked — "
        "nothing written (report only; rerun with --write to move)"
    )


def _refuse(blocked: list[tuple[str, str]]) -> int:
    print(
        f"archive: write refused — {len(blocked)} folder(s) cannot be interpreted safely; nothing modified:",
        file=sys.stderr,
    )
    for where, reason in blocked:
        print(f"blocked {where}: {reason}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Archive change folders whose bead is closed: headers stamped, folder moved, index regenerated.",
        epilog="Without --write this is a report only — no repository file and no tracker state changes.",
    )
    parser.add_argument("--write", action="store_true", help="move the eligible folders; without it, only report")
    args = parser.parse_args(argv)
    day = _today()
    try:
        render, statuses = _tracker_state()
        eligible, blocked, skipped = _classify(statuses, day)
    except (PreflightError, OSError, UnicodeError) as exc:
        print(f"archive: cannot measure — nothing attempted: {exc}", file=sys.stderr)
        return 1
    if not args.write:
        try:
            _report(eligible, blocked, skipped, day, render)
        except OSError as exc:
            print(f"archive: cannot report — nothing attempted: {exc}", file=sys.stderr)
            return 1
        return 0
    if blocked:
        return _refuse(blocked)
    return _write_batch(eligible, day)


if __name__ == "__main__":
    sys.exit(main())
