# GISTEMP basis alpha — reproduce the settlement input before NASA publishes it

Snapshot: **2026-08-11**

Purpose: isolate the highest-capacity weather-market edge found so far.

Polymarket's monthly global-temperature markets have historically traded **millions of dollars**, far more than a typical single airport-temperature ladder. They resolve on the **first published NASA GISTEMP v4 monthly Land-Ocean Temperature Index value**, in narrow 0.05°C brackets.

The strongest current thesis is not generic climate forecasting. It is:

> **Reproduce or tightly nowcast NASA's first-published GISTEMP number from the same upstream NOAA datasets before NASA's scheduled release, then trade only the bracket discrepancy.**

This can coexist with the high-frequency city-extrema engine. The economics are different: fewer opportunities, much larger capacity, slower information decay.

---

# 1. Contract target is exact and machine-reproducible

Current August 2026 Polymarket market:

https://polymarket.com/event/august-2026-temperature-increase-c-20260728155540489

Buckets:

- `<1.10°C`;
- `1.10–1.14°C`;
- `1.15–1.19°C`;
- `1.20–1.24°C`;
- `1.25–1.29°C`;
- `>1.29°C`.

The contract resolves from NASA's table:

`GLOBAL Land-Ocean Temperature Index in 0.01 degrees Celsius`

specifically the `2026` row and `Aug` column.

The rules explicitly state that the **first value published** is sufficient for resolution and later revisions are ignored.

NASA's 2026 release schedule states:

- July 2026 release: **2026-08-11 11:00 EDT / 15:00 UTC**;
- August 2026 release: **2026-09-10 11:00 EDT / 15:00 UTC**.

Official schedule:
https://data.giss.nasa.gov/gistemp/release_dates.html

This creates a known publication clock.

---

# 2. Historical capacity is large

Observed resolved Polymarket GISTEMP-bracket markets:

| Contract | Winning bracket | Total event volume |
|---|---|---:|
| Aug 2024 Temperature Increase | `>1.29°C` | **$1,628,206** |
| Nov 2024 Temperature Increase | `1.30–1.34°C` | **$2,554,058** |
| Feb 2025 Temperature Increase | `1.25–1.29°C` | **$3,742,945** |
| Feb 2026 Temperature Increase | `1.20–1.24°C` | **$220,989** |
| Jun 2026 Temperature Increase | `1.15–1.19°C` | **$88,622** |
| Jul 2026 Temperature Increase | unresolved/crawler pre-release snapshot | ~**$42.8K** in latest indexed snapshot |

Representative sources:

- https://polymarket.com/event/august-2024-temperature-increase-c
- https://polymarket.com/event/november-2024-temperature-increase-c
- https://polymarket.com/event/february-2025-temperature-increase-c
- https://polymarket.com/event/february-2026-temperature-increase-c

This is enough capacity that a modest, high-confidence probability edge can dominate many days of small airport trades in dollar terms.

---

# 3. NASA publishes the exact algorithm and input identity

NASA's GISTEMP v4 source page publishes the analysis source code as:

`gistemp4.0.tar.gz`

and documents that the software downloads its required input files itself.

Source:
https://data.giss.nasa.gov/gistemp/sources_v4/

NASA identifies the production inputs as:

## Land

NOAA/NCEI **GHCN-M v4 adjusted monthly mean temperature**, specifically the adjusted `qcf` product:

`ghcnm.tavg.latest.qcf.tar.gz`

## Ocean

NOAA/NCEI **ERSST v5**.

NASA's GISTEMP homepage states that its monthly update uses current GHCN v4 station data and ERSST v5 ocean data.

Sources:

https://data.giss.nasa.gov/gistemp/
https://data.giss.nasa.gov/gistemp/sources/gistemp.html

This means the settlement algorithm is not a black box.

---

# 4. ERSST-v5 is available much earlier than NASA publication

NCEI's public ERSST-v5 NetCDF directory currently shows:

`ersst.v5.202607.nc`

with modification timestamp:

**2026-08-03 10:42 UTC**.

Directory:
https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/netcdf/

July ended July 31. Thus the July 2026 ocean input was public roughly **2.4 days after month-end** and approximately **8 days before NASA's scheduled August 11 GISTEMP release**.

The directory update rewrites/refreshes the historical ERSST files as part of the monthly production, but the important point is that the new July file itself existed on August 3.

## Economic implication

By D+3, the ocean component used by NASA is essentially available.

The remaining uncertainty is dominated by:

