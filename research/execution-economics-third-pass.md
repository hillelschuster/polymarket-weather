# Execution economics — third pass

Snapshot: **2026-08-12**

Purpose: consolidate the newest acquisition and microstructure findings into the smallest set of measurements that can change net PnL.

## Verdict

The project now has enough evidence for one unified trading object:

> **estimate a coherent resolver probability vector `q`, then route each state through the execution mode with the highest expected net dollars.**

The strongest currently supported modes are:

1. **information-shock taker** — directly supported by the supplied wallet's fee-paying aggressive Weather buys;
2. **forecast-aware passive maker** — directly supported by zero-fee Weather maker fills from major profitable specialists;
3. **balanced YES/NO maker inventory + merge** — exact CTF economics and explicitly documented market-maker inventory operation; specialist attribution of deliberate merges remains unproven;
4. **NegRisk event-level conversion/arbitrage** — exact structural identities, pending live `negRiskFeeBips` and synchronized depth;
5. **penny-tail acquisition** — supported by specialist examples, still requiring loser-inclusive capacity/PnL measurement;
6. **near-certainty recycling** — directly observed in the supplied wallet.

The largest new research improvement is not another forecast model. It is that **the transaction and incentive ledger can now be reconstructed with public sources**.

---

# 1. Full target-wallet V2 history is now mechanically obtainable

Target:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

New collector:

`scripts/sqd_v2_wallet_orders.py`

The decisive V2 fact comes from Polymarket's exchange source:

`OrderFilled(orderHash, maker, taker, side, tokenId, makerAmountFilled, takerAmountFilled, fee, builder, metadata)`

uses indexed:

- `topic1 = orderHash`;
- `topic2 = maker / order owner`;
- `topic3 = taker field`.

For the active `takerOrder`, V2 still emits:

`maker = takerOrder.maker`

`taker = address(exchange)`.

Therefore:

`OrderFilled.topic2 == target_wallet`

is the canonical filter for the target's **own order rows**, passive or aggressive.

This avoids the main NegRisk reconstruction trap: summing all rows in a transaction where the target is the active taker can double-count the target's economic trade by also counting matched counterparty rows.

Primary source:

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/mixins/Events.sol

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/mixins/Trading.sol

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/libraries/Structs.sol

SQD public Polygon history gives a server-side topic-filtered route over both V2 exchanges.

Detailed note:

`research/sqd-wallet-backfill-breakthrough.md`

---

# 2. The V2 decoder is validated against two known target trades

These are manual transaction-level validations of the decoding method. The SQD network endpoint itself could not be reached from the current sandbox because DNS resolution is disabled; do not confuse source validation with an executed full backfill.

## July 12 target BUY

Transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

Canonical target-owned active row:

- side: BUY;
- shares: **166.68**;
- raw collateral: **$44.274**;
- raw price: **26.5623¢**;
- logged platform fee: **$1.62569**;
- all-in price: **27.5376¢**;
- builder: zero;
- active/aggressive role: target row's `taker` field is the exchange.

The fee matches the Weather curve:

`0.05 * p * (1-p)`

to on-chain rounding precision.

No builder code means there was no builder fee on this order path.

## Milan June 30 — 35°C BUY

Transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

Canonical target-owned row:

- order hash: `15E07FECD1530D5AD4432C33C1CCD9EB3E7927BC0FAB044CD998D6F5F06828CF`;
- BUY;
- token `47809137889791405662099861602793364077088639904534506506807768466233401292978`;
- 102.116 shares;
- $30 raw collateral;
- fee **$1.05932**;
- builder zero.

This exactly reproduces the earlier 29.38¢ raw / ~30.42¢ all-in reconstruction.

The target's known aggressive Weather trades therefore validate all important decoder fields:

- order owner;
- active/passive role;
- side;
- token;
- shares;
- collateral;
- platform fee;
- builder attribution.

---

# 3. Human enrichment no longer needs Struct

New script:

`scripts/enrich_v2_wallet_orders.py`

For every unique V2 token it joins three official Polymarket representations:

1. CLOB `markets-by-token/{token}`;
2. Gamma market by `condition_id`;
3. CLOB market info by `condition_id`.

It cross-checks the token's YES/NO label across all three rather than trusting one source.

The enriched row includes:

- condition ID;
- market/event title and slug;
- outcome/bucket;
- resolver/source text;
- event dates;
- fee-enabled state and fee schedule;
- CLOB tick/min-order/fee details;
- `negRisk`;
- `negRiskMarketID`;
- `negRiskFeeBips`;
- reward config where exposed.

