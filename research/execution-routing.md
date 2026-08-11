# Execution routing — when paying the taker fee is worth it

Snapshot: **2026-08-11**

Purpose: decide whether a positive-EV weather signal should cross immediately or rest passively, using one economic comparison rather than an execution framework.

Current Polymarket Weather economics:

- taker fee rate: **0.05**;
- maker fee: **0**;
- maker rebate allocation: **25%** of the fee pool for Weather markets;
- fee formula: `shares × 0.05 × p × (1-p)`;
- actual fee applicability remains per-market via `feesEnabled`.

Official docs:

https://docs.polymarket.com/trading/fees
https://docs.polymarket.com/market-makers/maker-rebates

The key decision is:

> **Is the fee/spread saving from waiting larger than the expected alpha lost while waiting for a fill?**

---

# 1. Taker EV

For YES fair value `q` and executable ask `a`:

`fee(a) = 0.05*a*(1-a)`

`taker_EV = q - a - fee(a)`

This is per share and assumes the desired size is available at `a`. For larger size, replace `a` with the actual book-walk cost by level.

---

# 2. Maker EV

Suppose a passive BUY rests at price `b`.

Let:

- `F` = probability it fills while the signal is still worth trading;
- `D` = expected fair-value decay/adverse-selection loss by the time it fills;
- `R` = expected maker rebate per filled share.

Then:

`maker_conditional_EV = q - D - b + R`

and opportunity-level expected value is:

`maker_EV = F * maker_conditional_EV`.

The maker route is better when:

`F * (q - D - b + R) > q - a - fee(a)`.

Break-even fill probability:

`F* = taker_EV / maker_conditional_EV`.

This is enough for the routing decision.

---

# 3. Example: 50¢ ask / 48¢ maker bid

Weather taker fee at 50¢ is **1.25¢/share**.

## Fair value 55% — 5 point edge over ask

Immediate taker:

`taker_EV = 55 - 50 - 1.25 = 3.75¢`.

Passive at 48¢:

### No decay/adverse selection

`maker_conditional_EV = 55 - 48 = 7¢`.

Break-even fill probability:

`F* = 3.75 / 7 = 53.6%`.

### 1 point expected decay before fill

`maker_conditional_EV = 55 - 1 - 48 = 6¢`.

`F* = 62.5%`.

### 2 point expected decay

`maker_conditional_EV = 5¢`.

`F* = 75.0%`.

So even a modest 5-point edge should be crossed if a passive order is unlikely to fill quickly enough.

---

# 4. Stronger signal makes waiting harder to justify

Same 50¢ ask / 48¢ bid.

## Fair value 60% — 10 point edge

Taker EV:

`60 - 50 - 1.25 = 8.75¢`.

Passive break-even fill probability:

| Expected value decay before fill | Break-even maker fill probability |
|---:|---:|
| 0 pp | 72.9% |
| 1 pp | 79.5% |
| 2 pp | 87.5% |

## Fair value 65% — 15 point edge

| Decay | Break-even maker fill probability |
|---:|---:|
| 0 pp | 80.9% |
| 1 pp | 85.9% |
| 2 pp | 91.7% |

This is the useful non-obvious result:

> **A large information edge raises the opportunity cost of waiting.**

Saving a 1.25¢ taker fee is not attractive if waiting risks missing an 8–14¢ immediate EV opportunity.

This matches the supplied wallet's recovered behavior: it sometimes pays the middle-of-the-curve Weather taker fee to acquire 26–30¢ exact-bucket positions immediately.

---

# 5. 30¢ market example

Suppose:

- ask = 30¢;
- maker quote = 29¢;
- Weather fee = 1.05¢.

## Fair value 35% — 5 point edge

Taker EV:

`35 - 30 - 1.05 = 3.95¢`.

Maker break-even fill probability:

| Decay | F* |
|---:|---:|
| 0 pp | 65.8% |
| 1 pp | 79.0% |
| 2 pp | 98.8% |

## Fair value 40% — 10 point edge

| Decay | F* |
|---:|---:|
| 0 pp | 81.4% |
| 1 pp | 89.5% |
| 2 pp | 99.4% |

