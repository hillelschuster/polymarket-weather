"""Compare multi-model daily-max forecasts against Polymarket Aug 16 high/low ladders.
Flags buckets where model-implied probability diverges from executable price after taker fees."""
import json, urllib.request, re, sys
from datetime import datetime, timezone

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=40))

# station coords for the highest-volume Aug-16 events (from resolver rules)
STATIONS = {
 "Wellington":      ("NZWN", -41.327, 174.805),
 "Seoul (Incheon)": ("RKSI", 37.460, 126.441),
 "Munich":          ("EDDM", 48.354, 11.786),
 "Beijing":         ("ZBAA", 40.080, 116.585),
 "Madrid":          ("LEMD", 40.472, -3.561),
 "Shanghai":        ("ZSPD", 31.144, 121.808),
 "Karachi":         ("OPKC", 24.907, 67.138),
 "Busan":           ("RKPK", 35.102, 128.937),
 "Tokyo":           ("RJTT", 35.553, 139.781),
 "Hong Kong":       ("HKO",  22.302, 114.174),
 "London":          ("EGLC", 51.505, 0.055),
 "Paris":           ("LFPB", 48.969, 2.441),
 "Kuala Lumpur":    ("WMKK", 2.746, 101.710),
 "Taipei":          ("RCSS", 25.069, 121.552),
 "Chongqing":       ("ZUCK", 29.719, 106.642),
 "Wuhan":           ("ZHHH", 30.784, 114.208),
 "Chengdu":         ("ZUUU", 30.579, 103.947),
 "Shenzhen":        ("ZGSZ", 22.639, 113.811),
 "Guangzhou":       ("ZGGG", 23.392, 113.299),
 "Amsterdam":       ("EHAM", 52.309, 4.764),
 "Warsaw":          ("EPWA", 52.166, 20.967),
 "Helsinki":        ("EFHK", 60.317, 24.963),
 "Milan":           ("LIMC", 45.630, 8.723),
 "Istanbul":        ("LTFM", 41.275, 28.752),
 "Tel Aviv":        ("LLBG", 32.011, 34.887),
 "Moscow":          ("UUWW", 55.592, 37.262),
 "Singapore":       ("WSSS", 1.364, 103.991),
 "Manila":          ("RPLL", 14.584, 121.002),
 "Jeddah":          ("OEJN", 21.680, 39.157),
 "Cape Town":       ("FACT", -33.965, 18.602),
 "NYC":             ("KLGA", 40.777, -73.873),
 "Miami":           ("KMIA", 25.793, -80.316),
 "Chicago":         ("KMDW", 41.786, -87.752),
 "Denver":          ("KBFL", None, None),
 "Ankara":          ("LTAC", 40.128, 32.995),
 "Toronto":         ("CYYZ", 43.677, -79.630),
 "Mexico City":     ("MMMX", 19.436, -99.072),
 "Los Angeles":     ("KLAX", 33.938, -118.389),
 "San Francisco":   ("KSFO", 37.619, -122.375),
 "Seattle":         ("KBFI", 47.530, -122.302),
 "Atlanta":         ("KATL", 33.640, -84.427),
 "Austin":          ("KAUS", 30.197, -97.670),
 "Dallas":          ("KDAL", 32.847, -96.852),
 "Houston":         ("KHOU", 29.645, -95.279),
 "Denver2":         ("KDEN", 39.862, -104.667),
}
MODELS = "ecmwf_ifs025,gfs_seamless,icon_seamless,gem_seamless,ukmo_seamless,jma_seamless"
TARGET = "August 16"

# fetch events
events, offset = [], 0
while True:
    b = get(f"https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset={offset}")
    if not b: break
    events += b; offset += 100
    if len(b) < 100: break
aug16 = [e for e in events if TARGET in (e.get("title") or "")]

def bucket_bounds(title):
    m = re.match(r"^(\d+)", title.strip())
    hi = re.search(r"or higher", title)
    lo = re.search(r"or below", title)
    return title.strip()

