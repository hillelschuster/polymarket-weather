# Public weather bot code audit

Snapshot: **2026-08-11**

This file records concrete strategy-code observations, not README marketing.

## `suislanchez/polymarket-kalshi-weather-bot`

Inspected file: `backend/core/weather_signals.py`

### Actual probability logic

For a threshold market, the code computes YES probability as the raw fraction of ensemble members that cross the threshold.

Then:

- clips the probability to `[0.05, 0.95]`;
- defines “confidence” from the fraction of members on the majority side;
- compares model probability with current market YES price;
- applies Kelly sizing;
- zeroes edge if entry price is above a configured maximum.

### Why this leaves room

1. **Raw ensemble counts are not calibrated probabilities.** Bias and dispersion errors are not corrected.
2. **5–95% clipping destroys tail information.** Weather ladders make tail calibration economically important.
3. **Member agreement is not forecast reliability.** A unanimous but underdispersed ensemble can still be badly overconfident.
4. **No member-level settlement-max transformation is visible in this signal layer.** The key target is station daily maximum, not merely a threshold applied to a generic forecast summary.
5. **Market price is treated more simply than executable book economics warrant.**

This is an excellent baseline to beat because it is simple and plausible.

Source: https://github.com/suislanchez/polymarket-kalshi-weather-bot/blob/main/backend/core/weather_signals.py

---

## `BallesJr/polymarket-weather-edge`

Inspected files:

- `weather_api.py`
- `signal_engine.py`

This repository is valuable because it contains real strategy evolution and openly documents prior bugs.

### Forecast distribution is hand-set, not learned

`fetch_forecast()` gets Open-Meteo `best_match` daily maximum and constructs an uncertainty band heuristically:

- T+0: ±1.0°C;
- T+1: ±1.5°C;
- T+2: ±2.0°C.

The probability engine converts the band to a Gaussian sigma using `(high-low)/3.29`, with a minimum sigma.

No station×lead×season empirical calibration is used in the live Gaussian path.

### Same-day logic is a heuristic, not conditional-max math

When today's observed METAR maximum exists but the day is unfinished, code sets:

- center = `max(observed_max, forecast_max)`;
- effective low = center − 0.5°C;
- effective high = center + 2.0°C;

That is then converted to a Gaussian bucket probability.

This is directionally sensible—it respects that the final max cannot fall below the observed max—but it does not model the distribution of the **remaining hourly maximum**. It ignores forecast-path shape and hours remaining to peak.

A stronger approach is:

`M_final = max(M_observed, max(remaining hourly path))`

for every calibrated ensemble path.

### The live trade rule is currently a price-band rule

`signal_engine.py` explicitly states that the deployed strategy buys NO only when:

- horizon is T+0;
- NO price is in `[0.15, 0.40]`;
- liquidity exceeds threshold;
- city is not statistically blocked.

The Gaussian model is recorded but **does not gate the trade**.

This is strategically important. If the reported clean-regime behavior survives independent reconstruction, the edge may be a **market-calibration / longshot-bias phenomenon**, not forecast superiority.

### The code's displayed `net_edge` is not directional EV

For forced `BUY_NO`, the code computes:

`edge = model_prob_yes - market_prob_yes`

then:

`net_edge = abs(edge) - fee(no_price)`

Using `abs(edge)` means the metric can look positive even when the weather model favors YES more strongly than the market, which is the wrong direction for a NO purchase.

The strategy does not gate on this number, so it does not necessarily change which trades are opened, but it means:

- the displayed/ranked `net_edge` should not be treated as economic edge;
- any analysis using it as a target must be recomputed from first principles.

For BUY_NO, correct hold-to-resolution edge before fees is:

`(1 - model_prob_yes) - no_entry_price`

### Point-in-time concern

The live code uses Open-Meteo `best_match`, which can change underlying model selection and is not a clean multi-model issued-forecast archive. Historical evaluation must retain the exact forecast available at trade time.

### Useful claims to reproduce independently

The repository self-reports:

- exact resolver-station METAR/IEM values match actual market resolutions much better than ERA5 grids;
- T+0 BUY_NO did far better than T+1/T+2;
- very cheap NO tokens performed badly;
- a middle NO-price band performed best.

These are high-value hypotheses, not established facts until we rebuild them from raw resolved markets and point-in-time prices.

Sources:

- https://github.com/BallesJr/polymarket-weather-edge/blob/main/weather_api.py
- https://github.com/BallesJr/polymarket-weather-edge/blob/main/signal_engine.py

---

## `GuillermoEguilaz/Polymarket-Weather-Bot`

From the documented strategy:

`NWS point forecast -> bucket containing forecast -> entry/exit price threshold`

This is not a probabilistic settlement model. A point estimate selects one bucket even though adjacent buckets may each have meaningful probability.

Competitive implication: a calibrated full distribution should dominate this class of bot if the market itself does not already incorporate better information.

Source: https://github.com/GuillermoEguilaz/Polymarket-Weather-Bot

---

## `alteregoeth-ai/weatherbot`

Public README describes a more complete baseline:

- ECMWF + HRRR/GFS;
- station coordinates;
- METAR;
- EV filters;
- Kelly;
- spread/slippage filter;
- per-city self-calibration;
- stored forecast/trade/resolution history.

This is closer to the architecture we would expect from a serious hobbyist bot. The exact calibration implementation still needs code-level audit; README statements alone do not establish calibration quality or PnL.

Source: https://github.com/alteregoeth-ai/weatherbot

---

## `yangyuan-zhen/PolyWeather`

This project goes much farther on meteorological intelligence:

- many local observations;
- settlement-oriented stations;
- recent-model-error weighting;
- probability bucket generation;
- DEB/model blending;
- EMOS/CRPS-related calibration work;
- intraday structured analysis.

Its own current research documentation says the Polymarket market-price pull layer was removed in v1.7, so this is best viewed as a weather-analysis reference rather than evidence of live execution alpha.

Source: https://github.com/yangyuan-zhen/PolyWeather

---

## What the audit implies

The public baseline to beat is not extremely high mathematically. Most visible systems use some combination of:

- point forecasts;
- raw ensemble votes;
- hand-set Gaussian sigma;
- short recent-error weights;
- simple price thresholds;
- midpoint-like market comparisons.

The harder and more defensible edge is still underrepresented publicly:

1. exact station + resolver model;
2. member-level daily maxima;
3. proper station/lead/regime probabilistic calibration;
4. conditional remaining-path nowcast;
5. point-in-time forecast release timing;
6. full-ladder/negative-risk pricing;
7. executable depth + maker/taker economics;
8. wallet-flow incremental information.

That is where the research effort should stay concentrated.
