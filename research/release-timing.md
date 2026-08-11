# Forecast release timing — the information clock

Snapshot: **2026-08-11**

Forecast alpha can only be captured after new information becomes available and before the market incorporates it. This file maps the clocks that matter and converts them into testable latency events.

The key timestamp is **actual first availability**, not nominal model initialization.

For each feed record:

`t_init -> t_first_available -> t_received -> t_fair_value -> t_order -> t_fill`.

Then measure market response from `t_first_available`.

---

# 1. NOAA LAMP — unusually frequent US station signal

Current LAMP v2.7:

- station guidance for 2m temperature and other elements;
- every hour for most variables;
- nominal cycle times **HH:30 UTC**;
- temperature projections every hour to 38 hours;
- built from recent station observations, analyses, simple model output and MOS inputs including GFS/HRRR-derived information.

Official:
- https://vlab.noaa.gov/web/mdl/lamp
- https://vlab.noaa.gov/web/mdl/lamp-elements
- https://vlab.noaa.gov/web/mdl/lamp-nws-webservices

## Trading hypothesis

US airport daily-high markets may reprice around the first appearance of each HH:30 LAMP run, especially when new guidance moves the predicted peak across a 2°F bucket boundary.

Event feature:

`lamp_shock = q_after_lamp - q_before_lamp`.

Measure order-book response through the first 5m/30m after actual file appearance.

---

# 2. NOAA NBM v5.0 — hourly blend plus probabilistic extrema

NBM v5.0 became operational May 5, 2026.

Current text-product availability documentation indicates many cycles arrive approximately **HH:30–HH:40 UTC**, with special cycle timing around 01/07/13/19 UTC. NBM is a calibrated blend of many NWS and non-NWS models and v5.0 substantially expands probabilistic products.

Official:
- https://vlab.noaa.gov/web/mdl/nbm
- https://vlab.noaa.gov/web/mdl/nbm-text-products
- https://vlab.noaa.gov/web/mdl/nbm-download
- https://vlab.noaa.gov/web/mdl/nbm-model-inputs

## Trading hypothesis

The NBM update can be treated as both:

- a direct fair-probability source;
- a compressed signal that several upstream models have changed.

For MaxT/MinT, track changes in mean, spread, percentiles and threshold probabilities.

The strongest event is likely when NBM's modal 2°F resolver bucket shifts while the CLOB still reflects the previous blend.

---

# 3. ECMWF IFS/AIFS — four global information waves per day

Current ECMWF open data has four daily cycles: 00/06/12/18 UTC.

The current dissemination schedule gives approximate availability windows for deterministic atmospheric products:

- 00 UTC run: begins around **05:45 UTC**;
- 06 UTC run: around **11:45 UTC**;
- 12 UTC run: around **17:45 UTC**;
- 18 UTC run: around **23:45 UTC**.

Forecast steps arrive progressively. Current AIFS ensemble schedule begins short-range batch availability around:

- 00 run day-0: ~06:40 UTC;
- 06 run: ~12:40;
- 12 run: ~18:40;
- 18 run: ~00:40.

IFS ensemble/open-product timing should be measured from actual files because public open data is released at the end of ECMWF's real-time dissemination process and product batches differ.

Official:
- https://www.ecmwf.int/en/forecasts/datasets/open-data
- https://confluence.ecmwf.int/spaces/DAC/pages/272310483/Dissemination+schedule

## Trading hypothesis

ECMWF creates globally synchronized repricing opportunities across many city markets. One model shock can be monetized in multiple locations.

A batch-level strategy can:

1. parse only the forecast hours required to determine target-date daily extrema;
2. update all affected city distributions immediately;
3. rank biggest `Δq` relative to current book;
4. execute highest marginal net-dollar opportunities first.

The most valuable cities may be international markets where competitors rely on later aggregators rather than direct ECMWF data.

---

# 4. Met Office — London-specific fast local cycles

Weather DataHub publishes explicit expected model-run availability windows.

Current guidance includes:

### UK deterministic

Frequent hourly runs, with examples such as:

- 12 UTC run expected around 13:45–14:05 UTC;
- 13 UTC around 14:20–14:40;
- 14 UTC around 15:20–15:40;
- continuing through the day.

### Global deterministic

Examples:

- 00 run ~04:30–04:50;
- 06 run ~10:15–10:35;
- 12 run ~16:30–16:50;
- 18 run ~22:10–22:30.

### MOGREPS-UK

Frequent ensemble updates with predictable windows.

Official schedule:
https://datahub.metoffice.gov.uk/support/model-run-availability

## Trading hypothesis

London daily-temperature books may be more sensitive to generic ECMWF/Open-Meteo than to each new UK local model cycle. If so, the high-frequency UK model provides repeated local informational shocks that can precede market repricing.

