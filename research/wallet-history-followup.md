# Supplied wallet history — second acquisition pass

Snapshot: **2026-08-11**

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

This file extends [`wallet-history-acquisition.md`](wallet-history-acquisition.md) with additional indexed history recovered after the first transaction-level pass.

The purpose is narrow: determine whether the visible exact-bucket strategy is static buy-and-hold or an actively revised forecasting strategy, and identify the best route to a much larger historical sample.

---

# 1. Milan June 30: the recovered T+1 35°C buy ultimately missed

Previously recovered transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

Verified entry:

- market: **Milan June 30 — 35°C YES**;
- timestamp: **2026-06-29 01:55:11 UTC** / 03:55:11 Rome;
- shares: **102.116**;
- base consideration: **$30.00**;
- raw price: **29.38¢**;
- fee: **$1.05932**;
- all-in cost: **30.42¢ per share**.

Polymarket's resolved June 30 event shows:

- **34°C = YES / 100%**;
- **35°C = NO**.

Source:
https://polymarket.com/event/highest-temperature-in-milan-on-june-30-2026

Therefore the 35°C position would have lost if the wallet simply held these shares through resolution.

## What this tells us

This is useful because it removes a misleading interpretation of the wallet as a near-perfect modal oracle.

The strategy is probabilistic. A next-day 35°C view around 30¢ can be a rational positive-EV trade and still lose. The important unknown is whether the wallet subsequently **reduced or exited** when later forecast information moved the distribution toward 34°C.

The next reconstruction target for this token is therefore all later SELLs or conversions involving:

`47809137889791405662099861602793364077088639904534506506807768466233401292978`

If a sell appears materially above zero after a forecast shift, the correct PnL is the actual trade path, not a synthetic full loss.

## Forecast context

Polymarket's archived market context from June 28 described ECMWF/GFS consensus near **34–35°C**. Treat that context only as descriptive evidence of the market's information environment, not as an authoritative historical forecast archive.

The 35°C purchase therefore appears close to the plausible forecast mode/adjacent mode rather than a penny-tail bet.

---

# 2. Milan June 25: indexed evidence of a large exact-bucket SELL

Struct's public Explorer indexed a trade by the supplied wallet in:

**“Will the highest temperature in Milan be 33°C on June 25?”**

Indexed trade row:

- trader: supplied wallet;
- outcome expression: **YES**;
- price: approximately **10.9¢**;
- share change: **-193.78 shares**;
- value: approximately **$21.1**.

Source:
https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

A negative share change on Struct's trade table represents selling/reducing that YES position.

The event ultimately resolved:

- **35°C = YES**;
- 33°C = NO;
- 34°C = NO;
- 36°C = NO.

Resolved 35°C market:
https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-35c

Resolved 33°C market:
https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

## Economic inference

This is the strongest new behavioral clue from the second pass.

The wallet did **not** simply hold every exact-bucket forecast until settlement. It sold 193.78 shares of a bucket that ultimately lost while the YES price was around 10.9¢.

We have not yet recovered the earlier BUY(s), exact transaction hash, or exact sell timestamp from the indexed snippet, so we cannot calculate realized PnL on the 33°C position yet.

But the observation is consistent with an **active probability-revision strategy**:

1. establish exact-bucket exposure when the distribution favors it;
2. update as new model/observation information arrives;
3. sell a bucket whose posterior probability collapses instead of mechanically holding to zero.

That is a materially different strategy from the simplistic public bots that buy one forecast bucket and wait.

### Highest-value missing link

Recover the earlier acquisition history for Milan June 25 33°C and align the 193.78-share sell with:

- ECMWF cycle changes;
- ICON-2I / AROME / other European high-resolution guidance;
- LIMC observations;
- movement in the neighboring 34°C / 35°C ladder.

If the exit occurs soon after the distribution shifts from 33°C toward 35°C, this becomes direct evidence of **forecast-revision trading**, not merely position liquidation.

---

# 3. Specialist overlap: supplied wallet and Poligarch in the same matched transaction

The previously recovered July 12 neg-risk transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

contains the supplied wallet as the aggregate taker-order maker and includes multiple matched counterparties.

One counterparty is:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

which is the public wallet **Poligarch**, independently identified as one of Polymarket's largest WEATHER-volume and profitable daily-temperature specialists.

This does not mean they necessarily held opposite weather forecasts. Negative-risk matching can pair economically equivalent YES/NO basket expressions. The useful result is narrower:

> **top weather-specialist order flow directly intersects in the same neg-risk matching process.**

That makes a specialist interaction graph worth measuring once the full fill dataset is available.

Candidate variables:

`wallet_A`
`wallet_B`
`condition_id`
`timestamp`
`token_expression`
`economic_direction_after_neg_risk_normalization`
`5m_markout`
`30m_markout`
`settlement_result`

The point is to test whether some specialists consistently lead other specialists or whether counterparties represent distinct strategy archetypes.

---

# 4. Another independent profitability snapshot

An indexed Polymarket WEATHER daily-profit leaderboard snapshot from late July showed the supplied wallet ranked **#7 for the day at approximately +$1,548**.

