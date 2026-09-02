"""Detached non-stop supervisor for Polymarket weather temperature markets.

Every cycle (~2 min):
  1. discovers active temperature events (cached 10 min);
  2. pulls resolver observations (aviationweather METAR batch + HKO official);
  3. for markets inside decision windows, pulls top-of-book for every bucket;
  4. fires conservative deterministic detectors (paper only — no orders sent);
  5. logs alerts to data/detections.jsonl, heartbeats to data/run.log;
  6. settles past events via IEM daily station data -> data/closures.jsonl
     with paper PnL per detection.

Run detached (Git Bash):   nohup python scripts/supervisor.py >/dev/null 2>&1 &
Windows detached:          run_supervisor.bat
Single cycle (test):       python scripts/supervisor.py --once
Stop:                      close the "weather-supervisor" window / kill python.
"""
import json, os, re, sys, time, urllib.request, socket
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

socket.setdefaulttimeout(20.0)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.environ.get("POLYWEATHER_DATA") or os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
DET = os.path.join(DATA, "detections.jsonl")
CLO = os.path.join(DATA, "closures.jsonl")
SURVEY = os.path.join(DATA, "survey.jsonl")
SEEN = os.path.join(DATA, "seen.json")
RUNLOG = os.path.join(DATA, "run.log")

# city -> (source, utc_off, iana_tz, dawn_local, last_light_local)  [August approximations]
MAP = {
    # Asian & Global cities (Restored & Verified)
    "Hong Kong": ("hko", 8, "Asia/Hong_Kong", 6.0, 18.8),
    "Seoul": ("RKSI", 9, "Asia/Seoul", 5.7, 18.7), "Busan": ("RKPK", 9, "Asia/Seoul", 5.8, 18.8),
    "Tokyo": ("RJTT", 9, "Asia/Tokyo", 5.5, 18.4), "Shanghai": ("ZSPD", 8, "Asia/Shanghai", 5.5, 18.3),
    "Beijing": ("ZBAA", 8, "Asia/Shanghai", 5.5, 18.9), "Taipei": ("RCSS", 8, "Asia/Taipei", 5.5, 18.2),
    "Chongqing": ("ZUCK", 8, "Asia/Shanghai", 6.0, 19.3), "Wuhan": ("ZHHH", 8, "Asia/Shanghai", 5.8, 19.0),
    "Chengdu": ("ZUUU", 8, "Asia/Shanghai", 6.3, 19.5), "Shenzhen": ("ZGSZ", 8, "Asia/Shanghai", 6.1, 18.9),
    "Guangzhou": ("ZGGG", 8, "Asia/Shanghai", 6.1, 18.9), "Singapore": ("WSSS", 8, "Asia/Singapore", 7.0, 19.1),
    "Kuala Lumpur": ("WMKK", 8, "Asia/Kuala_Lumpur", 7.1, 19.2), "Manila": ("RPLL", 8, "Asia/Manila", 5.7, 18.2),
    "Karachi": ("OPKC", 5, "Asia/Karachi", 6.0, 18.9), "Jeddah": ("OEJN", 3, "Asia/Riyadh", 5.9, 18.7),
    "Tel Aviv": ("LLBG", 3, "Asia/Jerusalem", 6.0, 19.2),
    "Cape Town": ("FACT", 2, "Africa/Johannesburg", 7.2, 18.3), "Wellington": ("NZWN", 12, "Pacific/Auckland", 7.1, 17.4),
    "Mexico City": ("MMMX", -6, "America/Mexico_City", 7.1, 19.9),
    "Sao Paulo": ("SBGR", -3, "America/Sao_Paulo", 6.3, 17.8),
    "Buenos Aires": ("SAEZ", -3, "America/Argentina/Buenos_Aires", 7.3, 18.3),

    # European cities
    "London": ("EGLC", 1, "Europe/London", 5.9, 20.2), "Paris": ("LFPB", 2, "Europe/Paris", 6.5, 20.8),
    "Amsterdam": ("EHAM", 2, "Europe/Amsterdam", 6.4, 20.7), "Warsaw": ("EPWA", 2, "Europe/Warsaw", 5.5, 19.8),
    "Helsinki": ("EFHK", 3, "Europe/Helsinki", 5.4, 20.9), "Madrid": ("LEMD", 2, "Europe/Madrid", 7.2, 20.9),
    "Milan": ("LIMC", 2, "Europe/Rome", 6.3, 20.2), "Munich": ("EDDM", 2, "Europe/Berlin", 6.2, 20.2),
    "Rome": ("LIRF", 2, "Europe/Rome", 6.2, 20.1), "Frankfurt": ("EDDF", 2, "Europe/Berlin", 6.1, 20.3),
    "Vienna": ("LOWW", 2, "Europe/Vienna", 5.8, 20.0), "Istanbul": ("LTFM", 3, "Europe/Istanbul", 6.1, 19.9),
    "Ankara": ("LTAC", 3, "Europe/Istanbul", 6.1, 19.7), "Moscow": ("UUWW", 3, "Europe/Moscow", 5.3, 19.9),

    # US cities
    "NYC": ("KLGA", -4, "America/New_York", 6.1, 19.5), "Miami": ("KMIA", -4, "America/New_York", 6.8, 19.5),
    "Atlanta": ("KATL", -4, "America/New_York", 6.9, 20.1), "Boston": ("KBOS", -4, "America/New_York", 5.9, 19.3),
    "Philadelphia": ("KPHL", -4, "America/New_York", 6.1, 19.4), "Washington DC": ("KDCA", -4, "America/New_York", 6.2, 19.5),
    "Chicago": ("KMDW", -5, "America/Chicago", 6.0, 19.4), "Dallas": ("KDAL", -5, "America/Chicago", 6.8, 20.1),
    "Austin": ("KAUS", -5, "America/Chicago", 6.9, 20.2), "Houston": ("KHOU", -5, "America/Chicago", 6.8, 19.9),
    "Denver": ("KDEN", -6, "America/Denver", 6.2, 19.4), "Phoenix": ("KPHX", -7, "America/Phoenix", 5.9, 19.3),
    "Las Vegas": ("KLAS", -7, "America/Los_Angeles", 6.0, 19.2),
    "Los Angeles": ("KLAX", -7, "America/Los_Angeles", 6.2, 19.3), "San Francisco": ("KSFO", -7, "America/Los_Angeles", 6.4, 19.4),
    "Seattle": ("KSEA", -7, "America/Los_Angeles", 6.2, 20.2), "Toronto": ("CYYZ", -4, "America/Toronto", 6.3, 19.9),
}
US_F = {"NYC", "Miami", "Chicago", "Dallas", "Austin", "Houston", "Denver", "Phoenix",
        "Los Angeles", "San Francisco", "Seattle", "Atlanta", "Boston", "Philadelphia",
        "Washington DC", "Las Vegas"}

