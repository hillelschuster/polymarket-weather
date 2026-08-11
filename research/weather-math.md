# Weather trading math

Snapshot: **2026-08-11**

The central mathematical object is a probability distribution over the **exact resolver outcome**, conditioned on every data vintage available at trade time.

For outcome bucket `i`:

`q_i(t) = P(Y = i | I_t)`

where `I_t` includes weather forecasts, observations, resolver state, market information and any validated specialist-wallet features available at time `t`.

The trading problem is then to compare `q_i(t)` with executable prices and choose the path with the highest expected net dollars.

---

## 1. Daily maximum from ensemble paths

A daily-high contract settles on:

`H = max_{h in resolver day} T(h)`

A common modeling error is:

`max_h E[T(h)]`

which is not equal to:

`E[max_h T(h)]`.

For ensemble member `m`:

`H_m = max_h T_m(h)`.

The raw empirical daily-max CDF is:

`F_raw(x) = (1/M) Σ_m 1(H_m <= x)`.

This preserves path dependence and peak timing.

### Resolver transformation

Let `g()` represent the contract-specific measurement and rounding rule. Examples include whole °C, whole °F or a 2°F range.

The contract probability is:

`q_i = P(g(H) ∈ B_i)`.

The resolver function belongs inside the model, not as a display-layer conversion.

---

## 2. Calibration of raw ensemble maxima

Raw ensemble frequency is not automatically a calibrated probability. Calibrate by station, model, horizon and regime.

A compact residual-dressing approach:

`H_actual = H_model + b_s,m,l,c + ε_s,m,l,c`

where:

- `s` = station;
- `m` = model;
- `l` = lead-time bucket;
- `c` = cycle/season/regime;
- `b` = learned bias;
- `ε` = empirical residual distribution.

Then sample or analytically convolve the member maxima with the residual distribution.

### EMOS-style alternative

For an ensemble mean `μ_e` and spread `σ_e`:

`H ~ D(a + b μ_e, c + d σ_e²)`

where distribution `D` can be Gaussian, truncated Gaussian, logistic, Student-t, skew-normal or another family chosen by calibrated bucket likelihood rather than habit.

For daily temperature maxima, the tail shape matters because Polymarket buckets are narrow.

### Hierarchical shrinkage

Small city samples can share information:

`bias_station = λ_station * local_bias + (1-λ_station) * regional/global_bias`

with `λ` increasing with effective local sample size.

This preserves city specificity without estimating noisy independent parameters from a handful of days.

---

## 3. Multi-model blending

Suppose each model `k` produces a calibrated bucket distribution `q_{ik}`.

Linear pool:

`q_i = Σ_k w_k q_{ik}`, with `w_k >= 0`, `Σ w_k = 1`.

Weights can vary by:

- station;
- lead time;
- forecast cycle;
- month/season;
- weather regime.

Use point-in-time scoring history to estimate weights. A simple exponentially weighted log-score or Brier-score weighting often captures most of the value.

Logarithmic opinion pool:

`q_i ∝ Π_k q_{ik}^{w_k}`

can produce sharper consensus when independent models agree.

The economic scoring target is trading PnL / log loss on resolver buckets rather than generic 2m-temperature RMSE.

---

## 4. Same-day conditional maximum

This is the highest-priority math.

At time `t` define:

`M_t = max_{h<=t} O(h)`

where `O(h)` is the resolver-aligned observed temperature.

Future remaining maximum:

`R_t = max_{h>t} T(h)`.

Final high:

`H = max(M_t, R_t)`.

Immediately:

`P(H < M_t) = 0`.

For `x >= M_t`:

`P(H <= x | I_t) = P(R_t <= x | I_t)`.

### Observation-conditioned member paths

Each model/member has an observed error at time `t`:

`e_m(t) = O(t) - T_m(t)`.

Correct remaining path:

`T*_m(h) = T_m(h) + b_{s,m,l} + α_m(h-t) e_m(t)`.

`α(Δ)` describes how much a current local model error persists into the next few hours. It is estimated historically and generally decays with lead.

Then:

`H_m(t) = max(M_t, max_{h>t} T*_m(h))`.

Apply residual dressing and resolver transformation to `{H_m(t)}`.

### Peak-crossing formulation

