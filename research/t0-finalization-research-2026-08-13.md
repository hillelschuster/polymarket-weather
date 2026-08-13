# T+0 resolver-source thesis — final research questions

Snapshot: **2026-08-13**

## Verdict

This remains the project's closest hypothesis to implementation because it already has synchronized live source/book evidence and historical replications.

The remaining research is no longer “does the market ever lag a weather observation?” That has been observed.

The remaining questions are:

1. how early can the chosen source actually expose resolver-relevant information;
2. how faithfully does that source map to the contractual resolver;
3. how often does economically meaningful market lag remain after actual source arrival;
4. how much capacity exists before the discrepancy disappears.

---

## 1. Source latency must be measured from first-seen, not valid time

The live KLGA case already demonstrated why.

The next research object should be a source race for the same station/report:

- NOAA station TXT first seen;
- AviationWeather.gov first seen;
- any available 5-minute ASOS stream first seen;
- MADIS OMO first seen via ordinary HTTPS/file path;
- MADIS OMO first seen via LDM if access is obtained;
- contractual Wunderground first seen where measurable;
- Polymarket material book change.

For each report:

`latency(source) = source_first_seen - observation_valid_time`.

Economic lead for source `s`:

`lead_s = market_material_reprice_time - source_first_seen_s`.

Only `lead_s > 0` is usable timing evidence for that source.

---

## 2. MADIS OMO is worth measuring, but ordinary MADIS file access is not automatically fast

NOAA MADIS documents 1-minute ASOS / One Minute Observations as a public operational feed for CONUS.

Important details:

- OMO observations arrive continuously/asynchronously;
- MADIS processes current/previous-hour OMO files every five minutes;
- ordinary MADIS real-time data accessed after stage-2 QC are documented as available on average about eight minutes after MADIS receives them;
- MADIS explicitly recommends **LDM** to users requiring the fastest access to real-time data;
- the MADIS application supports real-time LDM access and explicitly lists the 1-minute ASOS dataset.

Official sources:

- https://madis.ncep.noaa.gov/madis_OMO.shtml
- https://madis.ncep.noaa.gov/madis_ui.shtml
- https://madis.ncep.noaa.gov/madis_database.shtml
- https://madis.ncep.noaa.gov/data_application.shtml

Therefore the source hierarchy should distinguish:

`OMO via LDM`

from

`OMO via processed MADIS files/HTTPS`.

They are not economically equivalent.

A key next measurement is whether LDM receives OMO soon enough to materially precede the first Polymarket repricing at KLGA/KORD/KMIA-type resolver stations.

---

## 3. Resolver basis is a conditional probability, not an equality assumption

For source observation `x_t`, estimate:

`P(WU_final_bucket = k | source_path_to_t, remaining_weather)`.

Research must preserve disagreements caused by:

- whole-C versus tenth-C/whole-F representation;
- rolling average conventions;
- 1-minute versus METAR sampling;
- missing SPECI;
- Wunderground ingestion omissions;
- next-day revision/cutoff semantics.

The correct source is the one maximizing **resolver probability information per second of lead**, not necessarily the one with the highest sensor precision.

Useful source score:

`SourceValue = E[resolver information gain] * positive_lead_frequency * usable_market_capacity`.

---

## 4. Hard elimination versus soft probability revision

Separate two event classes.

### Hard state change

A new resolver-relevant observation makes a bucket mechanically impossible under the daily-extreme path.

For a daily high bucket with upper endpoint `U`:

`observed_running_max > U  => q_bucket = 0`.

This class requires almost no remaining forecast skill after source basis is trusted.

### Soft state change

A new observation changes survival/exceedance probability but does not eliminate a bucket.

For current running max `M_t` and candidate bucket `k`:

`q_k(t) = P(no later resolver value leaves bucket k | state_t)`.

Soft changes need a small remaining-weather model and are more vulnerable to calibration error.

Research should report the two classes separately because their required edge margin and expected half-life differ.

---

## 5. Market reaction statistic

Do not define “reprice” as first trade or UI price change.

For each source update, record the full relevant YES/NO book and define several market-response clocks:

- first best-bid change;
- first best-ask change;
- first material change, e.g. >= one tick or a chosen probability threshold;
- first trade after source update;
- first time depth-weighted executable value reaches the post-update region.

This lets research distinguish:

- quote cancellation;
- passive repricing;
- actual stale-flow fills.

The live NYC result showed that these clocks can differ by tens of seconds.

---

## 6. Capacity statistic

The correct historical/live capacity quantity is not event volume.

For a probability revision from `q0` to `q1`, define stale executable depth at source arrival:

`C(edge_min) = total shares available at prices whose all-in value remains at least edge_min away from q1`.

Track this through time after source arrival:

`C_tau(edge_min)` for tau = 0s, 1s, 5s, 10s, 30s, 60s.

This directly answers how many dollars the information lead can support before the market catches up.

---

## 7. Final historical/live dataset

For every resolver update:

### Source

- station;
- source type;
- raw source payload;
- valid time;
- provider-modified/published time if exposed;
- local first-seen timestamp.

### Resolver state

- running max/min before update;
- new source value;
- mapped resolver state distribution;
- hard-elimination flag;
- q vector before/after.

### Market

- condition/token IDs with explicit outcome labels;
- full relevant top-of-book/depth snapshots;
- first bid/ask changes;
- trade timestamps;
- short-horizon price history;
- eventual settlement.

The decisive output per event is:

`source lead seconds + probability revision + stale executable capacity + later markout`.

---

## 8. What would falsify or downgrade the thesis

Downgrade a particular source if:

- Polymarket usually reprices before the source first-seen time;
- source-to-Wunderground disagreements near bucket boundaries are frequent enough to erase the timing benefit;
- stale depth after source arrival is usually negligible;
- apparent markout is dominated by one event;
- the same information was already inferable from an earlier public source used by the market.

This would not falsify T+0 globally; it would falsify that source/city combination.

---

## 9. Finalization status

The thesis is sufficiently specified for dry implementation once one resolver/source pair has:

- measured first-seen timestamps;
- stable source-to-resolver mapping;
- repeated positive source-before-market lead;
- measurable stale executable depth after source arrival;
- deterministic q update from the source state.

For U.S. cities the highest-value unresolved research is therefore not another model. It is the **LDM/OMO versus market clock** and the source-to-Wunderground boundary mapping.