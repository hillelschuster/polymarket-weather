# Data sources and point-in-time requirements

Snapshot: **2026-08-11**

The eventual edge depends on reconstructing exactly what was knowable at each trade timestamp. A historical weather observation combined with today's reforecast is not a valid backtest of a forecast-latency strategy.

## 1. Polymarket market metadata and rules

### Gamma API

Use for:

- event discovery;
- market titles/slugs;
- outcomes/tokens;
- end dates;
- descriptions/resolution rules;
- negative-risk flags;
- fee/reward metadata where exposed.

The market description must be archived because **resolution station/source can change between events**.

### Rule fields to normalize

For every daily-temperature event store:

- city label;
- airport/station name;
- station code;
- timezone;
- settlement-day definition;
- temperature unit;
- bucket boundaries;
- resolver source/site;
- revision/finalization cutoff;
- negative-risk event identifier;
- token IDs;
- fee-enabled status.

Examples observed in 2026 Polymarket market rules:

- New York City -> LaGuardia Airport (`KLGA`), whole °F, Wunderground history;
- London -> London City Airport (`EGLC`), whole °C;
- Milan -> Malpensa (`LIMC`), whole °C;
- Paris -> Paris-Le Bourget (`LFPB`), whole °C.

The exact event description, not this document, is authoritative for any trade.

## 2. Polymarket prices, books and trades

### CLOB REST + WebSocket

Need point-in-time:

- full top-of-book or depth ladder per token;
- best bid/ask;
- spread;
- midpoint;
- tick size;
- last trade;
- price changes;
- market status;
- our own order/fill state later.

For research, the key missing historical artifact is often **full executable depth**. Price history alone cannot tell whether a nominal edge could have absorbed $10 or $10,000.

Therefore once collection starts, save compact book snapshots around:

- every model release;
- every station observation;
- every detected wallet trade;
- regular low-frequency intervals between catalysts.

No need for a huge generic data platform: timestamped compressed JSON/Parquet is enough initially.

### Data API

Official public endpoints expose:

- WEATHER leaderboard (`/v1/leaderboard`);
- public user trades (`/trades`);
- user activity (`/activity`);
- positions (`/positions`).

This is the main source for wallet research.

### On-chain fills

Polygon logs are useful when we need ground-truth fill-side / exchange mechanics or to resolve ambiguous platform data. Public transaction logs can reveal the taker address and negative-risk exchange fills.

Important limitation: quote placement/cancellation is off-chain, so historical on-chain data alone cannot reconstruct every wallet's resting quote lifecycle. This limits claims that a public wallet was a market maker unless fill patterns plus other evidence support the inference.

## 3. Exact settlement-station observations

### AviationWeather METAR API

Primary operational source for airport observations.

Official AviationWeather Data API provides worldwide METAR data, with a current METAR cache updated roughly once per minute and API history up to its documented window. It publishes rate guidance; archived data must therefore be collected elsewhere for longer historical reconstruction.

Fields relevant to same-day max:

- observation timestamp;
- air temperature;
- dew point;
- wind direction/speed/gust;
- sky cover;
- weather phenomena;
- pressure.

METAR temperature precision/reporting must be reconciled with the resolver's displayed whole-degree maximum. Do not assume raw METAR values map one-to-one to Wunderground's daily high without empirical validation.

### Resolver source itself

If the contract names Wunderground or another page as the resolution source, archive that source's daily history/final display as the **settlement truth**, even if meteorological station data is available elsewhere.

Use alternative official observations to forecast the resolver value, not to redefine the outcome.

### Regional official networks

Useful where they add timely local information while the airport remains the settlement anchor:

- NOAA/NWS networks in the US;
- national meteorological services;
- runway/AWOS networks where public;
- radar/satellite where nowcasting materially changes expected peak.

Only add a source if it improves calibrated probability or timing enough to affect PnL.

## 4. ECMWF

### IFS ENS

Current ECMWF ensemble documentation describes 50 perturbed members plus a control/deterministic context, with 00/06/12/18 UTC cycles and different forecast horizons by cycle. Since IFS Cycle 50r1 in May 2026, open-data file conventions changed; the control/deterministic relationship must be handled according to the current documentation rather than old examples.

Use member-level hourly/step paths to form each member's daily maximum at the station.

Important fields:

- 2m temperature;
- total cloud cover;
- wind;
- pressure/geopotential fields if regime models need them;
- precipitation/convection proxies where relevant.

### AIFS ENS

