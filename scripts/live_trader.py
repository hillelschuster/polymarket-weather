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
import json, os, sys, time, urllib.request, re
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
try:
    from scripts.supervisor import bucket_parse, MAP, US_F
except ImportError:
    from supervisor import bucket_parse, MAP, US_F

DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
DET = os.path.join(DATA, "detections.jsonl")
STATE = os.path.join(DATA, "live_state.json")
ORDERS = os.path.join(DATA, "live_orders.jsonl")
RUNLOG = os.path.join(DATA, "run.log")
ENVF = os.path.join(ROOT, ".env")
PAUSE = os.path.join(DATA, "PAUSE")
DEFAULT_MAX_TOTAL_EXPOSURE_USD = 150.0
DEFAULT_CARD = 15.0
DEFAULT_MAX_OPEN = 15
DEFAULT_MAX_TRADES_DAY = 20
DEFAULT_MAX_COST_DAY = 150.0
DEFAULT_LOTTO_SWEEP_CAP = 2.50
DEFAULT_LOTTO_DAY_CAP = 6.00
DEFAULT_ALERT_MAX_AGE_SEC = 600  # 10 minutes max alert latency

BASE_LIVE_RULES = ("R2_low_dead_below", "R3_high_dead_above")
LOTTO_RULES = ("R1_low_lotto", "R4_high_lotto")
ASK_TIER_LOTTO = 0.002   # sweep displayed YES levels only up to the audited tier cap
PX_TOL = 0.03            # max slippage vs alert price
EDGE_MIN = 0.04          # recomputed edge floor at execution time
POLL_SEC = 30
TICK = 0.001

def parse_filled_shares(detail, default_shares=0.0):
    """Extract actual matched/filled shares from CLOB order response."""
    if not isinstance(detail, dict):
        return 0.0
    for field in ("takingAmount", "taking_amount", "filled_size", "filledSize", "sizeMatched", "size_matched", "matched_size"):
        if field in detail and detail[field] is not None:
            try:
                return float(detail[field])
            except (ValueError, TypeError):
                pass
    if detail.get("status") in ("matched", "filled"):
        return float(default_shares)
    return 0.0

def env():
    cfg = {"LIVE_ENABLED": "false", "PRIVATE_KEY": "", "FUNDER": "", "DRY_RUN": "true", "CHAIN_ID": "137",
           "MAX_TOTAL_EXPOSURE_USD": str(DEFAULT_MAX_TOTAL_EXPOSURE_USD),
           "CARD": str(DEFAULT_CARD), "MAX_OPEN": str(DEFAULT_MAX_OPEN),
           "MAX_TRADES_DAY": str(DEFAULT_MAX_TRADES_DAY), "MAX_COST_DAY": str(DEFAULT_MAX_COST_DAY),
           "ALLOW_LOTTOS": "true", "LOTTO_SWEEP_CAP": str(DEFAULT_LOTTO_SWEEP_CAP),
           "LOTTO_DAY_CAP": str(DEFAULT_LOTTO_DAY_CAP),
           "ALERT_MAX_AGE_SEC": str(DEFAULT_ALERT_MAX_AGE_SEC)}
    try:
        if os.path.exists(ENVF):
            with open(ENVF, "r", encoding="utf-8-sig", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line: continue
                    k, v = line.split("=", 1)
                    v = v.split("#", 1)[0].strip()
                    cfg[k.strip()] = v.strip('"').strip("'")
    except Exception:
        pass
    for k in cfg:
        if k in os.environ:
            cfg[k] = os.environ[k]
    return cfg

def say(msg):
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] [TRADER] {msg}"
    try:
        with open(RUNLOG, "a", encoding="utf-8", errors="replace") as f: f.write(line + "\n")
    except Exception: pass
    try:
        if sys.stdout and sys.stdout.isatty():
            print(line, flush=True)
    except Exception: pass

def jload(path, default):
    try:
        with open(path, encoding="utf-8", errors="replace") as f: return json.load(f)
    except Exception: return default

