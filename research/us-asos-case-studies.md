# US ASOS case studies — earliest observable resolver bucket

Snapshot: **2026-08-11**

Purpose: identify the **earliest public observation time** at which a US airport's running observed maximum entered the eventual winning Polymarket bucket.

This replaces the weaker framing that treated the 6-hour extrema report itself as the signal.

The money-relevant state is:

`M_t = max(all authoritative temperature information publicly available by t)`.

Use every routine METAR, SPECI, precise `T` group and extrema group. The 6-hour maximum is valuable only when it reveals a peak not already visible in earlier reports.

The separate unresolved question remains whether Polymarket was still mispriced at the first-lock timestamp.

---

# 1. NYC / LaGuardia — July 20, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-nyc-on-july-20-2026

Resolver:

- `KLGA` LaGuardia;
- Weather Underground;
- whole °F;
- final bucket: **82–83°F**.

## Earlier routine observations

Aviation Weather history shows:

`METAR KLGA 202051Z ... T02720100 ...`

- 20:51 UTC / 16:51 EDT;
- precise T-group 27.2°C = 81.0°F.

Then:

`METAR KLGA 202151Z ... T02780100`

- **21:51 UTC / 17:51 EDT**;
- precise T-group **27.8°C = 82.0°F**.

At that moment the running observed maximum entered the eventual **82–83°F** winner.

The later report:

`METAR KLGA 202351Z ... T02390122 10283 20239 ...`

at 23:51 UTC / 19:51 EDT reported a six-hour max of **28.3°C = 82.9°F**, confirming the same bucket.

## Economic timing

Earliest verified bucket entry from the inspected routine stream:

- **17:51 EDT**;
- roughly **6h09m before local midnight**;
- roughly **2h before the 6-hour extrema summary**.

### Key lesson

The 6-hour max was not the unique information event here. A correct running-max parser would have reached the winning bucket earlier from the routine T-group.

The signal should fire when `M_t` first crosses a resolver boundary, regardless of report type.

---

# 2. Chicago / O'Hare — June 29, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-chicago-on-june-29-2026

Resolver:

- `KORD` O'Hare;
- Weather Underground;
- whole °F;
- final bucket: **92–93°F**.

Aviation / CheckWX history shows the afternoon sequence:

`KORD 291851Z ... T03220239`

- 18:51 UTC / 13:51 CDT;
- 32.2°C = 90.0°F.

`KORD 291951Z ... T03280233`

- 19:51 UTC / 14:51 CDT;
- 32.8°C = 91.0°F.

`KORD 292051Z ... T03330228`

- **20:51 UTC / 15:51 CDT**;
- precise T-group **33.3°C = 91.9°F**.

At whole-F resolver precision, that is the **92°F** side of the eventual 92–93°F bucket.

Further routine observations remained at the same peak:

- 21:51 UTC: `T03330228`;
- 22:51 UTC: `T03280233`.

The 23:51 UTC synoptic report later gave:

`10333`

- six-hour maximum **33.3°C / 91.9°F**;
- instantaneous T-group only 31.7°C / 89.1°F.

## Economic timing

Earliest verified winning-bucket observation:

- **15:51 CDT**;
- roughly **8h09m before local midnight**;
- roughly **3 hours before the 00Z-era 6-hour-max report**.

### Key lesson

Again, the profitable state is the running maximum, not the scheduled extrema summary.

A bot polling every routine METAR would know the resolver had reached the 92°F region several hours earlier than one waiting for the six-hour group.

---

# 3. Chicago / O'Hare — June 20, 2026

Polymarket event:

https://polymarket.com/event/highest-temperature-in-chicago-on-june-20-2026

Resolver:

- `KORD`;
- Weather Underground;
- whole °F;
- final bucket: **76–77°F**.

Official Aviation Weather history shows:

### Early afternoon

17:51 UTC / 12:51 CDT:

`T02330100 10239 20172`

- instantaneous 23.3°C / 73.9°F;
- preceding six-hour max 23.9°C / 75.0°F.

18:51 UTC:

`T02330111`

- 73.9°F.

19:51 UTC:

`T02390106`

- **23.9°C / 75.0°F**.

22:51 UTC:

`T02390100`

- 75.0°F.

### Late synoptic extrema

23:51 UTC / 18:51 CDT:

`T02390100 10250 20228`

- instantaneous 23.9°C / 75.0°F;
- **six-hour maximum 25.0°C / 77.0°F**.

The following early-morning report later included a 24-hour maximum of 25.0°C / 77.0°F.

## Current evidence