- land station coverage/content in the current GHCN adjusted file;
- NASA's spatial processing / combination;
- late reports and quality-control differences.

---

# 5. GHCN adjusted land input can appear before the scheduled NASA release

On **2026-08-11**, NCEI's GHCN v4 directory showed:

`ghcnm.tavg.latest.qcf.tar.gz`

last modified at:

**2026-08-11 03:42 UTC**.

NASA's scheduled July GISTEMP release was:

**2026-08-11 15:00 UTC**.

That is an approximately **11h18m lead** between the latest GHCN adjusted bundle timestamp and NASA's scheduled publication.

NCEI directory:
https://www.ncei.noaa.gov/pub/data/ghcn/v4/

### What is verified

- the qcf bundle existed with that 03:42 timestamp;
- NASA documents qcf as its land-data source;
- NASA's July release was scheduled for 15:00 UTC.

### What is not yet verified

The directory timestamp alone does not prove that every July station value NASA would ultimately use was already present at 03:42.

The decisive production experiment is therefore simple:

> archive the qcf file whenever its hash/timestamp changes and run GISTEMP immediately; compare the output with NASA's eventual first publication.

No broad infrastructure is required.

---

# 6. Direct-replica strategy

The highest-confidence late-stage strategy should try to reproduce NASA itself.

For month `m`:

1. obtain the newest ERSST-v5 monthly file;
2. obtain the newest GHCN v4 adjusted qcf bundle;
3. run the published GISTEMP v4 code with those exact current inputs;
4. read the computed global LOTI anomaly for month `m`;
5. map the result into the Polymarket 0.05°C bracket;
6. compare with executable prices and depth.

Call the replica result:

`G_replica(t)`.

The forecast distribution should include only uncertainty that remains between the current input snapshot and NASA's first publication:

`G_first = G_replica(t) + ε_input_lag + ε_processing`.

If repeated historical/live dry runs show the residual is usually below 0.01–0.02°C near release, the market can become close to deterministic relative to 0.05°C bins.

---

# 7. ERA5T provides an earlier independent basis

Copernicus/ECMWF documents ERA5T as available approximately **five days behind real time**, and its monthly mean is available around **five days after month-end**.

Official sources:

https://climate.copernicus.eu/key-update-climate-dataset-brings-data-five-days-behind-real-time
https://confluence.ecmwf.int/pages/viewpage.action?pageId=388500357

Thus around D+5, several days before NASA publication, we can have a complete preliminary reanalysis of the month.

## But ERA5T is not GISTEMP

ERA5T and GISTEMP differ in:

- observing systems and assimilation;
- spatial processing;
- land/ocean representation;
- SST / surface-air treatment over ocean;
- climatology/baseline details.

Therefore ERA5T is a **basis model**, not the settlement replica.

Use it to estimate:

`G_first ≈ a_month + b_month * ERA5T_month + residual`.

A better hybrid can separate land/ocean components:

`G_first ≈ a + b_L * ERA5T_land + b_O * ERSSTv5_ocean_metric`.

Keep the regression simple unless more structure improves bracket accuracy/net PnL.

---

# 8. Information ladder by date

The climate trade naturally becomes more precise through the post-month window.

## During month

Inputs:

- partial ERA5/near-real-time temperature fields;
- observed month-to-date climate anomalies;
- seasonal/short-range forecasts for remaining days.

Output:

`P(G_first bracket | partial month)`.

Useful for early positioning only if the market is materially wrong.

## D+1 to D+3

New ERSST-v5 can arrive. July 2026 arrived D+3.

Update ocean component materially.

## D+5

ERA5T monthly field should be available around this point.

This gives a strong full-month independent global estimate.

## Release-day / late pre-release

Newest GHCN qcf bundle appears. On Aug 11 it was updated at 03:42 UTC.

Run direct GISTEMP replica.

This should become the dominant forecast if historical dry runs show reproducibility.

## 15:00 UTC scheduled publication

NASA publishes first value; Polymarket can resolve.

---

# 9. First publication is the correct historical label

A major backtest trap:

Polymarket resolves on the **first published NASA value** and ignores later revisions.

NASA explicitly states that monthly files incorporate late reports and corrections for earlier months.

NASA documented one concrete case where later South Pole reports lowered the previously reported **June 2016 anomaly by 0.05°C**.

Source:
https://data.giss.nasa.gov/gistemp/news/20161017/

A 0.05°C revision equals an entire current Polymarket bracket width.

Therefore:

> **Do not train/backtest these markets against today's revised GISTEMP table as though it were the original settlement value.**

---

