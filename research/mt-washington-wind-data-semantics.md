# Mt. Washington monthly maximum wind — data and resolver research

Snapshot: **2026-08-13**

## Purpose

This note deepens the non-temperature Weather-market research around monthly maximum wind on Mount Washington, New Hampshire.

The family is attractive for research because it combines:

- one physical summit station;
- a long official archive;
- a running monthly maximum;
- nested threshold questions;
- a specialized local forecast product;
- meaningful prior Polymarket volume.

The immediate goal is to define the exact data objects and historical evidence needed before any profitability claim.

---

## 1. Polymarket settlement object

The July 2026 event asked whether the monthly summit maximum reached a series of thresholds from 85 mph through 115 mph.

The official rule says settlement is based on the highest whole-mile-per-hour wind speed reported by the Mount Washington Observatory in its monthly F6 records.

Official Polymarket event:

- https://polymarket.com/event/highest-mtpt-washington-wind-speed-in-july-20260626193609212

Indexed event volume was approximately $58k.

The rule also specifies a revision cutoff tied to publication of the first datapoint for the following month. Historical labels therefore need to preserve the relevant point-in-time F6 state rather than automatically substitute later archival corrections.

---

## 2. Mathematical structure

Let `W_m` be the maximum summit gust recorded for the month.

For thresholds `K1 < K2`:

`P(W_m >= K1) >= P(W_m >= K2)`

The threshold outcomes therefore share one latent monthly maximum and should not be modeled as unrelated binary events.

At date `t`, define the running maximum:

`M_t = max(observed daily maxima through t)`

The final value can be written:

`W_m = max(M_t, R_t)`

where `R_t` is the maximum of the remaining days.

This is the same one-sided information geometry as daily-high temperature, but over a monthly horizon and with extreme-gust event hazards rather than a diurnal heating cycle.

---

## 3. Observatory current data versus contractual F6 data

Mount Washington Observatory's Weather page currently provides:

- current summit conditions;
- real-time graphs of summit variables;
- wind speed and gust;
- 24-hour/current statistics;
- a regional mesonet;
- links to monthly F6 archives.

Official source:

- https://mountwashington.org/weather/

A 2026 Observatory retrospective notes that its F6 page is updated nightly.

Source:

- https://mountwashington.org/2025-by-the-numbers/

The first resolver-basis study should therefore compare, for every high-wind day:

- real-time/current summit gust;
- any displayed 24-hour maximum;
- nightly F6 daily maximum;
- final monthly F6 maximum;
- revisions before the contract cutoff.

The current conditions page should be treated as a precursor until its historical correspondence to F6 is measured.

---

## 4. Higher Summits Forecast

The Observatory publishes a 48-hour Higher Summits Forecast twice daily, written specifically for high elevations in the Presidential Range.

Official sources:

- https://mountwashington.org/weather/higher-summits-forecast/
- https://mountwashington.org/mwobs-weather-forecasts-expand-beyond-the-higher-summits/

The forecast includes wind information and discussion of relevant storm systems.

This is worth evaluating separately from ordinary gridded guidance because the summit has extreme terrain exposure and strong mountain-wave/pressure-gradient effects.

Useful historical research fields include:

- issue time;
- forecast wind/gust language;
- expected strongest-wind period;
- direction;
- revision from the previous issue;
- observed F6 maximum over the valid period.

The first question is simply whether the Observatory's local forecast materially improves the distribution of subsequent summit gust maxima relative to climatology and broad numerical guidance.

---

## 5. Long historical archive supports a strong prior

The Observatory maintains a substantial weather archive including monthly F6 forms and long-term climate statistics.

Official source:

- https://mountwashington.org/weather/

The 2025 annual summary reported:

- a highest gust of 161 mph;
- 163 days with gusts of at least 73 mph;
- 55 days with gusts of at least 100 mph.

Source:

- https://mountwashington.org/2025-by-the-numbers/

The monthly archive can estimate by calendar month:

- distribution of monthly maximum gust;
- frequency of 85/90/95/100/105/110/115+ mph days;
- timing of the monthly maximum;
- probability of a later higher gust given date and current running maximum.

Month-specific climatology is essential; annual frequencies should not be applied directly to July or August.

---

## 6. Event-driven meteorology

Unlike daily temperature, monthly summit maximum wind is dominated by a relatively small number of high-wind synoptic events.

Relevant event classes include:

- strong fronts;
- deep low-pressure passages;
- nor'easters;
- tropical remnants;
- large pressure-gradient events;
- mountain-wave amplification;
- severe convection.

Research should classify months by the count and intensity of these opportunities rather than assume a smooth normal distribution for the monthly maximum.

A useful historical object is the distribution of the **largest remaining event** conditional on date and the current running maximum.

---

## 7. Numerical guidance basis

Potential comparison sources include:

- Observatory Higher Summits Forecast;
- NWS higher-summits/local guidance;
- ECMWF/GEFS synoptic pressure/wind fields;
- higher-resolution U.S. model guidance near high-wind events.

Raw model-grid wind should not be equated directly to summit gust because terrain/exposure can amplify the observed value substantially.

A station-specific empirical mapping from forecast synoptic state to observed F6 summit gust is a more appropriate baseline.

---

## 8. Historical dataset

For each month:

- daily F6 maximum gust;
- running monthly maximum after each day;
- final monthly maximum;
- threshold-cross dates;
- current-condition precursor values where archived;
- Higher Summits Forecast vintages where available;
- broad model/synoptic state;
- any revisions to the F6 record.

For months with Polymarket markets, additionally preserve:

- threshold market identifiers;
- historical price series;
- event volume/liquidity;
- exact rule/revision cutoff.

This enables separate evaluation of forecast quality, source/publication timing and market behavior.

---

## 9. Research questions

1. How closely do real-time summit gusts reproduce the later F6 daily maximum?
2. How much does the twice-daily Higher Summits Forecast improve the probability distribution of the next 48-hour maximum?
3. How quickly does uncertainty about the final monthly maximum shrink as the month progresses?
4. How often does a new monthly running maximum occur after each calendar date?
5. Are historical threshold-market probabilities coherent with one common distribution over the monthly maximum?
6. How large are point-in-time F6 revisions before the contract cutoff?

---

## 10. Research priority

Evidence grade:

- resolver semantics: strong/explicit;
- running-maximum and nested-threshold structure: exact;
- historical source depth: strong;
- specialized local forecast source: strong;
- prior market capacity: meaningful (~$58k in July);
- market inefficiency: not yet measured.

Priority: **high among non-temperature Weather families**.

It offers a compact, well-defined research problem with one station, one official archive and one latent monthly maximum driving every threshold contract.