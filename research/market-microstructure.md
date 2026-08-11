# Polymarket weather microstructure

Snapshot: **2026-08-11**

Weather alpha is monetized through a central limit order book. Forecast quality and execution quality therefore multiply each other: the same correct probability can produce excellent PnL, mediocre PnL or negative PnL depending on price, fee, depth, fill timing and adverse selection.

The economic object is:

`expected net dollars = Σ fills × (fair settlement value - effective fill cost)`

not `forecast probability - displayed Polymarket percentage`.

---

# 1. Displayed price versus tradable price

Polymarket documents the displayed probability as normally the midpoint of best bid and best ask. When the spread exceeds $0.10, the UI can display the last traded price instead.

Therefore collect independently:

- best bid;
- best ask;
- depth at every level;
- last trade;
- displayed midpoint only for UI comparison.

For a buy, the immediate executable price is the ask. For a sell, it is the bid.

Source:
https://docs.polymarket.com/concepts/prices-orderbook

## Effective probability surface

For each outcome `i`, maintain:

- `bid_i`;
- `ask_i`;
- `mid_i`;
- spread;
- cumulative depth at 1¢/2¢/5¢ from top;
- last trade and age;
- recent signed flow;
- fee-enabled state.

This lets the strategy distinguish a real 8-point edge at 52¢ ask from a fake 8-point edge against a stale 48¢ last trade.

---

# 2. Current Weather fee curve

Polymarket currently lists fee-enabled Weather contracts at taker rate `0.05` and maker rate `0`.

Per-share taker fee:

`f(p) = 0.05 * p * (1-p)`

For a YES bought at ask `a` and held to settlement:

`EV/share = q - a - f(a)`.

Break-even fair probability:

`q_BE = a + f(a)`.

Examples:

| Ask | Fee/share | Fair probability needed to break even |
|---:|---:|---:|
| 0.05 | 0.002375 | 0.052375 |
| 0.10 | 0.004500 | 0.104500 |
| 0.20 | 0.008000 | 0.208000 |
| 0.30 | 0.010500 | 0.310500 |
| 0.40 | 0.012000 | 0.412000 |
| 0.50 | 0.012500 | 0.512500 |
| 0.60 | 0.012000 | 0.612000 |
| 0.80 | 0.008000 | 0.808000 |
| 0.95 | 0.002375 | 0.952375 |

The fee is largest in absolute cents near 50¢ and largest relative to token cost in cheap tails.

Fee schedule source:
https://docs.polymarket.com/trading/fees

Fee applicability is market-specific and should be read from market/CLOB metadata rather than inferred only from category name.

---

# 3. Maker economics

Polymarket currently allocates **25% of collected Weather taker fees** to the maker-rebate pool. Makers pay zero platform trading fee.

That means a maker order can earn from three components:

1. better entry price than crossing the spread;
2. eventual movement from price to fair value;
3. maker rebate.

But filled maker orders are selected by other traders, so expected adverse-selection markout matters.

For a maker buy at `b`:

`EV_filled = q - b + expected_rebate - expected_adverse_selection`.

At opportunity level:

`EV = P(fill) * EV_filled - P(no_fill) * missed_opportunity_cost`.

Source:
https://docs.polymarket.com/market-makers/maker-rebates

## Forecast-aware quote policy

A compact informed maker policy:

- fair value `q` from resolver model;
- quote bid below `q - required_margin`;
- quote ask above `q + required_margin` when inventory exists;
- tighten when spread is wide and information state is quiet;
- reprice immediately after forecast/observation shocks;
- skew inventory toward outcomes with positive weather residual;
- cross only when information half-life is shorter than likely passive fill time.

The best execution mode is therefore signal-specific rather than globally “maker” or “taker.”

---

# 4. Temperature ladders are one event, not independent binaries

If an event has `K` mutually exclusive temperature buckets:

`Σ_i q_i = 1`.

Every quoted binary book should be interpreted as one slice of that joint surface.

Weather information often shifts probability mass locally:

Example: a forecast revision from 31.2°C to 32.0°C may:

- sharply lower 30°C;
- lower 31°C;
- raise 32°C;
- moderately raise 33°C;
- barely affect distant tails.

Trading each outcome independently discards these conservation relationships.

## Coherent market surface

Take a price vector based on executable quotes or spread-aware mids and project it to the probability simplex.

Weighted least-squares projection:

`q_hat = argmin Σ_i w_i(q_i-p_i)^2`

subject to:

- `q_i >= 0`;
- `Σ q_i = 1`.

Weights can be inverse spread or depth-based.

Then calculate local residuals:

`residual_i = q_weather_i - q_market_coherent_i`.

This is cleaner than comparing one model bucket to one noisy binary midpoint.

---

# 5. Negative-risk conversions

Polymarket negative-risk mechanics allow a NO share in one outcome to convert into YES shares in every other outcome in the same event.

Economic identity:

`NO_i ≡ Σ_{j≠i} YES_j`.

At fair probability:

`1 - q_i = Σ_{j≠i} q_j`.

At market prices, continuously compare:

- best executable NO_i expression;
- executable basket of all other YES outcomes;
- mint/merge/convert routes when applicable;
- depth-limited basket cost;
- fees and gas/operational costs if any.

Source:
https://docs.polymarket.com/advanced/neg-risk

## Forecast-informed relative value

Pure arbitrage may disappear quickly. More durable relative value can remain when the ladder is coherent in aggregate but probability mass is placed on the wrong neighboring bucket.

