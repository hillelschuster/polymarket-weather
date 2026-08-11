# Edge thesis — where the money can come from

Snapshot: **2026-08-11**

The project starts from a favorable prior: weather markets contain repeatable, executable inefficiencies. The useful question is **which mechanism creates the most net dollars per unit of capital and attention**.

Each edge below is described by:

- **mechanism** — why the mispricing exists;
- **persistence** — why competition may not erase it immediately;
- **signal** — what we calculate;
- **monetization** — how the edge turns into PnL;
- **capacity** — where the dollars can scale;
- **decay** — what makes the edge weaker.

## 1. Same-day certainty-collapse edge

### Mechanism

A daily high is a running maximum. At time `t`:

`H = max(M_t, R_t)`

where `M_t` is the maximum already observed and `R_t` is the highest remaining temperature.

Once `M_t` enters a bucket, lower buckets become impossible. After the likely peak, the only important uncertainty is whether the station crosses the next resolver boundary. That probability can collapse rapidly after each observation.

A daily low has the symmetric structure:

`L = min(m_t, Rmin_t)`.

### Persistence

Many traders and public bots use a daily point forecast or generic weather app. Those inputs update less intelligently than a state-conditioned resolver model. International cities also have heterogeneous station/source conventions that increase the advantage of specialized plumbing.

### Signal

For every resolver bucket `i`:

`q_i(t) = P(bucket(H) = i | station observations through t, remaining forecast paths)`.

Condition each remaining model path on the model's observed error at the exact station, then map every member's final maximum through the exact resolver rounding function.

### Monetization

- buy the exact locked/modal bucket when `q_i - ask_i - fee_i` is positive;
- sell/fade neighboring buckets whose residual probability has collapsed;
- quote maker liquidity around the updated probability before stale orders reprice.

### Capacity

Daily temperature markets can reach tens or hundreds of thousands of dollars in volume. The strategy recurs across many cities every day, creating high turnover and diversification.

### Decay

The edge narrows as other participants consume the same station feed. Better conditioning, faster feed access and less-followed cities preserve the advantage.

**Current rank: #1.**

---

## 2. T+1 station-calibrated modal-bucket forecasting

### Mechanism

Public implementations often transform one deterministic daily maximum into a bucket or count raw ensemble members. The economically correct target is the distribution of the **resolver-station daily maximum**.

For model member `m` with hourly path `T_m(h)`:

`H_m = max_h T_m(h)`.

The distribution of `{H_m}` is then corrected for station/model/lead/cycle biases and residual dispersion before bucketization.

### Persistence

Weather forecast skill is heterogeneous by station, weather regime and lead time. A universal Gaussian/Laplace sigma or Open-Meteo “best match” forecast leaves information on the table. Global Polymarket coverage creates many stations that receive little bespoke calibration from traders.

### Signal

`q_i = P(g(H) in bucket_i | model vintages, calibrated residuals, local predictors)`

where `g` reproduces the resolver measurement/rounding convention.

Blend models by out-of-sample probability skill rather than generic reputation. Useful features include:

- cycle and lead time;
- station/model rolling bias;
- ensemble spread;
- cloud, wind, humidity, boundary-layer depth and advection regime;
- forecast disagreement;
- previous-cycle revision;
- climatological local forecast-error shape.

### Monetization

Concentrate on the modal bucket and high-EV adjacent outcomes rather than spreading across many YES contracts. Use maker orders where the taker fee consumes a material share of the edge.

### Capacity

Broad daily global market inventory. Highest capacity in established cities such as NYC, London, Paris, Hong Kong, Seoul and Beijing; potential higher percentage edge in less-followed cities.

### Decay

Generic model improvements reduce raw forecast error; station calibration and timing remain differentiators.

**Current rank: #2.**

---

## 3. Forecast-vintage repricing latency

### Mechanism

Weather information arrives in discrete shocks:

- ECMWF/GFS/ICON model cycles;
- NBM updates;
- LAMP/MOS guidance;
- METAR/SPECI and official station reports;
- national-agency observations;
- tropical cyclone advisories;
- climate/reanalysis updates.

The market may reprice with a delay after the new information becomes available.

### Signal

For each new data vintage:

`shock_i = q_i(new vintage) - q_i(previous vintage)`.

Align `shock_i` to the first realistically accessible timestamp and compare against CLOB bid/ask evolution at 1s, 10s, 1m, 5m, 30m and 2h horizons.

### Persistence

