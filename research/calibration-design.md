# Calibration design — smallest probability model worth testing

Snapshot: **2026-08-11**

Purpose: turn point-in-time weather forecasts into exact Polymarket resolver probabilities without creating a large statistical system before the data proves one is useful.

The literature and the public-bot failures point to the same starting point:

> **Correct the forecast's recent station/horizon bias, estimate its empirical residual distribution, convert that distribution into resolver buckets, and only then test whether one local model or the market itself adds incremental information.**

---

# 1. Start with a deterministic forecast plus empirical error distribution

For model `m`, resolver station `s`, event date `d`, and information time `t`:

`x_m(s,d,t) = max model 2m temperature across the resolver's local civil day`

Historical verifying resolver maximum:

`y(s,d)`

Historical model error:

`e_m = y - x_m`

For today's forecast `x*`, construct possible resolver maxima directly from historical errors:

`H_k = x* + e_k`

Then for each Polymarket bucket `i`:

`q_i = count(H_k resolves into bucket i) / K`

This yields a coherent probability vector without choosing an arbitrary Gaussian standard deviation.

It also handles fat tails, skew and integer-boundary behavior empirically.

---

# 2. Bias correction can remain extremely simple

The useful distinction is:

`error = systematic_bias + random_residual`.

Estimate current bias with either:

- rolling mean/median error;
- exponentially weighted mean error;
- model-version-specific mean error.

Then center the residual sample after removing that bias.

ECMWF reports that operational statistical post-processing usually improves 2 m temperature forecasts, sometimes substantially. An ECMWF/RMI implementation found that for 2 m temperature, **simple bias correction achieved CRPS improvement comparable to a fuller member-by-member calibration**, while more variance correction was needed for other variables such as Tmax/Tmin/wind gust.

Sources:

https://www.ecmwf.int/en/newsletter/166/meteorology/statistical-post-processing-ensemble-forecasts-belgian-met-service

https://confluence.ecmwf.int/spaces/FUG/pages/673551653/Section+9.2.1.1+Causes+of+errors+in+2m+temperature

This is exactly the result we want economically: try the cheap correction first.

---

# 3. Calibrate the actual daily maximum, not generic hourly temperature

The contract target is a nonlinear path statistic:

`H = max_t T(t)`.

Therefore historical residuals should ultimately be formed on:

`daily resolver maximum - forecast daily maximum`.

Do not assume that hourly 2 m temperature RMSE maps cleanly into daily-high bucket error.

A model may have small hourly bias but systematically miss peak timing or afternoon boundary-layer extremes.

Store one error observation per event/model/run:

`forecast_max, resolver_max, error`.

That is enough for the first probability model.

---

# 4. Horizon is a required conditioning variable

Forecast error distribution changes sharply with lead time.

At minimum split into:

- T+0;
- T+1;
- T+2+.

For T+1, a useful definition is the model run whose output was available during the prior local day and before the wallet/strategy decision.

For T+0, do not use the unconditional full-day residual distribution after observations have already constrained the outcome. Use the conditional-max formulation in section 9.

---

# 5. Model version changes: use recent or pooled current-version errors

A one-degree contract is highly sensitive to systematic model changes.

Current examples:

- ECMWF IFS changed to Cycle 50R1 on 2026-05-12;
- ICON-2I changed on 2026-06-17 specifically to reduce summer maximum-temperature overprediction caused by excessively dry model soil.

A large pre-upgrade residual history can therefore be worse than a smaller current-version sample.

### Simple solution

Use a recency-weighted or version-consistent sample.

If the current version has too few observations at one station, pool comparable nearby stations for the **same model version**, then shrink toward station-specific errors as they accumulate.

Example for post-June-17 ICON-2I around Milan:

- LIMC Malpensa station errors receive highest weight;
- nearby northern-Italy airport errors provide the initial prior;
- older pre-upgrade ICON-2I errors receive little or no weight until demonstrated useful after a bias adjustment.

This increases sample size without inventing a complicated model.

---

# 6. Regional pooling is a practical answer to sparse station data

For a recent model version, define a weighted residual sample from stations `r`:

`w_r ∝ similarity(r,s)`

Similarity can initially be crude and explicit:

- same regional model domain;
- similar elevation;
- similar coastal/interior regime;
- geographic proximity.

Then use weighted empirical residuals.

No Bayesian framework is required to start.

The statistical-postprocessing literature supports local/station calibration and grouped-station approaches where individual stations have limited information. Operational MOS is specifically designed to map gridded model output to point observations.

---

# 7. Do not add ML until linear/error methods leave money on the table

An ECMWF technical study tested linear regression, random forests and neural networks for 2 m temperature forecast-error correction and found **all three methods had similar ability**, improving RMSE roughly 10–15% in the reported application.