This is a dated snapshot, not a lifetime realized-PnL number. It matters because it independently confirms that the account's visible August profitability was not the only profitable daily window indexed during the research period.

Source:
https://polymarket.com/leaderboard/weather/today/profit

The leaderboard's crawl date and underlying “today” window must be recorded whenever it is used; do not combine daily snapshots as if they were independent lifetime PnL.

---

# 5. Struct is the best secondary history source found so far

Polymarket's official Data API remains the preferred source because it is public and directly joins fills to market metadata.

Struct adds several fields and derived PnL objects that can substantially reduce reconstruction work.

Official Struct endpoint:

`GET /v1/polymarket/trader/trades/{address}`

Struct documents cursor pagination and trader-level trade retrieval. Its market-trades schema includes:

- transaction hash;
- trader;
- side;
- token/position ID;
- USD amount;
- shares;
- price;
- exchange;
- trade type;
- block/log indices;
- order hash;
- taker;
- condition ID;
- outcome;
- question;
- market/event slug;
- probability;
- fee and fee percentage;
- builder attribution.

Docs:
https://docs.struct.to/api-reference/market/get-market-trades

## Per-position lifetime PnL

Most valuable Struct endpoint found:

`GET /v1/polymarket/trader/pnl/{address}/positions`

It returns one row per outcome token with:

- `won`;
- total buys/sells;
- shares bought/sold;
- USD bought/sold;
- redemption payout;
- average entry price;
- average exit price;
- **realized PnL**;
- **total fees**;
- first and last trade timestamps;
- current balance/value.

It can filter `status=open|closed`, `won=true|false`, search by title, sort by realized PnL or activity and paginate.

Docs:
https://docs.struct.to/api-reference/trader/get-trader-position-pnl

This endpoint is nearly the ideal first-pass wallet-decomposition dataset because it directly answers:

> Which weather outcomes did this wallet actually make or lose money on, after its complete sequence of buys, sells and redemptions?

## Daily PnL history

`GET /v1/polymarket/trader/pnl/{address}/calendar`

returns realized PnL per active trading day and paginates backward in 30-day windows.

Docs:
https://docs.struct.to/api-reference/trader/get-trader-pnl-calendar

## Time-series activity intensity

`GET /v1/polymarket/trader/volume-chart/{address}`

returns buy volume, sell volume and buy/sell trade counts over intervals as small as one minute.

Docs:
https://docs.struct.to/api-reference/trader/get-trader-volume-chart

This is valuable for release-latency work because activity bursts can be aligned with model update clocks even before every trade is weather-enriched.

## Authentication

Struct's API examples use an `X-API-Key`. The public Explorer exposes indexed market views without that key, which is how the Milan June 25 sell was recovered here. A full direct Struct backfill would require API access.

---

# 6. What the partial history now says about strategy structure

The evidence is no longer consistent with a single simplistic rule.

## Observed component A — T+1 exact-bucket entry

Milan June 30 35°C:

- bought around 29.4¢ raw / 30.4¢ all-in;
- roughly one day before event peak;
- outcome ultimately lost.

Interpretation: **probabilistic forward forecasting**.

## Observed component B — active losing-bucket reduction

Milan June 25 33°C:

- sold 193.78 YES around 10.9¢;
- bucket ultimately lost;
- neighboring 35°C ultimately won.

Interpretation: likely **posterior updating / exit logic**, pending acquisition of entry and exact timing.

## Observed component C — near-certain winner recycling

Mexico City July 16 25°C:

- winning YES sold at effectively ~99.895¢ net;
- only five minutes after local civil day end.

Interpretation: **capital-turnover optimization**.

## Observed component D — specialist liquidity interaction

July 12 neg-risk match includes both supplied wallet and Poligarch.

Interpretation: weather-specialist flow is sufficiently concentrated that cross-wallet interaction itself may be informative.

### Working composite model

The strongest current hypothesis is not “wallet predicts exact temperatures.” It is:

> **maintain an internal probability distribution over the resolver ladder, enter when a bucket is materially underpriced, revise that distribution when fresh weather information arrives, exit collapsing buckets, recycle locked winners, and repeat across many cities.**

That is a much richer and more plausible profitable strategy than static point-forecast betting.

---

# 7. Best next acquisition order

For maximum information per API row:

1. **Struct position-PnL endpoint** for all closed weather positions — gives complete economic outcome immediately;
2. official Polymarket `/trades` — recovers exact individual fill timestamps and transaction hashes;
3. Struct trader trades — adds fees, order/taker/builder fields and easier pagination;
4. official `/activity` — captures split/merge/conversion/redeem flows;
5. price history / Struct market trades — calculate markouts;
6. point-in-time weather vintages — explain the fills.

The priority is to turn a few compelling examples into a statistically meaningful table of:

`city × horizon × bucket_type × entry_price × entry_time × exit_time × outcome × realized_pnl × fee × forecast_release_alignment`.

That table is the shortest path from wallet curiosity to replicable alpha.