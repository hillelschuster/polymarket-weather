# Minimal data reconstruction — enough public API data to measure the edge

Snapshot: **2026-08-11**

This note defines the smallest historical dataset required to answer the profitable questions before implementing a trading strategy.

The useful result from the API research is that Polymarket already exposes nearly everything required for the first-pass wallet and market study. A custom historical exchange-data platform is unnecessary.

---

# 1. Wallet fills — official Data API

Official endpoint:

`GET https://data-api.polymarket.com/trades`

Wallet filter:

`?user=<proxy_wallet>`

Documented response fields include:

- `proxyWallet`;
- `side`;
- `asset` / token ID;
- `conditionId`;
- `size`;
- `price`;
- `timestamp`;
- `title`;
- `slug`;
- `eventSlug`;
- `outcome`;
- `outcomeIndex`;
- `transactionHash`.

Documented request limits:

- `limit` up to **10,000**;
- `offset` up to **10,000**.

Official docs:

https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets

For the supplied wallet, this is the preferred raw history source:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

One row per returned fill is sufficient initially.

---

# 2. Current and closed economic positions

Official current positions:

`GET https://data-api.polymarket.com/positions?user=<wallet>`

Fields include:

- size;
- average price;
- initial/current value;
- cash PnL;
- realized PnL;
- total bought;
- current price;
- title/slug/outcome;
- opposite token;
- negative-risk status.

Docs:

https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user

Use closed positions / market-position endpoints for realized economic outcome and reconciliation.

The official market-position endpoint can sort a wallet/market by realized or total PnL and includes both open and closed states:

`GET https://data-api.polymarket.com/v1/market-positions`

Docs:

https://docs.polymarket.com/api-reference/core/get-positions-for-a-market

The purpose is to avoid treating every BUY as a held-to-settlement bet when the wallet later sells or converts it.

---

# 3. Token → market mapping

If the trade row already contains title/slug/condition ID, no extra lookup is needed.

For token IDs recovered from Polygon logs or other sources, official CLOB endpoint:

`GET https://clob.polymarket.com/markets-by-token/{token_id}`

returns:

- condition ID;
- primary/YES token;
- secondary/NO token.

Docs:

https://docs.polymarket.com/api-reference/markets/get-market-by-token

Then Gamma market/event metadata attaches rules, description, dates, resolver and outcomes.

Gamma market list / market by ID:

https://docs.polymarket.com/api-reference/markets/list-markets

https://docs.polymarket.com/api-reference/markets/get-market-by-id

---

# 4. Historical price markout — official CLOB price history

Official endpoint:

`GET https://clob.polymarket.com/prices-history`

Parameters:

- `market` — despite the name, this is the **asset/token ID**;
- `startTs`;
- `endTs`;
- `interval`;
- `fidelity` in minutes, default 1.

Docs:

https://docs.polymarket.com/api-reference/markets/get-prices-history

This is enough to calculate for every wallet fill:

`markout_5m`

`markout_30m`

`markout_2h`

`markout_6h`

without maintaining our own historical price service.

For up to 20 tokens at once:

`POST https://clob.polymarket.com/batch-prices-history`

Docs:

https://docs.polymarket.com/api-reference/markets/get-batch-prices-history

### Important limitation

Historical token price is not historical full bid/ask depth.

That does **not** prevent the first wallet-information study. We already know the wallet's actual fill price. The question is whether price subsequently moved in the same direction.

For future production-fidelity execution studies, start recording live books ourselves from the point research begins.

---

# 5. Live executable price and depth

Official current book endpoint:

`GET https://clob.polymarket.com/book?token_id=<asset>`

Response includes:

- all visible bids and asks;
- size at each level;
- timestamp;
- tick size;
- minimum order size;
- neg-risk flag;
- last trade price.

Docs:

https://docs.polymarket.com/api-reference/market-data/get-order-book

Batch books are also available.

For a simple eventual trader, executable acquisition cost can be calculated directly by walking the real ask levels rather than fitting a slippage model.

---

# 6. Live capture from WebSocket

Public market channel:

`wss://ws-subscriptions-clob.polymarket.com/ws/market`

It supplies:

- full book snapshots;
- price-level changes;
- last trades;
- best bid/ask with custom feature enabled;
- new market events;
- resolution events.

Docs:

https://docs.polymarket.com/market-data/websocket/market-channel

This means historical depth can simply begin accumulating when the research collector is eventually written; no separate provider is required to start.

---

# 7. Minimal wallet-alpha reconstruction

For each wallet fill `j`:

## Trade fields

`wallet`
`timestamp`
`token_id`
`condition_id`
`side`
`outcome`
`size`
`price`
`transaction_hash`

## Derived market fields

`city`
`event_date`
`bucket`
`resolver_station`
`unit`
`T+0/T+1/T+2`

## Derived price response

For BUY:

`markout_tau = price(t+tau) - fill_price`

For SELL:

`markout_tau = fill_price - price(t+tau)`

Evaluate at:

- 5 minutes;
- 30 minutes;
- 2 hours;
- 6 hours;
- settlement.

A wallet with persistent positive short-horizon markout possesses timing/information alpha even before considering final resolution.

A wallet with weak short markout but positive settlement alpha has forecast accuracy without exceptional speed.

A wallet with positive short markout and positive settlement alpha is the most valuable model to reverse-engineer.

---

# 8. Information-event alignment

For every fill, add only the weather timestamps that can explain it:

`latest_authoritative_observation_available_at_fill`

`latest_model_run_available_at_fill`

`previous_model_run`

`minutes_since_new_run`

`forecast_daily_max_old`

`forecast_daily_max_new`

`running_observed_max`

Then classify fills into:

- observation reaction;
- forecast-run reaction;
- no obvious new information;
- capital-recycling exit.

The causal question is whether markout is strongest within a repeatable number of minutes after a particular information source.

---

# 9. A minimal dataset can answer the highest-value questions

## Is the supplied wallet worth following?

Measure price-controlled settlement alpha and markout.

## Is it fast or just accurate?

Compare short-horizon markout with final outcome performance.

## Which model/source matters?

Regress/classify markout against minutes since model/observation update.

## Which cities are strongest?

Aggregate net performance by resolver station.

## Which horizon is strongest?

T+0 versus T+1 versus T+2.

## Which entry prices are strongest?

Bin by executable price.

## Does size encode confidence?

Compare the wallet's round-dollar position tier with later markout and realized PnL.

## Does specialist consensus add information?

Join fills from other skilled wallets on the same token/event and compare incremental markout.

No broader dataset is needed to answer these first.

---

# 10. Minimal live market recording once research code begins

Only record changes relevant to later execution analysis:

`timestamp, token_id, best_bid, best_ask, bid_depth_top_N, ask_depth_top_N, last_trade`

This supports:

- spread cost;
- fillable notional;
- book-walking price;
- post-signal markout;
- maker/taker comparisons.

There is no need to reproduce a full exchange matching engine.

---

# 11. Why this matters economically

The previous uncertainty was that obtaining enough historical Polymarket data might require substantial infrastructure.

It does not.

For the highest-value research decision, the minimum chain is:

`Data API wallet fills`

`→ token / condition metadata`

`→ CLOB minute price history`

`→ resolver outcome`

`→ forecast/observation timestamps`

That is sufficient to determine whether the observed specialists have repeatable information advantage, where it comes from, and how quickly it decays.

The eventual data collector can therefore remain very small and still answer the money question.
