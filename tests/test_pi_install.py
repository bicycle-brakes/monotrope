"""The pinned-Pi installer and wrapper in `tools/pi/` - success and every refusal.

Each case builds a fake `tools/pi` directory in a temporary tree: the real
`install.sh` and wrapper scripts are copied in verbatim, and around them stand
synthetic `node` and `npm` executables that implement exactly the call shapes
the two scripts use, a fixture package that stands for the installed Pi, and a
hostile `pi` on PATH that marks every run. A fallback to a global Pi, a silent
auto-install or a lifecycle script cannot hide. Nothing here contacts a
registry or a real install.

Each test comes with its fault: the mutated installer or the broken metadata is
planted one variant at a time and named in the test.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PKG = "@earendil-works/pi-coding-agent"
PIN = "1.2.0"
NODE_OK = "26.9.9"  # a same-major patch of the declared 26.9.0: stays eligible
NODE_WRONG = "27.4.1"  # another major: refused before Pi starts
INTEGRITY = "sha512-abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQR=="
GUIDANCE = "bash tools/pi/install.sh"


def write_exec(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


# A synthetic node: it answers exactly the shapes tools/pi/install.sh and
# tools/pi/pi use - the major probe, the two pin-check snippets (recognised by
# their marker comments, executed with the same semantics a real node gives
# them) and running the local CLI file. Anything else is a loud refusal.
SYNTHETIC_NODE = """#!@PYTHON@
import json
import os
import sys
from pathlib import Path

version = os.environ.get("FAKE_NODE_VERSION", "")
argv = sys.argv[1:]
if not version:
    sys.stderr.write("synthetic node: FAKE_NODE_VERSION is not set\\n")
    raise SystemExit(3)
if len(argv) == 2 and argv[0] == "-p" and "process.versions" in argv[1]:
    print(version.split(".")[0])
elif len(argv) >= 3 and argv[0] == "-e" and "pin-check:version" in argv[1]:
    pkg = json.loads(Path(argv[2]).read_text())
    said = pkg.get("version")
    sys.stdout.write(said if isinstance(said, str) else "")
elif len(argv) >= 3 and argv[0] == "-e" and "pin-check:bin" in argv[1]:
    pkg = json.loads(Path(argv[2]).read_text())
    bin_entry = pkg.get("bin")
    bin_entry = bin_entry if isinstance(bin_entry, str) else (bin_entry or {}).get("pi")
    sys.stdout.write(bin_entry if isinstance(bin_entry, str) else "")
elif argv and Path(argv[0]).is_file():
    os.execv(argv[0], [argv[0], *argv[1:]])
else:
    sys.stderr.write(f"synthetic node: unexpected call: {argv}\\n")
    raise SystemExit(3)
"""

# A synthetic npm: it carries out exactly the `npm ci` contract install.sh
# relies on, against local fixture packages - refuse a manifest/lock mismatch,
# refuse broken integrity values, materialise node_modules from the fixtures,
# and run lifecycle scripts only when --ignore-scripts is absent. It contacts
# nothing and logs every call.
SYNTHETIC_NPM = """#!@PYTHON@
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

argv = sys.argv[1:]
with Path(os.environ["FAKE_NPM_LOG"]).open("a") as handle:
    handle.write(json.dumps({"argv": argv, "cwd": os.getcwd()}) + "\\n")


def refuse(reason):
    sys.stderr.write(f"npm error code ECONTRACT\\nnpm error {reason}\\n")
    raise SystemExit(1)


if not argv or argv[0] != "ci":
    refuse(f"synthetic npm only implements ci, not: {argv}")
ignore_scripts = "--ignore-scripts" in argv[1:]
cwd = Path.cwd()
manifest = json.loads((cwd / "package.json").read_text())
lock = json.loads((cwd / "package-lock.json").read_text())
if lock.get("packages", {}).get("", {}).get("dependencies", {}) != manifest.get("dependencies", {}):
    refuse("npm ci can only install with an intact dependency graph: package.json and package-lock.json are not in sync")
packages = {k: v for k, v in lock.get("packages", {}).items() if k.startswith("node_modules/")}
fixtures = Path(os.environ["FAKE_NPM_FIXTURES"])
installed = []
for key, entry in packages.items():
    name = key[len("node_modules/"):]
    integrity = entry.get("integrity", "")
    if not re.fullmatch(r"sha512-[A-Za-z0-9+/]+={0,2}", integrity):
        refuse(f"integrity mismatch for {name}: {integrity!r}")
    source = fixtures / f"{name.replace('/', '-')}-{entry.get('version')}"
    if not source.is_dir():
        refuse(f"no fixture package for {name}@{entry.get('version')}")
    destination = cwd / "node_modules" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    installed.append(destination)

