# Audit: “Four Strategies, 562 Trades, Zero Edge”

Snapshot: **2026-08-11**

Paper:

**Andreas Wenth, “Four Strategies, 562 Trades, Zero Edge: A Forensic Autopsy of Algorithmic Weather Betting” (2026).**

SSRN:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6496661

DOI:
https://doi.org/10.2139/ssrn.6496661

This is the most directly relevant negative empirical study found so far, because it reports hundreds of live Polymarket weather trades rather than theoretical objections.

The live losses are real evidence about **those implementations**. Several of the paper's broader impossibility conclusions do not follow from its own data and should not deter the resolver-first probability strategy being researched here.

---

# 1. What the paper actually tested

Reported live strategies:

| Strategy | Live trades | Reported PnL |
|---|---:|---:|
| v4 — 82-model ensemble + Student-t | 38 | -$102 |
| v6 — smart-wallet copy, diversified NO | 206 | -$134 |
| v7 — elite-wallet copy, YES | 35 | -$118 |
| v8 — 3+ wallet convergence | 230 | -$48 |
| **Total** | **509** | **-$401** |

The reported starting balance was $372 and position sizes were generally only a few to tens of dollars.

Paper configurations also produced positive simulated results, including an elite hold-to-resolution configuration with 79.7% reported win rate.

The negative live PnL is worth respecting as evidence that:

- naive ensemble-to-bucket execution can fail;
- delayed wallet copying can fail;
- simplistic wallet convergence can fail;
- live execution can diverge badly from paper assumptions.

It does **not** establish that calibrated resolver probabilities cannot beat executable weather prices.

---

# 2. The “information-theoretic limit” is not an information-theoretic limit

The paper's main claim is:

- point forecast MAE ≈ **2.03°F / 1.3°C**;
- common bucket width ≈ **2°F / 1°C**;
- therefore no probabilistic forecast edge can exist regardless of ensemble size.

The forecast-error sample behind this claim contains only **14 v4 trades with forecast data**.

That conclusion does not follow mathematically.

## Point MAE is not bucket probability calibration

A point forecast error statistic measures:

`E[|H_hat - H|]`

The trading problem requires:

`q_i = P(H lands in bucket i | information)`.

A distribution can have point MAE near one bucket width and still assign materially better probabilities than the market.

Example:

- executable market asks 20¢ for a bucket;
- calibrated weather distribution says 35%;
- the modal point forecast can still miss that exact bucket frequently;
- the trade nevertheless has positive expected value if the 35% probability is calibrated.

Classification hit rate and probability edge are different objects.

## Relative accuracy matters

Even poor absolute forecasting can be profitable if the market is worse in a systematic subset.

The relevant statistic is not:

`weather MAE < bucket width`.

It is:

`E[outcome - executable_price | signal] > costs`.

The paper does not show that this quantity is non-positive for a resolver-calibrated forecast model.

## Tiny sample for the strongest claim

Fourteen forecast observations are not enough to establish a universal error floor across:

- stations;
- seasons;
- horizons;
- T+0 versus T+1;
- stable versus frontal regimes;
- local national models;
- resolver-specific bias correction.

The claim is therefore best interpreted as:

> **their v4 point forecast was too inaccurate for the way they converted it into trades.**

That is useful; it is not a theorem about the opportunity set.

---

# 3. Their forecast target was mismatched to the resolver

This is the most important section of the paper for our project.

The authors report a **resolution-source mismatch**:

- system calibration used NWS official forecasts;
- Polymarket resolved on Weather Underground station observations;
- the sources differed by roughly **1–3°F for the same city/date**;
- at 2°F bucket widths this could flip the winning bucket.

The paper also reports a software defect, described as a **“phantom edge bug,”** that inflated NO-side edge signals during v4.

These facts weaken the claim that v4 measured the true forecastability of Polymarket's settlement target.

A model can only be evaluated as a Polymarket forecasting model if its target is:

> **the exact resolver station/source value under the exact settlement convention.**

That is precisely why this repository treats the station/source/rounding/day window as part of the prediction target rather than plumbing.

---

# 4. The ensemble construction did not solve resolver calibration

The v4 strategy is described as an **82-model ensemble with Student-t probability mapping**.

A large ensemble count does not automatically produce calibrated settlement probabilities.

The money-relevant questions are:

- were daily maxima calculated per path/member at the resolver station?
- were errors calibrated against that station's historical resolver values?
- were model families weighted for correlated error?
- was lead-time-specific bias learned?
- was current T+0 observation state incorporated?
- were local high-resolution models used where they add skill?

The reported resolver mismatch shows at least one of these core calibration layers was wrong.

More models cannot repair a wrong target.

---

# 5. v6-v8 mostly test naive copy trading, not weather alpha

After v4, the paper largely abandoned weather modeling:

- v6 copied “smart wallets” with diversified NO positions;
- v7 copied elite wallets, YES only;
- v8 required 3+ independent wallet signals.

Their failure is evidence against **unconditioned delayed copying**, not against using wallet flow as an incremental feature.

A wallet trade only has value to us if we know:

- fill timestamp;
- fill price;
- current market price when we can react;
- how much the market already moved;
- wallet's segment/city skill;
- normalized conviction size;
- whether it is entering or exiting;
- latest weather information event.

The paper itself states that it lacked block-level timing analysis for determining why elite wallets were successful.

Our Milan June 25 micro-case already shows why vote-count convergence can be inferior: the supplied wallet sold a losing 33°C bucket while other recognized specialists were still making small YES buys around the same price regime.

