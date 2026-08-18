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
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
DET = os.path.join(DATA, "detections.jsonl")
CLO = os.path.join(DATA, "closures.jsonl")
SURVEY = os.path.join(DATA, "survey.jsonl")
SEEN = os.path.join(DATA, "seen.json")
RUNLOG = os.path.join(DATA, "run.log")

# city -> (source, utc_off, iana_tz, dawn_local, last_light_local)  [August approximations]
# NOTE: Hong Kong suspended from auto-eligible cities until HKO-native historical API is wired.
# Station anchor (VHHH airport) diverges from official resolver (HKO downtown).
MAP = {
    # "Hong Kong": ("hko", 8, "Asia/Hong_Kong", 6.0, 18.8),
    "Seoul": ("RKSI", 9, "Asia/Seoul", 5.7, 18.7), "Busan": ("RKPK", 9, "Asia/Seoul", 5.8, 18.8),
    "Tokyo": ("RJTT", 9, "Asia/Tokyo", 5.5, 18.4), "Shanghai": ("ZSPD", 8, "Asia/Shanghai", 5.5, 18.3),
    "Beijing": ("ZBAA", 8, "Asia/Shanghai", 5.5, 18.9), "Taipei": ("RCSS", 8, "Asia/Taipei", 5.5, 18.2),
    "Chongqing": ("ZUCK", 8, "Asia/Shanghai", 6.0, 19.3), "Wuhan": ("ZHHH", 8, "Asia/Shanghai", 5.8, 19.0),
    "Chengdu": ("ZUUU", 8, "Asia/Shanghai", 6.3, 19.5), "Shenzhen": ("ZGSZ", 8, "Asia/Shanghai", 6.1, 18.9),
    "Guangzhou": ("ZGGG", 8, "Asia/Shanghai", 6.1, 18.9), "Singapore": ("WSSS", 8, "Asia/Singapore", 7.0, 19.1),
    "Kuala Lumpur": ("WMKK", 8, "Asia/Kuala_Lumpur", 7.1, 19.2), "Manila": ("RPLL", 8, "Asia/Manila", 5.7, 18.2),
    "Karachi": ("OPKC", 5, "Asia/Karachi", 6.0, 18.9), "Jeddah": ("OEJN", 3, "Asia/Riyadh", 5.9, 18.7),
    "Tel Aviv": ("LLBG", 3, "Asia/Jerusalem", 6.0, 19.2), "Istanbul": ("LTFM", 3, "Europe/Istanbul", 6.1, 19.9),
    "Ankara": ("LTAC", 3, "Europe/Istanbul", 6.1, 19.7), "Moscow": ("UUWW", 3, "Europe/Moscow", 5.3, 19.9),
    "Cape Town": ("FACT", 2, "Africa/Johannesburg", 7.2, 18.3), "Wellington": ("NZWN", 12, "Pacific/Auckland", 7.1, 17.4),
    "London": ("EGLC", 1, "Europe/London", 5.9, 20.2), "Paris": ("LFPB", 2, "Europe/Paris", 6.5, 20.8),
    "Amsterdam": ("EHAM", 2, "Europe/Amsterdam", 6.4, 20.7), "Warsaw": ("EPWA", 2, "Europe/Warsaw", 5.5, 19.8),
    "Helsinki": ("EFHK", 3, "Europe/Helsinki", 5.4, 20.9), "Madrid": ("LEMD", 2, "Europe/Madrid", 7.2, 20.9),
    "Milan": ("LIMC", 2, "Europe/Rome", 6.3, 20.2), "Munich": ("EDDM", 2, "Europe/Berlin", 6.2, 20.2),
    "Rome": ("LIRF", 2, "Europe/Rome", 6.2, 20.1), "Frankfurt": ("EDDF", 2, "Europe/Berlin", 6.1, 20.3),
    "Vienna": ("LOWW", 2, "Europe/Vienna", 5.8, 20.0),
    "NYC": ("KLGA", -4, "America/New_York", 6.1, 19.5), "Miami": ("KMIA", -4, "America/New_York", 6.8, 19.5),
    "Atlanta": ("KATL", -4, "America/New_York", 6.9, 20.1), "Boston": ("KBOS", -4, "America/New_York", 5.9, 19.3),
    "Philadelphia": ("KPHL", -4, "America/New_York", 6.1, 19.4), "Washington DC": ("KDCA", -4, "America/New_York", 6.2, 19.5),
    "Chicago": ("KMDW", -5, "America/Chicago", 6.0, 19.4), "Dallas": ("KDAL", -5, "America/Chicago", 6.8, 20.1),
    "Austin": ("KAUS", -5, "America/Chicago", 6.9, 20.2), "Houston": ("KHOU", -5, "America/Chicago", 6.8, 19.9),
    "Denver": ("KDEN", -6, "America/Denver", 6.2, 19.4), "Phoenix": ("KPHX", -7, "America/Phoenix", 5.9, 19.3),
    "Las Vegas": ("KLAS", -7, "America/Los_Angeles", 6.0, 19.2),
    "Los Angeles": ("KLAX", -7, "America/Los_Angeles", 6.2, 19.3), "San Francisco": ("KSFO", -7, "America/Los_Angeles", 6.4, 19.4),
    "Seattle": ("KSEA", -7, "America/Los_Angeles", 6.2, 20.2), "Toronto": ("CYYZ", -4, "America/Toronto", 6.3, 19.9),
    "Mexico City": ("MMMX", -6, "America/Mexico_City", 7.1, 19.9),
    "Sao Paulo": ("SBSP", -3, "America/Sao_Paulo", 6.3, 17.8),
    "Buenos Aires": ("SABE", -3, "America/Argentina/Buenos_Aires", 7.3, 18.3),
}
US_F = {"NYC", "Miami", "Chicago", "Dallas", "Austin", "Houston", "Denver", "Phoenix",
        "Los Angeles", "San Francisco", "Seattle", "Atlanta", "Boston", "Philadelphia",
        "Washington DC", "Las Vegas"}

