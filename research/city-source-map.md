# City source map — beat generic weather with resolver-specific local data

Snapshot: **2026-08-11**

This file maps the most relevant city-temperature markets to the exact Polymarket resolver and the highest-value local/direct weather sources found in the second research pass.

The core trading hypothesis is:

> **A local source only matters if it either predicts the exact resolver better or reaches us earlier than the sources the marginal trader uses.**

For each city the useful object is:

`local_source_alpha = incremental resolver skill × information lead × market spread/depth`.

Exact resolver rules must still be parsed per event because Polymarket has changed source conventions in some cities over time.

---

# Tier A — supplied-wallet cities with strong direct-source advantages

## Tel Aviv — Ben Gurion `LLBG`

### Current resolver

Current 2026 Polymarket rules inspected for Tel Aviv resolve from NOAA WRH time-series data for **Ben Gurion Airport `LLBG`**, using the highest reading under the `Temp` column, whole °C, with revisions accepted until the first datapoint of the following date is published.

Example:
https://polymarket.com/event/highest-temperature-in-tel-aviv-on-june-3-2026

### Direct observation stack

1. **NOAA WRH `LLBG`** — contract source itself.
2. **AviationWeather METAR/SPECI** — likely upstream airport observation stream and therefore useful before/alongside the WRH presentation layer.
3. **Israel Meteorological Service** — 1/10-minute automatic observations from ~85 stations, including `TD`, `TDMax`, radiation, humidity and wind; useful as dense local covariates even when the station is not the contract's LLBG resolver.

IMS API:
https://ims.gov.il/en/ObservationDataAPI

IMS current XML:
https://ims.gov.il/en/CurrentDataXML

Important timing detail: IMS ten-minute XML updates every 10 minutes but enters the system about 30 minutes after observation; hourly XML arrives about half an hour after the round hour. The API is described as near-real-time and should be latency-benchmarked separately.

### Alpha hypotheses

- exact `LLBG` METAR/NOAA value versus generic Tel Aviv forecast;
- boundary-crossing probability conditioned on Ben Gurion observation trajectory;
- IMS radiation/wind/temperature field as predictor of near-future LLBG heating/cooling;
- WRH publication lag after upstream aviation observation;
- sea-breeze onset timing as a city-specific peak-capping feature.

### Why high priority

The supplied wallet has large Tel Aviv positions on both T+0 and T+1, making this city directly relevant to reverse-engineering a profitable active strategy.

---

## Amsterdam — Schiphol `EHAM`

### Resolver

Polymarket 2026 markets inspected resolve on **Amsterdam Airport Schiphol `EHAM`** via Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-amsterdam-on-may-16-2026

### Direct forecast stack

**KNMI HARMONIE-AROME Cy43 EPS** is unusually attractive:

- operational regional ensemble;
- hourly output frequency;
- covers the Netherlands/Europe;
- open data API;
- MQTT update notifications;
- current datasets retained as a rolling operational feed.

Europe EPS:
https://dataplatform.knmi.nl/en/dataset/harmonie-arome-cy43-p4a-1-0

The KNMI platform also offers reforecast/historical HARMONIE products, which are valuable for station-specific calibration.

### Observation stack

- exact Schiphol METAR/SPECI through aviation feeds;
- KNMI station data where available;
- Wunderground only as the decisive display layer.

### Alpha hypotheses

- direct HARMONIE-EPS probability shock before generic ECMWF/Open-Meteo repricing;
- MQTT notification gives a clean first-availability trigger;
- Schiphol marine/cloud/wind regime calibration can outperform generic Dutch-city forecasts;
- ensemble member daily maxima + exact EHAM observation conditioning.

### Why high priority

The supplied wallet holds Amsterdam exact-bucket positions, and KNMI supplies an unusually good combination of local ensemble + machine-readable update notifications.

---

## Madrid — Barajas `LEMD`

### Resolver

Polymarket markets inspected resolve on **Adolfo Suárez Madrid-Barajas `LEMD`** through Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-madrid-on-may-6-2026

### Direct source stack

