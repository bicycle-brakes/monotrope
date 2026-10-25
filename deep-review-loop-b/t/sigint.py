import sys, threading, time, os, signal, subprocess
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import stage2
t0 = time.monotonic()
child = Path(sys.argv[2])
def one():
    try:
        stage2.launch(["/bin/sh", "-c", f"echo $$ > {child}; sleep 8"], Path("/tmp"), dict(os.environ), timeout=60)
        print("worker: child finished after", round(time.monotonic()-t0,1), "s", flush=True)
    except Exception as e:
        print("worker exc", e, flush=True)
th = threading.Thread(target=one); th.start()
threading.Timer(1.0, lambda: os.kill(os.getpid(), signal.SIGINT)).start()
try:
    th.join()
except KeyboardInterrupt:
    print("main: KeyboardInterrupt at", round(time.monotonic()-t0,1), "s; child pid", child.read_text().strip(), flush=True)
    raise SystemExit(130)
