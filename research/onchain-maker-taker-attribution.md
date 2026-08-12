# On-chain maker/taker attribution for Polymarket Exchange V2

Snapshot: **2026-08-12**

Purpose: prevent a money-relevant decoding error when classifying specialist Weather fills from Polygon logs.

## Verdict

Do **not** classify a trader as passive maker merely because its address appears in the `maker` field of an `OrderFilled` event.

In Polymarket CTF Exchange V2, the active taker order is itself a signed order created by a user. When the exchange emits the taker fill, it sets:

`maker = takerOrder.maker`

`taker = address(this)`

Therefore the field name `maker` in `OrderFilled` means **order creator**, not necessarily passive-liquidity maker.

The reliable transaction-level role signal is:

> `OrdersMatched.takerOrderMaker` identifies the active/taker order's user.

Matched `OrderFilled` rows belonging to other order creators are passive maker orders for that match.

Official source:

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/mixins/Trading.sol

---

# 1. Contract semantics

`matchOrders()` takes:

- one `takerOrder` — the active order;
- an array of `makerOrders` — passive orders matched against it.

The contract's `_emitTakerFilledEvents(...)` path emits `OrderFilledParams` with:

- `maker: takerOrder.maker`;
- `taker: address(this)`.

The passive maker paths emit `OrderFilled` with:

- `maker: makerOrder.maker`;
- `taker: takerOrder.maker`.

Finally, `OrdersMatched` emits the taker order hash and `takerOrderMaker`.

Therefore a robust decoder should first locate `OrdersMatched`, record `takerOrderMaker`, and then classify all order hashes/fills in the transaction relative to that active order.

---

# 2. Anchor proof A — target wallet June 30 Milan BUY is an active taker

Transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

PolygonScan:

https://polygonscan.com/tx/0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6

Market:

**Milan June 30 — 35°C YES**.

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`.

Observed transaction facts:

- wallet buys **102.116 YES**;
- raw consideration: **30 pUSD**;
- wallet transfers **31.05932 pUSD** into the exchange;
- `FeeCharged` = **1.05932 pUSD**;
- final target-wallet `OrderFilled` has `makerAmountFilled=30,000,000`, `takerAmountFilled=102,116,000`, `fee=1,059,320`;
- `OrdersMatched.takerOrderMaker` = **target wallet**.

Therefore this fill is not merely inferred to be aggressive from fee payment. It is directly identified by the exchange event as the **active/taker order**.

Economic cost:

`(30 + 1.05932) / 102.116 ≈ 30.415¢/share`.

This validates the prior thesis that the target wallet is willing to cross and pay the Weather taker fee when it believes the forecast edge is large enough.

---

# 3. Anchor proof B — Poligarch Wellington July 21 fill is passive maker liquidity

Transaction:

`0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213`

PolygonScan:

https://polygonscan.com/tx/0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213

Market:

**Wellington July 21 — 11°C**.

Poligarch:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`.

Observed transaction facts:

- `OrdersMatched.takerOrderMaker` = `0x5a218C7AD04135830a45c41AAed7294Df7809318`, **not Poligarch**;
- a matched `OrderFilled` has `maker = Poligarch` and `taker = 0x5a218...`;
- Poligarch `makerAmountFilled = 9.400590 pUSD`;
- Poligarch receives/acquires `9.990000` relevant tokens;
- Poligarch fill fee = **0**.

Effective acquisition price:

`9.400590 / 9.99 = 94.1¢`.

This is direct proof that Poligarch was a **passive maker order** in this Weather transaction.

---

# 4. Why this matters economically

Without correct role attribution, several money-critical measurements become wrong:

- maker fill probability;
- adverse-selection markout;
- maker rebate eligibility;
- true taker cost;
- whether a specialist reacts immediately to a forecast shock or waits passively;
- whether temporal complete-set inventory came from passive or aggressive fills.

`OrderFilled.maker == wallet` is insufficient and can invert the interpretation.

The historical collector should derive a canonical field:

`liquidity_role ∈ {TAKER, MAKER}`

from `OrdersMatched`, not from event-field names alone.

---

# 5. Minimal decoder rule

For each `matchOrders` transaction:

1. parse `OrdersMatched`:
   - `takerOrderHash`;
   - `takerOrderMaker`;
   - side/token/filled amounts.
2. classify the `OrderFilled` whose `orderHash == takerOrderHash` as **TAKER**;
3. classify other matched order fills as **MAKER**;
4. preserve fee per order from `OrderFilled.fee` / `FeeCharged` cashflows;
5. only then normalize economic YES/NO direction through NegRisk identities.

Also retain transaction-level CTF `MINT/MERGE` operations separately. An exchange-internal MINT/MERGE during matching is not automatically a user-initiated inventory operation.

---

# 6. Updated execution-archetype evidence

After correcting the field semantics, the main contrast survives and becomes stronger:

### Supplied forecasting wallet

At least one recovered T+1 Milan entry is **proven active/taker**, with a substantial mid-curve Weather fee. Combined with the separately observed losing-bucket exit and repeated post-18Z timing, this supports an information-driven crossing layer.

### Poligarch

At least one recovered Weather acquisition is **proven passive maker**, fee zero. Combined with its two-sided inventory and large maker-rebate history, this supports a market-making/inventory layer.

These two archetypes are therefore not an artifact of misreading the `maker` event field.

---

# Bottom line

For Exchange V2 research:

> **`OrdersMatched.takerOrderMaker` is the source of truth for active/taker role. `OrderFilled.maker` only tells us who created that order.**

This correction should be applied to every future specialist fill reconstruction before computing execution alpha.