This is enough to filter the raw wallet ledger into Weather and identify exact city/date/bucket without third-party APIs.

Official API docs:

https://docs.polymarket.com/api-reference/market-data/get-market-by-token

https://docs.polymarket.com/api-reference/markets/list-markets

https://docs.polymarket.com/api-reference/market-data/get-clob-market-info

---

# 4. The public Data API is now a useful first-pass wallet ledger

New script:

`scripts/polymarket_user_activity.py`

Polymarket's public Data API `GET /activity` returns human-enriched user activity for:

- `TRADE`;
- `SPLIT`;
- `MERGE`;
- `REDEEM`;
- `REWARD`;
- `CONVERSION`;
- `MAKER_REBATE`;
- `REFERRAL_REWARD`.

Source:

https://docs.polymarket.com/api-reference/core/get-user-activity

The endpoint's maximum offset is 10,000 and page limit is 500. The collector recursively splits requested timestamp windows whenever the final safe page is full, preventing silent truncation. If more than 10,000 rows occur in one Unix second it deliberately fails and sends the research path back to SQD.

Use this Data API layer for:

- rapid human market labeling;
- transformations/redeems/rebates;
- transaction hashes;
- coarse trade path.

Use the V2 `OrderFilled` ledger for:

- exact passive/aggressive role;
- exact order hash;
- platform fee;
- builder code;
- canonical non-double-counted economics.

This division minimizes engineering while preserving money-critical evidence.

---

# 5. Aug 10 position-basis update reduces current-state accounting work

Polymarket's Aug 10, 2026 changelog added optional position fields:

- `grossInitialValue` — remaining entry basis including attributed buy fees;
- `entryFeesUsdc` — the fee component.

`initialValue` and `avgPrice` remain fee-exclusive.

Source:

https://docs.polymarket.com/changelog/predictions

For current/open Weather positions this means the API can directly expose fee-inclusive remaining basis when those optional fields are present.

It does **not** replace the full fill ledger for closed/revised positions because the central research question is still the path:

`entry -> information revisions -> partial exit -> final exit/redemption`.

---

# 6. Milan June 25 is still the highest-value directional case

Market:

**Milan June 25 — 33°C YES**.

Struct's indexed trade table shows:

- target wallet: SELL/reduce **193.78 YES around 10.9¢**;
- other recognized specialists still buying small amounts around 11–12¢;
- 33°C ultimately lost; 35°C won.

Indexed snapshots also show an earlier market regime around Jun 23 where 33°C traded roughly **27–28¢**, followed by later states around the high teens / low teens.

This is consistent with a material downward probability revision before settlement.

What remains unproven is the causal link:

`fresh forecast revision -> target exit`.

The exact V2 topic2 backfill now makes that measurable.

First extraction after the collector runs:

1. every target BUY in the 33°C token;
2. exact 193.78-share SELL timestamp and role;
3. preceding 12Z/18Z ECMWF and local-model forecast maxima;
4. next available forecast run;
5. 33/34/35°C PMXT book before and after the exit;
6. 5m/30m/2h markout;
7. realized dollars saved versus holding to zero.

If the exit systematically follows a downward `Δq` across many cases, forecast-revision trading becomes reproducible alpha rather than anecdote.

---

# 7. Maker rebates are large enough to alter optimal routing

Current official Weather structure:

- taker fee rate: `r = 0.05`;
- maker platform fee: `0`;
- maker rebate pool: **25% of collected taker fees**;
- distribution: fee-curve weighted;
- maker fill weight:

`fee_equivalent = C * r * p * (1-p)`.

Official docs:

https://docs.polymarket.com/trading/fees

https://docs.polymarket.com/programs/maker-rebates

New collector:

`scripts/polymarket_maker_rebates.py`

uses the public no-auth endpoint:

`GET /rebates/current?date=...&maker_address=...`

and records **actual reported USDC rebate rows per condition/day**.

Source:

https://docs.polymarket.com/api-reference/rebates/get-current-rebated-fees-for-a-maker

This is superior to estimating rebates from total category volume.

---

# 8. Rebate algebra creates a potentially important maker subsidy

The official allocation is:

`rebate_i = own_fee_equivalent_i / total_fee_equivalent * rebate_pool`.

The pool is a percentage `R` of collected taker fees.

If, within one fixed-fee market/day, the sum of maker fee-equivalent equals the corresponding taker fees collected at actual execution prices, then:

`rebate_i = R * own_fee_equivalent_i`.

For Weather:

`R = 0.25`

`r = 0.05`.

So the implied rebate per filled maker share becomes:

`rebate/share ~= 0.0125 * p * (1-p)`.

### Important evidence label

This simplification is a **derived hypothesis**, not yet an audited accounting identity.

Supporting facts:

- maker rebate weights use the same `C * feeRate * p(1-p)` curve as taker fees;
- takers receive price improvement to the resting maker price;
- the pool is funded from collected taker fees.

But the actual per-day `/rebates/current` output remains the source of truth because rounding, aggregation and any implementation details can break exact equality.

The first live data validation should calculate:

`actual_rebate / sum(own maker fee_equivalent)`

for every Weather condition/day.

If this ratio clusters at 0.25, the simplification is validated.

---

# 9. Economic scale of that subsidy

Under the simplification above, for a passive maker **BUY** at price `p`, rebate as basis points of cash deployed is:

`10,000 * [0.25 * 0.05 * p(1-p)] / p`

which simplifies to:

`125 * (1-p) bp`.

Examples:

| Maker BUY price | Approx rebate / cash deployed |
|---:|---:|
| 5¢ | 118.75 bp |
| 10¢ | 112.50 bp |
| 20¢ | 100.00 bp |
| 30¢ | 87.50 bp |
| 40¢ | 75.00 bp |
| 50¢ | 62.50 bp |
| 60¢ | 50.00 bp |
| 70¢ | 37.50 bp |
| 80¢ | 25.00 bp |
| 90¢ | 12.50 bp |

This is a **capital-efficiency** view. Per-share rebate remains maximal at 50¢ because `p(1-p)` peaks there.

Consequences worth testing:

1. cheap-side passive BUY liquidity can receive a large rebate relative to cash committed;
2. rebate economics can make tiny repeated fills rational even when raw spread capture looks unimpressive;
3. maker inventory should be ranked on **net markout + actual rebate**, not markout alone;
4. penny-tail maker behavior may have materially different economics from penny-tail taker behavior.

Do not trade on this table until the actual rebate-ratio validation is run.

---

# 10. Balanced YES/NO maker inventory has a particularly clean test

Official CTF identity:

`1 YES + 1 NO -> $1 pUSD`.

Polymarket's own market-maker inventory documentation explicitly recommends merging equal YES/NO balances to free collateral.

Sources:

https://docs.polymarket.com/trading/ctf/merge

https://docs.polymarket.com/market-makers/inventory

Suppose passive BUY fills acquire equal quantities at:

`bY`

and

`bN`.

Before rebates:

`gross_pair_capture = 1 - bY - bN`.

Under the rebate simplification:

`pair_rebate ~= 0.25 * 0.05 * [bY(1-bY) + bN(1-bN)]`.

If prices are complementary:

`bN = 1 - bY`,

then raw pair capture is zero but estimated rebate capture is:

`0.025 * bY * (1-bY)`.

Examples:

- 30/70 pair: **52.5 bp of complete-set value**;
- 40/60 pair: **60 bp**;
- 50/50 pair: **62.5 bp**.

This is large enough to make balanced passive inventory a first-class strategy hypothesis.

### What destroys the apparent free edge

The pair only exists after **both sides fill**.

The real cost is residual inventory while one leg is unfilled:

- adverse selection after weather information shocks;
- fill imbalance;
- stale quote cancellation latency;
- opportunity cost of collateral;
- crossing cost if the bot forces completion;
- any mismatch between estimated and actual rebate allocation.

Therefore the correct score is not theoretical pair rebate. It is:

`realized spread/pair capture + actual rebate - residual inventory markout - forced-completion cost`.

This is exactly where weather information can produce an advantage over a generic market maker: it predicts which unpaired inventory is safe and when quotes must be canceled.

---

# 11. Poligarch is a strong candidate for this measurement

Indexed Poligarch snapshot around July 21 shows:

- roughly **229K trades** in the displayed period;
- average trade size around **$6.37**;
- **84.1% of buys under $10**;
- simultaneous residual YES and NO positions in Weather binaries;
- direct transaction-level zero-fee Weather maker activity already proven.

Source:

https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

Polymarket profile snapshots also show large Weather positions across many cities alongside non-Weather positions, so lifetime rebate/PnL totals must not be labeled Weather-only.

The useful experiment is condition-level:

For each Poligarch Weather condition/day:

`maker_fill_notional`

`maker_fee_equivalent`

`actual_rebate`

`10s/1m/5m/30m markout`

`end-of-day complementary inventory`

`dedicated merge/split calls`

`settlement PnL`.

Then compute:

`net_maker_edge = markout + spread_capture + actual_rebate - inventory_completion_cost`.

