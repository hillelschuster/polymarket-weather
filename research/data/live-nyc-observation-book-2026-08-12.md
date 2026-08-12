# Live NYC observation-to-book capture — 2026-08-12

Capture: `2026-08-12T16:51:07.123905+00:00` → `2026-08-12T17:11:07.718172+00:00`; polling **2.0s**.

Event: **Highest temperature in NYC on August 12?** (`highest-temperature-in-nyc-on-august-12-2026`).

Resolver/source metadata: `https://www.wunderground.com/history/daily/us/ny/new-york-city/KLGA`. Direct station feed measured: **KLGA** official NOAA station TXT.

AWC 12h seed running maximum: **81.0°F**.

Captured **461** batched book snapshots, **2** distinct station-file states, **56** event trade prints.

## Station file changes

| First seen UTC | NOAA Last-Modified | Temp F | Raw |
|---|---|---:|---|
| 2026-08-12T16:51:07.123917+00:00 | Wed, 12 Aug 2026 15:54:07 GMT | 81.0 | `KLGA 121551Z 01008KT 10SM FEW250 27/14 A2986 RMK AO2 SLP110 T02720139 $` |
| 2026-08-12T16:54:31.136858+00:00 | Wed, 12 Aug 2026 16:54:29 GMT | 82.9 | `KLGA 121651Z 36010G14KT 10SM FEW050 BKN300 28/14 A2984 RMK AO2 SLP106 FU BKN300 T02830144 $` |

## Observation changes captured

### First seen 2026-08-12T16:54:31.136858+00:00 — 82.94°F

| Bucket | Bid before | Ask before | Bid +10s | Ask +10s | Bid +60s | Ask +60s |
|---|---:|---:|---:|---:|---:|---:|
| 79°F or below | NA | 0.0010 | NA | 0.0010 | NA | 0.0010 |
| 94-95°F | NA | 0.0010 | NA | 0.0010 | NA | 0.0010 |
| 80-81°F | NA | 0.0010 | NA | 0.0010 | NA | 0.0010 |
| 84-85°F | 0.0600 | 0.1200 | 0.0700 | 0.1200 | 0.0800 | 0.1300 |
| 86-87°F | 0.4700 | 0.5300 | 0.4700 | 0.5300 | 0.4100 | 0.5000 |
| 88-89°F | 0.3600 | 0.4300 | 0.3600 | 0.4300 | 0.3900 | 0.4400 |
| 92-93°F | 0.0040 | 0.0050 | 0.0040 | 0.0050 | 0.0040 | 0.0050 |
| 96-97°F | NA | 0.0010 | NA | 0.0010 | NA | 0.0010 |
| 98°F or higher | NA | 0.0010 | NA | 0.0010 | NA | 0.0010 |
| 90-91°F | 0.0410 | 0.0520 | 0.0410 | 0.0520 | 0.0410 | 0.0520 |
| 82-83°F | 0.0010 | 0.0040 | 0.0010 | 0.0040 | 0.0010 | 0.0040 |

## Interpretation

This is a live synchronized measurement. `first_seen_utc` is when this GitHub runner first observed a changed official NOAA station file, not the station observation timestamp. CLOB rows are real public resting books sampled around that same wall clock. This directly measures an implementable public-feed latency path, with ±2s polling uncertainty plus network latency.

The AWC seed call is only for pre-run running-max context; it was not polled faster than the documented API rate guidance.
