# Public weather bots and tools — alpha map

Snapshot: **2026-08-11**

Public weather-trading repositories are valuable because they reveal what the obvious implementation looks like, which ideas have already attracted competition, and where public approaches remain mathematically weak.

The recurring public pattern is:

`generic forecast -> simple distribution -> compare to displayed/quoted price -> threshold -> bet`

The largest opportunity is therefore likely in the pieces that are **not** generic:

- exact resolver modeling;
- observation-conditioned remaining extrema;
- source-release timing;
- city-specific calibration;
- direct national/local feeds;
- full-ladder probability conservation;
- wallet information;
- execution economics.

---

## 1. `suislanchez/polymarket-kalshi-weather-bot`

Repository:
https://github.com/suislanchez/polymarket-kalshi-weather-bot

### Strategy visible in code

The weather signal path:

- fetches ensemble forecasts;
- estimates YES probability as fraction of member highs/lows above/below threshold;
- clips probabilities to `[0.05, 0.95]`;
- compares to market probability;
- treats ensemble agreement as confidence;
- applies Kelly sizing and fixed trade-size limits.

### Alpha gap

Raw member frequency is a baseline, not calibrated bucket probability. The implementation leaves several dimensions unused:

- exact resolver rounding;
- model-specific bias by station/lead/cycle;
- residual dressing;
- observation-conditioned same-day paths;
- multi-model skill weighting;
- full multi-outcome ladder;
- executable depth rather than one price;
- release latency.

The 5–95% clipping also destroys legitimate near-certainty information exactly when same-day extrema can become close to physically locked.

### Useful idea to retain

The code demonstrates a minimal event→forecast→probability→edge pipeline. The profitable version can stay equally compact while replacing raw member counts with resolver-calibrated probabilities.

---

## 2. `BallesJr/polymarket-weather-edge`

Repository:
https://github.com/BallesJr/polymarket-weather-edge

### Interesting empirical claim

The project reports an audit of 500+ historical trades where daily highs reconstructed from exact-station IEM METAR data agreed with market resolution about 93% of the time versus 66% for ERA5 grid data.

This is author-reported evidence, not independently reproduced here, but it strongly reinforces resolver fidelity as a high-value variable.

### Actual live strategy in current code

Despite computing a Gaussian weather probability, the current signal engine explicitly trades:

- BUY_NO only;
- T+0 only;
- NO token price between 0.15 and 0.40;
- minimum liquidity;
- city-performance filter.

The Gaussian is stored as a feature but **does not gate entry**.

The project states its prior Random Forest live inference had feature/sign mismatches, effectively degenerating into the price-band rule; the code makes the band rule explicit.

### Same-day weather model

Current code:

- uses exact-station METAR observed max when available;
- centers remaining-day belief around `max(observed_max, forecast)`;
- gives an unfinished day an ad hoc interval approximately `[-0.5°C, +2°C]` around that center;
- maps it through a Gaussian.

### Exploitable gaps

1. **No conditional remaining-path distribution.** It does not estimate the probability of crossing the next boundary from the actual remaining hourly forecast ensemble.
2. **Weather probability does not choose trades.** A superior probability model can potentially discriminate profitable from unprofitable trades inside the same NO-price band.
3. **Directional EV bug in analytics.** The signal code calculates `net_edge` from `abs(model_prob - market_prob)` despite forcing BUY_NO, so the reported edge can remain positive even when the model actually favors YES. This does not drive its price-band entry, but it makes the stored “edge” unsuitable as true directional expected value.
4. **Flat size.** Marginal book EV/capacity is unused.
5. **No full ladder.** Each contract is considered mostly independently.
6. **Single forecast source.** Open-Meteo `best_match` leaves model identity and direct local feeds underexploited.

### Money lesson

This repo may contain two separate phenomena worth testing independently:

- a behavioral T+0 NO price-band edge;
- meteorological resolver edge.

Combining them correctly could outperform either alone.

---

## 3. `jattree/weather-edge`

Repository:
https://github.com/jattree/weather-edge

