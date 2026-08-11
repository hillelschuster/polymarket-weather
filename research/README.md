# Weather alpha research — current synthesis

Snapshot: **2026-08-11**

## Verdict

Weather is a real, monetized Polymarket niche. The all-time WEATHER leaderboard currently contains multiple six-figure winners and several traders with more than $10M of weather volume. That establishes economic opportunity at category level. The research problem is to identify which repeatable mechanisms generate the profits and which of them remain accessible.

The strongest formulation is broader than “forecast better than the crowd”:

> **Estimate the exact settlement distribution faster and more accurately than the marginal trader, then monetize the discrepancy through the cheapest executable path.**

Six engines can produce PnL:

1. **Resolver-specific forecast calibration** — probability of the exact station/source bucket, including rounding and civil-day rules.
2. **State-conditioning / certainty collapse** — update daily maxima, minima and cumulative totals as observations arrive.
3. **Information-release latency** — new model runs and official observations can move fair value before the order book fully moves.
4. **Cross-outcome structure** — mutually exclusive ladders and negative-risk conversions create relative-value constraints.
5. **Wallet information** — profitable weather specialists reveal timing, city, horizon and price fingerprints.
6. **Execution alpha** — maker pricing, spread capture, rebates and informed quote placement can convert the same forecast into more net PnL than crossing the book.

## Public evidence that specialists make money

Current Polymarket WEATHER leaderboard snapshots show approximately:

- `gopfan2`: +$349k all-time WEATHER PnL;
- `aenews2`: +$285k;
- `ColdMath`: +$136k;
- `gopfan`: +$118k;
- `Poligarch`, `Hans323`, `automatedAItradingbot`, `WeatherTraderBot`, `HighTempTation` and others with substantial weather profit.

The WEATHER volume leaderboard includes several accounts above $10M of category turnover.

This is category evidence rather than proof of one strategy. WEATHER contains daily temperature, climate/global-temperature, precipitation, wind and other markets. Contract-level decomposition is therefore the useful unit of research.

Sources:
- https://polymarket.com/leaderboard/weather/all/profit
- https://polymarket.com/leaderboard/weather/all/volume

## The supplied forecasting wallet is especially informative

