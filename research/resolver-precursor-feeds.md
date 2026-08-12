# Direct resolver-precursor feeds — T+0 source-latency alpha

Snapshot: **2026-08-12**

Purpose: identify national/airport observation feeds that can update the eventual Polymarket temperature resolver state earlier or at higher precision than the displayed Wunderground/NOAA history page.

## Verdict

For several high-volume international temperature cities, the most promising T+0 edge is not another forecast model. It is a **faster observation stream at the exact resolver airport**.

The pattern is now concrete:

- Polymarket resolves many daily temperature markets from a named airport and a whole-degree Wunderground/NOAA history page;
- national meteorological agencies often expose the same airport at 1-, 6-, or 10-minute cadence and 0.1°C precision;
- those observations can update the posterior probability of the final whole-degree maximum/minimum before the slower resolver-facing page fully reflects the state;
- the source cannot be treated as contractual truth until its basis to the resolver is measured.

The best immediate candidates found are **Seoul/Incheon, Hong Kong, Singapore, Wellington, Paris, Amsterdam, Helsinki-Vantaa and Munich Airport**.

A live strategy should treat each fast feed as a **resolver precursor**, not as an automatic substitute for the contract source.

---

# 1. Economic object

For event bucket `i`, at receipt of a new direct observation `o_t`:

`q_i(t+) = P(resolver_final_bucket = i | resolver_state_to_t, direct_feed_o_t, weather_remaining)`.

The monetizable signal is:

`delta_q_i = q_i(t+) - q_i(t-)`.

For a taker YES:

`EV_cross = q_i(t+) - executable_ask_i - taker_fee_i`.

For an owned YES exit:

`EV_sell = net_bid_i - q_i(t+)`.

For a passive maker:

- cancel/reprice stale quotes immediately after `delta_q`;
- widen or skew toward the new probability surface;
- measure fill-conditioned adverse selection after every direct-source update.

The direct source is valuable only if its update reaches us before enough of the market price move has occurred to erase the edge.

---

# 2. Why direct high-frequency observations can beat the resolver page

Wunderground states that international airport observations can update at 1-, 3-, or 6-hour intervals depending on the station. National agencies can expose the underlying station much more frequently.

Wunderground data-source description:

https://www.wunderground.com/about/data

Therefore the relevant latency chain can be:

`physical airport temperature`

`-> national automatic observation feed`

`-> METAR/SPECI / GTS reporting`

`-> Wunderground/NOAA history ingestion`

`-> market participants notice/reprice`.

A trader connected near the beginning of this chain can update fair value before traders watching only the resolver page.

But upstream and resolver values can differ because of:

- averaging windows;
- sensor/channel choice;
- rounding;
- QC/revisions;
- report timing;
- source ingestion omissions;
- station/site mismatch.

So the correct object is a learned conditional mapping from precursor state to resolver state.

---

# 3. Priority ranking

Current ranking by likely economic value, combining exact-station match, cadence, precision, historical backtestability, specialist activity and observed market scale.

| Rank | City / resolver | Fast source | Cadence | Exact airport? | Historical depth | Current assessment |
|---:|---|---|---:|---|---|---|
| 1 | Seoul / Incheon `RKSI` | KMA AMOS | **1 min** | **Yes** | since ~2005 | Excellent |
| 2 | Hong Kong / HKG `VHHH` | HKO station feed / running extrema | 1-min means; extrema update ~10 min | **Yes / verify feed row** | strong HKO archive | Excellent |
| 3 | Singapore / Changi | NEA station temperature | up to **1 min**, API refresh ~5 min | likely exact/near airport; verify station ID | API history since 2016 | Excellent |
| 4 | Wellington / `NZWN` | MetService 1-minute observations | **1 min**, ~30–40s ingest | **Yes** | live range ~60d | Excellent but commercial |
| 5 | Paris / current resolver station | Météo-France observations | **6 min** | exact station available if correct resolver regime mapped | extensive | Excellent |
| 6 | Amsterdam / Schiphol `EHAM` | KNMI 10-minute observations | **10 min** + MQTT | airport network | extensive | Very good |
| 7 | Helsinki / Helsinki-Vantaa `EFHK` | FMI open observations | **10 min** | **Yes** | decades / free open data | Very good |
| 8 | Munich / `EDDM` | DWD 10-minute temperature, station 1262 | **10 min** | **Yes** | long historical archive | Very good |
| 9 | Tel Aviv / Ben Gurion `LLBG` | IMS 10-minute API | **10 min** | station mapping must be confirmed | public historical DB | High potential; resolver regime changed |
| 10 | US ASOS airports | NOAA/MADIS One-Minute ASOS | 1-min raw, processed every ~5 min | usually exact ASOS | long public archive | High potential, more basis complexity |
| 11 | Tokyo / Haneda `RJTT` | JMA AMeDAS Haneda | **10 min** / 0.1°C | **Yes** | extensive | Very good |
| 12 | Milan / Malpensa `LIMC` | Italian aviation/national observations | METAR often 30/60 min; faster exact feed not yet found | Yes for METAR | extensive | Lower observation-latency edge; forecast-cycle edge remains strong |