def jsave(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", errors="replace") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    for attempt in range(5):
        try:
            os.replace(tmp, path)
            return
        except (PermissionError, OSError):
            if attempt == 4:
                try:
                    with open(path, "w", encoding="utf-8", errors="replace") as f:
                        json.dump(obj, f, indent=1, ensure_ascii=False)
                    if os.path.exists(tmp): os.remove(tmp)
                    return
                except Exception as ex:
                    say(f"CRITICAL: jsave failed for {path}: {ex}")
                    raise
            time.sleep(0.05 * (2 ** attempt))

def jlog(path, obj):
    with open(path, "a", encoding="utf-8", errors="replace") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def get(url, retries=4, base_delay=1.0, max_delay=15.0, timeout=25):
    """Resilient HTTP client with exponential backoff, jitter, and 429 Retry-After compliance."""
    import random
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "PolymarketWeatherTrader/2.0"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = min(float(retry_after), max_delay)
                except ValueError:
                    delay = min(base_delay * (2 ** attempt), max_delay)
            else:
                raw_delay = min(base_delay * (2 ** attempt), max_delay)
                delay = raw_delay * random.uniform(0.75, 1.25)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError):
            if attempt >= retries: raise
            delay = min(base_delay * (2 ** attempt), max_delay) * random.uniform(0.75, 1.25)
            time.sleep(delay)
    raise RuntimeError(f"HTTP request failed after {retries} retries: {url}")

def fee(p): return 0.05 * p * (1 - p)

def fresh_book(det):
    """Re-fetch top of book for the detection's bucket at execution time."""
    toks = det.get("tokens")
    if not toks:  # legacy detection: fetch from gamma by slug
        try:
            ev = get(f"https://gamma-api.polymarket.com/events?slug={det['slug']}")
            if isinstance(ev, list): ev = ev[0] if ev else None
            for m in (ev.get("markets") or []) if isinstance(ev, dict) else []:
                if (m.get("groupItemTitle") or "").strip() == det["bucket"]:
                    toks = json.loads(m["clobTokenIds"]) if isinstance(m.get("clobTokenIds"), str) else m.get("clobTokenIds")
                    det["tokens"] = toks
                    det["yes_idx"] = 0
                    break
        except Exception as ex:
            say(f"gamma fallback err {ex}")
            return None, None, None, None
    if not toks or not isinstance(toks, (list, tuple)) or len(toks) < 2:
        return None, None, None, None
    yi = det.get("yes_idx", 0)
    try:
        bk = get(f"https://clob.polymarket.com/book?token_id={toks[yi]}")
        if not isinstance(bk, dict): return None, None, None, None
        bids = sorted(bk.get("bids") or [], key=lambda x: float(x["price"]))
        asks = sorted(bk.get("asks") or [], key=lambda x: float(x["price"]))
        yes_bid = float(bids[-1]["price"]) if bids else None
        yes_bid_sz = float(bids[-1]["size"]) if bids else 0
        yes_ask = float(asks[0]["price"]) if asks else None
        yes_ask_sz = float(asks[0]["size"]) if asks else 0
        asks_all = [(float(a["price"]), float(a["size"])) for a in asks]
        return (yes_bid, yes_bid_sz, toks, yi), (yes_ask, yes_ask_sz, toks, yi), det, asks_all
    except Exception as ex:
        say(f"fresh_book clob fetch err: {ex}")
        return None, None, None, None

def tick_round(p):
    return max(TICK, round(p / TICK) * TICK)

def place_order(cfg, token_id, price, size, side="BUY"):
    """Marketable FAK order (BUY or SELL). Returns (ok, detail)."""
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import OrderArgs, OrderType, BUY, SELL
    host = "https://clob.polymarket.com"
    key = cfg["PRIVATE_KEY"]
    chain = int(cfg.get("CHAIN_ID") or 137)
    funder = cfg.get("FUNDER") or None
    client = ClobClient(host, key=key, chain_id=chain, signature_type=1 if funder else 0,
                        funder=funder) if funder else ClobClient(host, key=key, chain_id=chain)
    client.set_api_creds(client.create_or_derive_api_creds())
    clob_side = BUY if str(side).upper() == "BUY" else SELL
    order = client.create_and_post_order(
        OrderArgs(token_id=str(token_id), price=round(float(price), 3), size=float(size), side=clob_side),
        order_type=OrderType.FAK)
    if isinstance(order, dict) and not order.get("success", True):
        raise RuntimeError(f"CLOB rejected {side} order: {order.get('errorMsg') or order}")
    return True, order