A 30¢ exact bucket can have excellent percentage return, but the same feature makes stale waiting expensive: if a fresh forecast revision says the contract is worth 40¢, losing the trade while trying to save 1–2¢ is poor economics.

---

# 6. 70¢ market is symmetric in fee shape

At 70¢, fee/share is again 1.05¢.

With a 69¢ passive bid:

- +5 point fair edge needs ~65.8% maker fill probability with no decay;
- +10 point fair edge needs ~81.4%;
- one point of decay pushes those thresholds toward ~79% and ~89.5%.

Thus the core routing result is driven mainly by:

- size of fair-value edge;
- spread captured by the passive quote;
- fee saved;
- probability/time of passive fill;
- how quickly the information advantage decays.

---

# 7. Rebate is secondary to fee saving and spread

Makers can receive Weather rebates from the daily pool, but the exact rebate per fill depends on the maker's share of fee-equivalent liquidity in that market.

Therefore do not hard-code the full 25% market allocation as a guaranteed per-trade rebate.

Use measured realized rebate history once available:

`R = expected_rebate_per_filled_share`.

Initially, setting `R=0` is a clean baseline. If passive trading is profitable without rebates, actual rebates improve it. If it only appears profitable because an optimistic rebate assumption is inserted, the edge is weak.

---

# 8. Information half-life is the real router

Classify signals by how fast fair value is expected to converge into market price.

## Fast signals — usually taker candidates

Examples:

- new local-model run causes a large exact-bucket revision;
- new METAR/SPECI moves the running maximum close to or across a resolver boundary;
- cloud/radar/sea-breeze event sharply changes remaining heating probability;
- specialist flow reveals a large fresh information trade before repricing.

If market repricing historically happens in minutes, passive fill probability before edge decay may be low.

## Slow signals — maker candidates

Examples:

- stable T+1 residual-calibration edge;
- market calibration prior not tied to a fresh release;
- cross-ladder relative value that persists for tens of minutes/hours;
- price is temporarily wide but the underlying weather state is unchanged.

Here the fee + spread saving can dominate urgency.

---

# 9. Minimal empirical router

No execution model is required initially.

From historical/live data, estimate by signal class:

`F(τ) = probability passive quote fills within τ`

and

`D(τ) = average fair-value / market markout decay by τ`.

Then compare a few candidate waiting windows such as:

- immediate taker;
- maker for 30 seconds;
- maker for 2 minutes;
- maker for 5 minutes.

For each:

`expected_EV(τ) = F(τ)*(q-D(τ)-quote+R) + fallback_value_if_unfilled`.

The fallback can be simple:

- cross after timeout if edge remains positive;
- cancel if edge has vanished.

The best timeout is whichever produces the most net dollars in replay/live evidence.

---

# 10. Book depth can be handled directly

Polymarket's public CLOB exposes full visible bids/asks and can calculate market-order fill price from depth.

Official docs:

https://docs.polymarket.com/trading/orderbook

For candidate notional `N`:

1. walk actual asks for taker route;
2. compute fee at each execution price;
3. stop adding size once marginal fill cost exceeds fair probability;
4. compare with passive expected value at available bid/quote levels.

This is more accurate and simpler than fitting a generic slippage formula.

---

# 11. What the supplied wallet currently suggests

Recovered fee-paying BUYs show the supplied wallet is willing to take immediate liquidity around intermediate prices where Weather fees are near their maximum.

That is compatible with one of two things:

1. its edge is large enough that saving 1–2¢ through passive execution is less important than securing the position;
2. its edge decays quickly after the information event.

The model-release timing of the recovered Milan T+1 BUY — about 1h43m after the relevant ECMWF 18Z early-step dissemination completed — makes both explanations plausible.

The correct next measurement is wallet fill markout versus time since forecast release, not speculation about whether it is “a taker strategy.”

---

# 12. Minimal eventual rule

For a candidate BUY:

1. compute immediate taker EV from actual book depth and fees;
2. compute passive conditional EV at best bid / chosen quote;
3. use measured fill probability and edge decay for that signal class;
4. choose the higher expected dollar route.

A compact equivalent:

> **Cross when the expected alpha lost while waiting exceeds the fee + spread/rebate benefit of making.**

This is the only routing principle required until empirical fills justify something more complex.