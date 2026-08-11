# Supplied wallet — recovered transaction history and acquisition path

Snapshot: **2026-08-11**

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

This note records fill-level history recovered from public indexed Polygon / Polymarket data for the supplied weather trader. It distinguishes **verified transaction facts** from **strategy inference** and from **unresolved mapping**.

The important result is that the wallet can be studied below the profile-position level. We recovered exact timestamps, token IDs, cash flows, share quantities, fees and transaction hashes for several fills.

---

# 1. Verified fill: Milan T+1 exact-bucket BUY

Transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

PolygonScan's indexed Polymarket action identifies this as:

> Bought **102.116 YES shares for $30.00** in **“Will the highest temperature in Milan be 35°C on June 30?”**

Timestamp:

- **2026-06-29 01:55:11 UTC**
- **2026-06-29 03:55:11 Europe/Rome**

Token ID:

`47809137889791405662099861602793364077088639904534506506807768466233401292978`

Fill accounting recovered from the Neg Risk CTF Exchange transaction:

- base trade consideration: **30.000000 pUSD**
- shares received: **102.116**
- raw share price: `30 / 102.116 = 0.29378`
- fee paid from wallet cash flow: **1.05932 pUSD**
- total wallet cash outflow: **31.05932 pUSD**
- fee as percentage of base consideration: **3.53%**
- **effective all-in cost per share: `31.05932 / 102.116 = 0.30416`**

So fees moved the economic break-even probability from about **29.38% raw to 30.42% all-in**, a roughly **1.04 percentage-point** hurdle before spread/markout considerations.

The fee magnitude is consistent with the current fee-enabled Weather functional form:

`shares × 0.05 × p × (1-p)`

## Economic significance

This is not a late T+0 certainty trade. The wallet bought an exact Milan bucket early on June 29 for the June 30 event, roughly a day-plus before the expected June 30 afternoon temperature peak.

That establishes a strategy component beyond same-day observation collapse:

> **The wallet takes next-day exact-bucket exposure while accepting roughly a full probability point of fee hurdle when its forecast view is strong enough.**

This is much more consistent with a forecast-distribution edge or forecast-release edge than with tiny price discrepancies.

---

# 2. Verified fill: Mexico City winning-bucket SELL immediately after local day end

Transaction:

`0xc9168bbf496f29f9590b5c56ab21320c6a67b5106736e416a4193c82b5304542`

PolygonScan's indexed action identifies this as:

> Sold **38 YES shares for $37.96** in **“Will the highest temperature in Mexico City be 25°C on July 16?”**

Timestamp:

- **2026-07-17 06:05:00 UTC**
- **2026-07-17 00:05:00 America/Mexico_City**

Token ID:

`78463043936379448001218148344987221684539232060665353644187692737062767330037`

Fill accounting:

- shares sold: **38**
- gross consideration: **37.962 pUSD**
- raw execution price: **0.999 per share**
- fee: **0.00189 pUSD**
- wallet net proceeds: **37.96011 pUSD**
- **net realized exit price: `37.96011 / 38 = 0.99895` per share**

## Economic significance

The wallet sold at effectively 99.895¢ only **five minutes after the Mexico City local civil day ended**.

That is strong behavioral evidence for **capital recycling / settlement-latency monetization**:

- once the daily-high state was effectively locked, remaining payoff to formal $1 settlement was only about 0.105¢ per share;
- the fee at ~99.9¢ was negligible because `p(1-p)` is tiny near 1;
- selling releases capital immediately for the next weather slate.

The economically correct comparison is:

`value of waiting for the final ~0.105¢` versus `expected return from redeploying the released cash during the settlement/redemption delay`.

For a high-turnover weather specialist, recycling can rationally dominate holding a near-certain winner to redemption.

---

# 3. Verified fill: July 12 exact-outcome BUY, market title not yet mapped

Transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

Timestamp:

- **2026-07-12 13:16:32 UTC**

The Neg Risk CTF Exchange transaction identifies the supplied wallet as the `takerOrderMaker` in the aggregate `OrdersMatched` record. The wallet's cash flow and matched token quantity give:

- side: **0**
- token ID: `91076181803621459956200090324917139595424901620108017335569536029558392706177`
- base consideration: **44.274 pUSD**
- shares acquired: **166.68**
- raw execution price: `44.274 / 166.68 = 0.26562`
- fee paid from wallet cash flow: **1.62569 pUSD**
- total wallet cash outflow: **45.89969 pUSD**
- fee as percentage of base consideration: **3.67%**
- **effective all-in cost per share: `45.89969 / 166.68 = 0.27538`**

The fee therefore raised the economic break-even probability from about **26.56% to 27.54%**, roughly a **0.98 percentage-point** hurdle.

Associated condition ID recovered from the transaction:

`0x1cbcd7f27f60388d43a9d3f1d5e7ed7d3cd31d1076c990a73ae48e644ef1f491`

The paired neg-risk token is:

`2655055245387824275985181109206555608704123016388750340070226258019209549699`

