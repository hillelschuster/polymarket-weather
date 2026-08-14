# Highest-value next measurements — profit-only ordering

Snapshot: **2026-08-14**

Objective:

`maximize realistic net dollars after fees + spread + depth + fills + latency + capital lock`.

Research is ranked by the probability that the next measurement materially changes profitable capital deployment.

The current integrated thesis is in:

- [`exploitative-alpha-discovery-2026-08-14.md`](exploitative-alpha-discovery-2026-08-14.md)

---

# Priority 1 — synchronized first-seen weather/model + full-L2 capture

This is now the highest-value common experiment because it answers the largest unresolved questions across multiple alpha families at once:

- ASOS/METAR observation -> market repricing latency;
- AIFS/GFS/HRRR model-file -> market repricing latency;
- stale executable depth after information shocks;
- information-response half-life;
- maker adverse selection around fresh releases;
- actual capacity curves rather than midpoint edge;
- whether specialist activity is early relative to public information.

## Minimal component

Create:

`scripts/live_latency_capture.py`

or an equivalent single-process recorder.

At one synchronized timestamp persist:

```text
utc_receive_time
monotonic_ns

resolver:
  event_id
  condition_id
  source
  station
  timezone
  native_unit
  buckets
  cutoff/revision convention
  rules snapshot hash

Polymarket:
  token_id
  full relevant bid/ask depth
  trades / last trade
  book hash/sequence if exposed
  tick / min size
  feesEnabled / fee schedule
  negRisk metadata

observations:
  station
  source observation time
  first seen time
  raw METAR/SPECI
  T-group
  6h/24h extrema
  running resolver state

models:
  provider/model
  cycle
  forecast step / target field
  first successful fetch
  local receive time
  content hash
  station-derived values

execution when live/shadowing:
  signal time
  order sent
  acknowledged
  matched
  confirmed
```

Append-only compressed JSONL or Parquet is sufficient.

## Core outputs

For each source/catalyst:

`L = t_market_first_reprice - t_source_first_seen`.

Report P10/P25/P50/P75/P90 by:

`station x source_type x local_hour x liquidity_state`.

For each candidate trade report:

`size -> VWAP -> fee -> impact -> expected net dollars`.

For maker fills report:

`10s / 1m / 5m / 30m / 2h signed markout`.

## Go/no-go consequences

- If public first-seen data normally arrive after the market has moved, demote latency taking for that source.
- If information leads the book but stale depth is too small after fees, keep it as a fair-value feature for maker routing rather than taker alpha.
- If stale depth persists with positive net EV, prioritize production execution immediately.

---

# Priority 2 — exact resolver metadata parser

Before autonomous trading, every active market must produce a deterministic resolver specification.

Required fields:

```text
source / station
timezone / day definition
native unit
bucket boundaries
rounding / precision
cutoff / revision rule
outcome token IDs
NegRisk relationship
fee schedule
tick / min size
```

Do not hard-code city -> station mappings. Recent contracts demonstrate that naive assumptions such as NYC/KNYC or Milan/LIML can be wrong for the actual Polymarket resolver object.

The resolver parser should preserve the exact rules text / metadata snapshot used for every trade so later replay targets the same settlement definition.

Relevant research:
- [`city-source-map.md`](city-source-map.md)
- [`resolution-alpha.md`](resolution-alpha.md)
- [`data-quality.md`](data-quality.md)

---

# Priority 3 — US ASOS extrema replay + live state

Daily US temperature remains the fastest route to repeated directional evidence.

The target is not generic METAR temperature. It is the most faithful point-in-time reconstruction of the contract's resolver-compatible running extreme.

## State

For daily high:

`M_t = highest resolver-compatible observation already known`.

`X_t = maximum over the remaining resolver day`.

`H = max(M_t, X_t)`.

Bucket probability:

`q_i(t) = P(H in bucket_i | information available at t)`.

After the likely physical peak, the key quantity is:

`P(X_t > M_t | current state)`.

## Initial data

Parse and retain:

- raw METAR;
- routine/SPECI distinction;
- T-group;
- six-hour extrema;
- 24-hour extrema where present;
- IEM/other validated resolver proxies;
- later DSM/CLI for end-of-day validation.

Relevant research:
- [`us-asos-observation-alpha.md`](us-asos-observation-alpha.md)
- [`us-asos-case-studies.md`](us-asos-case-studies.md)
- [`us-asos-low-alpha.md`](us-asos-low-alpha.md)

## Minimal model

Start small:

`logit P(H > M_t) = beta0 + beta1*(short_range_peak - M_t) + beta2*trend + beta3*solar + beta4*cloud + beta5*front_regime`.

Candidate guidance:

- HRRR;
- LAMP;
- NBM;
- only additional sources that improve resolver probability / executable PnL.

## Required experiment

For each resolved event reconstruct state at:

- each relevant SPECI/new extreme;
- 18Z six-hour extrema;
- 00Z six-hour extrema;
- local apparent peak;
- 1h/2h before contractual cutoff.

Measure:

```text
resolver bucket fidelity
first high-confidence time
CLOB response delay
fillable asks/bids before convergence
fees
net counterfactual PnL
capital time
capacity curve
```

Do not call this sub-second alpha unless prospective latency data prove it.

---

# Priority 4 — maker fill / markout simulator on the same fair values

Forecast-aware maker execution currently has the highest aggregate-income potential, but quoted spread is not enough evidence.

For every probability revision compare identical-signal execution paths.

## Cross now

`EV_cross = fair_probability - actual_executable_price - taker_fee - impact - uncertainty_margin`.

## Make

`EV_make = P(fill before edge decay) * (fair_at_fill - quote + rebate - adverse_markout)`.

Required measurements:

- fill probability;
- time to fill;
- spread captured;
- rebate actually earned;
- 10s/1m/5m/30m/2h markout;
- missed opportunity when no fill;
- inventory imbalance duration;
- dollars per capital-hour.

Expected routing should remain state-dependent:

- fresh large information shock -> cancel stale quotes and take positive-EV depth;
- quiet state / persistent edge -> make;
- source-locked near-deterministic state -> consume stale depth aggressively when fee-adjusted EV remains positive.

Relevant research:
- [`forecast-aware-maker-merge.md`](forecast-aware-maker-merge.md)
- [`execution-routing.md`](execution-routing.md)
- [`market-microstructure.md`](market-microstructure.md)

---

# Priority 5 — AIFS first-seen prospective experiment

ECMWF's public dissemination design makes AIFS a serious early-information candidate, but the thesis must be measured on actual file availability rather than nominal run clocks.

The repo has already narrowed the hypothesis correctly:

- AIFS open data can appear earlier than open IFS;
- free AIFS output is not a direct exact daily-max field;
- therefore the tradable object is a station-calibrated **probability revision**.

Relevant research:
- [`aifs-hypothesis-finalization-2026-08-13.md`](aifs-hypothesis-finalization-2026-08-13.md)
- [`aifs-public-timing-profit-thesis-2026-08-13.md`](aifs-public-timing-profit-thesis-2026-08-13.md)

## Required 20-50-cycle dataset

For each city/date/cycle:

```text
cycle
first_seen
sampled 2m path
ensemble paths when available
old bucket distribution
new bucket distribution
market distribution at first seen
+1m / +5m / +15m / +30m / +60m market state
next major model arrival
final resolver outcome
```

Core statistic:

`Delta q_AIFS -> later market price revision`, after conditioning on current market probability.

Go/no-go:

- demote if market typically reprices first;
- demote if station/grid uncertainty destroys narrow-bucket information;
- promote if AIFS revisions consistently predict later price movement with executable stale depth.

---

# Priority 6 — GFS/HRRR release-latency extension

Reuse the same first-seen infrastructure.

Nominal NCEP production schedules only determine when to intensify polling. The information timestamp is the first successful retrieval of the relevant target field.

Measure the same outputs as AIFS:

- old/new resolver bucket distribution;
- first seen;
- CLOB state;
- response latency;
- net executable dollars.

Do not build a new architecture per model.

---

# Priority 7 — finish GISTEMP forward resolver-vintage experiment

GISTEMP remains one of the highest-capacity hypotheses and already has useful infrastructure:

- `scripts/gistemp_input_watch.py`;
- `scripts/gistemp_market_watch.py`.

The change in ordering does **not** demote the economic thesis. It recognizes that synchronized first-seen/L2 measurement is the same missing primitive needed to establish executable alpha cleanly.

## Preserve every changed vintage

```text
GHCNm qcf vintage
ERSST target-month input
NASA resolver output
receipt timestamp
hash
synchronized all-outcome L2
```

For every input change calculate:

`replica_value_t`

`P(first_release_bucket_i | vintage_t)`

`executable YES/NO EV by depth`

`market response 5m/30m/2h later`.

After publication determine:

`t_correct = earliest public vintage whose high-probability bracket matches first NASA release`.

Then calculate:

`net executable dollars available between t_correct and market convergence`.

Relevant research:
- [`gistemp-basis-alpha.md`](gistemp-basis-alpha.md)
- [`gistemp-input-vintages.md`](gistemp-input-vintages.md)
- [`gistemp-first-release-labels.md`](gistemp-first-release-labels.md)

---

# Priority 8 — propagate monthly climate information into annual rank

Do not build a separate annual climate engine.

