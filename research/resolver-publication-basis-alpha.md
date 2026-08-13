# Resolver-publication basis alpha

Snapshot: **2026-08-13**

## Research verdict

Several Weather markets resolve from a **later official publication**, even though much of the underlying physical information exists earlier in other official/preliminary datasets.

This creates a distinct alpha family:

> estimate the value the resolver is likely to publish before that exact final/resolution page is updated.

This is different from generic weather forecasting. The core problem is reconstructing a publication pipeline and its basis/revision behavior.

The strongest current examples are:

1. monthly precipitation totals;
2. monthly/annual tornado counts;
3. GISTEMP, which is already developed separately in this repository.

The publication-basis idea generalizes whenever Polymarket names a delayed summary/index as the settlement source.

---

# Part I — monthly precipitation

## 1. NYC August contract semantics

The current NYC August 2026 precipitation market resolves from the finalized NOAA monthly summarized precipitation figure for **Central Park NY**, measured to two decimal places.

Official Polymarket event:

- https://polymarket.com/event/precipitation-in-nyc-in-august-20260728160805646

The rule is therefore not “how much radar-estimated rain falls over New York City.” It is the final Central Park station monthly total represented in the named NOAA climate product.

This precision matters because bracket boundaries can be crossed by hundredths of an inch.

---

## 2. The official total accumulates before the final monthly page exists

NWS New York documents that Central Park's Daily Climate Report (`CLI`) is produced twice daily:

- around **4:30 PM**, with preliminary data through roughly 4:00 PM local;
- around **1:30 AM**, with the completed 24-hour daily data.

Source:

- https://www.weather.gov/okx/centralparkhistorical

The NWS `CF6` preliminary local climatological product also contains daily precipitation (`WTR`) and a running monthly total.

Example/current product access:

- https://forecast.weather.gov/product.php?issuedby=NYC&product=CF6

Thus much of the eventual monthly resolver value can be reconstructed incrementally before the final monthly summary becomes available.

---

## 3. Three-state precipitation decomposition

At time `t`, define:

`P_final = A_t + U_t + R_t`

where:

- `A_t` = precipitation already incorporated into trusted official climate accumulation;
- `U_t` = precipitation that has physically occurred but has not yet entered the latest official climate summary;
- `R_t` = future precipitation remaining in the month.

This decomposition is useful because the uncertainty classes are different.

### `A_t`: almost deterministic

Use the latest official CLI/CF6/month-to-date total.

### `U_t`: current-event gauge/basis uncertainty

Estimate from station observations, gauge products and radar/multi-sensor QPE. This is often much narrower than a future forecast but must be calibrated to the Central Park gauge/climate product.

### `R_t`: meteorological forecast uncertainty

Use ensemble remaining-month precipitation with explicit heavy-rain/tropical-event scenarios.

The resulting bracket probabilities are:

`q_i = P(A_t + U_t + R_t falls in bracket i)`.

---

## 4. Why current-event precipitation can create information timing

During a heavy-rain event, the market may still be anchored to the last published official monthly total even though a substantial additional amount has already fallen.

Radar/multi-sensor precipitation products can reveal the event before the next climate report, but they are not settlement truth.

The research target is the conditional basis:

`P(next official increment | radar/QPE, station observations, event type)`

not a direct substitution of radar total for Central Park gauge precipitation.

Useful event classes:

- stratiform rain;
- convective storms;
- tropical remnants;
- snow/mixed precipitation seasonally;
- trace/small events near reporting precision.

Convective events can have especially large spatial gauge-vs-radar error, so a citywide QPE should never be treated as exact Central Park rainfall.

---

## 5. Monthly rain has monotone state geometry

Accumulated precipitation cannot decline.

Once official accumulation exceeds a bracket ceiling, that lower bracket is impossible.

Near month end, remaining uncertainty can become sharply constrained:

`required_remaining_rain(K) = K - (A_t + U_t)`

This turns the forecast problem into threshold exceedance of remaining rainfall rather than forecasting the whole monthly total from scratch.

The most informative states are likely:

- immediately after a large storm;
- when accumulated total approaches a bracket boundary;
- final week of the month;
- final 24–48 hours when most future uncertainty disappears.

---

## 6. Capacity evidence

Polymarket's precipitation category has already shown material prior-month volume. Current indexed category pages showed roughly:

- NYC July: **$41k**;
- Hong Kong July: **$51k**;
- London July: **$12k**;
- Seoul July: **$13k**.

Official category page:

- https://polymarket.com/weather/precipitation

This is below the largest daily-temperature events but large enough to justify a compact publication-pipeline model, especially because monthly contracts lock capital longer and may attract fewer specialized participants.

---

# Part II — tornado publication basis

## 7. Polymarket resolves a specific NCEI publication state