CYCLE_SEC = 120
EVENT_CACHE_SEC = 600
# $250 sizing card (10% per locked position, ~$3 lotto)
SIZE_LOCKED = 25.0   # >=90% confidence states
SIZE_LOTTO = 3.0     # cheap asks <= 0.002
# Audit 2026-08-16 tier math: break-even q = p+0.05*p*(1-p) = 0.21% at 0.002 vs 1.05-2.1%
# at 0.01-0.02; state-sample 95% lower bound 0.84% clears ONLY the <=0.002 tier (4x).
# Both Paris lotto losses were 0.01-0.019 entries; the HK win was 0.001.
# 1-2c states remain recorded by the survey logger for later re-admission with evidence.
ASK_MAX_LOTTO = 0.002

def say(msg):
    line = f"[{datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}"
    try:
        with open(RUNLOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    try:
        if sys.stdout:
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
        except (urllib.error.URLError, TimeoutError, OSError):
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
    os.replace(tmp, path)

def load_seen():
    try:
        with open(SEEN, encoding="utf-8") as f: return set(json.load(f))
    except Exception: return set()

def save_seen(s):
    atomic_save_json(SEEN, sorted(s))

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"], 1)}

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
    """-> (lo, hi, val) supporting negative numbers, decimals, and boundary phrases."""
    gt = gt.strip()
    m_range = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:-|to)\s*(-?\d+(?:\.\d+)?)", gt)
    if m_range:
        a, b = float(m_range.group(1)), float(m_range.group(2))
        return (a - 0.5, b + 0.5, a)
    m_single = re.search(r"(-?\d+(?:\.\d+)?)", gt)
    if not m_single: return None
    v = float(m_single.group(1))
    gt_lower = gt.lower()
    if "or below" in gt_lower or "below" in gt_lower or "<" in gt_lower:
        return (float("-inf"), v + 0.5, v)
    if "or higher" in gt_lower or "above" in gt_lower or ">" in gt_lower:
        return (v - 0.5, float("inf"), v)
    return (v - 0.5, v + 0.5, v)

def top_of_book(event):
    rows = []
    for m in event["markets"]:
        bp = bucket_parse(m.get("groupItemTitle") or "")
        if not bp: continue
        toks = json.loads(m["clobTokenIds"]) if isinstance(m.get("clobTokenIds"), str) else m.get("clobTokenIds")
        outcomes = json.loads(m.get("outcomes")) if isinstance(m.get("outcomes"), str) else m.get("outcomes")
        yes_idx = outcomes.index("Yes") if outcomes and "Yes" in outcomes else 0
        try:
            bk = get(f"https://clob.polymarket.com/book?token_id={toks[yes_idx]}")
        except Exception:
            continue
        bids = sorted(bk.get("bids") or [], key=lambda x: float(x["price"]))
        asks = sorted(bk.get("asks") or [], key=lambda x: float(x["price"]))
        rows.append({"bucket": m.get("groupItemTitle").strip(), "lo": bp[0], "hi": bp[1], "val": bp[2],
                     "tokens": toks, "yes_idx": yes_idx,
                     "yes_bid": float(bids[-1]["price"]) if bids else None,
                     "yes_bid_sz": float(bids[-1]["size"]) if bids else 0,
                     "yes_ask": float(asks[0]["price"]) if asks else None,
                     "yes_ask_sz": float(asks[0]["size"]) if asks else 0})
        time.sleep(0.04)  # Rate pacing to prevent IP burst collisions with other bots
    rows.sort(key=lambda r: r["val"])
    return rows

