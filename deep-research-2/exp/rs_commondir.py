import sys, subprocess, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import stage2_research_store as s
base = Path(tempfile.mkdtemp(dir=sys.argv[2]))
main = base / "main"; main.mkdir()
g = lambda *a, cwd=main: subprocess.run(["git", "-C", str(cwd), *a], check=True, capture_output=True, text=True).stdout.strip()
g("init", "-q"); (main / "f").write_text("f"); g("add", "f"); g("-c", "user.email=x@i", "-c", "user.name=x", "commit", "-qm", "b")
wt = main / ".claude/worktrees/w"; g("worktree", "add", "-q", str(wt))
git_dir = g("rev-parse", "--absolute-git-dir", cwd=wt); common = g("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=wt)
print("absolute-git-dir:", git_dir); print("common dir:     ", common)
for store_dir in (Path(common) / "state/research", main / "state/research"):
    try:
        s.Store(store_dir).assert_outside(wt, git_dir, home=base / "home"); print("ACCEPTED", store_dir)
    except s.StoreWriteError as e:
        print("refused", store_dir, e)
