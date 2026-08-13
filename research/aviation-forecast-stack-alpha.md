# Aviation forecast stack alpha

Snapshot: **2026-08-13**

## Research verdict

The project already uses airport observations because many temperature contracts resolve at airports. A less-developed opportunity is to use **airport-native operational forecasts** as an additional information layer.

Two sources stand out:

1. international TAFs, which can include explicit maximum/minimum temperature information and forecast timing in some national regimes;
2. NOAA LAMP for U.S. stations, which updates station-specific 2-meter temperature guidance hourly out to 38 hours.

The key hypothesis is not that aviation forecasts are universally more accurate than NWP. It is that they may contain **local airport information, recent-observation assimilation, human/local calibration or faster updates** that improve the exact resolver distribution.

---

## 1. TAF is an airport-specific operational forecast

Aviation Weather Center describes TAF as a forecast of expected meteorological conditions within 5 statute miles of the airport runway complex.

Official source:

- https://aviationweather.gov/help/data/

TAFs have an explicit issuance timestamp representing when the forecast is completed and ready for transmission. An amended TAF (`TAF AMD`) supersedes the previous forecast immediately.

This makes revisions and amendments clean point-in-time information events.

AWC also provides worldwide TAF API access, with a current complete TAF cache updated every ten minutes.

Source:

- https://aviationweather.gov/data/api/

For latency research, the AWC cache is a convenient reference source, but direct national aviation feeds may publish earlier and should be benchmarked where the event has enough value.

---

## 2. International TAF maximum/minimum temperature fields

TAF conventions differ by country. Some international TAFs include explicit `TX` and `TN` groups identifying forecast maximum/minimum temperature and associated valid time.

This is unusually relevant to exact daily-extreme contracts because the operational forecast directly expresses the variable of interest rather than requiring reconstruction from generic hourly output.

Coverage is heterogeneous. The correct research object is a resolver-airport catalogue:

- resolver ICAO;
- TAF available?;
- `TX/TN` present historically/currently?;
- issuance schedule;
- amendment frequency;
- direct source URL/API;
- AWC ingestion delay;
- historical archive availability.

Do not assume U.S. domestic TAFs have the same TX/TN structure as international products.

---

## 3. TAF revision features

For an airport with useful extrema fields, candidate research features are deliberately small:

- latest `TX`;
- latest `TN`;
- time of forecast maximum/minimum;
- `Delta_TX` versus prior TAF;
- `Delta_TN` versus prior TAF;
- whether the update is routine or amendment;
- cloud/wind/precipitation regime changes in the TAF;
- lead time to the target extreme.

The strongest signal may be **revision**, not absolute forecast value.

For a current bucket distribution `q_before`, define:

`Delta_q_TAF = q_after_TAF - q_before`

Then test whether `Delta_q_TAF` predicts subsequent market repricing or improves final resolver calibration after controlling for the latest model cycle.

---

## 4. Human/local information channel

A TAF can incorporate operational forecaster judgement and local aviation concerns not represented identically in one numerical model.

Potentially relevant daily-max mechanisms include:

- timing of marine-layer clearing;
- fog/low-cloud burnoff;
- frontal passage timing;
- sea-breeze onset;
- convection timing;
- wind-direction shifts;
- cloud-base/coverage changes affecting insolation.

These effects can move an exact airport maximum by one or two narrow buckets even when broad regional guidance is stable.

The empirical question is whether TAF adds information **conditional on** the model stack and market price.

---

## 5. U.S. LAMP is a low-cost station-native layer

NOAA's Localized Aviation MOS Program currently:

- updates most guidance **hourly**;
- covers more than 2,000 stations;
- provides 2-meter temperature forecasts;
- extends temperature guidance hourly from +1 through +38 hours;
- incorporates recent station observations and model/MOS information.

Official sources:

- https://vlab.noaa.gov/web/mdl/lamp
- https://vlab.noaa.gov/web/mdl/lamp-elements
- https://vlab.noaa.gov/web/mdl/lamp-nws-webservices

NOAA documentation also notes that station guidance incorporates information from GFS MOS and, in current versions, HRRR/RAP inputs.

This makes LAMP a natural candidate for U.S. airport resolvers such as KLGA/KORD/KMIA/KDEN.

---

## 6. LAMP research target: remaining-extreme probability

LAMP does not need to replace the full daily forecast model.

Near the daily peak, the economically relevant object is often:

`P(remaining temperature exceeds current running max | current observations, remaining hours)`

For a U.S. airport, compare simple models:

### Baseline

- latest resolver/ASOS state;
- time of day;
- current trend;
- HRRR/NBM or existing model distribution.

### Baseline + LAMP

Add station-specific hourly LAMP trajectory.

Measure improvement in:

- threshold-cross probability calibration;
- winning-bucket Brier/log loss;
- short-horizon market markout prediction.

If LAMP adds no incremental information, do not retain it merely because it is an official product.

---

## 7. Best initial TAF candidates

Priority should follow exact resolver matching and availability of useful TAF extrema fields.

Candidate airports already important elsewhere in the repository include:

- Seoul/Incheon `RKSI`;
- Paris airports after exact resolver regime mapping;
- selected European/Asian airports where operational TAFs include `TX/TN`;
- other international resolver airports discovered by a systematic TAF scan.

The catalogue should be generated from real TAF text rather than hand-maintained assumptions.

---

## 8. Point-in-time archive problem

AWC's current public Data API exposes only a limited recent history window, so long historical TAF-vintage research may require another archive or direct national source.

For forward evidence, raw TAF text is small and should be stored with:

- first-seen timestamp;
- issuance timestamp;
- station;
- raw text;
- parsed TX/TN and timing;
- amendment/routine flag.

This preserves exact forecast vintages and avoids later reconstruction ambiguity.

---

## 9. Decisive tests

### Test A — TAF incremental forecast value

For resolver airports with TX/TN:

1. reconstruct TAF revisions;
2. compare TAF extrema to final resolver value;
3. compare with latest numerical-model probability surface;
4. measure incremental calibration value.

### Test B — TAF revision versus market response

At each routine/amended TAF first-seen time, measure bucket price changes over:

- 5m;
- 15m;
- 30m;
- 1h.

Control for model releases occurring in the same window.

### Test C — LAMP remaining-heating value

For U.S. daily highs/lows, evaluate whether hourly LAMP trajectories improve one-report-ahead or remainder-of-day threshold probabilities over the existing baseline.

---

## 10. Economic priority

Evidence grade:

- **source availability:** strong, official;
- **airport relevance:** strong;
- **incremental forecast skill:** unknown and city-dependent;
- **Polymarket timing edge:** unmeasured.

Why this deserves medium-high priority:

- very low acquisition cost;
- exact station orientation;
- natural point-in-time revisions;
- complements rather than duplicates global models;
- potentially especially useful where one-degree bucket sensitivity is high.

The correct next step is not a complex aviation model. It is a simple question:

> **Does the newest station-native aviation forecast move the resolver probability surface in the correct direction before the market or broader model stack does?**

If yes, retain it as a compact feature/catalyst. If not, discard it.