CYCLE_SEC = 120
EVENT_CACHE_SEC = 600
# Sizing card for high-confidence dead-bucket NOs
SIZE_LOCKED = 15.0   # >=90% confidence states

def say(msg):
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}"
    try:
        with open(RUNLOG, "a", encoding="utf-8", errors="replace") as f:
            f.write(line + "\n")
    except Exception:
        pass
    try:
        if sys.stdout and sys.stdout.isatty():
            print(line, flush=True)
    except Exception:
        pass

def get(url, retries=4, base_delay=1.0, max_delay=15.0, timeout=25):
    """Production-grade resilient HTTP GET with exponential backoff, jitter, and Retry-After support."""
    import random
    headers = {"Accept": "application/json", "User-Agent": "PolymarketWeatherSupervisor/2.0"}
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode())
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

def log(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def atomic_save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    for _ in range(3):
        try:
            os.replace(tmp, path)
            break
        except Exception:
            time.sleep(0.05)

def load_seen():
    try:
        with open(SEEN, encoding="utf-8") as f:
            d = json.load(f)
            return d if isinstance(d, dict) else {k: 0 for k in d}
    except Exception: return {}

def save_seen(s):
    atomic_save_json(SEEN, s)

MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9, "october": 10, "oct": 10,
    "november": 11, "nov": 11, "december": 12, "dec": 12
}

def target_local_date(title, ref_dt=None):
    """'... on August 16?' -> (2026, 8, 16). Handles year boundaries adaptively."""
    m_year = re.search(r"(\b20\d\d\b)", title)
    m = re.search(r"on (\w+) (\d+)", title)
    if not m: return None
    mi = MONTHS.get(m.group(1).lower())
    if not mi: return None
    day = int(m.group(2))
    if m_year:
        return int(m_year.group(1)), mi, day
    ref = ref_dt or datetime.now(timezone.utc)
    y = ref.year
    if ref.month == 12 and mi == 1:
        y += 1
    elif ref.month == 1 and mi == 12:
        y -= 1
    return y, mi, day

