# Edge economics — how much forecast advantage is actually worth money

Snapshot: **2026-08-11**

This note answers one narrow question:

> Given an executable Polymarket Weather price and an internal fair probability, how large must the disagreement be to produce worthwhile dollar EV?

The eventual trading logic only needs this arithmetic plus a calibrated resolver probability.

---

# 1. Taker economics

For a fee-enabled Weather YES purchase at executable ask `a`:

`fee_per_share = 0.05 * a * (1-a)`

`c = a + fee_per_share`

where `c` is all-in cost per share before additional book-walking slippage.

With fair settlement probability `q`:

`EV_per_share = q - c`

For dollar notional `N`:

`shares = N / c`

`expected_profit = N * (q/c - 1)`

This is the economically correct ranking variable for a taker BUY.

---

# 2. Fee hurdle before slippage

| Executable ask | Fee/share | All-in cost | Fair q needed just to break even |
|---:|---:|---:|---:|
| 20¢ | 0.80¢ | 20.80¢ | 20.80% |
| 30¢ | 1.05¢ | 31.05¢ | 31.05% |
| 40¢ | 1.20¢ | 41.20¢ | 41.20% |
| 50¢ | 1.25¢ | 51.25¢ | 51.25% |
| 60¢ | 1.20¢ | 61.20¢ | 61.20% |
| 70¢ | 1.05¢ | 71.05¢ | 71.05% |
| 80¢ | 0.80¢ | 80.80¢ | 80.80% |

At the supplied wallet's typical 25–60¢ entry prices, the fee consumes roughly **1.0–1.25 probability points**.

If a research model reports “3 points of edge” versus the midpoint while the ask sits another 0.5–1.0 points above midpoint, most of that edge can disappear immediately. The model should therefore compare directly to the executable ask.

---

# 3. Dollar return from probability advantage

The table below assumes `q = ask + probability advantage`, uses the current Weather taker fee, and ignores extra depth slippage.

## At a 30¢ ask

All-in cost = 31.05¢.

| Fair q | Raw q-ask advantage | Expected ROI on dollars |
|---:|---:|---:|
| 32% | +2 pp | +3.1% |
| 33% | +3 pp | +6.3% |
| 35% | +5 pp | +12.7% |
| 38% | +8 pp | +22.4% |
| 40% | +10 pp | +28.8% |

## At a 40¢ ask

All-in cost = 41.20¢.

| Fair q | Advantage | Expected ROI |
|---:|---:|---:|
| 42% | +2 pp | +1.9% |
| 43% | +3 pp | +4.4% |
| 45% | +5 pp | +9.2% |
| 48% | +8 pp | +16.5% |
| 50% | +10 pp | +21.4% |

## At a 50¢ ask

All-in cost = 51.25¢.

| Fair q | Advantage | Expected ROI |
|---:|---:|---:|
| 52% | +2 pp | +1.5% |
| 53% | +3 pp | +3.4% |
| 55% | +5 pp | +7.3% |
| 58% | +8 pp | +13.2% |
| 60% | +10 pp | +17.1% |

## At a 60¢ ask

All-in cost = 61.20¢.

| Fair q | Advantage | Expected ROI |
|---:|---:|---:|
| 62% | +2 pp | +1.3% |
| 63% | +3 pp | +2.9% |
| 65% | +5 pp | +6.2% |
| 68% | +8 pp | +11.1% |
| 70% | +10 pp | +14.4% |

## At a 70¢ ask

All-in cost = 71.05¢.

| Fair q | Advantage | Expected ROI |
|---:|---:|---:|
| 72% | +2 pp | +1.3% |
| 73% | +3 pp | +2.7% |
| 75% | +5 pp | +5.6% |
| 78% | +8 pp | +9.8% |
| 80% | +10 pp | +12.6% |

---

# 4. Economic interpretation

The price regime changes how valuable a fixed probability-point edge is.

At 30¢, a 5-point forecast advantage produces roughly **12.7% expected return on committed dollars** before extra slippage.

At 50¢, the same 5 points produces roughly **7.3%**.

At 70¢, it produces roughly **5.6%**.

