# Snowfall hypothesis finalization — point-in-time evidence

Snapshot: **2026-08-13**

## Verdict

Snowfall remains the strongest new-family research lane because the January 24–26, 2026 Central Park exact-bracket event reached about **$1.448M** in total volume, while NOAA/WPC already publishes probabilistic snowfall guidance that can be transformed into bracket probabilities.

The remaining research question is precise:

> Can point-in-time official snowfall probabilities be calibrated to the exact Central Park resolver well enough that material probability revisions precede Polymarket repricing?

The research should answer that before any larger modeling effort.

---

## 1. Contractual object

The January 24–26 NYC event resolved from the sum of NOAA/NWS Central Park `New Snow (IN)` values for January 24, 25 and 26. Exact boundary values resolve to the higher bracket.

Official Polymarket event:

- https://polymarket.com/event/how-many-inches-of-snow-in-nyc-this-weekend-jan-24-26

The final event volume was about `$1,447,818`; the winning `10–12` bracket alone had roughly `$328k` volume.

---

## 2. Historical WPC information is reconstructable

WPC maintains an archive of winter-weather probabilistic forecasts going back to March 2012:

- https://www.wpc.ncep.noaa.gov/archives/web_pages/winwx/winwx.shtml

WPC also documents date/cycle-specific historical GIS snowfall exceedance files for Days 1–3, including probability thresholds such as 4, 8 and 12 inches:

- https://www.wpc.ncep.noaa.gov/html/gis_winter_sfc.html

Current PWPF products are richer and include:

- snowfall exceedance probabilities;
- 5/10/25/50/75/90/95 percentiles;
- GRIB2 products.

Official sources:

- https://www.wpc.ncep.noaa.gov/pwpf/wwd_percentiles.php
- https://www.wpc.ncep.noaa.gov/pwpf/wwd_accum_probs.php

Do not assume every current percentile product has a complete historical machine-readable archive. For January 2026, reconstruct what is demonstrably archived; prospectively preserve the full probability distribution for future events.

---

## 3. One CDF should price the whole ladder

Let `S` be contractual Central Park snowfall over the market window.

For bracket `[L,U)`:

`q_[L,U) = P(L <= S < U)`.

With CDF `F`:

`q_[L,U) = F(U-) - F(L-)`.

The first research model should therefore be a calibrated snowfall CDF, not independent bracket classifiers.

Use the official WPC probability distribution as the baseline `F_WPC` and learn only the mapping to the Central Park contractual measurement.

For historical event `n`:

`u_n = F_WPC,n(S_resolver,n)`.

Use PIT diagnostics and the smallest calibration that improves out-of-sample probability quality. Initial regime variables should remain compact:

- forecast horizon;
- all-snow versus mixed/sleet regime;
- coastal/warm-boundary-layer regime.

---

## 4. Separate snow already official, snow already fallen, and future snow

At time `t`:

`S_final = A_t + U_t + R_t`.

Where:

- `A_t` = snowfall already incorporated into trusted Central Park/NWS climate reporting;
- `U_t` = snowfall that appears to have occurred but is not yet reflected in the latest contractual climate state;
- `R_t` = future snowfall still to occur.

This decomposition matters because the uncertainty sources are different.

`A_t` is nearly known.

`U_t` is a publication/measurement-basis problem involving local reports, measurement timing, compaction and mixed precipitation.

`R_t` is the remaining meteorological probability distribution.

Near storm end the bracket problem can become very sharp. If resolver-aligned accumulation is 11.4 inches, then approximately:

`P(10–12) = P(R_t < 0.6)`.

---

## 5. Three information-event classes

Historical analysis should keep these separate.

### Forecast revision

A new WPC/NBM/model vintage moves the snowfall CDF before or during the storm.

### Observed accumulation

Physical accumulation becomes more certain before the contractual climate product incorporates it.

### Official publication

A preliminary/final climate product adds snow to the trusted official accumulated state.

For each class record:

- source valid time;
- source first-seen time where reconstructable;
- probability vector before and after;
- Polymarket price path before and after;
- eventual resolver value.

---

## 6. Decisive January 24–26 study

At each available information vintage from market creation through storm completion, preserve:

### Weather state

- WPC issue/cycle;
- available threshold probabilities/percentiles;
- Central Park or nearest-grid distribution;
- precipitation-type regime;
- operational accumulation reports;
- preliminary/completed NWS climate snowfall;
- final resolver snowfall.

### Market state

- explicit bracket token/outcome labels;
- historical prices by bucket;
- trade timestamps/size where available;
- market creation time;
- settlement.

Historical price history can establish timing and magnitude of repricing, but it cannot recreate resting depth. Treat it as evidence for whether a prospective order-book study is justified, not as production-fidelity execution evidence.

---

## 7. Statistics that matter

For each information update calculate:

- `Delta q_i` for every bracket;
- subsequent market-price change;
- lag between source information and market response;
- forecast error before/after update;
- calibration error by bracket boundary and precipitation regime;
- fraction of total apparent opportunity attributable to the largest storm/update.

The main family question is not percent return on one bucket. It is whether the probability information repeatedly arrives before market convergence in a family with demonstrated large capacity.

---

## 8. Falsification / downgrade criteria

Downgrade the thesis if:

1. WPC-to-Central-Park residual uncertainty remains comparable to or wider than the market brackets after simple calibration;
2. the market consistently incorporates WPC revisions before the public products are available;
3. historical price moves cannot be aligned point-in-time without look-ahead;
4. observed-but-unpublished snowfall is too unreliable to improve prediction of later climate totals;
5. apparent edge is concentrated entirely in one late-stage observation after the market has already converged;
6. the January 24–26 market proves to be an exceptional capacity outlier rather than a recurring family.

---

## 9. Final research deliverable

The snowfall hypothesis is sufficiently finalized when the repository contains a strict point-in-time January 24–26 reconstruction with:

- resolver-calibrated probability vectors through time;
- exact WPC/NWS vintages used;
- market price response through the same timeline;
- quantified calibration error;
- explicit identification of forecast-revision, observed-accumulation and official-publication effects.

At that point the unresolved question is market execution rather than basic snowfall probability construction.