def fee(p): return 0.05 * p * (1 - p)

def city_of(title):
    for k in MAP:
        if k in title: return k
    return None

def fetch_events():
    events, offset = [], 0
    while True:
        b = get(f"https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset={offset}")
        if not b: break
        events += b; offset += 100
        if len(b) < 100: break
    out = []
    for e in events:
        t = e.get("title") or ""
        if not t.startswith(("Highest temperature", "Lowest temperature")): continue
        c = city_of(t)
        if not c: continue
        out.append({"id": e.get("id"), "title": t, "city": c, "endDate": e.get("endDate"),
                    "slug": e.get("slug"), "markets": e.get("markets") or []})
    return out

def fetch_obs(events):
    need = sorted({MAP[e["city"]][0] for e in events if MAP[e["city"]][0] != "hko"})
    temps, raws, times = {}, {}, {}
    for i in range(0, len(need), 12):
        try:
            ms = get("https://aviationweather.gov/api/data/metar?ids=%s&format=json" % ",".join(need[i:i+12]))
            for m in ms:
                temps[m["icaoId"]] = m.get("temp")
                raws[m["icaoId"]] = m.get("rawOb") or ""
                times[m["icaoId"]] = m.get("obsTime")
        except Exception as ex:
            say("metar chunk err: %s" % ex)
    if "Hong Kong" in MAP:
        try:
            r = get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en")
            temps["hko"] = next((s["value"] for s in r.get("temperature", {}).get("data", [])
                                 if s.get("place") == "Hong Kong Observatory"), None)
            raws["hko"] = ""
            try:
                times["hko"] = datetime.fromisoformat(r.get("updateTime")).timestamp()
            except Exception:
                times["hko"] = None
            if "VHHH" not in temps:
                try:
                    ms = get("https://aviationweather.gov/api/data/metar?ids=VHHH&format=json")
                    if ms: temps["VHHH"] = ms[0].get("temp"); raws["VHHH"] = ms[0].get("rawOb") or ""; times["VHHH"] = ms[0].get("obsTime")
                except Exception: pass
        except Exception as ex:
            say("hko err: %s" % ex)
    return temps, raws, times

def bucket_parse(gt):
    """-> (lo, hi, val) supporting negative numbers, decimals, unicode dashes, and boundary phrases."""
    if not gt: return None
    gt = str(gt).strip()
    m_range = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:[-–—]|to)\s*(-?\d+(?:\.\d+)?)", gt)
    if m_range:
        a, b = float(m_range.group(1)), float(m_range.group(2))
        return (min(a, b) - 0.5, max(a, b) + 0.5, min(a, b))
    m_single = re.search(r"(-?\d+(?:\.\d+)?)", gt)
    if not m_single: return None
    v = float(m_single.group(1))
    gt_lower = gt.lower()
    if any(p in gt_lower for p in ("or below", "below", "or less", "less", "<")):
        return (float("-inf"), v + 0.5, v)
    if any(p in gt_lower for p in ("or higher", "above", "or more", "more", ">")):
        return (v - 0.5, float("inf"), v)
    return (v - 0.5, v + 0.5, v)

def top_of_book(event):
    rows = []
    for m in event.get("markets") or []:
        try:
            raw_title = (m.get("groupItemTitle") or "").strip()
            bp = bucket_parse(raw_title)
            if not bp: continue
            toks = m.get("clobTokenIds")
            if isinstance(toks, str): toks = json.loads(toks)
            outcomes = m.get("outcomes")
            if isinstance(outcomes, str): outcomes = json.loads(outcomes)
            yes_idx = next((i for i, o in enumerate(outcomes) if str(o).lower() == "yes"), 0) if outcomes else 0
            if not toks or len(toks) <= yes_idx: continue

            bk = get(f"https://clob.polymarket.com/book?token_id={toks[yes_idx]}")
            if not isinstance(bk, dict): continue
            bids = sorted(bk.get("bids") or [], key=lambda x: float(x.get("price", 0)))
            asks = sorted(bk.get("asks") or [], key=lambda x: float(x.get("price", 0)))
            rows.append({"bucket": raw_title, "lo": bp[0], "hi": bp[1], "val": bp[2],
                         "tokens": toks, "yes_idx": yes_idx,
                         "yes_bid": float(bids[-1]["price"]) if bids else None,
                         "yes_bid_sz": float(bids[-1]["size"]) if bids else 0,
                         "yes_ask": float(asks[0]["price"]) if asks else None,
                         "yes_ask_sz": float(asks[0]["size"]) if asks else 0})
            time.sleep(0.04)  # Rate pacing to prevent IP burst collisions with other bots
        except Exception:
            continue
    rows.sort(key=lambda r: r["val"])
    return rows

