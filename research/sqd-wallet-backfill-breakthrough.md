# Exact V2 wallet-order backfill via SQD Portal

Snapshot: **2026-08-12**

Target wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

## Verdict

The wallet-history acquisition bottleneck no longer requires profile scraping, paid APIs, or a scan of all Polygon `OrderFilled` rows.

Polymarket V2 emits the **owner of every order in indexed topic2 (`maker`)**. Crucially, this is true for both passive maker orders and the active/aggressive order: for the active order, the contract emits an `OrderFilled` row whose `maker` is `takerOrder.maker` and whose `taker` is the exchange contract itself.

Therefore the cleanest wallet ledger is:

> query both V2 exchange contracts for `OrderFilled` with `topic2 = target_wallet`.

That returns the wallet's own order fills exactly once at the order level and avoids incorrectly treating every counterparty leg in a NegRisk match as a separate target-wallet trade.

The relevant public Polygon history can be streamed from SQD Portal with server-side topic filters.

---

## 1. Primary-source V2 event layout

Polymarket V2 source:

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/mixins/Events.sol

Event signature:

`OrderFilled(bytes32,address,address,uint8,uint256,uint256,uint256,uint256,bytes32,bytes32)`

The contract emits `log4`, so indexed topics are:

- `topic0` = `OrderFilled` event signature;
- `topic1` = `orderHash`;
- `topic2` = `maker`;
- `topic3` = `taker`.

Non-indexed data words are:

1. `side`;
2. `tokenId`;
3. `makerAmountFilled`;
4. `takerAmountFilled`;
5. `fee`;
6. `builder`;
7. `metadata`.

Known topic0:

`0xd543adfd945773f1a62f74f0ee55a5e3b9b1a28262980ba90b1a89f2ea84d8ee`

---

## 2. Why topic2 is the canonical wallet filter

Polymarket V2 trading source:

https://github.com/Polymarket/ctf-exchange-v2/blob/main/src/exchange/mixins/Trading.sol

The source distinguishes an active `takerOrder` from passive `makerOrders`.

### Passive order row

For a passive `makerOrder`, emitted fields include:

- `maker = makerOrder.maker`;
- `taker = active-order owner`;
- `side = makerOrder.side`;
- `tokenId = makerOrder.tokenId`.

### Active/aggressive order row

For the active `takerOrder`, `_emitTakerFilledEvents` emits:

- `maker = takerOrder.maker`;
- `taker = address(this)`;
- `side = takerOrder.side`;
- `tokenId = takerOrder.tokenId`;
- the active order's aggregate filled amounts and fee.

This means `maker` in the event is best understood as **order owner**, not necessarily liquidity-provider role.

Hence:

`topic2 == wallet`

selects the wallet's own order rows whether the wallet was passive or aggressive.

By contrast, querying both `maker == wallet OR taker == wallet` and summing rows can double-count an aggressive trade because its counterparty maker rows coexist with the wallet's aggregate active-order row.

---

## 3. V2 exchange addresses to query

Current V2 exchanges on Polygon:

CTF Exchange V2:

`0xE111180000d2663C0091e4f400237545B87B996B`

Neg Risk CTF Exchange V2:

`0xe2222d279d744050d28e00520010520000310F59`

Daily multi-outcome Weather ladders use NegRisk heavily, so omitting `0xe222...` would destroy the Weather backfill.

SQD Portal documents public historical Polygon streaming and topic filtering:

https://portal.sqd.dev/datasets/polygon-mainnet

https://docs.sqd.ai/

---

## 4. Target-wallet topic2

Address:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

32-byte indexed topic:

