# Weather market families — mathematical opportunity map

Snapshot: **2026-08-11**

Polymarket weather is not one strategy. Different contract families expose different state variables, forecast horizons, resolver mechanics, capacity and information-release patterns.

The profitable common structure is:

> Observe the part of the settlement variable already realized, forecast only the remaining uncertainty, transform into the exact resolver distribution, then compare with executable market prices.

This file ranks families by the mathematics that can create edge.

---

# 1. Daily highest temperature

## State variable

`H = max_{local day} T(t)`

At current time:

`H = max(M_t, R_t)`

where `M_t` is the observed maximum and `R_t` is the remaining maximum.

## Why attractive

- recurring daily inventory across many global cities;
- narrow buckets amplify station/model precision differences;
- huge forecast-data ecosystem;
- same-day uncertainty collapses predictably;
- exact-station observations can make outcomes near-certain before resolution;
- market books are fragmented across many cities/outcomes.

## Primary alpha modes

1. T+1/T+2 calibrated forecast distribution;
2. T+0 observation-conditioned peak crossing;
3. model-release latency;
4. resolver/source timing;
5. market longshot/favorite miscalibration;
6. full-ladder relative value;
7. informed maker execution.

## Capacity

Historically one of the deepest recurring weather families. Daily-city pages regularly show tens to hundreds of thousands of dollars of volume in established locations.

**Current rank: highest priority.**

---

# 2. Daily lowest temperature

## State variable

`L = min_{local day} T(t)`

At current time:

`L = min(m_t, Rmin_t)`.

## Why attractive

The information geometry is the mirror of daily highs. During overnight/morning hours, once the observed minimum settles and temperatures begin rising, the chance of a new lower print can fall rapidly.

Potentially even cleaner in climates where minimum timing is tightly tied to sunrise.

## Primary alpha modes

- overnight ensemble minimum paths;
- cloud/wind/dew-point effects on radiational cooling;
- direct station observed minimum;
- sunrise/minimum timing model;
- post-sunrise certainty collapse;
- local-agency observation edge.

## Current resolver diversity

Examples observed:

- Shanghai low → Wunderground at Pudong `ZSPD`, whole °C;
- Hong Kong low → Hong Kong Observatory `Absolute Daily Min`, 0.1°C source precision.

This family deserves independent calibration because forecast-error distribution and optimal trade time differ from highs.

**Current rank: high, likely under-researched relative to highs.**

---

# 3. Monthly precipitation totals

Current Polymarket precipitation page includes monthly markets for NYC, London, Seattle and Hong Kong, with prior-month examples reaching material five-figure volume (e.g. July NYC around $41K and July Hong Kong around $51K in recent indexed pages).

Source:
https://polymarket.com/weather/precipitation

## State variable

`P_final = A_t + R_t`

where:

- `A_t` = official accumulated precipitation to date;
- `R_t` = remaining-month precipitation.

## Structural advantage

Accumulated rain is irreversible. After every storm, entire lower brackets become impossible. Late in the month, remaining uncertainty can shrink quickly.

Unlike temperature, precipitation distributions are strongly skewed and event-driven. This creates room for specialists who model storm scenarios rather than use a normal distribution.

## NYC August 2026

Current market resolves on finalized NOAA Central Park monthly summarized precipitation, with 0.01-inch source precision.

Possible strategy:

1. track exact Central Park precipitation-to-date;
2. build ensemble remaining-month total from GEFS/ECMWF/NBM;
3. explicitly model tropical cyclone/heavy-rain scenarios;
4. update bracket distribution after each observed event;
5. trade when market has stale cumulative state or underprices a forecast event.

## Hong Kong August 2026

Current market resolves on HKO Daily Extract total rainfall to 0.1 mm precision.

HKO exposes direct rainfall observations and nowcast products. Hong Kong's rainfall is typhoon/convective-event dominated, creating large discrete probability shifts after tropical-cyclone track updates.

## Best alpha modes

- cumulative-state lockout;
- storm forecast latency;
- resolver accumulation mismatch;
- local agency versus global model information;
- tropical cyclone scenario mixtures;
- late-month bracket certainty.

## Capacity

