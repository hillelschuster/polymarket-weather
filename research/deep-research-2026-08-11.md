# Deep research pass — 2026-08-11

## One objective

**Make money from forecastable weather outcomes on Polymarket.**

This second pass goes beyond “find a better forecast.” The strongest opportunity appears to be a stack of **resolver science + probabilistic weather + information timing + informed-trader flow + execution**.

The central question is:

> What part of the settlement outcome becomes knowable before the marginal Polymarket trader or bot updates its price, and how many executable dollars can we put through that information gap?

---

# 1. The opportunity is real and specialist-driven

Polymarket's current all-time WEATHER leaderboard shows several traders with six-figure category profits and high-volume accounts above $10M of weather turnover.

This matters more after looking at 2026 prediction-market research.

Recent studies using broad Polymarket transaction data report that prediction accuracy/profits are concentrated among a small minority of skilled traders rather than evenly distributed crowd wisdom. One 2026 paper estimates roughly 3% of accounts are persistently skilled, reacting to public information, removing law-of-one-price violations and trading against behavioral mistakes. Another Polymarket microstructure dataset paper finds that high-spread niche markets attract informed specialists rather than merely noise traders.

Research links:
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6617059
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6870538
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6933527

**Inference for weather:** a niche, fragmented, data-rich category is exactly where specialist skill can matter. We should expect competition from other specialists, but also expect public wallet behavior to contain information.

---

# 2. The supplied wallet changes the working hypothesis

The user-supplied account:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

is visibly holding many exact-bucket YES positions across global city temperature markets.

On the August 11 snapshot, several same-day positions bought around mid-range probabilities had already repriced close to $1:

- Istanbul 27°C: avg ~52.6¢ → ~100¢;
- Tel Aviv 35°C: ~56.9¢ → ~100¢;
- Milan 36°C: ~65¢ → ~100¢;
- Karachi 32°C: ~47.3¢ → ~100¢;
- Munich 31°C: ~52¢ → ~99.9¢.

It also held next-day modal buckets in Madrid, Tel Aviv, Wuhan, Paris, Singapore and others.

This is inconsistent with a simplistic thesis that profitable weather trading is primarily “buy NO against overpriced longshots.”

A more plausible family is:

### Strategy A — same-day modal certainty

Buy the exact bucket once current station observations plus remaining weather path make it substantially more likely than market price.

### Strategy B — next-day concentrated mode

Buy one exact forecast mode when multi-model/resolver calibration is sharper than the market distribution.

### Strategy C — forecast-release timing

Do A/B immediately after model/observation updates, before the market fully reprices.

The fill timestamps will identify which mechanism dominates.

Profile:
https://polymarket.com/@0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f-1774968947489

---

# 3. Same-day extrema are a path-conditioning problem

Public bots tend to treat a daily high as a point forecast plus uncertainty. That misses the most valuable state transition.

At time `t`:

`H = max(M_t, R_t)`

where:

- `M_t` = maximum already observed at resolver station;
- `R_t` = maximum over all remaining times in the local day.

If `M_t` has already reached 31.2°C and the resolver rounds to whole °C, all buckets materially below 31°C are already dead. The only economically relevant question may be:

`P(temperature reaches the 31→32 resolver boundary before the day ends)`.

As the solar peak passes, this probability can collapse nonlinearly.

## Better member conditioning

For member/model `m`:

`e_m(t) = observation(t) - model_m(t)`.

Correct future path:

`T*_m(h) = T_m(h) + station_bias + alpha(h-t)*e_m(t)`.

Then:

`H_m(t) = max(M_t, max_{h>t} T*_m(h))`.

Residual-dress each member with historical station/lead/regime errors and map through the exact contract rounding rule.

This produces one coherent bucket distribution.

### Novel edge variable: boundary survival probability

For each adjacent upper boundary `u`:

`S_u(t) = P(max remaining temperature < u | current information)`.

Near peak time, the derivative:

`dS_u/dt`

can be large. A market priced from a stale daily forecast can lag this physical certainty collapse.

The strategy should rank states where model probability is changing fastest **without equivalent price movement**.

---

# 4. The exact resolver can be a bigger edge than another forecast model

Public bot evidence is unusually clear here.

`jattree/weather-edge` initially reported a catastrophic live run, but its later audit found the strategy was trading through multiple wrong plumbing layers:

