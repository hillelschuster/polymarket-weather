# Weather market math

Snapshot: **2026-08-11**

The objective is not weather-forecast accuracy in the abstract. It is **well-calibrated probability at the exact contract boundary, converted into positive net executable EV**.

## 1. Model the daily maximum as a path functional

For ensemble member `m`, first map the forecast to the exact resolution station and settlement-day clock, then compute:

`X_m = max_h T[m,h]`

where `h` runs over all valid observations in the contract's settlement day.

This matters because:

`max_h E[T_h] != E[max_h T_h]`

and because the hourly temperatures are strongly correlated. A Gaussian pasted onto the maximum of the ensemble mean discards information we already have.

The primitive object should therefore be a collection of **member-level daily maxima**, not a point forecast.

## 2. Do not treat raw ensemble members as calibrated probabilities

Raw ensemble systems can be biased, under/over-dispersed, and station/grid mismatched. A useful simple baseline is EMOS / non-homogeneous Gaussian regression:

`X ~ Normal(mu, sigma^2)`

with a location model such as:

`mu = a + sum_k b_k * model_summary_k`

and spread model:

`sigma^2 = c + d*S^2`

where `S^2` is ensemble spread (or a model-specific spread vector).

Parameters should be conditional where data permits on:

- resolution station;
- lead time;
- season;
- forecast cycle;
- broad weather regime.

A simpler alternative worth testing first is empirical residual correction / quantile mapping of the member-max distribution.

The calibration loss should be a proper score: CRPS for the continuous maximum distribution, plus Brier/log loss for the exact Polymarket bucket probabilities. Trading PnL remains the final selection criterion.

## 3. Multi-model ensembles are not one giant bag of equally weighted members

Naively pooling 50 ECMWF members, 30 GFS members, and smaller ensembles gives model weight according to ensemble size rather than skill. Models are also correlated.

Prefer:

1. estimate a calibrated CDF `F_k(x)` per model;
2. combine CDFs using station/lead/regime weights learned from historical point-in-time forecasts;
3. constrain weights sensibly rather than allowing one short sample to create absurd coefficients.

Simple linear pool:

`F(x) = sum_k w_k F_k(x),  sum_k w_k = 1`

Weights can be chosen by rolling CRPS/log score. A dynamically weighted model can be tested later, but static station×horizon weights are a strong low-complexity baseline.

## 4. Same-day markets are conditional-max problems

At time `t`, let:

`M_obs(t) = max temperature actually observed at the resolver station so far`

and let `M_future(t)` be the maximum temperature from the remaining hours. Then:

`M_final = max(M_obs(t), M_future(t))`

For any threshold `x < M_obs(t)`:

`P(M_final <= x | information_t) = 0`

For `x >= M_obs(t)`:

`P(M_final <= x | information_t) = P(M_future(t) <= x | information_t)`

Use the remaining ensemble **paths**, preserving hourly dependence. Also update those paths with the day's observed forecast error: if every model is already running +1.4°F cold at the station under a persistent regime, the conditional distribution should move.

Useful same-day state variables:

- observed maximum so far;
- current station temperature/dew point/wind/clouds;
- time relative to climatological peak;
- latest model-run age;
- today's model-vs-observation residual;
- cloud/radar/sea-breeze/convection regime;
- remaining ensemble-path maxima.

## 5. Convert the continuous distribution into the resolver's discrete buckets

Never assume bucket boundaries until the contract rules and resolver reporting are verified.

If a contract resolves on an integer-valued reported temperature `R(X)`, then for bucket `B_i`:

`q_i = P(R(X) in B_i)`

The mapping `R()` must reproduce the resolver source's actual reporting/rounding semantics. If Wunderground displays a whole-degree station maximum derived from METARs, empirically validate how that display relates to raw observations before assuming `[x-0.5, x+0.5)`.

This is especially important for edge buckets such as `<= 72°F` and `>= 81°F`.

## 6. Fair probability is only the beginning: executable EV

Let `q` be our fair YES probability.

### Taker YES

For an executable YES ask `a`, held to resolution:

`EV_yes_per_share = q - a - fee(a)`

where current fee-enabled Weather markets use the Polymarket fee schedule and the exact per-order rounding rules.

### Taker NO

For executable NO ask `n`:

`EV_no_per_share = (1-q) - n - fee(n)`

### Maker order

For a maker limit `l`, the conditional value is more complex:

`EV_maker ~= P(fill) * [fair_value_after_fill - l + expected_rebate - adverse_selection]`

The probability after a fill is not the unconditional `q`: a fill may happen precisely because new weather information moved fair value through our stale quote. That adverse-selection term is central around forecast releases and same-day observations.

## 7. Kelly sizing for a binary share

If a YES share costs `a`, returns `$1` if YES and `$0` otherwise, and `f` is the fraction of bankroll spent on the position, the frictionless full-Kelly fraction is:

`f* = (q - a) / (1 - a)`

for `q > a`.

For a NO share, replace `q` by `1-q` and `a` by the NO price.

With fees, slippage, fill uncertainty, and especially probability-estimation uncertainty, use the effective payoff distribution rather than this closed form. The main point: **sizing is downstream of probability calibration**. A 5-point probability error can overwhelm any sophistication in Kelly sizing.

A principled way to reduce overbetting without arbitrary caps is to integrate over uncertainty in `q`: maximize expected log wealth under the posterior / bootstrap distribution of the probability estimate.

## 8. The whole ladder must live on the probability simplex

For `K` mutually exclusive temperature outcomes:

`q_i >= 0`

`sum_i q_i = 1`

and:

`P(NO_i) = 1 - q_i = sum_(j != i) q_j`

This creates mechanical consistency checks.

### Buy-all-YES condition

At executable asks `a_i`, with fees `f_i`:

`sum_i (a_i + f_i) < 1`

is a locked-in gross payout opportunity if all legs can actually be filled at quoted depth and the contracts are truly one exhaustive negative-risk event.

### Sell-all-YES / mint route

If the platform mechanics allow `$1` collateral to create the complete outcome set, then executable bids can create an opposite arbitrage when:

`sum_i (bid_i - fees_i) > 1`

The exact CTF / negative-risk adapter path and inventory constraints need to be verified before implementation.

### NO vs basket consistency

For outcome `i`, compare the executable NO_i price with the executable basket of every other YES. Negative-risk conversion should keep these linked, but thin books can still create temporary depth-level discrepancies.

## 9. Use the market as information, not truth

The market price may contain signals our weather model misses. Test a calibrated combination rather than either ignoring price or blindly accepting it:

`logit(q_final) = alpha + beta_w*logit(q_weather) + beta_m*logit(p_market) + beta_f*wallet_flow + regime_terms`

Regime terms can include:

- hours to resolution;
- bid/ask spread and depth;
- forecast-run age;
- observation availability;
- city/station;
- whether a major forecast update just landed.

If `beta_m` is large in some regimes and small in others, the correct strategy is regime-dependent.

## 10. Forecast-release alpha is an event study

For every forecast release `r`, compute the information shock, for example:

`delta_q_weather = q_new - q_old`

Then measure market response at lags `0, 1, 2, 5, 10, 30, 60...` minutes using executable books, not only mids.

Questions:

- How much of `delta_q_weather` is reflected immediately?
- Does response speed vary by city/liquidity/time of day?
- Can a taker monetize the first minutes after release after fees?
- Is the better trade a maker quote placed before the release and repriced instantly afterward?

The edge exists only if the point-in-time forecast was obtainable before the market move.

## 11. Profit diagnostics

For every candidate edge, segment realized / simulated net PnL by:

- city/station;
- horizon;
- price bucket;
- YES vs NO;
- distance of bucket from forecast median;
- forecast-cycle age;
- spread/depth;
- model disagreement;
- same-day observed-high state;
- wallet-flow state;
- maker/taker route.

Probability diagnostics still matter because they reveal whether profits came from real informational edge or accidental exposure:

- Brier score;
- log loss;
- CRPS;
- reliability curve;
- PIT/rank histograms;
- tail calibration.

But the strategy-level objective is **realized net PnL / deployed capital at executable prices**.

## Primary references

- Gneiting et al. (2005), EMOS: https://doi.org/10.1175/MWR2904.1
- Wilks & Hamill (2007), reforecast-based ensemble MOS: https://doi.org/10.1175/MWR3402.1
- ECMWF ensemble guide: https://confluence.ecmwf.int/spaces/FUG/pages/673550376/Section+2A.1.2.1+Medium+Range+Ensemble+forecasts
- NOAA NBM probabilistic elements: https://vlab.noaa.gov/web/mdl/nbm-weather-elements
- Polymarket fees: https://docs.polymarket.com/trading/fees
- Polymarket negative risk: https://docs.polymarket.com/advanced/neg-risk