This is one of the most technically ambitious public attempts and one of the most informative because it contains a live failure and a later audit.

### Architecture/strategy

Public README/archive describes:

- 6–8 model consensus;
- station bias correction;
- EMOS-style calibration;
- Brier-weighted model consensus;
- weather-pattern detectors;
- exact-station observation/resolution layer;
- directional trading and maker/taker execution;
- live portfolio/accounting.

### Reported live result

The archived run reports:

`$210 -> $51.61`, a **-75.4%** drawdown.

The first post-mortem attributed this partly to lack of durable forecast alpha.

### The later audit changes the interpretation

A June 2026 proving-run review states that the run never cleanly tested that claim because every trading window contained major correctness defects at the time, including:

- reanalysis instead of the actual resolver source;
- wrong stations for Denver, Houston and Hong Kong;
- multi-adjacent-bucket YES exposure;
- Fahrenheit bucket integration error that systematically inflated YES probability;
- later deliberate lottery-style configuration.

The later review's headline conclusion is effectively **alpha unmeasured**, not alpha disproven.

### High-value lessons for this project

#### Resolver error is strategy error

The archive reports about 0.9°C MAE between the wrong gridded resolution proxy and resolver observations, with 67% of tested trades mapping to a different whole-degree bucket. On a 1°C market this can completely invert the trade.

#### Generic complexity does not create alpha

Dual AI reviewers and elaborate architecture contributed much less than exact source/station/bucket correctness. This supports a small probability engine with better data rather than a large orchestration stack.

#### Adjacent YES positions need portfolio math

Buying several adjacent mutually exclusive YES buckets is not inherently irrational—one can buy a probability basket below fair combined value—but each basket must be valued jointly. Buying them as separate “high-edge trades” without accounting for guaranteed mutual exclusivity creates misleading exposure/accounting.

#### Public “failed strategy” results can contain reusable edge

The repo's later clean-up and station table are useful research inputs, while the failed PnL should not be treated as an unbiased test of calibrated resolver forecasting.

---

## 4. `nickkea05/weather-market-trading-bot`

Repository:
https://github.com/nickkea05/weather-market-trading-bot

### Strategy

The tool covers ~35 cities and:

- uses Open-Meteo forecasts or manual Wunderground forecast input;
- calculates city market centers;
- maps a forecast into bucket fair values;
- uses a **Laplace** error distribution to represent fatter temperature tails;
- scales MAE by lead time and coarse city classes;
- scans for discrepancies.

### Specific math

`fair_value.py` hardcodes a global lead-time MAE curve and applies simple city multipliers:

- coastal/tropical ×0.75;
- interior/volatile ×1.3;
- other ×1.0.

It assumes expected peak hour is 14:00 local.

### Alpha gap

This is smarter than a fixed Gaussian, but still leaves enormous station-level information unused:

- generic MAE table instead of station/model/cycle calibration;
- fixed city buckets instead of learned regime uncertainty;
- no live observed maximum conditioning;
- fixed 14:00 peak assumption;
- no direct local model feeds;
- no model-vintage timing;
- no specialist-wallet factor.

Its market-data layer uses Gamma `bestBid`/`bestAsk`/`outcomePrices` because its author reports near-empty CLOB `/book` responses for neg-risk weather markets. Our collector should independently test token/book endpoints and WebSocket behavior rather than inherit that assumption.

### Money lesson

Fat-tailed error distributions are worth testing. Distribution family should be chosen by resolver-bucket log score and trading PnL segment-by-segment rather than universally Gaussian or Laplace.

---

## 5. `GuillermoEguilaz/Polymarket-Weather-Bot`

Repository:
https://github.com/GuillermoEguilaz/Polymarket-Weather-Bot

### Strategy

- NWS forecast data;
- map forecast maximum into one Polymarket bucket;
- buy when the matching bucket's YES price is below a threshold;
- sell/exit above another threshold;
- support signal, paper and live modes.

### Alpha gap