Weather markets are geographically fragmented. A new Tokyo, Ankara or Wuhan forecast may receive much less instantaneous trading attention than a major sports line or BTC market.

### Monetization

- cross immediately when the expected price response exceeds fee + spread + impact;
- post inside stale books when latency is long enough for maker fills;
- prioritize revisions that move probability across narrow bucket boundaries.

### Capacity

Depends on depth during update windows. A large forecast shock can move several neighboring buckets simultaneously.

### Decay

Latency-sensitive and competitive. Direct feeds, WebSocket books and proximity to Polymarket's matching infrastructure improve capture.

**Current rank: #3.**

---

## 4. Resolver/source lead edge

### Mechanism

The market can reference a public website whose displayed value originates from an upstream observation network. The upstream value may be available earlier or at higher precision.

Examples:

- Wunderground Daily Observations often mirrors airport observations;
- Tel Aviv current rules use NOAA WRH LLBG data directly;
- Hong Kong can resolve from HKO Daily Extract data;
- US ASOS daily extrema involve measurement/rounding details that generic METAR parsers can mishandle.

### Signal

Estimate the eventual resolver-displayed value from the earliest authoritative/raw observation stream.

### Persistence

Source heterogeneity creates implementation cost. Many bots hard-code a city coordinate and a generic API instead of parsing rules and resolver semantics per event.

### Monetization

The largest payoff occurs near resolution when the physical outcome is effectively known but market prices remain below certainty.

### Capacity

Potentially high on heavily traded same-day buckets because uncertainty collapses while traders still exchange positions.

### Decay

Depends on how quickly Polymarket participants discover and automate the same upstream source.

**Current rank: #4, tightly connected to #1.**

---

## 5. Profitable-wallet information factor

### Mechanism

Specialist traders can encode private model choices, faster source access, local expertise or execution skill. Their fills are public data.

### Signal family

For wallet `w`, outcome `i`, time `t`:

- signed net flow;
- entry price;
- size relative to wallet history;
- city/horizon specialization;
- trade timing relative to model/observation releases;
- 30m/2h/close markout;
- realized PnL by contract type;
- consensus across independent profitable wallets.

A useful meta-feature is:

`wallet_signal_i(t) = Σ_w skill_weight_w(segment) * signed_flow_w,i(t)`.

Weights belong to segments: a wallet can be excellent on daily highs and irrelevant on climate markets.

### Persistence

The public market reveals fills, not the trader's underlying model. Following flow can therefore inherit information without reproducing the full research process, provided latency and price impact remain favorable.

### Monetization

Use wallet flow as an incremental feature alongside weather probability and market price. The highest-value test is whether specialist flow predicts settlement or near-term price movement **after controlling for current price and weather state**.

### Capacity

Scales with wallet opportunity set; especially useful as a ranking layer across many simultaneous cities.

### Decay

Copying after large visible fills can lose edge through price movement. Fast ingestion and agreement among several specialists improve value.

**Current rank: #5.**

---

## 6. Informed market making

### Mechanism

Weather currently has a 0 maker fee and a 25% maker-rebate allocation on fee-enabled markets, while takers pay the weather fee curve. Wide multi-outcome books can therefore reward a trader who knows fair value well enough to quote selectively.

### Signal

For candidate maker price `p_m`:

`EV_filled = q - p_m + expected_rebate_per_share - expected_adverse_selection_markout`

Expected dollars also multiply by fill probability.

Quote around a state-conditioned fair value and reprice when forecasts/observations move.

### Persistence

Most forecast bots focus on directional taker entries. Weather information can improve both side selection and stale-quote avoidance.

### Monetization

- capture spread;
- collect rebate share;
- accumulate favorable inventory before convergence;
- cross only for especially time-sensitive shocks.

### Capacity

Potentially larger than pure taker signals because repeated small fills monetize the same model continuously.

### Decay

Adverse selection increases around scheduled model releases and decisive observations. Quote freshness determines economics.

**Current rank: #6.**

---

## 7. Full-ladder / negative-risk relative value

### Mechanism

Only one temperature bucket wins, so coherent probabilities sum to one. Negative-risk conversion economically links one outcome's NO token to the YES basket of all other outcomes.

### Signal

Construct an arbitrage-consistent surface and compare:

- each YES bid/ask to weather fair value;
- `NO_i` to the basket `Σ_{j≠i} YES_j`;
- aggregate YES basket cost/revenue;
- nearest-simplex projection of quoted probabilities;
- depth-weighted relative distortions.

