"""Standalone detached background launcher for Polymarket weather supervisor and trader."""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
LOG = os.path.join(DATA, "run.log")

py = sys.executable.replace("python.exe", "pythonw.exe")
if not os.path.exists(py):
    py = sys.executable

p1 = subprocess.Popen([py, "-u", os.path.join(ROOT, "scripts", "supervisor.py")],
                      cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
p2 = subprocess.Popen([py, "-u", os.path.join(ROOT, "scripts", "live_trader.py")],
                      cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(f"Detached supervisor PID: {p1.pid}")
print(f"Detached trader PID: {p2.pid}")
