"""Design: 'Results that do not match stay stored, because a reverted edit may match again.' Do they?"""
import os, sys, subprocess, tempfile, time, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
work = Path(tempfile.mkdtemp(dir=sys.argv[2])); os.environ["XDG_STATE_HOME"] = str(work / "state")
import stage2_research_store as s, stage2_research_snapshot as snap
root = work / "repo"; root.mkdir()
g = lambda *a: subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True)
g("init", "-q"); (root / "plans/changes/ex").mkdir(parents=True)
R = "plans/changes/ex/research.md"; (root / R).write_bytes(b"---\nupdated: 2026-01-01\n---\nbody\n"); (root / "a.py").write_text("A = 1\n")
g("add", "-A"); g("-c", "user.email=x@i", "-c", "user.name=x", "commit", "-qm", "b")
def frozen():
    st = snap.freeze_research_state(root, "plans/changes/ex", deadline=time.monotonic() + 30)
    m = st.manifest(); b = st.sources()[R]; st.close(); return m, b
store = s.Store(s.research_dir("ex", root))
key = {"slot_id": "finders-0-1", "stage": "finders", "topic": None, "seat": 1, "endpoint": "go", "model": "m", "prompt_sha256": "p"}
# run A: paid finder result ok, then the run stops incomplete
m, b = frozen(); A = store.start_run("ex", "r1", snap.stored_binding(m, R, b))
store.write_result(A, "finders-0-1", {**key, "outcome": "ok", "stdout": "expensive answer"}); store.finish_run(A, "incomplete")
# the maintainer edits a.py, starts run B, aborts it at once (Ctrl-C before any slot)
(root / "a.py").write_text("A = 2\n"); m, b = frozen(); src = store.resume_source(m, R, b)
print("B sees:", src.usable, src.reasons)
B = store.start_run("ex", "r2", snap.stored_binding(m, R, b)); store.finish_run(B, "incomplete")
# ... reverts the edit and runs C on exactly A's inputs
(root / "a.py").write_text("A = 1\n"); m, b = frozen(); src = store.resume_source(m, R, b)
print("C sees source", "A" if src.run_id == A else "B", "usable:", src.usable, src.reasons, "results:", list(src.results))
print("A's result still on disk:", store.slot_records(A)[0].keys())
print("plan_reuse:", s.plan_reuse(src, [key], lambda r: True))