No inference from Struct's raw `merge count` is needed.

---

# 12. Historical Weather fee regime is now clearly dated

Polymarket's changelog states that **Fee Structure V2** expanded fees to Weather and several other categories on **March 30, 2026**.

On March 31 the documentation changed the recommended fee source to each market's `feeSchedule` object.

Source:

https://docs.polymarket.com/changelog/predictions

This matters for historical tests:

- do not apply today's category fee curve blindly to pre-March-30 history;
- persist each market's fee-enabled state / fee schedule;
- for Jun/Jul 2026 specialist trades, verify the market metadata but expect the V2 Weather regime.

The known target Jun30 and Jul12 on-chain fees already empirically confirm fee-enabled Weather execution in those cases.

---

# 13. PMXT completes the execution evidence stack

The remaining historical market-state join is PMXT's free hourly Polymarket market-channel Parquet archive, available from April 13, 2026 onward.

That overlaps every Jun/Jul specialist case in the current research.

For every wallet fill, retrieve:

- last book before fill;
- executable bid/ask and depth;
- full event ladder;
- 5m/30m/2h post-fill markout.

Then the directional and maker strategies can be evaluated on the same scale.

### Directional taker

`net_edge = q_after - all_in_fill_cost`

plus subsequent markout / realized exit economics.

### Maker

`net_edge = q_at_fill - fill_price + actual_rebate - adverse_markout`

with inventory pairing/merge handled separately.

---

# 14. Highest-value production-fidelity experiments now

## Experiment A — target wallet forecast revisions

Run:

`Data API activity + SQD own-order rows + official metadata + PMXT + model vintages`.

Primary events:

1. Milan Jun25 33°C;
2. Milan Jun30 35°C;
3. Mexico City Jul16 25°C;
4. every subsequent Weather exit/reduction.

Output:

`Δq before fill`

`role`

`fee`

`5m/30m/2h markout`

`realized exit value`

`value saved by exit vs hold`.

## Experiment B — Poligarch maker economics

For Weather conditions only:

`SQD passive fills`

`+ PMXT markout`

`+ actual /rebates/current cashflow`

`+ transformations`.

Output:

- actual rebate / maker fee-equivalent;
- net maker bp per matched dollar;
- net maker dollars/day;
- residual-inventory loss distribution;
- performance around forecast/observation shocks;
- pair completion rate/time.

## Experiment C — execution router comparison

For the exact same weather fair-value states, replay:

1. cross immediately;
2. post at best bid/ask improvement;
3. post q-centered two-sided quotes;
4. acquire balanced pair and merge when completed.

Rank by:

`net dollars / capital-hour`

and

`capacity`.

This determines whether forecast accuracy should primarily monetize through prediction, making, or both.

---

# 15. Updated economic thesis

The strongest current formulation is no longer merely:

> forecast the correct temperature better than the market.

It is:

> **maintain a better probability surface than the market, know when it just changed, and express that information through the cheapest/highest-dollar execution path available in the current market state.**

The evidence supports a state-dependent router:

### Quiet state

- post-only maker quotes around calibrated `q`;
- capture spread/margin;
- earn actual maker rebates;
- tolerate only forecast-favorable residual inventory;
- merge complete YES/NO sets when that releases capital advantageously.

### Fresh large information shock

- cancel stale maker quotes;
- cross clearly positive all-in depth immediately;
- the supplied wallet proves specialists sometimes pay the Weather fee for this privilege.

### Structural dislocation

- execute full-ladder / NegRisk cycle when synchronized depth clears all fees and `negRiskFeeBips`.

### Extreme tail

- acquire only where calibrated tail probability exceeds microprice plus execution cost;
- test maker and taker economics separately because rebates can materially change cheap-side capital efficiency.

This remains one compact strategy, not four systems. The shared core is the same `q` vector and the same event-level book/inventory object.

---

# Bottom line

The research bottleneck has shifted from **data access** to **measurement**.

We now have public routes for:

- exact V2 wallet-owned fills;
- maker/taker role;
- platform fee and builder attribution;
- human market/event metadata;
- transformations and redemptions;
- current position fee basis;
- actual per-condition/day maker rebates;
- historical point-in-time books;
- point-in-time forecast vintages.

The next material answer should not be another qualitative hypothesis. It should be one of two dollar measurements:

1. **How much value did the target wallet's forecast-revision exits save or earn after fees?**
2. **How many net basis points per matched Weather dollar does Poligarch-style passive making earn after actual rebates and adverse markout?**

Whichever is larger at meaningful capacity should receive implementation capital first.