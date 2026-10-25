import sys, subprocess, tempfile, time
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import stage2_research_history as h
root = Path(tempfile.mkdtemp(dir=sys.argv[2])) / "repo"; root.mkdir()
def git(*a, **k): return subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True, **k)
git("init", "-q"); (root / "a.py").write_text("x=1\n"); git("add", "a.py")
# a legacy commit whose message is Latin-1 without an encoding header (git stores bytes as given)
git("-c", "user.email=x@i", "-c", "user.name=x", "-c", "i18n.commitEncoding=UTF-8", "commit", "-q", "-F", "-", input=b"Fix f\xfcr M\xfcller\n")
(root / "b.py").write_text("y\n"); git("add", "b.py"); git("-c", "user.email=x@i", "-c", "user.name=x", "commit", "-qm", "unrelated")
head = git("rev-parse", "HEAD").stdout.decode().strip()
for paths in (["a.py"], ["b.py"]):
    try:
        r = h.build_research_history(root, head, paths, deadline=time.monotonic() + 30)
        print(paths, "-> ok", [c["subject"] for c in r["commits"].values()])
    except h.ResearchHistoryError as e:
        print(paths, "-> ResearchHistoryError:", e, "| cause:", repr(e.__cause__))
