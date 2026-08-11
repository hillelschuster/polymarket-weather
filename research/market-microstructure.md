# Weather market microstructure

Snapshot: **2026-08-11**

Meteorology creates fair value. Microstructure determines how much of that value becomes money.

## 1. Displayed probability is not executable probability

Polymarket's displayed price is generally the bid/ask midpoint (with a last-trade fallback for wide spreads). A trader buying immediately pays the ask and a seller receives the bid.

Therefore never calculate edge from the UI probability alone.

For each signal record:

- fair probability;
- best bid/ask;
- depth to target size;
- weighted average fill price;
- taker fee;
- expected exit/settlement value.

A 10-point midpoint edge can disappear completely in a thin 8-cent spread.

## 2. Current Weather fee economics

Official Polymarket documentation currently specifies, for fee-enabled Weather markets:

`fee = shares * 0.05 * p * (1-p)`

- maker fee rate: 0;
- taker fee rate: 0.05 in the category formula;
- Weather maker-rebate allocation: 25% of collected fees;
- rebate paid from executed maker liquidity, per market;
- `feesEnabled` and the current market fee parameters should be queried per market.

The fee curve peaks near 50¢ and is smaller in the tails. That means a fixed “minimum edge” is mathematically wrong: the required raw edge depends on price, spread, depth, and route.

## 3. Maker alpha is potentially first-class

If our weather fair value is superior, crossing the spread is not automatically the best monetization.

Approximate maker PnL per fill:

`fair-value edge + spread capture + rebate - adverse selection`

Weather gives unusually explicit adverse-selection clocks:

- scheduled model cycles;
- METAR updates;
- radar/nowcast shocks;
- local peak-temperature window.

A generic market maker centered on the current midpoint can be systematically picked off by a weather specialist. Conversely, a weather-informed maker can pull or skew quotes before those catalysts and quote more aggressively during quiet periods.

Polymarket publishes a current maker-rebate endpoint by maker address/date, which may help verify whether tracked wallets are receiving rebates.

## 4. Negative-risk ladders are one market, economically

Daily temperature buckets are mutually exclusive and usually exhaustive. In negative-risk events, Polymarket explicitly allows one NO share in outcome `i` to convert into one YES share in every other outcome.

This makes the natural trading object the entire ladder.

Monitor:

- all YES asks and bids;
- all NO asks and bids;
- sum of executable YES prices;
- NO_i versus other-YES basket;
- depth at each leg;
- fees on each route;
- conversion/mint/merge mechanics.

The weather model should output the same object: one probability vector summing to 1.

## 5. Cross-bucket statistical relative value

Even when there is no locked arbitrage, the ladder can be internally implausible.

Example shape constraints for a temperature distribution:

- probabilities should usually form a locally smooth/unimodal-ish mass function absent a genuinely bimodal weather regime;
- cumulative probabilities must be monotone;
- tail probabilities implied by adjacent thresholds should be coherent;
- the full vector must sum to one.

Fit an arbitrage-free market-implied distribution to executable quotes, then compare it with our calibrated weather CDF. This separates:

- `market structure error` — prices inconsistent with one another;
- `forecast disagreement` — internally coherent market distribution differs from weather model.

Both can make money, but execution differs.

## 6. On-chain maker/taker attribution is subtle

Polymarket CLOB matching is off-chain and settlement is on-chain. The current CTF Exchange V2 supports complementary, mint, and merge settlement paths. In complex negative-risk matches the exchange itself can appear as the counterparty in emitted events while multiple signed orders settle atomically.

This matters for wallet research. A naive rule like “the address in one `maker` event field is always a passive market maker” is not safe without reconstructing the matching path.

Concrete example from the user-supplied `0xbddc...55d4f` account:

- a June 29 Milan 35°C transaction is rendered by PolygonScan as the wallet buying 102.116 YES shares for $30;
- the transaction contains multiple negative-risk V2 fills and the wallet appears in order-event fields inside that aggregate settlement;
- another July 12 batch shows the same wallet as the explicit taker against several makers, while also containing a later fill where the wallet is an order maker and the exchange contract is the emitted taker.

Conclusion: reconstruct each signed order/match rather than classifying an account from a single log line.

## 7. Historical quote lifecycle is not fully recoverable on-chain

Because order placement/cancellation occurs off-chain, blockchain fills do not reveal every resting order or cancellation. Recent research on Polymarket microstructure explicitly flags this as a limitation for address-level market-maker classification.

What can still be measured reliably:

- executed fills;
- signed-side/fill-side information where contracts expose it;
- turnover;
- holding periods from position changes;
- repeated two-sided executions;
- markouts after fills;
- current/historical rebate evidence where endpoint coverage permits.

Going forward, our own WebSocket collector can capture the public book lifecycle at market level even though it cannot assign every quote to a wallet.

## 8. Queue/fill value

For a maker order at price `l`, the order has value only if it fills before fair value moves away.

Useful empirical statistic:

`markout_tau = side * (fair_or_mid_at_t+tau - fill_price)`

for `tau = 10s, 1m, 5m, 30m`.

If fills just before forecast shocks have strongly negative markouts, the maker needs catalyst-aware quote withdrawal. If quiet-period fills have positive markouts plus rebate, market making may monetize smaller forecast edges that are not worth crossing for.

## 9. Capacity is an order-book integral

For a candidate YES trade with fair value `q`, define the maximum profitable size by walking asks until:

`marginal_ask + marginal_fee >= q`

Expected dollar edge is the integral/sum over profitable levels, not `edge * arbitrary_size`.

Do the same across every bucket. This will reveal whether the highest-percentage opportunities are too tiny to matter and which cities support scalable PnL.

## 10. Public market-maker code is implementation reference, not strategy truth

Polymarket's archived official `poly-market-maker` demonstrates basic quote synchronization around midpoint. More recent public bots add inventory-aware quoting and toxicity logic. These are useful execution references, but our competitive difference should be the weather fair value and catalyst clock, not a generic market-making framework.

## Primary references

- Polymarket fees: https://docs.polymarket.com/trading/fees
- Maker rebates: https://docs.polymarket.com/market-makers/maker-rebates
- Current rebate endpoint: https://docs.polymarket.com/api-reference/rebates/get-current-rebated-fees-for-a-maker
- Orderbook: https://docs.polymarket.com/trading/orderbook
- Market WebSocket: https://docs.polymarket.com/market-data/websocket/market-channel
- Negative risk: https://docs.polymarket.com/advanced/neg-risk
- CTF Exchange V2: https://github.com/Polymarket/ctf-exchange-v2
- Archived CTF Exchange matching overview: https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md
- Polymarket-v1 Database paper: https://arxiv.org/abs/2606.04217
- Fill-side non-retail microstructure paper: https://arxiv.org/abs/2605.11640