Currently variable. New August markets are thin in early snapshots, but prior-month contracts demonstrate that the family can attract tens of thousands of dollars.

**Current rank: medium-high, with strong structural persistence.**

---

# 4. Monthly maximum wind

Current example:
`Highest Mt. Washington wind speed in August?`

Prior July market reached roughly $58K volume in indexed Polymarket data.

## State variable

`W_final = max(W_observed,t, W_remaining,t)`.

Threshold outcomes are nested, e.g. `>=85`, `>=90`, ..., `>=115 mph`.

## Structural constraints

Probabilities must satisfy:

`P(W>=85) >= P(W>=90) >= ...`.

If observed maximum exceeds a threshold, probability for that threshold becomes 1.

This creates both meteorological and mechanical edge.

## Forecast model

Remaining maximum is dominated by synoptic/extreme events rather than average daily conditions.

Useful predictors:

- ECMWF/GEFS maximum gust distributions;
- cyclone tracks;
- surface pressure gradient;
- frontal passages;
- mountain-wave conditions;
- time remaining in month;
- observed maximum to date.

Mixture model:

`P(W_remaining >= K) = Σ_event_scenario P(scenario) * P(max gust >= K | scenario)`.

## Alpha modes

- threshold monotonicity discrepancies;
- storm-update latency;
- official F6 versus live station state;
- tropical cyclone route changes;
- post-threshold certainty.

**Current rank: medium; event-driven but mathematically clean.**

---

# 5. Monthly global temperature anomaly — GISTEMP

Current event:
`August 2026 Temperature Increase (ºC)`

Current indexed market has six narrow outcome buckets; recent snapshot showed leading buckets around 1.20–1.24°C and 1.25–1.29°C.

## State variable

Final NASA GISTEMP global land-ocean anomaly for one month.

This is not a simple running maximum. It is an index produced from global station and sea-surface datasets with a specific methodology.

## Why economically attractive

- potentially much larger capacity than small daily cities;
- scheduled NASA release creates a clear information calendar;
- other global datasets become informative earlier;
- narrow 0.05°C buckets magnify dataset-basis skill;
- leaderboard evidence shows large weather profits can come from climate/global-temperature markets.

## August 2026 timeline

NASA's current release schedule lists August GISTEMP for **September 10, 2026 at 11:00 AM EDT**.

ERA5T is typically roughly five days behind real time; its monthly mean becomes available roughly five days after month-end. That creates a post-month-end window where a strong ERA5T→GISTEMP mapping can be highly informative before the official GISTEMP release.

## Model hierarchy

### Level 1 — historical basis regression

`GISTEMP = a + b*ERA5 + month effects + trend + residual`.

### Level 2 — multi-dataset ensemble

Features:

- ERA5T;
- NOAA GlobalTemp;
- Berkeley Earth;
- ERSST/SST proxies;
- partial GHCN information;
- ENSO/global weather regime;
- historical first-release revisions.

### Level 3 — partial-month nowcast

During month:

- observed global anomaly for elapsed days;
- ensemble/weather predictions for remaining days;
- historical mapping to GISTEMP monthly anomaly.

## Key metric

Residual standard deviation in °C at each information date.

Because buckets are only 0.05°C wide, reducing residual SD from 0.06°C to 0.03°C can dramatically sharpen the modal bucket.

## Alpha modes

- partial-month climate nowcast;
- post-month-end ERA5T lead;
- dataset-basis calibration;
- first-release versus later-revision semantics;
- price response to other global temperature datasets.

**Current rank: high-capacity strategic track.**

---

# 6. Annual hottest-year / rank markets

Polymarket's Record Temperatures page currently includes multi-million-dollar climate markets such as where 2026 ranks among hottest years.

## State variable

Annual global index rank relative to historical years.

## Why attractive

- very high capacity;
- information accumulates monthly;
- by late year, only remaining months are uncertain;
- climate trend and ENSO priors are strong;
- monthly GISTEMP nowcast naturally feeds annual rank probability.

## Model

For year `y` at month `m`:

`annual_anomaly = weighted observed months + distribution(remaining months)`.

Then:

`P(rank = r)` against historical year values and uncertainty in each remaining month.

