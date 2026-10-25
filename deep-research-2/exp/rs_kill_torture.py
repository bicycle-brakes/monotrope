import os, random, signal, subprocess, sys, tempfile, time
from pathlib import Path
tree, scratch = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree + "/scripts"); import stage2_research_store as s
bad = 0; temps = 0
for i in range(40):
    d = Path(tempfile.mkdtemp(dir=scratch)) / "research"
    child = f"""
import sys; sys.path.insert(0, {tree + '/scripts'!r}); import stage2_research_store as s
st = s.Store({str(d)!r}); run = st.start_run('c', 'r', {{}}); print(run, flush=True)
n = 0
while True:
    n += 1; st.write_result(run, 's1', {{'slot_id': 's1', 'outcome': 'ok', 'n': n, 'stdout': 'x' * (n % 7 * 300000)}})
"""
    p = subprocess.Popen([sys.executable, "-c", child], stdout=subprocess.PIPE, text=True)
    run = p.stdout.readline().strip(); time.sleep(random.uniform(0.05, 0.6)); p.send_signal(signal.SIGKILL); p.wait()
    st = s.Store(d); results, interrupted = st.slot_records(run)
    r = results.get("s1")
    if r is None or len(r["stdout"]) != r["n"] % 7 * 300000: bad += 1
    temps += sum(1 for x in (d / run).iterdir() if x.name.startswith(".tmp-"))
print("iterations 40, bad/torn results accepted:", bad, "leftover temp files:", temps)
