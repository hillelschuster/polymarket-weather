"""Process Watchdog — monitors and automatically restarts weather supervisor and trader if killed."""
import subprocess, sys, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LOG = os.path.join(DATA, "run.log")
CHECK_INTERVAL_SEC = 15

def spawn(script_name):
    flags = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
    with open(LOG, "a", encoding="utf-8") as f:
        p = subprocess.Popen([sys.executable, "-u", os.path.join(ROOT, "scripts", script_name)],
                             cwd=ROOT, creationflags=flags, stdout=f, stderr=f, close_fds=True)
    return p

if __name__ == "__main__":
    p_sup = spawn("supervisor.py")
    p_trd = spawn("live_trader.py")
    print(f"[WATCHDOG] Initialized: supervisor PID={p_sup.pid}, trader PID={p_trd.pid}")

    while True:
        try:
            if p_sup.poll() is not None:
                print(f"[WATCHDOG] Supervisor terminated (exit code {p_sup.returncode}). Restarting...")
                p_sup = spawn("supervisor.py")
                print(f"[WATCHDOG] Supervisor restarted with PID={p_sup.pid}")

            if p_trd.poll() is not None:
                print(f"[WATCHDOG] Trader terminated (exit code {p_trd.returncode}). Restarting...")
                p_trd = spawn("live_trader.py")
                print(f"[WATCHDOG] Trader restarted with PID={p_trd.pid}")

            time.sleep(CHECK_INTERVAL_SEC)
        except KeyboardInterrupt:
            print("[WATCHDOG] Stopping watchdog.")
            break
        except Exception as ex:
            time.sleep(5)
