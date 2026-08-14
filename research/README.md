# Weather alpha research — current synthesis

Snapshot: **2026-08-14**

## Current authoritative research document

Read first:

- [`exploitative-alpha-discovery-2026-08-14.md`](exploitative-alpha-discovery-2026-08-14.md)

It consolidates the current executive edge matrix, the six exploitation vectors, corrected fee/resolver mechanics, mathematical pricing rules, data pipelines, execution routing, failure modes and the profit-ranked implementation roadmap.

## Current verdict

Weather is a real, monetized Polymarket niche, but the strongest formulation is not merely “forecast better than the crowd.”

> **Estimate the exact settlement probability surface from point-in-time information, then monetize it through the cheapest executable route before the marginal market participant updates.**

The production design should therefore be one resolver-aligned probability engine with two regimes:

1. **Maker-first in ordinary information states** — quote around fair value, exploit the full mutually-exclusive ladder and NegRisk relationships, and demand enough margin to survive fill-conditioned adverse selection.
2. **Taker after fresh information shocks** — cancel stale quotes first, recompute the distribution, and cross only depth whose probability edge remains positive after Weather taker fees, spread, impact and model uncertainty.

The most important missing evidence is a **synchronized first-seen information + full Polymarket L2 dataset**. It is the common experiment for ASOS observation latency, AIFS/GFS/HRRR release latency, stale depth, maker toxicity, response half-life and real capacity.

## Current alpha ranking

### 1. Forecast-aware maker / full-ladder NegRisk trading

Why it ranks first in aggregate-dollar potential:

- can monetize repeated customer flow instead of waiting only for large directional signals;
- Weather makers currently pay zero platform trading fee on fee-enabled markets;
- maker rebates can improve economics when eligible;
- the same coherent weather probability surface identifies modal, tail and relative-value mispricing;
- direct repo evidence proves profitable specialist Weather maker activity.

Primary evidence:
- [`forecast-aware-maker-merge.md`](forecast-aware-maker-merge.md)
- [`market-microstructure.md`](market-microstructure.md)
- [`execution-economics-third-pass.md`](execution-economics-third-pass.md)

Primary missing statistic:

`spread captured + rebate + fill-conditioned markout`, stratified by information state.

### 2. US ASOS extrema / resolver-state certainty collapse

Why it is the strongest directional thesis:

- the resolver-relevant observation can differ from generic displayed METAR temperature;
- whole-C transmission can lose whole-F bucket information;
- T-groups, SPECI and six-hour extrema can reveal the peak state with higher resolver fidelity;
- after the likely physical peak, the problem reduces from forecasting the whole day to estimating only the probability of exceeding the already-observed maximum.

Primary evidence:
- [`us-asos-observation-alpha.md`](us-asos-observation-alpha.md)
- [`us-asos-case-studies.md`](us-asos-case-studies.md)
- [`us-asos-low-alpha.md`](us-asos-low-alpha.md)
- [`city-source-map.md`](city-source-map.md)

Primary missing statistic:

`source_first_seen -> CLOB_first_reprice` latency distribution plus executable stale depth.

### 3. AIFS / NWP first-seen probability revisions

The edge is not the nominal 00/06/12/18 cycle. It is the **actual first public availability** of target information relative to market repricing.

ECMWF's public dissemination asymmetry makes AIFS a serious candidate, but the repo has already verified an important limitation: free AIFS output is not a direct daily-maximum oracle. It must be transformed into station-calibrated bucket probabilities and evaluated as a probability **revision**.

Primary evidence:
- [`aifs-hypothesis-finalization-2026-08-13.md`](aifs-hypothesis-finalization-2026-08-13.md)
- [`aifs-public-timing-profit-thesis-2026-08-13.md`](aifs-public-timing-profit-thesis-2026-08-13.md)
- [`milan-18z-release-case.md`](milan-18z-release-case.md)
- [`release-timing.md`](release-timing.md)

Primary missing statistic:

`Delta q_model -> subsequent market markout`, using real first-seen timestamps rather than model initialization clocks.

### 4. Climate-vintage replication

GISTEMP, annual-rank and seasonal-extreme markets have lower turnover but potentially much higher capacity.

The point-in-time requirement is decisive: public upstream vintages must be archived when actually available. Today's `latest` file is not historical evidence of what could have been traded earlier.

Primary evidence / tools:
- [`gistemp-basis-alpha.md`](gistemp-basis-alpha.md)
- [`gistemp-input-vintages.md`](gistemp-input-vintages.md)
- [`gistemp-first-release-labels.md`](gistemp-first-release-labels.md)
- [`annual-rank-alpha.md`](annual-rank-alpha.md)
- `../scripts/gistemp_input_watch.py`
- `../scripts/gistemp_market_watch.py`

Primary missing statistic:

first public vintage where a resolver bracket becomes highly concentrated **and** meaningful stale executable depth still exists.

### 5. Spatial/upwind propagation

Use physical propagation only where it improves the **remaining exceedance probability** after conditioning on current local resolver state.

Useful phenomena:

- fronts;
- convection;
- marine layer / sea-breeze boundaries;
- precipitation bands;
- cloud/radiation transitions.

Do not build a giant generic nowcasting stack before the point-in-time station/radar dataset proves incremental resolver PnL.

