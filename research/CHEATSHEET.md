# Cheat card — print this, trade next to it

Verified 2026-08-15: fee = 0.05 x p x (1-p) per share, TAKER ONLY (makers pay 0, earn 25%
rebate). Tick 0.001. Min order 5 shares. NegRisk ladders. Sources: on-chain market
metadata + docs.polymarket.com/trading/fees.

## The three commands

    python scripts/watchlist.py                          # what's live + resolver temp now
    python scripts/sniper.py "<event title prefix>" hko   # HK markets (HKO official)
    python scripts/sniper.py "<event title prefix>" metar RKSI   # any METAR city

## When to strike (decision windows)

- LOW markets: from ~03:00 local until sunrise. Enter mid-window, not at the end (edge
  decays as the market converges — watched HK 27-bucket go 0.45 -> 0.20 in 90 min).
- HIGH markets: last 3-4h of local afternoon, when running max is near/attained.
- The strike condition: resolver obs pins bucket B (e.g. station reads 29, flat all
  night, no rain), book still prices B far from 1.00, and nothing observable (radar,
  warnings, wind shift) can crash the state.

## Every trade: compute BOTH expressions, take the cheaper

    edge_yes = q - yes_ask - 0.05*yes_ask*(1-yes_ask)
    edge_no  = (1-q) - (1-yes_bid) - 0.05*(1-yes_bid)*yes_bid

Worked example (HK low tonight, station 29C flat, no rain):
- q(27)<=0.20 -> NO-27 at 0.62: edge = 0.80-0.62-0.0118 = +0.168  -> TAKE
- q(29)>=0.30 -> YES-29 at 0.002: edge = 0.30-0.002-0.0001 = +0.298 -> TAKE (lotto)
- q(28)=0.45 -> NO-28 at 0.58: edge = 0.55-0.58 < 0 -> SKIP (fairly priced exists)

## Sizing ($100 bankroll — 2026-08-15 revision)

- >=90% confident locked state: up to $12 (12%)
- 75-90%: up to $8 (8%)
- lotto asks (<=0.02): up to $2 total per market
- max 3 open positions; max 1 per city/day
- after any -12% day: stop for the day

## The supervisor (detached, non-stop, paper mode)

    ./run_supervisor.bat                      # Windows detached start (min window)
    tail -f data/run.log                      # watch heartbeats + [ALERT]/[SETTLED] lines
    data/detections.jsonl                     # every alert with q, price, edge, size
    data/closures.jsonl                       # settled markets: resolver value, won, paper PnL

It alerts only on conservative deterministic locks (R1 low-lotto, R2 low-dead-below,
R3 high-dead-above), one alert per bucket/side/market, settles closed markets against
IEM station data, and sends NO orders. Manual you execute from alerts until the
20-trade paper record justifies wiring execution keys.

## Kill-switches (skip the trade)

- book spread wider than ~5c with no explanation (staleness, not opportunity)
- thunderstorm risk on a LOW snipe and you have not checked radar
  (HK: hko.gov.hk radar; US: radar.weather.gov; EU: national radars / windy)
- you cannot name the exact resolver station from the rules text
- T+1 (tomorrow) high with model spread > 2.5C — that is a forecast bet, not a snipe
- anything you would not re-enter at the same price if it went against you first

## Log every trade in trades.csv (this is the two-week evidence file)

timestamp_utc,event,bucket,side,price,shares,cost,q_estimate,fee,resolver_outcome,pnl,note
