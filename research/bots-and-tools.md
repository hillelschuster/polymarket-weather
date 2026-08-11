# Public Polymarket weather bots and tools

Snapshot: **2026-08-11**

This survey is for extracting ideas and identifying crowded/simple approaches. Repository claims about performance are **self-reported unless independently reconstructed**.

## Most relevant public projects

### 1. `suislanchez/polymarket-kalshi-weather-bot`

Strongest value: a concrete baseline implementation plus research notes.

Observed strategy code:

- gets ensemble forecasts;
- estimates YES probability as the fraction of members above/below the threshold;
- clips model probability into `[0.05, 0.95]`;
- compares that probability to market YES price;
- uses ensemble agreement as confidence;
- applies Kelly sizing.

Why it matters: this is a plausible version of what many hobbyist weather bots do.

Where it leaves edge:

- raw member fractions are not calibrated probabilities;
- probability clipping destroys genuine tail resolution;
- member agreement is not the same thing as forecast reliability;
- no serious station-specific postprocessing in the inspected signal path;
- model-price difference is a weaker objective than executable net EV.

Repository: https://github.com/suislanchez/polymarket-kalshi-weather-bot

### 2. `yangyuan-zhen/PolyWeather`

This is much more sophisticated weather intelligence than most trading bots.

Observed ideas in its docs/codebase:

- many observation sources including METAR and regional official networks;
- Dynamic Error Balancing using recent model MAE inverse weighting;
- ensemble p10/p90 converted into distribution spread;
- historical MAE floor;
- normal-distribution bucket probabilities;
- settlement-source awareness and strict bucket matching;
- persistent truth/training data;
- recent work around probability calibration / evaluation.

Important limitation for our purpose: its current v1.7 research report says the Polymarket price-pull/market-scan layer was removed, so it is currently more useful as a weather-intelligence reference than as a live trading blueprint.

Ideas to steal conceptually, not code blindly:

- exact settlement-source catalog;
- city-specific residual tracking;
- live observation conditioning;
- resolver-aware bucket mapping.

Repository: https://github.com/yangyuan-zhen/PolyWeather

### 3. `BallesJr/polymarket-weather-edge`

Interesting because the author documents failures and data bugs rather than only presenting a polished strategy.

Self-reported findings:

- audited 500+ historical trades;
- claims exact resolver-station METAR daily highs matched resolutions ~93% vs ~66% for ERA5 grid values;
- reports that a T+0 BUY_NO price-band strategy materially outperformed other tested regimes;
- disabled T+1 and T+2 after poor results;
- reports a NO-price band around 0.15–0.40 as the live paper rule;
- found an RF feature mismatch that had silently made the calibrator ineffective and removed it from the live path.

The author explicitly says clean forward validation is still accumulating. Therefore none of those win-rate/edge claims should be imported as facts.

The useful hypothesis is stronger: **exact-station same-day data plus possible tail overpricing deserves independent replication**.

Repository: https://github.com/BallesJr/polymarket-weather-edge

### 4. `GuillermoEguilaz/Polymarket-Weather-Bot`

A simpler TypeScript baseline:

- NWS forecast;
- map forecast max into one temperature bucket;
- buy when matching YES price is below an entry threshold;
- optional paper/live CLOB paths.

This illustrates how under-modeled the public landscape can be: a deterministic point forecast is being used where the contract payoff is fundamentally probabilistic.

Repository: https://github.com/GuillermoEguilaz/Polymarket-Weather-Bot

### 5. `RiekertQuant/polymarket-weather-bot-poc`

POC features:

- Open-Meteo forecast;
- fixed forecast sigma;
- cheap-share / strong-edge rules;
- optional ML calibrator;
- historical-forecast backtesting;
- paper-only execution.

Useful mainly as a list of basic components, not a competitive model.

Repository: https://github.com/RiekertQuant/polymarket-weather-bot-poc

### 6. `alteregoeth-ai/weatherbot`

