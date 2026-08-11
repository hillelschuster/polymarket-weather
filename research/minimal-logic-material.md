# Minimal trading-logic material

Snapshot: **2026-08-11**

Purpose: preserve only empirical and mathematical material that is directly useful for a small profitable weather-market trader.

The current evidence increasingly points to a compact trading loop:

1. estimate a probability distribution over the exact resolver ladder;
2. compare every bucket with its executable fee-adjusted price;
3. buy the few buckets with the strongest positive dollar EV;
4. use simple round-dollar conviction tiers;
5. update probabilities after forecast/observation changes;
6. sell positions whose posterior value falls below executable bid value;
7. recycle effectively settled winners when redeployment value exceeds the remaining discount to $1.

No extra system is required to express this logic.

---

# 1. Supplied wallet: current portfolio reveals the sizing rule

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Current Polymarket profile snapshot:

https://polymarket.com/@0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f-1774968947489

The first 20 visible weather positions imply approximately **$3,400 of entry cost**.

The striking property is that the entry notionals are almost exact round-dollar tiers:

| Entry-cost tier | Visible positions |
|---:|---:|
| $100 | 11 |
| $150 | 1 |
| $200 | 4 |
| $250 | 2 |
| $400 | 1 |
| $450 | 1 |

Examples:

| Market | Avg price | Shares | Approx entry cost |
|---|---:|---:|---:|
| Istanbul Aug 11 — 27°C | 52.6¢ | 856.0 | $450.26 |
| Tel Aviv Aug 11 — 35°C | 56.9¢ | 439.4 | $250.02 |
| Tel Aviv Aug 12 — 35°C | 48.7¢ | 821.0 | $399.83 |
| Madrid Aug 12 — 38°C | 31.5¢ | 634.0 | $199.71 |
| Milan Aug 11 — 36°C | 65.0¢ | 307.8 | $200.07 |
| Wuhan Aug 12 — 30°C | 40.1¢ | 623.0 | $249.82 |
| Tel Aviv Aug 12 — 34°C | 41.3¢ | 483.9 | $199.85 |
| Mexico City Aug 11 — 24°C | 24.9¢ | 804.0 | $200.20 |
| Ankara Aug 12 — 31°C | 26.4¢ | 568.5 | $150.08 |
| Paris Aug 12 — 35°C | 51.6¢ | 193.8 | $100.00 |
| Amsterdam Aug 12 — 28°C | 50.4¢ | 198.3 | $99.94 |

This is too exact to be an accidental consequence of share counts.

## Practical inference

The wallet likely chooses **dollar notional first**, then calculates shares from price.

A minimal reconstruction should therefore test position size as a discrete function of conviction/edge rather than attempt to infer a continuous Kelly optimizer from the share counts.

Candidate latent tiers from the observed data:

`$100 × {1, 1.5, 2, 2.5, 4, 4.5}`

A simpler production rule could eventually collapse this further if historical PnL does not justify six tiers.

---

# 2. Price regime: this wallet is not primarily buying penny tails

Visible entry-price distribution across the 20-position snapshot:

- median entry price: **49.55¢**;
- mean entry price: **45.02¢**;
- only **1/20** positions below 20¢;
- **5/20** between 20¢ and 40¢;
- **12/20** between 40¢ and 60¢;
- **2/20** at or above 60¢.

Sorted prices:

`18.7, 24.7, 24.9, 26.4, 31.5, 35.0, 40.1, 41.3, 47.3, 48.7, 50.4, 51.6, 52.0, 52.6, 53.0, 55.3, 56.9, 58.0, 65.0, 67.0¢`

This is consistent with **modal/near-modal probability trading**, not a lottery-ticket strategy.

The recovered historical fills support the same pattern:

- Milan June 30 35°C BUY: raw ~29.38¢;
- July 12 unresolved token BUY: raw ~26.56¢;
- Milan June 25 33°C position later SOLD around 10.9¢ after the view deteriorated.

