# Alpha integrity — preserving real forecasting edge in data

Snapshot: **2026-08-11**

A forecasting edge only becomes money if the research dataset represents the same information, resolver and executable market state that existed at trade time. Data fidelity is therefore part of alpha generation: it prevents false signals from displacing genuine ones and reveals source-specific edges other traders may miss.

The design principle is simple:

> Every row should answer: **what could we have known, when could we have known it, what exactly would the contract have paid, and what price could we actually have traded?**

---

# 1. Four clocks per weather datum

For each forecast/observation store separate times:

1. **reference time** — model initialization or observation time;
2. **source publication/availability time** — when provider made it accessible;
3. **our receipt time** — when collector obtained it;
4. **decision time** — when a fair-value calculation/trade could use it.

These timestamps allow direct measurement of information lead and system latency.

Example:

- ECMWF cycle nominal 12:00 UTC;
- file/member becomes available later;
- collector receives at 19:06:14;
- probability calculation completes 19:06:16;
- order reaches CLOB 19:06:17.

The economic latency is from **source availability to executable order**, not from nominal model initialization.

---

# 2. Forecast vintage is a first-class key

Never collapse a target date to one “forecast.” Store every vintage.

Primary key concept:

`(source, model, run_time, valid_time, station/location, variable, member)`.

For derived daily extrema:

`(source, model, run_time, resolver_event, member) -> member_daily_max/min`.

This enables:

- run-to-run forecast shock studies;
- point-in-time backtests;
- lead-time calibration;
- detection of stale data;
- market response alignment.

---

# 3. Resolver truth has versions

For each contract store three separate objects where available:

### Physical/source observation

The raw authoritative or upstream measurement stream.

### First resolver-published value

The value that current Polymarket rules may specify as decisive, especially when later revisions are explicitly ignored.

### Final/revised climatological value

Useful for meteorological analysis but potentially different from the contractual settlement value.

This distinction matters in markets whose rules say the first published value after a specified date/time controls resolution.

---

# 4. Resolver registry versioning

Key each rule set by event, not city alone.

Store:

- event ID/slug;
- city/market family;
- target date/period;
- station/source name;
- station identifier;
- resolver URL;
- source family;
- local timezone/civil day;
- native unit;
- source precision;
- bucket boundaries;
- rounding rule;
- revision window;
- rule text hash / captured text.

This turns source changes into measurable regimes instead of hidden errors.

Potential alpha: if a resolver switches source family and the market still prices using old participant habits, early correct mapping can be directly profitable.

---

# 5. Native-unit probability calculation

Calculate settlement in the contract's native resolver unit before bucketization.

For US Fahrenheit markets, preserve Fahrenheit semantics through:

- raw station/source reconstruction;
- maximum/minimum calculation;
- official precision/rounding;
- 2°F bucket mapping.

Repeated °C↔°F conversions around integer boundaries can move probability mass into the wrong contract.

For international whole-°C markets, apply the source's actual display precision and rounding behavior.

---

# 6. Exact station versus grid proxy

Store both:

- resolver station observation;
- model/gridpoint value.

The difference is not noise to discard; it is a feature:

`station_basis = resolver_station - model_gridpoint`.

Learn station basis by:

- model;
- cycle;
- season;
- wind regime;
- cloud regime;
- time of day.

Airports near coasts, urban heat islands, elevation differences and local terrain can create persistent forecast basis that a generic city-coordinate model misses.

---

# 7. Observation completeness for daily extrema

A daily maximum/minimum reconstructed from routine hourly reports can miss brief extrema.

Preserve where available:

- routine METAR;
- SPECI;
- T-group precision;
- 6-hour max/min groups;
- daily summary/DSM/CLI products;
- national-agency extrema feeds.

For each reconstructed daily high/low attach a provenance/coverage flag rather than silently substituting a gridded reanalysis value.

The flag can be used as a feature in resolver-discrepancy probability.

---

# 8. Market price provenance

For every model decision store:

- best bid;
- best ask;
- depth levels;
- last trade;
- midpoint;
- fee rate;
- book timestamp;
- collection timestamp.

Also store the precise hypothetical/actual order expression:

- side;
- limit price;
- size;
- maker/taker intention;
- effective fill price;
- filled size;
- fee/rebate.

This prevents later analysis from turning a midpoint signal into fictional executable PnL.

---

# 9. Full event snapshot

For temperature ladders, save all outcomes together under one event timestamp.

Required fields:

- outcome/bucket definition;
- YES token ID;
- NO token ID if applicable;
- bid/ask/depth;
- weather probability;
- coherent market probability;
- negative-risk group/metadata.

This allows reconstruction of:

- probability sum;
- basket opportunities;
- neighboring-bucket relative value;
- full-ladder shifts after forecasts.

Independent outcome snapshots collected at widely different times can create fake arbitrage, so event-level synchronization has direct economic value.

---

# 10. Wallet data normalization

For each fill record:

- wallet;
- timestamp;
- side;
- outcome/token;
- price;
- shares/notional;
- taker/maker inclusion mode/source;
- event family;
- resolver date;
- horizon at trade time;
- market state at nearest timestamp.

Normalize size by wallet's own historical distribution:

`size_z = notional / median_or_scale(wallet recent notionals)`.

A $500 trade means something different for a $50 typical wallet versus a $50k typical wallet.

---

# 11. Historical forecast source quality

Historical weather products can represent different things:

- archived operational forecast exactly as available then;
- hindcast/reforecast produced later with a current model;
- reanalysis assimilating future observations;
- historical API that reconstructs weather rather than stores old forecasts.

Label these explicitly.

For trading research, archived operational forecasts have the strongest causal relevance. Reforecasts are valuable for model-error estimation but should be marked as such.

---

# 12. Source outages and fallback as regimes

If the primary source is absent and the system uses a fallback, store:

- primary source status;
- fallback source;
- age of fallback;
- expected resolver-basis error.

Then measure PnL separately.

A fallback may remain profitable with a larger required edge, while a pristine direct source can justify more aggressive pricing. The data should let the model learn the difference.

---

# 13. Weather-rule parser validation as economic measurement

For each discovered market, automatically derive a normalized resolver specification and compare it with known city/source mappings.

When the parser sees a new station/source/rule regime, capture it as a new feature/regime immediately.

This is not process ceremony; source novelty can itself create the largest edge because other automated systems may continue targeting stale assumptions.

---

# 14. Calibration dataset design

One row per forecast decision point should include:

### Identity

- event/outcome;
- station;
- target period;
- bucket.

### Weather state

- forecast vintage(s);
- member extrema distribution;
- observations to date;
- current max/min/accumulation;
- forecast revision;
- local meteorological features.

### Market state

- bid/ask/depth;
- coherent ladder probabilities;
- recent flow;
- specialist-wallet factors.

### Outcome

- first resolver value;
- winning bucket;
- settlement timestamp.

### Execution outcome

- simulated/actual fill at observed book;
- fee/rebate;
- markouts;
- final PnL.

This one table can support probability calibration, market-residual models, wallet studies and execution analysis without a large framework.

---

# 15. Alpha-integrity checks that directly protect PnL

High-value checks include:

- all bucket probabilities sum to ~1;
- bucket parser reproduces known resolved events;
- station/date timezone maps to the correct local day;
- source availability timestamp precedes every decision using it;
- market ask/bid comes from the same or earlier timestamp than decision;
- fee formula matches current market metadata;
- realized settlement matches captured contract rule;
- fallback-source trades are identifiable;
- duplicate fills/positions are not counted twice;
- maker fills are not misclassified as taker price observations.

Each catches a defect that can materially alter measured or realized money.