Use the monthly resolver distributions directly:

`A_2026 = sum(M_1 ... M_12) / 12`.

After every material monthly/vintage revision:

1. update the annual distribution;
2. compare with historical annual rank thresholds;
3. derive rank probabilities;
4. compare with the direct annual-rank order book;
5. allocate only where incremental expected net dollars exceed the monthly trade or other competing use of capital.

Relevant research:
- [`annual-rank-alpha.md`](annual-rank-alpha.md)

---

# Priority 9 — specialist decomposition only where it can change a signal or execution rule

Wallet archaeology is not a top-level end in itself.

Continue only to:

1. identify an information source/catalyst we do not already consume;
2. estimate actual capacity/sizing at a validated edge;
3. improve maker/taker timing after controlling for our own fair value;
4. recover hidden event-level cashflow mechanics that alter profitability accounting.

High-value segments:

- supplied wallet — directional taker around information revisions;
- Poligarch — passive Weather maker behavior;
- ColdMath — near-certainty / microstructure archetype candidate;
- GISTEMP specialists — timing around qcf/ERSST/public resolver inputs.

Do not infer strategy from explorer-level merge counts without transaction/cashflow classification. Exchange-internal NegRisk settlement can generate merge-like events.

Relevant research:
- [`wallets.md`](wallets.md)
- [`wallet-history-acquisition.md`](wallet-history-acquisition.md)
- [`wallet-history-followup.md`](wallet-history-followup.md)
- [`forecast-aware-maker-merge.md`](forecast-aware-maker-merge.md)
- [`milan-18z-release-case.md`](milan-18z-release-case.md)

---

# Priority 10 — spatial/upwind propagation augmentation

Do this only after the point-in-time observation dataset exists.

Use physical features to improve **remaining exceedance probability**:

```text
front-normal temperature/dewpoint gradient
pressure tendency
wind shift
upstream extrema
radar reflectivity / cell motion
cloud/radiation transition
distance / advective velocity
current local resolver maximum
```

Fit only to resolver-bucket / trading outcomes.

Keep the feature set only if it improves out-of-sample executable PnL over the local-observation + short-range-model baseline.

---

# Always-on structural scan — complete sets / NegRisk

This is computationally cheap and should run continuously even though it is not the main research priority.

For mutually exclusive exhaustive YES asks `a_i`, require:

`sum_i a_i + 0.05 * sum_i[a_i*(1-a_i)] + impact < 1`

before calling a simple full-YES basket profitable.

Also search equivalent NegRisk representations and include any conversion economics, partial-fill risk and capital time.

A displayed sum below $1 is not profit if the legs cannot all be obtained at the modeled prices.

---

# One global marginal-dollar allocator

Every validated opportunity should emit a capacity curve:

`size -> expected net dollars -> expected capital time`.

Rank incremental capital across:

- daily extrema taker signals;
- AIFS/GFS/HRRR revisions;
- maker quotes;
- GISTEMP monthly;
- annual-rank implications;
- source-lock terminal trades;
- NegRisk / complete-set baskets;
- spatial signals only when validated.

Primary ranking quantity:

`expected_net_dollars / expected_dollar_days_locked`.

No fixed allocation by strategy family unless measured economics justify it.

---

# Required common evidence report

Every strategy should produce:

```text
opportunities
fills
turnover
gross_probability_edge
fees
spread
slippage / impact
rebates
net_pnl
pnl_per_turnover
pnl_per_dollar_day
5m / 30m / 2h markout
capacity_curve
resolver_fidelity
loss concentration / outlier dependence
```

Evidence priority:

1. live net PnL;
2. production-fidelity shadow results;
3. realistic real-time paper execution;
4. strict point-in-time replay;
5. conventional backtest;
6. theory.

---

# What remains demoted

## Generic tail/favorite rules

Price band alone is not a strategy. Buy YES or NO only when calibrated resolver probability makes the exact expression positive EV after costs.

## Broad model zoo

Add another weather/climate source only when it improves resolver probability or executable dollars over the current information set.

## Generic wallet copying

Use specialists to infer upstream information and execution mechanics, not to chase public fills after they occur.

## General infrastructure

No dashboard, service mesh, broad observability layer or data platform unless a measured opportunity needs it.

---

# Bottom line

The next research dollar should go to the measurement that resolves the most economically important uncertainty:

> **How long does genuinely new public weather/model information remain stale in the Polymarket book, how much depth is executable during that window, and is maker or taker routing the highest-net-PnL way to monetize it?**

Build the synchronized first-seen information + L2 recorder first. Then let measured net dollars, capacity and capital time determine whether the dominant production allocation goes to ASOS sniping, model-vintage taking, maker quoting, GISTEMP replication or structural baskets.