Test exact London City Airport resolver performance of UK deterministic/MOGREPS relative to ECMWF.

---

# 5. JMA MSM — frequent Tokyo/Japan mesoscale revisions

JMA MSM:

- 5 km grid;
- runs every 3 hours;
- 09 and 21 JST initializations extend to 78h;
- intermediate cycles extend to 39h.

Official:
https://www.data.jma.go.jp/developer/weatherdataguide/appendix/2-2-b.html

## Trading hypothesis

Tokyo/Japan markets can receive six-to-eight meaningful local forecast updates while a trader using only major global cycles sees fewer changes.

Measure:

`MSM revision -> resolver bucket probability -> Polymarket response`.

---

# 6. DWD ICON family — dense European update stream

DWD directly exposes open model files for ICON global, ICON-EU, ICON-D2 and ICON-D2-EPS. Directory structure shows frequent cycles, including 3-hourly ICON-D2 runs.

Official:
https://opendata.dwd.de/weather/nwp/

## Trading hypothesis

For Munich, Paris-adjacent continental regimes, Warsaw, Milan and other European cities, ICON-D2/D2-EPS may move earlier or differently than popular global forecasts.

High-value event study:

- update local high-resolution model;
- check whether ECMWF/Open-Meteo consensus has not yet changed;
- compare market reaction after later global/aggregator updates.

If DWD consistently leads the same direction, that lead is directly tradable.

---

# 7. Environment Canada HRDPS/RDPS — Toronto specialization

HRDPS provides high-resolution Canadian short-range guidance up to 48h with several cycles/day. RDPS provides broader North American coverage.

Official:
https://eccc-msc.github.io/open-data/

## Trading hypothesis

Toronto is an obvious market where a national high-resolution model and statistical post-processing may beat globally generic API outputs. Measure model run availability empirically and align each revision with the Toronto book.

---

# 8. HKO — direct observation clock can dominate forecast clock

HKO open data includes running max/min since midnight derived from 1-minute mean temperatures, updated every 10 minutes, plus current forecasts and local observation products.

Official:
https://www.hko.gov.hk/en/abouthko/opendata_intro.htm

## Trading hypothesis

For HKO-resolved contracts, every 10-minute extrema update is a potential probability shock. This can be more valuable than waiting for a global NWP cycle because it updates the actual accumulated settlement state.

For precipitation, rainfall-to-date updates similarly shift the support of the monthly total.

---

# 9. KMA — Korea direct observation/model clock

KMA API Hub provides ASOS/AWS and numerical-model services, including minute/hourly observations and KIM-related products.

Official:
https://apihub.kma.go.kr/

## Trading hypothesis

Seoul/Incheon contracts can be tested for whether direct KMA observations/local forecasts lead airport/general web products used by other traders.

---

# 10. NASA GISTEMP and ERA5T — a days-long climate information window

NASA publishes a scheduled GISTEMP calendar. For August 2026, release is scheduled for **September 10 at 11:00 AM EDT**.

ERA5T arrives roughly five days behind real time; monthly means become available around five days after month-end.

This creates an unusually long potential lead compared with daily temperature milliseconds/minutes:

`month end -> ERA5T/global proxy information -> GISTEMP scheduled release`.

## Trading hypothesis

The main edge is not reaction speed in milliseconds. It is dataset-basis calibration: how tightly can early proxy datasets predict the first NASA number?

A correct 0.03°C residual model on 0.05°C buckets can have large value for days.

---

# 11. Generic aggregator delay as a measurable competitor feature

Open-Meteo and weather websites are convenient, but they can expose model data after the direct provider and may transform/blend it.

Measure for every source/model:

`direct_provider_available_time`

versus

`aggregator_reflects_new_run_time`.

Then:

`aggregator_lead = t_aggregator - t_direct`.

If a large fraction of public bots use the aggregator, this gap is a plausible causal source of price latency.

---

# 12. Release event table to collect

For each source event store:

```text
source
model
nominal_run_time
first_file_seen
first_required_steps_complete
first_probability_update
cities_affected
max_abs_bucket_delta
book_before
book_1s
book_5s
book_30s
book_1m
book_5m
book_30m
traded_volume_after
```

Derived metrics:

- fair-value shock;
- price capture ratio;
- half-life;
- edge after taker fee at each lag;
- profitable depth;
- cross-city aggregate opportunity dollars.

---

# 13. Cross-city batching creates leverage

A major global model update is not one trade. It can change probability for dozens of simultaneous markets.

If one ECMWF cycle creates positive net EV in 8 cities, capital allocation should solve:

`max Σ_i size_i * marginal_EV_i`

subject to available bankroll/depth and correlation effects.

Rank signals by marginal dollar EV immediately after the release rather than process cities sequentially in arbitrary order.

This turns one forecast ingestion into a portfolio-scale information event.