**AEMET OpenData** exposes a REST API with:

- current conventional observations for all stations;
- current observations by station ID;
- hourly municipality forecasts;
- daily municipality forecasts;
- daily climatological values by station;
- station inventory and extremes.

Swagger/API:
https://opendata.aemet.es/dist/

### Alpha hypotheses

- exact AEMET station observation versus Wunderground update timing;
- resolver-specific historical daily maxima directly from AEMET for calibration;
- Spanish high-temperature bias/peak timing by synoptic regime;
- AEMET forecast/post-processing as independent feature versus ECMWF/ICON.

### Why high priority

The supplied wallet has a large Madrid T+1 modal-bucket position. A direct official observation API makes this one of the easiest international cities to calibrate properly.

---

## Milan — Malpensa `LIMC`

### Resolver

Polymarket markets inspected resolve on **Malpensa International `LIMC`** via Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-milan-on-may-9-2026

### Direct Italian forecast stack

**ItaliaMeteo / MeteoHub** exposes operational model products and APIs.

Most interesting:

### ICON-2I

- 2.2 km grid over Italy;
- ECMWF IFS-HRES boundary conditions;
- KENDA-LETKF initialization/assimilation;
- incorporates SYNOP, TEMP and aircraft observations from the Italian Air Force weather service;
- produced twice daily;
- accessible through MeteoHub API/GRIB.

Dataset:
https://www.dati.gov.it/node/view-dataset/dataset?id=9e46be8d-2da2-44e0-a635-98cbb40dc4ef

### Other ItaliaMeteo products

MeteoHub also exposes WRF and BOLAM/MOLOCH operational forecasts plus national observation data.

### Alpha hypotheses

- ICON-2I local boundary-layer forecast versus ECMWF/Open-Meteo consensus;
- exact `LIMC` aviation observation conditioning;
- Po Valley heating/cloud/advection regime-specific station bias;
- MeteoHub local model update before aggregator reflection.

### Why high priority

The supplied wallet's Milan 36°C T+0 position was one of its visible large winners.

---

## Paris — Le Bourget `LFPB`

### Resolver

Current 2026 markets inspected resolve on **Paris-Le Bourget `LFPB`**, not Charles de Gaulle, through Wunderground, whole °C.

This station distinction has already caused bugs in public trading projects.

### Direct French forecast stack

Météo-France's current operational models:

### AROME

- regional France model;
- current grid roughly **1.3 km**;
- designed for fine/local phenomena;
- current 2026 chain increased assimilated observations and ensemble scenarios;
- public AROME/ARPEGE real-time outputs are now freely accessible through `meteo.data.gouv`.

### ARPEGE

- Météo-France global model;
- fine resolution over Europe;
- useful as independent large-scale input.

Météo-France 2026 chain update:
https://meteofrance.com/presse/des-modeles-meteorologiques-plus-performants

### Alpha hypotheses

- exact `LFPB` aviation observation rather than generic Paris/CDG;
- AROME 1.3 km path/peak versus global-model mean;
- local urban/heating and cloud timing calibration;
- direct model availability versus aggregator update delay.

### Why high priority

The resolver/station error is already demonstrated in public bot history, and the supplied wallet actively trades Paris.

---

## Wuhan — Tianhe `ZHHH`

### Resolver

Current Polymarket markets inspected resolve on **Wuhan Tianhe `ZHHH`** through Wunderground, whole °C.

### Direct Chinese forecast stack

CMA currently describes:

- **CMA-GFS** global model at 12.5 km;
- **CMA-MESO** regional model at **1 km with one-hour updates**;
- ensemble forecasting at roughly 10 km over China.

Official CMA forecast/NWP overview:
https://www.cma.gov.cn/en/forecast/

CMA's National Meteorological Information Centre also exposes historical surface observation datasets through its data service platform.

### Alpha hypotheses

- 1 km hourly CMA-MESO revisions versus slower global/aggregator updates;
- exact ZHHH METAR conditioning;
- East Asian convection/cloud timing near the daily peak;
- local model forecast boundary crossings before Western forecast APIs update.

