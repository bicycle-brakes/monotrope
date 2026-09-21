# The verify commands live in ONE place: decisions/gates.yaml.
# make verify delegates to the runner, the runner asks ci_gates.py, and that
# reads the gate file. Nothing here restates a gate command — the two recipe
# lines below exist because tests/test_ci.py pins Makefile and gate list
# against each other (W-6).
#
# `make test` / `make staleness` are the two gates a developer runs by hand
# most often; their recipes are copied verbatim from decisions/gates.yaml and
# held there by test_the_makefile_runs_what_the_one_list_runs.

.PHONY: verify test staleness gates leakcheck

verify:
	bash scripts/verify_all.sh

test:
	python3 -m pytest tests/ -q

staleness:
	python3 scripts/plans_registry.py --check

gates:
	python3 scripts/ci_gates.py --list

leakcheck:
	@echo "leakcheck needs the denylist outside this repository and runs before a session on a foreign endpoint, not in CI — see AGENTS.md."
	@exit 1