results = []
for e in aug16:
    t = e.get("title") or ""
    city = t.replace(f"Highest temperature in ", "").replace(f"Lowest temperature in ", "").replace(f" on {TARGET.replace('August 16','August 16')}?", "")
    is_low = t.startswith("Lowest")
    key = None
    for k in STATIONS:
        if city.startswith(k): key = k; break
    if not key or STATIONS[key][1] is None: continue
    icao, lat, lon = STATIONS[key]
    try:
        om = get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&models={MODELS}&forecast_days=3&temperature_unit=celsius")
    except Exception as ex:
        print("OM err", key, ex); continue
    daily = om.get("daily", {})
    dates = daily.get("time", [])
    idx = None
    for i, d in enumerate(dates):
        if d == "2026-08-16": idx = i
    if idx is None: continue
    model_vals = []
    for mkey in daily:
        if mkey.startswith("temperature_2m_max_") and not mkey.endswith(("_0","_1","_2","_3","_4","_5")):
            pass
    # simpler: use hourly per model to compute local-day max/min
    hourly = om.get("hourly", {})
    times = hourly.get("time", [])
    model_cols = [c for c in hourly if c.startswith("temperature_2m_")]
    dayvals = {}
    for c in model_cols:
        model = c.replace("temperature_2m_", "")
        vals = [v for tt, v in zip(times, hourly[c]) if tt.startswith("2026-08-16") and v is not None]
        if vals: dayvals[model] = (max(vals), min(vals))
    if not dayvals: continue
    maxes = sorted(v[0] for v in dayvals.values())
    mins = sorted(v[1] for v in dayvals.values())
    # market ladder: bid/ask per bucket
    mkts = e.get("markets") or []
    ladder = []
    for m in mkts:
        gt = m.get("groupItemTitle") or ""
        bid, ask = m.get("bestBid"), m.get("bestAsk")
        mm = re.match(r"(\d+)°C", gt.strip())
        if not mm: continue
        val = int(mm.group(1))
        if "or below" in gt: bounds = (float("-inf"), val + 0.5)
        elif "or higher" in gt: bounds = (val - 0.5, float("inf"))
        else: bounds = (val - 0.5, val + 0.5)
        ladder.append((val, gt, bid, ask, bounds))
    ladder.sort()
    # model distribution: simple kernel over model maxes with ~0.8C std
    import math
    obs = mins if is_low else maxes
    def q(bounds):
        lo, hi = bounds
        # P(obs in [lo,hi)) via normal mixture
        p = 0.0
        for v in obs:
            mu, sd = v, 0.8
            cdf = lambda x: 0.5*(1+math.erf((x-mu)/(sd*math.sqrt(2)))) if x != float("inf") else 1.0
            lo2 = -1e9 if lo == float("-inf") else lo
            hi2 = 1e9 if hi == float("inf") else hi
            p += (cdf(hi2) - cdf(lo2))
        return p/len(obs)
    def fee(p): return 0.05*p*(1-p)
    flags = []
    for val, gt, bid, ask, bounds in ladder:
        if is_low:
            # NO side: P(low <= val-0.5) = 1 - q(bounds)
            pass
        qq = q(bounds)
        if ask is not None and qq - (ask + fee(ask)) > 0.04:
            flags.append(("BUY YES", gt, round(qq,3), ask, round(qq - ask - fee(ask),3)))
        if bid is not None:
            no_ask = 1 - bid
            p_no = 1 - qq
            if p_no - (no_ask + fee(no_ask)) > 0.04:
                flags.append(("BUY NO ", gt, round(p_no,3), round(no_ask,3), round(p_no - no_ask - fee(no_ask),3)))
    spread_consensus = (maxes[-1] - maxes[0]) if maxes else 0
    results.append((e.get("volume24hr") or 0, t, icao, [round(v,1) for v in obs], spread_consensus, flags))

results.sort(reverse=True)
for vol, t, icao, obs, spread, flags in results:
    kind = "LOW " if t.startswith("Lowest") else "HIGH"
    print(f"\n{kind} {t} | {icao} | vol24h={vol:.0f}")
    print(f"   model {'mins' if kind=='LOW ' else 'maxes'} Aug16: {obs} (spread {spread:.1f}C)")
    for f in flags:
        print(f"   *** {f[0]} {f[1]:<18} q={f[2]:<6} px={f[3]:<6} netEdge={f[4]}")
