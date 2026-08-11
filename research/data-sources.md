# Data sources — ranked by trading value

Snapshot: **2026-08-11**

A weather feed is valuable when it improves the probability of the exact resolver outcome **before the market incorporates it**. Resolution, latency, historical availability, spatial alignment and update timing matter more than brand prestige.

The data stack is therefore organized around four questions:

1. What source actually determines settlement?
2. What upstream observation reaches us earliest and at highest useful precision?
3. What forecast product best predicts the resolver state at this horizon?
4. Can we reconstruct the same data point-in-time historically?

---

# 1. Polymarket market and wallet data

## Gamma API — event discovery and rules

Use for:

- active/closed event discovery;
- titles/descriptions;
- outcome lists;
- token IDs;
- condition IDs;
- event grouping;
- resolution rules/URLs when exposed;
- `feesEnabled` / negative-risk metadata where present.

Base:
`https://gamma-api.polymarket.com`

Trading use: build the event/resolver catalog and parse exact city, date, unit, bucket, station/source and revision rule.

## CLOB API / WebSocket — executable market state

Base:
`https://clob.polymarket.com`

WebSocket:
`wss://ws-subscriptions-clob.polymarket.com`

Collect:

- best bid/ask;
- full depth;
- tick size;
- last trade;
- market status;
- fee rate;
- real-time book changes.

The displayed Polymarket probability is not a substitute for the executable book. UI price is normally midpoint and can display last trade when spread exceeds $0.10.

Primary docs:
- https://docs.polymarket.com/developers/CLOB/introduction
- https://docs.polymarket.com/concepts/prices-orderbook

## Data API — specialist-wallet and position research

Base:
`https://data-api.polymarket.com`

High-value endpoints:

- `/trades?user=<wallet>&takerOnly=false`
- `/positions?user=<wallet>`
- `/closed-positions?user=<wallet>`
- `/activity?user=<wallet>`
- leaderboard endpoints / WEATHER filters

Trade endpoint can return up to 10,000 fills per request and can include maker fills with `takerOnly=false`.

Trading use:

- reconstruct specialist entry timing;
- realized PnL by segment;
- price-band behavior;
- near-term markout;
- wallet consensus factors.

Docs:
https://docs.polymarket.com/market-data/overview

## Historical market data

The first collector should persist our own CLOB snapshots/WebSocket updates because precise historical depth is disproportionately valuable for execution and release-latency studies.

Useful public/research datasets can supplement older periods, but our own stream gives exact schema/timing control for forward evidence.

---

# 2. Settlement-source layer

## Contract rules are the resolver registry

Each event must store:

- resolver source family;
- exact station/location;
- source URL or identifier;
- local civil-day definition;
- metric: high/low/precip/wind/anomaly;
- native unit;
- source precision;
- bucket boundaries;
- rounding convention;
- publication/revision cutoff.

Examples observed in 2026 Polymarket rules:

- Paris high → Wunderground Daily Observations, Paris-Le Bourget `LFPB`;
- Wuhan high → Wunderground, Wuhan Tianhe `ZHHH`;
- Shanghai high/low → Wunderground, Pudong `ZSPD`;
- Ankara high → Wunderground, Esenboğa `LTAC`;
- Tel Aviv high → NOAA WRH station data, Ben Gurion `LLBG` in current rules;
- Hong Kong low → Hong Kong Observatory Daily Extract, Absolute Daily Min;
- NYC monthly precipitation → NOAA Central Park monthly summarized precipitation;
- Mt Washington monthly highest wind → Mount Washington Observatory F6;
- global monthly temperature anomaly → NASA GISTEMP.

The resolver registry should be versioned by event/date because source conventions can change.

---

# 3. Real-time observations: highest-value T+0 inputs

## AviationWeather METAR/SPECI

Official US aviation weather API:
`https://aviationweather.gov/data/api/`

Useful for airport-based resolver stations worldwide where METAR/SPECI observations mirror or closely feed Wunderground.

Capture:

- raw METAR text;
- observation timestamp;
- temperature/dew point;
- special reports;
- encoded T-group when available;
- max/min groups where present.

Trading value: live `M_t`/`m_t` for same-day extrema and model-error conditioning.

## Iowa Environmental Mesonet ASOS/AWOS archive

IEM provides rich station observation history and explicitly documents wagering/reconstruction issues for ASOS temperatures.

Key economic detail for US Fahrenheit markets: routine METAR temperature often carries whole-°C precision, while the official US ASOS temperature process/derived extrema can preserve different precision/rounding. IEM uses higher-precision T-groups and special/max-temperature reports when available.

Trading value:

- resolver-faithful historical daily extrema;
- US rounding/bucket reconstruction;
- long archive for station-specific calibration.