ECMWF also publishes a 50-member AI ensemble. It is an additional independent-ish predictive system to evaluate, not automatically a separate 50 votes. Its errors can be highly correlated with IFS and must be calibrated empirically.

## 5. NOAA / US models

### National Blend of Models (NBM)

Especially valuable for US airport markets because it already produces probabilistic temperature guidance.

NOAA documentation lists probabilistic maximum-temperature products including means, standard deviations and percentiles. Quantile-mapped distribution products aggregate large numbers of inputs with model weighting.

Useful as:

- a direct probabilistic benchmark;
- an input to our own station calibration;
- a way to detect when a raw global ensemble is clearly mis-dispersed.

### GEFS

Global ensemble useful for comparison and multi-model blend.

### HRRR

High-resolution deterministic model with frequent updates, particularly useful in the short range / same day. It should not be mistaken for an ensemble probability distribution by itself.

### HREF / other convection-allowing ensembles

Potentially useful for short-range US uncertainty if archive/access and station skill justify the added complexity.

## 6. Open-Meteo

Useful as a very convenient aggregation/access layer for:

- ECMWF/GFS/ICON and other model outputs;
- ensemble APIs;
- historical forecast APIs;
- quick prototype comparisons.

But for research integrity we should distinguish:

- provider-native model issue time;
- Open-Meteo processing/availability time;
- any interpolation to requested coordinates.

If the edge depends on minutes after a release, use native provider timestamps/data availability where possible.

## 7. Historical forecast archives

This is the hardest part of rigorous research.

We need **forecasts as issued at the time**, not hindsight analyses. Candidate sources:

- NOAA NOMADS/AWS archives for US models;
- ECMWF open/archive products where available under current access terms;
- Open-Meteo Historical Forecast for convenient model snapshots;
- public reforecast datasets for long-horizon calibration.

For each forecast record retain:

- model;
- run/cycle time;
- actual first-availability timestamp if measurable;
- valid time;
- coordinates/grid point/interpolation method;
- raw values;
- data revision/version identifiers where possible.

## 8. Reforecasts for calibration

A few years of live forecast archives may be insufficient for rare tail probabilities. Reforecasts/hindcasts are valuable for estimating station- and season-specific residual structure.

But reforecast skill must be reconciled with the operational model version; model upgrades can change error distributions.

Use reforecasts mainly to stabilize calibration, then use recent operational data to adapt intercept/spread.

## 9. Full-ladder market dataset

For every event-time snapshot, store **all buckets together**:

`event_id, timestamp, [bucket_i, yes_bid_i, yes_ask_i, no_bid_i, no_ask_i, depth...]`

This enables:

- sum-of-probabilities checks;
- negative-risk basket pricing;
- smoothness/shape diagnostics;
- market-implied distribution extraction;
- adjacent-bucket relative value;
- capacity estimates.

Treating each binary independently destroys this information.

## 10. Wallet dataset

For every tracked wallet trade:

- wallet;
- timestamp;
- condition/event/token;
- side;
- size;
- execution price;
- title/outcome;
- transaction hash;
- weather state immediately before trade;
- book state immediately before trade if collected;
- future price path;
- final settlement.

The goal is to estimate the wallet's conditional policy, not merely cumulative PnL.

## 11. Minimal retention strategy

Do not build a data lake. For the first research implementation, a few simple tables/files are enough:

1. `events` — immutable-ish normalized rules plus raw description snapshot;
2. `forecast_snapshots` — model/run/station/valid-time data;
3. `observations` — resolver-station and other local observations;
4. `market_snapshots` — all-bucket books/prices;
5. `wallet_trades` — tracked public trades;
6. `settlements` — final resolver truth.

The schema should follow the experiments, not precede them.

## Primary references

- Polymarket API docs index: https://docs.polymarket.com/llms.txt
- Leaderboard: https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings
- Public trades: https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets
- CLOB orderbook docs: https://docs.polymarket.com/developers/CLOB/prices-books/get-book
- Negative risk: https://docs.polymarket.com/advanced/neg-risk
- AviationWeather API: https://aviationweather.gov/data/api/
- ECMWF ensemble guide: https://confluence.ecmwf.int/spaces/FUG/pages/673550376/Section+2A.1.2.1+Medium+Range+Ensemble+forecasts
- ECMWF open data: https://www.ecmwf.int/en/forecasts/datasets/open-data
- NOAA NBM weather elements: https://vlab.noaa.gov/web/mdl/nbm-weather-elements
