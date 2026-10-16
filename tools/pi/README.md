# The runner's pinned Pi

The runner starts Pi from this directory only (bead coding-harness-agx,
ADR 0019): one repository-local npm install whose exact version
`package.json` pins, whose dependency graph and integrity values
`package-lock.json` records, and whose relied-on behaviour the offline
contract suite (`tests/test_pi_contract.py`) measures. A global `pi` on PATH
is never started, and a global update cannot change what the runner calls.

## Files

- `package.json` — the exact Pi dependency, the one source of the pin. The
  runner (`scripts/stage2.py`) and the wrapper read the pin from here; there
  is no second version literal.
- `package-lock.json` — the npm-generated lock: the exact dependency graph
  with registry integrity values. Never edited by hand; a move regenerates it
  with npm (below).
- `.node-version` — the exact CI Node runtime; its **major** is what the
  wrapper and the installer require locally. Minor and patch moves within
  that major stay eligible for the same contract suite.
- `install.sh` — installs exactly the manifest dependency in the exact lock
  graph with `npm ci --ignore-scripts`, after checking Node and npm. A failed
  install exits non-zero; it never falls back.
- `pi` — the wrapper. From any working directory it checks the Node major,
  the manifest pin and the installed version, then starts the installed Pi
  with the given arguments. It never installs, never uses `npx`, never falls
  back to a global Pi, and changes neither the caller's working directory,
  environment nor arguments.

## Fresh clone

```sh
bash tools/pi/install.sh
```

Prerequisites: Node of the major declared in `.node-version` (npm ships with
it) and access to the npm package registry — once, for the install. Running
Pi and the contract suite afterwards need no network and no registry.

The install step of the runner documents the same command; CI runs it in both
toolchain jobs before pytest (`scripts/ci_gates.py`), so a fresh checkout that
skipped it fails its first contract run instead of silently using a global Pi.

## Verify an install

```sh
tools/pi/pi --version   # must print the version package.json pins
```

Any refusal names the defect and ends non-zero: missing Node of the wrong
major, a missing or floating pin, an absent, mismatched or broken install.

## What the tests install versus what they run

`tests/test_pi_install.py` builds a fake `tools/pi` tree around the real
scripts with synthetic `node`/`npm` executables: it exercises the installer's
and wrapper's refusals (lock mismatch, corrupt integrity, lifecycle-script
denial, hostile PATH Pi, wrong Node major). Lock mismatch, integrity and
lifecycle controls also run real npm offline over a local tarball and empty
cache; no registry is contacted.
`tests/test_pi_contract.py` runs the **real** installed Pi against a loopback
stand-in: tool declarations, suppressed extension/MCP startup and
skill/prompt/theme discovery reads, context-file exclusion, scratch-agent
separation from ambient saved auth and command-valued model configuration,
the session policy, provider addresses and key mapping. Missing Pi or Node fails those contracts;
they never skip.

## Moving the pin

1. Change the dependency in `package.json` (and, when the measured major
   changes, `.node-version`).
2. Regenerate the lock with npm in this directory (`npm install
   --package-lock-only --ignore-scripts`), then `bash tools/pi/install.sh`.
3. Run the real contracts and the full verification:
   `.venv/bin/python3 -m pytest tests/test_pi_contract.py -q` and `make
   verify`. A failed contract is investigated or reported — never weakened to
   bless the candidate.
4. Propose the change as a pull request; the merge adopts the new pin.