Direction, size, freshness and entry-versus-exit state all matter.

---

# 6. The “profit-lock paradox” is not a universal exit rule

The paper argues that intermediate exits necessarily destroy value in binary markets.

Its example:

- buy at 20¢;
- winner ultimately pays $1;
- selling at 30¢ captures only 10¢ instead of 80¢ potential profit;
- downside remains 20¢ if wrong.

That only demonstrates that a **mechanical profit target without new information** can destroy a positive-EV position.

The correct exit problem is conditional on the updated posterior.

Suppose:

- bought at 20¢;
- market bid is now 30¢;
- fresh weather information changes fair probability to 10%.

Holding has value ≈ 10¢.

Selling at 30¢ has value near 30¢ before fee.

Exiting is clearly superior.

General rule:

`hold_value = q_new`

`exit_value = executable_net_bid + redeployment_value`

Sell when:

`exit_value > hold_value`.

This is ordinary Bayesian revaluation, not a stop-loss heuristic.

The supplied wallet provides two empirical examples that contradict the universal hold-to-resolution claim:

1. Milan June 25 33°C — sold/reduced 193.78 YES around 10.9¢; that bucket ultimately lost and 35°C won.
2. Mexico City July 16 25°C — sold the effectively locked winning bucket around 99.9¢ five minutes after local midnight, releasing capital rather than waiting for formal settlement.

An adaptive exit can therefore increase expected compounded dollars.

---

# 7. The paper's elite-wallet evidence actually supports further research

The on-chain study reports:

- 37,562 wallets observed;
- 276 “elite” wallets;
- elite win rates reported around 96.4–97.8%.

The authors hypothesize that this probably reflects Weather Underground resolution-source latency rather than superior forecasting.

But their limitations explicitly state they lacked block-level timing and **could not definitively distinguish latency arbitrage from superior forecasting**.

This is important.

The existence of a small persistently successful cohort is evidence that weather markets are not uniformly efficient.

The profitable question is simply to identify the mechanism:

- resolver publication latency;
- model-release latency;
- superior probabilistic forecasting;
- full-ladder relative value;
- maker economics;
- combinations of the above.

Our supplied wallet's verified T+1 Milan purchase proves at least that some active specialist behavior occurs well before resolver certainty and cannot be explained solely as post-observation resolution arbitrage.

That single transaction does not prove the wallet's T+1 strategy is profitable, but it makes “all elite edge is resolver latency” an unjustified assumption.

---

# 8. Live versus paper gap — the useful lesson

The paper reports:

- live: -$401;
- paper: +$172;
- large divergence in win rate and PnL.

The economically useful inference is not “discount all backtests by a fixed percentage.”

It is:

> **Historical research must reproduce the actual information and executable price available at the decision timestamp.**

For this project that means:

- point-in-time forecast vintage;
- exact resolver target;
- actual wallet/market fill price;
- fee schedule;
- live or historically observed spread where available;
- no future station observations;
- no current revised forecast substituted for an old forecast.

A fixed 40–60% “backtest discount” has no economic foundation. Model the actual costs instead.

---

# 9. What should be retained from the paper

Several observations are directly useful.

## Keep: target mismatch can destroy bucket strategies

Correct. A 1–3°F difference is enormous on 1°C/2°F contracts.

## Keep: naive copy trading loses edge after public fills

Plausible and supported by their live losses. Wallet flow must be tested for incremental markout, not blindly followed.

## Keep: many small NO bets can have bad payoff asymmetry

Correct. Win rate is not profitability. Every expression should be valued by expected dollars.

## Keep: live evidence dominates paper evidence

Correct. Actual fills/PnL are the highest-grade evidence.

## Keep: successful wallets may exploit information timing

Very plausible. Their exact mechanism was not measured.

## Reject: MAE ≈ bucket width implies no probability edge

Does not follow.

## Reject: all early exits are structurally harmful

False when posterior probabilities or opportunity costs change.

## Reject: public weather information is necessarily unprofitable

Not established by the study because its forecasting target was mismatched and the forecast sample underlying the impossibility claim was only 14 observations.

---

# 10. Research consequence

This paper actually narrows the strategy in a productive way.

Do **not** reproduce:

- generic city forecast → bucket;
- uncalibrated large model count;
- NWS/city forecast versus different resolver station;
- simple wallet vote counting;
- fixed profit targets;
- win-rate optimization.

Continue focusing on:

1. exact resolver distribution;
2. station/horizon calibration;
3. T+0 observed-state conditioning;
4. T+1 forecast revision timing;
5. executable fee-adjusted EV;
6. wallet markout conditioned on freshness/size/entry-vs-exit;
7. adaptive posterior exits;
8. dollar PnL rather than hit rate.

The paper's live failures make those distinctions more valuable, not less.

---

# Bottom line

The strongest negative weather-bot study found so far does **not** invalidate the project's core thesis.

Its own evidence shows:

- it forecast/calibrated a different object from the resolver;
- v4 had a signal bug;
- the headline forecast impossibility claim rests on 14 observations;
- later strategies mostly tested naive wallet copying rather than resolver forecasting;
- elite profitable wallets clearly existed;
- the paper could not determine what information those wallets exploited.

The correct economic lesson is narrower:

> **A generic forecast, wrong target, naive copying and static exits are insufficient. The profitable object remains a point-in-time calibrated probability distribution for the exact resolver, traded only when its executable value differs materially from price.**