Web-indexed public project described as combining ECMWF + HRRR/GFS + METAR, expected-value calculations, fractional Kelly and slippage, with station coordinates and self-calibration. It did not resolve cleanly through the GitHub repository connector during this research pass, so details need independent source inspection before relying on them.

### Other repositories discovered

GitHub search also surfaced:

- `MoonsatProtocol/Polymarket-Weather-Bot`
- `hcharper/polyBot-Weather`
- `idlepraxis/polymarket-weather-bot`
- `nicolastinkl/hermes_weatherbot`
- `hawx07/Polymarket-Weather-Arbitrage-Bot`
- `tobiasbischoff/polymarket-weather-bot`
- `MihirM9/polymarket-weather-bot`
- `api-claude-dev/polymarket-quant-bots`

These are secondary reading targets after the higher-signal projects above.

## About `moovdev`

Searches for `moovdev polymarket`, `moovdev weather bot`, and close variants did not produce a clear indexed GitHub match in this pass. It may be a spelling variant, a renamed/private repository, or a non-GitHub project. Do not invent a match. Keep it as an unresolved lead.

## Commercial / hosted projects

Several hosted sites advertise Polymarket weather prediction or automated systems. Their public descriptions are useful for discovering techniques other people consider marketable—multi-model ensembles, Bayesian/normal CDFs, city dashboards, etc.—but their stated win rates/PnL are marketing claims unless reconciled against public wallet history.

Use them as idea sources, not evidence.

## The common public-bot pattern

Across the inspected code and docs, the modal architecture is:

`weather API -> point/ensemble forecast -> ad-hoc probability -> market-price edge -> Kelly/threshold -> trade`

That misses several profit-critical layers:

1. exact station/resolver transformation;
2. point-in-time station-specific forecast calibration;
3. daily-max path statistics;
4. same-day conditional maximum;
5. full-ladder simplex / negative-risk relationships;
6. forecast-release latency;
7. maker/taker economics and fee/rebate treatment;
8. informed-wallet flow;
9. executable depth/capacity.

That gap is the main reason the project should not merely fork an existing bot.

## Techniques that look promising enough to reproduce

### Reproduce first

- exact station vs generic grid forecast error;
- T+0 vs T+1/T+2 profitability;
- tail/longshot calibration by market price bucket;
- multi-model calibration vs raw ensemble counts;
- model-release response lag;
- complete-ladder arbitrage/relative value;
- maker vs taker realized economics.

### Do not assume

- fixed sigma works across cities/horizons;
- raw member counts are calibrated;
- one week's wallet PnL reveals a durable policy;
- a reported backtest used point-in-time forecasts correctly;
- a high win rate means high EV;
- market midpoint is an executable price.

## Broader prediction-market tooling worth knowing

Polymarket's official stack already exposes most primitives we need:

- Gamma API for event/market discovery and rules metadata;
- CLOB REST/WebSocket for order books, prices and execution;
- Data API for trades, positions, activity and leaderboard;
- `py-clob-client` for Python trading integration later;
- negative-risk CTF adapter for multi-outcome conversion.

A research system does not need a large third-party framework. The competitive layer is the probability/execution logic and point-in-time dataset.

## References

- `suislanchez/polymarket-kalshi-weather-bot`: https://github.com/suislanchez/polymarket-kalshi-weather-bot
- `yangyuan-zhen/PolyWeather`: https://github.com/yangyuan-zhen/PolyWeather
- `BallesJr/polymarket-weather-edge`: https://github.com/BallesJr/polymarket-weather-edge
- `GuillermoEguilaz/Polymarket-Weather-Bot`: https://github.com/GuillermoEguilaz/Polymarket-Weather-Bot
- `RiekertQuant/polymarket-weather-bot-poc`: https://github.com/RiekertQuant/polymarket-weather-bot-poc
- Official API docs index: https://docs.polymarket.com/llms.txt
