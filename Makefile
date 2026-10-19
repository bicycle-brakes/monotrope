# The verify commands live in ONE place: decisions/gates.yaml.
# make verify delegates to the runner, the runner asks ci_gates.py, and that
# reads the gate file. Nothing here restates a gate command — the two recipe
# lines below exist because tests/test_ci.py pins Makefile and gate list
# against each other (W-6).
#
# `make test` / `make staleness` are the two gates a developer runs by hand
# most often; their recipes are copied verbatim from decisions/gates.yaml and
# held there by test_the_makefile_runs_what_the_one_list_runs.

# `make venv` builds this checkout's own `.venv` from the lock; `make lock`
# writes the lock from `pyproject.toml` (bead coding-harness-ei0). The lock's
# first lines record the exact command that wrote it, and rerunning that
# command must give the committed file byte for byte. Only the machine that
# changes a pin needs uv; CI and `make venv` install with pip.
.PHONY: verify test staleness gates leakcheck venv lock

verify:
	bash scripts/verify_all.sh

test:
	python3 -m pytest tests/ -q -n auto

staleness:
	python3 scripts/plans_registry.py --check

gates:
	python3 scripts/ci_gates.py --list

# Runs before a foreign call (scripts/stage2.py runs it itself) and never in CI:
# it needs the denylist each machine keeps outside the repository.
leakcheck:
	python3 scripts/leakcheck.py --name "$(NAME)"

venv:
	python3 -m venv .venv
	.venv/bin/python3 -m pip install --require-hashes -r requirements-ci.txt

lock:
	uv pip compile pyproject.toml --group dev --universal --generate-hashes --exclude-newer "$$(date -u +%Y-%m-%dT00:00:00Z)" -o requirements-ci.txt