### 6. Specialist-wallet reverse engineering

Public specialist flow is most useful as a way to infer:

- hidden information sources;
- release clocks;
- city/horizon specialization;
- maker versus taker routing;
- sizing and price bands;
- capacity.

It is not most useful as generic copy-trading after the fill is already public.

Primary evidence:
- [`wallets.md`](wallets.md)
- [`wallet-history-acquisition.md`](wallet-history-acquisition.md)
- [`wallet-history-followup.md`](wallet-history-followup.md)
- [`wallet-forecast-purity.md`](wallet-forecast-purity.md)
- [`specialist-archetypes.md`](specialist-archetypes.md)
- [`milan-18z-release-case.md`](milan-18z-release-case.md)

### 7. Pure structural / complete-set arbitrage

Always scan because it is mathematically cheap. But displayed ladder sums are not executable profit unless all fees, depth, partial fills, leg movement and NegRisk conversion economics are included.

For mutually exclusive exhaustive YES outcomes with asks `a_i`, a simple fee-adjusted basket condition is:

`sum_i a_i + 0.05 * sum_i[a_i * (1-a_i)] + impact < 1`.

Equivalent NegRisk token representations should also be searched.

## Resolver discipline

Never hard-code city -> station assumptions. Every active event must be parsed for:

```text
source / station
timezone / day definition
native unit
bucket boundaries
precision / rounding
cutoff / revision convention
outcome token IDs
NegRisk relationship
fee schedule / tick / min size
```

The same city can use different source/station conventions across markets or time. The prediction target is the contract's exact resolver object.

Primary reference:
- [`city-source-map.md`](city-source-map.md)
- [`resolution-alpha.md`](resolution-alpha.md)
- [`data-quality.md`](data-quality.md)

## Current core formulas

### Taker expected value

For YES fair probability `q` and executable ask `a`:

`fee(a) = 0.05 * a * (1-a)`

`EV_taker/share = q - a - fee(a) - impact - model_uncertainty_margin`.

### Remaining-extreme probability

For daily high:

`H = max(M_t, X_t)`

where `M_t` is the resolver-compatible maximum already observed and `X_t` is the future maximum over the remaining resolver day.

Trade the bucket vector:

`q_i(t) = P(H in bucket_i | point-in-time information)`.

After the likely peak, the key state becomes:

`P(X_t > M_t | information)`.

### Maker quotes

For fair YES `q`:

`YES_bid = q - mY`

`NO_bid = 1 - q - mN`.

If equal complementary quantities fill, raw pair capture is:

`mY + mN`.

But maker profitability must be evaluated after fill-conditioned adverse selection and capital time.

### Effective-cost Kelly

With effective one-share cost `c` and calibrated/shrunk win probability `p`:

`f* = (p - c) / (1 - c)`.

Capacity is additionally limited to book depth where marginal net EV remains positive.

## Minimum data architecture

The desired production core remains deliberately small:

```text
market_discovery.py
resolver.py
live_latency_capture.py
weather_observations.py
model_vintages.py
probability.py
clob.py
strategy.py
ledger.py
```

The new highest-value component is `live_latency_capture.py`, which should append synchronized point-in-time records for:

- complete relevant Polymarket L2;
- trades / book state;
- exact resolver metadata;
- raw station observations and first-seen times;
- model-vintage first-seen times and hashes;
- derived probability revisions;
- order/fill lifecycle timestamps.

No broader infrastructure is justified before this dataset proves where executable alpha survives.

## Profit-ranked next work

See [`next-research.md`](next-research.md).

Current order:

1. synchronized first-seen weather/model + full-L2 capture;
2. exact resolver metadata parser;
3. US ASOS extrema replay/live state;
4. maker fill/markout simulator;
5. AIFS first-seen prospective experiment;
6. GFS/HRRR extension;
7. finish the GISTEMP forward experiment;
8. monthly climate -> annual-rank propagation;
9. specialist decomposition only when it can change a signal/execution rule;
10. spatial propagation augmentation after point-in-time data exists.

## Evidence hierarchy

Use, in order:

1. live net PnL;
2. production-fidelity shadow results;
3. realistic real-time paper execution;
4. strict point-in-time replay;
5. conventional backtest;
6. theory.

Do not promote estimates, hypotheses or retrospective proxies into stronger evidence grades.

## Broader references

- [`edge-thesis.md`](edge-thesis.md)
- [`weather-math.md`](weather-math.md)
- [`market-families.md`](market-families.md)
- [`data-sources.md`](data-sources.md)
- [`point-in-time-forecast-reconstruction.md`](point-in-time-forecast-reconstruction.md)
- [`model-priority-matrix.md`](model-priority-matrix.md)
- [`calibration-design.md`](calibration-design.md)
- [`public-bot-code-audit.md`](public-bot-code-audit.md)
- [`zero-edge-paper-audit.md`](zero-edge-paper-audit.md)
- [`deep-research-2026-08-11.md`](deep-research-2026-08-11.md)

## Bottom line

The project no longer needs another broad weather-model survey before measurement infrastructure.

> **Build one synchronized first-seen information + L2 dataset, then allocate capital to whichever of ASOS sniping, model-vintage taking, maker quoting, climate replication or structural baskets produces the highest genuine net dollars per unit of capital time.**
