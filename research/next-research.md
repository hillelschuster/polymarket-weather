# Highest-value next measurements

Snapshot: **2026-08-11**

The next work is ranked by expected impact on future net PnL. Each measurement should either identify a profitable edge, improve the probability/execution model, or redirect capital toward a higher-dollar segment.

Priority score:

`ResearchValue ≈ expected edge × capacity × frequency × persistence × speed-to-measurement`

---

# Priority 1 — reverse-engineer the supplied forecasting wallet

Wallet:
`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

## Output

Reconstruct all accessible weather fills and closed positions, then build:

`fill_time × city × station × horizon × bucket × side × entry × size × final_outcome × PnL`

Join each fill to:

- latest resolver observation;
- current observed max/min;
- latest forecast vintages;
- forecast revision magnitude;
- market bid/ask/spread;
- 5m/30m/2h price markout.

## Questions with immediate PnL value

1. Do T+0 entries cluster after the resolver prints the eventual winning bucket?
2. Do fills cluster after ECMWF/NBM/LAMP/local-model releases?
3. Does the wallet buy the mode or forecast revisions toward the mode?
4. Does its flow predict settlement after controlling for market price?
5. Does its flow predict near-term price after controlling for our weather signal?
6. Which cities/horizons produce most of its PnL?
7. How much edge remains at the price immediately after its public fill?

## Why this is #1

The wallet is currently visible making large exact-bucket YES positions across many cities, including same-day positions bought far below final certainty. One successful reconstruction can reveal the dominant strategy family faster than broad theory.

---

# Priority 2 — build the resolver/station truth map

For every recoverable daily temperature event:

- event ID/date/city;
- all buckets;
- exact source/station;
- local civil day;
- unit/precision;
- rounding/bucket semantics;
- revision cutoff;
- resolved bucket;
- source regime through time.

## Economic outputs

### City opportunity map

Rank cities by:

- market volume;
- spread;
- resolver complexity;
- direct-source availability;
- historical station-model basis;
- number of public competitors using generic sources.

### Resolver discrepancy model

Measure how often:

- routine METAR max;
- IEM reconstruction;
- national agency extrema;
- Wunderground display;
- final market resolution

differ by a bucket.

Cities with predictable discrepancies can become late-resolution specialist opportunities.

---

# Priority 3 — T+0 certainty-collapse study

At repeated timestamps for each city/day, calculate:

- maximum/minimum observed so far;
- next relevant bucket boundary;
- remaining ensemble exceedance probability;
- final winning bucket;
- Polymarket book.

Suggested timestamps are event-driven rather than only fixed clock intervals:

- each METAR/SPECI observation;
- LAMP update;
- NBM update;
- major NWP cycle;
- first time observed max enters each bucket;
- local climatological peak window;
- subsequent hours after the current max stops increasing.

## Main probability

For current bucket upper boundary `u`:

`P(exceed u before local day ends | all current information)`.

## Economic outputs

For each city/time-to-peak state:

- model calibration;
- average taker edge;
- average maker edge;
- depth/capacity;
- price response after observations;
- PnL/day.

The most valuable result is a heatmap:

`city × local_hour × state -> expected executable net PnL`.

---

# Priority 4 — market calibration / behavioral bias map

Before relying solely on sophisticated weather forecasts, estimate whether the market itself contains systematic price distortions.

For resolved daily temperature outcomes, segment by:

- YES entry price;
- NO entry price;
- T+0/T+1/T+2;
- exact bucket vs tail;
- distance from market-implied mode;
- city;
- liquidity/spread;
- local time;
- time to likely daily peak.

Calculate:

- empirical hit probability;
- excess hit probability over price;
- fee-adjusted buy-YES PnL;
- fee-adjusted buy-NO PnL;
- capacity.

## Key public hypothesis to test

BallesJr reports a profitable historical T+0 NO price zone around ~0.20–0.35, while jattree's small clean-ish subset favored modal/consensus NO. Establish the true point-in-time curve independently.

Potential output:

`behavioral_prior(segment)`

which can combine with weather probability.

---

# Priority 5 — station/model forecast skill matrix

For every model/source and resolver station compute daily-extreme probability skill by:

- lead time;
- run cycle;
- month/season;
- local hour;
- regime;
- city.

Models/sources:

- ECMWF ENS/control;
- NBM;
- LAMP;
- HRRR/HREF;
- GFS MOS;
- DWD ICON family;
- JMA MSM;
- Met Office products;
- ECCC HRDPS/RDPS;
- HKO direct forecasts;
- KMA local products;
- Open-Meteo models as accessible baseline.

Metrics:

- bucket log loss;
- Brier score;
- CRPS for continuous max/min;
- mode hit rate;
- calibration by probability band;
- tail reliability;
- incremental trading PnL versus coherent market probability.

## Economic output

A source weight table:

`station × lead × cycle × regime -> source weights`

plus a data-cost/latency ranking.

---

# Priority 6 — forecast-release latency event study

For every model/observation release:

1. save pre-release fair distribution and book;
2. calculate first post-release fair distribution;
3. record full order-book response;
4. calculate capture at 1s/5s/10s/30s/1m/5m/30m.

Segment by:

- city;
- source/model;
- horizon;
- shock size;
- whether revision crosses a bucket boundary;
- spread/depth regime.

## Main outputs

- median price-response curve;
- information half-life;
- executable capacity before convergence;
- source-specific PnL per shock.

## Direct business implication

This decides which sources justify faster collection/execution and which are slow enough for ordinary polling.

---

# Priority 7 — specialist-wallet universe

After the supplied wallet, decompose:

- gopfan2;
- aenews2;
- ColdMath;
- gopfan;
- Poligarch;
- Hans323;
- automatedAItradingbot;
- WeatherTraderBot;
- HighTempTation;
- other high-PnL/high-volume WEATHER specialists.

Separate skill by market family.

## Incremental feature test

Compare:

`Model A = market + weather`

versus

`Model B = market + weather + specialist flow`.

Measure:

- log-loss improvement;
- near-term markout improvement;
- executable PnL improvement.

If several independent specialists trade the same bucket before price convergence, create a consensus factor.

---

# Priority 8 — full-ladder structural edge

For synchronized event snapshots calculate:

- sum of YES asks/bids;
- coherent probability projection;
- NO_i versus other-YES basket;
- executable basket cost by depth;
- duration of discrepancies;
- forecast-informed local relative value.

## Economic outputs

- pure arbitrage frequency/capacity;
- relative-value PnL after weather signal;
- which cities have the least synchronized ladders;
- whether structural edge is largest immediately after forecast shocks.

---

# Priority 9 — maker-versus-taker monetization

For the exact same fair-value signals simulate/measure two paths:

### Taker

- immediate ask/bid;
- fee;
- depth/impact;
- markout.

### Maker

- candidate quote;
- fill probability;
- fill latency;
- adverse-selection markout;
- rebate;
- inventory PnL.

## Output

Learn a routing rule:

`execution_mode = f(edge_size, half_life, spread, depth, time_to_resolution, recent_flow)`.

This can increase realized PnL without changing forecast accuracy at all.

---

# Priority 10 — GISTEMP monthly anomaly nowcast

This is the highest-capacity alternative weather track.

## Historical dataset

For each month collect:

- first-published GISTEMP anomaly;
- ERA5/ERA5T monthly anomaly in the corresponding reference convention;
- NOAA GlobalTemp;
- Berkeley Earth;
- GHCN/ERSST inputs or proxies;
- day-of-availability for each source;
- Polymarket climate-market price history where available.

## Model

At each day from late month through NASA release:

`P(GISTEMP bucket_i | data available by that day)`.

Key output:

- residual SD of each proxy/basis model;
- probability of each 0.05°C bucket;
- expected PnL/day and available depth;
- information gain curve from month-end to release.

ERA5T's roughly five-day publication lag versus NASA's scheduled ~10th-of-month GISTEMP release makes the post-month-end window especially interesting.

---

# Priority 11 — cumulative precipitation

For NYC monthly precipitation and future similar markets:

- reconstruct official precipitation-to-date exactly;
- collect remaining-month ensemble precip distributions;
- estimate skewed bracket probabilities;
- measure repricing after major rain events and tropical systems.

Core formula:

`P_final = observed_to_date + remaining_precip`.

Output expected net PnL by day-of-month and weather-event type.

---

# Priority 12 — monthly maximum wind / other running extremes

For Mt Washington and future extrema markets:

- running official maximum-to-date;
- ensemble future maxima;
- tropical-cyclone/front event features;
- nested threshold coherence;
- market depth.

Core formula:

`W_final = max(observed_max, remaining_max)`.

The threshold ladder gives both forecast edge and monotonic structural constraints.

---

# Priority 13 — city specialization map

Build a ranking for every active temperature city:

`CityScore = forecast_alpha × source_lead × spread × volume × opportunity_frequency × capacity`

Useful columns:

- resolver/source complexity;
- direct national feed availability;
- model MAE/log loss;
- public bot coverage;
- specialist wallet activity;
- average spread;
- average daily volume;
- average observed market lag after forecast shocks.

This can reveal unintuitive targets: a “hard” weather city may be extremely profitable when market calibration is even worse.

---

# Priority 14 — capacity and capital allocation

For every validated strategy segment estimate PnL curves at bankroll scales:

- $1k;
- $5k;
- $25k;
- $100k+.

Inputs:

- profitable depth;
- opportunity count/day;
- overlap/correlation;
- capital lock;
- fill probability;
- edge decay with size.

Output:

`marginal expected net dollars per additional dollar of bankroll`.

This determines which edge should receive capital first.

---

# Minimal research collector implied by these priorities

The smallest useful collector eventually needs only a few durable tables/files:

1. **events/resolvers** — rules, station, buckets, outcome;
2. **weather_vintages** — forecasts/observations with availability times;
3. **market_snapshots** — synchronized full ladder books;
4. **wallet_fills** — specialist public activity;
5. **derived_signals** — fair probability, net EV, execution choice;
6. **outcomes/fills** — realized settlement and PnL.

Everything else can be derived offline.

The first implementation should maximize data useful across several hypotheses rather than implement a broad trading framework.
