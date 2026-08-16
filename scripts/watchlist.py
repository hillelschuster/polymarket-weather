"""One-command watchlist: every active temperature event ending soon, with live resolver temp.

Run before each session:
  python scripts/watchlist.py

Shows: event | ends in | local hour | resolver current temp | nearest buckets' top of book.
You strike when: decision window is closing (lows: pre-dawn; highs: late local afternoon),
the resolver temp pins a bucket, and that bucket's price is still far from 1.0.
"""
import json, re, urllib.request
from datetime import datetime, timezone, timedelta

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))

# city prefix -> (ICAO | "hko", utc offset hours)  — offsets Aug (DST-correct enough)
MAP = {
    "Hong Kong": ("hko", 8), "Seoul": ("RKSI", 9), "Busan": ("RKPK", 9), "Tokyo": ("RJTT", 9),
    "Shanghai": ("ZSPD", 8), "Beijing": ("ZBAA", 8), "Taipei": ("RCSS", 8), "Chongqing": ("ZUCK", 8),
    "Wuhan": ("ZHHH", 8), "Chengdu": ("ZUUU", 8), "Shenzhen": ("ZGSZ", 8), "Guangzhou": ("ZGGG", 8),
    "Singapore": ("WSSS", 8), "Kuala Lumpur": ("WMKK", 8), "Manila": ("RPLL", 8),
    "Karachi": ("OPKC", 5), "Jeddah": ("OEJN", 3), "Tel Aviv": ("LLBG", 3), "Istanbul": ("LTFM", 3),
    "Ankara": ("LTAC", 3), "Moscow": ("UUWW", 3), "Cape Town": ("FACT", 2),
    "Wellington": ("NZWN", 12),
    "London": ("EGLC", 1), "Paris": ("LFPB", 2), "Amsterdam": ("EHAM", 2), "Warsaw": ("EPWA", 2),
    "Helsinki": ("EFHK", 3), "Madrid": ("LEMD", 2), "Milan": ("LIMC", 2), "Munich": ("EDDM", 2),
    "NYC": ("KLGA", -4), "Miami": ("KMIA", -4), "Atlanta": ("KATL", -4), "Boston": ("KBOS", -4),
    "Chicago": ("KMDW", -5), "Dallas": ("KDAL", -5), "Austin": ("KAUS", -5), "Houston": ("KHOU", -5),
    "Denver": ("KDEN", -6), "Phoenix": ("KPHX", -7), "Los Angeles": ("KLAX", -7),
    "San Francisco": ("KSFO", -7), "Seattle": ("KSEA", -7), "Toronto": ("CYYZ", -4),
    "Mexico City": ("MMMX", -6), "Sao Paulo": ("SBSP", -3), "Buenos Aires": ("SABE", -3),
}

# US cities resolve in degrees Fahrenheit; everything else in Celsius
US_F = {"NYC", "Miami", "Chicago", "Dallas", "Austin", "Houston", "Denver", "Phoenix",
        "Los Angeles", "San Francisco", "Seattle", "Atlanta", "Boston"}

def city_of(title):
    for k in MAP:
        if k in title:
            return k
    return None

events, offset = [], 0
while True:
    b = get("https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset=%d" % offset)
    if not b: break
    events += b; offset += 100
    if len(b) < 100: break

# temperature events only, ending within 40h
now = datetime.now(timezone.utc)
rows = []
for e in events:
    t = e.get("title") or ""
    if not t.startswith(("Highest temperature", "Lowest temperature")):
        continue
    try:
        end = datetime.fromisoformat((e.get("endDate") or "").replace("Z", "+00:00"))
    except Exception:
        continue
    hrs = (end - now).total_seconds() / 3600
    if not (-2 < hrs < 40):
        continue
    c = city_of(t)
    if not c:
        continue
    rows.append((hrs, e, c))

# current temps: batch METAR (chunked, retried) + HKO
need = {MAP[c][0] for _, _, c in rows if MAP[c][0] != "hko"}
temps = {}
need_list = sorted(need)
for i in range(0, len(need_list), 12):
    chunk = need_list[i:i+12]
    for attempt in range(3):
        try:
            ms = get("https://aviationweather.gov/api/data/metar?ids=%s&format=json" % ",".join(chunk))
            for m in ms:
                temps[m["icaoId"]] = m.get("temp")
            break
        except Exception:
            if attempt == 2:
                print("metar chunk err:", chunk)
try:
    r = get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en")
    temps["hko"] = next((s["value"] for s in r.get("temperature", {}).get("data", [])
                         if s.get("place") == "Hong Kong Observatory"), None)
except Exception:
    pass

print(now.strftime("%Y-%m-%d %H:%M UTC"))
print(f"{'event':<58}{'ends':>6} {'loc':>6} {'obs':>4}  nearest buckets (bid/ask x size)")
rows.sort(key=lambda r: r[0])
for hrs, e, c in rows:
    icao, off = MAP[c]
    local = now + timedelta(hours=off)
    cur = temps.get(icao)
    cur_disp = cur
    mkts = e.get("markets") or []
    lad = []
    for m in mkts:
        gt = m.get("groupItemTitle") or ""
        mm = re.match(r"(\d+)", gt.strip())
        if mm:
            lad.append((int(mm.group(1)), gt, m.get("bestBid"), m.get("bestAsk")))
    lad.sort()
    near = lad
    if cur is not None:
        match_val = cur
        if c in US_F:
            match_val = cur * 9 / 5 + 32
            cur_disp = f"{match_val:.0f}F"
        near = [x for x in lad if abs(x[0] - match_val) <= (3 if c in US_F else 2)]
    s = " ".join(f"{g}[{b}/{a}]" for _, g, b, a in near[:4])
    print(f"{e['title'][:56]:<58}{hrs:>5.1f}h {local.strftime('%H:%M'):>6} {str(cur_disp):>6}  {s}")
