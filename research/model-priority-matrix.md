# Model priority matrix — only forecast feeds worth testing

Snapshot: **2026-08-11**

Purpose: rank weather-model inputs by the only questions that matter for the eventual trader:

1. can the model improve the **exact resolver bucket probability**;
2. can its historical runs be reconstructed point-in-time;
3. does it arrive early enough to create a tradable price gap;
4. is the market/city large and recurrent enough to justify the feed.

The intended starting stack is deliberately small:

> **ECMWF + one genuinely local/high-resolution model + the market ladder.**

A third weather model earns a place only if it improves out-of-sample fee-adjusted dollar PnL.

---

# 1. Important model-version rule

Forecast-error distributions are not perfectly stationary because operational NWP systems change.

Two changes directly overlap the supplied wallet's life:

## ECMWF IFS

Open-Meteo's Single Runs archive notes:

- IFS Cycle 49R1 in the earlier archive;
- **Cycle 50R1 from 2026-05-12 06 UTC**.

Source:
https://open-meteo.com/en/docs/single-runs-api

## ItaliaMeteo / Arpae ICON-2I

Arpae changed the operational ICON-2I configuration on **2026-06-17** after operational verification found that excessively dry model soil in summer caused **overestimation of maximum temperatures**.

The change introduced soil-moisture nudging from ICON-EU. Arpae reports extensive verification showing an overall improvement, with the most obvious gains in near-surface variables, especially **2 m temperature and humidity**.

Source:
https://www.arpae.it/it/notizie/previsioni-meteo-nuova-configurazione-per-il-modello-icon-2i

This matters directly: the recovered supplied-wallet Milan June 30 trade was entered **2026-06-29**, only twelve days after the ICON-2I temperature-bias correction went operational.

## Minimal treatment

Do not build a complicated regime model. Use one of:

- residual history **after the latest material model upgrade** when sample size is adequate;
- or rolling recent residuals that naturally forget older model behavior;
- or a simple version indicator / bias offset when history is sparse.

Mixing old and new model bias without adjustment can destroy a one-degree bucket model.

---

# 2. Tier A — best research targets now

These cities combine specialist activity, useful market volume, exact resolver data, and historically reconstructable high-resolution models.

## Milan `LIMC` — highest priority

### Minimal stack

1. **ECMWF IFS HRES 9 km**
2. **ItaliaMeteo/Arpae ICON-2I ~2.2 km**
3. coherent Polymarket ladder

Secondary only if incremental:

- DWD ICON-EU;
- Météo-France ARPEGE Europe.

### Why Milan is unusually valuable

- multiple supplied-wallet observations already recovered;
- exact T+1 June 30 BUY has timestamp, price, fee and outcome;
- separate June 25 losing-bucket SELL shows active forecast revision;
- `LIMC` airport truth is reconstructable;
- ICON-2I runs are archived through Open-Meteo from April 2026;
- ICON-2I was specifically corrected for summer Tmax bias days before the recovered trade.

### Model mechanics

Arpae states ICON-2I:

- covers Italy at ~2.2 km;
- runs 00 and 12 UTC;
- forecasts to 72 hours;
- uses continuous data assimilation including WMO/radar observations;
- uses ECMWF boundary conditions.

Open-Meteo:
https://open-meteo.com/en/docs/italia-meteo-arpae-api

Arpae:
https://www.arpae.it/it/temi-ambientali/meteo/previsioni-meteo/previsioni-meteo-modellistiche

### First profitable test

For each Milan event after June 17:

- ECMWF resolver-max probability vector;
- ICON-2I resolver-max probability vector;
- simple average / skill-weighted pool;
- market ladder.

Compare exact-bucket log loss and fee-adjusted PnL.

If ICON-2I does not improve the Milan result after its June update, drop it. No reason to keep a local model on reputation alone.

---

## Amsterdam `EHAM`

### Minimal stack

1. ECMWF IFS HRES
2. **KNMI HARMONIE-AROME Netherlands ~2 km**
3. market ladder

### Why

- supplied wallet actively trades Amsterdam;
- exact Schiphol resolver;
- HARMONIE Netherlands is a true local high-resolution model;
- KNMI publishes machine-readable output frequently;
- Open-Meteo archives the individual runs;
- local Dutch marine/cloud/wind behavior can change the daily peak materially.

KNMI data platform:
https://dataplatform.knmi.nl/dataset/uwcw-extra-lv-ha43-nl-2km-1-0

Open-Meteo archive:
https://open-meteo.com/en/docs/single-runs-api

### Data advantage

The KNMI product exposes 2 m air temperature and delivers new files hourly. That gives both a local-skill hypothesis and a clean release-event clock.

### First test

`ECMWF` vs `HARMONIE` vs `ECMWF+HARMONIE` at EHAM by T+0/T+1.