Source:
https://www.ecmwf.int/en/elibrary/81297-statistical-modelling-2m-temperature-and-10m-wind-speed-forecast-errors

That is useful evidence against assuming nonlinear ML is necessary.

Initial hierarchy:

1. rolling/version-aware bias;
2. empirical residual distribution;
3. local+global model blend;
4. simple linear contextual correction if needed;
5. ML only if it produces material out-of-sample dollar improvement.

---

# 8. Combining ECMWF and a local model

The local model and global model are not independent; many local systems use ECMWF boundaries. Do not treat them as two independent votes.

Generate separate calibrated distributions:

`q_E`

`q_L`

Then test a one-parameter mixture:

`q_weather = α q_L + (1-α) q_E`.

Fit `α` on past resolver outcomes for the station/horizon, or simply test a small fixed grid such as:

`α ∈ {0, 0.25, 0.5, 0.75, 1}`.

Choose based on out-of-sample log loss and trading PnL.

A temperature post-processing study combining a convection-permitting limited-area model with a global ensemble found the combined calibrated forecast beat the individual calibrated systems in its setting. This supports testing the mixture, not assuming either local or global guidance always dominates.

Primary paper:
https://doi.org/10.1175/WAF-D-20-0141.1

---

# 9. T+0 conditional maximum requires less uncertainty, not more modeling

At time `t`:

`M_t = maximum resolver observation already available today`.

The final high is:

`H = max(M_t, R_t)`

where `R_t` is the maximum over remaining future temperatures.

For each historical/current model-error scenario:

1. take the remaining forecast path;
2. apply the relevant bias/error perturbation;
3. compute remaining maximum;
4. take `max(M_t, remaining_max)`;
5. map to resolver bucket.

As local afternoon progresses, probability mass mechanically disappears from low buckets.

Near peak, the entire problem may reduce to:

`P(next resolver boundary is crossed before end of day)`.

That is likely the highest signal-to-complexity T+0 model.

---

# 10. The market ladder is a useful prior, not an opponent to ignore

Let normalized coherent market probability be `q_market` and weather probability be `q_weather`.

Test:

`q_final = λ q_weather + (1-λ) q_market`.

Again, a tiny grid is enough initially:

`λ ∈ {0.25, 0.5, 0.75, 1}`.

If the market contains useful information the weather feeds miss, the blend should improve calibration.

If weather dominates consistently in a station/horizon regime, `λ` naturally moves toward 1.

Do not manually choose a philosophical weight for “crowd wisdom.” Measure it.

---

# 11. Direct trade score

For each YES bucket with executable ask `a_i`:

`fee_i = 0.05 * a_i * (1-a_i)`

`cost_i = a_i + fee_i + measured_book_walk_i`

`EV_i = q_final_i - cost_i`.

For NO:

`EV_no_i = (1-q_final_i) - no_all_in_cost_i`.

Multiple buckets can be bought if each has positive expected value.

The ranking variable is expected dollars at actual available depth, not whether a bucket is the modal forecast.

---

# 12. What to measure to decide whether complexity is useful

Every candidate method should produce the same small evaluation table:

`station`
`horizon`
`model_variant`
`N_events`
`log_loss`
`Brier`
`mean_calibration_error`
`number_of_trades`
`gross_model_edge`
`fees`
`spread/book_walk`
`net_PnL`
`PnL_per_event`
`PnL_per_dollar`

Compare:

- raw ECMWF;
- ECMWF bias corrected;
- ECMWF empirical residual distribution;
- local model residual distribution;
- ECMWF+local mixture;
- weather+market mixture.

Stop adding statistical machinery when incremental net dollars stop improving.

---

# 13. Highest-value immediate calibration cases

## Milan

Use post-June-17 ICON-2I regime separately because its Tmax behavior changed materially.

This is the best current forensic case because the supplied wallet's June 29 T+1 entry and June 25 exit give real behavior to align against model revisions.

## Amsterdam

ECMWF + KNMI HARMONIE at exact EHAM. Strong local model and clean archive.

## Paris

ECMWF + AROME with resolver station versioned per event.

## Tel Aviv

Historical ECMWF residual probability first; add live ICON-IL as soon as runs are captured. IMS verification already gives a strong prior that ICON-IL adds 2 m temperature skill.

---

# Bottom line

The first serious probability model can be only a few formulas:

`forecast daily max`

`+ recent/version-aware bias`

`+ empirical residual distribution`

`→ exact resolver bucket probabilities`

`→ optional one-parameter local/global blend`

`→ optional one-parameter weather/market blend`

`→ executable fee-adjusted EV`.

This is statistically legitimate, directly testable, and small enough that every extra layer must prove its dollar contribution.