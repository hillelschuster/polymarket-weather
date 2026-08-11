# Post-source-lock / pre-resolution Weather edge

Snapshot: **2026-08-11**

Purpose: isolate the daily period where a Weather market's rules have already made the resolver outcome mechanically knowable, but Polymarket has not yet completed formal UMA resolution.

## Verdict

This is a distinct and potentially high-confidence Weather edge:

> **Monitor the exact resolution source and rule-defined lock condition. As soon as the outcome becomes contractually fixed, value the winning YES and every losing NO at deterministic terminal value, then choose the highest-return route among taking stale near-$1 quotes, posting maker liquidity, NegRisk conversion of losing-NO baskets, or simply recycling existing winners.**

The edge is not meteorological forecasting. It is **resolution-source latency + CLOB repricing latency + UMA settlement latency**.

It exists every day in principle, but actual net dollars depend on:

- how quickly other bots observe the source lock;
- stale depth remaining after lock;
- current Weather taker fee near 0/1;
- event `negRiskFeeBips`;
- whether the CLOB remains tradeable at that exact stage;
- time until collateral becomes redeemable;
- the source-specific rule text.

The supplied target wallet already provides one concrete behavioral clue: it sold 38 winning Mexico City Jul 16 shares at roughly 99.9¢ only about five minutes after the local civil day ended, suggesting specialists actively recycle near-certain Weather capital rather than always wait for redemption. This is suggestive, not sufficient proof that the exact rule-defined source lock had already occurred at that fill.

---

# 1. The lock condition is written into many Weather rules

Example: NYC daily high / Wunderground LaGuardia markets state:

- the market cannot resolve until the first datapoint for the following date is published on the resolution source;
- revisions to the target day's temperatures are considered **until that first following-date datapoint**;
- alterations after that datapoint are not considered.

Example market:

https://polymarket.com/event/highest-temperature-in-nyc-on-june-14-2026/highest-temperature-in-nyc-on-june-14-2026-90-91f

Therefore there is a rule-defined time `t_lock`:

`t_lock = first publication on resolver source that makes later revisions irrelevant`.

After `t_lock`, if the page clearly identifies the daily maximum, the winning bucket is contractually fixed under those rules even though the CTF outcome may not yet be resolved onchain.

Milan markets using Wunderground LIMC use materially the same rule structure.

---

# 2. Other cities have different lock semantics

The engine must not assume a universal midnight rule.

Examples found in current/historical Polymarket Weather rules:

### Wunderground next-day-datapoint class

Examples include NYC and Milan.

Lock occurs only after the first datapoint for the following date appears. Revisions before that point count; later alterations do not.

### Wunderground finalized-data class

Some Seoul historical markets state that the market cannot resolve Yes until all data for the date has been finalized and that revisions after finalization do not count.

Example:

https://polymarket.com/event/highest-temperature-in-seoul-on-may-7-2026

Later Seoul markets sometimes use the next-day-datapoint wording instead, so rules can change by date even for the same city/station.

### Official-agency finalized-publication class

Hong Kong markets use the Hong Kong Observatory's `Daily Extract` / `Absolute Daily Max` and specify that the market cannot resolve until the date's data is published/finalized; later revisions after the specified publication/finalization do not count.

Example:

https://polymarket.com/event/highest-temperature-in-hong-kong-on-may-2-2026/highest-temperature-in-hong-kong-on-may-2-2026-26c

This creates a discrete source-publication catalyst rather than a simple local-midnight trigger.

### Consequence

For each city/date, parse and store the actual rule text and classify the lock trigger. Do not infer lock time from city alone.

---

# 3. Formal Polymarket resolution creates additional delay

Polymarket's current resolution documentation describes:

1. someone proposes a winning outcome and posts a bond;
2. UMA enters a **2-hour challenge period**;
3. if undisputed, the proposal is accepted and the market resolves;
4. disputes can extend the process substantially.

Official documentation:

https://docs.polymarket.com/concepts/resolution

Therefore:

`t_redeemable - t_lock`

can include:

- time before anybody proposes;
- the two-hour challenge period;
- any dispute/reproposal latency.

For clean Weather outcomes this creates a recurring interval in which economic uncertainty can be much lower than settlement latency.

Do not assume the interval is exactly two hours; two hours is only the challenge period after proposal.

---

# 4. Near-$1 taker fees are tiny

Current Weather taker fee formula:

`fee/share = 0.05 * p * (1-p)`.

At high-confidence prices:

| Price | Fee/share | Fee in cents/share |
|---:|---:|---:|
| 0.990 | 0.000495 | 0.0495¢ |
| 0.995 | 0.00024875 | 0.024875¢ |
| 0.998 | 0.0000998 | 0.00998¢ |
| 0.999 | 0.00004995 | 0.004995¢ |

