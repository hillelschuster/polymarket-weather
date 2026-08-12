# Weather maker economics continuation — 2026-08-12

Purpose: continue the specialist reconstruction after the forecast-aware maker/merge correction, with emphasis on Weather-only profitability, incentive contribution, and the next decisive measurements.

## 1. Weather-only leaderboard economics

Polymarket's indexed all-time Weather leaderboards provide category-specific profit and volume snapshots.

### ColdMath

- Weather profit: approximately **$136,377** (#3)
- Weather volume: approximately **$10,941,892** (#7)
- implied Weather profit / turnover: **~124.6 bps**

### Poligarch

- Weather profit: approximately **$84,711** (#6)
- Weather volume: approximately **$13,856,096** (#3)
- implied Weather profit / turnover: **~61.1 bps**

Sources:

- https://polymarket.com/leaderboard/weather/all/profit
- https://polymarket.com/leaderboard/weather/all/volume

These ratios are not audited realized return-on-capital. Volume is turnover and leaderboard PnL may include Polymarket's own accounting conventions. The important observation is narrower: **two of the largest Weather-volume accounts are simultaneously among the largest Weather-profit accounts.** This supports a repeatable high-turnover microstructure edge rather than a few isolated directional bets.

## 2. Incentives do not explain Poligarch's full economics

Struct's indexed Poligarch snapshot around July 21 showed approximately:

- cumulative all-category PnL: **$204K**
- all-category volume: **$21.2M**
- rebates: **$18.7K**
- liquidity rewards: **$5.42K**
- buys: **1.34M+**
- sells: **~1.26K**
- very small average trade size in the inspected active period (~$6)

Source:

https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

Relative to the indexed lifetime turnover snapshot:

- cumulative PnL ~= **96 bps** of volume;
- rebates ~= **8.8 bps** of volume;
- rewards ~= **2.6 bps** of volume.

This does **not** prove the residual 84+ bps is spread capture; PnL can include directional inventory and mark-to-market effects. But it does show that rebates/rewards alone are much too small to explain the indexed profitability.

Current Polymarket fee documentation independently confirms:

- Weather taker rate: **0.05**;
- maker rate: **0**;
- Weather maker rebate pool: **25%** of eligible taker fees.

Source:

https://help.polymarket.com/en/articles/13364478-trading-fees

Therefore maker-first execution has a structural cost advantage even before forecast skill is considered.

## 3. Cross-wallet evidence of microstructure specialization

ColdMath's Struct snapshot showed approximately:

- total volume: **$13.6M**;
- buys: **216,527**;
- sells: **1,287**;
- cumulative PnL: **$132K**;
- Weather leaderboard profit: ~**$136K**.

Source:

https://explorer.struct.to/traders/0x594edb9112f526fa6a80b8f858a6379c8a2c1c11

ColdMath's highlighted Weather wins include many markets with hundreds or thousands of tiny fills. Struct also assigns large merge values to several of those rows, but the earlier transaction audit showed raw merge counts can reflect exchange settlement mechanics. So the reliable conclusion is **high-frequency passive/inventory-heavy activity**, not "ColdMath manually merges every pair."

The coincidence that both ColdMath and Poligarch are huge Weather-volume traders and huge Weather-profit traders raises the priority of maker-fill markout research.

## 4. On-chain target-wallet / Poligarch interaction is stronger than previously summarized

Transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

PolygonScan indexed multiple `OrderFilled` logs where:

- supplied wallet `0xbddc...5d4f` is the **taker**;
- Poligarch `0xb40e...7cc9` appears as a matched **maker** on the same neg-risk token flow;
- the maker logs show **fee = 0**;
- other makers supplied the same token at different cash/token ratios in the same aggregate taker transaction.

Source:

https://polygonscan.com/tx/0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597

This directly connects two distinct profitable archetypes:

1. a directional wallet willing to cross/pay Weather fees when it wants immediate exposure;
2. a high-turnover specialist supplying passive zero-fee liquidity into that flow.

That suggests a natural production router rather than choosing one archetype exclusively:

- **quiet state:** make around fair value;
- **fresh forecast/observation shock:** cancel stale maker inventory, then cross only the depth that remains materially positive EV after taker fee/impact.

## 5. Current exact maker math

For bucket fair YES probability `q`, choose passive buy margins `mY,mN`:

`bid_yes = q - mY`

`bid_no = 1 - q - mN`

If equal quantities eventually fill on both sides and are available as complementary inventory, complete-set value is `$1`, so gross paired value is:

`mY + mN`

per matched share before any inventory carrying cost and execution transformations.

The actual money-critical object for one-sided maker fills is:

`EV_filled_yes = q_after_fill - fill_price + expected_rebate - adverse_selection`

and symmetrically for NO.

The decisive empirical statistic is therefore **fill-conditioned markout**, not posted spread.

For each maker fill collect:

- fair `q` immediately before fill;
- fair `q` after next weather-data update;
- market midpoint/ask/bid at 10s, 1m, 5m, 30m;
- whether the fill came just before a forecast/observation shock;
- maker rebate allocation;
- residual inventory duration.

## 6. `feeBips` remains unresolved and should not be guessed

The NegRisk Adapter exposes a market-specific conversion fee (`feeBips`). The existing negative-risk research derived exact subset-conversion inequalities conditional on that value.

I still do **not** have a verified daily-Weather `negRiskMarketID -> getFeeBips()` result. Search-indexed Polymarket pages expose event/market slugs and rules but not enough on-chain market metadata to safely derive the adapter key in this environment.

Therefore:

- do not classify sub-percent NO-subset discrepancies as executable yet;
- do not assume zero conversion fee;
- the live collector should resolve `negRiskMarketID` from Gamma/event metadata and call `getFeeBips(bytes32)` directly.

This is a single integer lookup per event and should be treated as mandatory market metadata, not a research abstraction.

## 7. A negative control: generic market making is not sufficient

Struct profile `weather-smart` shows approximately:

- volume: **$43.7K**;
- rebates: **$105**;
- rewards: **$7.78**;
- cumulative PnL: only **+$21.7**;
- profit factor: **1.08x**.

Source:

https://explorer.struct.to/traders/0xd610011479209c9c970a35168b30f61f2250b3e4

This is useful because it argues against the trivial thesis "maker rebates = easy money." A small, active weather trader can collect meaningful rebates and still have nearly zero economic PnL.

The edge must therefore come from some combination of:

- better fair-value centering;
- better quote withdrawal around information shocks;
- superior inventory selection;
- wider realized spread / better queue positioning;
- city/source specialization;
- structural neg-risk routes.

That strengthens, rather than weakens, the value of the weather probability engine.

## 8. Highest-value next experiment

The next production-fidelity experiment should be deliberately small:

### One event, one major maker wallet

Choose one resolved daily-temperature event with heavy Poligarch or ColdMath activity.

Recover every fill in chronological order and create:

`timestamp, token, YES/NO, maker/taker, price, shares, fee, q_before, q_after, 1m_markout, 30m_markout, final_outcome`

Then compute:

1. zero-fee maker share of volume;
2. average and median 1m/30m adverse markout;
3. realized spread conditional on both sides filling;
4. PnL of unmatched inventory marked to settlement;
5. rebate contribution;
6. net cents/share and net bps/turnover;
7. markout conditional on proximity to ECMWF/local-model/METAR updates.

### Decision criterion

If forecast-aware filtering improves maker fill PnL by even **20–40 bps of turnover** at Poligarch/ColdMath-like volume, it is economically important. Their observed Weather turnover is multi-million dollars, so small execution improvements scale into large dollars.

## Bottom line

The research priority has shifted materially.

The strongest currently supported architecture is not a pure forecasting bettor and not a blind market maker. It is:

> **one coherent resolver probability engine feeding a state-dependent execution router: passive maker-first in quiet states, immediate taker only after sufficiently large information shocks, with negative-risk transformations scanned deterministically whenever market-specific conversion costs permit.**

The next dollar-relevant evidence is maker fill markout, not more generic weather-model enumeration.