`0x000000000000000000000000bddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

The same method applies to specialists such as Poligarch and ColdMath by replacing this topic only.

---

## 5. Minimal SQD query

Use the Polygon dataset stream/finalized stream and request only the relevant logs.

Conceptual request:

```json
{
  "type": "evm",
  "fromBlock": 84902353,
  "fields": {
    "block": {"number": true, "timestamp": true},
    "log": {
      "address": true,
      "topics": true,
      "data": true,
      "transactionHash": true,
      "logIndex": true
    }
  },
  "logs": [
    {
      "address": [
        "0xe111180000d2663c0091e4f400237545b87b996b",
        "0xe2222d279d744050d28e00520010520000310f59"
      ],
      "topic0": [
        "0xd543adfd945773f1a62f74f0ee55a5e3b9b1a28262980ba90b1a89f2ea84d8ee"
      ],
      "topic2": [
        "0x000000000000000000000000bddc2a7690bf600e347d5eb4a9c28f9f24e55d4f"
      ]
    }
  ]
}
```

For finalized historical research prefer the finalized stream if available. A response window can end before the requested/current height; resume at `last_block + 1` until caught up.

The block start should be verified against actual exchange deployment history when used as a production collector. Starting earlier is harmless for a filtered historical scan.

---

## 6. Exact event decode

Let the log `data` be seven consecutive 32-byte words.

Decode:

`side = uint8(word0)`

`token_id = uint256(word1)`

`maker_amount = uint256(word2) / 1e6`

`taker_amount = uint256(word3) / 1e6`

`fee = uint256(word4) / 1e6`

`builder = bytes32(word5)`

`metadata = bytes32(word6)`

From topics:

`order_hash = topic1`

`order_owner = last20bytes(topic2)`

`taker_field = last20bytes(topic3)`

Store raw integer amounts as well as normalized decimal amounts so future token/collateral decimal changes cannot corrupt evidence.

---

## 7. Maker/taker-role classifier

For a row already selected by `topic2 == wallet`:

### Aggressive / active order

If:

`taker_field == emitting_exchange_address`

then the row is the wallet's active `takerOrder` rollup.

This is the canonical row for the wallet's aggressive trade.

### Passive maker order

If `taker_field` is another user/order owner rather than the emitting exchange, then the wallet's selected row is a passive `makerOrder` fill.

This classification comes directly from V2 `Trading.sol`, not from heuristic price movement.

---

## 8. Price and cash economics

For the wallet's own order row:

### BUY (`side = 0`)

The order gives collateral and receives outcome tokens.

Raw unit price before fee:

`price = maker_amount / taker_amount`

For an aggressive BUY, the V2 source charges its order fee in collateral in addition to maker amount, so:

`all_in_cash = maker_amount + fee`

`all_in_price = (maker_amount + fee) / taker_amount`

For a passive maker BUY, platform maker fee is normally zero on current Weather markets; preserve the event fee field rather than assuming.

### SELL (`side = 1`)

The order gives outcome tokens and receives collateral.

Raw unit price:

`price = taker_amount / maker_amount`

For an aggressive SELL, fee is deducted from collateral proceeds:

`net_cash = taker_amount - fee`

`net_price = (taker_amount - fee) / maker_amount`

Do not mix the target active-order row with its same-transaction counterparty maker rows when computing wallet PnL.

---

## 9. Builder attribution is economically relevant

V2 adds `builder` and `metadata` to `OrderFilled`.

A non-zero builder can matter because builder-level fees can be additive to platform fees under Polymarket's current builder-fee system.

For every target-wallet fill, retain:

- `builder`;
- `metadata`;
- platform/event fee from the log;
- any separately attributable builder fee/rate where available.

This lets the backfill answer whether the supplied wallet's previously recovered ~1¢ Weather fee is the complete execution cost or whether some order path adds builder cost.

Official builder documentation:

https://docs.polymarket.com/developers/builders/builder-fees

---

## 10. Join graph after acquisition

The raw wallet-order stream becomes much more valuable after four small joins.

### Token -> contract/event

Use Gamma / market metadata to map:

`token_id -> condition_id -> event -> bucket -> city/date/resolver`.

Persist:

- `negRiskMarketID`;
- `negRiskFeeBips`;
- fee-enabled state;
- resolver rules;
- all outcome token ids.

### Fill -> executable market state

PMXT hourly historical market-channel Parquet begins in April 2026 and overlaps the relevant wallet period.

For each fill, reconstruct synchronized:

- pre-fill bid/ask;
- spread;
- depth;
- 5m / 30m / 2h markout;
- full ladder state.

### Fill -> forecast vintage

Open-Meteo Single Runs plus official dissemination timing provide the last available model runs.

Calculate:

- prior fair distribution `q_before`;
- newest available distribution `q_after`;
- `Δq` for the traded bucket;
- whether revision crossed a bucket boundary.

### Fill -> observations

Use resolver-station observations to reconstruct running T+0 maximum/minimum and remaining exceedance probability.

---

## 11. First decisive extractions

Once the topic2 stream is run, search in this order:

1. **Milan June 25 — 33°C**: recover every target-wallet BUY/SELL and exact exit timestamp. This is the highest-value probability-revision case.
2. **Milan June 30 — 35°C**: determine whether the known 29.38¢ BUY was later reduced after forecast mass shifted to 34°C.
3. **Mexico City July 16 — 25°C**: verify exact role/fee of the near-$1 post-midnight sale.
4. **July 12 known NegRisk tx**: use the target's own topic2 row to identify its true side/token/fee, rather than infer economic direction from counterparty rows.
5. Backfill every Weather fill and estimate PnL by city, horizon, side, role and release alignment.

---

## 12. Same method for market-maker specialists

For Poligarch / ColdMath, topic2-only history gives the same canonical own-order rows.

That enables direct measurement of:

- fraction of Weather volume that is passive maker;
- 5m/30m/2h maker markout;
- spread capture before rebates;
- directional residual inventory;
- actual taker episodes after information shocks;
- builder attribution.

Then join Polymarket's per-maker/date/condition rebate endpoint rather than estimating rebates from category totals.

The result can answer whether forecast-aware making or directional taking contributes more net dollars per capital-hour.

---

## Bottom line

The full target-wallet transaction history is no longer an access problem in principle.

The clean data path is:

`SQD V2 topic2(wallet)`

`-> exact own-order fills + maker/taker role + fee + builder`

`+ Gamma token/event metadata`

`+ PMXT historical books`

`+ point-in-time weather vintages/observations`

`-> entry/revision/exit economics and executable markouts`.

This is a materially stronger route than continuing manual PolygonScan archaeology one transaction at a time.