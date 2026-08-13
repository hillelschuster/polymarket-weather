# Mt. Washington threshold structure — deep dive

Snapshot: **2026-08-13**

## Verdict

Mt. Washington monthly wind is more interesting than a generic wind forecast market because every threshold is a claim on the **same latent monthly maximum**.

That creates three separable research mechanisms:

1. **exact threshold payoff relationships** across markets;
2. **running-maximum state** that makes crossed thresholds deterministic;
3. **future exceedance hazard** for thresholds not yet crossed.

The first mechanism is purely mathematical and does not require a meteorological edge.

The second can benefit from real-time summit data before the nightly F6 publication used by the contract.

The third uses a compact station-specific extreme-wind model.

Official sources:

- Polymarket July event: https://polymarket.com/event/highest-mtpt-washington-wind-speed-in-july-20260626193609212
- Mt. Washington Observatory weather/data: https://mountwashington.org/weather/
- F6/current-data update description: https://mountwashington.org/2025-by-the-numbers/

---

## 1. One latent variable prices every threshold

Let:

`W = final monthly maximum summit gust in whole mph`.

For threshold `K`:

`Y_K = 1(W >= K)`.

Therefore:

`q_K = P(W >= K)`.

For `K1 < K2`:

`q_K1 >= q_K2`.

Every threshold probability is simply one point on the survival function:

`S_W(K) = 1 - F_W(K^-)`.

A separate binary classifier for each threshold is unnecessary and can violate basic probability structure.

The correct object is a single distribution over `W`.

---

## 2. Exact cross-threshold payoff identity

Take two thresholds with `K1 < K2`.

Consider the terminal portfolio:

`YES(W >= K1) + NO(W >= K2)`.

Its payout is:

| Final monthly maximum | Lower-threshold YES | Higher-threshold NO | Total |
|---|---:|---:|---:|
| `W < K1` | 0 | 1 | **1** |
| `K1 <= W < K2` | 1 | 1 | **2** |
| `W >= K2` | 1 | 0 | **1** |

Thus:

`payoff = 1 + 1(K1 <= W < K2)`.

This gives two immediate mathematical conclusions.

### Minimum terminal value

`minimum payoff = $1` per matched pair.

So if the **simultaneously fillable all-in acquisition cost** of the pair is below $1, the price set is mechanically inconsistent with the common resolver outcome.

The relevant cost must include:

- actual executable asks/depth for both legs;
- taker fees on both fills if crossed;
- incomplete-fill risk;
- any operational cost that is not negligible.

Displayed probabilities are not enough.

### Expected value above the floor

If all-in pair cost is `C`:

`EV = 1 - C + P(K1 <= W < K2)`.

The probability of the middle interval is:

`P(K1 <= W < K2) = q_K1 - q_K2`.

Therefore the meteorological distribution is valuable even when the pair costs more than $1:

`fair pair value = 1 + q_K1 - q_K2`.

This is a cleaner relative-value target than treating the two thresholds independently.

---

## 3. General interval-strip representation

The threshold ladder can be transformed into probabilities of disjoint intervals.

For ordered thresholds:

`K1 < K2 < ... < Kn`,

interval masses are:

`P(K_i <= W < K_{i+1}) = q_Ki - q_K(i+1)`.

Tail:

`P(W >= K_n) = q_Kn`.

Below first threshold:

`P(W < K1) = 1 - q_K1`.

This is analogous to converting cumulative option prices into a distribution.

Research diagnostics should therefore work in **interval mass space** as well as raw threshold space.

Negative interval mass means a probability inconsistency.

---

## 4. Running monthly maximum collapses part of the ladder

Let:

`M_t = highest trusted F6-equivalent summit gust observed so far in the month`.

For every `K <= M_t`:

`q_K(t) = 1`

subject only to resolver-source/revision uncertainty.

For `K > M_t`:

`q_K(t) = P(R_t >= K)`

where `R_t` is the largest remaining gust in the month.

This means the state naturally decomposes into:

- thresholds already crossed;
- nearby thresholds exposed to the next high-wind event;
- remote tails.

No model should continue assigning ordinary forecast uncertainty to a threshold already established in the contractual data path.

---

## 5. Current summit data versus nightly F6 creates a publication-basis problem

Mount Washington Observatory exposes current conditions and related weather data, while its F6 page is described as being updated nightly.

The contract resolves from the F6 record.

Therefore define:

`G_live(t) = highest summit gust visible from the real-time/current data path`

`G_F6(t) = running maximum already published in F6`.

A potentially useful state is:

`U_t = G_live(t) - G_F6(t)`

when a new gust has occurred but the nightly F6 has not yet reflected it.

Do not assume `G_live` equals later F6 exactly. The decisive resolver-basis study is:

`P(F6 daily maximum >= K | live source has printed >=K)`.