if not ignore_scripts:
    for destination in installed:
        scripts = json.loads((destination / "package.json").read_text()).get("scripts", {})
        for hook in ("preinstall", "install", "postinstall"):
            if hook in scripts:
                subprocess.run(["/bin/sh", "-c", scripts[hook]], check=True)
"""

# The local CLI the wrapper must end in: it proves it was started, from where,
# with which arguments and which environment - the stand-in a successful
# wrapper run bottoms out in.
LOCAL_CLI = """#!@PYTHON@
# synthetic local Pi CLI: records the run the wrapper gave it.
import json
import os
import sys
from pathlib import Path

with Path(os.environ["FAKE_PI_LOG"]).open("a") as handle:
    handle.write(
        json.dumps(
            {
                "cwd": os.getcwd(),
                "argv": sys.argv[1:],
                "caller_mark": os.environ.get("CALLER_MARK"),
            }
        )
        + "\\n"
    )
sys.stdout.write("local-pi ran\\n")
"""

# A hostile PATH pi: any run is a fault - the wrapper must never fall back.
PATH_PI = """#!@PYTHON@
import json
import os
import sys
from pathlib import Path

with Path(os.environ["PATH_PI_LOG"]).open("a") as handle:
    handle.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd()}) + "\\n")
sys.stderr.write("the global pi was started\\n")
raise SystemExit(7)
"""


@dataclass
class Pin:
    """A fake tools/pi tree around the real scripts, with its synthetic toolchain."""

    root: Path
    bin: Path
    fixtures: Path

    @property
    def manifest(self) -> Path:
        return self.root / "package.json"

    @property
    def lock(self) -> Path:
        return self.root / "package-lock.json"

    @property
    def node_version(self) -> Path:
        return self.root / ".node-version"

    @property
    def installed_json(self) -> Path:
        return self.root / "node_modules" / PKG / "package.json"

    def manifest_dict(self, pin: str = PIN) -> dict:
        return {
            "name": "coding-harness-pi",
            "private": True,
            "version": "1.0.0",
            "dependencies": {PKG: pin},
        }

    def lock_dict(self, pin: str = PIN, integrity: str = INTEGRITY) -> dict:
        return {
            "name": "coding-harness-pi",
            "version": "1.0.0",
            "lockfileVersion": 3,
            "packages": {
                "": {"name": "coding-harness-pi", "version": "1.0.0", "dependencies": {PKG: pin}},
                f"node_modules/{PKG}": {"version": pin, "integrity": integrity},
            },
        }

    def write_installed(self, pin: str = PIN, bin_entry: str | None = "dist/cli.py", broken: bool = False) -> None:
        """The installed package the wrapper checks: version, bin entry, the CLI file itself."""
        directory = self.installed_json.parent
        (directory / "dist").mkdir(parents=True, exist_ok=True)
        if broken:
            self.installed_json.write_text("{ not json", encoding="utf-8")
            return
        package: dict = {"name": PKG, "version": pin}
        if bin_entry is not None:
            package["bin"] = {"pi": bin_entry}
        self.installed_json.write_text(json.dumps(package), encoding="utf-8")
        write_exec(directory / "dist" / "cli.py", LOCAL_CLI.replace("@PYTHON@", sys.executable))

    def fixture_package(self, pin: str = PIN) -> None:
        """The package the synthetic npm installs: it carries a lifecycle-script sentinel."""
        name = PKG.replace("/", "-")
        source = self.fixtures / f"{name}-{pin}"
        (source / "dist").mkdir(parents=True, exist_ok=True)
        (source / "package.json").write_text(
            json.dumps(
                {
                    "name": PKG,
                    "version": pin,
                    "bin": {"pi": "dist/cli.py"},
                    "scripts": {"preinstall": "touch preinstall-ran"},
                }
            ),
            encoding="utf-8",
        )
        write_exec(source / "dist" / "cli.py", LOCAL_CLI.replace("@PYTHON@", sys.executable))

    def env(self, node: str = NODE_OK, path: list[Path] | None = None) -> dict:
        entries = path if path is not None else [self.bin, Path("/usr/bin"), Path("/bin")]
        return {
            "PATH": os.pathsep.join(str(entry) for entry in entries),
            "FAKE_NODE_VERSION": node,
            "FAKE_PI_LOG": str(self.root / "local-pi.jsonl"),
            "PATH_PI_LOG": str(self.root / "path-pi.jsonl"),
            "FAKE_NPM_LOG": str(self.root / "npm-calls.jsonl"),
            "FAKE_NPM_FIXTURES": str(self.fixtures),
        }

    def _run(self, script: str, *args: str, cwd: Path, env: dict, mutate=None) -> subprocess.CompletedProcess:
        if mutate is not None:
            write_exec(self.root / script, mutate((self.root / script).read_text(encoding="utf-8")))
        return subprocess.run(
            [str(self.root / script), *args],
            cwd=cwd,
            env={**os.environ, **env},
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def run_installer(self, node: str = NODE_OK, mutate=None):
        return self._run("install.sh", cwd=self.root, env=self.env(node=node), mutate=mutate)

    def run_wrapper(
        self,
        *args: str,
        cwd: Path | None = None,
        node: str = NODE_OK,
        path: list[Path] | None = None,
        env_extra: dict | None = None,
    ):
        env = self.env(node=node, path=path) | (env_extra or {})
        return self._run("pi", *args, cwd=cwd if cwd is not None else self.root, env=env)

    def local_runs(self) -> list[dict]:
        log = self.root / "local-pi.jsonl"
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []

    def path_runs(self) -> list[dict]:
        log = self.root / "path-pi.jsonl"
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []

    def npm_calls(self) -> list[dict]:
        log = self.root / "npm-calls.jsonl"
        return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []

    def installed_names(self) -> set[str]:
        base = self.root / "node_modules"
        if not base.is_dir():
            return set()
        found = set()
        for scope in base.iterdir():
            if not scope.is_dir():
                continue
            if not scope.name.startswith("@"):
                found.add(scope.name)
                continue
            for name in scope.iterdir():
                found.add(f"{scope.name}/{name.name}")
        return found


@pytest.fixture
def pin(tmp_path: Path) -> Pin:
    """The fake pin tree: the real scripts, the synthetic toolchain, the hostile PATH pi."""
    root = tmp_path / "tools" / "pi"
    root.mkdir(parents=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    for name, template in (("node", SYNTHETIC_NODE), ("npm", SYNTHETIC_NPM)):
        write_exec(bin_dir / name, template.replace("@PYTHON@", sys.executable))
    # The hostile PATH pi: the wrapper must never reach it.
    write_exec(bin_dir / "pi", PATH_PI.replace("@PYTHON@", sys.executable))
    write_exec(root / "install.sh", (REPO_ROOT / "tools" / "pi" / "install.sh").read_text(encoding="utf-8"))
    write_exec(root / "pi", (REPO_ROOT / "tools" / "pi" / "pi").read_text(encoding="utf-8"))
    built = Pin(root=root, bin=bin_dir, fixtures=fixtures)
    built.manifest.write_text(json.dumps(built.manifest_dict(), indent=2) + "\n", encoding="utf-8")
    built.lock.write_text(json.dumps(built.lock_dict(), indent=2) + "\n", encoding="utf-8")
    built.node_version.write_text("26.9.0\n", encoding="utf-8")
    built.write_installed()
    built.fixture_package()
    return built


# ---------------------------------------------------------------------------
# Criterion 1: the installer
# ---------------------------------------------------------------------------


def test_install_obeys_lock_integrity_and_disables_scripts(pin: Pin) -> None:
    """Criterion 1: exactly the lock's graph, scripts off; a changed graph, corrupt integrity, a floating pin refuse."""
    done = pin.run_installer()
    assert done.returncode == 0, done.stderr
    assert (pin.root / "node_modules" / PKG / "dist" / "cli.py").is_file(), "the pinned package is not installed"
    assert pin.installed_names() == {PKG}, f"a graph other than the lock's was installed: {pin.installed_names()}"
    assert not (pin.root / "preinstall-ran").exists(), "a lifecycle script ran under --ignore-scripts"
    assert pin.npm_calls() == [{"argv": ["ci", "--ignore-scripts"], "cwd": str(pin.root)}]

    # the fault that gives the sentinel meaning: the flag mutated away runs the script
    flag_off = pin.run_installer(mutate=lambda text: text.replace("npm ci --ignore-scripts", "npm ci"))
    assert flag_off.returncode == 0, flag_off.stderr
    assert (pin.root / "preinstall-ran").exists(), "the fault plant does not reach the lifecycle sentinel"

    # a lock whose graph disagrees with the manifest is refused, and nothing is installed for it
    (pin.root / "preinstall-ran").unlink()
    bad_graph = pin.lock_dict()
    bad_graph["packages"][""]["dependencies"] = {PKG: "9.9.9"}
    pin.lock.write_text(json.dumps(bad_graph, indent=2) + "\n", encoding="utf-8")
    refused = pin.run_installer()
    assert refused.returncode != 0 and "not in sync" in refused.stderr
    assert pin.installed_names() == {PKG}, "a refused install still changed node_modules"

    # a corrupt integrity value is refused
    corrupt = pin.lock_dict()
    corrupt["packages"][f"node_modules/{PKG}"]["integrity"] = "sha512-not!!base64"
    pin.lock.write_text(json.dumps(corrupt, indent=2) + "\n", encoding="utf-8")
    refused = pin.run_installer()
    assert refused.returncode != 0 and "integrity mismatch" in refused.stderr

    # a floating pin never reaches npm: the installer refuses it itself
    pin.lock.write_text(json.dumps(pin.lock_dict(), indent=2) + "\n", encoding="utf-8")
    pin.manifest.write_text(json.dumps(pin.manifest_dict(pin="^1.2.0"), indent=2) + "\n", encoding="utf-8")
    before = len(pin.npm_calls())
    refused = pin.run_installer()
    assert refused.returncode != 0 and "not an exact" in refused.stderr
    assert len(pin.npm_calls()) == before, "the installer started npm for a floating pin"