Example:

- market: 31°C 35%, 32°C 40%, 33°C 20%, others 5%;
- resolver model after observation shock: 31°C 10%, 32°C 68%, 33°C 20%, others 2%.

The best trade may be long 32°C versus short/fade 31°C rather than a naked long versus cash.

---

# 6. Order-book response to weather information

Every forecast/observation update produces two timelines:

1. fair-value movement;
2. market-price movement.

Record around each event:

- `t_source_created` — nominal model/observation timestamp;
- `t_source_available` — first time our collector could retrieve it;
- `t_model_parsed` — fair value updated;
- `t_order_sent`;
- `t_fill`;
- order-book snapshots before/after.

Then estimate price response at:

- 1 second;
- 5 seconds;
- 10 seconds;
- 30 seconds;
- 1 minute;
- 5 minutes;
- 30 minutes.

## Information half-life

If fair-value shock is `Δq` and market move by lag `τ` is `Δp(τ)`:

`capture_ratio(τ)=Δp(τ)/Δq`.

Estimate the time until 50% and 80% of the forecast shock is reflected.

This tells us whether a data source belongs to:

- normal polling;
- WebSocket + immediate execution;
- direct source push/stream;
- low-latency colocated execution.

---

# 7. Latency economics and server geography

Polymarket documents its primary CLOB servers in AWS `eu-west-2` (London), and notes direct co-location possibilities for approved professional market makers; `eu-west-1` is the closest unrestricted AWS region it recommends for latency-sensitive infrastructure.

Source:
https://docs.polymarket.com/market-makers/latency

This only matters when measured information half-life justifies it.

Potential weather-latency hierarchy:

1. data-source availability dominates when source lag is minutes/hours;
2. parser/model computation dominates if probability update is slow;
3. network/order latency dominates only when other participants consume the same feed almost instantly.

For global city weather, the first category may be much more important than microseconds.

---

# 8. Fill probability and queue economics

A maker order's expected value is incomplete without fill probability.

Features that can predict fill:

- distance from best bid/ask;
- queue position proxy;
- recent trade intensity;
- signed order flow;
- spread;
- time to resolution;
- fair-value distance;
- forecast-update schedule;
- bucket centrality;
- market volume regime.

Track maker quote episodes with:

- posted price/size;
- top-of-book when posted;
- fill fraction;
- time to first fill;
- time to complete fill;
- markout 10s/1m/5m after each fill;
- eventual settlement PnL;
- rebate earned.

The useful statistic is **net dollars per posted dollar-second or per unit of capital**, not fill rate by itself.

---

# 9. Taker depth and marginal sizing

Suppose asks are `(p_1,s_1),...,(p_n,s_n)` ascending.

For each level:

`marginal_EV_k = q - p_k - f(p_k)`.

Consume book depth while marginal expected dollars justify the capital versus alternative opportunities.

Total expected PnL for size `S`:

`EV(S) = Σ_k fill_k(S) * marginal_EV_k`.

This produces a natural signal capacity curve:

- first $100 may have 8¢/share edge;
- next $500 may have 4¢;
- next $2,000 may have 0.5¢;
- further size may be inferior to another city.

Rank capital globally by marginal expected return rather than giving every signal a fixed cap.

---

# 10. Cross-city correlation and shared weather regimes

Daily markets are not independent when cities share synoptic systems or the same forecast-model error.

Examples:

- NYC/Philadelphia/other Northeast cities;
- European heatwave cities;
- East Asian monsoon/heat regimes;
- multiple contracts driven by one tropical cyclone.

Correlation matters economically because one forecast error can affect many positions simultaneously.

Estimate historical residual correlation by:

- resolver error;
- model revision;
- final bucket outcome residual;
- trade PnL.

Capital can then be assigned to the portfolio with highest expected compound growth or expected dollars under the actual correlation matrix.

---

# 11. Late-resolution certainty trades

As a physical weather outcome becomes effectively fixed, fair probability can approach 1 while market ask remains below 1 because of:

- stale orders;
- source uncertainty;
- capital lock until resolution;
- participants exiting early;
- disagreement over resolver mechanics.

For a near-certain outcome at ask `a`:

`annualization` is less relevant than absolute expected dollars per day of capital lock.

Define:

`capital_efficiency = expected_profit / (cash_cost * expected_days_locked)`.

This permits comparison against other same-day opportunities.

Resolver-source knowledge is most valuable here because small uncertainty about the official final value dominates weather-model uncertainty.

---

# 12. Market-making versus directional-trading decision rule

For every forecast signal compute two estimates:

### Cross now

`EV_cross = size_cross * (q - effective_ask - fee - impact)`

### Post maker

`EV_maker = P(fill before edge decay) * size_maker * (q - quote + rebate - adverse_selection)`

Choose the higher expected dollars after considering the information half-life.

The result may vary by state:

- **fresh large forecast shock** → cross;
- **slow convergence, wide spread** → make;
- **near resolution, stale opposing quote** → cross aggressively;
- **uncertain fair value, rich spread** → quote only at substantial margin.

---

# 13. Microstructure research table

For every opportunity store:

- event/outcome/token;
- resolver city/date/family;
- fair probability before/after information shock;
- bid/ask/depth before/after;
- fee rate;
- taker EV by depth level;
- hypothetical maker quote EV;
- actual fill(s);
- 10s/1m/5m/30m markouts;
- rebate;
- settlement PnL;
- capital lock time.

This table connects meteorological alpha directly to realized execution economics.
