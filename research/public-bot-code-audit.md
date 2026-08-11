# Public weather-bot code audit — money-relevant findings

Snapshot: **2026-08-11**

This file records code-level findings that can directly improve expected PnL. The objective is not software review; it is identifying where public strategies leave statistical or execution edge unclaimed.

---

# 1. BallesJr: the weather model is not currently the entry rule

Repository:
`BallesJr/polymarket-weather-edge`

Files inspected:

- `weather_api.py`
- `signal_engine.py`
- README

## Current decision rule

The signal engine explicitly uses:

- `TRADE_HORIZON_DAYS = 0`;
- direction forced to `BUY_NO`;
- NO entry price in `[0.15, 0.40]`;
- minimum liquidity;
- rolling city filter.

The Gaussian weather probability is computed and stored, but comments state it **does not gate the decision**.

This creates a valuable research split:

### Hypothesis A — behavioral price-band alpha

Same-day outcomes priced with NO in roughly this region may exhibit systematic favorite/longshot miscalibration.

### Hypothesis B — incremental meteorological alpha

Within the same price band, a correct resolver model can rank which NO contracts actually have positive expected value.

Test both independently and combined:

`EV = market_price_factor + weather_residual + interaction`.

If weather improves PnL inside the band, this public bot has already identified a useful market regime but leaves substantial information unused.

---

# 2. BallesJr: same-day probability uses an ad hoc future range

In `weather_api.py`, unfinished-day logic does approximately:

- `effective_temp = max(observed_max, forecast_max)`;
- `effective_low = effective_temp - 0.5`;
- `effective_high = effective_temp + 2.0`;
- infer Gaussian sigma from that interval.

This is a heuristic representation of a running maximum.

## Stronger replacement

Use the actual remaining hourly paths:

`H_m(t) = max(M_t, max_{h>t} T*_m(h))`.

Then estimate probability of crossing the next resolver boundary directly.

This gains information from:

- expected peak time;
- current temperature trajectory;
- cloud/solar changes;
- wind shift/advection;
- member disagreement;
- current model error;
- whether the peak has likely already passed.

A single `[-0.5,+2]` interval cannot represent these states.

---

# 3. BallesJr: stored net edge can be directionally wrong

The signal engine forces `BUY_NO` but computes:

`net_edge = _compute_net_edge(abs(edge), entry_prob)`

where:

`edge = model_prob_yes - market_prob_yes`.

For BUY_NO, true directional probability advantage is:

`(1-model_prob_yes) - no_price`

before fees.

Taking `abs(edge)` can label a trade as high “net edge” even when the model says YES is underpriced and therefore NO is overvalued.

Because the current band rule ignores this number for entry, it does not necessarily change which trades are opened. But it contaminates:

- signal ranking;
- confidence labels;
- stored feature interpretation;
- any later analysis that assumes `net_edge` is expected return.

## Profit-relevant correction

Store both:

`raw_yes_residual = model_yes - yes_market`

and direction-specific:

`net_ev_yes = model_yes - yes_ask - fee(yes_ask)`

`net_ev_no = (1-model_yes) - no_ask - fee(no_ask)`.

Rank the actual expression being traded.

---

# 4. BallesJr: probability distribution floor/cap can distort tails

The probability engine clips final bucket probabilities to `[0.001, 0.999]`.

Small numerical floors can be convenient, but a 0.1% artificial floor across many impossible/far-tail outcomes adds probability mass and breaks full-ladder coherence unless renormalized.

For a 10-bucket ladder, nine artificial 0.1% floors already consume nearly 1 percentage point.

## Better formulation

- derive all bucket probabilities from one continuous or empirical resolver distribution;
- allow true numerical values close to zero;
- enforce `Σ q_i = 1` once after bucketization;
- use tiny epsilon only inside log-loss computation.

This preserves near-certainty same-day information.

---

# 5. BallesJr: historical observation choice is a strong idea

