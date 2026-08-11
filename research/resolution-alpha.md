# Resolver alpha — trade the contract's thermometer, not generic weather

Snapshot: **2026-08-11**

The resolver is part of the forecasting problem. A Polymarket temperature contract does not pay on an abstract city temperature; it pays on a specific published number produced by a specific station/source under a specific civil-day, precision and revision convention.

For narrow weather buckets, predicting the physical atmosphere well while predicting the wrong resolver can lose money. Conversely, understanding the resolver better than the market can create a direct edge even when everyone has the same weather forecast.

Core decomposition:

`contract outcome = g(source measurement process, local-day window, publication precision, rounding, revision rule)`.

The profitable target is the distribution of this output `g`, not raw 2m temperature.

---

# 1. Why resolver basis is economically large

International daily-high markets often use 1°C buckets. US contracts often use narrow Fahrenheit ranges.

A persistent station/source basis of only 0.5–1.0°C can:

- move the modal outcome by one bucket;
- invert YES/NO expected value;
- turn a seemingly 70% bucket into a 20% bucket;
- create late-day certainty for one source while generic apps still show another number.

Public weather projects have already reported exactly this failure mode. `jattree/weather-edge` later documented wrong-station and wrong-source issues large enough to dominate its reported PnL. `BallesJr/polymarket-weather-edge` reports much higher agreement when resolving against exact-station IEM data than ERA5 grid data.

The tradeable lesson is positive: **resolver mapping is a specialization moat.**

---

# 2. Resolver specification schema

Normalize every market into:

```text
resolver_spec = {
  market_family,
  location_label,
  station_or_index,
  source_family,
  source_url,
  local_timezone,
  measurement_window,
  variable,
  native_unit,
  source_precision,
  bucket_boundaries,
  boundary_tie_rule,
  publication_gate,
  revision_cutoff,
  fallback_rule
}
```

This object feeds the probability model directly.

Examples of economically distinct rules:

- whole-°C daily maximum from a Wunderground airport page;
- 2°F bracket from a US airport source;
- HKO daily minimum at 0.1°C source precision;
- monthly precipitation finalized to 0.01 inches;
- first-published GISTEMP monthly anomaly where later revisions do not count.

---

# 3. Source families observed in current weather markets

## Wunderground airport daily observations

Common in global daily temperature markets.

Current examples inspected in 2026 include:

- Paris → Paris-Le Bourget `LFPB`;
- Wuhan → Wuhan Tianhe `ZHHH`;
- Shanghai → Shanghai Pudong `ZSPD`;
- Ankara → Ankara Esenboğa `LTAC`.

The likely upstream physical observations are METAR/SPECI or national aviation/weather networks, but the contract's exact rule text controls which display/publication is decisive.

### Alpha path

1. fetch upstream station observation earlier than the daily Wunderground summary;
2. reconstruct the eventual displayed maximum/minimum;
3. estimate probability the later resolver page differs because of precision, delayed report or special observation;
4. trade when market still prices generic forecast uncertainty rather than near-fixed resolver state.

---

## NOAA WRH / US official climate pages

Some current contracts point directly to NOAA WRH station/climate data rather than Wunderground.

Example observed: Tel Aviv current high-temperature rules reference NOAA WRH data for Ben Gurion `LLBG`.

Monthly NYC precipitation resolves against NOAA's finalized monthly summarized Central Park precipitation.

### Alpha path

Parse the precise station/page and learn the publication timing. If the upstream daily/monthly data can be reconstructed before the finalized page updates, the difference is an information lead.

---

## Hong Kong Observatory

Hong Kong contracts can resolve directly from HKO Daily Extract fields rather than airport METAR.

Current low-temperature rules use HKO's `Absolute Daily Min`; current August precipitation uses HKO Daily Extract total rainfall.

HKO also publishes direct open data including:

- latest 1-minute mean temperature;
- running max/min since midnight from 1-minute means, updated every 10 minutes;
- rainfall;
- local forecasts.

### Alpha path

For HKO-resolved markets, this is almost ideal: the agency exposes the **same style of running statistic** needed by the settlement variable. A generic airport feed can be inferior even if it is meteorologically nearby.

Official open-data index:
https://www.hko.gov.hk/en/abouthko/opendata_intro.htm

---

## NASA GISTEMP

Global monthly temperature anomaly contracts resolve on NASA's specific index, not a generic global temperature average.

The first released GISTEMP value matters under current contract wording; later revisions can be irrelevant.

### Alpha path

Predict the *first-published NASA value* from earlier global datasets and the known GISTEMP methodology/basis. This is a resolver-basis trade, not simply a climate forecast.

---

## Mount Washington Observatory F6

Monthly maximum wind markets resolve from the Observatory's daily F6 records.

### Alpha path

Track official maximum wind to date plus upstream/live station observations. Once an observed threshold is represented in the eventual F6 record with high confidence, lower nested thresholds become certain and only higher exceedance probabilities remain.

---

# 4. US ASOS Fahrenheit microstructure

US temperature resolution is unusually subtle because measurement, transmission and display precision can differ.

Iowa Environmental Mesonet documents several important properties of US ASOS temperature data:

