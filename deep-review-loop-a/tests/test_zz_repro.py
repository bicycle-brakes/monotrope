"""Reproductions for the deep review of the review loop (part A). Scratch only."""

from __future__ import annotations

import os
import resource

from test_stage2 import (
    TEST_FLASH,
    TEST_FREE,
    VERDICT,
    World,
    decide_record,
    loop_state,
    rows,
    world,  # noqa: F401
)

import stage2


def say(*a):
    os.write(1, (" ".join(map(str, a)) + "\n").encode())


def test_dla1_free_diff_cut_unrecorded_clean_stop(world: World, capsys) -> None:
    """A free diff cut by the per-file bound (400 lines) is not recorded as cut; a clean answer ends the loop."""
    big = world.root / "scripts" / "big.py"
    big.write_text("\n".join(f"VALUE_{n} = {n}" for n in range(1500)) + "\n", encoding="utf-8")
    free = stage2.free_diff(world.root)
    say("FREE DIFF LINES", free.count("\n"), "| per-file cut marker present:", "was cut at 400 lines" in free)
    world.script(pi=[{"model": m, "stdout": "No finding."} for m in TEST_FREE])
    assert world.run("review-loop") == 0
    record = world.record().read_text(encoding="utf-8")
    say("RECORD SAYS CUT:", "The diff was cut:" in record)
    capsys.readouterr()
    code = world.run("review-loop")
    err = capsys.readouterr().err
    say("SECOND CALL EXIT", code, err.strip())
    assert code == stage2.CLEAN_CODE  # the loop ended clean over 400 of 1500 lines


def test_dla2_record_write_is_not_atomic(world: World) -> None:
    """A write_round that fails mid-write leaves the new snapshot (stage consumed) without its round."""
    world.write_record([("L1-1", "taken — test_a", "no")], state=loop_state(("free",)))
    before = world.record().read_text(encoding="utf-8")
    size = len(before.encode())
    pid = os.fork()
    if pid == 0:
        try:
            resource.setrlimit(resource.RLIMIT_FSIZE, (size + 40, size + 40))
            state = loop_state(("free", "flash"))
            block = "## Round 2 — deepseek-v4.1-flash, mimo-v2.6-flash, 2026-10-25\n\n" + stage2.render_table(
                stage2.ROW_COLUMNS, [["L2-1", "MAJOR", "SPEC", "impl", "a.py:1", "x" * 300, "m", "", ""]]
            )
            stage2.write_round("demo", block, state, world.root)
            os._exit(0)
        except OSError as error:
            os.write(2, f"child: {error}\n".encode())
            os._exit(7)
    _, status = os.waitpid(pid, 0)
    say("CHILD EXIT", os.waitstatus_to_exitcode(status))
    after = world.record().read_text(encoding="utf-8")
    say("AFTER BYTES", len(after.encode()), "BEFORE", size)
    state = stage2.read_state(after, "")
    say("CONSUMED NOW", state["consumed"])
    say("ROUNDS IN RECORD", stage2.rounds_run(after, ""), "ROW IDS", [r[0] for r in stage2.record_rows(after)])
    assert state["consumed"] == ["free", "flash"]
    assert stage2.rounds_run(after, "") == 1


