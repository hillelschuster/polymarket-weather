"""Live trader — executes supervisor dead-bucket NO detections on Polymarket CLOB with strict risk controls."""
import json, os, sys, time, urllib.request, socket
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

socket.setdefaulttimeout(20.0)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
try:
    from scripts.supervisor import bucket_parse, MAP, US_F, fee, target_local_date, official_outcome
except ImportError:
    from supervisor import bucket_parse, MAP, US_F, fee, target_local_date, official_outcome

DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
DET = os.path.join(DATA, "detections.jsonl")
STATE = os.path.join(DATA, "live_state.json")
ORDERS = os.path.join(DATA, "live_orders.jsonl")
LIVE_CLOSURES = os.path.join(DATA, "live_closures.jsonl")
RUNLOG = os.path.join(DATA, "run.log")
ENVF = os.path.join(ROOT, ".env")
PAUSE = os.path.join(DATA, "PAUSE")

DEFAULT_MAX_TOTAL_EXPOSURE_USD = 150.0
DEFAULT_CARD = 15.0
DEFAULT_MAX_OPEN = 15
DEFAULT_MAX_TRADES_DAY = 30
DEFAULT_MAX_COST_DAY = 300.0
DEFAULT_ALERT_MAX_AGE_SEC = 600
PRICE_FLOOR = 0.50   # Hard floor: reject all sub-50c lottery/adverse selection traps
PRICE_CEILING = 0.88
PX_TOL = 0.03
EDGE_MIN = 0.030
MAX_SLIPPAGE = 0.08
POLL_SEC = 30
TICK = 0.001
BASE_LIVE_RULES = ("R2_low_dead_below", "R3_high_dead_above", "R5_high_dead_below")

_clob_client = None

def env():
    cfg = {"LIVE_ENABLED": "false", "PRIVATE_KEY": "", "FUNDER": "", "DRY_RUN": "true", "CHAIN_ID": "137",
           "MAX_TOTAL_EXPOSURE_USD": str(DEFAULT_MAX_TOTAL_EXPOSURE_USD), "CARD": str(DEFAULT_CARD),
           "MAX_OPEN": str(DEFAULT_MAX_OPEN), "MAX_TRADES_DAY": str(DEFAULT_MAX_TRADES_DAY),
           "MAX_COST_DAY": str(DEFAULT_MAX_COST_DAY), "ALLOW_LOTTOS": "false",
           "ALERT_MAX_AGE_SEC": str(DEFAULT_ALERT_MAX_AGE_SEC)}
    if os.path.exists(ENVF):
        try:
            with open(ENVF, "r", encoding="utf-8-sig", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        cfg[k.strip()] = v.split("#", 1)[0].strip().strip('"').strip("'")
        except Exception: pass
    for k in cfg:
        if k in os.environ: cfg[k] = os.environ[k]
    return cfg

def say(msg):
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] [TRADER] {msg}"
    try:
        with open(RUNLOG, "a", encoding="utf-8", errors="replace") as f: f.write(line + "\n")
    except Exception: pass
    if sys.stdout and sys.stdout.isatty(): print(line, flush=True)

def jload(path, default):
    try:
        with open(path, encoding="utf-8", errors="replace") as f: return json.load(f)
    except Exception: return default