### Why high priority

The supplied wallet held a large Wuhan next-day modal bucket. Hourly 1 km local NWP makes this one of the strongest direct-source asymmetry candidates found.

---

## Shanghai — Pudong `ZSPD`

### Resolver

Current high- and low-temperature Polymarket rules inspected use **Shanghai Pudong `ZSPD`** through Wunderground, whole °C.

### Direct source stack

Same CMA stack as Wuhan:

- CMA-MESO 1 km/hourly;
- CMA-GFS;
- China-region ensemble;
- exact airport METAR/SPECI.

### Alpha hypotheses

- Pudong coastal/sea-breeze regime can differ materially from generic Shanghai urban forecast;
- local 1 km model should have particular value in sea-breeze onset/low-cloud regimes;
- daily low contracts provide a second signal using overnight minimum-path math.

### Why high priority

Shanghai appears in the supplied wallet and now has both high and low markets, increasing reuse of city calibration.

---

# Tier B — strong official/local data and/or clean resolver feed

## Singapore — Changi `WSSS`

### Resolver

Polymarket 2026 markets resolve on **Singapore Changi `WSSS`** via Wunderground, whole °C, with finalization tied to the next date's first datapoint in newer rules.

Example:
https://polymarket.com/event/highest-temperature-in-singapore-on-june-21-2026

### Direct data

Meteorological Service Singapore publishes current observations from automated instruments and states they are automatically published as they are generated. Changi aviation METAR/SPECI is also directly accessible.

MSS current observations:
https://www.weather.gov.sg/weather-currentobservations-rainfall/

### Alpha hypotheses

- exact WSSS METAR plus local MSS observations;
- cloud/convection timing is the dominant daily-high cap in equatorial Singapore;
- use radar/rain onset to update probability that heating has ended;
- same-day boundary survival around 31/32/33°C;
- local observation publication before Wunderground daily history updates.

### Why high priority

Singapore is a high-volume recurring market and appears in the supplied wallet.

---

## Wellington — Wellington Intl `NZWN`

### Resolver

Polymarket 2026 markets inspected resolve on **Wellington International `NZWN`** via Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-wellington-on-may-6-2026

### Direct source stack

MetService exposes WMO WIS2 machine-readable feeds including **hourly SYNOP observations** and notifications. NIWA/Earth Sciences NZ DataHub provides long historical climate-station datasets useful for calibration, including hourly station data products.

MetService WIS2 SYNOP metadata:
https://wis2.metservice.com/oapi/collections/discovery-metadata/items/urn%3Awmo%3Amd%3Anz-metservice%3Asurface-based-observations.synop?f=html

NIWA hourly station archive:
https://data.niwa.co.nz/products/climate-station-hourly

### Alpha hypotheses

- direct `NZWN` aviation observation plus MetService WIS2;
- Wellington's extreme wind/topographic regime requires city-specific forecast errors rather than generic MAE;
- peak temperature can be advection-driven rather than fixed near 14:00;
- use wind-direction regime as a strong conditional feature.

---

## Karachi — Masroor `OPKC`

### Resolver

Polymarket markets inspected resolve on **Masroor Airbase `OPKC`** via Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-karachi-on-may-7-2026

### Direct source stack

Pakistan Meteorological Department's Regional Meteorological Center Karachi explicitly provides airport aviation products including:

- **METAR and SPECI hourly and half-hourly**;
- TAF;
- local/area forecasts;
- TREND forecasts;
- airport warnings and upper-air products.

Official PMD Karachi aviation service:
https://rmcsindh.pmd.gov.pk/Services_Aviation.html

### Alpha hypotheses

- direct half-hourly/airport observations versus Wunderground timing;
- Karachi sea-breeze onset strongly determines daily max;
- TAF/TREND/local PMD forecast as a short-range regime feature;
- Masroor differs from generic Karachi/Jinnah forecast location.

### Why high priority

The supplied wallet's Karachi 32°C same-day position was a visible strong winner.

---

## Mexico City — Benito Juárez `MMMX`

