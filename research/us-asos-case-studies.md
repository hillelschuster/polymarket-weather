# US ASOS extrema case studies — resolver information before midnight

Snapshot: **2026-08-11**

Purpose: validate the concrete part of the ASOS observation-alpha thesis on resolved Polymarket daily-high events.

The question in this file is deliberately narrow:

> **Did a late-day ASOS 6-hour maximum already identify the eventual winning Polymarket Fahrenheit bucket while the local civil day was still open?**

This is **not yet** a claim that Polymarket prices were stale after the report. The separate price-response study remains necessary.

---

# 1. Chicago — June 20, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-chicago-on-june-20-2026

Resolver:

- Chicago O'Hare `KORD`;
- Weather Underground;
- whole degrees Fahrenheit;
- final winning bucket: **76–77°F**.

Official Aviation Weather Center history shows:

`METAR KORD 202351Z 32007KT 10SM SCT080 SCT250 24/10 A2991 RMK AO2 SLP126 T02390100 10250 20228 58006`

Timestamp:

- **2026-06-20 23:51 UTC**;
- **18:51 CDT**.

Decoded 6-hour maximum:

- `10250` → **25.0°C = 77.0°F**.

The ordinary instantaneous METAR temperature at that moment was only **75.0°F**.

### Result

The 6-hour extrema field said **77°F**, directly inside the final **76–77°F winning bucket**, while the instantaneous displayed temperature was lower.

This was available at approximately **18:51 local**, about **5 hours 9 minutes before local midnight**.

The following day's early ASOS report later carried a 24-hour maximum of 77.0°F as well, confirming the same daily maximum.

Primary sources:

- Aviation Weather Center METAR history for KORD;
- Polymarket resolved event above.

### Why this matters

A strategy watching only current temperature at 18:51 would see 75°F. The extrema remark already encoded a 77°F peak that had occurred during the preceding six hours.

For the prediction market, those are materially different states.

---

# 2. New York / LaGuardia — July 20, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-nyc-on-july-20-2026

Resolver:

- LaGuardia `KLGA`;
- Weather Underground;
- whole degrees Fahrenheit;
- final winning bucket: **82–83°F**.

Aviation Weather Center history shows:

`METAR KLGA 202351Z 18009KT 10SM FEW200 SCT250 24/12 A2995 RMK AO2 SLP141 T02390122 10283 20239 53001`

Timestamp:

- **2026-07-20 23:51 UTC**;
- **19:51 EDT**.

Decoded state:

- instantaneous temperature: **75.0°F**;
- 6-hour maximum: **28.3°C = 82.9°F**.

### Result

The 6-hour maximum maps directly into the eventual **82–83°F** Polymarket winner.

It was published around **19:51 local**, approximately **4 hours 9 minutes before midnight**.

The information gap versus current-temperature displays is extreme in this example:

- instantaneous observation: 75°F;
- peak-window 6-hour max: 82.9°F.

Anyone using only the current reading would be looking at a completely different resolver state.

---

# 3. Chicago — June 29, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-chicago-on-june-29-2026

Resolver:

- O'Hare `KORD`;
- Weather Underground;
- whole degrees Fahrenheit;
- final winner: **92–93°F**.

Aviation Weather Center history shows:

`METAR KORD 292351Z 20017G26KT 10SM SCT042 BKN250 32/23 A2988 RMK AO2 PK WND 19028/2330 SLP110 T03170228 10333 20311 55001 $`

Timestamp:

- **2026-06-29 23:51 UTC**;
- **18:51 CDT**.

Decoded state:

- instantaneous temperature: **89.1°F / 31.7°C**;
- 6-hour maximum: **91.9°F / 33.3°C**.

Polymarket ultimately resolved **92–93°F**.

### Result

The 6-hour max of 91.9°F is the high-fidelity value that, when represented at the contract's whole-Fahrenheit resolution, is consistent with the **92–93°F winning bucket**.

Again, the instantaneous temperature was materially lower than the already-observed peak.

The report arrived roughly **5 hours before local midnight**.

---

# 4. Three-event pattern

| Event | Report local time | Instant temp | 6h max | Final Polymarket bucket | Time to midnight |
|---|---:|---:|---:|---|---:|
| Chicago Jun 20 | 18:51 CDT | 75.0°F | **77.0°F** | **76–77°F** | 5h09m |
| NYC Jul 20 | 19:51 EDT | 75.0°F | **82.9°F** | **82–83°F** | 4h09m |
| Chicago Jun 29 | 18:51 CDT | 89.1°F | **91.9°F** | **92–93°F** | 5h09m |

