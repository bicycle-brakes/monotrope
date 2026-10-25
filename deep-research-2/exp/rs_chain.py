import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
os.environ["XDG_STATE_HOME"] = tempfile.mkdtemp(dir=sys.argv[2])
import stage2_research_store as s
store = s.Store(s.research_dir("ex", Path(sys.argv[2])))
b = {"paths": {}, "research": "r", "research_normalised_sha256": "0"}
A = store.start_run("ex", "r", b)
store.write_result(A, "s1", {"slot_id": "s1", "outcome": "ok", "started_at": "T_A0", "ended_at": "T_A1", "leak_check": {"clean": True}})
B = store.start_run("ex", "r", b); store.adopt(B, s.Source(True, run_id=A), store.slot_records(A)[0]["s1"])
C = store.start_run("ex", "r", b); store.adopt(C, s.Source(True, run_id=B), store.slot_records(B)[0]["s1"])
print("A =", A); print("B =", B); print("C record:", store.slot_records(C)[0]["s1"])
