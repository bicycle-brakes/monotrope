"""SIGKILL while the runner appends a research record: is research.md ever torn?"""
import os, signal, subprocess, sys, tempfile, time
from pathlib import Path
tree, scratch = sys.argv[1], sys.argv[2]
work = Path(tempfile.mkdtemp(dir=scratch)); path = work / "research.md"
body = "---\nupdated: 2026-01-01\n---\n" + ("earlier research line, not committed yet\n" * 2_500_000)  # ~100 MB
child = f"""
import sys; sys.path.insert(0, {tree + '/scripts'!r}); import stage2
from pathlib import Path
print('go', flush=True); stage2.append(Path({str(path)!r}), '<!-- research-swarm/v2 run x -->\\nrecord')
"""
for delay in (0.15, 0.3, 0.45, 0.6):
    path.write_text(body)
    p = subprocess.Popen([sys.executable, "-c", child], stdout=subprocess.PIPE, text=True)
    p.stdout.readline(); time.sleep(delay); p.send_signal(signal.SIGKILL); p.wait()
    size = path.stat().st_size
    print(f"kill after {delay:.2f}s: size {size} of {len(body)} -> {'TORN (earlier research lost)' if size < len(body) else 'intact'}")