This does **not** mean low-price contracts are automatically better. Tail probabilities are harder to calibrate, and forecast error in a 30¢ bucket can be larger. It means the ranking should use dollar EV after cost rather than probability-point edge alone.

A compact score is:

`expected_dollars_i = candidate_notional_i * (q_i/c_i - 1)`

Then compare opportunities across all cities and buckets.

---

# 5. What the supplied wallet implies about economically meaningful edge

Recovered BUYs include:

- Milan June 30 35°C at about **29.38¢ raw / 30.42¢ all-in**;
- July 12 unresolved outcome at about **26.56¢ raw / 27.54¢ all-in**.

Its current visible portfolio has a median raw entry around **49.55¢** and many positions near 40–60¢.

The wallet is therefore repeatedly willing to pay the largest part of the Weather fee curve.

That is informative: a strategy centered on intermediate-probability buckets must often believe its fair probability is several points away from the ask, not a fraction of a point away.

Current visible markouts support that scale. Examples include a Madrid Aug 12 38°C entry around 31.5¢ before a later market around the high-50s, and several other T+1 entries that subsequently moved 10+ points in the wallet's direction.

The research target should be **large, explainable probability revisions**, not statistical detection of 0.5-point discrepancies.

---

# 6. Spread and book depth

The ask already embeds the immediate cost of crossing the spread. Therefore:

- when comparing `q` to the **ask**, do not subtract half-spread a second time;
- when a research signal is defined versus **midpoint**, convert it to executable ask before computing EV.

Live modal weather buckets inspected on Aug 11 frequently showed roughly **1–2¢ top-of-book spreads** near 40–60¢. Combined with the ~1.2–1.25¢ taker fee in that region, a signal that is only 2 points above midpoint can easily have no executable EV.

Depth adds another simple term. For intended dollar size `N`, walk the ask levels until filled and calculate volume-weighted average acquisition cost plus fee at each fill price.

No generic slippage model is necessary if the actual book is available.

---

# 7. Maker versus taker

A passive maker fill has no Weather trading fee under the current schedule and may receive maker rebates. But its expected value is not simply `q - maker_price` because fill probability and adverse selection matter.

The useful comparison is:

`taker_EV = immediate_fill_EV`

versus

`maker_EV = fill_probability * (fair_value_at_fill - quote_price + expected_rebate - expected_adverse_markout)`.

For short-lived information shocks, crossing can dominate because waiting loses the forecast advantage.

For slow-moving T+1 distributions, passive quoting may preserve more edge.

The supplied wallet's recovered fee-paying BUYs prove that at least some opportunities are valuable enough to justify taking immediately.

---

# 8. Exit economics

At current bid `b`:

`sell_fee = 0.05 * b * (1-b)`

`net_bid = b - sell_fee`

If updated fair probability is `q_new`, selling dominates pure hold value when:

`net_bid > q_new`.

For a nearly certain winner, add capital reuse:

`sell_now = net_bid + expected_value_of_redeployment_before_settlement`

`hold = q_new`

The recovered Mexico City position sold at ~99.9¢ just after local midnight is exactly this second problem. A tiny discount to $1 can be worth paying if the released dollars immediately fund another high-EV weather opportunity.

---

# 9. What this means for sizing

The supplied wallet appears to use round-dollar tiers around $100, $150, $200, $250, $400 and $450 rather than continuous share-based sizing.

A minimal eventual rule can therefore be:

1. calculate expected ROI and expected dollars for each candidate;
2. assign a simple notional tier based on edge strength, forecast confidence and available depth;
3. allocate more dollars only when the incremental expected dollar return remains attractive.

There is no evidence yet that a continuous Kelly formula is necessary to capture the observed behavior.

---

# Bottom line

The economically relevant signal is not `forecast_probability - midpoint`.

It is:

`net_edge_i = calibrated_probability_i - executable_all_in_cost_i`

and the allocation objective is:

`maximize Σ expected_dollars_i`.

At the price levels weather specialists actually trade, **5–10 probability points of genuine forecast advantage are highly monetizable**, while 1–2 point disagreements are often mostly consumed by fee/spread friction.
