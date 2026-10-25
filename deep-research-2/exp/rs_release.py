"""Does release-loop delete the research state store (and its lock) of the same change?"""
import os, sys, subprocess, tempfile, time
from pathlib import Path
TREE = Path(sys.argv[1]); sys.path.insert(0, str(TREE / "scripts"))
work = Path(tempfile.mkdtemp(prefix="rs-release-", dir=sys.argv[2]))
os.environ["XDG_STATE_HOME"] = str(work / "state")
root = work / "repo"; (root / "plans/changes/example").mkdir(parents=True)
(root / "plans/changes/example/findings.md").write_text("# Findings\n\nPhase 6 verdict: codex abc, 2026-10-25\n")
import stage2, stage2_research_store as s
store = s.Store(s.research_dir("example", root))
run = store.start_run("plans/changes/example", "r", {"paths": {}, "research": "x", "research_normalised_sha256": "0"})
store.write_result(run, "s1", {"slot_id": "s1", "outcome": "ok", "report": "paid result"})
store.write_launch(run, "s2", {"slot_id": "s2"})
print("before:", sorted(p.name for p in store.directory.iterdir()), store.slot_records(run))
# a research run of the same change holds the store lock (another process)
holder = subprocess.Popen([sys.executable, "-c", f"""
import sys,time; sys.path.insert(0,{str(TREE/'scripts')!r})
import stage2_research_store as s
st=s.Store({str(store.directory)!r}); st.acquire_lock(); print('held',flush=True); time.sleep(30)"""], stdout=subprocess.PIPE, text=True)
assert holder.stdout.readline().strip() == "held"
stage2.write_state("example", {"consumed": [], "free": {}, "paid": {}}, root)  # a review-loop record exists
lp = stage2.record_dir("example", root) / "loop.md"; lp.write_text(lp.read_text() + "\n## Round 1 — free swarm\n\nNo finding.\n")
print("record dir mode:", oct(os.stat(stage2.record_dir("example", root)).st_mode & 0o777))
rows = stage2.release(root, "example")
print("release returned rows:", rows)
print("research dir exists after release:", store.directory.exists())
second = s.Store(store.directory)
try:
    second.acquire_lock(); print("second run acquired the lock while the first still holds its descriptor: True")
except s.StoreLocked:
    print("second run refused (lock held)")
print("runs visible to resume:", second.runs())
holder.kill()