@pytest.mark.parametrize(
    ("missing", "needle"),
    [
        ("package.json", "package.json is missing"),
        ("package-lock.json", "package-lock.json is missing"),
        (".node-version", ".node-version is missing"),
    ],
    ids=["no-manifest", "no-lock", "no-node-version"],
)
def test_an_install_without_its_inputs_refuses(pin: Pin, missing: str, needle: str) -> None:
    """Criterion 1's edge: an installer without manifest, lock or Node declaration stops with guidance."""
    (pin.root / missing).unlink()
    done = pin.run_installer()
    assert done.returncode != 0 and needle in done.stderr
    assert pin.npm_calls() == [], "npm ran without its inputs"


@pytest.mark.parametrize(
    ("node", "declared", "needle"),
    [
        (NODE_WRONG, "26.9.0\n", "not the declared major"),
        (NODE_OK, "26\n", "holds no"),
        (NODE_OK, "twenty-six\n", "holds no"),
    ],
    ids=["wrong-major", "bare-declaration", "garbled-declaration"],
)
def test_an_install_on_the_wrong_node_refuses(pin: Pin, node: str, declared: str, needle: str) -> None:
    """The installer measures the declared major like the wrapper does (Q-5)."""
    assert pin.run_installer().returncode == 0, "the baseline install failed before the fault"
    pin.node_version.write_text(declared, encoding="utf-8")
    done = pin.run_installer(node=node)
    assert done.returncode != 0 and needle in done.stderr, done.stderr
    assert len(pin.npm_calls()) == 1, "npm ran on an unmeasured toolchain"