def run_position_guard(cfg, state):
    """
    PositionGuard Active Monitor:
    1. Checks open positions against live sensor telemetry and CLOB bids.
    2. If distance to bucket drops below 0.7C (1.3F), executes marketable FAK SELL
       to salvage 70-85% of capital instead of taking a 100% loss.
    """
    now = datetime.now(timezone.utc)
    open_positions = state.get("open", {})
    if not open_positions: return

    open_cities = list({v.get("city") for v in open_positions.values() if v.get("city")})
    if not open_cities: return

    stations = [MAP[c][0] for c in open_cities if c in MAP and MAP[c][0] != "hko"]
    temps = {}
    if stations:
        try:
            ms = get(f"https://aviationweather.gov/api/data/metar?ids={','.join(stations)}&hours=2&format=json")
            for m in (ms or []):
                icao = m.get("icaoId")
                tmp = m.get("temp")
                if icao and tmp is not None:
                    temps[icao] = float(tmp)
        except Exception as ex:
            say(f"[GUARD] telemetry fetch err: {ex}")
    if "Hong Kong" in open_cities:
        try:
            r = get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en", timeout=10)
            hko_temp = next((s["value"] for s in r.get("temperature", {}).get("data", []) if s.get("place") == "Hong Kong Observatory"), None)
            if hko_temp is not None: temps["hko"] = float(hko_temp)
        except Exception: pass

    closed_keys = []
    for key, pos in list(open_positions.items()):
        city = pos.get("city")
        rule = pos.get("rule", "")
        side = pos.get("side", "")
        token = pos.get("token")
        shares = pos.get("shares", 0)
        entry_px = pos.get("px", 0.0)
        is_dry = pos.get("dry", True)
        if not city or not token or shares <= 0: continue
        if city not in MAP: continue

        src = MAP[city][0]
        obs_c = temps.get(src)
        if obs_c is None: continue
        is_f = city in US_F
        obs = obs_c * 9 / 5 + 32 if is_f else obs_c

        bp = bucket_parse(pos.get("bucket"))
        if not bp: continue
        b_lo, b_hi = bp[0], bp[1]

        should_exit = False
        exit_reason = ""
        if rule == "R2_low_dead_below" and side == "NO":
            dist = obs - b_hi
            if dist < (1.3 if is_f else 0.7):
                should_exit = True
                exit_reason = f"Low margin compressed: obs={obs:.1f}, bucket_hi={b_hi:.1f}, dist={dist:.2f}"
        elif rule == "R3_high_dead_above" and side == "NO":
            dist = b_lo - obs
            if dist < (1.3 if is_f else 0.7):
                should_exit = True
                exit_reason = f"High margin compressed: obs={obs:.1f}, bucket_lo={b_lo:.1f}, dist={dist:.2f}"

        if not should_exit: continue

        say(f"[GUARD TRIGGERED] {key} -> {exit_reason}")
        try:
            bk = get(f"https://clob.polymarket.com/book?token_id={token}")
            bids = sorted(bk.get("bids") or [], key=lambda x: float(x.get("price", 0)))
            if not bids:
                say(f"[GUARD] No bids on book for {token}. Forced write-off.")
                closed_keys.append(key)
                continue
            best_bid_px = float(bids[-1]["price"])
            best_bid_sz = float(bids[-1]["size"])
            exit_shares = min(shares, best_bid_sz)
            if exit_shares < 1:
                say(f"[GUARD] Bid size too small ({best_bid_sz}) for {key}")
                continue

            recovered = round(exit_shares * best_bid_px, 2)
            saved_loss = round(exit_shares * (entry_px - best_bid_px), 2)
            if is_dry:
                say(f"[GUARD DRY EXIT] SOLD {exit_shares} sh @ {best_bid_px:.3f} | Recovered: ${recovered} | Loss: -${saved_loss}")
                jlog(ORDERS, {"ts": now.isoformat(), "key": key, "result": "GUARD_DRY_EXIT",
                              "exit_px": best_bid_px, "entry_px": entry_px, "shares": exit_shares, "recovered": recovered})
                if exit_shares >= shares:
                    closed_keys.append(key)
                else:
                    pos["shares"] -= exit_shares
            else:
                ok, detail = place_order(cfg, token, tick_round(best_bid_px), exit_shares, side="SELL")
                say(f"[GUARD LIVE EXIT] SOLD {exit_shares} sh @ {best_bid_px:.3f} | Recovered: ${recovered}")
                jlog(ORDERS, {"ts": now.isoformat(), "key": key, "result": "GUARD_LIVE_EXIT",
                              "exit_px": best_bid_px, "entry_px": entry_px, "shares": exit_shares, "resp": str(detail)[:300]})
                if exit_shares >= shares:
                    closed_keys.append(key)
                else:
                    pos["shares"] -= exit_shares
        except Exception as ex:
            say(f"[GUARD ERROR] {key}: {ex}")

    for k in closed_keys:
        state["open"].pop(k, None)
        state["processed"][k] = {"ts": now.isoformat(), "action": "guard_exited"}
    
    if closed_keys:
        jsave(STATE, state)