The project prefers IEM daily station summaries over ERA5 grid reanalysis for resolved-market auditing and reports materially higher agreement with market outcomes.

This is directionally exactly right: the forecast model and the truth source are separate problems. A sophisticated forecast evaluated against the wrong truth can appear profitable or unprofitable for the wrong reason.

Our extension:

- reconstruct the resolver from raw station reports where possible;
- store the first resolver publication and any later revision separately;
- compare our reconstruction to actual Polymarket resolution event-by-event;
- learn source-specific discrepancy probability.

That last variable can itself become a late-resolution pricing feature.

---

# 6. suislanchez: raw member count is an uncalibrated probability

`backend/core/weather_signals.py` estimates probability by counting ensemble members above/below the threshold.

Then it clips to 5–95% and uses ensemble agreement as confidence.

## Money-relevant weaknesses

### Raw ensemble reliability

If 35/50 members land above a threshold, the true calibrated probability is not necessarily 70%. Ensemble spread can be under/overdispersed and biased by station/lead/regime.

### Agreement is not confidence

50 nearly identical members can all share the same systematic error. High agreement can coexist with poor calibration.

### Hard clipping destroys certainty-collapse

A same-day bucket that becomes 99% likely is forcibly represented as 95%, potentially suppressing a profitable near-resolution trade.

## Better formulation

Train a mapping from ensemble distribution features to resolver bucket probabilities:

- member maxima quantiles;
- mean/spread/skew;
- model bias;
- station;
- lead;
- observed maximum;
- current member error;
- weather regime.

Probability calibration, not member unanimity, determines confidence.

---

# 7. nickkea: generic Laplace error is a useful but coarse prior

`weather-market-trading-bot/src/fair_value.py` uses a Laplace distribution with a hard-coded MAE-by-lead table and coarse city classes.

Examples:

- coastal/tropical city multiplier 0.75;
- interior/volatile 1.3;
- fixed expected peak at 14:00 local.

## Useful insight

Forecast errors can be more leptokurtic than Gaussian. Testing Laplace/Student-t/skewed families is worthwhile.

## Exploitable gap

City labels are proxies for the variables we can measure directly:

- station-specific residual distribution;
- season;
- forecast cycle;
- cloud regime;
- frontal passage;
- marine layer;
- urban heat / land-water effects;
- model-specific bias;
- peak timing distribution.

Rather than multiplying global MAE by 0.75/1.3, estimate a hierarchical distribution that shrinks sparse stations toward regional priors.

### Peak hour

Daily max need not occur at 14:00. A sea-breeze arrival, front, foehn/chinook or evening heat retention can move peak timing substantially. Ensemble member maxima naturally solve this without a hard-coded peak hour.

---

# 8. nickkea: Gamma best bid/ask as order-book proxy deserves verification

The code comments say CLOB `/book` returns near-empty books for neg-risk weather markets and therefore it uses Gamma `bestBid`, `bestAsk` and `outcomePrices`.

This is a concrete infrastructure hypothesis to test against current 2026 APIs:

- token-specific CLOB book requests;
- market-channel WebSocket updates;
- Gamma best bid/ask timestamps;
- parity during active trading;
- depth visibility for neg-risk outcomes.

If Gamma top-of-book is fresh but depth is unavailable, it is adequate for rough scanning but not capacity or slippage calculation.

The profitable collector should resolve the data path empirically for current markets.

---

# 9. jattree: the failed PnL is mainly a map of hidden money leaks

`jattree/weather-edge` reported a severe live loss, then later identified many defects.

The economically useful interpretation is not “weather edge fails.” It is a list of PnL leaks that a simpler correct system can avoid.

## Leak A — wrong truth source

Reported backtests used Open-Meteo reanalysis rather than the actual Wunderground/METAR-aligned resolver state. Archive claims about 0.9°C MAE between these objects and a different whole-degree bucket for a large majority of sampled cases.

