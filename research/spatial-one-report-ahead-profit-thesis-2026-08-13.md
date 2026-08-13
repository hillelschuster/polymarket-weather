# Spatial one-report-ahead resolver nowcast — deep dive

Snapshot: **2026-08-13**

## Verdict

Spatial nowcasting should be treated as an **enhancement to T+0 resolver trading**, not as a replacement for direct exact-station feeds.

Where the resolver station itself is available every 1–10 minutes, use it directly.

Spatial information becomes valuable when it can answer a sharper question before the next resolver report:

> What is the probability that the next resolver-station observation crosses the currently relevant contract boundary?

This is a short-horizon supervised probability problem with physically interpretable features and an immediate market-state consequence.

---

## 1. Define the exact prediction target

Suppose the last contractual/resolver-station observation is at time `t0`, and the next expected resolver observation is at `t1`.

For relevant boundary `B`, define:

`Y = 1(T_resolver(t1) >= B)`

for an upward daily-high boundary.

Estimate:

`p_cross = P(Y=1 | information available at t < t1)`.

For a daily low, reverse the inequality.

This is much easier to calibrate than forecasting the entire final daily maximum from nearby stations.

---

## 2. Link next-report crossing to the final bucket distribution

Let current running resolver maximum be `M_t` and current candidate exact bucket be `k`.

The final survival probability of bucket `k` can be decomposed:

`P(final max <= k) = P(no crossing next report) * P(no later crossing | no next crossing)`.

That is:

`q_survival(k,t) = (1 - p_cross_next) * q_later(k,t1 | no crossing)`.

Near the daily peak, `q_later` can be high and the next report dominates the entire probability update.

Thus a good one-report model directly sharpens the T+0 threshold-survival model already supported by London/NYC evidence.

---

## 3. Start with a simple temperature residual model

A first model should predict the next resolver temperature rather than the binary threshold directly.

Let:

`T_next = mu(X_t) + epsilon`.

Then:

`p_cross(B) = 1 - F_epsilon(B - mu(X_t))`.

This has two advantages:

- one model produces crossing probabilities for every nearby threshold;
- residual calibration can be checked directly.

Use regularized linear regression/GAM first. A complex spatiotemporal neural model is unjustified until the simple residual model leaves material probability skill on the table.

---

## 4. Minimal feature set

### Resolver-station state

- last resolver temperature;
- last 2–4 observation slope;
- running daily maximum;
- time since last report;
- minutes to expected next report;
- local solar time / minutes from climatological peak;
- dew point/humidity if available;
- wind direction/speed at resolver station.

### Nearby stations

For station `j`:

- basis-corrected temperature difference to resolver;
- recent temperature slope;
- distance;
- bearing from resolver;
- observation age;
- station elevation/site class.

### Advective geometry

Nearby information should not be weighted only by Euclidean distance.

Let wind vector point toward the resolver from station `j` with along-flow projected distance `d_parallel,j` and cross-flow distance `d_perp,j`.

A simple physical weight is:

`w_j ∝ exp(-|d_parallel,j - v*tau|/L_parallel) * exp(-|d_perp,j|/L_perp)`

where:

- `v` = representative wind/advection speed;
- `tau` = time to next resolver report.

This favors stations whose current air mass is plausibly moving toward the resolver over the forecast interval.

The exact exponential form is a starting hypothesis; historical calibration decides whether it beats simpler inverse-distance weighting.

---

## 5. Front/sea-breeze/cloud regimes matter more than static station levels

The biggest short-horizon errors are likely regime changes rather than smooth interpolation.

Useful compact indicators:

- wind shift crossing at upstream station;
- pressure tendency/front passage;
- radar precipitation arrival;
- cloud-cover/radiation change;
- sea-breeze boundary location;
- nearby stations already crossing the target temperature;
- convective outflow/cold pool.

A regime mixture is appropriate:

`P(T_next) = sum_r P(r | X_t) * P(T_next | r, X_t)`.

But start with a small number of interpretable regimes such as:

- continued heating;
- marine/front cooling onset;
- convective/cloud interruption.

---

## 6. Station basis must be learned, not assumed

Nearby stations differ systematically due to:

- elevation;
- land use;
- airport surface exposure;
- coast distance;
- sensor type;
- urban heat island;
- observation averaging.

For each neighbor `j`, estimate historical basis conditional on weather regime:

`b_j(h,r) = E[T_resolver(t+h) - T_j(t) | regime r]`.

Use basis-corrected neighbor predictor:

`T_j_adj = T_j + b_j`.

This is more important than adding many stations. Five well-calibrated stations can be superior to fifty unmodeled observations.

---

## 7. The most valuable target is boundary distance, not raw temperature RMSE

Prediction errors matter asymmetrically around Polymarket bucket boundaries.

Let:

`D = B - T_last`.

A model that reduces RMSE from 0.8°C to 0.7°C is not automatically valuable.

What matters is calibration of:

`P(T_next >= B)`

when `D` is small enough that the next report can change the contract distribution.

Evaluate:

- Brier score for crossing events;
- log loss;
- reliability curves;
- precision/recall conditional on `|D| <= 1°C` or the resolver-specific boundary band;
- incremental information versus the market itself.

---

## 8. Market-aware incremental test

Let market probability before the next report be `p_m` for a relevant outcome.

Let baseline resolver-state model probability be `q_base`.

Let spatial model probability be `q_spatial`.

The spatial data are useful only if they add information beyond both the baseline and market.

Test a meta-model:

`logit(P(Y=1)) = alpha + beta_m*logit(p_m) + beta_b*logit(q_base) + beta_s*logit(p_cross_spatial)`.

If `beta_s` is stable and improves out-of-sample log loss, the spatial signal has incremental value.

Then measure whether the corresponding fair-value revision precedes market repricing.

---

## 9. City selection should follow source cadence

Spatial nowcast is highest-value where:

- resolver reports are 30–60 minutes apart;
- nearby stations update every 1–10 minutes;
- local boundaries/fronts can materially move the next report;
- the Polymarket bucket is narrow;
- books have useful capacity.

It is lower priority where the exact resolver station already has a trusted one-minute precursor feed with low latency.

This changes the city ranking from “largest markets first” to:

`expected value ∝ report gap * nearby information density * threshold sensitivity * market capacity`.

---

## 10. London-style example

The existing London July 12 reconstruction had:

- current running max: 27°C;
- target wallet buying the 27°C exact bucket;
- next archived EGLC observation 3m28s later at 28°C;
- sharp subsequent repricing.

The spatial research question is not whether 28°C eventually occurred.

It is:

> At 13:16 UTC, did nearby/upstream observations, local trend and boundary state assign materially higher probability to an EGLC 28°C next report than the market implied?

That is a precise historical label and a natural first case study.

---

## 11. Smallest historical experiment

For each target station and day:

1. enumerate resolver observation timestamps;
2. for each report, take the state 5/10/20 minutes before it;
3. collect all nearby station observations that were available by that clock;
4. compute resolver trend and boundary distance;
5. label next resolver temperature/crossing;
6. fit on earlier dates and score later dates;
7. join Polymarket price history on resolved market days.

Do not use later observations to choose the “best” nearby station for the event. Station graph and basis models must be estimated out of sample.

---

## 12. Promotion criterion

Spatial nowcast deserves hot-path complexity only if it does all three:

1. improves next-report crossing probability versus resolver-only baseline;
2. adds information after conditioning on current market price;
3. produces probability revisions before the actual resolver observation and before enough market repricing to remove economic value.

Otherwise keep the direct resolver/precursor strategy simpler.

## Bottom line

The strongest spatial thesis is not broad weather prediction.

It is:

> **Use a small basis-corrected, wind-aware station graph to estimate the probability of the next resolver observation crossing the active bucket boundary; feed that one probability into the existing T+0 survival model.**

This is simple enough to test rigorously and directly targets the few minutes of information lead that matter economically.