- gridded reanalysis instead of the actual resolver feed;
- wrong stations in Denver/Houston/Hong Kong;
- Fahrenheit bucket integration error;
- mutually exclusive buckets treated badly in execution/accounting.

The later review explicitly concluded that the underlying forecast alpha was **not cleanly measured**.

Repository:
https://github.com/jattree/weather-edge

Meanwhile, BallesJr reports 93% exact-station IEM agreement with historical market outcomes versus 66% for ERA5 grid on 500+ historical trades.

Repository:
https://github.com/BallesJr/polymarket-weather-edge

Those numbers are author-reported, but the mechanism is physically obvious: airport/local-station temperatures differ from a reanalysis grid, and Polymarket bins are narrow.

### Deep implication

Instead of viewing resolver mapping as boring plumbing, view it as a **basis model**:

`resolver_value = physical/model value + station/source basis + publication residual`.

A trader can profit by forecasting all three terms better than the market.

---

# 5. US Fahrenheit markets may have a hidden measurement-process edge

US ASOS temperature processing is subtle enough to matter at Polymarket bucket width.

Iowa Environmental Mesonet documents that routine METAR temperature precision and official/extrema reconstruction are not identical. Higher-precision T-groups, six-hour max/min groups and daily summary products can contain information missed by a simple stream of rounded routine METAR temperatures.

That creates a late-day probability model with two sources of uncertainty:

1. will the physical temperature exceed the next boundary?
2. will the official/resolver measurement process represent the maximum in the expected Fahrenheit bucket?

Instead of treating station observation as exact truth:

`H_resolver = H_physical + eta_measurement/publication`.

Estimate `eta` historically from exact resolver/source comparisons.

This can be a niche edge specifically in 2°F US markets.

---

# 6. US short-range data is much richer than most public bots use

## LAMP

Current NOAA LAMP v2.7:

- station-specific;
- uses latest station observations plus model/MOS information;
- updates hourly for temperature;
- nominal cycles HH:30 UTC;
- forecasts hourly out to 38h.

That is almost tailor-made for airport T+0/T+1 markets.

## NBM v5.0

NBM v5.0 became operational May 5, 2026. It is explicitly calibrated and blends large numbers of NWS/non-NWS model inputs. Current availability is frequent, with many cycles around HH:30–40.

It provides probabilistic extrema products and can serve as:

- a strong baseline probability distribution;
- a feature/source in our blend;
- a discrete information-release event.

## Strategy idea: LAMP–NBM disagreement

When LAMP, using recent station observations, shifts the expected peak but broader NBM/extrema distribution has not yet fully followed, the disagreement can signal a fast local change.

Feature:

`local_update_residual = q_LAMP_conditioned - q_NBM`.

If Polymarket price resembles the older/broader NBM state, LAMP may offer a short-lived edge.

Official:
- https://vlab.noaa.gov/web/mdl/lamp
- https://vlab.noaa.gov/web/mdl/nbm

---

# 7. International cities may offer a larger attention/data asymmetry

The supplied wallet trades Wuhan, Karachi, Ankara, Tel Aviv, Wellington, Shanghai and other markets that receive far less generic trading attention than NYC/London.

Public GitHub bots often:

- hard-code a small city list;
- use Open-Meteo globally;
- use a generic city coordinate;
- apply one uncertainty formula everywhere.

But national agencies expose highly specific data:

- JMA MSM: 5 km, every 3 hours for Japan;
- DWD ICON-D2/D2-EPS: high-resolution frequent European guidance;
- Met Office UK/MOGREPS: frequent London/UK local runs with explicit availability windows;
- ECCC HRDPS: ~2.5 km Canadian guidance useful for Toronto;
- HKO: direct running max/min observations and local post-processing;
- KMA: direct Korean ASOS/AWS and model data.

### Strong specialization thesis

Build a source map per city and ask:

`incremental resolver skill of local source versus popular aggregator`.

The best city may not have the easiest weather. It may have the largest gap between **our data quality** and **market participant data quality**.

---

# 8. Direct-source versus aggregator latency may be causal alpha

Forecast websites and aggregators add a layer between the model producer and the trader.

For source/model `s`:

`lead_s = time aggregator reflects new run - time direct model becomes available`.

If public bots poll an aggregator every 15–30 minutes while direct data appears earlier, the edge can persist even if everyone uses the same underlying ECMWF/GFS model.

This is particularly testable for:

- ECMWF direct open data versus Open-Meteo ECMWF exposure;
- Met Office Weather DataHub versus generic London forecasts;
- JMA direct MSM versus generic Tokyo forecast pages;
- KMA/HKO direct data versus airport/global aggregation.

The experiment is simple: timestamp both and measure Polymarket response.

---

# 9. Forecast update schedules form a global trading calendar

Current official schedules produce repeated predictable information windows.

### LAMP

Hourly HH:30.

### NBM

Frequent hourly cycles; current v5.0 text product windows documented around HH:30–40 for many cycles.

### ECMWF

Four global cycles/day. Current dissemination starts roughly:

- 05:45 UTC for 00 run;
- 11:45 for 06;
- 17:45 for 12;
- 23:45 for 18,

with ensemble/product batches following.

### Met Office

Frequent UK model cycles and MOGREPS updates throughout the day; Weather DataHub publishes expected availability windows.

### JMA MSM

Every three hours.

### DWD ICON-D2

Frequent European cycles.

This gives the future system a **forecast catalyst calendar** just like an economic trader has CPI/FOMC releases.

Instead of scanning every market uniformly, concentrate compute and order attention around the next expected information release for the relevant city.

---

# 10. Weather probability calibration should be hierarchical and time-series aware

Meteorological literature strongly supports post-processing raw ensemble forecasts.

Daily maximum-temperature EMOS research has shown calibrated predictive distributions outperform uncalibrated/estimative approaches on log score, CRPS and coverage. More recent time-series EMOS work explicitly models seasonality, trends and autocorrelated forecast errors, improving temperature calibration across stations/lead times.

References:
- Gneiting et al. EMOS foundations: https://doi.org/10.1175/MWR2904.1
- daily maximum temperature EMOS application: search `Ensemble model output statistics for temperature forecasts in Veneto`
- 2024 time-series EMOS: https://doi.org/10.1002/qj.4844

### Trading-specific extension

We do not need to optimize generic temperature CRPS alone. Fit directly for **resolver bucket log likelihood** and net trading performance.

Hierarchical model:

`bias = global + region + station + model + lead + cycle + season + regime`.

Variance/spread calibration:

`scale = f(ensemble spread, lead, season, current observation error, model disagreement)`.

With shrinkage, less-active cities borrow statistical strength from related stations while preserving local basis.

---

# 11. Distribution family should vary by market family

No universal Gaussian is required.

### Temperature

Candidate residual families:

- Gaussian;
- Student-t;
- logistic;
- Laplace;
- skew-normal;
- empirical residual dressing.

For daily extrema, the empirical member-max distribution plus residual dressing is especially natural.

### Precipitation

Precipitation requires a mass near zero and heavy/right-skewed positive amounts. EMOS literature uses censored extreme-value or related skewed distributions.

### Wind maximum

Extreme-value/tail calibration is more relevant than normal error.

### GISTEMP

Dataset-basis residual may be close to Gaussian but must be tested at the tiny 0.05°C bucket scale.

Choose the family with best **out-of-sample resolver probability and dollar PnL**, not mathematical familiarity.

---

# 12. Favorite-longshot bias is not universal — weather-specific measurement is valuable

Public weather bots sometimes report that cheap YES tails are systematically bad and mid-priced NOs are profitable.

General betting literature documents favorite-longshot bias, but prediction-market evidence is mixed. Recent 2026 Kalshi research finds low-probability unemployment contracts substantially overpriced, while a separate CPI study finds much weaker/no classic aggregate bias.

This category dependence is useful.

Research:
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7110758
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7087538

### Implication

Do not assume “tail NO” as a universal law. Measure **weather-specific calibration** by:

- horizon;
- city;
- local hour;
- distance from weather mode;
- price band;
- spread;
- time since latest model update.

If T+0 longshots are overpriced after the likely peak, that could be a behavioral edge with a physical explanation: traders overweight the chance of one more surprising temperature print.

This could combine beautifully with certainty-collapse math.

---

# 13. Market price should enter the model rather than be treated as dumb

Prediction markets contain informed traders. A strong weather model should use market probability as a feature/prior and trade only the residual information it adds.

Let:

- `q_w` = calibrated weather probability;
- `q_m` = coherent market probability;
- `W` = specialist-wallet factor;
- `X` = spread/flow/update-state features.

Model:

`logit(q*) = a + b logit(q_w) + c logit(q_m) + d W + beta X`.