def fetch_running(in_window_events):
    """Running (day_max, day_min, trend) per station, restricted to each event's local calendar day.
    Uses instantaneous METARs for trend velocity and remarks extrema for daily bounds."""
    out = {}
    stations = sorted({(MAP[e["city"]][0], MAP[e["city"]][1], MAP[e["city"]][2]) for e in in_window_events})
    if not stations: return out
    for i in range(0, len(stations), 10):
        chunk = stations[i:i+10]
        ids = ",".join(("VHHH" if s == "hko" else s) for s, _, _ in chunk)
        try:
            # LOOKBACK FIX: 28 hours guarantees full 00:00 to 23:59 civil day coverage
            ms = get("https://aviationweather.gov/api/data/metar?ids=%s&hours=28&format=json" % ids)
        except Exception as ex:
            say("recent metar err %s" % ex); continue
        instant_by = {}
        extremes_by = {}
        for m in (ms or []):
            if not isinstance(m, dict): continue
            icao = m.get("icaoId")
            if not icao: continue
            t, tmp = m.get("obsTime"), m.get("temp")
            raw = m.get("rawOb") or ""
            if isinstance(t, (int, float)):
                # Decode high-precision T-group remarks (tenths Celsius): T(sn)(TTT)
                mT = re.search(r"\bT([01])(\d{3})(?:[01]\d{3})?\b", raw)
                if mT:
                    sign = -1.0 if mT.group(1) == "1" else 1.0
                    t_val = sign * (int(mT.group(2)) / 10.0)
                    instant_by.setdefault(icao, []).append((t, t_val))
                    extremes_by.setdefault(icao, []).append((t, t_val, False))
                elif isinstance(tmp, (int, float)):
                    instant_by.setdefault(icao, []).append((t, float(tmp)))
                    extremes_by.setdefault(icao, []).append((t, float(tmp), False))
                m6 = re.search(r"\b1([01])(\d{3})\b", raw)
                if m6:
                    extremes_by.setdefault(icao, []).append((t, (-1 if m6.group(1) == "1" else 1) * int(m6.group(2)) / 10, True))
                n6 = re.search(r"\b2([01])(\d{3})\b", raw)
                if n6:
                    extremes_by.setdefault(icao, []).append((t, (-1 if n6.group(1) == "1" else 1) * int(n6.group(2)) / 10, True))
        for (src, off, tz), _res in [(c, None) for c in chunk]:
            st = "VHHH" if src == "hko" else src
            ext_list = extremes_by.get(st) or []
            inst_list = instant_by.get(st) or []
            now_utc = datetime.now(timezone.utc)
            now_ts = now_utc.timestamp()
            try:
                nowloc = now_utc.astimezone(ZoneInfo(tz))
                day_start_utc = nowloc.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc).timestamp()
            except Exception:
                nowloc = now_utc + timedelta(hours=off)
                day_start_utc = (nowloc.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=off)).timestamp()
            # 15-minute tolerance captures routine 05:50-05:55Z synoptic transmissions
            vals = [tmp for tt, tmp, is_6h in ext_list if tt >= day_start_utc and (not is_6h or tt >= day_start_utc + 6 * 3600 - 900)]
            # calculate 30-90m trend (instantaneous rate of change in C/hr) strictly from instantaneous obs
            sorted_obs = sorted([(tt, tmp) for tt, tmp in inst_list if isinstance(tt, (int, float)) and tmp is not None], key=lambda x: x[0])
            trend = None
            if len(sorted_obs) >= 2:
                t_last, temp_last = sorted_obs[-1]
                # Guard against stale telemetry: trend only valid if latest obs <= 90m old
                if now_ts - t_last <= 5400:
                    for t_prev, temp_prev in reversed(sorted_obs[:-1]):
                        dt_hr = (t_last - t_prev) / 3600.0
                        if 0.3 <= dt_hr <= 1.5:
                            trend = round((temp_last - temp_prev) / dt_hr, 2)
                            break
            if vals:
                out[src] = (max(vals), min(vals), trend)
    return out

