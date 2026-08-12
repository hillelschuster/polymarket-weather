# US T+0 feed priority — 2026-08-12

## Profitability verdict

The US observation strategy is now primarily a **data-latency competition**. Nominal METAR observation timestamps are not executable timestamps.

Live KLGA Aug 12 evidence:

- precise routine METAR observation timestamp: `16:51Z`;
- NOAA public station-file `Last-Modified`: `16:54:29Z`;
- therefore this specific simple public station-file route lagged the nominal observation time by about **3m29s**;
- the report moved KLGA from **80.96°F at 15:51Z** to **82.94°F at 16:51Z**, crossing a Polymarket bucket boundary;
- historical CLOB minute marks already moved across higher buckets around the 16:54–16:55 public-arrival window.

This means historical backtests must anchor to **source arrival time**, not METAR valid time.

## Highest-value US source hierarchy to test

### 1. Direct/continuous ASOS distribution

NWS says most ASOS stations send shortened observations every five minutes in addition to the hourly complete METAR. The shortened reports include temperature but at lower precision. NWS also states ASOS internally observes every minute and computes a rolling five-minute temperature average.

Official sources:

- https://www.weather.gov/lot/weather_observations_faq
- https://www.weather.gov/lox/asostemperature

Economically, the five-minute stream can reveal a temperature regime/bucket approach well before the next full hourly tenth-degree-C `T` group. It should be treated as an early-warning state, with explicit rounding uncertainty.

### 2. MADIS OMO / one-minute ASOS via the fastest distribution path

MADIS documents operational One Minute ASOS (OMO/HFMETAR) data and says real-time data arrive continuously/asynchronously. Its normal file processing is every five minutes, so ordinary HTTPS files are not a sub-minute edge. MADIS separately recommends **LDM** for users requiring the fastest real-time access and offers real-time LDM access by application.

Official sources:

- https://madis.ncep.noaa.gov/madis_OMO.shtml
- https://madis.ncep.noaa.gov/madis_ui.shtml
- https://madis.ncep.noaa.gov/data_application.shtml
- https://madis.ncep.noaa.gov/madis_sample_data.shtml

For US contracts with enough capacity, acquiring/testing the LDM OMO path has much higher expected value than optimizing a 2-second poller on a feed that is already minutes late.

### 3. AviationWeather.gov API/cache

AWC says it generally displays station observations within a minute or two **of receiving them**, and the public API/cache is minute-scale. This is worth measuring against NOAA station files but cannot be assumed to beat direct distribution.

Official sources:

- https://aviationweather.gov/data/api/
- https://aviationweather.gov/help/

### 4. NOAA station TXT

Useful, trivial, and reproducible, but today's KLGA measurement shows it can be several minutes behind nominal observation time. It is a baseline/verification source, not currently the preferred production trigger.

## Execution implication

If synchronized books show that Polymarket materially reprices before NOAA station TXT first-seen time, do **not** spend effort making the CLOB client faster first. The money bottleneck is upstream weather dissemination. Test five-minute ASOS and MADIS LDM/OMO.

If stale executable depth survives after the NOAA first-seen timestamp, the cheap public route itself may be sufficient and the next optimization is CLOB WebSocket + immediate IOC/marketable execution.

## Backtest correction

Every T+0 observation event should store three clocks separately:

1. `observation_valid_time` — station timestamp;
2. `source_first_seen_time` — when our chosen feed exposed it;
3. `market_reprice_time` — first material executable book reaction.

Only `(3 - 2)` is directly monetizable by that feed. `(3 - 1)` overstates alpha whenever dissemination is delayed.