# 10. Cheap first-release labels from Polymarket itself

For historical bracket classification, the resolved Polymarket market already tells us the first-release bucket.

Examples:

- Aug 2024 → `>1.29`;
- Nov 2024 → `1.30–1.34`;
- Feb 2025 → `1.25–1.29`;
- Feb 2026 → `1.20–1.24`;
- Jun 2026 → `1.15–1.19`.

This is sufficient for the first trading backtest because the strategy is also choosing among brackets.

Exact hundredth-degree first-release values are useful later for calibrating the replica residual, but they are not required to ask:

`Did our pre-release estimate choose the correct Polymarket bracket?`

---

# 11. Historical dry-run design

For every historical month with a Polymarket GISTEMP bracket market:

## Label

`winning_first_release_bucket` from resolved Polymarket outcome.

## Data snapshots

Reconstruct or archive candidate information at:

- month end;
- D+3;
- D+5;
- D+7;
- release-day latest qcf;
- 1h before NASA release where available.

## Models

1. market price alone;
2. ERA5T basis;
3. ERSST + ERA5 land hybrid;
4. direct GISTEMP replica using current upstream files;
5. replica + simple residual calibration.

## Metrics

- correct bracket frequency;
- log loss across brackets;
- distance in °C to winning bracket;
- executable fee-adjusted PnL;
- capacity at actual book depth;
- information lead before market repricing.

The direct replica is useful only if it beats the market early enough to fill meaningful size.

---

# 12. July 2026 is the ideal live forensic test

Today, **2026-08-11**, was NASA's scheduled July release date.

Known pre-publication input chronology:

- **Aug 3 10:42 UTC:** July ERSST-v5 file public;
- **Aug 11 03:42 UTC:** latest adjusted GHCN qcf bundle timestamp;
- **Aug 11 15:00 UTC:** scheduled NASA GISTEMP publication.

Indexed Polymarket snapshots before release strongly favored the **1.20–1.24°C** bracket, roughly around the high-70s/low-80s probability range in late-July/early-August crawls.

The exact NASA July first-release result had not yet propagated into the search index during this research pass, so **do not assert the July winner from stale search results**.

Once the official result is retrievable, July should become the first full dry-run target:

- run/estimate from Aug 3 information;
- from Aug 6 ERA5T;
- from Aug 11 03:42 qcf;
- compare with first NASA value and market prices.

---

# 13. Market may already be informed — that is measurable, not a reason to dismiss the strategy

The July 2026 market had already concentrated roughly ~80% probability on one 0.05°C bracket before release in indexed snapshots.

That implies specialist climate information is already present.

The economic question is not whether the market is naive. It is:

> **Does the direct-replica / input-latency process move uncertainty from, say, 80% to 98–100% before the market does, and is enough depth still available?**

On a million-dollar historical market, even late-stage movement from 80¢ to true 99¢ can support meaningful dollar PnL.

---

# 14. Minimal live data required

A climate replica needs only a handful of files/state variables:

`month`
`ersst_file_hash`
`ersst_available_time`
`ghcn_qcf_hash`
`ghcn_qcf_available_time`
`gistemp_replica_value`
`replica_bracket`
`era5t_estimate`
`market_bid_ask_by_bracket`
`NASA_release_time`.

No broader climate platform is necessary.

---

# 15. Extension to monthly rank and annual rank

Once a monthly GISTEMP distribution exists, related Polymarket markets are nearly free extensions.

## Hottest-month rank

Compare predicted current-month GISTEMP first value with historical same-calendar-month values, using the vintage semantics specified by the contract.

Polymarket has traded markets such as first/second/third hottest month with six-figure volume.

## Annual rank

For year `Y`:

`annual_Y = (Σ known_months + Σ future_month_distributions) / 12`.

As the year progresses, remaining variance falls.

This is directly relevant to large specialist positions such as `gopfan2`'s visible 2026 annual-rank exposure.

The same monthly model can therefore support several high-capacity contracts without a separate forecasting engine.

---

# Bottom line

The strongest high-capacity weather thesis is now concrete:

> **NASA publishes its algorithm and exact NOAA inputs. ERSST-v5 can arrive days before GISTEMP, ERA5T supplies a full-month independent basis around D+5, and the adjusted GHCN land bundle can update hours before NASA's scheduled release. A small direct-replica process can potentially know the 0.05°C settlement bracket before Polymarket fully converges.**

The next research priority is historical first-release reconstruction, beginning with the exact months for which Polymarket provides resolved brackets and multi-million-dollar capacity evidence.