This is fundamentally different from the ~1¢/share fee around 30–70¢.

For a source-locked winning YES ask `a`:

`hold_to_redeem_edge/share = 1 - a - 0.05*a*(1-a) - capital_time_cost`.

Examples before capital-time:

- buy at 99.0¢ -> ~0.9505¢ net edge/share;
- buy at 99.5¢ -> ~0.4751¢;
- buy at 99.8¢ -> ~0.1900¢;
- buy at 99.9¢ -> ~0.0950¢.

The percentage return is small, but the outcome can be economically deterministic after source lock and the holding period may be hours rather than days.

Capacity, not forecast accuracy, is likely the limiting variable.

Official fee docs:

https://docs.polymarket.com/trading/fees

---

# 5. Losing NO tokens are equally deterministic after lock

If winning bucket is `w`, then for every other bucket `i != w`:

`N_i -> $1` at resolution.

A source-locked losing-NO ask `aNi` therefore has the same simple hold-to-redemption economics:

`edge_i = 1 - aNi - taker_fee(aNi) - capital_time_cost`.

This matters because a temperature event has many losing buckets.

Even if the winning YES book reprices instantly, some of the `K-1` losing-NO books may contain slower/staler liquidity.

The edge scanner should therefore search **all binary books**, not only the winner YES.

---

# 6. NegRisk conversion can recycle most losing-NO capital immediately

For a `K`-bucket exhaustive NegRisk event with known winner `w`, select every losing NO:

`S = {i : i != w}`

so `|S| = K-1`.

Polymarket's NegRisk Adapter identity gives, for one unit of every selected NO:

`selected losing NOs`

`-> lambda*(K-2) collateral + lambda*Y_w`

where:

`lambda = 1 - negRiskFeeBips/10_000`.

This is powerful because the initial capital is roughly `K-1` dollars per unit, but conversion returns roughly `K-2` dollars immediately. Only the fee-adjusted winning YES remains as delayed/market-risk capital if it is not immediately sold.

Official NegRisk Adapter docs:

https://github.com/Polymarket/neg-risk-ctf-adapter/blob/main/docs/NegRiskAdapter.md

---

# 7. Immediate conversion-and-liquidation inequality

For each losing NO `i`, let:

`cNi(x)` = depth-aware all-in cost/share to acquire size `x`, including Weather taker fee.

Let:

`bYw(x)` = executable bid for the winning YES at the resulting output size.

If selling the output YES as taker, define:

`net_bYw = bYw - 0.05*bYw*(1-bYw)`

before depth integration.

Then a one-unit approximation for the source-locked cycle is:

`cycle_proceeds = lambda*(K-2) + lambda*net_bYw`

`cycle_cost = sum_{i != w} cNi + conversion_gas`

and:

`cycle_edge = cycle_proceeds - cycle_cost`.

Trade only if the **depth-aware** cycle edge is positive at common size.

This can return essentially all capital immediately rather than waiting for CTF redemption.

---

# 8. Conversion contract availability is stronger than expected

Direct inspection of Polymarket's `NegRiskAdapter.sol` shows `convertPositions` checks:

- market prepared;
- question count > 1;
- valid index set;
- nonzero amount.

It does **not** check `marketData.determined()` before converting.

Source:

https://github.com/Polymarket/neg-risk-ctf-adapter/blob/main/src/NegRiskAdapter.sol

The function internally synthetically mints collateral and calls CTF splitting for complementary YES positions.

Gnosis ConditionalTokens' `splitPosition` also checks condition preparation and partition validity, but does **not** contain a payout-resolution-state rejection in the inspected implementation.

Source:

https://github.com/gnosis/conditional-tokens-contracts/blob/master/contracts/ConditionalTokens.sol

### Interpretation

At minimum, there is no obvious contract guard preventing conversion in the source-locked / pre-formal-resolution interval.

The source code appears to permit conversion even after conditions have been formally resolved, but this should be validated against the exact currently deployed Polymarket adapter and a resolved small-position call before relying on that stronger claim in execution logic.

For the intended source-lock edge, the important interval is **before** formal resolution, where conversion availability is strongly supported by the code path.

---

# 9. Why this can beat simply buying the winner YES

Buying winner YES uses only one book and one dollar/share of capital.

Buying losing NOs uses many books and more gross capital, but NegRisk conversion can release most of that capital immediately.

Potential economic advantages:

1. **more stale surfaces** — `K-1` losing-NO books versus one winner-YES book;
2. **aggregate capacity** — the sum of stale depth across losing buckets can exceed winner depth;
3. **fast capital recycle** — conversion returns `K-2` collateral immediately;
4. **tiny taker fees near 1** — unlike mid-price basket arbitrage;
5. **maker option** — a bot may already own losing NO inventory from pre-lock passive fills and convert as soon as the winner is fixed.