def jsave(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", errors="replace") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    for _ in range(5):
        try:
            os.replace(tmp, path); return
        except Exception: time.sleep(0.05)

def jlog(path, obj):
    with open(path, "a", encoding="utf-8", errors="replace") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def get(url, retries=4, base_delay=1.0, max_delay=15.0, timeout=25):
    import random
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "PolymarketWeatherTrader/2.0"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r: return json.loads(r.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt >= retries: raise
            retry_after = exc.headers.get("Retry-After")
            delay = None
            if retry_after:
                try: delay = min(float(retry_after), max_delay)
                except (ValueError, TypeError): pass
            if delay is None:
                delay = min(base_delay * (2 ** attempt), max_delay) * random.uniform(0.75, 1.25)
            time.sleep(delay)
        except Exception:
            if attempt >= retries: raise
            time.sleep(min(base_delay * (2 ** attempt), max_delay) * random.uniform(0.75, 1.25))
    raise RuntimeError(f"HTTP request failed: {url}")

def tick_round(p): return max(TICK, round(p / TICK) * TICK)

def parse_filled_shares(detail, default_shares=0.0, side="BUY", client=None):
    if not isinstance(detail, dict): return 0.0
    for f in ("filled_size", "filledSize", "sizeMatched", "size_matched", "matched_size"):
        if detail.get(f) is not None:
            try:
                v = float(detail[f])
                return v / 1e6 if v > 10000 else v
            except Exception: pass
    target_f = "takingAmount" if str(side).upper() == "BUY" else "makingAmount"
    if detail.get(target_f) is not None:
        try:
            v = float(detail[target_f])
            return v / 1e6 if v > 10000 else v
        except Exception: pass

    # If orderID is present, query client.get_order() for exact fill status
    order_id = detail.get("orderID") or detail.get("orderId")
    if order_id and client is not None:
        try:
            order_info = client.get_order(order_id)
            if isinstance(order_info, dict):
                for f in ("size_matched", "sizeMatched", "filled_size"):
                    if order_info.get(f) is not None:
                        v = float(order_info[f])
                        return v / 1e6 if v > 10000 else v
        except Exception: pass

    # In py_clob_client, a successful FAK order returns {"success": True, "orderID": "...", "orderHashes": [...]}
    if detail.get("success") is True and detail.get("orderHashes"):
        return float(default_shares)

    return float(default_shares) if detail.get("status") in ("matched", "filled") else 0.0

def get_clob_client(cfg):
    global _clob_client
    if _clob_client is None and cfg.get("PRIVATE_KEY"):
        from py_clob_client.client import ClobClient
        client = ClobClient("https://clob.polymarket.com", key=cfg["PRIVATE_KEY"], chain_id=int(cfg.get("CHAIN_ID") or 137),
                            signature_type=1 if cfg.get("FUNDER") else 0, funder=cfg.get("FUNDER") or None)
        client.set_api_creds(client.create_or_derive_api_creds())
        _clob_client = client
    return _clob_client

def place_order(cfg, token_id, price, size, side="BUY"):
    from py_clob_client.clob_types import OrderArgs, OrderType, PartialCreateOrderOptions, BUY, SELL
    client = get_clob_client(cfg)
    if client is None:
        from py_clob_client.client import ClobClient
        client = ClobClient("https://clob.polymarket.com", key=cfg["PRIVATE_KEY"], chain_id=int(cfg.get("CHAIN_ID") or 137),
                            signature_type=1 if cfg.get("FUNDER") else 0, funder=cfg.get("FUNDER") or None)
        client.set_api_creds(client.create_or_derive_api_creds())
        global _clob_client
        _clob_client = client
    order = client.create_and_post_order(
        OrderArgs(token_id=str(token_id), price=round(float(price), 3), size=float(size),
                  side=BUY if str(side).upper() == "BUY" else SELL),
        options=PartialCreateOrderOptions(neg_risk=True, tick_size="0.001"),
        order_type=OrderType.FAK,
    )
    if isinstance(order, dict) and not order.get("success", True):
        raise RuntimeError(f"CLOB rejected: {order.get('errorMsg') or order}")
    return True, order

def fresh_book(det):
    toks, yi = det.get("tokens"), det.get("yes_idx", 0)
    if not toks or len(toks) < 2: return None
    try:
        no_tok = toks[1 - yi]
        bk_no = get(f"https://clob.polymarket.com/book?token_id={no_tok}")
        asks_no = sorted(bk_no.get("asks") or [], key=lambda x: float(x.get("price", 1))) if isinstance(bk_no, dict) else []
        if not asks_no or float(asks_no[0].get("size", 0)) <= 0:
            return None
        return (float(asks_no[0]["price"]), float(asks_no[0]["size"]), toks, yi)
    except Exception as ex:
        say(f"fresh_book error: {ex}"); return None

def read_new_detections(state):
    if not os.path.exists(DET): return []
    offset = state.get("det_offset", 0)
    if offset > os.path.getsize(DET): offset = 0
    new_dets = []
    with open(DET, "rb") as f:
        f.seek(offset)
        while True:
            line_start = f.tell()
            raw_line = f.readline()
            if not raw_line: break
            if not raw_line.endswith(b"\n"):
                f.seek(line_start)
                break
            stripped = raw_line.strip()
            if not stripped:
                state["det_offset"] = f.tell()
                continue
            try:
                new_dets.append(json.loads(stripped.decode("utf-8", errors="replace")))
                state["det_offset"] = f.tell()
            except Exception:
                state["det_offset"] = f.tell()
    return new_dets

def run_position_guard(cfg, state):
    now = datetime.now(timezone.utc)
    open_pos = state.get("open", {})
    if not open_pos: return
    open_cities = list({v.get("city") for v in open_pos.values() if v.get("city") in MAP})
    stations = [MAP[c][0] for c in open_cities if MAP[c][0] != "hko"]
    temps = {}
    if stations:
        try:
            for m in (get(f"https://aviationweather.gov/api/data/metar?ids={','.join(stations)}&format=json") or []):
                if m.get("icaoId") and m.get("temp") is not None and m["icaoId"] not in temps:
                    temps[m["icaoId"]] = float(m["temp"])
        except Exception: pass
    if "Hong Kong" in open_cities:
        try:
            r = get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en", timeout=10)
            t = next((s["value"] for s in r.get("temperature", {}).get("data", []) if s.get("place") == "Hong Kong Observatory"), None)
            if t is not None: temps["hko"] = float(t)
        except Exception: pass

    closed = []
    for key, pos in list(open_pos.items()):
        city, rule, side, token = pos.get("city"), pos.get("rule", ""), pos.get("side", ""), pos.get("token")
        shares, entry_px, is_dry = pos.get("shares", 0), pos.get("px", 0.0), pos.get("dry", True)
        if not city or not token or shares <= 0 or city not in MAP: continue
        # Maximum temperature is monotonic; evening cooling does not threaten R5 dead-below positions
        if rule == "R5_high_dead_below": continue
        obs_c = temps.get(MAP[city][0])
        if obs_c is None: continue
        is_f = city in US_F
        obs = obs_c * 9 / 5 + 32 if is_f else obs_c
        bp = bucket_parse(pos.get("bucket"))
        if not bp: continue
        dist = (obs - bp[1]) if rule in ("R2_low_dead_below", "R5_high_dead_below") else (bp[0] - obs)
        if dist >= (1.3 if is_f else 0.7): continue

        say(f"[GUARD TRIGGERED] {key} dist={dist:.2f}")
        try:
            bk = get(f"https://clob.polymarket.com/book?token_id={token}")
            bids = sorted(bk.get("bids") or [], key=lambda x: float(x.get("price", 0)))
            if not bids:
                say(f"[GUARD WARN] No bids to exit {key}; keeping position open")
                continue
            bid_px, exit_sh = float(bids[-1]["price"]), min(shares, float(bids[-1]["size"]))
            if exit_sh < 5: continue
            if is_dry:
                say(f"[GUARD DRY EXIT] SOLD {exit_sh} @ {bid_px:.3f}")
                jlog(ORDERS, {"ts": now.isoformat(), "key": key, "result": "GUARD_DRY_EXIT", "exit_px": bid_px, "entry_px": entry_px, "shares": exit_sh})
                if exit_sh >= shares: closed.append(key)
                else:
                    old_sh = pos["shares"]
                    pos["shares"] -= exit_sh
                    if old_sh > 0:
                        pos["cost"] = round(float(pos.get("cost", 0.0)) * (pos["shares"] / old_sh), 2)
            else:
                ok, detail = place_order(cfg, token, tick_round(bid_px), exit_sh, side="SELL")
                act_exit = parse_filled_shares(detail, default_shares=exit_sh, side="SELL", client=get_clob_client(cfg))
                if act_exit > 0:
                    say(f"[GUARD LIVE EXIT] SOLD {act_exit} @ {bid_px:.3f}")
                    jlog(ORDERS, {"ts": now.isoformat(), "key": key, "result": "GUARD_LIVE_EXIT", "exit_px": bid_px, "entry_px": entry_px, "shares": act_exit})
                    if act_exit >= shares: closed.append(key)
                    else:
                        old_sh = pos["shares"]
                        pos["shares"] -= act_exit
                        if old_sh > 0:
                            pos["cost"] = round(float(pos.get("cost", 0.0)) * (pos["shares"] / old_sh), 2)
                else:
                    say(f"[GUARD UNFILLED] 0 shares matched for {key}")
        except Exception as ex: say(f"[GUARD ERROR] {key}: {ex}")

    for k in closed:
        state["open"].pop(k, None)
        state["processed"][k] = {"ts": now.isoformat(), "action": "guard_exited"}
    jsave(STATE, state)

def process(cfg):
    state = jload(STATE, {"processed": {}, "open": {}, "daily": {}, "settling": {}, "det_offset": 0})
    if not isinstance(state, dict):
        state = {"processed": {}, "open": {}, "daily": {}, "settling": {}, "det_offset": 0}
    if not isinstance(state.get("daily"), dict): state["daily"] = {}
    if not isinstance(state.get("open"), dict): state["open"] = {}
    if not isinstance(state.get("processed"), dict): state["processed"] = {}
    if not isinstance(state.get("settling"), dict): state["settling"] = {}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = state["daily"].setdefault(today, {"trades": 0, "cost": 0.0})
    max_open = int(cfg.get("MAX_OPEN") or DEFAULT_MAX_OPEN)
    max_trades_day = int(cfg.get("MAX_TRADES_DAY") or DEFAULT_MAX_TRADES_DAY)
    max_cost_day = float(cfg.get("MAX_COST_DAY") or DEFAULT_MAX_COST_DAY)
    max_exp = float(cfg.get("MAX_TOTAL_EXPOSURE_USD") or DEFAULT_MAX_TOTAL_EXPOSURE_USD)
    alert_max_age = int(cfg.get("ALERT_MAX_AGE_SEC") or DEFAULT_ALERT_MAX_AGE_SEC)
    nowts = datetime.now(timezone.utc)

    # Prune expired open positions to release capacity and track in settling
    settling = state.setdefault("settling", {})
    for k, v in list(state["open"].items()):
        end = v.get("end") or v.get("endDate")
        expired = False
        if end:
            try:
                end_dt = datetime.fromisoformat(str(end).replace("Z", "+00:00"))
                if nowts > (end_dt if end_dt.tzinfo else end_dt.replace(tzinfo=timezone.utc)) + timedelta(hours=2): expired = True
            except Exception: pass
        if not expired and v.get("city") in MAP:
            try:
                # If local civil date has passed, release slot to prevent timezone deadlock
                tz = MAP[v["city"]][2]
                loc_t = nowts.astimezone(ZoneInfo(tz))
                tld = target_local_date(v.get("key", "").split("|")[0])
                if tld and (loc_t.year, loc_t.month, loc_t.day) > tld:
                    expired = True
            except Exception: pass
        if not expired and not end and v.get("city") not in MAP and v.get("ts"):
            try:
                ts_dt = datetime.fromisoformat(str(v["ts"]).replace("Z", "+00:00"))
                if nowts > (ts_dt if ts_dt.tzinfo else ts_dt.replace(tzinfo=timezone.utc)) + timedelta(hours=18): expired = True
            except Exception: pass
        if expired:
            settling[k] = v
            del state["open"][k]
            state["processed"][k] = {"ts": nowts.isoformat(), "action": "pruned_awaiting_settlement"}

    # Settle any positions in settling that have officially resolved on Polymarket
    for k, pos in list(settling.items()):
        official = official_outcome(pos)
        if official is None: continue
        bucket_hit = official
        pos_won = (not bucket_hit) if pos.get("side") == "NO" else bucket_hit
        filled_sh = float(pos.get("shares", 0))
        cost = float(pos.get("cost", 0))
        payout = filled_sh * 1.0 if pos_won else 0.0
        net_pnl = round(payout - cost, 2)
        jlog(LIVE_CLOSURES, {
            "ts": nowts.isoformat(), "key": k, "city": pos.get("city"), "bucket": pos.get("bucket"),
            "side": pos.get("side"), "shares": filled_sh, "entry_px": pos.get("px"),
            "cost_usd": cost, "won": pos_won, "payout_usd": round(payout, 2), "realized_pnl": net_pnl,
            "dry": pos.get("dry", True)
        })
        say(f"[SETTLED] {k} won={pos_won} pnl=${net_pnl:+.2f}")
        del settling[k]
        state["processed"][k] = {"ts": nowts.isoformat(), "action": "settled", "pnl": net_pnl}

    run_position_guard(cfg, state)

    for det in read_new_detections(state):
        key = det.get("key")
        if not key or det.get("rule") not in BASE_LIVE_RULES or det.get("side") != "NO": continue
        if det.get("px", 0.0) < PRICE_FLOOR or det.get("px", 0.0) > PRICE_CEILING: continue
        if key in state["processed"]: continue

        det_ts_str = det.get("ts")
        if not det_ts_str: continue
        try:
            det_dt = datetime.fromisoformat(str(det_ts_str).replace("Z", "+00:00"))
            if (nowts - (det_dt if det_dt.tzinfo else det_dt.replace(tzinfo=timezone.utc))).total_seconds() > alert_max_age:
                state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_stale_alert"}; continue
        except Exception: continue

        if os.path.exists(PAUSE): say("PAUSE file present — skipping"); continue
        cur_exp = sum(float(p.get("cost", 0.0) or (p.get("px", 0.0) * p.get("shares", 0.0))) for p in state["open"].values())
        rem_budget = max(0.0, max_exp - cur_exp)
        if rem_budget < 5 * TICK or len(state["open"]) >= max_open: continue
        if daily["trades"] >= max_trades_day or daily["cost"] >= max_cost_day: continue

        city_pos = [v for v in state["open"].values() if v.get("city") == det.get("city")]
        city_exp = sum(float(p.get("cost", 0.0) or (p.get("px", 0.0) * p.get("shares", 0.0))) for p in city_pos)
        rem_city_budget = max(0.0, 35.0 - city_exp)
        if len(city_pos) >= 3 or rem_city_budget < 5 * TICK: continue

        fb = fresh_book(det)
        if not fb or fb[0] is None: continue
        px_now, sz_now, tokens, yi = fb
        if px_now < PRICE_FLOOR or px_now > PRICE_CEILING: continue

        # Inherit q from detector to maintain exact margin coupling without artificial inflation
        q = det.get("q")
        if q is None:
            q = 0.97 if px_now > 0.70 else 0.92
        edge_now = q - px_now - fee(px_now)
        if edge_now < EDGE_MIN: continue
        if det.get("px") and (px_now - det["px"]) > MAX_SLIPPAGE: continue

        base_card = 15.0 if px_now <= 0.70 else (12.0 if px_now <= 0.85 else 8.0)
        card_tier = min(base_card, rem_budget, rem_city_budget)
        eff_px = px_now + fee(px_now)
        shares = int(min(card_tier / max(TICK, eff_px), 0.9 * sz_now))
        if shares < 5: continue

        cost = round(eff_px * shares, 2)
        token = tokens[1 - yi]
        base = {"ts": nowts.isoformat(), "key": key, "rule": det["rule"], "city": det["city"],
                "bucket": det["bucket"], "side": "NO", "alert_px": det.get("px"), "end": det.get("end")}

        dry = cfg.get("DRY_RUN", "true").lower() != "false" or cfg.get("LIVE_ENABLED", "false").lower() != "true"
        if dry:
            jlog(ORDERS, {**base, "result": "DRY_RUN_WOULD_ORDER", "px": round(px_now, 4), "shares": shares, "cost": cost, "token": token})
            say(f"DRY_RUN BUY NO {det['city']} {det['bucket']} px={px_now:.4f} x{shares} (${cost})")
            state["open"][key] = {**base, "token": token, "px": round(px_now, 4), "shares": shares, "cost": cost, "dry": True}
            daily["trades"] += 1; daily["cost"] += cost
        else:
            try:
                state["processed"][key] = {"ts": nowts.isoformat(), "action": "submitting_order"}
                jsave(STATE, state)
                ok, detail = place_order(cfg, token, tick_round(px_now), shares, side="BUY")
                filled = parse_filled_shares(detail, default_shares=shares, side="BUY", client=get_clob_client(cfg))
                if filled > 0:
                    act_cost = round(eff_px * filled, 2)
                    jlog(ORDERS, {**base, "result": "LIVE_ORDER", "px": round(px_now, 4), "shares": filled, "cost": act_cost, "token": token})
                    say(f"LIVE BUY NO {det['city']} {det['bucket']} px={px_now:.4f} x{filled} (${act_cost})")
                    state["open"][key] = {**base, "token": token, "px": round(px_now, 4), "shares": filled, "cost": act_cost, "dry": False}
                    daily["trades"] += 1; daily["cost"] += act_cost
                    state["processed"][key]["action"] = "filled"
                else:
                    state["processed"].pop(key, None)
                    say(f"[ORDER UNFILLED] 0 shares matched for {key}; eligible for retry")
            except Exception as ex:
                say(f"ORDER ERROR {key}: {ex}")
                state["processed"].pop(key, None)
    jsave(STATE, state)

if __name__ == "__main__":
    once = "--once" in sys.argv
    cfg = env()
    say(f"trader start | LIVE_ENABLED={cfg['LIVE_ENABLED']} DRY_RUN={cfg['DRY_RUN']} key={'set' if cfg['PRIVATE_KEY'] else 'MISSING'} once={once}")
    while True:
        try: process(env())
        except Exception as ex: say(f"pass error: {ex}")
        if once: break
        time.sleep(POLL_SEC)