This is a research ranking, not yet a measured PnL ranking. The decisive next statistic is event-level markout after each feed update.

---

# 4. Seoul — strongest exact-station match found

Polymarket Seoul contracts explicitly resolve from:

**Incheon Intl Airport Station, `RKSI`**, whole °C, via Wunderground.

Example official Polymarket market:

https://polymarket.com/event/highest-temperature-in-seoul-on-may-6-2026/highest-temperature-in-seoul-on-may-6-2026-13c

Korea Meteorological Administration APIHub exposes **AMOS minute data** for Incheon Airport:

- station ID: **113 Incheon Airport**;
- production cadence: **minute, hourly, daily**;
- archive: roughly February 2005 onward, station-dependent;
- `TA`: temperature at **0.1°C** precision;
- other fields include humidity, pressure, precipitation and runway wind;
- API key required but KMA states APIHub service is free.

Official endpoint documentation:

https://apihub.kma.go.kr/apiList.do?apiMov=%EA%B8%B0%EC%83%81%EC%B2%AD+AMOS+%EB%A7%A4%EB%B6%84%EC%9E%90%EB%A3%8C+%EC%A1%B0%ED%9A%8C&seqApi=14&seqApiSub=259

This is unusually clean because the fast source is airport-specific and the contract source names the same airport/ICAO.

## Immediate Seoul state variable

Maintain:

`direct_running_max_0.1C`

and estimate:

`P(WU_final_whole_C = k | KMA_AMOS_path, time_of_day, historical_KMA_to_WU_basis)`.

Because the contract resolves at whole degrees, the biggest price changes should cluster when the 0.1°C direct state approaches/crosses a resolver integer boundary or when the climatological heating window closes without crossing it.

## Highest-value Seoul test

Backfill 30–100 resolved Seoul days:

1. minute AMOS path;
2. Wunderground finalized max;
3. Polymarket minute/short-interval price history;
4. timestamp of every first AMOS crossing of `k - 0.5`, `k`, and nearby thresholds;
5. 5s/30s/1m/5m/30m market markout.

If the market is still slow after AMOS updates, Seoul should move to the top of deployment priority.

---

# 5. Hong Kong — direct running-extrema product

Hong Kong Observatory publishes:

- regional/latest **1-minute mean air temperature**;
- running **maximum and minimum since midnight calculated from 1-minute mean temperatures**;
- these running extrema are updated approximately every 10 minutes.

Official HKO open-data documentation:

https://www.hko.gov.hk/en/abouthko/opendata_intro.htm

DATA.GOV.HK running max/min dataset:

https://data.gov.hk/en-data/dataset/hk-hko-rss-current-weather-report

HKO station documentation identifies Hong Kong International Airport as a reference synoptic station with temperature instrumentation.

Polymarket Hong Kong temperature markets use Hong Kong International Airport/Wunderground `VHHH` in the rule set inspected during this research.

This is particularly attractive because the upstream provider already computes the key path-dependent variable:

`running_max_since_midnight`

or

`running_min_since_midnight`.

That removes one reconstruction step.

## Main caveat

Verify the exact HKO row/site identifier used by the open feed and measure its historical basis to Wunderground `VHHH` before equating the values.

If the mapping is stable, Hong Kong could support both daily-high and daily-low T+0 strategies with almost identical code.

---

# 6. Singapore — minute-scale data plus long API history

Singapore's National Environment Agency / data.gov.sg exposes station-level air temperature:

- observations at up to **one-minute intervals**;
- API publication designed to occur automatically as readings are generated;
- API dataset history extending back to roughly **2016**;
- open-data reuse.

Official data.gov.sg dataset:

https://data.gov.sg/datasets/d_91ffc9a8f6756072c0e6a22c68f3fbd1/view

Official collection:

https://data.gov.sg/collections/1459/view

The economic advantage over Wellington is historical depth: a direct precursor-to-resolver basis model can be estimated before live deployment rather than waiting months to accumulate data.

Highest-value task:

- identify the exact Changi airport station ID in the API;
- join minute path to historical Wunderground Changi daily highs;
- measure probability of WU whole-degree bucket conditional on minute-scale NEA running max.

---

# 7. Wellington — fastest observed source, but commercial

Polymarket Wellington contracts inspected in this project resolve from Wellington International Airport `NZWN` on Wunderground.

MetService's 1-Minute Observations API documents:

- exact **1-minute** automatic observations;
- Wellington Airport station `93110 / NZWN`;
- air temperature among available variables;
- observations recorded each minute;
- typical transmission/ingestion around **30–40 seconds** after observation;
- live/history range roughly 60 days;
- currently a commercial data service.

Official MetService API documentation:

https://about.metservice.com/our-company/our-services/data-services/1-minute-observations-api/

This is the clearest sub-minute publication latency found in the city set.

Commercial cost should be evaluated against measured obtainable edge, not rejected a priori. Even a small recurring T+0 edge can justify data cost if Wellington books have adequate frequency/depth.

---

# 8. Paris — six-minute national observations

Météo-France now exposes real-time observations via API at **6-minute frequency** from more than 2,000 stations, with public/free access following France's meteorological open-data expansion.

Official page:

https://meteofrance.com/actualites-et-dossiers/actualites/les-donnees-meteorologiques-de-meteo-france-sont-desormais-libres-et-gratuites

This is high-value for Paris because the project already found a 2026 resolver-source/station regime change. The same Paris label can represent a different physical target across time.

Therefore each event must map:

`event -> resolver station -> Météo-France station ID -> direct feed`.

Do not merge Charles de Gaulle and Le Bourget data into one residual/basis distribution.

Once the current station is correctly mapped, six-minute direct observations plus AROME guidance provide an unusually strong T+0 stack.

---

# 9. Amsterdam — 10-minute airport observations + push notification

KNMI open data provides near-real-time **10-minute automated station observations** from Dutch stations, including airport networks, and exposes update notification through MQTT.

Official KNMI open-data portal/API:

https://developer.dataplatform.knmi.nl/

This matters operationally because the bot need not poll blindly. It can react to a KNMI notification, fetch the newest station row, update `q`, cancel stale quotes and trade.

Amsterdam/Schiphol is therefore attractive even if the raw cadence is slower than Seoul/Wellington: **known arrival time and push notification reduce detection latency**.

---

# 10. Helsinki — free 10-minute exact-airport observations

Polymarket Helsinki contracts explicitly resolve from:

**Helsinki Vantaa Airport, `EFHK`**, whole °C via Wunderground.

Example:

https://polymarket.com/event/highest-temperature-in-helsinki-on-may-9-2026

Finnish Meteorological Institute identifies **Vantaa Helsinki-Vantaa airport** as an observation station and exposes surface weather observations through its Open Data WFS service.

FMI guidance states weather observations such as precipitation are observed at 10-minute cadence, and its climate statistics service documents observation availability at 10-minute resolution depending on station/variable.

Official FMI sources:

https://en.ilmatieteenlaitos.fi/open-data-manual-time-series-data

https://en.ilmatieteenlaitos.fi/guidance-to-observations

https://en.ilmatieteenlaitos.fi/climate-statistics

This is an excellent backtest candidate because the source is free and has long historical archives.

---

# 11. Munich — DWD station 1262 is Munich Airport and has 10-minute temperature

Polymarket Munich contracts resolve from:

**Munich Airport, `EDDM`**, whole °C via Wunderground.

Example:

https://polymarket.com/event/highest-temperature-in-munich-on-may-10-2026/highest-temperature-in-munich-on-may-10-2026-23c

DWD's station metadata/timeseries identify station ID:

**1262 = München-Flughafen**.

DWD's live 10-minute air-temperature directory includes:

`10minutenwerte_TU_01262_now.zip`.

Official live directory:

https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/now/

DWD also provides `recent` and `historical` 10-minute air-temperature archives.

Historical directory:

https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/historical/

This is a very clean station-matched precursor source and should be tested before spending effort on generic city weather APIs for Munich.