For a multi-outcome ladder, use a softmax/Dirichlet/log-opinion-pool equivalent and renormalize.

### Segment-specific market weight

`c` should be high where the market historically beats weather models and lower where resolver/local-source data has shown independent edge.

This directly answers the question:

> How much new information does our forecast add beyond what the price already knows?

---

# 14. Specialist-wallet flow is justified by broader Polymarket research

Recent 2026 studies indicate:

- a small skilled minority drives substantial prediction-market accuracy;
- informed flow is economically meaningful;
- negative-risk/longer-lived market design relates to informed trading;
- high-spread niche markets can attract specialists;
- public fill data can identify performance/timing, while full quote lifecycle remains off-chain.

Relevant research:
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6617059
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6933527
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6751284
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6870538

### Weather implementation

For each wallet `w` estimate skill conditional on:

`market_family × city × horizon × direction × price_band`.

Then:

`wallet_factor_i(t) = Σ skill_w * normalized_signed_flow_w * decay(age)`.

The crucial test is incremental:

`weather + market + wallet` versus `weather + market`.

If the wallet factor improves both settlement prediction and short-term markout, it can become a live signal amplifier.

---

# 15. The full ladder offers a second strategy independent of forecast superiority

Temperature outcomes are mutually exclusive. Therefore the event is one probability distribution even though Polymarket exposes separate binary books.

A model shock should conserve probability mass.

For example, if observed station maximum jumps into 35°C and the remaining chance of 36°C is 15%, a coherent distribution might become:

- <=34: 0%;
- 35: 85%;
- 36: 13%;
- 37+: 2%.

Separate books may update asynchronously.

### Relative-value signal

Project market quotes onto a coherent simplex, then calculate:

`weather_residual_i = q_weather_i - q_market_coherent_i`.

Trade the largest local deviations, potentially hedged with neighboring outcomes.

### Negative risk

Because `NO_i` is economically linked to all other YES outcomes, continuously price:

`NO_i` versus `basket(other YES)`.

This can reveal structural discrepancies even if our weather model equals market consensus.

---

# 16. Prediction-market microstructure says cheap tails are expensive to trade

A 2026 order-book study reports a **longshot spread premium** on Polymarket and that depth is distributed more broadly through the book than a top-of-book-only model may assume.

Research:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6658364

Weather fees also hit cheap tokens significantly in percentage terms.

Therefore penny tails face three hurdles:

1. behavioral overpricing may exist;
2. spread premium;
3. taker fee relative to token cost.

This makes “buy every cheap forecast tail” a particularly weak generic strategy.

Conversely, informed maker quotes in tail books may be attractive when fair value and adverse selection are modeled accurately.

---

# 17. Maker/taker choice is an alpha multiplier

Weather currently pays makers through a rebate pool funded by taker fees.

For a large, fresh information shock:

`edge decay speed > expected maker fill speed`

so crossing can dominate.

For a slow-moving T+1 forecast discrepancy:

`spread + rebate + price improvement > value of immediate execution`

so maker orders can dominate.

The routing rule should estimate:

`EV_cross` and `EV_maker` for the same signal.

This is likely one of the easiest ways to improve realized PnL once probability alpha exists, because it requires no new meteorological insight.

---

# 18. GISTEMP may be the highest-capacity mathematical weather strategy

Daily city markets are frequent, but monthly/annual climate markets can carry much larger dollars.

Current August 2026 GISTEMP market has narrow 0.05°C buckets. NASA's August release is scheduled for September 10.

ERA5T arrives only a few days behind real time and monthly means around five days after month-end.

That suggests a strong sequence:

### During month

Nowcast global monthly mean using observed days + weather forecasts for remaining days.

### Month-end + ~5 days

Use near-complete ERA5T as high-information proxy.

### Before NASA release

Blend additional datasets / reproduce GISTEMP basis.

### Target

`P(first-published GISTEMP in each 0.05°C bucket)`.

Because the variable is low-noise and aggregation is global, a well-calibrated basis model may achieve much tighter uncertainty than city weather while supporting much more capital.

This track could ultimately outrank daily temperature by expected dollar PnL even if its percentage edge is smaller.

---

# 19. Cross-market climate consistency is underexplored

Current weather inventory can include simultaneously:

- monthly GISTEMP anomaly bucket;
- monthly/annual hottest-rank market;
- annual hottest-year ranking.

