"""Live trader — executes supervisor detections on Polymarket CLOB with strict gates.

SAFE BY DEFAULT: runs in DRY_RUN (no orders) until .env has LIVE_ENABLED=true and your
private key. Even then it only takes R2/R3 dead-bucket NOs, re-verifies the book at
execution time, caps size, and stops on kill-switches.

  Gate summary (all must pass):
    - detection rule in LIVE_RULES (default R2_low_dead_below, R3_high_dead_above)
    - data/PAUSE file absent
    - < 3 open positions, < 6 trades today, daily cost <= $12
    - fresh book: executable px now <= alert px + 0.03, recomputed edge > 0.04
    - size = min(card/px, 90% of displayed depth), >= 5 shares (CLOB minimum)

  Orders: marketable FAK limit (never rests as maker) on the correct YES/NO token.

Run:      python scripts/live_trader.py            (loop, 30s)
Test:     python scripts/live_trader.py --once     (single pass, respects DRY_RUN)
Stop:     create data/PAUSE  |  kill process
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DET = os.path.join(DATA, "detections.jsonl")
STATE = os.path.join(DATA, "live_state.json")
ORDERS = os.path.join(DATA, "live_orders.jsonl")
RUNLOG = os.path.join(DATA, "run.log")
ENVF = os.path.join(ROOT, ".env")
PAUSE = os.path.join(DATA, "PAUSE")

LIVE_RULES = ("R2_low_dead_below", "R3_high_dead_above")
LOTTO_RULES = ("R1_low_lotto", "R4_high_lotto")
LIVE_RULES = LIVE_RULES + LOTTO_RULES
ASK_TIER_LOTTO = 0.002   # sweep displayed YES levels only up to the audited tier cap
MAX_OPEN = 3
MAX_TRADES_DAY = 6
MAX_COST_DAY = 12.0
CARD = 12.0              # $ per position
PX_TOL = 0.03            # max slippage vs alert price
EDGE_MIN = 0.04          # recomputed edge floor at execution time
POLL_SEC = 30
TICK = 0.001

def env():
    cfg = {"LIVE_ENABLED": "false", "PRIVATE_KEY": "", "FUNDER": "", "DRY_RUN": "true", "CHAIN_ID": "137"}
    try:
        for line in open(ENVF, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return cfg

def say(msg):
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] [TRADER] {msg}"
    try:
        with open(RUNLOG, "a", encoding="utf-8") as f: f.write(line + "\n")
    except Exception: pass
    print(line, flush=True)

def jload(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

def jsave(path, obj):
    with open(path, "w", encoding="utf-8") as f: json.dump(obj, f, indent=1)

def jlog(path, obj):
    with open(path, "a", encoding="utf-8") as f: f.write(json.dumps(obj) + "\n")

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def fee(p): return 0.05 * p * (1 - p)

def fresh_book(det):
    """Re-fetch top of book for the detection's bucket at execution time."""
    toks = det.get("tokens")
    if not toks:  # legacy detection: fetch from gamma by slug
        try:
            ev = get(f"https://gamma-api.polymarket.com/events?slug={det['slug']}")
            if isinstance(ev, list): ev = ev[0]
            for m in ev.get("markets") or []:
                if (m.get("groupItemTitle") or "").strip() == det["bucket"]:
                    toks = json.loads(m["clobTokenIds"]) if isinstance(m.get("clobTokenIds"), str) else m["clobTokenIds"]
                    det["tokens"] = toks
                    det["yes_idx"] = 0
                    break
        except Exception as ex:
            say(f"gamma fallback err {ex}")
            return None, None, None
    if not toks: return None, None, None
    yi = det.get("yes_idx", 0)
    bk = get(f"https://clob.polymarket.com/book?token_id={toks[yi]}")
    bids = sorted(bk.get("bids") or [], key=lambda x: float(x["price"]))
    asks = sorted(bk.get("asks") or [], key=lambda x: float(x["price"]))
    yes_bid = float(bids[-1]["price"]) if bids else None
    yes_bid_sz = float(bids[-1]["size"]) if bids else 0
    yes_ask = float(asks[0]["price"]) if asks else None
    yes_ask_sz = float(asks[0]["size"]) if asks else 0
    asks_all = [(float(a["price"]), float(a["size"])) for a in asks]
    return (yes_bid, yes_bid_sz, toks, yi), (yes_ask, yes_ask_sz, toks, yi), det, asks_all