---

# 12. Tel Aviv — potentially strong 10-minute feed, but resolver regime is versioned

Israel Meteorological Service exposes near-real-time automatic observation APIs with:

- 10-minute and some 1-minute data products;
- temperature `TD`;
- maximum/minimum temperature channels;
- API selection by station/channel/time range;
- public historical meteorological databases, including 10-minute data.

Official IMS API:

https://ims.gov.il/en/ObservationDataAPI

Official database metadata:

https://ims.gov.il/en/MetaDataSources

But Tel Aviv requires **strict event-level resolver versioning**.

A March 14 Polymarket contract resolved from Wunderground at Ben Gurion Airport `LLBG`:

https://polymarket.com/event/highest-temperature-in-tel-aviv-on-march-14-2026

By May 12, Polymarket used NOAA's `weather.gov/wrh/timeseries?site=LLBG` as the resolver source instead of Wunderground.

Example:

https://polymarket.com/event/highest-temperature-in-tel-aviv-on-may-12-2026

Therefore the model must not fit one permanent `IMS -> WU` mapping for every Tel Aviv event.

Required event fields:

`resolver_source_family`
`resolver_url`
`station_id`
`rule_version`
`rounding`
`revision_cutoff`.

The supplied wallet has substantial Tel Aviv exposure, so this source-regime handling is directly money-relevant.

---

# 13. US airports — one-minute ASOS is useful but basis is subtle

NOAA/NWS/MADIS provides One-Minute ASOS data for many US stations. Public documentation indicates the feed is processed on a near-real-time basis, while routine METARs are typically much less frequent.

However, NWS documentation explains that ASOS temperature processing uses short-window averaging and that raw one-minute values are not necessarily identical to the official daily extreme/reporting value.

Therefore do **not** use:

`max(raw_1min_temp)`

as if it automatically determines the Polymarket bucket.

Use it as a feature predicting:

- next METAR/SPECI whole-degree temperature;
- official running daily max;
- probability of a threshold crossing before the peak window ends.

This is still highly attractive because US data is public, long-lived and operationally easy to acquire.

---

# 14. Tokyo — JMA Haneda 10-minute data

Polymarket Tokyo markets in the project map to Tokyo Haneda Airport `RJTT`.

JMA publishes Haneda/Amedas observations at roughly **10-minute cadence** with temperature to **0.1°C** on its historical/current observation pages.

JMA AMeDAS documentation:

https://www.jma.go.jp/jma/en/Activities/amedas/amedas.html

This creates the same basic state as Munich/Helsinki:

`direct_running_max_0.1C -> probability of final WU whole-degree bucket`.

A machine-friendly JMA acquisition path should be confirmed before implementation, but the observation itself is already available.

---

# 15. Milan — direct observation latency looks less special; forecast-cycle latency remains stronger

Polymarket Milan contracts resolve from Malpensa Airport `LIMC`.

Example:

https://polymarket.com/event/highest-temperature-in-milan-on-may-12-2026/highest-temperature-in-milan-on-may-12-2026-21c

The Italian Air Force documents airport METAR updates typically hourly or half-hourly and provides access to METAR/TAF products.

Official:

https://www.meteoam.it/it/metar-info

https://www.meteoam.it/it/metar-taf

ItaliaMeteo's MeteoHub provides downloadable observed-network data, but this research has not yet verified an exact Malpensa sub-30-minute station feed comparable to KMA AMOS or MetService 1-minute observations.

Therefore Milan's current highest-confidence source edge remains the already-recovered **ECMWF 18Z forecast-cycle timing**, not a newly proven observation feed.

Do not force every city into the same T+0 architecture.

---

# 16. Minimal probability transform for T+0

Let:

- `D_t` = direct-feed running maximum to time `t`;
- `R_t` = resolver-visible maximum to time `t`;
- `F_t` = distribution of remaining-day future maximum from weather model/residual history;
- `B` = historical direct-to-resolver basis/rounding process.

For each historical analogue/sample `s`:

`direct_final_s = max(D_t, F_t_s)`.

Map through a sampled/empirical source basis:

`resolver_final_s = g_source(direct_final_s, B_s)`.

Then:

`q_i = mean(bucket(resolver_final_s) == i)`.

This is safer than hard-rounding the latest direct temperature.

As empirical evidence accumulates and the basis proves deterministic, `g_source` can simplify.