The strongest near-term research band for this wallet is therefore roughly **20–70¢**, with particular attention to 25–60¢.

---

# 3. Horizon structure

At the August 11 snapshot:

- **8/20** visible positions are August 11 same-day contracts;
- **11/20** are August 12 next-day contracts;
- **1/20** is an August 13 contract.

This is strong evidence for a two-horizon engine:

## T+0

Observation-conditioned extrema / certainty collapse.

Primary variables:

- resolver maximum observed so far;
- time remaining before likely temperature peak;
- cloud/radiation/wind/precipitation state;
- remaining ensemble-member maxima;
- next integer resolver boundary.

## T+1

Forecast-distribution edge and model-release repricing.

Primary variables:

- latest local/high-resolution guidance;
- ensemble daily-max distribution at the exact station;
- change from previous model vintage;
- station-specific error distribution;
- market probability surface before and after the update.

T+2 currently appears secondary in this wallet snapshot.

---

# 4. Geographic / contract concentration

Of the 20 visible positions:

- **18** are international whole-degree Celsius exact buckets;
- **2** are US two-degree-Fahrenheit ranges.

The visible international cities include Istanbul, Tel Aviv, Madrid, Milan, Wuhan, Karachi, Munich, Mexico City, Paris, Singapore, Wellington, Amsterdam, Ankara and Shanghai.

This is economically important. International one-degree buckets create a sharper need for:

- exact station targeting;
- local national-model data;
- station-specific calibration;
- precise observation updates;
- correct integer display/resolution behavior.

The supplied wallet therefore looks much more like an **international airport-extrema specialist** than a US-only NWS bot.

---

# 5. Adjacent YES buckets can be rational

The wallet currently owns both:

- Tel Aviv Aug 12 — 35°C YES: ~821 shares at 48.7¢, ~$400 raw entry cost;
- Tel Aviv Aug 12 — 34°C YES: ~483.9 shares at 41.3¢, ~$200 raw entry cost.

Current Polymarket ladder snapshot is approximately:

- 35°C: 50%;
- 34°C: 45–46%;
- 36°C: 5%;
- 33°C: 3–4%;
- other outcomes: near zero.

Market:
https://polymarket.com/event/highest-temperature-in-tel-aviv-on-august-12-2026

Resolver:
NOAA Ben Gurion Airport `LLBG`, whole °C.

## Fee-adjusted portfolio economics

Using the current Weather taker fee formula with rate `r = 0.05`:

`fee_per_share = r * p * (1-p)`

Estimated all-in costs if both positions were taker-filled at their displayed average prices:

- 34°C effective cost/share ≈ **42.51¢**;
- 35°C effective cost/share ≈ **49.95¢**;
- total estimated all-in cost ≈ **$615.80**.

Settlement PnL of the combined position:

- if 35°C wins: about **+$205.20**;
- if 34°C wins: about **-$131.90**;
- if neither wins: about **-$615.80**.

The position is therefore not a symmetric hedge. It is a **primary 35°C forecast plus meaningful secondary mass at 34°C**.

The correct general principle is:

> Mutually exclusive buckets may both be worth buying when each is independently underpriced relative to the trader's calibrated probability distribution.

Buying adjacent buckets is not structurally wrong. Buying them without probability-aware pricing is wrong.

---

# 6. Minimal fee-adjusted signal math

For one YES share at executable ask `a` on a fee-enabled Weather market:

`fee(a) = 0.05 * a * (1-a)`

`all_in_cost(a) = a + fee(a)`

If internal fair settlement probability is `q`:

`EV_per_share = q - all_in_cost(a)`

Trade only the economics implied by this expression; midpoint disagreement is not the signal.

Fee hurdle by price, before spread/slippage:

| Raw price | Fee/share | All-in break-even q |
|---:|---:|---:|
| 10¢ | 0.45¢ | 10.45% |
| 20¢ | 0.80¢ | 20.80% |
| 30¢ | 1.05¢ | 31.05% |
| 40¢ | 1.20¢ | 41.20% |
| 50¢ | 1.25¢ | 51.25% |
| 60¢ | 1.20¢ | 61.20% |
| 70¢ | 1.05¢ | 71.05% |
| 80¢ | 0.80¢ | 80.80% |
| 90¢ | 0.45¢ | 90.45% |

For a dollar allocation `N` at all-in unit cost `c`:

`shares = N / c`

`expected_profit = N * (q/c - 1)`

This is sufficient for ranking candidate buckets by expected dollars.

## Exit economics

For a YES share sold at executable bid `b`:

`net_sale_value = b - 0.05*b*(1-b)`

With current posterior settlement probability `q_new`, a pure value exit exists when:

`net_sale_value > q_new`

For nearly settled winners, include capital-redeployment value:

`sell_now_value = net_sale_value + value_of_redeploying_capital`

versus:

`hold_value ≈ q_new`

The recovered Mexico City July 16 sale at ~99.9¢ five minutes after local midnight is direct evidence that this wallet uses the second comparison.

---

# 7. Current markout evidence from the supplied wallet

Using the profile's displayed average entry and mark price for the 20 visible positions:

- **16/20** have positive markout;
- **4/20** have negative markout;
- aggregate displayed markout is roughly **+$1.06k** on **~$3.40k** raw entry cost.

The profile itself reports about **+$1,018.71 past-day PnL**, broadly consistent with the visible portfolio explaining most of the day's result.

This is not a settlement hit-rate statistic because actively sold positions disappear from the active snapshot. It is useful for something else: the portfolio contains many positions that were entered materially before the market repriced toward them.

Examples:

- Madrid Aug 12 38°C: avg entry 31.5¢; market later around 53–59%;
- Paris Aug 12 35°C: avg entry 51.6¢; later ~63.5%;
- Singapore Aug 12 32°C: avg entry 53¢; later ~64.5%;
- Denver Aug 11 96–97°F: avg entry 55.3¢; later ~64.5%;
- Miami Aug 11 92–93°F: avg entry 67¢; later ~81%.

The most valuable missing field remains **entry timestamp**. Markout combined with minutes-since-forecast-release will reveal whether the edge is forecast quality, release latency, or both.

---

# 8. Live ladder evidence: the wallet is trading concentrated distributions

## Madrid Aug 12

Current ladder snapshot:

- 38°C ≈ 59%;
- 39°C ≈ 38%;
- 40°C ≈ 4%;
- 37°C ≈ 3%;
- others near zero.

Volume: about **$49.9k**.

Resolver: Madrid-Barajas `LEMD`, Wunderground Daily Observations, whole °C.

Wallet entry: 38°C YES at **31.5¢**, ~$200 raw notional.

Market:
https://polymarket.com/event/highest-temperature-in-madrid-on-august-12-2026

The market context now cites official AEMET guidance around 38°C. If the wallet's entry preceded the relevant AEMET/model shift, this is a high-value release-latency case study.

## Wuhan Aug 12

Current ladder snapshot:

- 30°C ≈ 42%;
- 31°C ≈ 23%;
- 29°C ≈ 21%;
- 32°C ≈ 9%;
- other outcomes small.

Volume: about **$21.8k**.

Resolver: Wuhan Tianhe `ZHHH`, Wunderground Daily Observations, whole °C.

Wallet entry: 30°C YES at **40.1¢**, ~$250 raw notional.

Market:
https://polymarket.com/event/highest-temperature-in-wuhan-on-august-12-2026

This is a wider distribution than Tel Aviv or Madrid. The $250 position despite only modest markout is useful for identifying whether the wallet sizes from **forecast confidence/edge at entry** rather than expected short-term markout.

