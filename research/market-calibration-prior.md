# Market calibration prior — test price bias instead of assuming it

Snapshot: **2026-08-11**

Purpose: determine whether Polymarket's own weather prices contain a repeatable probability distortion that can improve the forecast model for free.

The eventual strategy should not assume either:

- “market price is always an unbiased probability”; or
- “longshots are always overpriced.”

Both claims are too broad. Calibration can change by domain and horizon.

---

# 1. Relevant external evidence: short-horizon weather can have the opposite of classic longshot bias

A 2026 study, **Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics in Prediction Markets**, analyzes tens of millions of trades by domain and time to resolution.

Paper:
https://arxiv.org/abs/2602.19520

For **Kalshi Weather** markets, reported logistic calibration slopes are:

| Time to resolution | Weather slope `b` |
|---|---:|
| 0–1h | 0.69 |
| 1–3h | 0.84 |
| 3–6h | 0.73 |
| 6–12h | 0.87 |
| 12–24h | 0.91 |
| 24–48h | 0.97 |
| 2d–1w | 1.20 |
| 1w–1mo | 1.20 |
| 1mo+ | 1.37 |

In the paper's convention:

- `b = 1` ≈ perfect calibration when the intercept is near zero;
- `b < 1` = prices are too extreme / overconfident;
- `b > 1` = prices are too compressed toward 50% / classic favorite-longshot style underconfidence.

The paper gives a non-parametric illustration: at a raw **75¢ Weather price**, its isotonic estimate is about **69.1%**.

### Important transfer limitation

The paper does **not** establish the same Weather curve on Polymarket. Its Polymarket sample through 2025 had too little classified Weather coverage for the formal cross-platform weather comparison.

Therefore these numbers are a prior for what to test, not a correction to apply blindly.

---

# 2. Economic interpretation if the same pattern exists on Polymarket

Short-horizon overconfidence (`b < 1`) means prices are too far from 50%.

Conceptually:

- a 75¢ favorite may truly be worth less than 75¢;
- a 25¢ secondary outcome may truly be worth more than 25¢.

That would fit one observable weather-specialist style: `badatmath.` repeatedly buys exact YES buckets in roughly the 10–30¢ region and sometimes captures large repricing moves.

It could also explain profitable high-priced NO/favorite-fading expressions.

But the direction must be measured directly on Polymarket daily-temperature ladders before being used.

---

# 3. Do not estimate calibration from every trade

Using every trade creates several distortions for our purpose:

- high-volume markets receive enormous weight;
- one event appears thousands of times with the same final outcome;
- trade frequency changes with news and certainty;
- stale/low-size prints can contaminate the price object;
- event outcomes within one ladder are mutually exclusive, not independent binaries.

The clean trading calibration dataset should use **one coherent event snapshot at a defined decision time**.

---

# 4. Fixed-horizon event snapshots

For each daily-temperature event, reconstruct the full YES ladder at standard horizons such as:

- T+1 local morning / approximately 24h before expected peak;
- 12h before expected peak;
- 6h before expected peak;
- 3h before expected peak;
- 1h before expected peak;
- after likely peak but before local-day end.

The exact grid can be simplified after sample size is known.

For each horizon `h`, event `e`, and bucket `i` store:

`raw_price_{e,i,h}`

`final_outcome_{e,i}`.

Use the most recent price **known before the snapshot timestamp**, with a staleness field.

---

# 5. Build a coherent market probability surface first

Historical token prices can be asynchronous across buckets.

At a chosen snapshot:

1. take the latest pre-snapshot price for each bucket;
2. reject or downweight excessively stale buckets;
3. form raw vector `p_i`;
4. project/renormalize it to a probability simplex for the informational prior.

Simplest normalization:

`p_i^* = p_i / Σ_j p_j`.

For future live research, use simultaneous bid/ask/mid snapshots and a better no-arbitrage simplex projection if the simple normalization produces a meaningful difference.

Do **not** use the normalized prior as executable trade cost. Execution still uses actual ask/bid plus fees.

---

# 6. One-parameter calibration test

Start with the smallest useful model:

`logit(P(Y_i=1)) = a_h + b_h * logit(p_i^*)`.

Estimate separately by horizon `h`.

Interpretation:

- `b_h ≈ 1`, `a_h ≈ 0`: leave the market prior alone;
- `b_h < 1`: flatten probabilities toward 50% / reduce extremity;
- `b_h > 1`: sharpen away from 50%;
- nonzero `a_h`: directional YES frequency bias that slope alone does not capture.

Because buckets within one event are dependent, use event-level resampling / clustering for uncertainty rather than treating every bucket as independent.

For the eventual trading model, statistical significance is secondary to whether the correction improves **out-of-sample net dollar PnL**.

---

# 7. Even simpler non-parametric check

Before fitting anything, group coherent market prices into bands:

`0–10%`
`10–20%`
`20–30%`
`30–40%`
`40–50%`
`50–60%`
`60–70%`
`70–80%`
`80–90%`
`90–100%`.

For each horizon compute:

`observed_hit_rate - mean_market_probability`.

This directly answers questions such as:

- do 10–20¢ daily-temperature buckets win more than 10–20% of the time?
- are 70–90¢ favorites actually less reliable than their prices imply near local peak?
- does the effect disappear at T+1?

If the binned curve is flat around zero, omit the bias correction.

---

# 8. Weather and market should be tested separately before blending

For every historical event snapshot compute:

`q_weather`

`q_market_calibrated`.

Then compare:

1. market raw;
2. market recalibrated;
3. weather only;
4. weather + raw market;
5. weather + recalibrated market.

Simple blend:

`q_final = λ q_weather + (1-λ) q_market_calibrated`.

Use a tiny grid for `λ`.

This reveals whether the market calibration prior contributes information independently of weather.

---

# 9. Price bias and forecast edge can interact

A weather trade is especially attractive when two independent components point the same way.

Example:

- market asks 20¢ for a bucket;
- historical Polymarket weather calibration says 20¢ buckets at that horizon behave more like 23%;
- resolver weather model says 31%;
- all-in taker cost is about 20.8¢ before book walk.

The behavioral prior alone is small, but it strengthens a much larger meteorological signal.

Conversely, if the market prior says 20¢ outcomes historically resolve only 16%, a weather model needs stronger evidence to overcome that base-rate pattern.

This is why the market calibration correction belongs as a **small prior**, not the entire strategy.

---

# 10. Same-day calibration should condition on information state, not only clock time

A fixed “1 hour to resolution” variable is imperfect for daily highs because the meteorological peak may already be over or still ahead.

Once there is enough data, the most economically meaningful split is:

- before expected peak;
- near expected peak;
- after observed/forecast peak;
- current running maximum already inside favorite bucket;
- next boundary still realistically reachable.

But do not start there. First determine whether simple T+0 horizon calibration already has a large effect.

---

# 11. Historical data needed is already minimal

For first-pass calibration:

`event_id`
`bucket`
`snapshot_time`
`token_price_before_snapshot`
`price_staleness`
`winning_bucket`
`time/horizon class`.

No weather data is required for this specific experiment.

Polymarket's official CLOB price-history endpoint provides timestamped token prices, so each token can be sampled at fixed historical times. Join those to event metadata and resolution.

---

# 12. What result changes the bot

## If short-horizon Polymarket weather is overconfident

Use a mild flattening prior on market probabilities before combining with weather. Search secondary/adjacent outcomes aggressively when the weather model also assigns them excess mass.

## If short-horizon longshots are overpriced

Do the opposite: require more meteorological evidence for low-price YES and favor NO expressions where weather agrees.

## If market prices are already calibrated

Set market recalibration to identity and move on. The edge must come from meteorology/timing/execution instead.

---

# Bottom line

There is credible external evidence that **weather-market calibration is horizon-dependent and can reverse the usual favorite-longshot story**.

The correct response is not to copy the Kalshi curve. It is to run one small Polymarket-specific experiment:

> **At fixed horizons, do resolved daily-temperature outcomes occur at the frequencies implied by the coherent Polymarket ladder?**

If not, the measured distortion becomes a cheap prior in the same simple weather probability engine.