If this correspondence is essentially deterministic for clean gust observations, live data can reduce uncertainty before formal F6 publication.

If revisions/QC often change threshold status, the probability must reflect that basis error.

---

## 6. Future threshold probability is an exceedance-hazard model

For thresholds not yet crossed, the cleanest model is event hazard.

Let `h_d(K)` be the conditional probability that day `d` produces a summit gust >=K, given the current forecast state and no earlier future crossing.

Then:

`q_K(t) = 1 - product_d (1 - h_d(K))`.

For small daily hazards:

`q_K(t) ~= 1 - exp(-Lambda_K)`

with

`Lambda_K = sum_d lambda_d(K)`.

This makes the monthly horizon mathematically simple.

Far-future days use climatological hazards.

Known forecast events replace climatological hazards with event-specific probabilities.

---

## 7. Compact event-specific hazard features

Mt. Washington is terrain-amplified, so raw grid gust should not be treated as the summit gust.

Use a station-specific mapping with a small feature set:

- Observatory Higher Summits Forecast wind/gust language;
- forecast pressure gradient;
- 850/700 hPa wind speed and direction;
- frontal/deep-low passage indicator;
- tropical/remnant cyclone indicator;
- mountain-wave-favorable direction;
- time remaining in month;
- current running maximum.

A logistic event model for threshold `K`:

`logit(h_event(K)) = alpha_K + beta_K' X_event`.

A more data-efficient formulation models the next-event maximum gust `Z`:

`Z = mu(X_event) + epsilon`

then

`h_event(K) = P(Z >= K)`.

One fitted gust distribution can price every threshold coherently.

---

## 8. Local Observatory forecast is a high-value predictor candidate

The Observatory publishes a 48-hour Higher Summits Forecast twice daily and specifically targets high elevations in the Presidential Range.

This is unusually relevant compared with ordinary city contracts because the resolver itself is an extreme mountain summit.

The smallest skill test is:

`subsequent 48h F6 maximum ~ HigherSummitsForecast + climatology`

versus:

`subsequent 48h F6 maximum ~ broad model guidance + climatology`.

Measure incremental CRPS/log loss for threshold probabilities.

If the local forecast has no incremental skill, omit it. If it does, it is a compact specialist-data advantage.

---

## 9. Cross-threshold coherence diagnostics

At every timestamp, store executable bid/ask for all thresholds.

For asks `a_yes(K)` and `a_no(K)`, examine for `K1<K2`:

`C_pair = all_in_yes(K1) + all_in_no(K2)`.

Also compute fair value:

`V_pair = 1 + q_K1 - q_K2`.

Research quantities:

`structural_floor_gap = 1 - C_pair`

`model_relative_value_gap = V_pair - C_pair`.

The structural floor does not require a wind model.

The model component values the probability of the monthly maximum ending in `[K1,K2)`.

Historical screenshots that appear to violate monotonicity must be treated cautiously because Polymarket can display last trade instead of midpoint when spreads exceed 10 cents. Use L2/executable prices for real conclusions.

---

## 10. Capacity and empirical relevance

The July 2026 event accumulated roughly **$57k–$64k** depending on indexed snapshot time, with substantial volume in the 90/95/100 mph thresholds.

This is smaller than the largest snowfall markets but large enough for a compact single-station strategy family to merit study.

The source/archive burden is also low:

- one station;
- one monthly F6 series;
- one Higher Summits Forecast source;
- seven nested thresholds in the inspected event.

Research cost per dollar of possible capacity is attractive.

---

## 11. Historical study

For at least 10–20 years of monthly F6 data, estimate by calendar month:

- distribution of monthly maximum `W`;
- daily running maximum `M_t`;
- date of final monthly maximum;
- empirical remaining-month exceedance probability by date/current max;
- high-wind event classification.

For the 2026 Polymarket months additionally collect:

- L2/price histories;
- threshold-cross timestamps in live/current data;
- nightly F6 update timestamps;
- Higher Summits Forecast vintages;
- exact resolver cutoff.

The highest-value historical experiment is source timing around actual threshold crossings:

`live summit threshold first_seen -> F6 publication -> market repricing`.

---

## 12. Promotion logic

Mt. Washington has three ways to survive as a profitable research lane:

1. repeated all-in cross-threshold price inconsistencies;
2. reliable live-source lead over F6/market repricing after actual gust crossings;
3. forecast hazard skill that prices uncrossed thresholds better than the market.

Any one is sufficient to justify continued work.

If all three fail, the family can be dropped cheaply.

## Bottom line

The central insight is not “forecast Mt. Washington winds.”

It is:

> **Treat the seven binaries as one survival curve over a monthly maximum, exploit the exact interval/payoff identities mathematically, and use live/F6 state plus event hazard only for the uncertainty that remains.**
