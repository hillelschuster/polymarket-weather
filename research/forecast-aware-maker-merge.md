# Forecast-aware market making — corrected merge interpretation

Snapshot: **2026-08-11**

Purpose: identify the smallest structural execution edge that can monetize a weather probability engine, while separating **directly observed trader behavior** from **exchange-internal settlement mechanics**.

## Corrected verdict

The strongest structural evidence is still **forecast-aware passive market making**, but an earlier interpretation was too strong.

### What remains supported

`Poligarch` is directly proven to provide **zero-fee maker liquidity** in daily Weather markets. It has enormous buy activity, very few direct sells, simultaneous YES/NO inventory in the same binaries, material maker rebates, and substantial Weather leaderboard profit/volume.

A coherent weather probability `q` gives a natural two-sided quote surface:

`YES bid = q - mY`

`NO bid  = 1 - q - mN`

If both bids eventually fill for the same quantity, combined cash cost is:

`1 - mY - mN`

and the complete YES/NO set can be merged to `$1 pUSD`.

Therefore deliberate paired inventory can mechanically capture:

`mY + mN`

before rebates/rewards/operational costs.

### What is **not** yet proven

Struct's displayed trader `Merges` count is **not sufficient evidence that the trader manually paired inventory and called merge later**.

Polymarket's exchange contract itself has matching paths that mint or merge complete sets during order settlement. In a directly inspected Poligarch transaction, a `PositionsMerge` occurs inside the same neg-risk exchange transaction in which Poligarch supplies maker liquidity. That merge can therefore be exchange settlement plumbing rather than a discretionary post-fill action by Poligarch.

The corrected thesis is:

> **Use a calibrated weather distribution to provide passive two-sided liquidity and control adverse selection. Treat manual pair-and-merge recycling as a valid strategy primitive, but do not attribute it to Poligarch/ColdMath until trader-specific token and cashflow reconstruction proves it.**

---

# 1. Direct Weather maker proof

Poligarch wallet:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

Transaction:

`0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213`

PolygonScan:

https://polygonscan.com/tx/0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213

Timestamp:

`2026-07-21 01:56:10 UTC`

Daily Weather event:

**Wellington July 21 — 11°C**.

Relevant `OrderFilled` log:

- `maker = 0xB40e89677d59665d5188541aD860450A6e2a7cc9`;
- Poligarch contributes `9.400590 pUSD`;
- receives `9.990000` related outcome tokens;
- `fee = 0`.

Effective acquisition price:

`9.400590 / 9.990000 = 94.1¢`.

This directly proves:

1. passive Weather maker activity;
2. zero maker platform fee on the fill;
3. inventory acquisition inside a neg-risk temperature match.

It does **not** by itself prove later manual merge or the exact economic direction of the neg-risk token without full token mapping.

---

# 2. Poligarch aggregate shape still matters — but interpret it correctly

Struct indexed approximately:

- cumulative PnL: **$207K**;
- volume: **$24.5M**;
- fees: **$2.29K**;
- buys: **1,612,158**;
- sells: **1,287**;
- redemptions: **40,882**;
- merges: **67,647**;
- splits: **0**;
- converts: **2**;
- rebates: **$19.3K**;
- liquidity rewards: **$5.52K**.

Source:

https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

The buy/sell operation ratio is roughly **1,253:1**.

That is strong evidence that a conventional `buy -> later sell` lifecycle is not the dominant visible activity.

However, the `67,647 merges` figure must now be treated as **ambiguous attribution** until Struct's event-accounting semantics are established at transaction level.

It can contain or reflect exchange-internal transformation paths, not only user-initiated merge operations.

Do not use `merge count / sell count` as proof of capital-recycling behavior.

---

# 3. Why the merge-count correction is necessary

Direct transaction:

`0xee8fd0c9e0de9ceb8f42a615188dba0d40aa17f939075fc523fdcb63fcc0b716`

PolygonScan:

https://polygonscan.com/tx/0xee8fd0c9e0de9ceb8f42a615188dba0d40aa17f939075fc523fdcb63fcc0b716

Timestamp:

`2026-05-10 13:17:36 UTC`.

In this single Neg Risk CTF Exchange transaction:

