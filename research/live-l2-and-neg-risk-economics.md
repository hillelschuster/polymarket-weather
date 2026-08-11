# Live L2 + NegRisk execution economics

Snapshot: **2026-08-11**

Purpose: turn the deterministic NegRisk identities into a realistic evidence plan by quantifying the current Weather taker hurdle and identifying exactly which market data can and cannot be reconstructed historically.

## Verdict

The mathematical NegRisk identities are real, but **small cross-ladder inconsistencies are not taker arbitrage under current Weather fees**.

For a diffuse 8–12 bucket ladder, buying one share of every outcome as taker costs roughly **4.4–4.6¢ in platform fees per complete event basket**, before spread, impact, gas, and any NegRisk conversion haircut.

Therefore the economically strongest formulation is currently:

> **Use live synchronized L2 to detect event-level inconsistencies, but accumulate structurally attractive legs passively whenever the discrepancy is smaller than the taker hurdle. Use the calibrated weather distribution to value the uncompleted basket and protect the maker from adverse selection.**

The second key finding is data-related:

> **Recent historical L2 cannot be faithfully recovered from Polygon fills alone because Polymarket matching is offchain. The old unofficial/legacy `/orderbook-history` path is reported to have stopped emitting new snapshots around 2026-02-20. Production-fidelity evidence therefore requires capturing the public market WebSocket from now forward, or obtaining a genuine third-party L2 archive.**

---

# 1. Current Weather taker and maker economics

Polymarket's current official fee schedule gives Weather:

- taker fee rate `r = 0.05`;
- maker fee = `0`;
- maker rebate allocation = `25%` of the eligible taker-fee pool.

Current fee formula:

`fee = shares * r * p * (1-p)`.

Official sources:

https://docs.polymarket.com/trading/fees

https://docs.polymarket.com/market-makers/maker-rebates

For 100 Weather shares the official table shows approximately:

- 10¢ or 90¢: `$0.45` fee;
- 30¢ or 70¢: `$1.05` fee;
- 50¢: `$1.25` fee.

That means taker friction is **0.45–1.25¢ per share** over most economically relevant prices.

The supplied target wallet's recovered transactions are consistent with this order of magnitude: it paid about one cent/share in protocol fee on mid-priced Weather taker purchases.

---

# 2. Full-ladder taker fee has a clean closed form

Let an exhaustive `K`-bucket Weather event have coherent true/fair probabilities:

`q_1 + ... + q_K = 1`.

At fair prices:

- YES price for bucket `i` is `q_i`;
- NO price is `1 - q_i`.

Suppose we buy **one share of every YES** as taker.

Total fee is:

`F_yes = r * sum_i q_i * (1-q_i)`.

Using `sum_i q_i = 1`:

`F_yes = r * (1 - sum_i q_i^2)`.

Now buy **one share of every NO** as taker.

For NO price `1-q_i`:

`(1-q_i) * q_i = q_i * (1-q_i)`.

Therefore:

`F_no = r * (1 - sum_i q_i^2)`.

The full YES and full NO baskets have the same approximate total taker fee when their quotes are coherent.

This is useful because it gives the event-level taker hurdle directly from concentration of the probability distribution.

---

# 3. Size of the hurdle for temperature ladders

If probability were uniform over `K` buckets:

`q_i = 1/K`.

Then:

`sum q_i^2 = 1/K`

and:

`F = r * (1 - 1/K)`.

With current Weather `r=0.05`:

| K | Full-basket taker fee/share-set |
|---:|---:|
| 6 | 4.167¢ |
| 8 | 4.375¢ |
| 10 | 4.500¢ |
| 12 | 4.583¢ |
| 15 | 4.667¢ |

Real Weather distributions are usually more concentrated than uniform, so actual fee is somewhat lower.

Example concentration:

`q = [0.40, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02]`

has:

`sum q_i^2 = 0.26`

so:

`F = 0.05 * 0.74 = 3.70¢`.

Thus a realistic full-event taker fee is often roughly **3–5¢ per one-share basket**.

This is much larger than the 0.5–2¢ apparent price-sum discrepancies that look interesting when fees are ignored.

---

# 4. Exact executable deterministic inequalities

For actual asks `aYi` and `aNi`, do not substitute fair `q` in execution calculations.

## Full YES settlement basket

Gross settlement value = `$1`.

For common size `x`, depth-aware all-in expected PnL is:

`PnL_yes(x) = x * [1 - sum_i VWAP_ask_yes_i(x)]`

`- sum_i taker_fee_yes_i(x)`

`- capital_time_cost`

`- execution_failure_cost`.

At one-share top-of-book approximation:

`edge_yes = 1 - sum_i aYi - r * sum_i aYi*(1-aYi)`.

This must be positive **after** fee and depth, not merely `sum ask < 1`.

## Full NO NegRisk conversion basket

Let:

`lambda = 1 - negRiskFeeBips/10_000`.

For `K` selected NOs, conversion yields:

`lambda * (K-1)` collateral per unit.

One-share top-of-book approximation:

`edge_no = lambda*(K-1) - sum_i aNi - r*sum_i aNi*(1-aNi) - gas`.

Again, `sum NO asks < K-1` is not enough.

The conversion haircut can be comparable to the entire observed price discrepancy.

For `K=10`:

- 0 bps conversion fee: output `$9.000`;
- 10 bps: `$8.991` — 0.9¢ haircut;
- 50 bps: `$8.955` — 4.5¢ haircut.

So the actual event `negRiskFeeBips` is mandatory input.

---

# 5. Gamma already exposes the NegRisk metadata needed

Polymarket's official Gamma `GET /events/slug/{slug}` response includes:

- `negRisk`;
- `negRiskMarketID`;
- `negRiskFeeBips`;
- nested `markets`.

Official docs:

https://docs.polymarket.com/api-reference/events/get-event-by-slug

This is simpler than requiring an RPC read for normal discovery.

Production path:

1. fetch event by slug;
2. verify `negRisk == true`;
3. record `negRiskMarketID` and `negRiskFeeBips`;
4. enumerate the nested market list and token IDs;
5. optionally validate the fee onchain through the NegRisk Adapter.

### API caveat

A 2026 issue in Polymarket's own `py-clob-client` repository reports that Gamma's `/markets?negRiskMarketID=...` filter can silently return unrelated markets.

Therefore do **not** depend on that filter to prove group exhaustiveness.

Prefer the parent event's nested markets plus explicit event identity, and verify question count / market ID consistency.

Issue:

https://github.com/Polymarket/py-clob-client/issues/341

---

# 6. Current public L2 path is good enough for production-fidelity evidence

Polymarket exposes:

`POST /books`

for batch current order books across multiple token IDs.

Official docs:

https://docs.polymarket.com/api-reference/market-data/get-order-books-request-body

For persistent synchronized data, the public market WebSocket is better:

`wss://ws-subscriptions-clob.polymarket.com/ws/market`

with asset IDs and `custom_feature_enabled: true`.

It emits:

- initial/full `book` snapshots;
- `price_change` updates on placements/cancellations;
- `best_bid_ask` changes;
- `last_trade_price`;
- tick-size changes;
- new-market and resolved-market events.

Official docs:

https://docs.polymarket.com/market-data/websocket/market-channel

No authentication is required for the market channel.

For the subset scanner this is the exact evidence needed: synchronized L2 depth with exchange timestamps.

---

# 7. Historical price history is not historical L2

The official current CLOB API provides `GET /prices-history` for a token.

That gives price time series, not the resting bid/ask depth that would have been executable for a multi-leg basket.

Official orderbook docs:

https://docs.polymarket.com/trading/orderbook

A backtest that uses historical last prices or midpoint series to simulate simultaneous multi-leg taker execution will systematically overstate capacity and can create fictitious arbitrage.

---

# 8. The old orderbook-history route is currently unusable for recent history

A February 2026 NautilusTrader issue documents that Polymarket's former `/orderbook-history` endpoint stopped returning new snapshots around **2026-02-20 20:00 UTC**; later windows returned empty data.

Source:

https://github.com/nautechsystems/nautilus_trader/issues/3635

This is not an official Polymarket statement, but it is a concrete reproducible report and is consistent with the endpoint no longer appearing in current Polymarket API documentation.

Current official market-data docs list:

- `/book`;
- `/books`;
- `/prices-history`;

but not a current historical-L2 endpoint.

Conclusion:

> **Do not assume recent official historical orderbook snapshots are obtainable.**

---

# 9. Polygon fills cannot recreate offchain book history

Polymarket explicitly describes the CLOB as hybrid-decentralized:

1. orders are matched **offchain**;
2. matched trades settle **onchain**.

Official source:

https://docs.polymarket.com/concepts/prices-orderbook

Consequences:

Onchain `OrderFilled` / `OrdersMatched` records can recover:

- actual fills;
- maker/taker identities;
- prices;
- quantities;
- fees;
- transaction ordering.

They cannot recover the full historical set of:

- unfilled resting orders;
- cancellations that never traded;
- queue depth ahead of an order;
- transient book states with no fill.

Therefore the chain is sufficient for **wallet/fill research** but insufficient for a production-fidelity **historical L2 arbitrage replay**.