The main signal is deterministic bucket matching rather than probabilistic valuation.

It therefore cannot correctly compare:

- 30% at 10¢ versus 70% at 50¢;
- adjacent-bucket probabilities;
- forecast uncertainty changes;
- tail probabilities;
- observation-conditioned same-day state.

It is a good example of the public baseline we should beat mathematically.

---

## 6. `RiekertQuant/polymarket-weather-bot-poc`

Repository:
https://github.com/RiekertQuant/polymarket-weather-bot-poc

### Strategy

- Polymarket market discovery;
- Open-Meteo forecasts;
- probability engine with configured sigma;
- cheap-share filters;
- optional calibrator;
- backtest/paper framework.

### Alpha gap

The public strategy uses relatively generic forecast uncertainty and price/edge gates. Its synthetic-data fallback and generic historical-weather resolution make it more useful as software reference than as evidence of a profitable weather edge.

---

## 7. `tobiasbischoff/polymarket-weather-bot`

Repository:
https://github.com/tobiasbischoff/polymarket-weather-bot

### Public claims

README describes:

- NOAA + Open-Meteo forecasts;
- ≥15% forecast confidence edge;
- whitelist of warm/stable cities;
- self-reported 8-day backtest with 58.7% overall win rate and higher projected whitelist results.

It claims warm/stable climates outperformed cold/volatile cities in that short test.

### Research value

Treat the performance numbers as author-reported and short-sample. The more interesting hypothesis is **city forecastability varies enough to justify explicit capital ranking**.

Instead of a static whitelist, estimate for every city:

`city_value = incremental weather skill × available market edge × capacity × opportunity frequency`.

A city can be volatile yet profitable if market traders price it even worse; forecast MAE alone does not determine trading edge.

---

## 8. `yangyuan-zhen/PolyWeather`

Repository:
https://github.com/yangyuan-zhen/PolyWeather

This is more of a weather-intelligence platform than a clean trading bot.

Interesting components from the repository/documentation include:

- multi-source weather collection;
- exact airport and national observation feeds;
- DEB/dynamic error weighting;
- ensemble/trend probability logic;
- broad international city/source mapping.

It also shows how much local-source work can exist outside conventional global APIs: AMOS/AWOS, HKO, MGM, JMA, NWS and related networks.

### Research value

The source registry and local-observation ideas are more valuable to this project than the product/dashboard architecture.

---

# Clone/fork contamination in GitHub search

Search results contain many repositories with identical names/sizes matching `suislanchez/polymarket-kalshi-weather-bot`. Treat near-identical forks as one strategy family, not independent evidence that many people independently discovered the same profitable method.

This matters when estimating competitive crowding from GitHub counts.

---

# Public strategy taxonomy

| Public family | Typical probability model | Main weakness | Our stronger formulation |
|---|---|---|---|
| deterministic bucket | one forecast → one bucket | no probability | calibrated full distribution |
| raw ensemble | member fraction | uncalibrated | station residual dressing |
| fixed Gaussian | point + hand sigma | wrong tails/regimes | empirical/EMOS distribution |
| fixed Laplace | point + generic MAE | coarse calibration | station/model/cycle hierarchy |
| T+0 price band | market price heuristic | weather not decision variable | combine behavioral + resolver signal |
| multi-model consensus | weighted forecast | can still target wrong resolver | exact station/source + point-in-time calibration |
| AI-review bot | LLM qualitative filters | weak causal link to resolver probability | use physical/weather variables directly |

---

# The public gap we should target

Very little inspected public code simultaneously does all of the following:

1. parse the exact resolver and revision rule per event;
2. use upstream/direct local observations;
3. calculate per-member remaining-day extrema conditioned on live observation error;
4. calibrate bucket probabilities by station/model/horizon;
5. use full ladder probability conservation;
6. incorporate specialist-wallet information;
7. value each CLOB depth level after the current Weather fee;
8. dynamically choose maker versus taker based on information half-life;
9. rank opportunities by expected **dollar** PnL and capacity.

That combination is the current research target.
