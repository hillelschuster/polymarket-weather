# Spatial nowcast and cross-market propagation research

Snapshot: **2026-08-13**

## Research verdict

The existing T+0 work establishes value in reacting to resolver-station observations. A potentially stronger extension is to predict the next resolver update **before it appears**, using spatially related observations and related-market information.

Two distinct mechanisms should be measured separately:

1. **physical spatial propagation** — nearby/upstream weather observations help predict the resolver station's next threshold crossing;
2. **market information propagation** — one Weather market reprices before another correlated market affected by the same weather/model error.

Neither is deterministic arbitrage. Both are conditional probability updates that can create a timing advantage if the relation is stable and the lagging market remains inefficient.

---

# Part I — spatial one-report-ahead nowcasting

## 1. Economic object

Suppose a daily-high resolver currently has running maximum `M_t` and next relevant bucket boundary `K`.

Instead of waiting for the next resolver report, estimate:

`h(t) = P(next resolver observation >= K | resolver state, nearby observations, wind/cloud/radar state)`

or more generally:

`P(final maximum lands in bucket i | spatial state before next resolver report)`.

This converts the T+0 strategy from reaction to short-horizon nowcasting.

---

## 2. Why nearby stations can lead

Airport temperature changes are often driven by spatially propagating processes:

- fronts;
- sea-breeze boundaries;
- outflow boundaries;
- cloud clearing/arrival;
- precipitation cooling;
- wind shifts/advection;
- marine-layer erosion;
- urban/coastal gradients.

A nearby station can observe a regime change before the resolver airport does.

The useful relation is not raw correlation. It is conditional lead time given flow direction and regime.

For station `j` relative to resolver `r`, candidate variables include:

- distance and bearing;
- current wind vector;
- temperature difference `T_j - T_r`;
- recent temperature slopes;
- wind-shift timing;
- pressure tendency;
- cloud/precipitation state;
- time since the neighboring station crossed the relevant threshold.

A small physics-aware model is preferable to a generic high-dimensional ML system until evidence justifies complexity.

---

## 3. Candidate city structures

### NYC / LaGuardia

Potential nearby information sources include other NYC-area airports and surface networks. The research question is whether JFK/Newark/nearby mesonet changes systematically precede KLGA threshold crossings under identifiable wind regimes.

### London City

Nearby London-region airports and surface stations can reveal frontal/cloud/air-mass changes before EGLC depending on wind direction.

### Coastal Asian airports

Seoul/Incheon, Hong Kong, Singapore and other coastal airports may exhibit particularly structured marine/convective propagation.

### European airport clusters

Paris/Amsterdam/Munich and nearby station networks can provide dense observations with good archives.

Prioritize locations where the resolver already has meaningful Polymarket liquidity and where station feeds are timestamped accurately.

---

## 4. Radar/cloud information

For convective/front-driven cases, radar and satellite/cloud information can predict abrupt changes in remaining heating or cooling.

For the U.S., NOAA/NSSL MRMS is an operational multi-sensor system combining radar and other observations with near-real-time products.

Official source:

- https://www.nssl.noaa.gov/projects/mrms/

The initial research should not ingest every MRMS field. A few categorical variables may be sufficient:

- precipitation approaching resolver station?;
- precipitation currently at resolver?;
- convective boundary nearby?;
- persistent clear/cloud regime?

The value of radar is largest when it changes the probability of further heating, not as a generic weather feature.

---

## 5. Spatial-nowcast validation

For each resolver report:

- timestamp all nearby station observations available beforehand;
- freeze the feature set at a chosen lead such as 2m/5m/10m;
- predict whether next resolver observation crosses the current relevant threshold;
- record actual next report;
- compare with a resolver-only baseline.

Primary metrics:

- Brier/log-loss improvement;
- calibration by lead time;
- threshold-cross precision/recall;
- incremental information over the current Polymarket price;
- market price change after the resolver report.

