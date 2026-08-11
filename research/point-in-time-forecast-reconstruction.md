# Point-in-time forecast reconstruction — the smallest faithful weather backtest

Snapshot: **2026-08-11**

Purpose: define the cheapest historical weather dataset that can reproduce what a profitable trader could actually have known when a Polymarket temperature trade was placed.

The important discovery is that **Open-Meteo now archives individual historical model runs by initialization time** and also exposes fixed-lead previous-run series. Combined with raw airport METAR history and Polymarket fills, this is sufficient to reconstruct a point-in-time resolver forecast without building a weather-data warehouse first.

---

# 1. Two Open-Meteo archives solve two different jobs

## Single Runs API — exact run reconstruction

Official documentation:

https://open-meteo.com/en/docs/single-runs-api

Endpoint:

`https://single-runs-api.open-meteo.com/v1/forecast`

Key parameter:

`run=YYYY-MM-DDTHH:MM`

The API returns the **full forecast horizon of one specific model initialization**.

Coverage:

- ECMWF IFS HRES 9 km: from **2024-03-14**;
- most other supported global/regional models: from **2026-04-02**.

The archive includes models directly relevant to the supplied wallet's city set, including:

- ECMWF IFS HRES;
- DWD ICON Global / ICON EU;
- ItaliaMeteo ICON-2I;
- Météo-France ARPEGE / AROME;
- CMA GRAPES;
- JMA GSM/MSM;
- KMA GDPS/LDPS;
- KNMI HARMONIE-AROME;
- UK Met Office;
- GEM;
- GFS / NBM / HRRR for US markets.

Use Single Runs when the exact intraday sequence matters:

- which run existed before a wallet fill;
- how much the forecast changed from the previous run;
- whether a trade followed a fresh release;
- whether a later run justified an exit.

## Previous Runs API — cheap historical error distributions

Official documentation:

https://open-meteo.com/en/docs/previous-runs-api

This API returns values forecast at fixed lead offsets such as:

`temperature_2m_previous_day1`

`temperature_2m_previous_day2`

Most models are archived from **January 2024**, with GFS 2m temperature from 2021 and JMA GSM/MSM from 2018.

This is ideal for estimating:

- station-specific T+1 forecast bias;
- T+2 bias;
- residual spread;
- seasonal error;
- model ranking by station/horizon.

It is cheaper than reconstructing every historical individual run.

---

# 2. Ensemble limitation changes the historical baseline

Open-Meteo's standard Ensemble API retains individual ensemble members for only about **three days** historically.

The Ensemble Mean API stores mean/spread for longer, with much of the archive available since roughly March 2026.

Therefore the clean historical baseline should **not depend on unavailable old ensemble members**.

The simplest faithful baseline is:

> **point-in-time deterministic daily maxima + empirical station/horizon forecast-error distributions.**

This already yields a full probability distribution.

Live trading can later add current ensemble spread/members if they improve net PnL.

---

# 3. Resolver truth — use raw airport observations, not reanalysis

Iowa State University's Iowa Environmental Mesonet maintains a global ASOS/AWOS/METAR archive.

Docs:

https://mesonet.agron.iastate.edu/request/download.phtml?network=ASOS

API docs:

https://mesonet.agron.iastate.edu/api/

The archive is built from sources including Unidata IDD, NCEI ISD and MADIS, and is synced from the real-time ingest every 10 minutes.

For many supplied-wallet stations it has long history, for example:

- Madrid `LEMD`: IEM archive beginning 1931, timezone Europe/Madrid;
- Tel Aviv / Ben Gurion `LLBG`: archive beginning 2001;
- Milan Malpensa `LIMC`: active Italy ASOS archive;
- Wuhan Tianhe `ZHHH`: active China ASOS archive.

IEM's computed daily summaries generally use each station's local calendar day, but for trading reconstruction the raw observations are more valuable because they allow replay of **running maximum at every point in time**.

For each event date:

`resolver_max = max(authoritative station reports inside the contract's local-day window)`

and for T+0 replay at timestamp `t`:

`M_t = max(reports available by t)`.

The market's actual rules remain decisive if the named source or station differs from the generic METAR archive.

---

# 4. A concrete recovered-wallet timing case: Milan June 30

Recovered supplied-wallet trade:

- market: **Milan June 30 — 35°C YES**;
- transaction: `0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`;
- fill timestamp: **2026-06-29 01:55:11 UTC**;
- raw price ~29.38¢;
- all-in price ~30.42¢;
- event ultimately resolved **34°C**, so 35°C lost if held.

ECMWF current dissemination schedule for its control/HRES-equivalent forecast:

- 18 UTC run, steps 0–90: delivered approximately **23:45–00:12 UTC**;
- next 00 UTC run does not begin dissemination until about **05:45 UTC**.

The target June 30 afternoon is within the T+0–90 step window of the June 28 18Z run.

Therefore at the wallet's **01:55 UTC** fill:

- the June 28 **18Z ECMWF run was fully available** for the relevant target hours;
- the June 29 00Z run was **not yet available**;
- the fill occurred roughly **1h43m after completion of the relevant 18Z dissemination window**.

This is the first strong recovered example where a wallet T+1 fill can plausibly be aligned with a specific fresh global model cycle.

## Test to perform

Retrieve:

- ECMWF 12Z June 28 run;
- ECMWF 18Z June 28 run;
- relevant ICON/ICON-2I/ARPEGE runs available before 01:55 UTC;

and calculate each run's forecast daily maximum for `LIMC` on June 30.

Then ask:

`Did new information shift probability mass toward 35°C before the wallet bought it?`

If yes, compare market price response after the fill.

Then retrieve later runs and ask:

`Did probability mass shift back toward 34°C before settlement, and did the wallet sell/reduce?`

This one trade can directly test the hypothesized entry/revision/exit mechanism.

---

# 5. Exact historical availability matters

A model's **initialization time is not its public availability time**.

Open-Meteo explicitly notes that:

- global models commonly need roughly 4–6 hours after initialization;
- regional models often need roughly 1–3 hours.

ECMWF publishes a formal dissemination schedule. For direct atmospheric output in current IFS control/HRES-equivalent runs:

| Base run | Relevant early-step delivery window |
|---|---|
| 00Z | ~05:45–06:12 UTC |
| 06Z | ~11:45–12:12 UTC |
| 12Z | ~17:45–18:12 UTC |
| 18Z | ~23:45–00:12 UTC |

For future live collection, Open-Meteo's model metadata exposes a `last_run_availability_time`; store that actual timestamp.

For historical backtests, use official dissemination schedules where available rather than pretending `run_time == information_time`.

---

# 6. Minimal deterministic probability model

For model `m`, station `s`, horizon class `h`, and date `d`:

`x_m(d) = model forecast daily maximum at resolver station`

Observed resolver maximum:

`y(d)`

Historical residual:

`e_m(d) = y(d) - x_m(d)`

For a new forecast with daily maximum `x_m*`, use the historical residual sample:

`H_{m,k} = x_m* + e_{m,k}`

where `k` indexes past comparable days.

Then bucket probability is simply:

`q_{m,i} = mean( H_{m,k} falls inside resolver bucket i )`.

This creates a probability distribution without choosing an arbitrary Gaussian sigma.

## Comparable-history filters

Start with only variables likely to materially affect error:

- same station;
- same forecast horizon class (T+0/T+1/T+2);
- broad season or rolling recent window.

Add weather-regime conditioning only if it improves out-of-sample PnL/calibration.

If station history is sparse, shrink toward a regional/global model residual distribution rather than fitting a complex local model.

---

# 7. Multi-model combination — keep it small

Do not pool 20 correlated model feeds as if they were independent observations.

Test only a few economically distinct candidates:

1. **ECMWF HRES residual distribution**;
2. **best local/high-resolution model residual distribution**;
3. **one secondary global model** if it adds out-of-sample information;
4. **market-implied coherent ladder**.

A deliberately simple weather blend is:

`q_weather = Σ_m w_m q_m`

with weights chosen from rolling historical bucket log loss / Brier / net PnL.

A deliberately simple market-weather combination is:

`q_final = λ q_weather + (1-λ) q_market`

where `q_market` is the normalized coherent probability surface derived from the ladder and `λ` is fit by horizon/station group only if data supports segmentation.

This protects against throwing away information already embedded in prices.

The first tests should compare:

- market alone;
- ECMWF alone;
- local model alone;
- ECMWF + local;
- weather + market linear pool.

If a more complex model does not improve fee-adjusted out-of-sample dollar PnL, it has no economic role.

---

# 8. Daily maximum must be calculated from the forecast path

For each deterministic run:

`x_m(d) = max_{t in resolver local day} T_m(t, station)`

not:

- city-center daily forecast;
- max of a smoothed multi-model mean;
- temperature at a fixed 14:00 hour.

This automatically handles changing peak time.

The same principle applies to ensemble members in live trading:

`H_j = max_t T_j(t)`

then bucketize member/path maxima.

---

# 9. T+0 probability is even simpler

At trade time `t`:

`M_t = observed resolver maximum so far`

For historical residual sample or remaining-path model:

`R_k(t) = possible future maximum from t to end of local day`

Final maximum sample:

`H_k(t) = max(M_t, R_k(t))`

As the day evolves:

- every bucket below `M_t` becomes impossible;
- probability mass shifts only among `M_t` and higher outcomes;
- after the likely peak, the key probability often reduces to crossing the next integer threshold.

This is the cleanest high-frequency weather edge candidate because uncertainty mechanically collapses during the day.

---

# 10. Station/source versioning is economically necessary

Do not assume one permanent station per city.

Paris is a concrete 2026 example: after anomalous readings at Charles de Gaulle became the subject of a Météo-France complaint/investigation, Polymarket subsequently shifted the Paris temperature resolver to Le Bourget.

Therefore training labels must store per event:

`event_slug`
`event_date`
`resolver_source`
`station_id`
`timezone`
`unit`
`rounding/display rule`

This is not a generalized data-governance requirement. It prevents mixing different physical targets in the same station-error distribution.

---

# 11. Minimal training record

One row per model/event/horizon is enough:

`event_id`
`station`
`event_date`
`model`
`run_initialization`
`estimated_availability_time`
`trade_horizon`
`forecast_daily_max`
`resolver_daily_max`
`error`

For T+0, add snapshots only at economically interesting times:

`running_max`
`current_temp`
`minutes_to_expected_peak`
`latest_model_daily_max`

No broader feature store is required initially.

---

# 12. Best first city/model pairs from supplied-wallet activity

## Milan `LIMC`

Primary historical models:

- ECMWF IFS HRES;
- ItaliaMeteo ICON-2I;
- DWD ICON EU;
- ARPEGE Europe if incremental.

Why: supplied wallet has multiple recovered Milan trades, including one T+1 entry and one losing-bucket exit.

## Madrid `LEMD`

Primary:

- ECMWF IFS;
- DWD ICON EU;
- ARPEGE Europe;
- AEMET observations/direct guidance as live incremental information.

IEM has Madrid METAR history back decades.

## Tel Aviv `LLBG`

Primary:

- ECMWF IFS;
- ICON Global/EU where applicable;
- GFS;
- IMS regional observations/live fields as later incremental predictors.

IEM has LLBG history from 2001.

## Wuhan `ZHHH`

Primary:

- ECMWF IFS;
- CMA GRAPES;
- JMA GSM as independent East Asia global model.

IEM maintains ZHHH observation history.

## Amsterdam `EHAM`

Primary:

- KNMI HARMONIE-AROME;
- ECMWF IFS.

This pair is especially attractive because KNMI exposes direct update notifications and high-resolution regional guidance.

## Paris — use resolver version from each event

Primary current-era pair:

- Météo-France AROME;
- ECMWF IFS.

Do not combine pre- and post-station-change labels without explicit resolver identity.

---

# 13. What would falsify extra complexity

The baseline earns precedence unless another method improves **out-of-sample fee-adjusted PnL**.

Examples:

- if ensemble spread does not improve bucket probabilities beyond empirical deterministic residuals, omit it;
- if five models do not beat ECMWF + best local model, omit the extra models;
- if nonlinear ML does not beat a residual distribution / linear pool, omit ML;
- if market price adds no incremental calibration after weather, λ can go to 1;
- if wallet flow adds no markout after weather+market, omit wallet flow from execution logic.

The intended result is the smallest probability engine that actually improves dollars.

---

# Bottom line

The historical weather side no longer requires a large custom archive.

The minimal faithful chain is:

`Open-Meteo Previous Runs`

`→ station/horizon residual distribution`

`+ Single Runs around important fills`

`+ raw resolver METAR history`

`+ Polymarket fill/price data`

`→ calibrated exact-bucket probabilities`

`→ fee-adjusted trade PnL`.

The recovered Milan fill already provides a concrete event where this chain can test whether a specialist reacted to the fresh ECMWF 18Z revision before the market fully converged.