---

# 17. Threshold-event triggers

Polling every feed continuously is unnecessary if the fair distribution barely changes.

Highest-value triggers:

1. first direct running max enters a new 0.1°C band near an integer boundary;
2. first direct observation exceeds previous resolver-visible max;
3. new direct max/min after the expected peak window;
4. large 10-minute temperature slope change;
5. cloud/radiation/wind state changes that alter probability of another degree;
6. source-specific observation publication event (e.g. KNMI MQTT);
7. direct feed crosses a threshold while Polymarket ladder remains stale.

At each trigger, save a synchronized full ladder book before any trade decision.

---

# 18. Profitability test — shortest credible experiment

For each candidate city, collect 30–100 event-days, not years of generic weather data.

Per source update:

`event_id`
`station`
`resolver_source`
`direct_source`
`direct_observation_time`
`direct_publication_time`
`our_receipt_time`
`resolver_visible_value`
`running_direct_max/min`
`q_before`
`q_after`
`book_before`
`book_after_1s`
`book_after_5s`
`book_after_30s`
`book_after_1m`
`book_after_5m`
`final_resolver_bucket`.

Outputs:

- probability calibration;
- median market response lag;
- share of updates where `delta_q` exceeds taker fee+spread;
- profitable depth before convergence;
- maker adverse selection if quotes were resting;
- net dollars/event;
- net dollars/$1,000 capital-hour.

The correct city ranking is then empirical:

`T0SourceScore = net executable PnL/day × capacity × opportunity frequency`.

---

# 19. Execution architecture implied by the source edge

The smallest live process is one event loop:

`new direct observation`

`-> update source-normalized resolver state`

`-> recompute full ladder q`

`-> cancel stale maker quotes`

`-> if large fast edge: cross positive-EV book depth`

`-> otherwise repost passive quotes around q`

`-> record markout`.

No separate city microservice is economically necessary. Each city only needs a tiny source adapter plus a resolver mapping.

---

# 20. What could make this edge persist

The structural persistence argument is stronger than generic 'weather is underfollowed':

- contract settlement uses a specific resolver source, while weather professionals commonly optimize for meteorological truth rather than contractual data lineage;
- many casual traders watch model forecasts or the Polymarket page, not national station feeds;
- national APIs are heterogeneous across languages/authentication/formats;
- source cadence and rounding differ city by city;
- the most important updates occur only during a short local peak window;
- integrating source publication time with CLOB execution is operationally annoying but technically simple;
- edge can coexist with expert specialists because the market has many simultaneous cities and short-lived updates.

The likely decay mechanism is straightforward: once several bots consume the same high-frequency feed and react within seconds, market response half-life falls and taker capture disappears. Maker protection still retains value because the feed prevents stale passive quotes.

---

# 21. Current highest-value implementation order

Based on exact-source quality rather than architectural convenience:

1. **Seoul / KMA Incheon AMOS minute data** — exact resolver airport, minute cadence, long history;
2. **Hong Kong / HKO running extrema** — direct extrema product and high specialist activity;
3. **Singapore / NEA minute temperature** — long historical API and fast cadence;
4. **Munich / DWD 10-minute airport station** — exact station + excellent archive; easiest clean historical replay;
5. **Helsinki / FMI 10-minute airport observations** — same reason;
6. **Wellington / MetService 1-minute** — highest feed speed but paid data and only ~60d direct API retention;
7. **Paris / Météo-France 6-minute** — high-value but station-regime versioning must be exact;
8. **Amsterdam / KNMI 10-minute + MQTT** — good push-driven execution candidate;
9. **Tel Aviv / IMS 10-minute** — very relevant to supplied wallet but first map resolver regime and exact station basis;
10. **Milan** — prioritize forecast-cycle edge until a faster exact Malpensa feed is verified.

This ordering should be changed only by measured market response/capacity.

---

# Bottom line

The strongest new T+0 formulation is:

> **Trade the contract's future resolver value using the fastest trustworthy observation stream from the same airport, not the slowest webpage named in the resolution rule.**

For several international cities, that means minute-to-10-minute national airport data with 0.1°C precision feeding a calibrated mapping to the finalized whole-degree resolver value.

Seoul is the cleanest new case: Polymarket names Incheon `RKSI`, and KMA exposes minute-by-minute AMOS temperature from Incheon itself. This deserves a production-fidelity event study before adding more forecast-model complexity.