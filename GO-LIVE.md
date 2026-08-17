# GO-LIVE — from paper to real money

Two processes do all the work:

| Process | Role |
|---|---|
| `run_supervisor.bat` -> `scripts/supervisor.py` | eyes + brain: watches stations/markets, writes detections, settles paper record |
| `python scripts/live_trader.py` | hands: reads detections, applies live gates, sends orders (or DRY_RUN logs them) |

## Safety architecture (already built in)

- trader starts in DRY_RUN with no key: it logs `DRY_RUN_WOULD_ORDER` lines, never orders.
- live gates: only R2/R3 dead-bucket NOs (or lotto sweeps if ALLOW_LOTTOS=true); price re-verified at execution (max +0.03 slip);
  recomputed edge > 0.04; size = min(CARD, 90% of displayed depth), >= 5 shares;
  max 3 open ($75 max capital lock on $250 base), max 1 per city, max 8 trades/day, max $50/day cost cap; orders are FAK
  (fill-and-kill — never rests as a stale maker quote).
- kill switch: create a file named `PAUSE` in `data\` -> trader stops new orders instantly
  (`echo. > data\PAUSE`). Delete it to resume.
- everything auditable: `data/live_orders.jsonl` (every decision + exchange response),
  `data/live_state.json` (positions/caps), `data/run.log`.

## Your steps to go live (30 minutes)

1. **Deposit**: Polymarket -> Deposit -> USDC (Polygon network). Recommended initial bankroll: **$250**.
2. **Create credentials**: Polymarket UI -> Settings -> Export Private Key. Put it in `.env`
   (copy `.env.example` to `.env`, fill PRIVATE_KEY, set FUNDER to your deposit address if
   the account was created via email login).
3. **Rehearse**: run `python scripts/live_trader.py` as-is (DRY_RUN). During the next alert
   window you should see `DRY_RUN_WOULD_ORDER` lines with live prices/sizes. Compare them
   to the book in the browser — this validates the price path.
4. **Flip live**: in `.env` set `LIVE_ENABLED=true` and `DRY_RUN=false`. Restart the trader.
   First sessions: watch `tail -f data/run.log` while it trades.
5. **Daily review**: `data/closures.jsonl` (paper record) + `data/live_orders.jsonl` (live fills).

## Scaling rule

Add capital only after: >= 20 settled live positions AND win rate >= 80% AND live fill
prices within 0.02 of alert prices. Scale the `CARD` in live_trader.py and `SIZE_*` in
supervisor.py together:
- **$100 Bankroll:** `CARD=12`, `MAX_COST_DAY=20`, `SIZE_LOCKED=12`, `SIZE_LOTTO=2`
- **$250 Bankroll (CURRENT):** `CARD=25`, `MAX_COST_DAY=50`, `SIZE_LOCKED=25`, `SIZE_LOTTO=3`
- **$500 Bankroll:** `CARD=50`, `MAX_COST_DAY=100`, `SIZE_LOCKED=50`, `SIZE_LOTTO=5`
- **$1,000 Bankroll:** `CARD=100`, `MAX_COST_DAY=200`, `SIZE_LOCKED=100`, `SIZE_LOTTO=10`

## Known maintenance items

- Timezone offsets in supervisor.py MAP are fixed values, correct for Aug 2026. They go
  stale when DST changes (NZ Sep 20, EU Oct 25, US Nov 1, Israel Oct 4). Update the offsets
  column on those dates or the windows shift by an hour.
- HK settlements use the airport (VHHH) as proxy for the HKO downtown station; spot-check
  HK closures against the HKO daily extract before trusting HK live size.
- R1 lotto alerts are manual-only by design: take them in the browser, log in trades.csv.
