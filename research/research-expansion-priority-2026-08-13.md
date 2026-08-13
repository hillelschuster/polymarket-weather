# Expanded Weather research priorities — 2026-08-13

## Purpose

This note ranks the most useful additional research directions discovered after the repository's existing daily-temperature, resolver-observation, model-vintage, specialist-wallet and climate-index work.

Ranking criteria are:

- recurrence;
- historical/current market scale;
- clarity of resolver semantics;
- availability of point-in-time source data;
- ability to measure information lead cleanly;
- reuse across multiple markets;
- validation cost.

These are research priorities, not profitability claims.

---

## Tier A — highest-value measurements

### Market-opening efficiency

File: `research/market-opening-efficiency.md`

Major recurring city-temperature markets can open roughly two days before the target date, after several useful forecast cycles already exist. The main study is to build a point-in-time pre-list probability surface and compare it with the first market prices and subsequent convergence.

The attraction is recurrence, large established city-event volume and almost complete reuse of the existing temperature probability engine.

### ECMWF AIFS information timing

File: `research/new-weather-information-sources-2026-08-13.md`

ECMWF currently documents that real-time AIFS open data are released as soon as the forecast is produced. AIFS Single and AIFS ENS run four times daily.

The key test is whether early AIFS probability revisions anticipate later model consensus and market repricing for international airport-temperature markets.

Official source: https://www.ecmwf.int/en/forecasts/datasets/aifs-machine-learning-data

### Spatial one-report-ahead resolver nowcast

File: `research/spatial-and-cross-market-propagation.md`

Nearby/upstream stations, wind shifts, cloud/radar and boundary propagation can be tested as predictors of the next resolver-station threshold crossing before the resolver report itself appears.

This directly extends the existing T+0 observation research while preserving a small, physically interpretable feature set.

### Seasonal snowfall

File: `research/snowfall-cumulative-state-alpha.md`

The January 2026 NYC monthly snowfall ladder reached roughly $112k in event volume, and the Jan 24–26 multi-city snowfall event reached roughly $59.8k.

Monthly snowfall is a running sum. NWS daily climate reports expose intermediate official state, NOHRSC provides observation-based snow analyses, and NOAA/NBM provides probabilistic snow accumulation guidance.

This deserves high seasonal research priority when similar markets recur.

### Mt. Washington monthly maximum wind

File: `research/mt-washington-wind-data-semantics.md`

The July event reached roughly $58k. One summit station, one monthly F6 resolver series, nested thresholds, a long archive, current summit conditions and a specialized twice-daily Higher Summits Forecast make this a compact non-temperature research family.

---

## Tier B — strong diversification

### AirNow PM2.5 daily AQI

File: `research/air-quality-publication-alpha.md`

NYC and Chicago July events had meaningful five-figure volume. Final daily PM2.5 AQI is a 24-hour quantity, while AirNow current AQI uses a NowCast algorithm. The nested “below 100 by date” structure can be modeled with one first-clean-day distribution.

### Arctic sea-ice minimum

File: `research/arctic-sea-ice-minimum-alpha.md`

The current event has shown roughly $65k in recent Weather-page snapshots. The contract explicitly resolves on raw single-day `NH-Daily-Extent`, while the familiar public graph uses a five-day trailing average. The running minimum is monotone and near-real-time precursor products exist.

### Monthly precipitation publication basis

File: `research/resolver-publication-basis-alpha.md`

Official accumulated rain is monotone. Daily/intermediate climate products reveal state before the finalized monthly summary, while precipitation that has physically occurred but is not yet in the latest climate product forms a separate publication-basis component.

### Tornado first-publication basis

File: `research/resolver-publication-basis-alpha.md`

Monthly tornado contracts can depend on the first scheduled NCEI value, including a first value labelled preliminary. Historical research should therefore target the first publication, not a later revised tornado count.

---

## Tier C — strategically useful or lower current scale

### U.S. Drought Monitor

File: `research/drought-monitor-publication-basis.md`

The weekly USDM has a Tuesday data cutoff and Thursday publication, with a large set of publicly identified input layers and an explicitly judgement-based human synthesis process. Current Polymarket markets are new/small, but the publication-basis structure is unusually clean.

### Tropical cyclone advisory timing

File: `research/tropical-cyclone-advisory-research.md`

NHC has a structured six-hour advisory cycle plus special updates, public ATCF state and contracts whose exact semantics can depend on the initial official advisory rather than later reanalysis. Event frequency is low but some hurricane markets have substantial capacity.

### ENSO/RONI first-publication basis

File: `research/enso-roni-publication-basis.md`

The current Super El Niño contract targets first-published CPC RONI values across overlapping seasons. RONI has a specific relative-ERSST transformation and recent values can later revise. Direct current market scale is modest, but the research also improves global-temperature priors.

### TAF/LAMP airport-native guidance

File: `research/aviation-forecast-stack-alpha.md`

TAF revisions and NOAA LAMP provide exact-airport operational information. They should be retained only if they add resolver probability information beyond existing numerical guidance and market price.

### Resolver local-day boundary

File: `research/local-day-boundary-data-quality.md`

The first observation assigned to the target local day mathematically constrains daily extrema. The main research need is correct timezone/source-date handling and measurement of whether this boundary update changes market prices materially.

---

## Cross-cutting research themes

### Publication-basis transformation

Many Weather markets now fit one common template:

`raw/preliminary physical information -> official processing/QC -> delayed contractual publication`

Examples include:

- GISTEMP;
- monthly precipitation;
- tornado counts;
- AQI;
- Drought Monitor;
- RONI;
- sea ice;
- snowfall;
- F6 wind records.

For these families preserve at least:

1. physical event/valid time;
2. raw/precursor first-seen time;
3. intermediate official/QC first-seen time;
4. contractual publication first-seen time.

Historical studies should model the transformation between stages instead of using revised final data as though it existed earlier.

### Cross-market information propagation

File: `research/spatial-and-cross-market-propagation.md`

Same-city adjacent dates, nearby cities and shared forecast cycles can be studied using market-vs-model residuals rather than raw price correlation. This helps test whether one market contains incremental information for another after direct weather-model effects are removed.

### Maker/reward economics as a separate explanatory variable

File: `research/market-opening-efficiency.md`

Weather maker rebates and any market-specific liquidity incentives should be measured separately from forecast or resolver skill so historical returns are not attributed to the wrong mechanism.

---

## Seasonal / lower-priority watchlist

### Event-specific snowfall

Already promoted into the main snowfall family because 2026 examples demonstrated substantial volume.

### Motorsport/race rain

Radar nowcasting and exact FIA weather-report semantics are interesting, but the inspected example had very low market volume.

### Eclipse/cloud visibility

Exact METAR cloud-category settlement is technically clean, but the inspected event had negligible volume.

### Other one-off weather events

Do not prioritize a market merely because it is meteorologically forecastable. Prefer families with recurrence, capacity, unusual resolver structure or reusable data value.

---

## Overall research conclusion

The project now contains several distinct information mechanisms:

- physical forecast skill;
- faster source/nowcast information;
- market-formation/convergence effects;
- resolver/publication reconstruction;
- cumulative running maxima/minima/sums;
- exact logical relationships across thresholds and deadlines.

The broadest reusable idea is that many Weather contracts are not simply forecasts of nature. They are forecasts of **the exact statistic a named resolver will publish after transforming already-observed and future physical information**.

That framing should guide future research selection because it combines meteorology, point-in-time data and contract semantics without assuming one universal model can price every Weather market.