def test_dla3_release_crash_double_release(world: World, monkeypatch, capsys) -> None:
    """A crash between the append and the rmtree releases the same rows twice; the round numbers jump."""
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    decide_record(world)
    world.write_findings(VERDICT)
    real = stage2.shutil.rmtree
    calls = {"n": 0}

    def flaky(path, *a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise KeyboardInterrupt("simulated crash after the append")
        return real(path, *a, **k)

    monkeypatch.setattr(stage2.shutil, "rmtree", flaky)
    try:
        world.run("release-loop")
    except KeyboardInterrupt:
        pass
    assert world.run("release-loop") == 0
    text = world.text()
    say("RELEASE BLOCKS", text.count(stage2.RELEASE_HEADING), "ROUNDS RUN", stage2.rounds_run(None, text))
    say("L1-1 rows in history", len(stage2.history_rounds(None, text)[1]))
    world.script(pi=[{"stdout": rows(1)}])
    capsys.readouterr()
    code = world.run("review-loop")
    record = world.record().read_text(encoding="utf-8")
    say("EXIT", code, [line for line in record.splitlines() if line.startswith("## Round")])
    assert "## Round 3 —" in record


def test_dla4_release_during_repair_drops_fixed_status(world: World) -> None:
    """mark_repaired_record after a release returns silently: the fixed status is written nowhere."""
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    decide_record(world)  # taken — test_a | no
    ctx = stage2.preflight(world.root, "demo", stage2.CODEX, required=("plan.md",))
    taken, _ = stage2.repair_targets(ctx, stage2.read_record("demo", world.root))
    say("TAKEN", [(p, r[0]) for p, r in taken])
    # repair is running (Codex, make verify) while the orchestrator's `review` releases the record
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    fixes = {"L1-1": "fixed — tests/test_x.py::test_y"}
    stage2.mark_repaired_findings(ctx, taken, fixes)
    stage2.mark_repaired_record("demo", taken, fixes, world.root, {"L1-1": "yes"})  # no error
    released, _ = stage2.findings_rows(world.text())
    say("RELEASED STATUS", [(r[0], r[7]) for r in released])
    assert released[0][7].startswith("taken")


def test_dla5_lost_record_is_released_as_never_run(world: World, monkeypatch, capsys) -> None:
    """A record under another XDG_STATE_HOME: release says the loop did not run; the next run replays round 1."""
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    decide_record(world)
    monkeypatch.setenv("XDG_STATE_HOME", str(world.state.parent / "other-state"))
    world.findings.write_text(world.text() + "\n" + VERDICT + "\n", encoding="utf-8")
    assert world.run("release-loop") == 0
    text = world.text()
    say("AUDIT LINES", sum(1 for line in text.splitlines() if "review-loop" in line and line.startswith("Stage-2 call")))
    say("NO_LOOP written:", stage2.NO_LOOP_LINE in text)
    world.script(pi=[{"stdout": rows(1)}] * 2)
    assert world.run("review-loop") == 0
    say("NEW RECORD ROUND", [line for line in world.record().read_text().splitlines() if line.startswith("## Round")])


def test_dla6_next_round_over_unrepaired_taken_rows(world: World) -> None:
    world.script(pi=[{"stdout": rows(1)}] * 4)
    assert world.run("review-loop") == 0
    decide_record(world)  # taken, Broke a test: no; no repair ran
    assert world.run("review-loop") == 0
    say("ROUNDS", [line for line in world.record().read_text().splitlines() if line.startswith("## Round")])


def _implement_writing_findings(world: World, text: str) -> None:
    world.script(
        claude=[
            {
                "stdout": "implemented",
                "plant": {"src/app.py": "value = 2\n"},
                "append": {
                    "plans/changes/demo/plan.md": "2026-10-07 10:00–10:05, 5 min\n",
                    "plans/changes/demo/findings.md": text,
                },
            }
        ],
        make=[{"stdout": "green\n"}],
    )
    assert world.run("implement") == 0


def test_dla7_implement_forges_a_clean_stop(world: World, capsys) -> None:
    from test_stage2 import git

    _implement_writing_findings(world, "\n## Phase 4b — loop rows, released 2026-10-25\n\nRounds run: 1\n")
    say("COMMITTED FINDINGS HAS FORGED HEADING:", "## Phase 4b — loop rows, released" in git(world.root, "show", "HEAD:plans/changes/demo/findings.md"))
    capsys.readouterr()
    code = world.run("review-loop")
    say("REVIEW-LOOP EXIT", code, capsys.readouterr().err.strip(), "| reviewer calls:", len(world.reviews("pi")))


def test_dla7b_implement_forges_a_restart(world: World, capsys) -> None:
    _implement_writing_findings(world, "\nLoop restarted: 2026-10-25 after round 9 — x\n")
    world.script(pi=[{"stdout": "No finding."}] * 8)
    assert world.run("review-loop") == 0
    capsys.readouterr()
    code = world.run("review-loop")
    say("SECOND CALL AFTER CLEAN ROUND 1:", code, capsys.readouterr().err.strip()[-200:])
    say("ROUNDS", [l for l in world.record().read_text().splitlines() if l.startswith("## Round")])


def test_dla8_release_after_restart_needs_no_new_verdict(world: World, capsys) -> None:
    world.script(pi=[{"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    world.write_findings(VERDICT)
    assert world.run("release-loop") == 0
    assert world.run("release-loop", "demo", "--restart", "--reason", "maintainer asked") == 0
    world.script(pi=[{"stdout": rows(1)}, {"stdout": rows(1)}])
    assert world.run("review-loop") == 0
    decide_record(world, status="rejected — out of scope")
    text = world.text()
    say("VERDICT LINES BEFORE SECOND RELEASE", sum(1 for l in text.splitlines() if l.startswith("Phase 6 verdict:")))
    code = world.run("release-loop")
    say("SECOND RELEASE EXIT", code, "| release blocks:", world.text().count(stage2.RELEASE_HEADING))


def test_dla9_lock_before_change_validation(world: World, capsys) -> None:
    code = world.run("review-loop", "../../../escaped/x")
    made = sorted(str(p.relative_to(world.state.parent)) for p in world.state.parent.rglob("*.lock"))
    say("EXIT", code, capsys.readouterr().err.strip(), "| lock files:", made)