Profile:
`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

On the 2026-08-11 snapshot the account shows:

- 792 predictions;
- about $4.5k of open position value;
- +$1,018.71 past-day PnL;
- large exact-bucket YES positions spread across Istanbul, Tel Aviv, Madrid, Milan, Wuhan, Karachi, Munich, Mexico City, Paris, Singapore, Miami, Denver, Wellington, Amsterdam, Ankara and Shanghai.

Several same-day positions were bought around 47–67¢ and had repriced near $1 by the snapshot: Istanbul 27°C, Tel Aviv 35°C, Milan 36°C, Karachi 32°C and Munich 31°C. The wallet also holds next-day modal-bucket positions such as Madrid 38°C and Tel Aviv 35°C.

**Inference:** the visible portfolio is more consistent with a strategy that buys exact modal buckets as weather uncertainty collapses than with a generic “fade longshots” strategy. The account combines T+0 and T+1 forecasts across many international cities. Trade timestamps and historical closed positions are required to identify whether the dominant edge is forecast-vintage timing, live-observation conditioning, or both.

Profile source:
https://polymarket.com/@0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f-1774968947489

## The most promising daily-temperature edge: certainty collapse

For a daily high, define:

- `M_t` = maximum already observed at the exact resolution station by time `t`;
- `R_t` = maximum temperature over the remaining local civil day;
- `H = max(M_t, R_t)` = final resolver high.

Once the station has already printed a value inside bucket `b`, downside probability below `b` vanishes. As the likely daily peak passes, the remaining probability of exceeding the next rounding boundary can collapse quickly.

The tradeable quantity becomes:

`q_b(t) = P(round_resolver(max(M_t, R_t)) == b | information available at t)`

This is fundamentally different from forecasting tomorrow's high from scratch.

A strong implementation can condition every forecast member on current station error:

`x*_{m,h} = x_{m,h} + bias(model, station, lead) + alpha(h-t) * (obs_t - x_{m,t}) + residual_dressing`

Then:

`H_m(t) = max(M_t, max_{h>t} x*_{m,h})`

The empirical distribution of `H_m(t)` is mapped through the contract's actual rounding/bucket function. Historical station-specific residual calibration converts raw members into reliable bucket probabilities.

This mechanism has a causal reason to persist: the physical process becomes more constrained during the day, while traders and generic bots may still reference stale point forecasts or lagging web summaries.

## US short-range markets have richer data than most public bots use

Two NOAA products are unusually aligned with US temperature contracts:

### LAMP

NOAA Localized Aviation MOS Program guidance is station-specific, updates hourly for most elements, incorporates recent station observations plus model/MOS information, and provides temperature guidance to roughly 38 hours.

That makes LAMP a natural feature for T+0/T+1 airport settlement markets.

### NBM

The National Blend of Models publishes probabilistic MaxT fields including mean, standard deviation, percentiles and threshold probabilities. The blend is already designed as a calibrated probabilistic guidance product rather than a raw deterministic forecast.

A profitable US stack should compare, rather than blindly average:

- live exact-station observations;
- LAMP station guidance;
- NBM probabilistic MaxT;
- HRRR/HREF short-range guidance;
- GFS MOS;
- ECMWF ENS.

The target is resolver-bucket log loss / trading PnL, not generic weather MAE.

## Global city markets create geographic attention asymmetry

The supplied wallet is active in cities such as Wuhan, Karachi, Ankara, Wellington, Tel Aviv and Shanghai as well as major Western cities. Public projects often emphasize NYC/London/Miami and route global forecasts through Open-Meteo.

That suggests a useful specialization strategy:

- map every Polymarket city to its resolver station;
- map every resolver to the best local/national observation and NWP source;
- measure where direct/local data beats popular global aggregators;
- rank cities by incremental forecast skill × market volume × spread × response latency.

The underexploited edge may therefore be **city-specific data plumbing plus calibration**, not one universal weather model.

## Resolution mechanics are themselves alpha

Public projects have repeatedly lost money or fabricated backtest edge by targeting the wrong data source or station.

One open-source project (`jattree/weather-edge`) reported a $210 → $51.61 live run. Its later audit found that the run used, at different times, gridded reanalysis instead of the resolver feed, incorrect stations, incorrect Fahrenheit bucket integration and multi-bucket execution. Its later review concluded the weather alpha had never actually been measured under correct plumbing.

This matters economically because a 1°C station/source error is the width of many international buckets.

Current Polymarket rules vary by market:

- Paris daily high: Wunderground Daily Observations at Paris-Le Bourget `LFPB`;
- Wuhan: Wunderground at Wuhan Tianhe `ZHHH`;
- Shanghai: Wunderground at Pudong `ZSPD`;
- Ankara: Wunderground at Esenboğa `LTAC`;
- Tel Aviv: current rules use NOAA WRH station data at Ben Gurion `LLBG`;
- Hong Kong low-temperature markets can resolve directly from Hong Kong Observatory Daily Extract data.

Rules, units and even source families vary through time. Parse each event rather than hard-code a permanent city convention.

## US Fahrenheit resolver reconstruction contains a niche technical edge

Iowa Environmental Mesonet documentation highlights a subtle issue: official US ASOS temperature observations are internally based on whole-degree Fahrenheit conventions, while routine METAR temperature transmission is commonly whole Celsius and can be distorted by Fahrenheit↔Celsius round trips. IEM prioritizes higher-precision T-groups and incorporates special/max-temperature reports where available.

Therefore `max(routine METAR temp_c) -> convert to °F -> round` is not always the same object as the eventual official daily high.

For 2°F US Polymarket buckets, this difference can move the winning contract. Exact ASOS/DSM/CLI/T-group logic deserves explicit modeling.

## Market price is a feature, not an opponent to ignore

The market itself aggregates information. The strongest forecaster can learn the residual value of weather information relative to the market:

`P(Y=i | weather_state, market_distribution, wallet_flow, microstructure)`

A practical hierarchy is:

1. calibrated weather-only distribution `q_weather`;
2. coherent market distribution `q_market` projected onto the probability simplex;
3. learned combination whose weight varies by city, horizon and market state;
4. trade the residual between the combined probability and executable price.

This allows the crowd to contribute information while preserving an independent weather edge.

## Full-ladder probability is the correct object

A temperature event with `K` mutually exclusive buckets has:

`sum_i q_i = 1`

Polymarket negative-risk mechanics link a NO share in one outcome to YES shares in the others. That turns the event into a structured relative-value surface.

Useful calculations include:

- coherent weather probabilities across all buckets;
- coherent executable market probabilities;
- deviations after projecting market prices onto the simplex;
- NO_i versus the basket of other YES outcomes;
- fee/depth-adjusted all-outcome basket prices;
- relative-value trades where weather information identifies which local distortion is wrong.

## Execution changes the edge materially

Polymarket currently lists Weather with:

- taker fee rate `0.05` on fee-enabled contracts;
- maker fee `0`;
- 25% of collected Weather taker fees allocated to the maker-rebate pool.

Fee per share:

`fee(p) = 0.05 * p * (1-p)`

For a YES bought at executable ask `a` and held to resolution:

`EV_taker/share = q - a - fee(a)`

The displayed Polymarket price is normally the bid/ask midpoint and can switch to last trade when spread exceeds $0.10. It is therefore unsuitable as the final execution price.

A weather strategy with modest informational edge may monetize better by posting informed liquidity around fair value, especially in wide global-city ladders. The relevant comparison is expected dollars from crossing now versus expected dollars from a maker order after fill probability, adverse-selection markout and rebate.

Sources:
- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates
- https://docs.polymarket.com/concepts/prices-orderbook
- https://docs.polymarket.com/advanced/neg-risk

## Weather market families extend beyond daily highs

The same mathematical framework applies to several current Polymarket families:

### Daily lows

`L = min(m_t, remaining_min)`.

Information becomes one-sided as the night/morning minimum is observed.

### Monthly precipitation

`P_month = observed_accumulation_t + remaining_precipitation`.

Observed rainfall is permanent state; uncertainty decreases as the month advances. Current NYC August precipitation markets resolve from NOAA Central Park monthly summarized precipitation.

### Monthly wind maximum

`W_month = max(observed_max_t, remaining_wind_max)`.

Mt. Washington August markets resolve from Mount Washington Observatory F6 data. Extreme-wind probability is strongly conditional on tropical-cyclone and synoptic forecasts.

### Global temperature anomaly

Current monthly anomaly ladders resolve from NASA GISTEMP. NASA publishes a 2026 release schedule; August data are scheduled for September 10 at 11:00 AM EDT. ERA5T daily data arrive about five days behind real time and monthly means about five days after month-end. A calibrated historical mapping from partial-month/ERA5T/global datasets into eventual GISTEMP bins is a high-capacity research path.

## Ranked alpha priorities

Current research ranking by expected combination of edge, persistence and capacity:

1. **T+0 exact-bucket certainty collapse at resolver stations.**
2. **T+1 station-calibrated full-ladder forecasting, especially under-followed international cities.**
3. **Forecast/observation release-latency event studies.**
4. **Profitable-wallet timing and consensus as an incremental feature.**
5. **Informed maker execution around weather fair value.**
6. **Cross-bucket/negative-risk relative value.**
7. **GISTEMP monthly anomaly nowcasting for larger-capacity climate contracts.**
8. **Cumulative precipitation and monthly-extreme markets.**

Ranking should evolve with measured expected dollar PnL/day and capacity.
