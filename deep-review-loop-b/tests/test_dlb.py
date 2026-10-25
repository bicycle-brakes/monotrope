import sys, json, re
from pathlib import Path
import yaml, pytest
sys.path.insert(0, str(Path(__file__).parent))

from test_stage2 import world, loop_state, rows, rung_of, decide_record, TEST_LADDER  # noqa
import stage2


def _flash(world):
    world.write_record([("L1-1", "taken — test_a", "no")], state=loop_state(("free",)))


def test_b1_replacement_refused_discards_answers(world, capsys):
    _flash(world)
    p = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(p.read_text())
    e = next(x for x in data["endpunkte"] if x["name"] == "opencode-go")
    e["modelle_terms"]["mimo-v2.6-pro"]["uebersprungen"] = "2026-10-20"
    e["modelle_terms"]["mimo-v2.6-pro"]["grund"] = "terms changed"
    p.write_text(yaml.safe_dump(data))
    world.script(pi=[
        {"model": "deepseek-v4.1-flash", "exit": 1, "stderr": "Model is unavailable"},
        {"model": "mimo-v2.6-flash", "stdout": rows(2, "M")},
    ])
    code = world.run("review-loop")
    err = capsys.readouterr().err
    print("EXIT", code); print(err[-600:])
    text = world.record().read_text()
    print("ROUND2 IN RECORD:", "## Round 2" in text)
    print("CALLS", [rung_of(c) for c in world.reviews("pi")])
    code2 = world.run("review-loop")
    print("EXIT2", code2, "CALLS", [rung_of(c) for c in world.reviews("pi")])


def test_b2_excluded_free_id_blocks_free_stage(world, capsys):
    p = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(p.read_text())
    data["ausgeschlossen"] = [{"was": "beacon dropped", "klasse": "framework", "modelle": ["beacon"]}]
    p.write_text(yaml.safe_dump(data))
    world.script(pi=[{"stdout": rows(1, "A")}, {"stdout": rows(1, "B")}])
    for _ in range(2):
        code = world.run("review-loop")
        err = capsys.readouterr().err
        print("EXIT", code, err.strip().splitlines()[-1])
    print("record exists:", world.record().exists(), "reviews:", len(world.reviews("pi")))


def test_b2b_excluded_paid_in_ladder(world, capsys):
    p = world.root / "model-endpoints.yaml"
    data = yaml.safe_load(p.read_text())
    data["ausgeschlossen"] = [{"was": "mimo dropped", "klasse": "framework", "modelle": ["mimo-v2.6-flash"]}]
    p.write_text(yaml.safe_dump(data))
    print("ladder:", stage2.ladder(world.root), "skipped:", stage2.skipped_models(world.root))
    st = stage2.new_state(world.root, {"selected": []})
    print("flash:", st["paid"]["flash"])


def test_b3_unattributed_prose(world, capsys):
    world.script(pi=[
        {"model": "acme-v1-free", "stdout": rows(1, "A") + "\nI am sure: the whole module is broken (alpha)."},
        {"model": "beacon-2-free", "stdout": rows(1, "B") + "\n| a | b |\nsee note (beta)"},
    ])
    assert world.run("review-loop") == 0
    print(world.record().read_text().split("## Round 1", 1)[1])


def test_b4_glm_key_in_answer(world, capsys):
    from test_stage2 import KEY, OKEY
    world.script(pi=[
        {"model": "acme-v1-free", "stdout": f"| X1 | MAJOR | MAINT | impl | x | the secrets file holds {KEY} and @KEY@ |"},
        {"model": "beacon-2-free", "exit": 1, "stderr": f"auth failed for {KEY}\n"},
    ])
    assert world.run("review-loop") == 0
    rec = world.record().read_text()
    err = capsys.readouterr().err
    print("GLM key in record:", KEY in rec, "| OpenCode key in record:", OKEY in rec, "| GLM key on stderr:", KEY in err)
    print([l for l in rec.splitlines() if "L1-1" in l or "failed" in l])


def test_b7_pipe_in_catalog_id(world, capsys):
    catalog = (
        "provider model context input output\n"
        "opencode-go deepseek-v4.1-flash 128000 0.15 0.60\n"
        "opencode-go mimo-v2.6-flash 128000 0.14 0.28\n"
        "opencode-go mimo-v2.6-pro 128000 0.435 0.87\n"
        "opencode-go acme|rejected-free 128000 0 0\n"
    )
    world.script(pi_catalog=catalog, pi=[{"stdout": rows(2, "A")}])
    assert world.run("review-loop") == 0
    rec = world.record().read_text()
    with capsys.disabled():
        print([l for l in rec.splitlines() if l.startswith("| L1") or l.startswith("## Round")])
        print("rows:", stage2.record_rows(rec))
    code = world.run("review-loop")
    print("SECOND EXIT", code, capsys.readouterr().err.strip().splitlines()[-1])


def test_b10_unstarted_replacement_consumed(world, capsys, monkeypatch):
    import time as _t
    _flash(world)
    monkeypatch.setattr(stage2, "REVIEWER_MINUTES", 3 / 60)
    orig = stage2.checked_prompt
    def slow(ctx, endpoint, prompt, adm=None):
        if endpoint[1] == "mimo-v2.6-pro":
            _t.sleep(2.5)
        return orig(ctx, endpoint, prompt, adm)
    monkeypatch.setattr(stage2, "checked_prompt", slow)
    world.script(pi=[
        {"model": "deepseek-v4.1-flash", "exit": 1, "stderr": "Rate limited"},
        {"model": "mimo-v2.6-flash", "stdout": rows(1, "M"), "sleep": 1},
    ])
    assert world.run("review-loop") == 0
    rec = world.record().read_text()
    with capsys.disabled():
        print("called:", [rung_of(c) for c in world.reviews("pi")])
        print([l for l in rec.splitlines() if "failed" in l])
        print("consumed:", stage2.read_state(rec, "")["consumed"])
    decide_record(world)
    capsys.readouterr()
    code = world.run("review-loop")
    with capsys.disabled():
        print("next:", code, capsys.readouterr().err.strip().splitlines()[-1])
