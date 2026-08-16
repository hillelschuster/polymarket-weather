"""Resolver-state sniper: poll exact resolver source + Polymarket books, print fee-adjusted edge.

Usage:
  python scripts/sniper.py "Lowest temperature in Hong Kong on August 16" hko
  python scripts/sniper.py "Highest temperature in NYC on August 16" metar KLGA

Sources:
  hko  = HKO official station (rhrread current + mintempFrom00To09) — resolves to 0.1C
  metar = aviationweather.gov METAR (whole C unless T-group present; whole F for US)
Edge convention (per repo edge-economics):
  fee(p) = 0.05 * p * (1-p)
  net_edge_yes = q - ask_yes - fee(ask_yes)
  net_edge_no  = (1-q) - ask_no - fee(ask_no)   [ask_no = 1 - bid_yes]
Only you supply q. The script prints both executable expressions per bucket.
"""
import json, re, sys, time, urllib.request
from datetime import datetime, timezone

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def fee(p): return 0.05 * p * (1 - p)

def resolver_state(src, station=None):
    if src == "hko":
        r = get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en")
        cur = next((s["value"] for s in r.get("temperature", {}).get("data", [])
                    if s.get("place") == "Hong Kong Observatory"), None)
        return {"current": cur, "min_so_far_0009": r.get("mintempFrom00To09"),
                "updateTime": r.get("updateTime"), "icon": r.get("icon"),
                "tc": r.get("tcmessage")}
    if src == "metar":
        m = get(f"https://aviationweather.gov/api/data/metar?ids={station}&format=json")
        r = m[0] if m else {}
        raw = r.get("rawOb", "")
        tg = re.search(r"\sT(\d{3})(\d)", raw)  # T-group: tenths C
        t_tenths = None
        if tg:
            sign = -1 if tg.group(1)[0] == "1" else 1
            t_tenths = sign * (int(tg.group(1)) / 10.0)
        return {"current": r.get("temp"), "t_group_tenths_C": t_tenths, "raw": raw,
                "obs_utc": r.get("obsTime")}
    raise SystemExit(f"unknown source {src}")

def find_event(title_prefix):
    events, offset = [], 0
    while True:
        b = get(f"https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset={offset}")
        if not b: break
        events += b; offset += 100
        if len(b) < 100: break
    for e in events:
        if (e.get("title") or "").startswith(title_prefix):
            return e
    raise SystemExit(f"event not found: {title_prefix}")

def books(event):
    rows = []
    for m in event.get("markets") or []:
        gt = m.get("groupItemTitle") or ""
        mm = re.match(r"(\d+)", gt.strip())
        if not mm: continue
        toks = json.loads(m.get("clobTokenIds")) if isinstance(m.get("clobTokenIds"), str) else m.get("clobTokenIds")
        yes_tok = toks[0]
        bk = get(f"https://clob.polymarket.com/book?token_id={yes_tok}")
        bids = sorted(bk.get("bids") or [], key=lambda x: float(x["price"]))
        asks = sorted(bk.get("asks") or [], key=lambda x: float(x["price"]))
        rows.append({"bucket": gt.strip(), "val": int(mm.group(1)),
                     "yes_bid": float(bids[-1]["price"]) if bids else None,
                     "yes_bid_sz": float(bids[-1]["size"]) if bids else 0,
                     "yes_ask": float(asks[0]["price"]) if asks else None,
                     "yes_ask_sz": float(asks[0]["size"]) if asks else 0})
    rows.sort(key=lambda r: r["val"])
    return rows

if __name__ == "__main__":
    title, src = sys.argv[1], sys.argv[2]
    station = sys.argv[3] if len(sys.argv) > 3 else None
    st = resolver_state(src, station)
    ev = find_event(title)
    print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"), "|", ev.get("title"))
    print("RESOLVER STATE:", json.dumps(st))
    print(f"{'bucket':<16}{'yes_bid':>8}{'x':>8}{'yes_ask':>8}{'x':>8}{'no_ask':>8}")
    for r in books(ev):
        no_ask = 1 - r["yes_bid"] if r["yes_bid"] is not None else None
        print(f"{r['bucket']:<16}"
              f"{('%0.3f' % r['yes_bid']) if r['yes_bid'] is not None else '-':>8}"
              f"{r['yes_bid_sz']:>8.0f}"
              f"{('%0.3f' % r['yes_ask']) if r['yes_ask'] is not None else '-':>8}"
              f"{r['yes_ask_sz']:>8.0f}"
              f"{('%0.3f' % no_ask) if no_ask is not None else '-':>8}")
    print("\nfee(p)=0.05*p*(1-p). Compute q per bucket from state above; then")
    print("  edge_yes = q - yes_ask - fee(yes_ask)")
    print("  edge_no  = (1-q) - no_ask - fee(no_ask)")