- Poligarch transfers pUSD into the exchange in multiple maker fills;
- the transaction also contains a `PositionsMerge` path releasing **33.46** collateral;
- the merge is executed through the exchange/adapter settlement path, not shown as a standalone Poligarch wallet call.

This is exactly the failure mode that makes raw `Merges` counts unsafe as trader-behavior evidence.

Polymarket's own exchange source describes three matching paths:

- complementary BUY vs SELL: direct transfer;
- two BUY orders: `MINT` complete sets;
- two SELL orders: `MERGE` complete sets.

Official source:

https://github.com/Polymarket/ctf-exchange-v2

Legacy exchange overview with matching scenarios:

https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md

Therefore a `PositionsMerge` event can be part of **order matching itself**.

---

# 4. Manual merge remains a valid economic primitive

The correction above changes attribution, not the CTF identity.

Official Polymarket mechanics remain:

`1 YES + 1 NO -> $1 pUSD`.

Sources:

https://docs.polymarket.com/trading/ctf/merge

https://docs.polymarket.com/concepts/positions-tokens

Polymarket's market-maker inventory guide explicitly describes merging equal YES/NO inventory to free collateral:

https://docs.polymarket.com/market-makers/inventory

For paired quantities `m` acquired at prices `bY` and `bN`:

`pair_cost = m * (bY + bN)`

`merge_value = m`

`gross_pair_capture = m * (1 - bY - bN)`.

If:

`bY + bN < 1`

then a completed pair has positive mechanical value independent of weather resolution.

But whether **these specialists deliberately exploit this post-fill** remains an empirical question.

---

# 5. The cleanest maker formulation comes directly from fair probability

For one binary bucket, let calibrated resolver probability be `q`.

Then:

`fair YES = q`

`fair NO = 1 - q`.

Choose maker margins `mY > 0`, `mN > 0`:

`bid_yes = q - mY`

`bid_no  = 1 - q - mN`.

If both sides fill equally:

`bid_yes + bid_no = 1 - mY - mN`.

The complete set is worth exactly `$1`, so the raw pair capture is:

`mY + mN` per paired share.

This is important because it shows that **the weather model and the pair economics are the same object**:

- `q` determines where each side is actually cheap;
- `mY,mN` are the compensation demanded for fill-conditioned adverse selection, queue risk, uncertainty and capital-time;
- if both sides fill, the two margins become mechanical pair capture;
- if only one side fills, the forecast distribution determines whether the residual inventory is good or toxic.

That is the simplest professional formulation of a forecast-aware maker.

---

# 6. Maker rebates materially reduce the required gross edge

Current Weather fee structure from Polymarket documentation:

- taker fee rate: **0.05**;
- maker fee rate: **0**;
- Weather maker rebate allocation: **25%** of eligible taker fees.

Fee curve:

`fee = shares * 0.05 * p * (1-p)`.

Official sources:

https://docs.polymarket.com/trading/fees

https://docs.polymarket.com/market-makers/maker-rebates

Approximate taker fee/share before rounding:

- at 50¢: **1.25¢**;
- at 30¢/70¢: **1.05¢**;
- at 10¢/90¢: **0.45¢**.

Maker rebate allocation is competition-dependent:

`rebate = own_fee_equivalent / total_market_fee_equivalent * rebate_pool`.

Do not assume every maker receives 25% of the fee-equivalent generated by its own fill.

For strategy selection, rebates should be measured empirically and added **after** the core maker economics, not used to rescue a structurally losing quote.

---

# 7. Liquidity rewards are currently an overlay, not the Weather thesis

Polymarket also supports market-specific liquidity rewards.

Official docs:

https://docs.polymarket.com/market-makers/liquidity-rewards

https://docs.polymarket.com/api-reference/rewards/get-current-active-rewards-configurations

Struct's indexed active-rewards page inspected in this research showed 25 active reward markets and **no Weather market** among them.

Source:

https://explorer.struct.to/rewards

This is a point-in-time observation, not a permanent rule.

Production logic should query current reward configuration per market and assign zero expected LP reward unless the contract is actually eligible.

---

# 8. Same-market YES + NO inventory remains useful evidence

Struct showed Poligarch simultaneously carrying YES and NO residual inventory in the same Weather binaries, including examples in New York City, Houston, Toronto and London.

That is consistent with continuous two-sided quoting and incomplete inventory matching.