No extra Dutch models unless this pair leaves obvious residual information.

---

## Paris — current resolver `LFPB`, historical resolver event-versioned

### Minimal stack

1. ECMWF IFS HRES
2. **Météo-France AROME France / AROME HD**
3. market ladder

### Why

Météo-France describes AROME as its fine-scale French model, currently around **1.3 km**, intended to add local detail over global guidance. In March 2026 Météo-France deployed a new forecasting chain and reported overall forecast-quality improvement.

Official descriptions:
https://meteofrance.com/meteo-a-z/les-modeles-de-prevision-meteo
https://meteofrance.com/presse/des-modeles-meteorologiques-plus-performants

Open-Meteo archives AROME runs from April 2, 2026.

### Resolver issue

Use the station named by each event's rules. Paris changed resolver station in 2026, so one timeless “Paris error” series is invalid.

### First test

AROME versus ECMWF on exact airport daily-max buckets, separately for each resolver station/version.

---

## Munich / Warsaw / Central Europe

### Minimal stack

1. ECMWF IFS HRES
2. best station-covering high-resolution regional model from the archive
3. market ladder

Candidates:

- DWD ICON-EU / ICON-D2;
- CHMI ALADIN Central Europe;
- GeoSphere AROME Austria where geography fits.

### Why

These cities recur in Poligarch and supplied-wallet activity, and Central Europe has unusually rich run-level historical model coverage.

Select the local model empirically by station/horizon bucket loss; do not average all regional models by default.

---

# 3. Tier A-live — highly attractive national model, historical replay less frictionless

## Tel Aviv `LLBG`

### Historical baseline

1. ECMWF IFS HRES
2. exact LLBG observation state
3. market ladder

Optional independent global model only if it adds information.

### High-value live model: IMS ICON-IL / ICON-LAM

Israel Meteorological Service publishes:

- ~2.5 km regional model;
- 90-hour horizon;
- 00Z and 12Z cycles;
- IFS deterministic boundary conditions;
- initial maps around **06:10 / 18:10 UTC**;
- complete 90-hour maps around **07:45 / 19:45 UTC**.

Official source:
https://ims.gov.il/en/ICON_LAM

### Actual verification evidence

IMS's model-verification report for 2022 compared ICON-IL with IFS, GFS, UKMO, ICON-GL and COSMO-IL, verified against 81 stations. IMS reports that **ICON-IL had the best temperature forecast performance across the year** in that comparison.

That makes ICON-IL a first-class live input for Tel Aviv, not merely a “local models should be better” assumption.

### Why high priority

The supplied wallet has large T+0 and T+1 Tel Aviv positions, including a $600 two-bucket Aug 12 distribution.

### First live event study

Record Tel Aviv ladder probabilities immediately before and after:

- ~06:10 first ICON-IL maps;
- ~07:45 complete 00Z run;
- ~18:10 first 12Z maps;
- ~19:45 complete 12Z run.

Test whether the local model moves fair probability before the market reprices.

---

## Madrid `LEMD`

### Historical baseline

1. ECMWF IFS HRES
2. DWD ICON-EU or Météo-France ARPEGE Europe
3. market ladder

### High-value live model: AEMET HARMONIE-AROME

AEMET documents HARMONIE-AROME as:

- non-hydrostatic convection-permitting model;
- **2.5 km** grid;
- 48-hour horizon;
- cycles **00, 06, 12, 18 UTC**;
- with surface 2 m temperature products.

Official source:
https://www.aemet.es/es/eltiempo/prediccion/modelosnumericos/harmonie_arome/ayuda

AEMET specifically describes local temperature as a variable that benefits from this higher-resolution system.

### Why high priority

The supplied wallet's Madrid Aug 12 38°C position entered near 31.5¢ and later repriced dramatically higher in the inspected snapshot.

### Economic approach

Do not delay historical Madrid research while searching for a perfect HARMONIE archive. Establish the baseline with replayable models, and save each AEMET HARMONIE run from the moment live collection starts. Test its incremental PnL directly.

---

# 4. Tier B — scientifically strong, data-access economics decide inclusion

## Singapore `WSSS`

### Minimal baseline

1. ECMWF IFS
2. exact Changi observation state
3. market ladder

### Local model

Singapore's SINGV system is designed specifically for tropical convection around Singapore:

- ~1.5 km;
- 48-hour forecasts;
- eight runs/day;
- regional observation assimilation.

Official source:
https://ccrs.weather.gov.sg/singv-%E2%94%80-a-tropical-convective-scale-nwpnowcasting-capability-for-singapore/

### Priority logic

SINGV is scientifically attractive, but same-day Singapore may obtain most incremental PnL from **current Changi temperature + radar/cloud/rain onset** because convection terminates heating abruptly.