# ---------------------------------------------------------------------------
# Criterion 2: the wrapper from any working directory
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("where", [".", "elsewhere", "deep/nested/cwd"], ids=["pin-dir", "sibling", "nested"])
def test_wrapper_ignores_global_pi_from_any_cwd(pin: Pin, tmp_path: Path, where: str) -> None:
    """Criterion 2: only the repository-local Pi starts, from any cwd; the hostile PATH pi never runs."""
    cwd = (tmp_path / where).resolve()
    cwd.mkdir(parents=True, exist_ok=True)
    done = pin.run_wrapper("--print", "Review the change demo as the appended instructions say.", cwd=cwd)
    assert done.returncode == 0, done.stderr
    assert done.stdout == "local-pi ran\n"
    runs = pin.local_runs()
    assert len(runs) == 1, f"the local Pi started {len(runs)} times"
    assert runs[0]["cwd"] == str(cwd), "the wrapper changed the caller's working directory"
    assert runs[0]["argv"] == ["--print", "Review the change demo as the appended instructions say."]
    assert pin.path_runs() == [], "a PATH pi ran"
    assert pin.npm_calls() == [], "the wrapper installed something"


def test_the_wrapper_forwards_arguments_and_env_untouched(pin: Pin, tmp_path: Path) -> None:
    """The wrapper execs with the caller's arguments and environment; it adds nothing of its own."""
    cwd = tmp_path / "caller"
    cwd.mkdir()
    done = pin.run_wrapper("--version", cwd=cwd, env_extra={"CALLER_MARK": "kept"})
    assert done.returncode == 0, done.stderr
    (run,) = pin.local_runs()
    assert run["argv"] == ["--version"]
    assert run["cwd"] == str(cwd), "the wrapper changed the caller's working directory"
    assert run["caller_mark"] == "kept", "the wrapper dropped the caller's environment"


