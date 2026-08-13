# Resolver local-day boundary research

Snapshot: **2026-08-13**

## Purpose

Daily-high and daily-low markets depend on observations assigned to a specific local calendar date. This note defines the data-quality and point-in-time research needed around the start of that resolver day.

The topic matters because many recurring Weather markets are already open before their target local date begins, yet research pipelines can accidentally group observations by UTC date or by the wrong source timezone.

---

## 1. Daily extrema become constrained from the first target-date observation

For a daily maximum `H` and first target-date temperature `T0`:

`H >= T0`

For a daily minimum `L`:

`L <= T0`

These are mathematical properties of extrema, independent of any forecast model.

The practical question is how the contractual source assigns observations to the target date and at what precision.

---

## 2. Timezone fields required per resolver

Each city/source record should preserve:

- IANA timezone;
- UTC offset on the event date;
- daylight-saving state;
- contractual source date convention;
- first source observation assigned to the target date;
- observation cadence around midnight;
- source precision/rounding.

Do not infer target-day membership from the UTC date alone.

---

## 3. Common boundary errors

Potential research/data failures include:

1. grouping by UTC instead of station-local date;
2. using a fixed timezone offset across daylight-saving changes;
3. assuming the first observation after `00:00` is exactly at midnight;
4. mixing precursor-feed timestamps with resolver-page date assignment;
5. converting units/rounding before determining the extrema;
6. treating source corrections after the contract cutoff as valid historical information.

Any one of these can change the reconstructed running maximum/minimum and therefore the inferred probability surface.

---

## 4. Precursor versus contractual source

For cities with a faster direct airport/national feed, store separately:

- `precursor_first_target_day_obs`;
- `resolver_first_target_day_obs`;
- their first-seen timestamps;
- their values before/after unit conversion;
- eventual final resolver extrema.

This allows measurement of whether the faster source reliably predicts the contractual source at the day boundary.

Do not equate them until the historical basis is quantified.

---

## 5. Candidate regimes for study

The first observation may be especially informative in climates with small diurnal range or unusually warm/cold nights.

Examples worth stratifying include:

- tropical/humid airports;
- summer heatwave nights in Mediterranean/European cities;
- post-frontal cold nights;
- daily-low contracts where the minimum occurs near midnight rather than sunrise.

The objective is not to assume these are inefficient markets, but to measure whether the first-day state changes the market probability surface more than currently represented in historical research.

---

## 6. Event-study fields

For each daily event:

- event/city/date;
- resolver/source;
- exact local-day start in UTC;
- first precursor observation after local-day start;
- first contractual-source observation after local-day start;
- running max/min implied by those values;
- Polymarket price marks around the boundary;
- final resolver result.

Suggested descriptive windows:

- 30 minutes before;
- 10 minutes before;
- nearest mark at/after the first observation;
- +5m;
- +15m;
- +30m.

Forward L2 collection can later add executable book information without changing the historical data definition.

---

## 7. Mechanical and probabilistic effects should be separate

### Mechanical state constraint

The first observation constrains which extrema remain possible under the contract's precision semantics.

### Forecast update

The observed starting temperature can also contain information about the later daily extreme beyond the mechanical bound.

These should be evaluated independently so that model skill is not confused with simple state accounting.

---

## 8. Research question

The smallest useful study is:

> Across resolved high/low markets, how much does the correctly reconstructed resolver-local first observation change the feasible bucket set and subsequent probability distribution, and how quickly do market prices reflect that information?

Evidence grade today:

- extrema constraint: exact;
- local-day mapping importance: exact;
- market inefficiency around the boundary: unmeasured.

This is a low-cost addition to the point-in-time data model and can reveal whether a neglected daily catalyst deserves further attention.