All three cases have the same economically useful shape:

1. the afternoon/evening peak had already occurred or nearly occurred;
2. current temperature had fallen below that peak;
3. the synoptic METAR explicitly reported the preceding 6-hour maximum;
4. that maximum mapped to the eventual winning Polymarket bucket;
5. several hours of local-day trading time remained.

This validates the **information object**. It does not yet validate the **price lag**.

---

# 5. Why ordinary current-temperature feeds can be materially wrong for trading

In the three cases above, current temperature versus 6-hour maximum differed by:

- Chicago Jun 20: **2.0°F**;
- NYC Jul 20: **7.9°F**;
- Chicago Jun 29: **2.8°F**.

Every difference is at least one full 2°F Polymarket bucket width; NYC spans several buckets.

Thus a simplistic T+0 algorithm of:

`current airport temperature + forecast remaining heating`

can badly misrepresent the state if it does not separately track the maximum already achieved.

The minimum state variable is:

`M_t = maximum authoritative temperature observed/reported so far`.

For US ASOS, the 6-hour max report can improve `M_t` materially beyond spot observations.

---

# 6. Minimal trading probability after the 00Z/late-day report

Once the late-day 6-hour max `M` is known, the problem is no longer a full-day high forecast.

It becomes:

`P(final maximum exceeds M before local midnight | current state)`.

For many late-day regimes this can be tiny because:

- solar forcing is collapsing;
- the current temperature is already below the peak;
- the next several hours are evening/night;
- LAMP/HRRR/NBM can estimate any exceptional rebound risk.

Then the probability vector is approximately:

- large mass on the bucket containing `M`;
- small mass on only higher reachable buckets;
- zero mass on buckets below the known observed maximum.

That is a much easier inference problem than predicting the original high 24 hours earlier.

---

# 7. The most important unresolved test: did the market already know?

These case studies become a trading edge only if the winning bucket was still available below its fair value when the extrema report became public.

For each event we need the winning-token price around the report timestamp:

- `t - 5m`;
- `t`;
- `t + 5m`;
- `t + 15m`;
- `t + 30m`;
- `t + 60m`.

Then calculate:

`observation_markout_tau = p(t+tau) - executable_price_at_signal`.

Also compare neighboring buckets.

A strong result would look like:

- winning bucket still 50–80¢ immediately after the high-fidelity max report;
- higher/lower impossible buckets still retain meaningful price;
- prices converge toward 1/0 over the following minutes.

A weak/no-edge result would be:

- winning bucket already ~98–100¢ before the report;
- no fillable depth at stale prices;
- repricing occurs faster than our acquisition path.

The entire ASOS thesis can be judged by this one event-study family.

---

# 8. Do not require the 6-hour max to be the final max deterministically

The report covers the preceding six hours, not the remaining night.

The correct signal is probabilistic:

`q_same_bucket = 1 - P(later exceedance crosses next bucket boundary)`.

Cases with ongoing warm advection, downslope wind, fronts, unusual nighttime mixing or late-day western peaks can still exceed `M`.

The benefit of the 6-hour max is not certainty by definition. It is that it gives a much higher-fidelity lower bound on the final resolver maximum.

---

# 9. High/low symmetry

The same logic applies to lowest-temperature markets using the METAR 6-hour **minimum** group.

The most relevant report clock differs because the overnight minimum usually occurs around dawn rather than afternoon.

Once daily-high observation latency is quantified, daily lows can reuse essentially the same parser/math:

`final_min = min(observed_min_so_far, remaining_min)`.

This potentially doubles the recurring US opportunity set with almost no new statistical machinery.

---

# 10. Money-relevant conclusion

Three resolved 2026 US Polymarket events independently confirm that the ASOS 6-hour extrema field can expose the eventual winning temperature bucket **4–5 hours before local midnight**, while the instantaneous airport temperature has already moved materially away from the high.

That makes ASOS extrema parsing one of the highest-value simple T+0 research targets.

The next decision is binary and empirical:

> **After the 18Z/00Z 6-hour extrema publication, does Polymarket still offer stale probability at executable size?**

If yes, this may be simpler and higher-confidence than trying to win purely through better multi-model forecasting. If no, the same extrema state still materially improves same-day probability calibration.