def fetch_running(in_window_events):
    """Running (day_max, day_min) per station, restricted to each event's local calendar day.
    Returns {(station): (runmax, runmin)} using up to 14h of recent METARs."""
    out = {}
    stations = sorted({(MAP[e["city"]][0], MAP[e["city"]][1]) for e in in_window_events})
    if not stations: return out
    for i in range(0, len(stations), 10):
        chunk = stations[i:i+10]
        ids = ",".join("VHHH" if s == "hko" else s for s, _ in chunk)
        try:
            ms = get("https://aviationweather.gov/api/data/metar?ids=%s&hours=14&format=json" % ids)
        except Exception as ex:
            say("recent metar err %s" % ex); continue
        by = {}
        for m in ms:
            t, tmp = m.get("obsTime"), m.get("temp")
            raw = m.get("rawOb") or ""
            if isinstance(t, (int, float)):
                if tmp is not None:
                    by.setdefault(m["icaoId"], []).append((t, tmp))
                m6 = re.search(r"\b1([01])(\d{3})\b", raw)
                if m6:
                    by.setdefault(m["icaoId"], []).append((t, (-1 if m6.group(1) == "1" else 1) * int(m6.group(2)) / 10))
                n6 = re.search(r"\b2([01])(\d{3})\b", raw)
                if n6:
                    by.setdefault(m["icaoId"], []).append((t, (-1 if n6.group(1) == "1" else 1) * int(n6.group(2)) / 10))
        for (src, off), _res in [(c, None) for c in chunk]:
            st = "VHHH" if src == "hko" else src
            obs_list = by.get(st) or []
            nowloc = datetime.now(timezone.utc) + timedelta(hours=off)
            day_start_utc = (nowloc.replace(hour=0, minute=0, second=0, microsecond=0)
                             - timedelta(hours=off)).timestamp()
            vals = [tmp for tt, tmp in obs_list if tt >= day_start_utc]
            # calculate 30-60m trend (rate of change in C/hr) from timestamped observations
            sorted_obs = sorted([(tt, tmp) for tt, tmp in obs_list if isinstance(tt, (int, float)) and tmp is not None], key=lambda x: x[0])
            trend = None
            if len(sorted_obs) >= 2:
                t_last, temp_last = sorted_obs[-1]
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
    margin_base = 3.6 if is_f else 2.0     # 2.0C / 3.6F standard margin
    margin_strict = 5.0 if is_f else 2.8   # 2.8C / 5.0F strict margin for high-price NOs (>0.75)
    bd_min = 1.4 if is_f else 0.8          # 0.8C boundary margin against resolver-vs-METAR noise
    out = []

    def mk(rule, side, q, r):
        px = r["yes_ask"] if side == "YES" else 1 - r["yes_bid"]
        avail = (r["yes_ask_sz"] if side == "YES" else r["yes_bid_sz"]) * 0.9
        want = (SIZE_LOTTO if rule in ("R1_low_lotto", "R4_high_lotto") else SIZE_LOCKED) / px
        shares = max(0, int(min(want, avail)))
        edge = (q - px - fee(px)) if side == "YES" else (q - px - fee(px))
        return dict(rule=rule, side=side, q=q, edge=round(edge, 3), px=round(px, 4),
                    size_usd=round(shares * px, 2), shares=shares, **r)

    for r in book:
        in_bucket = r["lo"] <= obs_m < r["hi"]
        # state anchors: RUNNING extremes for the local day (current obs alone lies when
        # rain/shower drops temp after the peak, making achieved buckets look dead)
        runmax_m = (runmax * 9 / 5 + 32) if (runmax is not None and is_f) else runmax
        runmin_m = (runmin * 9 / 5 + 32) if (runmin is not None and is_f) else runmin
        min_anchor = runmin_m if runmin_m is not None else obs_m
        
        # Velocity filter: block low-side entries if temperature is rapidly falling (trend < -0.3 C/hr)
        trend_ok_low = (trend is None) or (trend >= -0.3)
        if is_low and (dawn - 2.5) <= local_hour <= dawn and not precip and trend_ok_low:
            # R1 lotto: running min inside bucket, boundary distance >= bd_min, ask dirt cheap -> floor q 0.15
            min_in_bucket = (r["lo"] <= min_anchor < r["hi"]) and in_bucket
            bd_low = min(min_anchor - r["lo"], r["hi"] - min_anchor) if min_in_bucket else 0
            if min_in_bucket and bd_low >= bd_min and r["yes_ask"] is not None and r["yes_ask"] <= ASK_MAX_LOTTO:
                q = 0.15
                if q - r["yes_ask"] - fee(r["yes_ask"]) > 0.10:
                    out.append(mk("R1_low_lotto", "YES", q, r))
            # R2 dead-below: progressive margin based on price
            if r["yes_bid"] is not None:
                no_ask = 1 - r["yes_bid"]
                req_margin = margin_strict if no_ask > 0.75 else margin_base
                if r["hi"] <= min_anchor - req_margin:
                    q_no = 0.98 if no_ask > 0.75 else 0.95
                    if q_no - no_ask - fee(no_ask) > 0.05:
                        out.append(mk("R2_low_dead_below", "NO", q_no, r))
                        
        # Velocity filter: block high-side entries if temperature is still surging (trend > +0.3 C/hr)
        trend_ok_high = (trend is None) or (trend <= 0.3)
        if (not is_low) and local_hour >= lastlight - 2.5 and local_hour <= lastlight and not precip and trend_ok_high:
            max_anchor = runmax_m if runmax_m is not None else obs_m
            max_in_bucket = (r["lo"] <= max_anchor < r["hi"]) and (r["lo"] <= obs_m or obs_m < r["hi"])
            bd_high = min(max_anchor - r["lo"], r["hi"] - max_anchor) if max_in_bucket else 0
            if max_in_bucket and bd_high >= bd_min and r["yes_ask"] is not None and r["yes_ask"] <= ASK_MAX_LOTTO:
                q4 = 0.15
                if q4 - r["yes_ask"] - fee(r["yes_ask"]) > 0.10:
                    out.append(mk("R4_high_lotto", "YES", q4, r))
            # R3 dead-above after peak: progressive margin based on price
            if r["yes_bid"] is not None:
                no_ask = 1 - r["yes_bid"]
                req_margin = margin_strict if no_ask > 0.75 else margin_base
                if r["lo"] >= max_anchor + req_margin:
                    q_no = 0.98 if no_ask > 0.75 else 0.95
                    if q_no - no_ask - fee(no_ask) > 0.05:
                        out.append(mk("R3_high_dead_above", "NO", q_no, r))
    return out