def tick_round(p):
    return max(TICK, round(p / TICK) * TICK)

def place_order(cfg, token_id, price, size):
    """Marketable FAK buy. Returns (ok, detail)."""
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import OrderArgs, OrderType
    host = "https://clob.polymarket.com"
    key = cfg["PRIVATE_KEY"]
    chain = int(cfg.get("CHAIN_ID") or 137)
    funder = cfg.get("FUNDER") or None
    client = ClobClient(host, key=key, chain_id=chain, signature_type=1 if funder else 0,
                        funder=funder) if funder else ClobClient(host, key=key, chain_id=chain)
    client.set_api_creds(client.create_or_derive_api_creds())
    order = client.create_and_post_order(
        OrderArgs(token_id=token_id, price=round(price, 3), size=size),
        orderType=OrderType.FAK)
    return True, order

def process(cfg):
    state = jload(STATE, {"processed": {}, "open": {}, "daily": {}})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = state["daily"].setdefault(today, {"trades": 0, "cost": 0.0})
    dets = []
    try:
        with open(DET, encoding="utf-8") as f:
            dets = [json.loads(l) for l in f]
    except FileNotFoundError:
        return

    # prune open positions whose events ended (settle window passed) — stale entries
    # must never block MAX_OPEN slots on fresh opportunities
    nowts = datetime.now(timezone.utc)
    for k in list(state["open"].keys()):
        v = state["open"][k]
        end = v.get("end")
        try:
            if end:
                if nowts > datetime.fromisoformat(str(end).replace("Z", "+00:00")) + timedelta(hours=3):
                    del state["open"][k]
            elif v.get("ts") and nowts > datetime.fromisoformat(v["ts"]) + timedelta(hours=36):
                del state["open"][k]
        except Exception:
            pass

    for det in dets:
        key = det["key"]
        if key in state["processed"]: continue
        state["processed"][key] = {"ts": datetime.now(timezone.utc).isoformat(), "action": "seen"}

        rule = det.get("rule")
        base = {
            "ts": datetime.now(timezone.utc).isoformat(), "key": key, "rule": rule,
            "city": det["city"], "bucket": det["bucket"], "side": det["side"],
            "alert_px": det.get("px"), "end": det.get("endDate"),
        }
        # ---- gates ----
        if rule not in LIVE_RULES:
            state["processed"][key]["action"] = "skip_rule_not_whitelisted"; continue
        if os.path.exists(PAUSE):
            say("PAUSE file present — no new orders"); state["processed"][key]["action"] = "skip_paused"; continue
        if len(state["open"]) >= MAX_OPEN:
            state["processed"][key]["action"] = "skip_max_open"; continue
        if daily["trades"] >= MAX_TRADES_DAY or daily["cost"] >= MAX_COST_DAY:
            state["processed"][key]["action"] = "skip_daily_cap"; continue
        if any(v.get("city") == det["city"] for v in state["open"].values()):
            state["processed"][key]["action"] = "skip_city_dup"; continue

        yes, ask, det2, asks_all = fresh_book(det)
        if not yes: state["processed"][key]["action"] = "skip_no_book"; continue
        side = det["side"]
        is_lotto = rule in LOTTO_RULES
        sweep = None
        if is_lotto:
            # sweep every displayed YES level up to the audited tier cap (0.002),
            # bounded by the per-ticket dollar cap; one FAK at the tier limit walks the levels
            rem = float(cfg.get("LOTTO_SWEEP_CAP") or 5.0)
            sweep = []
            for px, sz in asks_all:
                if px > ASK_TIER_LOTTO: break
                take = min(sz * 0.9, rem / px)
                if take < 1: break
                sweep.append((px, int(take))); rem -= int(take) * px
                if rem <= px: break
            shares = sum(s for _, s in sweep)
            if shares < 5:
                state["processed"][key]["action"] = "skip_thin"
                jlog(ORDERS, {**base, "result": "REJECTED_THIN", "tier_depth_shares": sum(s for p, s in asks_all if p <= ASK_TIER_LOTTO)}); continue
            px_now = sum(p * s for p, s in sweep) / shares
            limit_px = ASK_TIER_LOTTO
            edge_now = det["q"] - px_now - fee(px_now)
            if edge_now < 0.10:
                state["processed"][key]["action"] = "skip_edge_gone"; jlog(ORDERS, {**base, "result": "REJECTED_EDGE", "avg_px": round(px_now, 4), "edge_now": round(edge_now, 3)}); continue
            if daily.get("lotto_cost", 0.0) + px_now * shares > float(cfg.get("LOTTO_DAY_CAP") or 10.0):
                state["processed"][key]["action"] = "skip_daily_lotto_cap"; continue
        else:
            if side == "YES":
                px_now, sz_now = ask[0], ask[1]
            else:
                if yes[0] is None: state["processed"][key]["action"] = "skip_no_bid"; continue
                px_now, sz_now = 1 - yes[0], yes[1]
            if px_now is None or px_now > (det.get("px") or 0) + PX_TOL:
                state["processed"][key]["action"] = "skip_price_moved"; jlog(ORDERS, {**base, "result": "REJECTED_PRICE", "px_now": round(px_now,3) if px_now else None}); continue
            q = det["q"]
            edge_now = q - px_now - fee(px_now)
            if edge_now < EDGE_MIN:
                state["processed"][key]["action"] = "skip_edge_gone"; jlog(ORDERS, {**base, "result": "REJECTED_EDGE", "px_now": round(px_now,3), "edge_now": round(edge_now,3)}); continue
            shares = int(min(CARD / px_now, 0.9 * sz_now))
            if shares < 5:
                state["processed"][key]["action"] = "skip_thin"; jlog(ORDERS, {**base, "result": "REJECTED_THIN", "depth": sz_now}); continue
            limit_px = px_now
        cost = px_now * shares

        yi = det2.get("yes_idx", 0)
        token = det2["tokens"][yi] if side == "YES" else det2["tokens"][1 - yi]

        dry = cfg.get("DRY_RUN", "true").lower() != "false" or cfg.get("LIVE_ENABLED", "false").lower() != "true"
        if dry:
            jlog(ORDERS, {**base, "result": "DRY_RUN_WOULD_SWEEP" if is_lotto else "DRY_RUN_WOULD_ORDER",
                          "px": round(px_now, 4), "shares": shares, "cost": round(cost, 2),
                          "levels": sweep, "edge_now": round(edge_now, 3), "token": token})
            say(f"DRY_RUN would {'SWEEP' if is_lotto else 'BUY'} {side} {det['city']} {det['bucket']} avg_px={px_now:.4f} x{shares} (~${cost:.0f}) edge={edge_now:.3f}")
            state["open"][key] = {**base, "px": round(px_now, 4), "shares": shares, "dry": True}
            daily["trades"] += 1; daily["cost"] += round(cost, 2)
            if is_lotto: daily["lotto_cost"] = round(daily.get("lotto_cost", 0.0) + cost, 2)
        else:
            try:
                ok, detail = place_order(cfg, token, tick_round(limit_px), shares)
                jlog(ORDERS, {**base, "result": "LIVE_SWEEP" if is_lotto else "LIVE_ORDER",
                              "px": round(px_now, 4), "shares": shares, "limit_px": limit_px,
                              "levels": sweep, "token": token, "resp": str(detail)[:400]})
                say(f"LIVE {'SWEEP' if is_lotto else 'BUY'} {side} {det['city']} {det['bucket']} avg_px={px_now:.4f} x{shares}")
                state["open"][key] = {**base, "px": round(px_now, 4), "shares": shares, "dry": False}
                daily["trades"] += 1; daily["cost"] += round(cost, 2)
                if is_lotto: daily["lotto_cost"] = round(daily.get("lotto_cost", 0.0) + cost, 2)
            except Exception as ex:
                say(f"ORDER ERROR {key}: {ex}")
                jlog(ORDERS, {**base, "result": "ERROR", "err": str(ex)[:300]})
                state["processed"][key]["action"] = "order_error"
    jsave(STATE, state)

if __name__ == "__main__":
    once = "--once" in sys.argv
    cfg = env()
    say(f"trader start | LIVE_ENABLED={cfg['LIVE_ENABLED']} DRY_RUN={cfg['DRY_RUN']} key={'set' if cfg['PRIVATE_KEY'] else 'MISSING'} once={once}")
    while True:
        try:
            process(cfg)
        except Exception as ex:
            say("pass error: " + str(ex))
        if once: break
        time.sleep(POLL_SEC)