These are linked.

If anomaly distribution implies an 80% chance August is top-3 hottest but the rank market prices 55%, there is relative value.

Build one latent climate distribution and derive fair values for all linked contracts.

This is the climate equivalent of a temperature ladder.

---

# 20. Precipitation markets have beautiful state monotonicity

Current monthly precipitation markets exist in NYC, London, Seattle and Hong Kong. Recent prior-month pages show meaningful volume in some contracts.

State:

`P_final = accumulated_to_date + remaining_precip`.

Every observed rain event permanently eliminates lower brackets. Every day passing without rain reduces remaining opportunity.

### Strong edge moments

- immediately after a major observed storm;
- tropical cyclone track revisions;
- ensemble consensus on a multi-day rainfall event;
- late month with narrow remaining uncertainty;
- direct national/local gauge totals ahead of summarized resolver page.

Because many bettors think in monthly climatological totals rather than conditional remaining distributions, this could be a less crowded analogue of T+0 temperature certainty-collapse.

---

# 21. Weather market discovery should rank physical information geometry

Rather than hard-code “temperature only,” automatically classify each new WEATHER event:

- running maximum;
- running minimum;
- running sum/count;
- published index;
- nested threshold;
- other.

Then map it to the correct generic probability engine.

This makes new niche weather markets immediately researchable without building new architecture.

Examples:

- daily high → running max engine;
- daily low → running min;
- precipitation → running sum;
- wind max → running max + nested thresholds;
- hurricanes/tornadoes → running count;
- GISTEMP → index/basis model.

This is a reusable profit abstraction, not framework-for-framework's-sake.

---

# 22. A stronger alpha ranking after the second pass

## Tier 1 — immediate highest expected research value

### A. Supplied-wallet reconstruction

Fastest way to discover a real active specialist's policy.

### B. Same-day resolver certainty-collapse

Strong causal physical mechanism, recurring daily, directly visible in supplied wallet behavior.

### C. Exact resolver/source model

Affects every other strategy and has already caused huge public-bot errors.

### D. Weather-specific price calibration

Can reveal a behavioral edge even before sophisticated forecasts.

## Tier 2 — likely profit multipliers

### E. Direct model-release latency

LAMP/NBM/ECMWF/Met Office/JMA/DWD/KMA/HKO.

### F. T+1 station-calibrated modal bucket

Broad recurring opportunity.

### G. Specialist-wallet consensus

Public informed-flow feature.

### H. Maker/taker dynamic routing

Turns forecast alpha into more net PnL.

### I. Full-ladder/negative-risk relative value

Independent structural engine.

## Tier 3 — high-capacity expansion

### J. GISTEMP monthly anomaly

Potentially the largest dollar opportunity if basis residuals are tight.

### K. Annual climate rank cross-market model

Leverages same climate engine with larger volume.

### L. Monthly precipitation

Strong cumulative-state math, less mature market.

### M. Wind/hurricane/tornado extrema/counts

Event-specific but structurally forecastable.

---

# 23. The smallest powerful empirical dataset

All of the Tier 1/2 research can be supported by a compact point-in-time dataset.

## Events

```text
event_id
family
city
station/index
rules
buckets
resolver
```

## Weather vintages

```text
source
model
run_time
available_time
received_time
station
valid_time
member/value
```

## Resolver observations

```text
source
station
observation_time
available_time
raw_value
running_extreme/accumulation
```

## Market ladder snapshots

```text
timestamp
event_id
outcome
yes_bid
yes_ask
depth
fee
```

## Wallet fills

```text
wallet
timestamp
event/outcome
side
price
size
```

## Outcome

```text
first_resolver_value
winning_bucket
resolution_time
```

Everything else—calibration, release studies, wallets, execution, capacity—can be derived.

---

# 24. Profit equation for the whole project

For opportunity `i`, depth level `k`:

`edge_ik = P(settlement_i | all information) - effective_price_ik - fees_ik`.

Expected dollars:

`E[PnL] = Σ_i,k fill_probability_ik * size_ik * edge_ik + maker_rebates - adverse_selection - impact`.

The forecast research improves the probability term.

Resolver research improves the definition of settlement.

Release timing improves how early the probability is known.

Wallet research improves the information set.

Microstructure improves effective price/fill/rebate.

Capacity research decides where the next dollar goes.

That is the complete thesis.