Suppose current resolver value maps to bucket `b`, whose next upper decision boundary is `u_b`.

The core late-day probability is:

`r_t = P(max_{h>t} T(h) >= u_b | I_t)`.

If there is no lower ambiguity because `M_t` is already in `b`, then approximately:

`q_b(t) = 1 - r_t`.

This makes the strategy computationally simple near the peak: estimate one exceedance probability accurately.

---

## 5. Same-day conditional minimum

For low-temperature markets:

`m_t = min_{h<=t} O(h)`

`Rmin_t = min_{h>t} T(h)`

`L = min(m_t, Rmin_t)`.

Once the overnight/morning minimum is established, upper buckets become impossible. The key late-period probability becomes whether the temperature will fall below the next lower resolver boundary.

This is the mirror image of certainty-collapse in daily highs.

---

## 6. Cumulative precipitation

For monthly precipitation:

`P_final = A_t + R_t`

where:

- `A_t` = resolver-aligned accumulated precipitation through time `t`;
- `R_t` = remaining-month precipitation.

Precipitation is strongly non-Gaussian. Model `R_t` through ensemble totals or a zero-inflated / gamma-like distribution, then calibrate bucket probabilities directly.

If bracket `B_i=[l_i,u_i)`:

`q_i(t) = P(l_i - A_t <= R_t < u_i - A_t | I_t)`.

Every realized rainfall event shifts the support permanently.

---

## 7. Running maximum for wind thresholds

For a monthly highest-wind market:

`W_final = max(W_obs,t, W_remaining,t)`.

For threshold `K`:

`P(W_final >= K) = 1` if `W_obs,t >= K`.

Otherwise:

`P(W_final >= K) = P(W_remaining,t >= K | I_t)`.

Nested threshold contracts should obey monotonicity:

`P(W>=85) >= P(W>=90) >= ... >= P(W>=115)`.

Any market surface violating this relationship offers immediate structural information even without a superior weather model.

---

## 8. GISTEMP monthly anomaly mapping

Let `G_m` be final NASA GISTEMP anomaly for month `m`.

Useful proxy datasets `Z_m` include ERA5/ERA5T, NOAA GlobalTemp, Berkeley Earth and partial inputs closer to the NASA pipeline.

Simple historical basis model:

`G_m = a_month + b ERA5_m + c ENSO_m + d trend_m + ε_m`.

A stronger model uses multiple datasets and revision-state variables:

`G_m = f(ERA5T_m, GHCNcoverage_m, ERSST_m, NOAA_m, Berkeley_m, season, trend, previous revisions)`.

For an unfinished month, use partial observed global temperature plus ensemble/weather predictions for remaining days:

`ProxyFinal_m(t) = weighted_mean(observed days 1..t, forecast distribution days t+1..end)`.

Then map the proxy into the historical GISTEMP basis distribution.

The 0.05°C Polymarket buckets make residual standard deviation the key quantity. A model with 0.02–0.03°C residual error can create very different bucket probabilities from one with 0.06°C error even if both have tiny MAE in climate terms.

---

## 9. Full ladder coherence

For mutually exclusive outcomes:

`q_i >= 0`

and:

`Σ_i q_i = 1`.

The weather model naturally satisfies this when all buckets partition the resolver state.

Quoted market midpoints generally will not sum exactly to one because of separate books and spreads. Build coherent market estimates by projecting an input price vector `p` onto the simplex:

`q_market = argmin_q Σ_i w_i (q_i - p_i)^2`

subject to `q_i>=0`, `Σ q_i=1`.

Weights can reflect spread/depth so liquid outcomes influence the projection more.

A logistic/entropy projection is another option.

---

## 10. Negative-risk relationships

In a negative-risk event, one NO share in outcome `i` can convert to one YES share in every other outcome.

Economically:

`NO_i ≡ basket(YES_j for j != i)`.

Fair probability:

`q(NO_i) = 1 - q_i = Σ_{j != i} q_j`.

At executable prices, compare:

- buying NO_i;
- buying the other-YES basket;
- selling either expression when inventory/conversion permits.

Depth and transaction fees determine realizable size.

---

## 11. Market as prior / feature

Let `m_i` be a coherent market probability estimate and `w_i` a weather model probability.

