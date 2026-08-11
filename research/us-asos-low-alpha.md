# US ASOS daily-low alpha — running minimum after dawn

Snapshot: **2026-08-11**

Purpose: define the simplest resolver-state strategy for Polymarket US **lowest-temperature** markets.

The initial 12Z-extrema framing was too narrow. The correct signal is earlier and simpler:

> **Track the exact running observed minimum from every routine METAR/SPECI/T-group. Use the six-hour minimum only to recover a lower trough that routine reports missed.**

For time `t`:

`m_t = min(all credible resolver-aligned temperatures publicly available by t)`

and final daily low:

`L = min(m_t, remaining_future_min)`.

---

# 1. NYC / LaGuardia July 20 — final bucket visible before 12Z summary

Polymarket event:

https://polymarket.com/event/lowest-temperature-in-nyc-on-july-20-2026

Resolver:

- `KLGA` LaGuardia;
- Weather Underground;
- whole °F;
- final bucket: **66–67°F**.

Aviation Weather history shows the overnight sequence.

At:

- **09:51 UTC / 05:51 EDT**

routine METAR:

`METAR KLGA 200951Z 03005KT 10SM CLR 19/12 A2997 RMK AO2 SLP150 T01940117 $`

The precise T-group is:

- **19.4°C = 66.9°F**.

That is already inside the eventual **66–67°F winning bucket**.

Two hours later, at 11:51 UTC / 07:51 EDT:

`METAR KLGA 201151Z ... T02060106 10217 20194 ...`

reported the same **19.4°C** as the six-hour minimum.

## Correct economic timing

The winning bucket was publicly observable from the routine stream by **05:51 EDT**, not first at the 12Z extrema report.

That leaves roughly **18h09m until local midnight**.

The 12Z-era minimum summary confirms the trough but does not create the earliest signal in this case.

---

# 2. Why this is more attractive than the original checkpoint idea

At 05:51 EDT the station had reached 66.9°F.

Subsequent routine values rose:

- 06:51 EDT equivalent reports higher;
- 07:51 EDT current value was ~69.1°F;
- later daytime temperatures continued upward.

The economic problem from the first trough is simply:

> **What is the probability KLGA falls below 66.9°F again before local midnight?**

In a normal summer diurnal cycle, that can become small quickly after sunrise.

So the market can potentially be valued from an authoritative lower bound **before most of the day's capital is locked**.

---

# 3. Running-minimum update rule

For every new report:

1. parse precise T-group;
2. parse SPECI if any;
3. parse six-hour minimum if present;
4. update:

`m_t = min(m_{t-1}, newly observed minima)`;

5. map `m_t` into the native Polymarket bucket;
6. estimate probability of a later move into a still-lower bucket.

A trading signal is strongest when:

- `m_t` enters a new resolver bucket;
- temperature immediately begins/continues rising;
- sunrise has passed;
- remaining forecast paths rarely fall below `m_t` later;
- the market still assigns meaningful probability to higher or lower alternatives inconsistent with the new state.

---

# 4. Six-hour minimum remains useful as a gap filler

Routine observations can miss the true trough between reports.

The six-hour minimum field can then lower `m_t` beyond every routine T-group seen so far.

That is a genuinely new information event.

Do not assume it happens every day. Measure it.

For each event classify the first final-bucket observation as:

- routine T-group;
- SPECI;
- six-hour minimum;
- other resolver source.

This directly tells us how much unique value the extrema parser contributes.

---

# 5. Daily-low probability after first bucket entry

Suppose `m_t` is in bucket `B`.

For each remaining-path scenario `k`:

`L_k = min(m_t, remaining_min_k)`.

Bucket probabilities are simply frequencies of `L_k` outcomes.

Near/after sunrise the distribution often becomes concentrated because only a substantial later cool-down can leave `B` for a lower bucket.

Useful predictors of later re-break probability:

- forecast minimum over remaining local day;
- cold-front timing;
- convective/rain-cooled outflow risk;
- evening dewpoint/cloud/wind regime;
- current trend relative to `m_t`;
- climatological remaining-night cooling potential before midnight.

Start with remaining-path NBM/LAMP/HRRR plus observed state. Add other variables only if they improve dollar PnL.

---

# 6. Capital-turnover advantage

Daily lows can produce information very early.

NYC Jul 20 demonstrates a final-bucket state by **05:51 local**.

If price remains inefficient around that time, a position can potentially:

- be opened in the morning;
- reprice during the day;
- be exited/recycled before the afternoon high-temperature opportunity.

That creates two independent daily weather cycles from the same station parser:

1. morning running-minimum edge;
2. afternoon running-maximum edge.

This can materially increase dollars earned per unit bankroll if both have positive EV.

---

# 7. The correct price-response anchor

Do not anchor daily-low studies automatically at 12Z.

For each event define:

`t_lock = first timestamp when m_t enters the eventual winning bucket`.

Sample market prices at:

- `t_lock - 5m`;
- `t_lock`;
- `+5m`;
- `+15m`;
- `+30m`;
- `+60m`;
- `+2h`;
- later morning/afternoon.

Measure both:

- winning-bucket repricing;
- residual price in buckets made impossible or highly implausible by the observed minimum.

The latter can support either YES or NO expressions depending on book prices.

---

# 8. Do not equate entering the eventual bucket with certainty

A morning observed minimum can still be broken later in the same civil day by:

- cold-front passage;
- strong cold advection;
- rain-cooled outflow;
- unusually fast evening radiational cooling;
- high-elevation/desert diurnal regimes.

The signal is:

`q_B = P(no later crossing into lower bucket | observed state + remaining forecast)`.

This may be 60%, 90% or 99% depending on regime. Trade only when price is below the fee-adjusted fair value.

---

# 9. Shared high/low implementation object

One small parser supports both families.

Maintain:

`running_max_F`

`running_min_F`

from:

- precise T-group;
- SPECI;
- native/processed station temperature if fidelity is known;
- six-hour extrema;
- final DSM/24h extrema for validation.

Then:

High:
`H = max(running_max, remaining_max)`

Low:
`L = min(running_min, remaining_min)`.

Nothing more elaborate is required to express the observation-conditioned state.

---

# 10. Highest-value next empirical sample

Build a resolved-event table for NYC and other US low markets with:

`event`
`winning_bucket`
`first_time_running_min_enters_winner`
`source_type`
`minutes_after_local_sunrise`
`hours_to_midnight`
`market_price_at_first_lock`
`+5m/+30m/+2h markout`
`later_lower_crossing?`

The key questions are:

1. How early is the winning bucket usually first observed?
2. How often is that bucket later broken by a new lower reading?
3. What price remains at first lock?
4. Which regimes produce the highest net dollars?

---

# Bottom line

NYC July 20 sharpens the daily-low strategy materially:

> **The eventual 66–67°F winner was already in the routine KLGA T-group at 05:51 EDT, about 18 hours before midnight and two hours before the six-hour minimum summary confirmed it.**

The opportunity is therefore not a fixed 12Z-report trade. It is a **continuous running-minimum strategy** that reacts the first time the resolver enters a new bucket and estimates only the chance of a later lower crossing.