"""Quick live weather market scan: full ladders, ladder sums, US cities focus."""
import json, urllib.request, sys
from datetime import datetime, timezone

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))

# paginate active weather events
events, offset = [], 0
while True:
    batch = get(f"https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset={offset}&order=endDate&ascending=true")
    if not batch: break
    events += batch; offset += 100
    if len(batch) < 100: break

print(f"active weather events: {len(events)}", file=sys.stderr)
now = datetime.now(timezone.utc)
rows = []
for e in events:
    end = e.get("endDate")
    try:
        enddt = datetime.fromisoformat(end.replace("Z","+00:00"))
    except Exception:
        enddt = None
    mkts = e.get("markets") or []
    # full ladder ask sum (mutually exclusive outcomes)
    asks, bids = [], []
    for m in mkts:
        a, b = m.get("bestAsk"), m.get("bestBid")
        if a is not None: asks.append((m.get("question"), a, b, m.get("outcomes")))
    if not asks: continue
    total_ask = sum(a for _,a,_,_ in asks)
    rows.append((enddt or now, e.get("title"), len(asks), total_ask, asks))

rows.sort(key=lambda r: r[0])
print(f"{'endsUTC':<17}{'event':<52}{'n':>3}{'sumAsk':>8}  top outcomes (q | bid/ask)")
for enddt, title, n, s, asks in rows:
    hrs = (enddt-now).total_seconds()/3600
    if hrs < -24: continue
    hs = f"{enddt.strftime('%m-%d %H:%M')}"
    # compact: strip common prefix
    print(f"{hs:<17}{title[:50]:<52}{n:>3}{s:>8.3f}  ends in {hrs:5.1f}h")
