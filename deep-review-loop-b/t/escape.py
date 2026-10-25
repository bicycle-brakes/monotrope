import sys, time, os
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import stage2
t0 = time.monotonic()
try:
    stage2.launch(["/bin/sh", "-c", "setsid sleep 6 & sleep 100"], Path("/tmp"), dict(os.environ), timeout=1, limit="1s test limit")
except Exception as e:
    print(type(e).__name__, e, "after", round(time.monotonic() - t0, 1), "s")