- official ASOS temperature measurement is derived from short high-frequency samples and averaged;
- routine METAR often transmits temperature in whole °C;
- higher-precision T-groups can be present;
- six-hour max/min groups and daily summary products can preserve extrema that routine observation snapshots miss;
- reconstructing an official whole-Fahrenheit daily extreme from only routine whole-°C METAR can produce a different result.

This is exactly the scale that can shift a Polymarket Fahrenheit bucket.

## Modeling approach

Maintain several candidate state estimates:

`M_routine` = running max from routine reported temp

`M_tgroup` = running max using high-precision T-group when available

`M_maxgroup` = running max including 6h max reports

`M_official_proxy` = best reconstruction of eventual official daily high

Then estimate:

`P(resolver bucket = i | all raw report groups and historical discrepancy patterns)`.

A late-day trade can be driven as much by **measurement-process probability** as remaining atmospheric uncertainty.

---

# 5. Civil-day/timezone edge

The daily maximum is typically over the resolver station's local civil day, not UTC.

This matters especially for:

- US markets observed after 00:00 UTC while the local date is still previous day;
- East Asia where the local day can end many hours before UTC date change;
- daylight-saving transitions;
- markets whose publication page uses a defined local climate day rather than strict midnight-to-midnight.

The model should maintain:

`resolver_local_time(t)`

and determine exactly which observations belong to the target settlement day.

Potential alpha arises when generic data pipelines bucket observations by UTC date or browser-local date.

---

# 6. Rounding and bucket boundary edge

Suppose the displayed source ultimately rounds to integer °C.

If underlying best estimate is 31.48°C versus 31.52°C, the modal resolver outcome can change abruptly even though atmospheric difference is tiny.

The correct model integrates over the underlying measurement distribution around exact rounding boundaries.

For half-up whole-degree rounding:

`P(display = k) = P(k-0.5 <= X < k+0.5)`

with precise tie behavior based on the source.

For a 2°F bracket `[92,93]`, derive bounds in **native Fahrenheit resolver space** rather than convert rounded Celsius values afterward.

### Measurement uncertainty

Let physical station maximum be `H` and publication/measurement residual `η`:

`X_resolver = H + η`.

Then:

`q_k = P(g(X_resolver)=k)`.

Historical source-to-source discrepancies estimate `η`.

---

# 7. Publication timing as a trading event

Many contract rules specify a gate such as:

- first datapoint from the next calendar day appears;
- monthly summary becomes finalized;
- NASA scheduled release time;
- later revisions ignored.

These gates create explicit event times.

For each resolver source learn:

- typical first publication latency;
- timestamp distribution;
- whether data appears incrementally or all at once;
- frequency and direction of revisions;
- market repricing around publication.

Potential trade modes:

### Pre-publication resolver reconstruction

Physical outcome already inferable; official page has not updated yet.

### Publication race

Official decisive value appears and book still contains stale orders.

### Revision-basis trade

Market participants incorrectly expect later revisions to affect a contract whose rule freezes first publication.

---

# 8. Resolver discrepancy probability

Even with excellent reconstruction, upstream and decisive display can differ.

Model:

`P(D = resolver_value - reconstructed_value | station, source, report coverage, date, weather state)`.

Useful features:

- missing SPECI/T-groups;
- peak between routine reports;
- source quality-control flags;
- unusual report cadence;
- station maintenance/outage;
- source revision history.

Then convolve physical-forecast probability with resolver discrepancy probability.

This converts “source uncertainty” into tradable quantitative uncertainty rather than a blanket haircut.

---

# 9. City/source specialization ranking

For each city compute:

`ResolverAlphaScore = basis_magnitude × predictability × source_lead × spread × market_volume`.

Candidate attributes:

- Wunderground vs direct national source lag;
- station/grid basis;
- bucket width;
- observation frequency;
- source precision;
- historical discrepancy rate;
- current market volume/depth;
- number of obvious public bots targeting it.

This can identify cities where meteorology is easy but resolver plumbing is difficult—the ideal specialization zone.

---

# 10. Resolver-aware same-day probability

The ultimate T+0 calculation is:

`P(outcome_i | physical state, remaining forecast, measurement process, publication process)`.

Decompose:

1. physical final high/min/accumulation distribution;
2. measurement/source transformation;
3. publication/rounding transformation;
4. contract bucket function.

For daily high:

`H_phys = max(M_obs, R_future)`

`H_source = H_phys + η_source`

`Y = bucket(round_rule(H_source))`.

Monte Carlo implementation is straightforward:

- sample/calibrate remaining ensemble paths;
- sample source residual;
- apply native-unit resolver transform;
- count outcome frequencies.

This is “smart math” with a direct economic purpose: put probability mass on the contract that will actually pay.

---

# 11. Resolver-alpha research outputs

The useful deliverables are compact tables:

### Resolver registry

`event -> exact settlement specification`

### Source-basis matrix

`station × source_pair × season -> bias / MAE / bucket disagreement`

### Publication-lag matrix

`resolver source -> availability distribution`

### Late-day certainty table

`city × local hour × observed bucket × remaining-boundary distance -> outcome calibration and market edge`

### Source novelty monitor

Identify new/changed resolver rules on market creation and immediately compare them with existing automated assumptions.

These tables directly feed pricing and city selection.
