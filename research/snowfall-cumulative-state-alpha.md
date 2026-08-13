# Snowfall cumulative-state and publication-basis research

Snapshot: **2026-08-13**

## Research verdict

Snowfall should be promoted from a seasonal curiosity to a serious Weather family.

Two resolved January 2026 examples demonstrate meaningful capacity:

- NYC monthly snowfall ladder: about **$112k** final event volume;
- multi-city Jan 24–26 “at least 0.1 inch on any day” event: about **$59.8k** total volume.

Official Polymarket examples:

- https://polymarket.com/event/how-many-inches-of-snow-in-nyc-in-january-235
- https://polymarket.com/event/where-will-it-snow-this-weekend-january-24-26-352

The underlying structure is favorable:

- monthly snowfall is an accumulating nondecreasing sum;
- each snowstorm creates a discrete state update;
- daily NWS climate reports provide intermediate official state;
- preliminary/operational snow observations exist before finalized climate products;
- probabilistic snow-accumulation guidance is directly available from NOAA/NBM.

This makes snowfall a seasonal analogue of monthly precipitation, but with additional uncertainty from precipitation type and snow-to-liquid ratio.

---

## 1. NYC monthly resolver object

The January NYC market resolved according to total monthly snowfall at **Central Park**, using NOAA/NWS climate data and bracketed total inches.

The rules point to the finalized monthly `New Snow (IN)` quantity for the Central Park area.

The event eventually resolved to **12–14 inches** and accumulated roughly $112k in volume.

This is high enough that a purpose-built seasonal model can be economically relevant if the family recurs.

---

## 2. Monthly snowfall is a running sum

Let:

`S_t = official snowfall accumulated through time t`

and

`R_t = snowfall remaining in the month`.

Then:

`S_final = S_t + R_t`

with:

`S_final >= S_t`.

Once the running total exceeds a bracket ceiling, lower brackets become impossible.

Near month end or after a major storm, the problem becomes much simpler:

`P(S_final in bracket i | current official total, remaining storm distribution)`.

This is a direct monotone-state advantage.

---

## 3. Intermediate official climate state is available during the month

NWS New York states that Central Park's Daily Climate Report (`CLI`) is produced twice daily:

- around 4:30 PM local with preliminary data through roughly 4:00 PM;
- around 1:30 AM with the completed 24-hour daily report.

Official source:

- https://www.weather.gov/okx/centralparkhistorical

The daily climate reports contain snowfall fields when snow occurs, while monthly climate reports are produced after the month completes.

This creates a useful publication ladder:

`storm observations -> preliminary CLI -> completed daily CLI -> monthly finalized total`.

The point-in-time research should measure basis/revision behavior across these layers rather than rely only on the final monthly total.

---

## 4. Operational snowfall observations are precursors, not settlement truth

NOAA's National Gridded Snowfall Analysis gathers reports from many networks including:

- ASOS;
- COOP;
- CoCoRaHS;
- FAA;
- NWS spotters;
- other observing networks.

Official source:

- https://www.nohrsc.noaa.gov/snowfall_v2/index.html

NOHRSC notes that these products are observation-based analyses and that early products can be sparse while reports arrive.

Therefore they are useful for estimating snowfall that has physically occurred before the latest climate report, but should not be equated with Central Park's contractual monthly gauge/report without historical basis calibration.

For NYC, the key mapping is:

`P(next/final Central Park CLI snow increment | point-in-time local snow reports + radar/analysis)`.

---

## 5. Three-state decomposition

At any point during a storm/month, define:

`S_final = A_t + U_t + F_t`

where:

- `A_t` = snowfall already incorporated into trusted NWS climate reports;
- `U_t` = snowfall that has occurred but is not yet reflected in the latest climate total;
- `F_t` = future snowfall through the contract horizon.

These components have different uncertainty:

### `A_t`

Nearly deterministic state.

### `U_t`

Observation/publication basis: local reports, snow board timing, compaction, measurement/QC.

### `F_t`

Forecast uncertainty: storm track, QPF, precipitation type, snow ratio, band placement.

This decomposition is more useful than treating monthly snowfall as one undifferentiated forecast variable.

---

## 6. Snow-specific forecast uncertainty

Snow amount is roughly driven by:

`Snow = liquid_QPF × snow_to_liquid_ratio × p(snow/ptype)`

but each term is spatially and temporally uncertain.

Important variables include:

- storm track;
- mesoscale banding;
- liquid QPF;
- boundary-layer temperature;
- warm nose / sleet/freezing-rain risk;
- snow-to-liquid ratio (SLR);
- timing relative to surface temperature;
- melting/compaction and measurement period.

This makes deterministic snowfall maps particularly fragile near narrow brackets.

The correct probability object is a distribution over the **resolver location's reported accumulation**.

---

## 7. NBM already provides probabilistic snowfall products

NOAA's National Blend of Models documentation includes probabilities for specific snow-accumulation thresholds over multiple windows, including 1h, 6h, 24h, 48h and 72h, plus snow-ratio guidance.

Official source:

- https://vlab.noaa.gov/web/mdl/nbm-weather-elements-v4.1

This is a strong low-complexity baseline because it directly provides threshold probabilities rather than requiring a custom ensemble conversion from scratch.

Research should compare:

- NBM probabilistic snow accumulation;
- raw ensemble guidance;
- official NWS snowfall forecasts;
- eventual Central Park/NWS climate accumulation.

The simplest calibrated combination that best predicts the resolver should win.

---

## 8. Short-window ≥0.1 inch contracts have a simpler target

The Jan 24–26 multi-city event resolved Yes for a city if the NWS daily climate report showed at least **0.1 inch** of snowfall on any eligible day.

This is much simpler than a monthly exact-total ladder.

For each day/city define:

`p_d = P(CLI daily snowfall >= 0.1 in)`.

For a multi-day window, model the joint probability of at least one qualifying day, preserving storm dependence across days.

Useful information includes:

- precipitation-type probability;
- any measurable snow reaching the official station;
- temperature profile;
- storm track;
- ongoing observed snowfall before CLI publication.

The threshold is small enough that trace-versus-0.1-inch measurement semantics become important.

---

## 9. Cross-city storm structure

The Jan 24–26 event had many cities under one synoptic storm system.

This creates correlated outcomes:

- track shifts move snow probability across several cities together;
- warm-sector/rain-snow line shifts create opposite effects across nearby cities;
- one model revision can update many contracts simultaneously.

A shared storm latent state is cleaner than forecasting each city independently.

For a major cyclone, estimate a joint distribution over:

- storm track;
- QPF field;
- thermal profile;
- banding;
- resulting station snowfall.

Then map the same scenario ensemble into each city's resolver contract.

This also creates a natural test for cross-market propagation: one city's market can move first after the same storm-track update.

---

## 10. Point-in-time snowfall publication basis

For historical events, store:

- raw local snowfall reports first seen;
- NOHRSC analysis vintages;
- NWS preliminary CLI snowfall;
- completed daily CLI snowfall;
- monthly climate report/final monthly value;
- any corrections/revisions;
- exact Polymarket rule cutoff.

Measure:

- provisional-to-final bias;
- frequency of threshold/bracket changes due to reporting revisions;
- time lag between observed snow and climate-product publication;
- city/station differences.

This separates meteorological forecast error from resolver-publication error.

---

## 11. Historical model for monthly brackets

For a monthly ladder with current accumulated amount `A` and remaining storm scenarios `r`:

`q_i = P(A + r in bracket i)`.

Build `r` from a mixture of:

- currently forecast storms within 7–10 days;
- climatological future storm count/amount beyond the skillful deterministic horizon;
- season/date dependence.

As month end approaches, the climatological tail shrinks and explicit forecast storms dominate.

This is the same general logic as hurricane-count and monthly-precipitation contracts, but with snowfall-specific storm physics.

---

## 12. Research priority

Evidence grade:

- historical Polymarket capacity: **high for at least one NYC monthly event (~$112k)**;
- multi-city short-window capacity: **meaningful (~$59.8k)**;
- resolver source: explicit;
- cumulative-state math: exact;
- probabilistic NOAA guidance: strong;
- publication-basis edge: unmeasured.

Priority: **high seasonal research lane**.

It should rank above many exotic low-volume Weather ideas because it has already demonstrated substantial capital capacity and reuses the project's core strengths:

- exact resolver modeling;
- cumulative state;
- point-in-time publication tracking;
- probabilistic weather distributions;
- cross-city scenario consistency.

The smallest decisive historical study is the January 2026 NYC monthly ladder: reconstruct the daily accumulated snowfall distribution and market price path through each storm, then separate forecast revision, observed-but-unpublished snow, and final climate-report basis.