A strong monthly GISTEMP model becomes a reusable component.

## Alpha modes

- monthly update latency;
- seasonally constrained remaining-year distribution;
- cross-market consistency between monthly anomaly and annual rank markets;
- climate dataset basis.

**Current rank: potentially very high by dollar capacity.**

---

# 7. Hottest-month / record-temperature markets

Contracts such as “August 2026 1st/2nd/3rd hottest on record?” derive from the same global-index process but often have rank/binary outcomes rather than numeric anomaly buckets.

## Structural relationship

If anomaly bucket probabilities imply a distribution for the month, they should imply rank probabilities too.

This creates cross-market relative value:

`P(rank event) = Σ_b P(anomaly bucket b) * P(rank event | b)`.

If the numeric anomaly ladder and rank market disagree, trade the cheaper expression after accounting for resolver-definition consistency.

**Current rank: strong adjunct to GISTEMP model.**

---

# 8. Hurricane count / storm-count markets

Current Weather page includes Atlantic hurricane season count markets.

## State variable

`N_final = N_observed + N_remaining`.

As storms form, lower counts become impossible.

Forecasting requires:

- seasonal priors;
- basin conditions;
- ENSO;
- SST;
- MJO;
- current disturbances;
- ensemble genesis probabilities;
- NHC designation/resolution semantics.

## Alpha modes

- official storm designation timing;
- ensemble genesis before crowd repricing;
- cumulative count state;
- seasonal count distributions;
- cross-market consistency across thresholds/count buckets.

This is forecastable but meteorologically different from temperature, so it should use a separate model family.

**Current rank: medium/high capacity, specialized research track.**

---

# 9. Tornado count / severe weather counts

Current Weather page also lists tornado-count markets.

## State variable

`N_final = observed verified count + remaining count`.

Complication: preliminary tornado reports and final verified counts can differ. Therefore resolver process is especially important.

## Alpha modes

- preliminary-vs-final count calibration;
- severe-weather outlook probabilities;
- convective-season climatology;
- late-month cumulative state;
- event outbreaks.

The key edge may be **verification-count basis**, analogous to station resolver basis in temperature markets.

**Current rank: research-worthy but lower immediate priority than temperature/climate.**

---

# 10. General mathematical taxonomy

Weather contracts can be classified by how information accumulates.

## Running maximum

Examples:

- daily high temperature;
- monthly maximum wind.

`X_final = max(X_observed, X_remaining)`.

Information produces one-sided lockouts upward through time.

## Running minimum

Example:

- daily low temperature.

`X_final = min(X_observed, X_remaining)`.

One-sided lockouts downward.

## Running sum/count

Examples:

- precipitation;
- hurricanes;
- tornadoes.

`X_final = X_observed + X_remaining`.

Past state is permanent and remaining variance shrinks through time.

## Published index

Examples:

- GISTEMP monthly anomaly;
- annual global rank.

`X_final = f(global observations/data pipeline)`.

Edge comes from early proxy datasets, methodology reproduction and publication timing.

## Event threshold

Examples:

- `wind >= K`;
- count `>= K`.

Nested thresholds create monotonic structural constraints.

---

# 11. Market-family ranking framework

Rank each family by:

`FamilyValue = forecastability × information_lead × market_capacity × recurrence × resolver_edge × execution_spread`.

Current qualitative ranking:

| Family | Forecastability | Recurrence | Capacity | Resolver/source edge | Research priority |
|---|---|---|---|---|---|
| daily high temp | high | daily | medium/high | high | #1 |
| daily low temp | high | daily/newer | medium | high | #2 |
| GISTEMP monthly | high with basis model | monthly | high | high | #3 strategic |
| annual temp rank | medium/high | annual | very high | high | high-capacity |
| monthly precip | medium | monthly | emerging | high | medium/high |
| monthly max wind | event-driven | monthly | emerging/medium | high | medium |
| hurricane counts | medium | seasonal | potentially high | medium | separate track |
| tornado counts | medium | monthly/seasonal | unknown | high verification basis | exploratory |

The ranking should ultimately be replaced by measured expected net PnL/day and capital capacity.