This is exactly the kind of structural daily edge that generic sports-market agents are less likely to model because it combines resolver semantics, weather source publication, multi-outcome token algebra and capital-time accounting.

---

# 10. Capital-time metric

Do not rank a 99.9¢ purchase only by raw cents/share.

Define realized annualization only for internal comparison, not as a stable expected-return claim:

`edge_rate = net_dollars / (capital_dollars * hours_locked)`.

More directly useful:

`net_dollars_per_1000_capital_hour = 1000 * net_dollars / (capital * hours_locked)`.

For routes that NegRisk-convert most collateral immediately, split capital-time into:

- acquisition-to-conversion exposure for the released `(K-2)` collateral;
- remaining winner-YES exposure until sale/redemption.

This avoids penalizing a high-turnover conversion route as if all gross notional were locked for the full UMA window.

---

# 11. The source watcher is more important than midnight

A naive implementation that wakes at 00:00 local is wrong.

For every active event, the engine should know:

`resolver_url`
`rule_text`
`lock_class`
`target_date_local`
`station/source timezone`
`last_source_state`
`first_following_date_datapoint_seen`
`finalized_flag / publication fingerprint`
`locked_max_or_min`
`t_lock_detected`
`winning_bucket`.

The source watcher emits:

`SOURCE_LOCK(event_id, winning_bucket, observed_value, source_hash, t_detected)`.

That should immediately trigger:

1. cancel stale maker quotes on losing directional sides;
2. value all YES/NO books at deterministic outcomes;
3. scan winner-YES and all loser-NO asks;
4. scan the losing-NO NegRisk conversion route;
5. offer near-$1 maker liquidity where expected fill is still favorable;
6. recycle preexisting winning inventory if better opportunities exist elsewhere.

---

# 12. This is also an execution-risk reduction layer for the forecast strategy

Even if no post-lock arbitrage is available, source lock has value.

Once the resolver outcome is fixed:

- all forecast uncertainty should be removed from the event;
- residual positions can be valued exactly;
- maker quotes based on pre-lock q are stale and should be canceled;
- losing positions should no longer be held because a forecast model still gives them tiny probability;
- collateral can be ranked against other live cities with exact opportunity cost.

This prevents the forecasting engine from contaminating a deterministic settlement state.

---

# 13. Best historical/live measurement

For each Weather event, record:

`target_date`
`source_url`
`lock_rule`
`source publication timestamps`
`t_lock`
`winning bucket`
`CLOB books at t_lock - 5m ... t_lock + resolution`
`winner YES ask/bid depth`
`all loser NO ask/bid depth`
`negRiskFeeBips`
`proposal timestamp`
`resolution timestamp`
`redemption availability`
`all fills after t_lock`.

Then calculate:

### Winner route

- stale edge at 1s / 5s / 30s / 5m after lock;
- profitable depth after fee;
- PnL if held to redemption;
- PnL if sold before resolution.

### Loser-NO route

- aggregate stale depth across `K-1` books;
- best single-NO holds;
- depth-aware NegRisk conversion cycle;
- capital released immediately;
- residual winning-YES exposure.

### Competition

- time until first price level reaches 99.9/100%;
- number and size of competing fills;
- whether lock-reaction latency is sub-second, seconds, or minutes by city/source.

This empirical reaction-time distribution determines whether direct taker execution or pre-positioned maker orders have the higher expected dollars.

---

# 14. Priority within the overall strategy

Current evidence suggests four complementary states:

## Pre-event / quiet

Forecast-aware passive maker around calibrated resolver probabilities.

## Fresh model or observation shock

Fee-paying directional taker only when `Delta q` clears spread + current taker fee + impact.

## Source-lock event

Deterministic terminal-value router:

- winner YES;
- losing NOs;
- NegRisk conversion;
- capital recycling.

## Extreme tails

Small cheap-tail acquisition when calibrated probability materially exceeds microprice.

The source-lock state is particularly attractive for research because it eliminates most meteorological-model uncertainty and converts the problem into latency, book depth and exact rules.

---

# Bottom line

The strongest new near-term hypothesis is:

> **Daily Weather markets may offer a recurring resolver-latency trade after the rule-defined source value is frozen but before the market completes UMA resolution. Near-$1 Weather taker fees are tiny, every losing NO creates another stale surface, and NegRisk conversion can recycle most losing-NO capital immediately.**

This is not yet quantified as profitable because recent historical synchronized L2 is unavailable from the official API. The correct next evidence is therefore the same high-value action identified by the broader research: **capture live Weather L2 and source publication timestamps continuously from now forward.**

That single dataset will reveal the actual dollar capacity of this edge within days of normal market operation.