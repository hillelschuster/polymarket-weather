"""Process Watchdog — monitors and automatically restarts weather supervisor and trader if killed."""
import subprocess, sys, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
LOG = os.path.join(DATA, "run.log")
PID_FILE = os.path.join(DATA, "watchdog.pid")
CHECK_INTERVAL_SEC = 15
MAX_RAPID_CRASHES = 5
CRASH_WINDOW_SEC = 60

flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0

def spawn(script_name):
    with open(LOG, "a", encoding="utf-8", errors="replace") as f:
        p = subprocess.Popen([sys.executable, "-u", os.path.join(ROOT, "scripts", script_name)],
                             cwd=ROOT, creationflags=flags, stdout=f, stderr=f, close_fds=True)
    return p

def cleanup_children(procs):
    for p in procs:
        if p and p.poll() is None:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass

if __name__ == "__main__":
    try:
        with open(PID_FILE, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

    p_sup = spawn("supervisor.py")
    p_trd = spawn("live_trader.py")
    print(f"[WATCHDOG] Initialized: supervisor PID={p_sup.pid}, trader PID={p_trd.pid}")

    sup_crashes, trd_crashes = [], []

    try:
        while True:
            now = time.time()
            if p_sup.poll() is not None:
                sup_crashes = [t for t in sup_crashes if now - t < CRASH_WINDOW_SEC] + [now]
                if len(sup_crashes) >= MAX_RAPID_CRASHES:
                    print(f"[WATCHDOG] CRITICAL: Supervisor crashed {len(sup_crashes)} times in {CRASH_WINDOW_SEC}s. Pausing restarts for 60s.")
                    time.sleep(60)
                print(f"[WATCHDOG] Supervisor terminated (exit code {p_sup.returncode}). Restarting...")
                p_sup = spawn("supervisor.py")
                print(f"[WATCHDOG] Supervisor restarted with PID={p_sup.pid}")

            if p_trd.poll() is not None:
                trd_crashes = [t for t in trd_crashes if now - t < CRASH_WINDOW_SEC] + [now]
                if len(trd_crashes) >= MAX_RAPID_CRASHES:
                    print(f"[WATCHDOG] CRITICAL: Trader crashed {len(trd_crashes)} times in {CRASH_WINDOW_SEC}s. Pausing restarts for 60s.")
                    time.sleep(60)
                print(f"[WATCHDOG] Trader terminated (exit code {p_trd.returncode}). Restarting...")
                p_trd = spawn("live_trader.py")
                print(f"[WATCHDOG] Trader restarted with PID={p_trd.pid}")

            time.sleep(CHECK_INTERVAL_SEC)
    except KeyboardInterrupt:
        print("[WATCHDOG] Stopping watchdog and terminating child processes...")
    finally:
        cleanup_children([p_sup, p_trd])
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass
        print("[WATCHDOG] Clean shutdown complete.")
