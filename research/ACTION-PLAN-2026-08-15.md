# Action plan — fastest path to net PnL with ~$300 bankroll

Snapshot: 2026-08-15 19:30 UTC. Written after live market verification (scripts below).

## Verdict

Start with **resolver-state taker sniping** (repo Priority 2/3), not maker quoting and not
T+1 model-vs-market bets. Reasons:

1. it is observation-driven, so edge is verifiable in real time against the exact resolver source;
2. the weather fee curve `fee(p)=0.05*p*(1-p)` collapses to ~0 near certainty, so
   near-locked states are the cheapest expressions on the platform;
3. it repeats every night (lows) and every afternoon (highs) across ~40 city markets;
4. needs zero infrastructure — browser + the three scripts in `scripts/`.

## Live verified example — 2026-08-15/16 HK low window

- 03:00 HKT: HKO official station (exact resolver) reads 29C, airport flat 29-30C since
  midnight, no rain, no TC warning. HKO own forecast for Aug 16: min 28C.
- Market at that moment: 27C bucket ~45-50%, 28C ~45-50%, 29C offered at 0.001-0.002.
- Book: YES 29 available 0.001 x10, 0.002 x5019. NO 27 ~0.62.
- Interpretation: market distribution sits a full degree below the live resolver state;
  29-bucket is a free option; NO-27 at <=0.65 carries large edge unless an early-morning
  thunderstorm crashes the temperature (the stated tail risk: "isolated thunderstorms at
  first" per HKO).

## Daily snipe windows (UTC)

| Window (UTC)      | Markets                              | Resolver source |
|-------------------|--------------------------------------|-----------------|
| 19:00-21:30       | HK low (HKO), Seoul/Tokyo/Shanghai lows | HKO rhrread; METAR RKSI/RJTT/ZSPD |
| 05:00-14:00       | European highs (London EGLC, Paris LFPB, Madrid LEMD, Munich EDDM, Milan LIMC, Amsterdam EHAM) | METAR + Wunderground Daily Observations |
| 14:00-21:00       | US highs/lows in F (NYC KLGA, Miami KMIA, Chicago, Denver, Dallas, Austin, Houston...) | METAR + T-group precision; Wunderground F convention |

Lows are the easiest first trades: min is locked by sunrise; after ~05:00 local the
remaining-exceedance math is trivial. Highs: certainty collapses 1-3h before sunset local.

## Scripts (in `scripts/`)

- `sniper.py "<event title prefix>" hko|metar <ICAO>` — resolver state + both sides of every bucket book.
- `ladder_now.py "August 16"` — full ladder dump for a date.
- `fair_value_scan.py` — 6-model daily max/min vs market distribution, flags fee-adjusted divergence (use only when model spread < ~2C).
- `live_scan.py` — all active weather events sorted by end time.

## Sizing rules

- Confidence-tiered: >=90% states -> up to 15% of bankroll; 70-85% -> <=8%; lotto clips
  (0.001-0.005 asks) capped by book size, always <=2% of bankroll.
- Never market-buy into a spread wider than ~5 cents without recomputing both expressions.
- Both expressions computed before every trade: YES at ask vs NO at (1 - yes_bid); take the cheaper.
- Skip states with a physical crash mechanism you cannot observe (thunderstorm risk without radar check, frontal timing).

## Do NOT spend time on yet

- Maker quoting (needs markout measurement first — repo Priority 1 recorder).
- T+1 forecast positions where model spread > ~2.5C (Seoul high tonight: 2.9C spread — untradable).
- GISTEMP/climate vintage replication — high capacity but slow; revisit after 2 weeks of daily PnL.
- Wallet copy-trading.

## Scaling path

1. Week 1: manual snipes, log every trade (state snapshot, q, price, size, outcome) to a JSONL.
2. Week 2: automate the sniper poll loop (2-min cadence) with desktop alerts; add remaining cities.
3. Week 3+: if realized net edge > 5%/trade after 20+ trades, scale bankroll; build the
   synchronized L2 recorder (repo Priority 1) to unlock maker and AIFS latency regimes.