def detectors(event, city_cfg, local_hour, obs, precip, book, runmax=None, runmin=None, trend=None):
    """Conservative deterministic rules with progressive margin & velocity trend gating."""
    src, off, tz, dawn, lastlight = city_cfg
    is_low = event["title"].startswith("Lowest")
    is_f = event["city"] in US_F
    obs_m = obs * 9 / 5 + 32 if is_f else obs
    margin_base = 3.6 if is_f else 2.0     # 2.0C / 3.6F standard margin (p <= 0.70)
    margin_strict = 5.4 if is_f else 3.0   # 3.0C / 5.4F strict margin for high-price NOs (>0.70)
    out = []

    def mk(rule, side, q, r):
        px = max(0.001, float(1 - r["yes_bid"]))
        avail = float(r.get("yes_bid_sz", 0)) * 0.9
        card_tier = 15.0 if px <= 0.70 else (12.0 if px <= 0.85 else 8.0)
        eff_px = px + fee(px)
        want = card_tier / eff_px
        shares = max(0, int(min(want, avail)))
        edge = q - px - fee(px)
        return dict(rule=rule, side=side, q=q, edge=round(edge, 3), px=round(px, 4),
                    size_usd=round(shares * eff_px, 2), shares=shares, **r)

    for r in book:
        # state anchors: RUNNING extremes for the local day
        runmax_m = (runmax * 9 / 5 + 32) if (runmax is not None and is_f) else runmax
        runmin_m = (runmin * 9 / 5 + 32) if (runmin is not None and is_f) else runmin

        # Velocity filter: block low-side entries if temperature is rapidly falling (trend < -0.3 C/hr)
        trend_ok_low = (trend is None) or (trend >= -0.3)
        if is_low and runmin is not None and (dawn - 2.5) <= local_hour <= (dawn + 2.5) and not precip and trend_ok_low:
            # R2 dead-below: progressive margin based on price
            if r.get("yes_bid") is not None:
                no_ask = 1 - r["yes_bid"]
                req_margin = margin_strict if no_ask > 0.70 else margin_base
                if r["hi"] <= runmin_m - req_margin:
                    q_no = 0.97 if no_ask > 0.70 else 0.92
                    if q_no - no_ask - fee(no_ask) > 0.04:
                        out.append(mk("R2_low_dead_below", "NO", q_no, r))

        # High-side contracts: R3 dead-above & R5 dead-below in afternoon window
        trend_ok_high = (trend is None) or (trend <= 0.3)
        in_afternoon = (lastlight - 3.5) <= local_hour <= (lastlight + 3.0)
        if (not is_low) and runmax is not None and in_afternoon:
            if r.get("yes_bid") is not None:
                no_ask = 1 - r["yes_bid"]
                # R3 dead-above after peak heating window
                if trend_ok_high:
                    req_margin = margin_strict if no_ask > 0.70 else margin_base
                    q_no = 0.97 if no_ask > 0.70 else 0.92
                    if q_no - no_ask - fee(no_ask) > 0.04:
                        if r["lo"] >= runmax_m + req_margin:
                            out.append(mk("R3_high_dead_above", "NO", q_no, r))
                # R5 dead-below (MONOTONIC: daily high can never decrease)
                mono_buf = 1.0 if is_f else 0.6
                if r["hi"] <= runmax_m - mono_buf:
                    q_no = 0.97 if no_ask > 0.70 else 0.92
                    if q_no - no_ask - fee(no_ask) > 0.04:
                        out.append(mk("R5_high_dead_below", "NO", q_no, r))
    return out

