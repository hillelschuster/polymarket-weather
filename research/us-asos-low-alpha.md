# US ASOS daily-low alpha — the 12Z minimum checkpoint

Snapshot: **2026-08-11**

Purpose: extend the same ASOS extrema mechanism used for daily highs to Polymarket **lowest-temperature** markets.

The daily-low version may be even more economically attractive because the nocturnal minimum usually occurs near sunrise. A high-fidelity 6-hour minimum can therefore identify the eventual resolver bucket early in the local day, leaving many hours before Polymarket's civil-day window ends.

---

# 1. Same resolver math, reversed

For lowest-temperature contract state at time `t`:

`m_t = minimum authoritative observation achieved so far`.

Final daily low:

`L = min(m_t, R_t)`

where `R_t` is the lowest temperature possible over the remaining future path.

Once an observed minimum has entered a bucket:

- every **higher** bucket that excludes `m_t` becomes impossible;
- only the current bucket and lower reachable outcomes retain probability.

After sunrise, if temperatures are already rising and no strong cold advection is expected later, the probability of setting a new lower minimum can collapse rapidly.

---

# 2. The useful ASOS report clock is around 12Z

At many US ASOS stations, the synoptic METARs carry 6-hour minimum/maximum groups at 00/06/12/18Z.

12Z occurs approximately:

| Region in summer | 12Z local time |
|---|---:|
| Eastern | 08:00 EDT |
| Central | 07:00 CDT |
| Mountain | 06:00 MDT |
| Pacific | 05:00 PDT |

The exact routine METAR is commonly around `:51` before the synoptic hour.

This is close to the climatological overnight-minimum window for many airports.

The 12Z six-hour minimum covers roughly the preceding midnight-to-dawn period — exactly the interval most likely to contain the final daily low.

---

# 3. Resolved case: NYC / LaGuardia July 20, 2026

Polymarket event:

https://polymarket.com/event/lowest-temperature-in-nyc-on-july-20-2026

Resolver:

- LaGuardia `KLGA`;
- Weather Underground;
- whole degrees Fahrenheit;
- final winning bucket: **66–67°F**.

The LaGuardia METAR at:

- **2026-07-20 11:51 UTC**;
- **07:51 EDT**;

was:

`METAR KLGA 201151Z 03009KT 10SM FEW250 21/11 A3001 RMK AO2 SLP162 T02060106 10217 20194 51021 $`

The extrema groups encode:

- 6-hour maximum: `10217` → 21.7°C;
- **6-hour minimum: `20194` → 19.4°C = 66.9°F**.

### Final result

66.9°F lies directly in Polymarket's eventual **66–67°F** winning bucket.

The report arrived at **07:51 local**, approximately **16 hours 9 minutes before midnight**.

This is a much larger remaining trading window than the late-evening high-temperature examples.

---

# 4. Why the current spot temperature is again the wrong state variable

At 11:51 UTC / 07:51 EDT, KLGA's instantaneous temperature was:

- 20.6°C ≈ 69.1°F.

But the 6-hour minimum was:

- **19.4°C ≈ 66.9°F**.

So current temperature was already roughly **2.2°F above the overnight minimum**.

A bot reading only the current 69°F observation could incorrectly believe the daily low remained around 68–69°F or higher.

The ASOS extrema group explicitly said the station had already reached the eventual **66–67°F** outcome.

---

# 5. Remaining-low probability after sunrise

After the 12Z checkpoint, the only important meteorological question is:

> **Will the station fall below the known morning minimum later in the same civil day?**

In a normal diurnal cycle, this usually requires an unusual later event:

- strong cold-frontal passage;
- cold-air advection large enough to overcome daytime heating;
- convective outflow / rain-cooled air;
- rapid clearing plus unusually strong evening radiational cooling;
- other regime-specific reversal.

A simple model can estimate:

`P(new minimum below m_12Z before midnight)`.

This is easier than predicting the overnight low from the prior evening.

For many summer cases, that probability may be very small by late morning.

---

# 6. Daily lows may have better capital turnover than highs

A daily-high observation edge often becomes strongest around late afternoon/evening.

A daily-low observation edge can become strongest near dawn/morning.

That creates two potentially separate same-day capital cycles:

1. **morning:** trade low-temperature certainty collapse;
2. **afternoon/evening:** trade high-temperature certainty collapse.

The same bankroll can potentially turn through both if settlement/exit liquidity allows.

This is economically useful because it increases opportunity frequency without adding a new weather model family.

---

# 7. Exact low-side signal

For a known 6-hour minimum `m`:

1. map `m` to the resolver's whole-F bucket;
2. calculate remaining-path probability distribution from LAMP/HRRR/NBM/current conditions;
3. for each remaining path `k`, calculate:

`L_k = min(m, remaining_min_k)`;

4. convert `L_k` into Polymarket bucket probabilities;
5. compare all YES/NO expressions with executable fee-adjusted prices.

This is the mirror image of the daily-high T+0 formula.

---

# 8. Most informative price-response study

For each low market and 12Z extrema report:

sample the eventual winning token at:

- 5 min before report;
- report availability;
- +5m;
- +15m;
- +30m;
- +60m;
- +2h.

Also sample the immediate neighboring lower and higher buckets.

The strongest observation-latency signature would be:

- winning bucket materially below fair probability after the 6-hour minimum is published;
- higher impossible/implausible buckets still priced above zero;
- rapid convergence over the next minutes/hour.

If the market is already 95–100% by report time, the observation is useful for modeling but not a direct latency trade.

---

# 9. Do not assume morning minimum is permanently locked

The July 20 NYC case worked cleanly, but a trading rule must retain later-cooling probability.

Examples where the morning low can be broken later:

- evening frontal passage;
- post-convective cold pool;
- unusually dry clearing and strong sunset cooling;
- mountain/desert stations with large evening drops.

The correct model is conditional, not deterministic:

`q_current_bucket = 1 - P(later minimum crosses lower bucket boundary)`.

The simplicity comes from estimating only the remaining crossing probability.

---

# 10. Highest-value next samples

NYC daily-low markets already provide repeated resolved events and meaningful volume, including July 18, July 20 and others.

Then extend to airports where:

- ASOS extrema groups are available;
- low-temperature Polymarket markets recur;
- overnight cycle is reasonably regular;
- market volume supports useful dollar deployment.

Use exact current resolver rules for each city/date.

---

# 11. Shared parser with high-temperature strategy

No additional observation infrastructure is required.

The same raw METAR record yields:

- `1snTxTxTx` — six-hour maximum;
- `2snTnTnTn` — six-hour minimum;
- precise T-group;
- timestamp;
- current temperature.

The difference is only the extrema operator:

High:
`H = max(observed_max, remaining_max)`

Low:
`L = min(observed_min, remaining_min)`.

This is an unusually cheap way to add a second recurring market family.

---

# Bottom line

The first resolved low-temperature case is unusually clean:

> **At 07:51 EDT on July 20, KLGA's six-hour minimum was already 66.9°F, matching the final 66–67°F Polymarket winning bucket, with more than 16 hours left in the civil day.**

If historical price response shows that the market did not immediately incorporate this extrema field, US daily lows could be one of the simplest recurring observation-driven opportunities in the project.

Even if the market is fast, the 12Z minimum should still materially improve T+0 probability estimation at almost zero additional implementation cost.