# ---------------------------------------------------------------------------
# Criterion 3: the wrapper against an unusable local install
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fault", "needle"),
    [
        ("no-manifest", "package.json is missing"),
        ("no-node-version", ".node-version is missing"),
        ("malformed-manifest", "declares no"),
        ("floating-pin", "not an exact"),
        ("absent-install", "is not installed"),
        ("wrong-version", "not the pinned"),
        ("broken-installed", "could not be read"),
        ("no-bin", "no pi bin entry"),
        ("missing-entry", "is missing from the install"),
    ],
)
def test_wrapper_refuses_unusable_local_pi(pin: Pin, fault: str, needle: str) -> None:
    """Criterion 3: every unusable install refuses with guidance - no launch, no install, no PATH fallback."""
    if fault == "no-manifest":
        pin.manifest.unlink()
    elif fault == "no-node-version":
        pin.node_version.unlink()
    elif fault == "malformed-manifest":
        pin.manifest.write_text("this is not a manifest\n", encoding="utf-8")
    elif fault == "floating-pin":
        pin.manifest.write_text(json.dumps(pin.manifest_dict(pin="~1.2.0"), indent=2) + "\n", encoding="utf-8")
    elif fault == "absent-install":
        shutil.rmtree(pin.root / "node_modules")
    elif fault == "wrong-version":
        pin.write_installed(pin="1.1.0")
    elif fault == "broken-installed":
        pin.write_installed(broken=True)
    elif fault == "no-bin":
        pin.write_installed(bin_entry=None)
    elif fault == "missing-entry":
        pin.installed_json.parent.joinpath("dist", "cli.py").unlink()

    done = pin.run_wrapper("--version")
    assert done.returncode != 0, f"the {fault} fault started Pi"
    assert needle in done.stderr, done.stderr
    assert GUIDANCE in done.stderr, f"the {fault} refusal carries no setup guidance"
    assert pin.local_runs() == [], "Pi started anyway"
    assert pin.path_runs() == [], "the wrapper fell back to the PATH pi"
    assert pin.npm_calls() == [], "the wrapper installed"


def test_a_wrapper_without_node_refuses_before_everything(pin: Pin, tmp_path: Path) -> None:
    """Criterion 4's first half: no Node on PATH, no Pi - the check runs before any metadata is read."""
    empty = tmp_path / "empty-bin"
    empty.mkdir(exist_ok=True)
    done = pin.run_wrapper("--version", path=[empty])
    assert done.returncode != 0
    assert "node is not on PATH" in done.stderr
    assert pin.local_runs() == [] and pin.path_runs() == []


# ---------------------------------------------------------------------------
# Criterion 4: the Node major
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("node", "declared", "starts"),
    [
        (NODE_OK, "26.9.0\n", True),
        ("26.0.0", "26.9.0\n", True),
        (NODE_WRONG, "26.9.0\n", False),
    ],
    ids=["same-major-patch", "other-minor", "wrong-major"],
)
def test_wrapper_checks_node_major(pin: Pin, node: str, declared: str, starts: bool) -> None:
    """Criterion 4: another major refuses before Pi starts; minor/patch moves of the major stay eligible."""
    pin.node_version.write_text(declared, encoding="utf-8")
    done = pin.run_wrapper("--version", node=node)
    if starts:
        assert done.returncode == 0, done.stderr
        assert len(pin.local_runs()) == 1, "the eligible Node did not start Pi"
    else:
        assert done.returncode != 0
        assert "major" in done.stderr, done.stderr
        assert pin.local_runs() == [], "Pi started on a refused toolchain"
    assert pin.path_runs() == [], "the PATH pi ran"
    assert pin.npm_calls() == [], "the wrapper installed"