def official_outcome(det):
    """If the market itself has resolved (closed + outcomePrices), return bucket_hit (bool)
    from the official result; else None. Settle strictly on official exchange ground truth."""
    try:
        slug = det.get("slug")
        if not slug:
            t = det.get("title", "").replace("?", "").strip()
            t = re.sub(r"[^a-zA-Z0-9\s-]", "", t).strip().lower()
            slug = re.sub(r"\s+", "-", t) + "-2026"
        evg = get(f"https://gamma-api.polymarket.com/events?slug={slug}")
        if isinstance(evg, list): evg = evg[0] if evg else None
        if not evg or not evg.get("closed"): return None
        for m in evg.get("markets") or []:
            b_title = (m.get("groupItemTitle") or "").strip().replace("\ufffd", "°")
            det_b = (det.get("bucket") or "").strip().replace("\ufffd", "°")
            if b_title == det_b:
                op = m.get("outcomePrices")
                if op is None: return None
                prices = json.loads(op) if isinstance(op, str) else op
                if not isinstance(prices, (list, tuple)) or not prices: return None
                try:
                    num_prices = [float(p) for p in prices if p is not None]
                except (ValueError, TypeError): return None
                # Guard against transitional zeroed prices before UMA settlement finalization
                if sum(num_prices) < 0.90 or sum(num_prices) > 1.10:
                    return None
                outcomes = m.get("outcomes") or ["Yes", "No"]
                if isinstance(outcomes, str): outcomes = json.loads(outcomes)
                yi = next((i for i, o in enumerate(outcomes) if str(o).lower() == "yes"), 0) if outcomes else 0
                if len(num_prices) > yi:
                    return num_prices[yi] > 0.5
    except Exception:
        return None
    return None

def settle_past(seen_pending):
    """Settle detected events strictly against Polymarket's official resolution API.
    Zero proxy guessing. If the market is not officially closed on Polymarket, keep pending."""
    now = datetime.now(timezone.utc)
    done = []
    for key, det in list(seen_pending.items()):
        official = official_outcome(det)
        if official is None:
            # Polymarket has not officially closed/resolved the contract yet — keep pending
            continue
        bucket_hit = official
        pos_won = bucket_hit if det["side"] == "YES" else (not bucket_hit)
        px = det.get("px") or (det["yes_ask"] if det["side"] == "YES" else 1 - det["yes_bid"])
        px = max(0.001, float(px))
        shares = det.get("shares") if det.get("shares") is not None else (det.get("size_usd", 0) / px)
        pnl = (shares * (1 if pos_won else 0)) - shares * px - fee(px) * shares
        log(CLO, {
            "ts": now.isoformat(), "key": key, "city": det["city"], "station": "OFFICIAL_POLYMARKET",
            "title": det["title"], "slug": det.get("slug"), "bucket": det["bucket"], "side": det["side"],
            "bucket_hit": bucket_hit, "pos_won": pos_won,
            "paper_size_usd": round(shares * px, 2), "shares": round(shares, 1),
            "entry_px": round(px, 4), "resolver_extremum": -999,
            "won": pos_won, "paper_pnl": round(pnl, 2), "note": "re-verified official settlement"
        })
        say(f"[SETTLED-OFFICIAL] {det['city']} {det['bucket']} {det['side']} bucket_hit={bucket_hit} pos_won={pos_won} pnl={pnl:+.2f}")
        done.append(key)
    for k in done:
        seen_pending.pop(k, None)

