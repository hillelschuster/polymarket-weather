# Weather edge research

Snapshot: **2026-08-11**

## Bottom line

The starting axiom is supported by public evidence: meaningful realized profit exists in Polymarket's weather category. The current all-time weather leaderboard shows multiple six-figure winners, led by `gopfan2` at roughly $349k, `aenews2` at roughly $285k, and `ColdMath` at roughly $136k. Several explicitly weather/bot-themed accounts have five-figure weather profit. This proves opportunity exists; it does **not** prove any specific public strategy still has positive forward EV.

The strongest research conclusion so far is that the edge is not simply “use a better forecast.” There are at least **five separate PnL engines**:

1. **Forecast calibration** — turn ensemble paths into a calibrated distribution of the exact settlement-station daily maximum.
2. **Observation/nowcast edge** — as the day unfolds, condition the remaining maximum on the observed station maximum and current atmosphere.
3. **Information timing** — react to new model runs / observations before prices fully reprice.
4. **Cross-bucket structure** — exploit mutually exclusive ladder probabilities and negative-risk relationships when books are inconsistent.
5. **Execution alpha** — maker pricing, spreads, rebates, depth, and queue timing can materially change net EV.

A sixth source, **wallet alpha**, can improve all five: public weather-specialist wallets can reveal where and when informed traders act.

## Why public bots leave room

Most public implementations are surprisingly crude relative to the problem:

- raw ensemble-member counting;
- one deterministic forecast mapped to one bucket;
- normal distributions with hand-set sigma;
- naive pooling of models;
- generic city coordinates instead of settlement stations;
- edge computed against midpoint rather than executable net price;
- little or no modeling of the full mutually-exclusive ladder.

A representative open-source bot (`suislanchez/polymarket-kalshi-weather-bot`) calculates probability as the fraction of ensemble members crossing a threshold, clips it to 5–95%, then compares it with market price and applies Kelly sizing. That is a useful baseline, but the clipping and raw-member interpretation throw away tail information and calibration structure.

## The key modeling object

For a daily-high event, the object we need is not “tomorrow's temperature.” It is:

> **P(the exact resolver-reported daily maximum falls in bucket i | every forecast run and observation available at trade time)**

For each ensemble member/path, compute the **daily maximum at the settlement station**, not the maximum of a mean forecast. Then calibrate the distribution using station-, lead-time-, season-, and regime-specific historical errors.

Once observations begin, the final maximum is constrained by the observed maximum so far. This makes same-day markets mathematically different from T+1/T+2 markets and likely explains why several public projects converge on strong same-day performance.

## Market structure matters

Daily temperature events contain many mutually exclusive buckets. Polymarket documents negative-risk conversion for multi-outcome events: a NO share in one outcome can be converted into YES shares for every other outcome. Therefore the ladder must be modeled as one probability surface, not independent binaries.

At fair value:

`sum_i q_i = 1`

and for each outcome `i`:

`P(NO_i) = 1 - q_i = sum_{j != i} q_j`

This creates direct relative-value checks between YES/NO books and the rest of the ladder, independently of whether our weather forecast is better.

## Fees change the signal

Current Polymarket documentation lists Weather with a taker fee rate of `0.05` on fee-enabled markets, using:

`fee = shares * feeRate * p * (1-p)`

Makers are not charged platform trading fees, and Weather currently receives a 25% maker-rebate allocation from collected fees. Fee applicability is per market (`feesEnabled` / fee schedule), so it must be queried rather than assumed.

This means the real signal is not `model_probability - midpoint`. It is expected PnL at an executable price, including fees, fill probability and exit/settlement path.

## Resolution is part of the alpha

Examples from 2026 Polymarket rules:

- New York City: LaGuardia / `KLGA`, whole °F, Wunderground history.
- London: London City Airport / `EGLC`, whole °C, Wunderground history.
- Milan: Malpensa / `LIMC`, whole °C, Wunderground history.
- Paris: Paris-Le Bourget / `LFPB`, whole °C, Wunderground history.

Rules also define when revisions stop counting. A model aimed at “New York City” or “Paris” generically is solving the wrong target.

## Research discipline

The repo will distinguish:

- **Verified:** official API/rules, public leaderboard values, public wallet activity, inspected source code.
- **Self-reported:** performance or strategy claims made by bot authors.
- **Inference:** strategy patterns inferred from public activity.
- **Hypothesis:** an edge we still need to measure point-in-time.

## Primary references

- Polymarket leaderboard: https://polymarket.com/leaderboard/weather/all/profit
- Polymarket fees: https://docs.polymarket.com/trading/fees
- Maker rebates: https://docs.polymarket.com/market-makers/maker-rebates
- Negative risk: https://docs.polymarket.com/advanced/neg-risk
- Polymarket API docs index: https://docs.polymarket.com/llms.txt
- ECMWF ensemble guide: https://confluence.ecmwf.int/spaces/FUG/pages/673550376/Section+2A.1.2.1+Medium+Range+Ensemble+forecasts
- NOAA NBM weather elements: https://vlab.noaa.gov/web/mdl/nbm-weather-elements
- AviationWeather METAR API: https://aviationweather.gov/data/api/
- Gneiting et al. EMOS paper: https://doi.org/10.1175/MWR2904.1

See the other files in this directory for the detailed thesis.
