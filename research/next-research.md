# Next research: experiments that decide what gets built

Snapshot: **2026-08-11**

No production bot should be built until the first few questions below are answered with point-in-time data. This is not ceremony; these experiments determine which math is worth implementing.

## Priority 0 — build the truth map

### A. Historical event / resolution-station catalog

For every daily-temperature event we can recover:

- event date and city;
- full outcome ladder;
- exact station/resolver source;
- units and bucket rules;
- final resolved bucket;
- negative-risk grouping;
- fee-enabled state if recoverable.

Output wanted: a compact table showing every city and station-rule regime over time.

Reason: if this mapping is wrong, all later model accuracy numbers are garbage.

## Priority 1 — measure whether the market is miscalibrated before adding weather models

### B. Market calibration / longshot-bias study

For resolved daily-temperature buckets, group entry prices by:

- YES price decile / fine bucket;
- NO price bucket;
- horizon T+0/T+1/T+2+;
- city;
- center vs tail bucket;
- liquidity/spread regime.

For each group calculate:

- observed hit rate;
- expected return buying YES at historical executable price proxy;
- expected return buying NO;
- Brier/calibration residual;
- volume/capacity.

Critical question:

> Are low-probability temperature outcomes systematically overpriced, and is that effect concentrated same-day?

This independently tests the strongest public-bot claim without relying on its code/results.

## Priority 2 — measure the actual weather-model edge

### C. Station-specific forecast error matrix

For every candidate model, compute daily-max error at the exact resolver station by:

- city;
- lead time;
- cycle;
- month/season;
- weather regime.

Compare:

1. deterministic point forecasts;
2. raw ensemble member-max distribution;
3. simple bias correction;
4. calibrated EMOS/residual distribution;
5. calibrated multi-model blend;
6. market-implied distribution.

Metrics:

- MAE for center;
- CRPS;
- bucket Brier/log loss;
- tail reliability.

The decisive output is **where weather information beats the market**, not merely which weather model has lowest MAE.

## Priority 3 — same-day nowcast edge

### D. Conditional observed-high study

At repeated intraday timestamps, reconstruct:

- max observed temperature so far;
- current station conditions;
- remaining ensemble paths;
- final resolver high;
- market ladder prices.

Then calculate fair probabilities using the conditional-max formula.

Measure net EV at horizons such as:

- market open/morning;
- 6h before local peak;
- 3h before peak;
- 1h before peak;
- just after each new METAR near the peak.

Questions:

- When does uncertainty collapse faster than price?
- Which cities have the most predictable peak timing?
- Does same-day NO-tail edge remain after using exact station observations?

## Priority 4 — information-release latency

### E. Forecast-run event study

For every material model cycle:

1. compute old and new fair ladder distributions;
2. identify buckets whose fair probability moves by >X points;
3. align order-book history around first data availability;
4. measure repricing at seconds/minutes after release.

Segment by:

- model;
- city;
- local time;
- event horizon;
- market liquidity;
- size of forecast revision.

Output:

- median price-response curve;
- fraction of shocks with positive taker EV after fees;
- approximate executable capacity before convergence.

If prices reprice inside seconds, this edge is not worth building with ordinary polling. If lag persists for minutes, it becomes a prime strategy.

## Priority 5 — full-ladder structural edge

### F. Probability-simplex / negative-risk study

At each all-bucket snapshot calculate:

- sum of YES bids;
- sum of YES asks;
- fee-adjusted buy-all cost;
- fee-adjusted mint/sell revenue;
- NO_i vs other-YES basket discrepancy;
- depth available at profitable levels;
- duration of each discrepancy.

Also project market prices to the nearest arbitrage-free probability distribution and measure local bucket deviations.

Questions:

- How frequently do true executable ladder arbitrages exist?
- Are they gone after fee/depth?
- Do forecast-informed relative-value trades remain when pure arbitrage does not?

## Priority 6 — reverse-engineer profitable wallets

### G. Wallet policy study

Start with:

- user-supplied `0xbddc...55d4f`;
- gopfan2;
- aenews2;
- ColdMath;
- Poligarch;
- Hans323;
- automatedAItradingbot;
- WeatherTraderBot;
- HighTempTation;
- meteoblue;
- opopv.;
- badatmath.;
- WeatherHK/WeatherHK2.

For each wallet, reconstruct every daily-temperature trade possible and cluster behavior by the fingerprints in `wallets.md`.

Highest-value tests:

- trade timing vs forecast releases;
- signed flow vs our weather residual;
- price band preference;
- T+0 concentration;
- tail distance;
- city specialization;
- whether trade predicts next 30m/2h market move;
- whether trade predicts settlement after controlling for market price.

Do not infer maker behavior merely from on-chain fills; resting-order lifecycle is not fully public.

## Priority 7 — informed market-making economics

### H. Maker vs taker comparison

Once we have fair values and live books, simulate a minimal informed quote policy:

- quote only when spread/rebate + model edge covers expected adverse selection;
- pull/reprice around scheduled model releases;
- skew away from inventory whose fair value moved against us;
- compare to simply crossing the book on the same signal.

Record:

- fill probability;
- spread capture;
- markout 10s/1m/5m after fill;
- rebate per filled dollar;
- inventory PnL;
- total net PnL.

The goal is to determine whether weather alpha is best monetized as **directional information** or **informed liquidity**.

## Priority 8 — capacity

### I. Dollar capacity by edge type

A strategy that makes 30% ROI on $100 of available depth is not equivalent to one making 4% on $50k.

For each validated strategy calculate:

- average profitable depth;
- price impact by order size;
- number of opportunities/day;
- capital lock duration;
- PnL/day at $1k, $5k, $25k, $100k bankroll assumptions;
- overlap/correlation between city bets.

Rank strategies by expected dollar profit, not percentage edge alone.

## Separate research track — climate contracts

The all-time WEATHER leaderboard's biggest wins include monthly/global temperature anomaly and hottest-record markets. These may have more capacity but use completely different mathematics.

After daily temperature research is established, separately investigate:

- exact NASA/GISTEMP or other index definition;
- preliminary data availability before official publication;
- revision mechanics;
- model/observation coverage during the month;
- seasonal forecast ensembles;
- climate trend priors;
- publication-lag arbitrage.

Do not contaminate daily-airport model calibration with climate-index contracts.

## Stop conditions for hypotheses

The project should keep promising hypotheses alive until measured, but each one needs a clear economic rejection condition:

- **weather calibration edge:** no positive executable EV out of sample;
- **run-latency edge:** prices move before realistic access/execution;
- **same-day edge:** market already incorporates observations as fast as us;
- **ladder arb:** fee/depth eliminates discrepancies;
- **wallet alpha:** no incremental predictive value after controls;
- **maker edge:** spread/rebate is eaten by adverse selection.

Rejecting a hypothesis frees attention for a stronger one; it is not a reason to add architecture.

## First implementation after this research phase

When implementation begins, the first code should be a **small data/research collector**, not a trading framework. It should answer experiments A–G with the least code possible.

Before live trading, the minimal signal formula should look like:

`net_edge = calibrated_settlement_probability - executable_price - fees/slippage`

with full-ladder consistency and point-in-time inputs.

Everything else is optional until it demonstrably adds net PnL.