## Tel Aviv Aug 12

Volume: about **$16.4k**.

Distribution concentrated almost entirely in 34°C/35°C.

Wallet raw notional across those two buckets: about **$600**.

This is the clearest current example of event-level conviction being much larger than per-bucket baseline sizing.

---

# 9. Comparison with other profitable temperature specialists

The supplied wallet is not the only evidence that exact-bucket forecasting is monetizable.

## `badatmath.`

Current/recent Polymarket snapshots show:

- roughly 17k predictions;
- around $7.4M WEATHER turnover on an all-time volume snapshot;
- repeated strong weekly/monthly WEATHER PnL snapshots;
- exact YES positions such as Beijing 34°C around 23.8¢, Taipei 37°C around 17.2¢, Wuhan 29°C around 14.8¢, Helsinki 18°C around 13.7¢ and Guangzhou 34°C around 28.7¢ that later repriced strongly or resolved as winners in the indexed profile snapshots.

Profile:
https://polymarket.com/profile/0x8fbd7cf5f806f563080864694415829f7229a959

This trader appears much higher frequency and often enters exact buckets at lower prices than the supplied wallet.

## `meteoblue`

A public profile identified as a meteoblue staff account has shown profitable exact-temperature positions including Tokyo, London, Miami, Seoul, Los Angeles, Toronto and Madrid, with several YES entries in roughly the 10–40¢ range.

Profile:
https://polymarket.com/profile/@meteoblue

This independently supports the idea that professional weather information can be converted into exact-bucket prediction-market profit.

## `WeatherHK2`

This account is more regionally specialized and expresses both YES and NO positions in Hong Kong/China temperature markets.

Profile:
https://polymarket.com/profile/0xdadbf9e1df1b8d7a184a0d6ab9c83b2337b61870

The strategy diversity matters: there is no evidence that only one trade expression works. A strong fair-probability surface can support modal YES, adjacent YES, tail NO, or near-certainty expressions depending on price.

---

# 10. The smallest useful forecasting object

For each city/event, estimate only:

`q_i = P(final resolver daily maximum lands in bucket i | information available now)`

The useful state is:

- resolver station and exact rules;
- latest observations;
- running daily max `M_t`;
- model/ensemble daily maxima at the station;
- historical station/horizon residuals;
- market asks/bids across the full ladder;
- actual information-availability timestamps.

Everything else is secondary until it proves incremental PnL.

## T+1 construction

For each ensemble/model path `m`:

`H_m = max_t T_{m,t}(station)`

Then calibrate the daily-max errors using historical residuals for the same station and lead-time regime.

A deliberately simple calibration is non-parametric:

1. calculate current forecast daily maximum `mu` or ensemble-member maxima;
2. retrieve historical resolver errors `e_k` for comparable horizon/station/season;
3. generate calibrated outcomes `H_k = mu + e_k`, or perturb each ensemble maximum with calibrated residuals;
4. count calibrated outcomes inside each exact resolver bucket;
5. normalize to a probability vector.

This is simpler and more defensible than choosing a hand-set Gaussian sigma.

## T+0 construction

Let:

`M_t = maximum authoritative observation already seen today`

`R_t = maximum temperature over the remaining future path`

Then:

`H = max(M_t, R_t)`

Once `M_t` has crossed a bucket boundary, all lower outcomes become zero-probability mechanically.

Near the daily peak, the economically important question is often only:

> What is the probability that the resolver crosses the next integer boundary before the day is over?

That can be much easier to estimate than the original full-day maximum distribution.

---

# 11. Minimal event-level selection rule implied by the evidence

For every bucket `i`:

1. calculate calibrated `q_i`;
2. obtain executable ask `a_i`;
3. calculate `c_i = a_i + 0.05*a_i*(1-a_i)` plus measured slippage;
4. calculate `edge_i = q_i - c_i`;
5. calculate expected dollars at candidate round-dollar tier;
6. rank all positive-EV expressions across all cities;
7. allocate only to the best current opportunities.