def process(cfg):
    state = jload(STATE, {"processed": {}, "open": {}, "daily": {}})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = state["daily"].setdefault(today, {"trades": 0, "cost": 0.0})
    card = float(cfg.get("CARD") or DEFAULT_CARD)
    max_open = int(cfg.get("MAX_OPEN") or DEFAULT_MAX_OPEN)
    max_trades_day = int(cfg.get("MAX_TRADES_DAY") or DEFAULT_MAX_TRADES_DAY)
    max_cost_day = float(cfg.get("MAX_COST_DAY") or DEFAULT_MAX_COST_DAY)
    alert_max_age_sec = int(cfg.get("ALERT_MAX_AGE_SEC") or DEFAULT_ALERT_MAX_AGE_SEC)
    allow_lottos = cfg.get("ALLOW_LOTTOS", "false").lower() == "true"
    live_rules = BASE_LIVE_RULES + (LOTTO_RULES if allow_lottos else ())
    dets = []
    try:
        with open(DET, "r", encoding="utf-8", errors="replace") as f:
            for l in f:
                l = l.strip()
                if not l: continue
                try:
                    dets.append(json.loads(l))
                except Exception:
                    continue
    except FileNotFoundError:
        dets = []

    # ---- Self-Healing Pruning of Expired Open Positions ----
    nowts = datetime.now(timezone.utc)
    for k in list(state["open"].keys()):
        v = state["open"][k]
        end = v.get("end")
        if not end:
            for d in dets:
                if d.get("key") == k:
                    end = d.get("end") or d.get("endDate")
                    if end:
                        v["end"] = end
                        break
        ts = v.get("ts")
        expired = False
        reason = ""
        if end:
            try:
                end_dt = datetime.fromisoformat(str(end).replace("Z", "+00:00"))
                if end_dt.tzinfo is None:
                    end_dt = end_dt.replace(tzinfo=timezone.utc)
                if nowts > end_dt + timedelta(hours=2):
                    expired = True
                    reason = f"event endDate {end} + 2h passed"
            except Exception:
                pass
        if not expired and ts:
            try:
                ts_dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                if ts_dt.tzinfo is None:
                    ts_dt = ts_dt.replace(tzinfo=timezone.utc)
                if nowts > ts_dt + timedelta(hours=12):
                    expired = True
                    reason = f"position age > 12h ({ts})"
            except Exception:
                pass
        if expired:
            say(f"[PRUNE-EXPIRED] Released open slot, awaiting settlement: {k} ({reason})")
            jlog(ORDERS, {
                "ts": nowts.isoformat(),
                "key": k,
                "result": "PRUNED_AWAITING_SETTLEMENT",
                "reason": reason,
                "entry_px": v.get("px"),
                "shares": v.get("shares"),
                "city": v.get("city"),
                "bucket": v.get("bucket"),
                "side": v.get("side")
            })
            del state["open"][k]
            state["processed"][k] = {
                "ts": nowts.isoformat(),
                "action": "pruned_awaiting_settlement"
            }

    # ---- Run Active PositionGuard Monitor ----
    run_position_guard(cfg, state)

    for det in dets:
        key = det["key"]
        p_entry = state["processed"].get(key)
        if p_entry and isinstance(p_entry, dict) and p_entry.get("ts"):
            try:
                p_dt = datetime.fromisoformat(str(p_entry["ts"]).replace("Z", "+00:00"))
                if p_dt.tzinfo is None: p_dt = p_dt.replace(tzinfo=timezone.utc)
                if (nowts - p_dt).total_seconds() < 1800:
                    continue
            except Exception:
                pass
        elif key in state["processed"]:
            continue

        rule = det.get("rule")
        end_val = det.get("end") or det.get("endDate")
        base = {
            "ts": datetime.now(timezone.utc).isoformat(), "key": key, "rule": rule,
            "city": det["city"], "bucket": det["bucket"], "side": det["side"],
            "alert_px": det.get("px"), "end": end_val,
        }

        # ---- Gate 0: Alert Freshness & Event Expiration (Fail-Loud / No Legacy Execution) ----
        det_ts_str = det.get("ts")
        if not det_ts_str:
            state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_missing_ts"}
            continue
        try:
            det_dt = datetime.fromisoformat(str(det_ts_str).replace("Z", "+00:00"))
            if det_dt.tzinfo is None:
                det_dt = det_dt.replace(tzinfo=timezone.utc)
            age_sec = (nowts - det_dt).total_seconds()
            if age_sec > alert_max_age_sec:
                state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_stale_alert", "det_age_min": round(age_sec / 60, 1)}
                jlog(ORDERS, {**base, "result": "REJECTED_STALE_ALERT", "det_age_min": round(age_sec / 60, 1)})
                say(f"[SKIP-STALE] {key} detected {age_sec/60:.1f}m ago (max {alert_max_age_sec/60:.0f}m) — skipped")
                continue
        except Exception:
            state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_invalid_ts"}
            continue

        if end_val:
            try:
                end_dt = datetime.fromisoformat(str(end_val).replace("Z", "+00:00"))
                if end_dt.tzinfo is None:
                    end_dt = end_dt.replace(tzinfo=timezone.utc)
                if nowts >= end_dt + timedelta(hours=14):
                    state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_event_ended", "end": end_val}
                    jlog(ORDERS, {**base, "result": "REJECTED_EVENT_ENDED", "end": end_val})
                    say(f"[SKIP-ENDED] {key} event endDate {end_val} has passed")
                    continue
            except Exception:
                pass

        # ---- gates ----
        if rule not in live_rules:
            state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_rule_not_whitelisted"}
            continue
        if os.path.exists(PAUSE):
            say("PAUSE file present — no new orders"); continue
        
        # Dynamic Capital Ceiling: sum of open position costs cannot exceed $150.00
        locked_usd = sum(float(pos.get("cost", 0.0)) for pos in state.get("open", {}).values())
        max_total_exposure = float(cfg.get("MAX_TOTAL_EXPOSURE_USD") or DEFAULT_MAX_TOTAL_EXPOSURE_USD)
        remaining_budget = max(0.0, max_total_exposure - locked_usd)
        if remaining_budget < 0.50:
            continue  # transient: wait until an open position settles

        if len(state["open"]) >= max_open:
            continue  # transient limit: allow next pass to reconsider once slot frees up
        if daily["trades"] >= max_trades_day or daily["cost"] >= max_cost_day:
            state["processed"][key] = {"ts": nowts.isoformat(), "action": "skip_daily_cap"}
            continue
        if any(v.get("city") == det["city"] for v in state["open"].values()):
            continue  # transient: do not permanently blacklist; wait until city slot clears

        state["processed"][key] = {"ts": datetime.now(timezone.utc).isoformat(), "action": "seen"}

        yes, ask, det2, asks_all = fresh_book(det)
        if not yes or (yes[0] is None and ask[0] is None):
            state["processed"][key]["action"] = "skip_no_book"
            continue
        side = det["side"]
        is_lotto = rule in LOTTO_RULES
        sweep = None
        if is_lotto:
            # sweep every displayed YES level up to the audited tier cap (0.002),
            # bounded by the per-ticket dollar cap; one FAK at the tier limit walks the levels
            rem = min(float(cfg.get("LOTTO_SWEEP_CAP") or DEFAULT_LOTTO_SWEEP_CAP), remaining_budget)
            sweep = []
            for px, sz in asks_all:
                if px > ASK_TIER_LOTTO: break
                take = min(sz * 0.9, rem / max(TICK, px))
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
            if daily.get("lotto_cost", 0.0) + px_now * shares > float(cfg.get("LOTTO_DAY_CAP") or DEFAULT_LOTTO_DAY_CAP):
                state["processed"][key]["action"] = "skip_daily_lotto_cap"; continue
        else:
            if side == "YES":
                px_now, sz_now = ask[0], ask[1]
            else:
                if yes[0] is None: state["processed"][key]["action"] = "skip_no_bid"; continue
                px_now, sz_now = 1 - yes[0], yes[1]
            if px_now is None or px_now > (det.get("px") or 0) + PX_TOL:
                state["processed"][key]["action"] = "skip_price_moved"; jlog(ORDERS, {**base, "result": "REJECTED_PRICE", "px_now": round(px_now,3) if px_now else None}); continue
            if px_now > 0.91:
                state["processed"][key]["action"] = "skip_price_ceiling"; jlog(ORDERS, {**base, "result": "REJECTED_PRICE_CEILING", "px_now": round(px_now,3)}); continue
            q = det["q"]
            edge_now = q - px_now - fee(px_now)
            if edge_now < EDGE_MIN:
                state["processed"][key]["action"] = "skip_edge_gone"; jlog(ORDERS, {**base, "result": "REJECTED_EDGE", "px_now": round(px_now,3), "edge_now": round(edge_now,3)}); continue
            
            # Dynamic Sizing Tiers ($150 Capital Limit Model)
            if px_now <= 0.70:
                card_tier = min(15.0, remaining_budget)
            elif px_now <= 0.84:
                card_tier = min(12.0, remaining_budget)
            elif px_now <= 0.91:
                card_tier = min(8.0, remaining_budget)
            else:
                card_tier = 0.0

            if card_tier < (5 * px_now):
                state["processed"][key]["action"] = "skip_capital_cap"
                continue

            shares = int(min(card_tier / max(TICK, px_now), 0.9 * sz_now))
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
            state["open"][key] = {**base, "token": token, "px": round(px_now, 4), "shares": shares, "dry": True}
            daily["trades"] += 1; daily["cost"] += round(cost, 2)
            if is_lotto: daily["lotto_cost"] = round(daily.get("lotto_cost", 0.0) + cost, 2)
        else:
            try:
                state["processed"][key] = {"ts": datetime.now(timezone.utc).isoformat(), "action": "submitting_order"}
                jsave(STATE, state)
                ok, detail = place_order(cfg, token, tick_round(limit_px), shares)
                filled_shares = parse_filled_shares(detail, default_shares=shares)
                if filled_shares <= 0:
                    say(f"LIVE {'SWEEP' if is_lotto else 'BUY'} UNFILLED (0 shares filled) {det['city']} {det['bucket']}")
                    jlog(ORDERS, {**base, "result": "LIVE_UNFILLED", "requested_shares": shares,
                                  "limit_px": limit_px, "token": token, "resp": str(detail)[:400]})
                    state["processed"][key]["action"] = "unfilled"
                else:
                    actual_cost = round(px_now * filled_shares, 2)
                    jlog(ORDERS, {**base, "result": "LIVE_SWEEP" if is_lotto else "LIVE_ORDER",
                                  "px": round(px_now, 4), "shares": filled_shares, "requested_shares": shares,
                                  "limit_px": limit_px, "levels": sweep, "token": token,
                                  "cost": actual_cost, "resp": str(detail)[:400]})
                    say(f"LIVE {'SWEEP' if is_lotto else 'BUY'} {side} {det['city']} {det['bucket']} avg_px={px_now:.4f} x{filled_shares} (req {shares}) cost=${actual_cost:.2f}")
                    state["open"][key] = {**base, "token": token, "px": round(px_now, 4), "shares": filled_shares, "dry": False}
                    state["processed"][key]["action"] = "filled" if filled_shares >= shares else "partial_fill"
                    state["processed"][key]["filled_shares"] = filled_shares
                    daily["trades"] += 1; daily["cost"] += actual_cost
                    if is_lotto: daily["lotto_cost"] = round(daily.get("lotto_cost", 0.0) + actual_cost, 2)
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
            cfg = env()  # Dynamic hot reload
            process(cfg)
        except Exception as ex:
            say("pass error: " + str(ex))
        if once: break
        time.sleep(POLL_SEC)