It is **not** enough to calculate pair PnL from displayed average entry prices because:

- YES/NO quantities differ;
- average prices combine fills from different times;
- earlier transformations may already have removed matched inventory;
- current balances are residual state, not the chronological ledger.

The correct measurement is lot-level cashflow reconstruction.

---

# 9. ColdMath remains independent evidence of non-directional microstructure, but not proof of manual merge

ColdMath wallet:

`0x594edb9112f526fa6a80b8f858a6379c8a2c1c11`

Struct indexed approximately:

- volume: **$14M**;
- buys: **224,892**;
- sells: **1,306**;
- merges: **6,790**;
- cumulative PnL: **$132K**.

Polymarket's indexed all-time Weather leaderboard placed ColdMath around **#3 by Weather profit** and among the largest Weather-volume accounts.

This supports the broader conclusion that very profitable Weather activity can have a highly nonstandard buy/sell lifecycle.

But the same merge-attribution caveat applies: **do not call ColdMath a manual merge strategy until its token/cashflow path is reconstructed.**

---

# 10. Corrected highest-value experiment

The original experiment was:

> reconstruct complementary fills and later merge.

It now needs one extra classification layer.

For one Poligarch or ColdMath Weather binary, recover every relevant transaction and classify each transformation as:

### A. Exchange settlement transformation

Transaction is an order-matching call to the CTF / Neg Risk CTF Exchange and the mint/merge occurs internally as part of matching.

### B. Trader-initiated inventory transformation

The trader/proxy/relayer initiates a dedicated CTF/adapter split, merge, redeem or conversion outside an order-match settlement.

For each fill/operation collect:

`timestamp`
`tx_hash`
`order_hash`
`condition_id`
`token_id`
`YES/NO`
`BUY/SELL`
`maker/taker`
`price`
`shares`
`fee`
`pUSD wallet delta`
`token wallet delta`
`internal MINT/MERGE path`
`dedicated merge/split/convert call`
`rebate`
`reward`.

Then calculate trader-level economics from wallet deltas, not explorer labels.

Decisive questions:

1. What fraction of Weather volume is zero-fee maker?
2. What is the 5m / 30m / 2h markout of maker fills?
3. How often does the trader end up with both complementary balances?
4. Are those balances deliberately merged later, or does the exchange transformation explain most `merge` events?
5. What is realized spread / pair capture before rebates?
6. How long is unpaired inventory held?
7. How strongly do forecast revisions predict adverse selection?
8. What is net PnL per dollar-hour of inventory and per $1M maker turnover?

---

# 11. Synthesis with the supplied directional wallet

The supplied wallet gives a different execution archetype.

Recovered purchases show it explicitly submitting **fee-paying taker orders** when it wants immediate Weather exposure.

That implies a state-dependent router:

## Quiet information state

Use maker quotes around calibrated `q`:

- maker fee = zero;
- collect spread/margin;
- possible rebate;
- manage unpaired inventory with q;
- deliberately merge complete sets if and only if doing so improves capital efficiency.

## Fresh information shock

Cancel stale quotes first.

Cross only when:

`q_new - executable_price - taker_fee - impact > required_margin`.

The target wallet's recovered Milan and Jul 12 purchases show that a specialist is willing to pay roughly **~1¢/share** Weather taker fee when the information advantage is large enough.

---

# 12. Bottom line

The most defensible structural thesis after the correction is:

> **A calibrated weather distribution should be monetized with maker-first, two-sided quoting during quiet states and taker execution only after fast information shocks. Complete-set merge is a valid capital-recycling primitive, but specialist manual-merge behavior remains unproven until wallet-level operation attribution is reconstructed.**

This is actually a cleaner research target than the earlier interpretation.

The edge does not depend on assuming that Poligarch manually merged 67K times.

What is already proven is enough to justify the next measurement:

- major profitable Weather specialists provide passive liquidity;
- makers pay zero Weather trading fee;
- rebates are economically material;
- target-wallet specialists sometimes pay substantial taker fees for immediate information-driven execution;
- Polymarket's own CTF mechanics allow deliberate pair merge whenever complementary inventory is acquired cheaply.

The next production-fidelity evidence should therefore measure **maker fill markout + trader-level inventory cashflows**, not raw Struct merge counts.