### Resolver

Polymarket 2026 markets inspected resolve on **Benito Juárez International `MMMX`** via Wunderground, whole °C.

Example:
https://polymarket.com/event/highest-temperature-in-mexico-city-on-may-17-2026

### Direct source stack

Mexico's Servicio Meteorológico Nacional exposes a municipality forecast web service in JSON, updated roughly every **1 hour 15 minutes**, plus operational WRF/GFS model products.

SMN web service:
https://smn.conagua.gob.mx/es/web-service-api

### Alpha hypotheses

- exact MMMX METAR conditioning at high elevation;
- local convective/cloud onset and dryline/moisture changes;
- SMN forecast update timing versus global aggregator;
- altitude/model-grid station basis.

---

# Tier C — useful local source, machine-readable access less clear in this pass

## Ankara — Esenboğa `LTAC`

### Resolver

Polymarket markets inspected resolve on **Ankara Esenboğa `LTAC`** via Wunderground, whole °C.

### Local source

Turkey's Meteorological General Directorate (`MGM`) maintains official station/climate data and national weather forecasting systems. Machine-readable current-model access was not cleanly established in this research pass.

Official climate/statistics portal:
https://mgm.gov.tr/veridegerlendirme/il-ve-ilceler-istatistik.aspx

### Immediate useful feeds

- exact LTAC METAR/SPECI;
- ECMWF ENS;
- DWD ICON/ICON-EU where coverage is useful;
- MGM official forecast as an independent comparison.

### Alpha hypothesis

Continental dry-air Ankara can produce sharp afternoon peaks; local airport observation plus direct regional model calibration should outperform generic city forecasts.

---

## Istanbul

The supplied wallet's visible same-day Istanbul 27°C position was its largest visible winner in the snapshot.

The exact resolver station should be parsed from the current event rather than inferred from city name. Once identified:

- exact aviation observation is first priority;
- MGM regional forecast/observations are independent features;
- sea-breeze/cloud regime needs station-specific calibration;
- ECMWF/ICON regional forecasts provide the base ensemble.

The size of the visible wallet win makes Istanbul a top target even though the direct MGM API path needs more work.

---

# Direct local source principle for every new city

For each newly listed temperature city, search in this order:

1. **exact Polymarket resolver rule and station/index**;
2. direct resolver/upstream observation;
3. national meteorological service real-time observation API;
4. national/regional high-resolution NWP;
5. national ensemble/post-processing/MOS;
6. ECMWF/DWD/other global-regional ensembles;
7. aggregator as a baseline and competitor proxy.

The edge research then asks two empirical questions:

### Skill

`ΔSkill = resolver log-loss(local stack) - resolver log-loss(generic stack)`.

### Lead

`Δt = time generic stack reflects information - time direct stack first exposes it`.

A city with both positive skill and positive lead deserves disproportionate capital/research attention.

---

# Highest-value city experiments from this map

## 1. Amsterdam

HARMONIE-EPS + MQTT versus ECMWF/Open-Meteo and Polymarket response.

## 2. Wuhan / Shanghai

CMA-MESO hourly 1 km forecast revisions versus market price and generic global feeds.

## 3. Paris

Exact Le Bourget + AROME 1.3 km versus CDG/generic Paris and global models.

## 4. Milan

ICON-2I 2.2 km + exact Malpensa observation versus global models.

## 5. Madrid

AEMET exact-station observations/history + resolver calibration.

## 6. Tel Aviv

Exact LLBG NOAA/METAR state plus dense IMS local radiation/temperature field to predict remaining heating.

## 7. Singapore

WSSS + MSS convection/radar timing for same-day peak lock.

## 8. Karachi

OPKC half-hourly PMD aviation feed + sea-breeze timing.

## 9. Wellington

NZWN + wind-regime calibration and direct WIS2/MetService feeds.

## 10. Mexico City

MMMX + elevation/convective-regime calibration + frequent SMN forecast feed.

The ranking should be replaced by measured expected dollar PnL once synchronized weather/book data is collected.