The most valuable cases are those where the spatial model was confident **and** the market later moved materially after the resolver caught up.

---

# Part II — cross-market information propagation

## 6. Related Weather markets share forecast error

Market prices can contain information beyond the weather models. A liquid Weather market may reveal that informed traders collectively disagree with a model before a thinner related market adjusts.

Useful relationship classes:

1. same city, adjacent dates;
2. nearby cities under one air mass/front;
3. multiple cities updated by the same model cycle;
4. daily anomaly/numeric market versus derived rank/threshold market;
5. specialist activity across a regional cluster.

This is not an exact payoff relationship. It is a correlated residual problem.

---

## 7. Model-relative market residual

For a market/bucket `i`, define a transformed residual such as:

`delta_i = logit(market_probability_i) - logit(model_probability_i)`

Then estimate historical relationships between residuals rather than raw prices.

For two related markets `i` and `j`:

`E[delta_j | delta_i]`

can be estimated with a simple regression or empirical conditional table.

This asks a useful question:

> When informed flow pushes one market away from our weather model, how much of that disagreement usually belongs in the related market too?

The model price remains the baseline; the leading market supplies an additional correction term.

---

## 8. Same-city adjacent dates

Forecast errors often persist across neighboring days because model biases in air mass, cloud regime or boundary-layer mixing are serially correlated.

Example research setup:

- today/T+1 market becomes strongly hotter relative to model;
- tomorrow/T+2 market has not moved similarly;
- determine whether historical same-city residual correlation implies an adjustment.

The relationship should be conditioned on mechanism:

- broad warm/cold air-mass error likely persists;
- timing error in a passing front may shift in the opposite direction across adjacent days;
- isolated convection may have little persistence.

Therefore event-type classification may matter more than raw correlation.

---

## 9. Nearby-city propagation

Pairs such as London/Paris or regionally related European cities may respond asynchronously to the same model/air-mass revision.

The correct test is not “these cities are correlated.” It is:

1. remove each city's direct latest model forecast;
2. measure remaining market-vs-model residual;
3. test whether one city's residual leads the other's;
4. measure lead/lag duration and executable magnitude.

If the lag disappears after controlling for the model update, there is no independent market-propagation signal.

---

## 10. Specialist flow as a propagation signal

The repository already shows specialist Weather wallets can contain information.

A stronger use than copying individual trades may be to treat specialist revaluation in one market as evidence about a **shared latent forecast correction** affecting related markets.

Research fields:

- specialist wallet;
- first affected city/date;
- direction/magnitude of market residual change;
- related market residuals before/after;
- model releases in the same interval;
- subsequent resolver outcomes.

This can distinguish genuine shared information from merely following the same public model release.

---

## 11. Cross-market validation

Create synchronized panels at model/observation event times:

- model probability by market;
- market probability/executable state;
- residual `delta`;
- related-market residuals;
- specialist flow;
- final result.

Measure:

- residual correlation;
- directional lead/lag;
- conditional persistence by event type;
- incremental predictive value over model + own-market price;
- short-horizon markout of the lagging market.

Avoid selecting pairs after observing large moves. Define relationship groups before evaluating them.

---

## 12. Economic ranking

### Spatial one-report-ahead nowcast

Priority: **high** if the existing post-observation T+0 edge survives, because this directly attacks the remaining information lead and may move the signal minutes earlier.

Main difficulty: correct point-in-time station/radar alignment and city-specific calibration.

### Cross-market propagation

Priority: **medium-high**, because it can reuse existing model/market data and scale across many simultaneous Weather events.

Main difficulty: false correlation and overlapping public catalysts.

The smallest professional next measurements are:

1. one resolver city with a dense nearby-station network for spatial threshold prediction;
2. one same-city adjacent-date panel plus one nearby-city pair for market-residual lead/lag.

Only if those simple studies show incremental information should the feature set expand.