## Matched specialist counterparty

The same transaction contains multiple counterparties. One is:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

which is the public wallet previously identified as **Poligarch**, a top WEATHER PnL / high-volume daily-temperature specialist.

This is verified transaction-level co-participation in the same neg-risk match. It does **not** by itself prove that the two wallets held opposite meteorological forecasts: neg-risk matching can express economically equivalent YES/NO baskets through conversions. But it is valuable evidence that major weather specialists directly interact in the same liquidity pool.

## Mapping status

**Market title / city remains unresolved from the indexed sources inspected.**

Do not attach a city or weather question to this token until the condition/token is mapped through Polymarket's market metadata.

The official CLOB now documents:

`GET /markets-by-token/{token_id}`

which resolves a token ID to its condition ID and paired token IDs. Gamma/CLOB market metadata can then attach the market question. Direct dynamic access to that exact token URL was unavailable in the present research environment, so the title remains deliberately unmapped.

## Economic significance even without title

The transaction independently confirms the same behavior as Milan:

- intermediate-probability outcome around **26.6¢ raw / 27.5¢ all-in**;
- meaningful share size;
- roughly one percentage point of absolute fee hurdle;
- matched execution rather than relying exclusively on free passive fills.

---

# 4. What the recovered transactions change about the wallet thesis

Before fill recovery, the modal-bucket hypothesis came mainly from the current-position profile snapshot.

After fill recovery, we have transaction-level support for four behaviors.

## A. Next-day exact-bucket forecasting is real

The Milan transaction proves the wallet takes exact-bucket exposure substantially before same-day certainty collapse.

This makes **T+1 forecast calibration and forecast-release timing** first-class research targets.

## B. The wallet accepts meaningful execution cost

The two recovered BUYs around 26–29¢ incurred about **0.98–1.04 percentage points of additional all-in probability hurdle** from fees alone.

That is a better economic framing than saying the fee is 3.5–3.7% of notional. The strategy needs fair probability above roughly 27.54% and 30.42%, respectively, merely to break even at settlement before any additional spread/slippage effect.

Repeated trades of this form imply either:

1. materially higher internal fair probabilities;
2. positive short-horizon expected markout large enough to justify urgency;
3. high value placed on acquiring the desired position before repricing;
4. a combination of the above.

## C. At least some flow is aggressive/information-taking

The July 12 aggregate match explicitly names the supplied wallet as the taker-order maker, and the recovered BUYs incur the fee-bearing cash flow expected from active execution.

This supports an **information-taking** component rather than a pure passive market-making strategy.

Full-history role classification is still needed before estimating the wallet's overall maker/taker mix.

## D. It actively recycles near-settled winners

The Mexico City sell at effectively 99.895¢ five minutes after local midnight implies turnover economics matter.

A useful model variable is:

`redeployment edge = expected next-opportunity return during settlement delay - discount_to_$1 - exit_fee`

If positive, recycling is economically superior to waiting.

---

# 5. Public Polymarket API acquisition path

Polymarket's **Gamma API and Data API are fully public and require no authentication**. The current limitation in this research session is access to arbitrary parameterized dynamic URLs, not a Polymarket permission requirement.

## Trades

Request shape:

`GET https://data-api.polymarket.com/trades?user=<wallet>&limit=10000&offset=0`

The public trades response includes:

- proxy wallet;
- BUY/SELL side;
- asset/token ID;
- condition ID;
- size;
- price;
- timestamp;
- title;
- market/event slug;
- outcome/index;
- transaction hash.

Documented limits:

- `limit <= 10000`
- `offset <= 10000`

This is the best first extraction route because it already joins blockchain fills to Polymarket market metadata.

## Current positions

`GET https://data-api.polymarket.com/positions?user=<wallet>&limit=500`

Useful fields include size, average price, initial/current value, cash PnL, realized PnL, token IDs, market title, outcome and negative-risk state.

## Closed positions

`GET https://data-api.polymarket.com/closed-positions?user=<wallet>&limit=50&offset=<n>&sortBy=TIMESTAMP&sortDirection=DESC`

Documented closed-position pagination permits offsets up to **100,000**. It directly exposes `avgPrice`, `totalBought`, `realizedPnl`, timestamp, title and outcome.

This is likely the fastest source for historical strategy decomposition by city/horizon before reconstructing every individual fill.

## Activity

`GET https://data-api.polymarket.com/activity?user=<wallet>&limit=500&offset=<n>`

Activity supports filters for:

- `TRADE`
- `SPLIT`
- `MERGE`
- `REDEEM`
- `REWARD`
- `CONVERSION`
- `MAKER_REBATE`
- `REFERRAL_REWARD`

This matters because a neg-risk trader's economic history cannot always be inferred correctly from simple token transfers. Splits, merges and conversions explain how multi-outcome expressions are created or transformed.

## Accounting snapshot

`GET https://data-api.polymarket.com/v1/accounting/snapshot?user=<wallet>`

The documented response is a ZIP containing:

- `positions.csv`
- `equity.csv`

