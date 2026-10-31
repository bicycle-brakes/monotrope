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
.PHONY: verify test staleness gates leakcheck venv lock change index report close-merged help

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

# The interpreter must meet `requires-python` in pyproject.toml (the one place
# the minimum is declared). Default: the first of python3.12, python3 on PATH;
# `make venv PYTHON=/opt/homebrew/bin/python3.12` names one. A wrong version
# is refused before `.venv` exists, so no half-built environment is left
# behind (bead coding-harness-y9q).
PYTHON ?= $(shell command -v python3.12 || command -v python3)

venv:
	@need=$$(sed -n 's/^requires-python *= *">=\([0-9.]*\)".*/\1/p' pyproject.toml); \
	have=$$('$(PYTHON)' -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null); \
	if [ -z "$$need" ]; then echo "make venv: no requires-python in pyproject.toml" >&2; exit 1; fi; \
	if [ -z "$$have" ] || [ "$$(printf '%s\n%s\n' "$$need" "$$have" | sort -t. -k1,1n -k2,2n | head -n 1)" != "$$need" ]; then \
		echo "make venv: '$(PYTHON)' is Python $${have:-unknown}, but the lock needs $$need or newer." >&2; \
		echo "Provide one, e.g.: make venv PYTHON=/opt/homebrew/bin/python3.12" >&2; \
		exit 1; \
	fi
	'$(PYTHON)' -m venv .venv
	.venv/bin/python3 -m pip install --require-hashes -r requirements-ci.txt

lock:
	uv pip compile pyproject.toml --group dev --universal --generate-hashes --exclude-newer "$$(date -u +%Y-%m-%dT00:00:00Z)" -o requirements-ci.txt

# The entry the workflow promises (docs/WORKFLOW.md, bead coding-harness-i0l).
# NAME and BEAD are checked on the make level — given on the command line, never
# taken from a stray exported variable — and the recipe passes them to
# the entry script through its exported environment — their values are never
# interpolated into the shell line, so arguments stay data, never code.
change:
	$(if $(and $(NAME),$(filter command line,$(origin NAME))),,$(error usage: make change NAME=<name> BEAD=<existing-bead-id> — both on the command line))
	$(if $(and $(BEAD),$(filter command line,$(origin BEAD))),,$(error usage: make change NAME=<name> BEAD=<existing-bead-id> — both on the command line))
	@export NAME BEAD; python3 scripts/new_change.py "$$NAME" --bead "$$BEAD"

index:
	@python3 scripts/plans_registry.py --index

# The run report (bead coding-harness-o2yc): one local, read-only snapshot of the
# active changes - recorded attempts, time against the plan-card appetite, live
# process and memory figures. The optional CHANGE selection passes as data in the
# environment; its value is never interpolated into the shell line. It is not a
# gate and runs nowhere in verify (docs/WORKFLOW.md, "The run report").
report:
	@export CHANGE; python3 scripts/run_report.py

# Closes beads whose work merged (bead coding-harness-l1if): the reconciler
# reads Closes-Bead trailers from a freshly fetched origin/main and closes what
# they declare through the pinned tools/bd — reporting only, unless ARGS=--write.
# Only command-line ARGS is accepted. Capture its raw value without expanding
# make functions, then validate the exact bytes in the shell as environment data.
# Anchor this target to this Makefile, even when invoked with -f elsewhere.
# Export the full path as data so checkout paths containing spaces stay intact.
override CLOSE_MERGED_MAKEFILE := $(strip $(MAKEFILE_LIST))
export CLOSE_MERGED_MAKEFILE
ifeq ($(origin ARGS),command line)
override CLOSE_MERGED_ARGS := $(value ARGS)
else
override CLOSE_MERGED_ARGS :=
endif
export CLOSE_MERGED_ARGS
unexport ARGS

close-merged:
	@cd "$$(dirname "$$CLOSE_MERGED_MAKEFILE")" && \
	case "$$CLOSE_MERGED_ARGS" in \
	  "") python3 scripts/close_merged_beads.py ;; \
	  --write) python3 scripts/close_merged_beads.py --write ;; \
	  *) echo 'close-merged: ARGS must be empty or --write' >&2; exit 2 ;; \
	esac

help:
	@echo 'make verify                             every locally runnable gate (the CI runs the same)'
	@echo 'make test                               the test suite, by hand'
	@echo 'make staleness                          hygiene of the plans/ artefacts'
	@echo 'make gates                              what the CI runs, read from decisions/gates.yaml'
	@echo 'make leakcheck NAME=<name>              the leak check before a foreign call'
	@echo 'make venv [PYTHON=<interpreter>]        build .venv from the hash-checked lock'
	@echo 'make lock                               rewrite requirements-ci.txt from pyproject.toml'
	@echo 'make change NAME=<name> BEAD=<existing-bead-id>'
	@echo '                                        create plans/changes/<name>/ linked to an existing bead'
	@echo 'make index                              regenerate plans/INDEX.md from the registry'
	@echo 'make report [CHANGE=<name>]             one read-only snapshot of the active changes (not a gate)'
	@echo 'make close-merged [ARGS=--write]        close beads a merged Closes-Bead trailer declared (report without ARGS)'
	@echo '                                        reporting also fails on unresolved declarations (nonzero exit)'
	@echo 'make help                               this list'