def official_outcome(det):
    """If the market itself has resolved (closed + outcomePrices), return bucket_hit (bool)
    from the official result; else None. Preferred over any station proxy."""
    try:
        evg = get(f"https://gamma-api.polymarket.com/events?slug={det['slug']}")
        if isinstance(evg, list): evg = evg[0] if evg else None
        if not evg or not evg.get("closed"): return None
        for m in evg.get("markets") or []:
            if (m.get("groupItemTitle") or "").strip() == det["bucket"]:
                op = m.get("outcomePrices")
                if op is None: return None
                prices = json.loads(op) if isinstance(op, str) else op
                outcomes = m.get("outcomes") or ["Yes", "No"]
                if isinstance(outcomes, str): outcomes = json.loads(outcomes)
                yi = outcomes.index("Yes") if "Yes" in outcomes else 0
                if len(prices) > yi and prices[yi] is not None:
                    return float(prices[yi]) > 0.5
    except Exception:
        return None
    return None

def settle_past(seen_pending):
    """Fetch IEM daily data for closed+detected events, resolve winner, log paper PnL."""
    now = datetime.now(timezone.utc)
    done = []
    for key, det in list(seen_pending.items()):
        try:
            end = datetime.fromisoformat(det["end"].replace("Z", "+00:00"))
        except Exception:
            continue
        if det["city"] not in MAP:
            if det["city"] == "Hong Kong":
                src, off, tz, dawn, lastlight = ("hko", 8, "Asia/Hong_Kong", 6.0, 18.8)
            else:
                continue
        else:
            src, off, tz, dawn, lastlight = MAP[det["city"]]
        # settle only after the event's LOCAL day has fully ended (endDate alone is too
        # early for US/EU high markets whose day continues past the admin endDate)
        tld = target_local_date(det["title"])
        if tld is not None:
            local_day_end_utc = datetime(tld[0], tld[1], tld[2], tzinfo=timezone.utc) \
                + timedelta(days=1) - timedelta(hours=off)
            settle_when = local_day_end_utc + timedelta(hours=2)
        else:
            settle_when = end + timedelta(hours=3)
        if now < settle_when: continue
        station = "VHHH" if src == "hko" else src
        official = official_outcome(det)
        if official is not None:
            bucket_hit = official
            ex = -999  # official market resolution; station value not needed
            px = det.get("px") or (det["yes_ask"] if det["side"] == "YES" else 1 - det["yes_bid"])
            shares = det.get("shares") or det["size"] / px
            pos_won = bucket_hit if det["side"] == "YES" else (not bucket_hit)
            pnl = (shares * (1 if pos_won else 0)) - shares * px - fee(px) * shares
            log(CLO, {"ts": now.isoformat(), "key": key, "city": det["city"], "station": "OFFICIAL",
                      "title": det["title"], "bucket": det["bucket"], "side": det["side"],
                      "bucket_hit": bucket_hit, "pos_won": pos_won,
                      "paper_size_usd": round(shares * px, 2), "shares": round(shares, 1),
                      "entry_px": round(px, 4), "resolver_extremum": ex,
                      "won": pos_won, "paper_pnl": round(pnl, 2), "note": "official_outcome"})
            say(f"[SETTLED-OFFICIAL] {det['city']} {det['bucket']} {det['side']} bucket_hit={bucket_hit} pos_won={pos_won} pnl={pnl:+.2f}")
            done.append(key)
            continue
        tld = target_local_date(det["title"])
        if tld is not None:
            y, m, d = tld
        else:
            loc = end + timedelta(hours=off)
            y, m, d = loc.year, loc.month, loc.day
        url = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={station}&data=tmpc"
               f"&year1={y}&month1={m}&day1={d}"
               f"&year2={y}&month2={m}&day2={d}"
               f"&tz={tz}&format=onlycomma&latlon=no&missing=M&trace=T&direct=no&report_type=3&report_type=4")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "supervisor"})
            vals = []
            for line in urllib.request.urlopen(req, timeout=40).read().decode().strip().split("\n")[1:]:
                p = line.split(",")
                if len(p) > 2 and p[2] not in ("M", ""): vals.append(float(p[2]))
            if not vals: continue
            extremum = min(vals) if det["title"].startswith("Lowest") else max(vals)
            ex = extremum * 9 / 5 + 32 if det["city"] in US_F else extremum
            bucket_hit = det["lo"] <= ex < det["hi"]
            pos_won = bucket_hit if det["side"] == "YES" else (not bucket_hit)
            px = det.get("px") or (det["yes_ask"] if det["side"] == "YES" else 1 - det["yes_bid"])
            shares = det.get("shares") or det["size"] / max(0.001, px)
            pnl = (shares * (1 if pos_won else 0)) - shares * px - fee(px) * shares
            log(CLO, {"ts": now.isoformat(), "key": key, "city": det["city"], "station": station,
                      "title": det["title"], "bucket": det["bucket"], "side": det["side"],
                      "bucket_hit": bucket_hit, "pos_won": pos_won,
                      "paper_size_usd": round(shares * px, 2), "shares": round(shares, 1),
                      "entry_px": round(px, 4),
                      "resolver_extremum": round(ex, 1), "won": pos_won, "paper_pnl": round(pnl, 2),
                      "note": "IEM proxy" if station == "VHHH" else ""})
            say(f"[SETTLED] {det['city']} {det['bucket']} {det['side']} bucket_hit={bucket_hit} pos_won={pos_won} pnl={pnl:+.2f}")
            done.append(key)
        except Exception as ex:
            say("settle err %s %s" % (key, ex))
    for k in done: seen_pending.pop(k)

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
        if not (0 < hrs < 40): continue
        local = now + timedelta(hours=off)
        local_hour = local.hour + local.minute / 60
        # CRITICAL: only act inside the event's own local calendar day
        tld = target_local_date(e["title"])
        if tld is None or (local.year, local.month, local.day) != tld:
            continue
        is_low = e["title"].startswith("Lowest")
        in_window = ((dawn - 2.5) <= local_hour <= dawn) if is_low else (lastlight - 2.5) <= local_hour <= lastlight
        if not in_window: continue
        obs = temps.get(src) if src != "hko" else temps.get("hko")
        if obs is None: continue
        in_window_events.append((e, obs))

    running = fetch_running([e for e, _ in in_window_events])

    # pass 2: books + detectors with running-extremum state
    for e, obs in in_window_events:
        city = e["city"]
        src, off, tz, dawn, lastlight = MAP[city]
        local = now + timedelta(hours=off)
        local_hour = local.hour + local.minute / 60
        raw = raws.get("VHHH" if src == "hko" else src, "")
        precip = bool(re.search(r"\b(RA|SN|SHRA|-RA|RA\s|TSRA|RASN|SNRA|SHSN)\b", raw))
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
            if key in seen: continue
            seen.add(key)
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