On 1°C bins this destroys backtest meaning.

## Leak B — wrong station

Denver, Houston and Hong Kong were mapped to different physical stations/sources from Polymarket's actual resolver.

The lesson is profitable specialization: **a station map is part of the model**.

## Leak C — Fahrenheit range integration

Later audit found a Fahrenheit conversion/bucket-boundary error that systematically inflated YES probability on a heavily traded contract type.

This illustrates why all probability mass should be generated in the contract's native resolver unit and bucket convention.

## Leak D — independent “high-edge” adjacent YES trades

Several mutually exclusive YES buckets were opened as if each were independent. The correct object is basket probability/value.

If three adjacent buckets have model probabilities `[0.25,0.40,0.20]` and total ask cost `[0.15,0.25,0.10]`, buying all three can be excellent because combined fair value 0.85 exceeds cost 0.50. If the model values are wrong or the basket cost exceeds combined probability, it is poor. Mutual exclusivity itself is not the problem; failing to account for it jointly is.

## Leak E — cost-free paper fills

Later review reports paper fills originally used midpoint and omitted dynamic fees/spread.

The direct profit improvement is obvious: use executable ask/bid and fee at the time of the hypothetical fill.

## Leak F — noisy bias correction

The project later found blanket bias corrections damaged some cities. This suggests hierarchical/shrunk station bias instead of either “always correct” or “never correct.”

---

# 10. jattree: one potentially valuable historical signal

The later review reports that the clean-ish subset of modal/consensus NO bets went 4/4, while tail YES behavior was poor/contaminated. Sample size is tiny and not proof.

But it aligns with two independent public observations:

- BallesJr's T+0 BUY_NO price-band focus;
- the possibility that weather longshots are behaviorally overpriced.

This justifies a dedicated **price-band calibration study** across resolved daily-temperature markets before assuming all alpha must come from superior forecasting.

A strong system can trade both:

`q_final = weather_model + market_miscalibration_prior`.

---

# 11. Deterministic-bucket bots create predictable market behavior

Several public bots simply buy the bucket containing a deterministic forecast.

If enough participants behave this way, forecast revisions that cross an integer bucket boundary can create discontinuous flows:

- previous bucket gets sold/faded;
- new bucket gets bought;
- adjacent probabilities may overshoot.

This creates a potential second-order strategy:

1. observe forecast revision before generic bot refresh cadence;
2. estimate which bucket their deterministic rule will switch to;
3. trade the expected flow or quote ahead of it.

This is testable via price/volume response around popular NWS/Open-Meteo update times.

---

# 12. Common public blind spots

Across inspected projects, the biggest recurring gaps are:

### Resolver semantics

Generic station coordinates or stale hard-coded mappings.

### Same-day extrema

Point forecast instead of `max(observed_so_far, remaining_path)` / `min(...)`.

### Calibration

Fixed sigma, raw ensemble count or generic MAE rather than station/lead/cycle probability calibration.

### Direct sources

Heavy dependence on Open-Meteo/NWS summary rather than national/local observations and model output.

### Market structure

Independent binary evaluation instead of one coherent ladder.

### Execution

Midpoint/price thresholds rather than fee- and depth-aware EV.

### Wallet information

Almost no public bot integrates specialist public flow.

### Capacity

Fixed $ caps rather than marginal expected PnL across depth and competing signals.

---

# 13. Minimal superior strategy architecture implied by the audit

The code needed to beat these public baselines can remain compact:

1. parse current weather event and exact resolver;
2. fetch resolver-aligned observation and chosen model vintages;
3. build calibrated daily-extreme distribution;
4. condition on current observation state;
5. map one distribution across all buckets;
6. combine with coherent market prior and optional wallet factor;
7. compute bid/ask/depth/fee-adjusted EV;
8. choose maker or taker based on information half-life;
9. allocate dollars by marginal expected PnL.

The competitive advantage is the math/data mapping, not framework size.