def cycle(events_cache):
    now = datetime.now(timezone.utc)
    if events_cache is None or (now - events_cache[0]).total_seconds() > EVENT_CACHE_SEC:
        events_cache = (now, fetch_events())
    events = events_cache[1]
    temps, raws, times = fetch_obs(events)
    seen = load_seen()
    pending = {}
    try:
        with open(os.path.join(DATA, "pending.json"), encoding="utf-8") as f:
            pending = json.load(f)
    except Exception: pass

    active = 0
    # pass 1: find in-window events
    in_window_events = []
    for e in events:
        city = e["city"]
        src, off, tz, dawn, lastlight = MAP[city]
        try:
            end = datetime.fromisoformat((e["endDate"] or "").replace("Z", "+00:00"))
        except Exception: continue
        hrs = (end - now).total_seconds() / 3600
        if not (-14 < hrs < 48): continue
        try:
            local = now.astimezone(ZoneInfo(tz))
        except Exception:
            local = now + timedelta(hours=off)
        local_hour = local.hour + local.minute / 60.0
        # CRITICAL: only act inside the event's own local calendar day
        tld = target_local_date(e["title"])
        if tld is None or (local.year, local.month, local.day) != tld:
            continue
        is_low = e["title"].startswith("Lowest")
        in_window = ((dawn - 2.5) <= local_hour <= (dawn + 2.5)) if is_low else ((lastlight - 3.5) <= local_hour <= (lastlight + 3.0))
        if not in_window: continue
        obs = temps.get(src) if src != "hko" else temps.get("hko")
        if obs is None: continue
        in_window_events.append((e, obs))

    running = fetch_running([e for e, _ in in_window_events])

    # pass 2: books + detectors with running-extremum state
    for e, obs in in_window_events:
        city = e["city"]
        src, off, tz, dawn, lastlight = MAP[city]
        try:
            local = now.astimezone(ZoneInfo(tz))
        except Exception:
            local = now + timedelta(hours=off)
        local_hour = local.hour + local.minute / 60.0
        raw = raws.get("VHHH" if src == "hko" else src, "")
        precip = bool(re.search(r"(?:^|\s)([-+]?(?:RA|SN|DZ|PL|GR|GS|SHRA|TSRA|RASN|SNRA|SHSN))\b", raw))
        run_info = running.get(src, (None, None, None))
        runmax, runmin = run_info[0], run_info[1]
        trend = run_info[2] if len(run_info) > 2 else None
        book = top_of_book(e)
        active += 1

        # ---- SURVEY: record EVERY in-window state (denominator) regardless of detectors ----
        is_low = e["title"].startswith("Lowest")
        is_f = city in US_F
        anchor = runmin if is_low else runmax
        anchor_m = (anchor * 9 / 5 + 32) if (anchor is not None and is_f) else anchor
        minutes_to_lock = round(((dawn if is_low else lastlight) - local_hour) * 60)
        obs_t = times.get("VHHH" if src == "hko" else src)
        obs_age_min = round((now.timestamp() - obs_t) / 60, 1) if obs_t else None
        rel = []
        for r in book:
            contains = anchor_m is not None and r["lo"] <= anchor_m < r["hi"]
            adjacent = anchor_m is not None and (0 < anchor_m - r["hi"] <= 1.6 or 0 < r["lo"] - anchor_m <= 1.6)
            cheap = r["yes_ask"] is not None and r["yes_ask"] <= 0.02
            if contains or adjacent or cheap:
                bd = round(min(anchor_m - r["lo"], r["hi"] - anchor_m), 2) if contains else None
                rel.append({"b": r["bucket"], "bid": r["yes_bid"], "ask": r["yes_ask"],
                            "ask_sz": r["yes_ask_sz"], "contains": contains, "bd": bd})
        log(SURVEY, {"ts": now.isoformat(), "title": e["title"], "city": city,
                     "side": "low" if is_low else "high", "min_to_lock": minutes_to_lock,
                     "runmax": runmax, "runmin": runmin, "obs": obs, "obs_age_min": obs_age_min,
                     "precip": precip, "buckets": rel, "trend_c_per_hr": trend})

        for d in detectors(e, MAP[city], local_hour, obs, precip, book, runmax, runmin, trend):
            if d.get("shares", 0) < 5:   # CLOB minimum order size
                continue
            key = f"{e['title']}|{d['bucket']}|{d['side']}"
            if key in seen and (now.timestamp() - float(seen.get(key, 0))) < 1800: continue
            seen[key] = now.timestamp()
            bd = next((x["bd"] for x in rel if x["b"] == d["bucket"] and x["bd"] is not None), None)
            rec = {"ts": now.isoformat(), "key": key, "city": city, "title": e["title"],
                   "slug": e.get("slug"), "end": e["endDate"], "resolver_obs_c": obs,
                   "runmax_c": runmax, "runmin_c": runmin, "trend_c_per_hr": trend,
                   "minutes_to_lock": minutes_to_lock, "obs_age_min": obs_age_min,
                   "boundary_distance": bd, **d}
            log(DET, rec)
            pending[key] = rec
            px = d.get("yes_ask") if d["side"] == "YES" else round(1 - d["yes_bid"], 3)
            say(f"[ALERT] {d['rule']} {city} {d['bucket']} {d['side']} px={px} edge={d['edge']} obs={obs}C runmax={runmax} runmin={runmin} trend={trend}")
        save_seen(seen)  # per-event persistence prevents duplicate re-fires after mid-cycle errors
    save_seen(seen)
    atomic_save_json(os.path.join(DATA, "pending.json"), pending)
    settle_past(pending)
    atomic_save_json(os.path.join(DATA, "pending.json"), pending)
    say(f"cycle done: {len(events)} events, {active} in window, {len(pending)} pending")
    return events_cache

if __name__ == "__main__":
    once = "--once" in sys.argv
    cache = None
    say("supervisor starting (pid=%s, once=%s)" % (os.getpid(), once))
    while True:
        try:
            cache = cycle(cache)
        except KeyboardInterrupt:
            say("stopped"); break
        except Exception as ex:
            say("cycle error: " + str(ex))
        if once: break
        time.sleep(CYCLE_SEC)