The current August 2026 tornado-count market resolves according to the first relevant NCEI U.S. Tornadoes time-series count published after the scheduled September 9, 2026 release time.

The rules explicitly state that if this first post-scheduled value is labelled **preliminary**, it still determines settlement; later revisions do not change the market outcome.

Official Polymarket event:

- https://polymarket.com/event/how-many-tornadoes-in-the-us-in-august-2026-20260727150226367

NCEI publishes explicit U.S. Tornadoes release times, commonly at **11:00 AM ET** for the monthly release in examples inspected.

Official NCEI source:

- https://www.ncei.noaa.gov/access/monitoring/tornadoes/climatology

This rule creates a very specific target:

> predict the first scheduled NCEI count that Polymarket will use, not an eventual revised historical tornado count.

---

## 8. Preliminary reports are not equal to published tornado count

Operational severe-weather reporting contains duplicates, uncertain event types and later survey/verification changes.

The research model therefore needs a historical mapping such as:

`N_NCEI_first_release = f(preliminary_reports, surveyed_events, outbreak_structure, reporting_lag, month/region)`

Candidate features:

- preliminary tornado report count;
- unique spatial/temporal clusters;
- duplicate-report rate;
- confirmed/surveyed count available point-in-time;
- outbreak versus isolated-event mix;
- late-month events with limited survey time before publication;
- regional composition;
- historical preliminary-to-first-NCEI conversion ratio.

The target label must be the first publication that matches Polymarket's rule, not a later revised NCEI value.

---

## 9. Scheduled-release timing is valuable

Unlike continuous forecast markets, the NCEI count has a known publication catalyst.

The information sequence is:

`storms occur -> preliminary reports -> surveys/verification -> month ends -> publication pipeline -> scheduled NCEI release`

If the publication count can be estimated tightly before the scheduled page update, the probability distribution may collapse before the market formally has settlement-source certainty.

This resembles the GISTEMP thesis but has a different data-generation process and potentially fewer inputs.

---

## 10. Annual tornado market creates a second capacity layer

Polymarket also has a 2026 annual tornado-count ladder with observed volume in the tens of thousands of dollars.

Example event:

- https://polymarket.com/event/how-many-tornadoes-in-the-us-in-2026

The annual variable decomposes naturally as:

`N_annual = sum(published_months) + current_month_distribution + future_month_distribution`

Each monthly NCEI release reduces annual uncertainty and should map mechanically into the annual probability surface.

This creates a research opportunity to reuse one monthly publication model across:

- monthly count market;
- annual count market;
- potentially related severe-weather markets.

Cross-market consistency should be derived from the same count distribution, not estimated independently.

---

# Part III — general publication-basis framework

## 11. Four clocks

For delayed resolver publications, store:

1. **physical event time** — when rain/tornado/weather occurred;
2. **preliminary data first-seen time**;
3. **official intermediate/QC state first-seen time**;
4. **contractual resolver publication time**.

The research edge is often in the interval between 2/3 and 4.

---

## 12. Revision-basis calibration

For each source pipeline, estimate:

`resolver_value = preliminary_estimate + basis_error`

with basis error conditioned on event type and information date.

The key statistic is not just mean bias. It is the full residual distribution near Polymarket bracket boundaries.

For a narrow bracket market, reducing basis residual SD can be more economically important than improving the raw meteorological forecast.

---

## 13. Evidence plan

### Precipitation

For historical months:

- reconstruct daily official accumulation vintages;
- reconstruct point-in-time storm/radar/gauge information;
- label finalized monthly value;
- calculate bracket probabilities at each information date;
- join to Polymarket price history where available.

### Tornadoes

For historical months:

- freeze preliminary reports at multiple dates;
- reconstruct point-in-time verification information;
- record first scheduled NCEI release count;
- fit a simple preliminary-to-publication distribution;
- compare with Polymarket monthly/annual prices.

---

## 14. Economic priority

### Monthly precipitation

Priority: **medium-high**.

Advantages:

- monotone accumulated state;
- recurring monthly markets;
- observable intermediate official data;
- discrete large storm updates;
- demonstrated five-figure capacity in several prior markets.

Main challenge: point-gauge basis and longer capital lock.

### Tornado publication basis

Priority: **medium, potentially high-capacity adjunct**.

Advantages:

- explicit scheduled release;
- unusual resolver rule based on first publication;
- reusable monthly-to-annual distribution;
- less overlap with conventional weather-betting automation.

Main challenge: building a trustworthy point-in-time preliminary/verification archive and historically matching the exact first NCEI publication.

The broader conclusion is important:

> Some Weather alpha is not forecasting atmosphere better. It is understanding the transformation from already-observed raw facts into the later official number that Polymarket settles against.