This is useful for reconciling reconstructed fills to account-level state.

## Token / market mapping

Official endpoint:

`GET https://clob.polymarket.com/markets-by-token/{token_id}`

It returns the parent condition ID and primary/secondary token IDs.

Then use CLOB/Gamma market metadata to attach:

- question/title;
- city;
- event date;
- bucket;
- resolver rules;
- negative-risk grouping.

## Historical price markout

The public CLOB exposes `GET /prices-history` for token price history. Once fills are acquired, this enables 5m/30m/2h markout without needing authenticated wallet data.

---

# 6. Practical complete-history acquisition sequence

The smallest useful extraction sequence is:

1. pull `/trades` for fill-level history;
2. pull `/closed-positions` through all pages for realized-PnL reconciliation;
3. pull `/activity` for split/merge/conversion/redeem events;
4. pull `/positions` and accounting snapshot for current-state reconciliation;
5. map any on-chain-only token IDs using `/markets-by-token/{token_id}`;
6. deduplicate economic fills by transaction hash + asset + side + timestamp + size;
7. enrich weather contracts with exact resolver station/rules and local timestamps;
8. enrich each fill with point-in-time forecast/observation state and CLOB price markout.

No trading framework is needed for this. The output can be compact tables/CSV/SQLite used directly for research.

---

# 7. Full-history reconstruction schema

One row per economic fill:

`wallet`
`tx_hash`
`timestamp_utc`
`timestamp_resolver_local`
`market_title`
`event_slug`
`condition_id`
`token_id`
`city`
`resolver_station`
`event_date`
`horizon_hours_to_peak`
`side`
`outcome_expression`
`bucket`
`shares`
`base_consideration`
`fee`
`effective_cash`
`raw_price`
`effective_price`
`maker_taker_role`
`final_outcome`
`realized_pnl`

Point-in-time enrichment:

`latest_observation`
`observed_running_high_or_low`
`latest_forecast_vintage`
`previous_forecast_vintage`
`forecast_revision`
`our_fair_probability`
`market_bid`
`market_ask`
`5m_markout`
`30m_markout`
`2h_markout`

---

# 8. Highest-value tests once more fills are recovered

## T+1 release alignment

For every next-day BUY, calculate minutes since:

- ECMWF new cycle availability;
- high-resolution local-model update;
- NBM/LAMP update for US cities;
- national meteorological-service run where available.

If entries cluster tightly after a particular feed, that feed becomes a likely source of wallet alpha.

## T+0 observation alignment

For same-day fills, calculate:

- minutes after latest METAR/SPECI/official station observation;
- distance of running maximum from bucket boundaries;
- forecast probability of another boundary crossing;
- minutes to forecast/climatological peak.

## Fee-adjusted implied conviction

For each BUY, use **all-in cost per share**, not displayed raw trade price, as the settlement break-even probability.

The two recovered BUYs already show roughly a one-point absolute difference between raw price and economic cost.

## Short-horizon information markout

For every fill:

`markout_τ = signed_side × (price_{t+τ} - entry_price)`

at 5m, 30m and 2h.

Positive markout plus positive settlement alpha implies genuine fast information. Positive settlement alpha with weak markout suggests slower fundamental forecasting edge.

## Exit / capital-recycling policy

For near-1 exits, compute:

- expected time until redemption;
- discount to $1;
- exit fee;
- next trade entry time;
- realized return on redeployed cash.

The Mexico City transaction makes this a real strategy question rather than bookkeeping.

## Specialist interaction graph

The July 12 Poligarch co-match suggests another dataset:

`wallet A × wallet B × market × timestamp × economic side`

Test whether top specialists tend to:

- agree through differently expressed neg-risk positions;
- trade against each other at forecast regime changes;
- lead/follow one another in time;
- cluster around the same model/observation releases.

---

# 9. Current evidence grade

## Verified

- Milan BUY: exact market, timestamp, 102.116 shares, cash outflow, token and fee-bearing all-in cost;
- Mexico City SELL: exact market, timestamp, 38 shares, gross/net proceeds, token and near-$1 exit price;
- July 12 BUY: exact transaction accounting, token/condition IDs and multiple counterparties;
- Poligarch wallet participated as a counterparty in that same July 12 neg-risk transaction;
- Polymarket's public API officially supports trades, current positions, closed positions, activity, accounting snapshots and token-to-market resolution.

## Inference

- exact/modally concentrated forecasting appears to be a core behavior;
- T+1 forecast information matters, not only T+0 observations;
- the wallet sometimes pays roughly a full probability point of fee hurdle for immediate position acquisition;
- near-settlement capital recycling appears intentional;
- interaction among specialist wallets may itself contain information.

## Unresolved

- complete wallet fill history;
- exact market mapping of the July 12 token;
- full maker/taker mix;
- which forecast source drives T+1 entries;
- whether T+0 entries systematically follow observation updates;
- price-controlled realized alpha over the full sample.

The next useful increment is more raw history and resolver/forecast alignment, not more qualitative speculation.