Adjacent buckets can both be selected if both have positive `edge_i`.

The current wallet evidence suggests testing **round-dollar notional tiers** before introducing any sophisticated sizing optimizer.

The natural research mapping is:

- baseline edge → ~$100;
- stronger edge/confidence → ~$150–250;
- exceptional event-level conviction → ~$400–450+.

The exact tier thresholds should come from reconstructed wallet/history PnL and our own forecast-vs-price evidence, not from aesthetic risk percentages.

---

# 12. Minimal exit rule implied by observed behavior

The recovered Milan June 25 33°C sale shows the supplied wallet reduces a bucket that later loses.

Therefore a useful bot should continuously recompute `q_i`, not freeze the entry forecast.

Minimal exit comparison:

`hold_value = q_i_new`

`sell_value = bid_i - sell_fee_i`

Sell when executable sell value dominates the updated forecast value, or when redeployment makes the opportunity cost of holding larger than the remaining expected gain.

This is likely enough. A separate elaborate stop-loss framework is not required to express the economics.

---

# 13. Data acquisition that directly supports this logic

The final research dataset needs only a few compact tables.

## Market table

`event_id, city, date, station, source, timezone, unit, bucket, token_id, neg_risk_group, fee_enabled`

## Trade/price table

`timestamp, token_id, bid, ask, last_price, trade_price, trade_size, wallet, side, fee`

## Observation table

`availability_timestamp, observation_timestamp, station, temperature, running_max`

## Forecast table

`availability_timestamp, model, run_time, station, valid_time, member, temperature`

## Settlement table

`event_id, final_resolver_max, winning_bucket`

## Wallet table

`timestamp, wallet, event_id, bucket, side, price, shares, dollars, fee, realized_pnl`

These tables are sufficient to reconstruct the key alpha tests without a broader data platform.

---

# 14. Highest-value empirical tests from here

## A. Supplied wallet position-size function

Recover full closed positions and fills, then regress / bucket position dollars against:

- entry price;
- horizon;
- city;
- realized edge over market;
- short-term markout;
- whether multiple adjacent buckets were bought;
- recent forecast revision magnitude.

Goal: determine whether the visible $100/$150/$200/$250/$400/$450 tiers correspond to edge/confidence bands.

## B. Entry-after-release timing

For each T+1 fill:

`delay = fill_time - first_availability_time_of_new_forecast`

Measure markout versus delay.

This directly answers whether speed around specific model releases is profitable.

## C. T+0 boundary-crossing edge

At every same-day fill, reconstruct:

- running resolver max;
- distance to next integer boundary;
- remaining forecast heating potential;
- time to expected peak;
- market probability before/after next official observation.

This should identify when probability collapses faster than the market.

## D. Full-ladder calibration

For historical events, compare:

- raw market probability;
- calibrated weather probability;
- combined weather+market model if useful;
- final resolver outcome.

Rank by **fee-adjusted dollar return**, not forecast MAE.

## E. Specialist consensus

For supplied wallet, badatmath., meteoblue, Poligarch and other proven daily-temperature specialists, normalize fills into the same event/bucket probability surface.

Test whether multiple specialists entering the same bucket before repricing predicts additional markout beyond weather and market price alone.

---

# Bottom line

The data now supports a much smaller and more specific eventual trading logic than a generic "weather bot":

> **Build a calibrated probability vector for the exact resolver's daily maximum, compare every bucket to executable fee-adjusted prices, allocate simple round-dollar conviction tiers to the strongest positive-EV expressions, recompute after every important forecast/observation update, exit probability collapses, and recycle locked winners.**

The supplied wallet's current portfolio, recovered historical fills, active exits and round-dollar sizing all fit this model.

The next research value comes from filling the missing timestamps and historical probability states, not adding more architecture.