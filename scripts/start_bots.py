"""Standalone detached background launcher for Polymarket weather supervisor and trader."""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
LOG = os.path.join(DATA, "run.log")

py = sys.executable
# Win32: CREATE_NO_WINDOW (0x08000000) | CREATE_NEW_PROCESS_GROUP (0x00000200)
# NOTE: Never combine DETACHED_PROCESS (0x08) with CREATE_NO_WINDOW (0x08000000)
flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0

with open(LOG, "a", encoding="utf-8", errors="replace") as f:
    p1 = subprocess.Popen([py, "-u", os.path.join(ROOT, "scripts", "supervisor.py")],
                          cwd=ROOT, creationflags=flags, stdout=f, stderr=f, close_fds=True)
    p2 = subprocess.Popen([py, "-u", os.path.join(ROOT, "scripts", "live_trader.py")],
                          cwd=ROOT, creationflags=flags, stdout=f, stderr=f, close_fds=True)

print(f"Detached supervisor PID: {p1.pid}")
print(f"Detached trader PID: {p2.pid}")