The indexed official history inspected so far shows routine spot/T-group values up to 75°F, while the 23:51 report reveals a 77°F six-hour maximum.

This is therefore the strongest current candidate for a **hidden between-report peak**: a whole bucket-width increase in the authoritative running maximum that is not visible in the routine observations we have recovered.

However, the complete 20:51/21:51/SPECI set must be checked before calling the 23:51 extrema group the *first* public 77°F evidence.

### Economic significance if confirmed

If no intervening METAR/SPECI exposed 25.0°C, then parsing the six-hour extrema group adds genuinely new resolver information beyond ordinary hourly feeds.

This is the exact data advantage worth measuring, rather than assuming every six-hour extrema report is unique.

---

# 4. Corrected event-state table

| Event | First verified winning-bucket state | Local time | Source | Later 6h max | Hours to midnight |
|---|---|---:|---|---:|---:|
| NYC Jul 20 | 27.8°C = 82.0°F → 82–83 | **17:51 EDT** | routine T-group | 82.9°F | 6h09m |
| Chicago Jun 29 | 33.3°C = 91.9°F → 92–93 | **15:51 CDT** | routine T-group | 91.9°F | 8h09m |
| Chicago Jun 20 | 77°F candidate first visible at late extrema report | **≤18:51 CDT** | 6h max unless earlier omitted report exists | 77.0°F | ≥5h09m |

This materially improves the research target.

---

# 5. The true observation-driven signal

For each incoming report at timestamp `t`:

1. parse current precise temperature;
2. parse any SPECI precise temperature;
3. parse six-hour max if present;
4. update:

`M_t = max(M_{t-1}, all newly reported credible extrema)`;

5. map `M_t` into the Polymarket resolver's native Fahrenheit bucket;
6. estimate only the probability of a later crossing into a **higher** bucket.

Signal importance is highest when a new report:

- enters a new bucket;
- crosses the midpoint/rounding threshold relevant to whole-F resolution;
- eliminates lower outcomes;
- substantially lowers remaining-crossing probability because peak time has passed.

There is no need to privilege 18Z/00Z except that their extrema fields can reveal peaks the routine stream missed.

---

# 6. Why this is simpler and potentially earlier

The old framing waited for a scheduled six-hour extrema report.

The corrected approach reacts immediately whenever the station first enters a resolver bucket.

For NYC Jul 20 that advances the useful state by about **2 hours**.

For Chicago Jun 29 it advances it by about **3 hours**.

If Polymarket price convergence is slower than these observation updates, this earlier trigger directly increases captured edge and fill capacity.

---

# 7. Resolver fidelity hierarchy

For US same-day reconstruction, retain raw METAR/SPECI text and derive:

1. precise T-group temperature;
2. native/processed Fahrenheit where reliable;
3. routine mandatory whole-C field;
4. six-hour extrema;
5. later 24-hour/DSM truth.

The empirical question is which combination reproduces Weather Underground/Polymarket resolutions most reliably.

The six-hour max is best viewed as a **gap-filling observation**, not the primary state variable.

---

# 8. Price-latency test must use the first-lock timestamp

For each event define:

`t_lock = first public report time when running observed extreme enters the eventual resolver bucket`.

Then sample the full Polymarket ladder around:

- `t_lock - 5m`;
- `t_lock`;
- `+5m`;
- `+15m`;
- `+30m`;
- `+60m`;
- `+2h`.

This is superior to anchoring every event on 00Z/12Z.

Measure:

`markout_tau = p_winner(t_lock+tau) - executable_price(t_lock)`

and the collapse of now-impossible neighboring buckets.

---

# 9. Remaining meteorological uncertainty

Entering the eventual winning bucket does not mean it will remain the winner.

The tradable fair probability after `t_lock` is:

`P(no later temperature crosses the next bucket boundary | current atmosphere, remaining hours)`.

This is where LAMP/HRRR/NBM and recent station trajectory belong.

The high-value combination is:

> **authoritative running maximum + simple remaining-boundary-crossing probability.**

That is much easier than forecasting the whole-day maximum from scratch.

---

# Bottom line

The case-study audit improves the US observation thesis:

> **Track the exact resolver-aligned running maximum continuously. Routine T-groups often reveal the final bucket hours before the scheduled extrema summary; six-hour extrema groups add value primarily when they expose hidden between-report peaks.**

NYC Jul 20 and Chicago Jun 29 prove the earlier-running-max mechanism. Chicago Jun 20 is the current best candidate for genuine extra information from a six-hour extrema field.

The decisive remaining economic test is still the same: **what executable Polymarket price remained at the first-lock timestamp?**