References:
- https://mesonet.agron.iastate.edu/
- IEM ASOS network/download documentation and “Wagering on ASOS Temperatures” notes.

## Hong Kong Observatory direct open data

HKO exposes machine-readable APIs and open datasets. Particularly valuable:

- regional latest 1-minute mean temperature;
- regional max/min since midnight from 1-minute mean temperatures, updated every 10 minutes;
- current/local forecasts;
- daily max/min historical climate datasets;
- rainfall and wind products.

This is a major advantage over generic aggregators when Polymarket resolves directly from HKO.

Official index:
https://www.hko.gov.hk/en/abouthko/opendata_intro.htm

HKO also operates a 10 km non-hydrostatic NWP model updated four times daily and publishes location-specific forecast products that incorporate real-time local observations.

## Korea Meteorological Administration direct data

KMA API Hub provides:

- ASOS surface observations;
- AWS observations at hundreds of sites;
- minute/hour/day data;
- station metadata;
- numerical-model products, including KIM APIs.

For Seoul/Korean contracts, compare exact Polymarket resolver semantics against KMA's direct station observations rather than assuming airport METAR is the best representation.

Official:
- https://apihub.kma.go.kr/
- https://data.kma.go.kr/

## Local/national source principle

For every international city, search for the national meteorological agency's direct observations before accepting an aggregator. Local agencies can offer:

- higher temporal resolution;
- exact station metadata;
- post-processed local forecasts;
- earlier/extrema-specific products;
- different rounding/quality-control behavior.

The expected edge is largest where the public market habitually references Wunderground/Open-Meteo while a direct national feed exposes cleaner or earlier state.

---

# 4. US probabilistic and station forecast stack

## NOAA LAMP

Localized Aviation MOS Program is unusually aligned with airport temperature markets.

Properties:

- station-specific;
- updated hourly for most elements;
- uses recent observations plus model/MOS inputs;
- temperature guidance to roughly 38 hours;
- nominal availability around HH:30 for hourly cycles.

Trading value:

- T+0/T+1 station forecast;
- observation-conditioned short-range changes;
- precise release event for latency study.

Official:
https://vlab.noaa.gov/web/mdl/lamp

## NOAA National Blend of Models (NBM)

NBM provides probabilistic MaxT fields including:

- mean;
- standard deviation;
- percentiles;
- threshold/exceedance probabilities.

The blend can incorporate very large member counts and is closer to the contract's required probability object than a single deterministic high.

Trading value:

- calibrated prior distribution for US daily highs/lows;
- tails and bucket probabilities;
- comparison baseline against our own ensemble calibration.

Official:
https://vlab.noaa.gov/web/mdl/nbm-weather-elements

## HRRR / HREF

HRRR:

- high-resolution deterministic short-range US forecast;
- frequent updates;
- useful for temperature path/peak timing.

HREF:

- convection-allowing ensemble guidance;
- useful for short-range spread/regime uncertainty.

Access via NOAA/NOMADS/AWS and tools such as Herbie for research convenience.

Trading value: path shape and local boundary-layer evolution around T+0 peak.

## GFS MOS

Station-based statistical post-processing of GFS, four cycles/day, useful to roughly 72h.

Trading value:

- calibrated station point guidance;
- independent comparison to raw-grid models;
- release-time event signal.

Official MDL MOS documentation:
https://vlab.noaa.gov/web/mdl/mos

---

# 5. Global ensemble and NWP sources

## ECMWF ENS

Current ensemble structure:

- 50 perturbed members + 1 control;
- 4 cycles/day;
- 00/12 UTC extend to day 15;
- 06/18 UTC shorter horizon;
- roughly 9 km current operational resolution.

Trading use:

- global T+1/T+2 path distribution;
- run-to-run revision shocks;
- member daily maxima at exact resolver coordinates;
- regime spread.

Official:
https://www.ecmwf.int/en/forecasts/dataset/ecmwf-ifs

Open-data documentation:
https://www.ecmwf.int/en/forecasts/datasets/open-data

## DWD ICON family

Germany's DWD publishes direct open GRIB data for:

- ICON global;
- ICON-EU;
- ICON-D2;
- ICON-D2-EPS.

Open directories expose multiple cycles per day; ICON-D2 products are especially attractive for European cities because of high spatial resolution and frequent updates.

Trading value:

- European city T+0/T+1 high-resolution path;
- independent forecast shocks relative to ECMWF;
- ensemble uncertainty where D2-EPS covers the resolver.

Official open-data root:
https://opendata.dwd.de/weather/nwp/

## UK Met Office models

Weather DataHub provides current Met Office model data including:

- global deterministic;
- high-resolution UK deterministic;
- MOGREPS global/UK ensemble products.

Trading value:

- London/UK local forecast specialization;
- independent global ensemble;
- potential release-latency signal.

Official:
https://datahub.metoffice.gov.uk/