A compact residual learner:

`logit(q_i*) = a + b logit(w_i) + c logit(m_i) + β'X_i`.

`X_i` can contain:

- weather-model disagreement;
- lead time;
- city;
- time since latest forecast update;
- spread/depth;
- specialist-wallet flow.

The learned coefficients tell us where independent weather information has incremental predictive value over the crowd.

Because outcomes are mutually exclusive, fit the multi-class version with softmax or transform logits and renormalize.

---

## 12. Taker expected value

For a YES token with true probability `q` and executable ask `a`:

`gross_EV/share = q - a`.

Current Weather taker fee on fee-enabled markets:

`fee(a) = 0.05 * a * (1-a)`.

Holding to resolution:

`net_EV_taker/share = q - a - fee(a)`.

Expected return on cash spent:

`ROI = (q - a - fee(a)) / (a + fee(a))`.

For NO, replace `q` with `1-q_yes` and use the executable NO ask.

### Fee hurdle examples

At 50¢ the weather fee is 1.25¢ per share, so a taker needs fair probability above 51.25% to have positive pre-slippage EV.

At 20¢ the fee is 0.8¢ per share, so fair probability above 20.8% clears the fee hurdle.

At 5¢ the fee is 0.2375¢ per share, a large percentage of the cheap token's cost.

This is one reason raw “model probability minus midpoint” overstates usable edge.

---

## 13. Maker expected value

Suppose we post a buy at `b < ask` and it fills.

Per filled share:

`EV_maker_filled = q_after_fill - b + rebate_share - adverse_selection_cost`.

The relevant opportunity-level expectation is:

`EV_opportunity = P(fill) * EV_maker_filled + P(no fill) * opportunity_cost`.

For fast forecast shocks, crossing may dominate because fill delay loses the information edge. For slower fair-value convergence, maker execution can dominate due to zero maker fee, spread improvement and rebates.

This comparison belongs to each signal rather than one global execution mode.

---

## 14. Optimal size from marginal EV and depth

Binary Kelly under known `q` and price `p` is a useful starting point, but capacity and probability uncertainty matter.

For YES at total cost per share `c = p + fee` and payout 1, full Kelly fraction on bankroll can be written from binary odds. In practice, the economically useful size is the maximum of expected log growth or expected dollars after accounting for:

- probability estimation uncertainty;
- order-book price ladder;
- correlated city/weather exposures;
- capital lock until resolution;
- competing opportunities.

A direct depth-aware expected-PnL calculation is often clearer:

For orderbook levels `(p_k, size_k)`:

`PnL_k = fill_k * (q - p_k - fee(p_k))`.

Consume levels while marginal expected dollars remain attractive relative to alternative trades.

---

## 15. Information half-life

For a forecast/observation shock at time `t0`, define market response:

`Δp(τ) = p(t0+τ) - p(t0-)`.

And fair-value shock:

`Δq = q(new) - q(old)`.

Capture ratio:

`C(τ) = Δp(τ) / Δq`.

If `C(10s)=0.2` and `C(5m)=0.8`, most of the edge remains briefly after release. If `C(1s)` is already near 1, the opportunity belongs to faster infrastructure or a different data source.

Estimate half-life `τ50` where `C(τ50)=0.5`.

This converts vague “market lag” into an execution parameter.

---

## 16. Wallet incremental information

Let `S_w(t,i)` be signed flow from specialist wallet `w` into outcome `i`.

A wallet factor can be:

`W_i(t) = Σ_w α_{w,segment} * decay(t - trade_time_w) * signed_notional_w`.

Estimate `α` from historical incremental predictive value within city/horizon/market family.

The important regression is not whether a profitable wallet wins often. It is whether:

`P(Y=i | market, weather, W) - P(Y=i | market, weather)`

is economically meaningful.

---

## 17. Profit-first scoring

Forecast scoring metrics:

- log loss;
- Brier score;
- CRPS for continuous extrema;
- calibration curves;
- tail reliability.

Trading metrics:

- executable expected PnL;
- realized PnL;
- markout after entry;
- fill-adjusted edge capture;
- dollar capacity;
- PnL per unit of locked capital;
- opportunity frequency.

The model exists to improve the second group. The first group diagnoses where that improvement comes from.