---

# 10. Why live L2 capture has unusually high research value now

The data is public, high-rate limits are generous, and Weather has a manageable number of markets.

The current official rate limits include up to hundreds of `/books` requests per 10 seconds and thousands of general CLOB requests; the WebSocket avoids most polling entirely.

Source:

https://docs.polymarket.com/api-reference/rate-limits

A minimal collector only needs to persist state-changing messages for active Weather asset IDs.

Store:

`exchange_timestamp`
`local_receive_timestamp`
`event_id`
`condition_id`
`token_id`
`book_hash`
`price levels`
`event negRiskFeeBips`
`fee schedule`
`market lifecycle`.

From those messages, every candidate basket can be replayed exactly at each event timestamp.

This is a much higher-value data asset than collecting additional daily midprices.

---

# 11. Maker accumulation becomes more attractive after the fee calculation

The full-event taker hurdle of ~3–5¢ does **not** apply to maker fills because current maker platform fee is zero.

Suppose the fair bucket probability is `q_i` and we quote:

`YES bid_i = q_i - mYi`

`NO bid_i = 1 - q_i - mNi`.

Every passive fill earns the quoted valuation margin before adverse selection.

If complementary inventory eventually completes:

`YES bid_i + NO bid_i = 1 - mYi - mNi`.

A complete binary set can merge to `$1`, giving raw capture:

`mYi + mNi`.

For event-level NegRisk baskets, the same concept generalizes: accumulate selected legs below model/transform value with maker orders; only pay conversion/gas once the deterministic route is complete enough.

This is the likely economic reason to combine:

- deterministic NegRisk identities;
- Weather fair-value distributions;
- passive maker execution.

---

# 12. Rebates can now be measured directly rather than inferred from Struct

Polymarket documents a public endpoint:

`GET /rebates/current?date=YYYY-MM-DD&maker_address=0x...`

which returns per-condition maker rebated fees and requires **no authentication**.

Official docs:

https://docs.polymarket.com/api-reference/rebates/get-current-rebated-fees-for-a-maker

This is valuable for specialist reverse engineering.

For Poligarch or another maker candidate, daily rebate history can be joined to:

- onchain maker notional;
- Weather condition IDs;
- daily PnL;
- number of maker fills.

Useful derived metrics:

`rebate_bps = rebate_usdc / maker_notional`

`rebate_per_fill`

`rebate / estimated spread_capture`

`rebate / total_net_pnl`.

This allows the project to determine whether rebates are incidental or central to maker profitability without relying only on Struct aggregates.

---

# 13. Direct NegRisk conversion is not yet exposed by the official CLI

Polymarket's current CLI supports standard:

- split;
- merge;
- redeem;
- redeem-neg-risk.

But an open feature request asks for a direct NegRisk `convert` command, implying it is not currently available in the CLI abstraction.

Source:

https://github.com/Polymarket/polymarket-cli/issues/64

The contract operation itself is supported by the NegRisk Adapter.

Therefore a production scanner that chooses to execute subset conversion should call the adapter/current collateral adapter directly through a minimal contract binding rather than depend on a CLI command.

This is implementation detail, not a strategy obstacle.

---

# 14. Updated evidence priority

The current evidence ladder for the structural strategy is now:

### Highest priority — live synchronized L2

Measure:

- how often fee-adjusted deterministic inequalities actually occur;
- duration;
- depth;
- maximum net dollars;
- whether passive accumulation improves them enough to matter.

### Second — maker fill markout

For Poligarch-like flow and our future quotes:

- 5s / 30s / 5m / 30m markout;
- adverse selection by forecast-catalyst state;
- spread capture;
- rebate contribution.

### Third — target wallet information shocks

Recover point-in-time forecast `Δq` around fee-paying taker fills.

This establishes when paying the ~0.5–1.25¢/share taker hurdle is justified.

### Fourth — penny tails

Replay the complete loser-inclusive basket using actual extreme-price fee rounding and depth.

---

# Bottom line

The NegRisk discovery is still important, but the economically viable target is narrower than a naive sum-arbitrage bot:

> **Current Weather taker fees make small deterministic ladder discrepancies untradeable. The strongest formulation is to collect synchronized L2, use the NegRisk identities as exact terminal/transform values, and place zero-fee maker orders whose incomplete-basket risk is controlled by a calibrated weather distribution. Cross only large, short-lived violations or genuine forecast shocks.**

The single highest-value missing dataset is now **our own live Weather L2 archive**, because it is the only clean route to production-fidelity spread/depth/capacity evidence for current 2026 markets.