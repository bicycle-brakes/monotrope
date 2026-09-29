# Omnigent default policy (layer 2)

A second, per-machine layer behind the deny rules in `.claude/settings.json`
(layer 1). Both refuse the Omnigent tools that write, run, spawn or change
state (`sys_os_write`, `sys_os_shell`, terminals, sessions, scheduled tasks and
so on), and Claude Code's file tools writing Omnigent's own config file.

**What it is not.** Nothing in this repository depends on it: layer 1 holds
alone (ADR 0006). It is per machine, not per repository, so once installed it
refuses those tools in every Omnigent session on the machine. It reaches only
calls that pass Omnigent's policy check: Omnigent's bridge runs its own
`sys_os_*` tools without any policy while its relay does not advertise them,
and harnesses Omnigent does not hook (Goose, Qwen, Kiro, Cursor, Antigravity)
are not covered at all.

`policy.yaml` is generated. The one list it comes from is
`scripts/omnigent_policy.py`; to change it, edit the list, run
`python3 scripts/omnigent_policy.py --write`, and reinstall.

## Use (the maintainer, in a terminal)

```bash
tools/omnigent/install.sh            # merge into ~/.omnigent/config.yaml
tools/omnigent/install.sh --check    # do the installed policies equal this file?
tools/omnigent/install.sh --remove   # take them out again
```

- The old config is kept as `config.yaml.bak-<timestamp>`; comments in it are
  not carried over by the merge, the backup keeps them.
- Omnigent reads `policies:` only when its server starts. After a change, stop
  a running background server with `omnigent server stop` (its sessions end);
  the next `omnigent claude` starts it with the policy. The installer says so,
  and never starts or stops anything itself.
- `$OMNIGENT_CONFIG_HOME` moves the config, `$OMNIGENT_PYTHON` names Omnigent's
  interpreter.