Test observation-conditioned T+0 first. Add raw SINGV only if it materially changes bucket probabilities beyond that baseline.

---

## Wellington `NZWN`

### Baseline

1. ECMWF IFS
2. exact NZWN observation state
3. market ladder

### Local models

Earth Sciences New Zealand / NIWA lists:

- NZCSM ~1.5 km, 48 h, four runs/day;
- NZENS 18-member ensemble ~4.4 km, five days;
- blended operational forecasting products.

Source:
https://niwa.co.nz/climate-and-weather/weather-and-climate-forecasting-services/weather-and-climate-forecasting-data-services

### Inclusion rule

Wellington's wind/topography can make local models valuable, but the feed is worth operational work only if ECMWF+station calibration leaves profitable unexplained error.

---

# 5. China — separate historical baseline from better live local guidance

## Wuhan `ZHHH` / Shanghai `ZSPD`

### Historically reconstructable baseline

1. ECMWF IFS HRES
2. **CMA GRAPES Global ~15 km**
3. exact airport observations
4. market ladder

Open-Meteo archives `cma_grapes_global` run-by-run.

### Higher-value live candidate

CMA describes **CMA-MESO around 1 km with hourly updates** in its operational system.

That should be more relevant to convection/cloud/sea-breeze timing than the 15 km global model, but it is not the same easy historical archive.

### Minimal approach

Prove whether the city/horizon is profitable with ECMWF + GRAPES + station state first. Then test CMA-MESO live as incremental information. Do not block the strategy on it.

---

# 6. US daily-temperature markets

For US airports, start with the tools specifically built for station-level short-range forecasting rather than a generic multi-global blend.

### Minimal stack

1. exact resolver airport;
2. **NBM probabilistic temperature/extrema guidance**;
3. **LAMP station-specific guidance** for short horizons;
4. HRRR remaining-path evolution where useful;
5. market ladder.

ECMWF is optional independent information, not automatically the center of the US stack.

### Priority

The supplied wallet's visible portfolio is overwhelmingly international 1°C buckets. US markets are likely more heavily automated around NOAA feeds, so international source asymmetry remains the first research focus.

---

# 7. Historical reconstructability ranking

| City/region | ECMWF replay | Local-model replay | Exact observations | Wallet evidence | Priority |
|---|---|---|---|---|---|
| Milan | excellent | ICON-2I excellent from Apr 2026 | strong | multiple recovered fills | **1** |
| Amsterdam | excellent | KNMI HARMONIE excellent | strong | active position | **2** |
| Paris | excellent | AROME excellent from Apr 2026 | strong | active position | **3** |
| Munich/Warsaw | excellent | strong Central-Europe archive | strong | specialist activity | **4** |
| Tel Aviv | excellent | local model best live; replay harder | strong | very large active exposure | **5 / top live** |
| Madrid | excellent | local HARMONIE live; replay less direct | excellent | strong markout case | **6 / top live** |
| Wuhan/Shanghai | excellent | GRAPES global replay; local MESO live harder | strong | active positions | **7** |
| Singapore | excellent | SINGV access less frictionless | strong | active position | **8** |
| Wellington | excellent | NZCSM/NZENS access service | strong | active position | **9** |

This ranking is for **research information per unit of work**, not a permanent capital allocation.

---

# 8. Minimal model-selection experiment

For each station and horizon, evaluate only these variants first:

1. market ladder alone;
2. ECMWF residual distribution alone;
3. local-model residual distribution alone;
4. 50/50 ECMWF + local;
5. skill-weighted ECMWF + local;
6. best weather model blended with market prior.

Metrics:

- exact-bucket log loss;
- Brier score;
- calibration by probability band;
- **fee-adjusted executable PnL** at historical prices where available;
- PnL concentrated by station/horizon/price band.

The winner is the smallest model with the highest credible dollar PnL.

---

# 9. Why model-version breaks matter specifically to money

The expected edge can be only 5–10 probability points on many trades.

A stale +1°C summer Tmax bias learned from an old model version can move most of the probability mass into the wrong 1°C bucket and erase far more than the trading edge.

Therefore version handling is not infrastructure ceremony. It changes orders.

The simplest correct solution is **recent/version-consistent residual calibration**.

For Milan after June 17, begin by measuring post-update ICON-2I errors separately. For ECMWF after May 12, separately inspect Cycle 50R1 residuals before pooling older Cycle 49R1 history.

---

# Bottom line

The forecast research should not become a model zoo.

For the highest-value international markets, the default question is:

> **Does the best local high-resolution model add executable bucket-probability edge beyond ECMWF and the market?**

Milan, Amsterdam and Paris let us answer that historically right now. Tel Aviv and Madrid offer unusually attractive live local-model timing tests. Everything else is secondary until these simple pairs are measured.