### Persistence

Separate binary books can move asynchronously when the forecast shifts. The full event may momentarily contain inconsistencies even when each individual quote looks plausible.

### Monetization

Capture pure structural discrepancies where available, then use weather forecasts to choose the direction of relative-value discrepancies that remain after costs.

### Capacity

Constrained by the shallowest leg of a basket. Repeated across every multi-outcome event.

### Decay

Mechanical arbitrage is highly automatable; forecast-informed relative value has greater durability.

**Current rank: #7.**

---

## 8. Market-residual learning / crowd-as-feature

### Mechanism

The crowd contains information that weather models omit. Conversely, weather models contain information the crowd underweights. The best probability can combine both.

### Signal

Examples:

`logit(q*) = a_segment + b_segment logit(q_weather) + c_segment logit(q_market) + dX`

or a regularized probability pool with weights learned point-in-time.

Segment by city, horizon and time-of-day. Add wallet flow and microstructure only when they improve out-of-sample probability/PnL.

### Monetization

Trade the residual `q* - executable_price`, which directly measures incremental informational advantage over the existing market.

### Persistence

Market efficiency varies across segments. Learning the segment-specific weight of crowd versus weather prevents overconfident trades where the market is genuinely more informed.

**Current rank: #8 as a meta-model feeding other strategies.**

---

## 9. GISTEMP monthly climate nowcast

### Mechanism

Polymarket trades narrow 0.05°C GISTEMP anomaly buckets. NASA's monthly GISTEMP result is released on a scheduled date roughly ten days into the following month. Other global datasets and reanalyses become available earlier.

ERA5T is updated roughly five days behind real time, with monthly means roughly five days after month-end. NASA GISTEMP uses GHCN v4 land-station data and ERSST v5 sea-surface data.

### Signal

Learn a historical mapping:

`GISTEMP_month = f(ERA5/ERA5T, Berkeley Earth, NOAA, ERSST, partial GHCN, season, ENSO, data coverage)`.

More directly, reproduce as much of the GISTEMP pipeline as practical from early inputs and model the residual between proxy datasets and final published GISTEMP.

### Persistence

The contract resolves on one specific index, while many traders reason from generic “global temperature.” Dataset-specific basis is the edge.

### Monetization

As the month completes and preliminary/reanalysis information arrives, buy the narrow GISTEMP bucket whose calibrated probability exceeds price. The known NASA release schedule creates a precise information timeline.

### Capacity

Potentially much larger than small-city daily contracts; weather leaderboard winners have historically made large profits in global/climate markets.

### Decay

Basis-model accuracy and early data latency determine the advantage.

**Current rank: #9 now, with potential to move much higher after capacity analysis.**

---

## 10. Monthly cumulative precipitation

### Mechanism

Monthly precipitation is an accumulating state:

`P_final = P_observed(t) + P_remaining(t)`.

Observed rainfall cannot disappear. As the month advances, the forecastable remaining distribution becomes a smaller part of the total.

### Signal

Combine exact resolver precipitation-to-date with ensemble precipitation totals for the remaining month. Calibrate the highly skewed precipitation distribution and account for source measurement conventions.

### Monetization

Trade bucket transitions following major rain events and late-month certainty collapse.

### Capacity

Current monthly precipitation markets are new and can be thin, making them potentially high percentage-edge but initially smaller dollar opportunities.

**Current rank: #10 with high structural interest.**

---

## 11. Monthly wind-maximum / event-driven extrema

### Mechanism

Monthly maximum wind is another running maximum:

`W_final = max(W_observed(t), W_remaining(t))`.

For Mt. Washington, tropical cyclones, fronts and strong pressure-gradient events dominate tail probabilities.

### Signal

Blend observed maximum-to-date with ensemble maximum-gust distributions conditioned on synoptic events and tropical cyclone tracks.

### Monetization

Threshold markets allow direct trading of exceedance probabilities. A major storm forecast can reprice several nested thresholds at once.

### Capacity

Current August market is small, while prior July volume reached tens of thousands, so capacity may be episodic.

**Current rank: #11.**

---

## Meta-ranking formula

For research prioritization, score each strategy approximately by:

`ResearchValue ≈ expected_net_edge × executable_capacity × opportunity_frequency × persistence × measurement_speed`

For deployment economics, rank by:

`ExpectedNetPnL/day = Σ opportunities E[filled_size × per_share_net_EV] - financing/operational drag`

This keeps the project pointed at dollars rather than abstract forecast accuracy.
