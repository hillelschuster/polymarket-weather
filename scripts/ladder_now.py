"""Full ladder dump for Aug-16 weather events: bucket, bid, ask, spread."""
import json, urllib.request, sys
from datetime import datetime, timezone

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))

target = sys.argv[1] if len(sys.argv)>1 else "August 16"
events, offset = [], 0
while True:
    batch = get(f"https://gamma-api.polymarket.com/events?tag_slug=weather&closed=false&limit=100&offset={offset}")
    if not batch: break
    events += batch; offset += 100
    if len(batch) < 100: break

sel = [e for e in events if target in (e.get("title") or "")]
print(f"events matching '{target}':", len(sel))
for e in sorted(sel, key=lambda x: -(x.get("volume24hr") or 0)):
    mkts = e.get("markets") or []
    print("\n===", e.get("title"), f"| vol24h={e.get('volume24hr') or 0:.0f}")
    desc = (mkts[0].get("description") or "")[:300] if mkts else ""
    print("  rules:", desc.replace("\n"," ")[:250])
    for m in sorted(mkts, key=lambda m: m.get("groupItemTitle") or ""):
        print(f"   {str(m.get('groupItemTitle'))[:28]:<30} bid={m.get('bestBid')} ask={m.get('bestAsk')}")