## Japan Meteorological Agency MSM

JMA's Meso-Scale Model:

- 5 km grid;
- updated every 3 hours;
- 09/21 JST initializations extend to 78h, intermediate runs to 39h;
- temperature, wind, humidity, precipitation, solar radiation and related fields.

Trading value:

- Tokyo/Japan short-range specialization;
- superior local detail versus a generic global model;
- frequent forecast revisions around the daily peak.

Official data guide:
https://www.data.jma.go.jp/developer/weatherdataguide/appendix/2-2-b.html

## Environment and Climate Change Canada

HRDPS:

- ~2.5 km;
- 48h;
- up to four cycles/day;
- direct open Datamart data;
- post-processed near-surface temperature products also exist.

RDPS:

- ~10 km;
- 84h;
- four cycles/day across North America.

Trading value:

- Toronto/Canadian city specialization;
- high-resolution local temperature path;
- independent information for northern US cities.

Official MSC Open Data / model documentation:
https://eccc-msc.github.io/open-data/

## Hong Kong Observatory NWP/post-processing

HKO's own model covers East Asia at 10 km and updates at 00/06/12/18 UTC. Its public location-specific automatic forecast blends multiple global NWP sources with local real-time observations.

Trading value:

- Hong Kong / Pearl River Delta specialized forecast;
- local bias/post-processing signal unavailable from raw global models alone.

Official:
https://www.hko.gov.hk/en/nhm/prodinfo.htm

---

# 6. Aggregators: fast breadth and benchmark value

## Open-Meteo

Useful for:

- rapid multi-city prototyping;
- simple REST access;
- many deterministic/ensemble models;
- historical forecast endpoints;
- baseline forecast collection.

Its strength is breadth and convenience. The edge research should preserve the underlying model identity/run time rather than collapse everything into `best_match` when model-specific behavior matters.

Trading role:

- baseline/backup;
- global breadth;
- historical point-in-time forecast collection;
- quick cross-check.

## Meteoblue / other commercial forecast APIs

Potentially valuable as independent calibrated forecasts and for city-specific verification statistics. Measure incremental resolver-bucket skill rather than assume superiority.

---

# 7. Climate-index data for GISTEMP markets

## NASA GISTEMP

Settlement target for Polymarket monthly global temperature anomaly contracts.

NASA publishes a scheduled monthly release calendar; August 2026 GISTEMP is scheduled for **September 10, 2026 at 11:00 AM EDT**.

GISTEMP uses:

- GHCN v4 land station data;
- ERSST v5 sea-surface temperature;
- NASA-specific gridding/analysis steps.

Trading value: exact target index and historical basis dataset.

Official:
https://data.giss.nasa.gov/gistemp/

## ERA5 / ERA5T

ERA5T is the preliminary near-real-time ERA5 stream:

- daily data roughly five days behind real time;
- monthly means roughly five days after month-end.

That creates a substantial information lead relative to the scheduled GISTEMP publication date.

Trading value:

- partial/final-month global anomaly proxy;
- historical ERA5→GISTEMP basis model;
- high-capacity monthly bucket nowcast.

Official Copernicus/ECMWF ERA5 documentation.

## NOAA GlobalTemp / Berkeley Earth / ERSST / GHCN

These provide independent or upstream information about global monthly temperature.

Most valuable research question:

> Which combination predicts the first-published GISTEMP number with the smallest historical residual standard deviation at each day of the month / days after month-end?

The relevant output is bucket probability on Polymarket's 0.05°C ranges.

---

# 8. Precipitation and wind-extreme data

## NYC monthly precipitation

If resolution is NOAA Central Park monthly summarized precipitation, collect:

- resolver-aligned precipitation to date;
- official daily/hourly Central Park observations;
- GEFS/ECMWF/NBM ensemble accumulated precipitation for remaining month;
- tropical cyclone / heavy-rain scenario ensembles.

The variable is additive, so every observed rain event permanently shifts bucket support.

## Mt Washington wind maximum

If resolution is Mount Washington Observatory F6:

- daily F6 observations;
- live station gusts where available;
- ECMWF/GFS/GEFS/HREF storm forecasts;
- NHC advisories for tropical systems;
- pressure-gradient predictors.

The variable is a running maximum, so once a threshold is exceeded its contract becomes physically locked.

---

# 9. Source-selection score

Rank each candidate feed for each market segment by:

`DataValue ≈ incremental_resolver_skill × information_lead × market_capacity × availability_reliability`

Useful columns:

- market family;
- city/station;
- source;
- variable;
- native resolution;
- update cycle;
- observed publication latency;
- archive depth;
- resolver match;
- incremental log-loss improvement;
- incremental trading PnL.

This naturally pushes high-value local feeds to the top and relegates redundant feeds to backup status.
