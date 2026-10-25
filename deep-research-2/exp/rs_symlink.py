import os, sys, subprocess, tempfile, time
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import stage2_research_snapshot as snap
def git(root, *a): subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True)
for case in ("committed-symlink", "submodule", "unstaged-deletion"):
    root = Path(tempfile.mkdtemp(dir=sys.argv[2])) / "repo"; root.mkdir()
    git(root, "init", "-q"); git(root, "config", "user.email", "x@invalid"); git(root, "config", "user.name", "x")
    (root / "plans/changes/ex").mkdir(parents=True); (root / "plans/changes/ex/research.md").write_text("r\n")
    (root / "AGENTS.md").write_text("rules\n")
    if case == "committed-symlink":
        os.symlink("AGENTS.md", root / "CLAUDE.md")  # in-repo, relative, harmless
    if case == "submodule":
        sub = root.parent / "sub"; sub.mkdir(); git(sub, "init", "-q"); (sub / "f").write_text("f"); git(sub, "add", "."); git(sub, "-c", "user.email=x@i", "-c", "user.name=x", "commit", "-qm", "s")
        subprocess.run(["git", "-C", str(root), "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub), "vendor/sub"], check=True, capture_output=True)
    git(root, "add", "-A"); git(root, "commit", "-qm", "base")
    if case == "unstaged-deletion":
        (root / "AGENTS.md").unlink()
    try:
        st = snap.freeze_research_state(root, "plans/changes/ex", deadline=time.monotonic() + 30)
        print(case, "-> frozen", sorted(st.manifest()["paths"])); st.close()
    except snap.ResearchSnapshotError as e:
        print(case, "-> ResearchSnapshotError:", e, "| cause:", repr(e.__cause__))
