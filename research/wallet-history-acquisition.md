# Supplied wallet — recovered transaction history and acquisition path

Snapshot: **2026-08-11**

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

This note records fill-level history recovered from public indexed Polygon / Polymarket data for the supplied weather trader. It distinguishes **verified transaction facts** from **strategy inference** and from **unresolved mapping**.

The most important result is that the wallet can be studied below the profile-position level. We recovered exact timestamps, token IDs, USDC amounts, share quantities, fees and transaction hashes for several fills.

---

# 1. Verified fill: Milan T+1 exact-bucket BUY

Transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

Indexed Polymarket action:

> Bought **102.116 YES shares for $30.00** in **“Will the highest temperature in Milan be 35°C on June 30?”**

Timestamp:

- **2026-06-29 01:55:11 UTC**
- **2026-06-29 03:55:11 Europe/Rome**

Token ID:

`47809137889791405662099861602793364077088639904534506506807768466233401292978`

Fill accounting recovered from the Neg Risk CTF Exchange logs:

- base trade consideration / maker amount filled: **30.000000 pUSD**
- shares received / taker amount filled: **102.116**
- raw share price: `30 / 102.116 = 0.29379`
- fee: **1.05932 pUSD**
- total wallet cash outflow: **31.05932 pUSD**
- fee as percentage of base consideration: **3.53%**

The fee matches the current fee-enabled Weather functional form closely:

`shares × 0.05 × p × (1-p)`

## Economic significance

This is a particularly useful observation because it is **not a late T+0 certainty trade**. The wallet bought an exact Milan bucket early on June 29 for the June 30 event, roughly a day-plus before the expected June 30 afternoon temperature peak.

That directly supports a second strategy component beyond same-day observation collapse:

> **The wallet is willing to pay substantial taker fees for next-day exact-modal-bucket exposure when it believes the bucket probability is materially underpriced.**

A 29.4¢ exact bucket with a ~3.5% fee burden requires a nontrivial probability advantage to justify crossing. This is much more consistent with a forecast-distribution edge than with tiny microstructure arbitrage.

---

# 2. Verified fill: Mexico City winning-bucket SELL immediately after local day end

Transaction:

`0xc9168bbf496f29f9590b5c56ab21320c6a67b5106736e416a4193c82b5304542`

Indexed Polymarket action:

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

## Economic significance

The wallet sold at ~99.9¢ only **five minutes after the Mexico City local civil day ended**.

That is strong behavioral evidence of **capital recycling / settlement-latency monetization**:

- once the resolver state was effectively locked, remaining upside to formal settlement was about 0.1¢ per share;
- the fee at 99.9¢ was negligible because `p(1-p)` is tiny near 1;
- selling releases capital immediately for the next slate of weather contracts.

The relevant comparison for the eventual strategy is therefore not always `hold winner to $1` versus `sell early`; it is:

`incremental 0.1¢ settlement value` versus `expected return from redeploying that capital during the settlement delay`.

For a high-turnover weather specialist, immediate recycling can dominate waiting for redemption even when the exit is a tiny discount to $1.

---

# 3. Verified fill: July 12 exact-outcome BUY, market title not yet mapped

Transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

Timestamp:

- **2026-07-12 13:16:32 UTC**

Neg Risk CTF Exchange order data identifies the supplied wallet as the order maker in the matched transaction and records:

- side: **0**
- token ID: `91076181803621459956200090324917139595424901620108017335569536029558392706177`
- maker amount filled: **44.274 pUSD**
- taker amount filled: **166.68 shares**
- raw execution price: `44.274 / 166.68 = 0.26562`
- fee: **1.62569 pUSD**
- total wallet cash outflow: **45.89969 pUSD**
- fee as percentage of base consideration: **3.67%**

Associated condition ID recovered from the transaction:

`0x1cbcd7f27f60388d43a9d3f1d5e7ed7d3cd31d1076c990a73ae48e644ef1f491`

A related token appearing in the same neg-risk transaction is:

`2655055245387824275985181109206555608704123016388750340070226258019209549699`

## Mapping status

**Market title / city remains unresolved from the indexed sources inspected.**

Do not attach a city or weather question to this token until the condition/token is mapped through Gamma/Data API metadata.

## Economic significance even without title

The transaction independently confirms another behavior visible in the Milan fill:

- intermediate-probability exact outcome around **26.6¢**;
- meaningful share size;
- explicit fee burden around **3.7% of base notional**;
- immediate execution through the Neg Risk exchange rather than waiting only for free passive fills.

This strengthens the hypothesis that the wallet's core edge can be large enough to cross the book, especially around exact modal buckets.

---

# 4. What the recovered transactions change about the wallet thesis

Before fill recovery, the modal-bucket hypothesis came mainly from the current-position profile snapshot.

After fill recovery, we have transaction-level support for four distinct behaviors.

## A. Next-day exact-bucket forecasting is real

The Milan transaction proves the wallet takes exact-bucket exposure substantially before same-day certainty collapse.

This makes **T+1 forecast calibration and release timing** a first-class research target rather than an optional extension.

## B. The wallet accepts substantial taker-fee drag

Two recovered BUYs around 26–29¢ paid roughly **3.5–3.7% of base consideration** in Weather fees.

Therefore the wallet is not surviving on 1–2 percentage-point theoretical edges at those entries. Either:

1. its fair probability is materially above market;
2. rapid expected markout justifies urgency;
3. it values position acquisition sufficiently to accept the fee;
4. some combination of the above.

This is a useful prior for our own edge threshold research: exact modal-bucket signals worth copying should be large enough to dominate actual fee and spread costs, not just clear midpoint by a few points.

## C. It appears willing to cross for conviction

In the recovered matched-order logs, the supplied wallet appears on the initiating/taker-order side of the matching flow and pays the fee.

That suggests at least some of its strategy is **information taking**, not merely passive market making.

Do not generalize this to the full wallet until the complete fill set is classified by maker/taker role.

## D. It actively recycles near-settled winners

The Mexico City sell at 99.9¢ five minutes after local midnight implies turnover economics matter to the strategy.

This should become a measured variable:

`redeployment edge = expected next-opportunity return during settlement delay - discount_to_$1 - exit_fee`

If positive, recycling a locked winner is economically superior to waiting.

---

# 5. Public Polymarket API acquisition path

Polymarket's public Data API exposes enough data to reconstruct substantially more history once direct HTTP access is available.

## Trades

Conceptual request:

`GET https://data-api.polymarket.com/trades?user=<wallet>&limit=10000&offset=0`

Useful fields include:

- proxy wallet;
- side;
- token / asset ID;
- condition ID;
- size;
- price;
- timestamp;
- title;
- event slug / market slug;
- outcome;
- transaction hash.

The documented trade request supports a maximum `limit` of **10,000** and pagination via `offset`.

## Current positions

`GET https://data-api.polymarket.com/positions?user=<wallet>&limit=500`

Use this to recover average cost, position size, current value and token/event metadata for unresolved/open holdings.

## Closed positions

`GET https://data-api.polymarket.com/closed-positions?user=<wallet>&limit=50&offset=<n>`

Closed positions are especially valuable because they expose realized PnL and can be sorted/paginated deeply.

## Activity

`GET https://data-api.polymarket.com/activity?user=<wallet>`

This can recover a broader event stream including fills and related position activity.

## Accounting snapshot

`GET https://data-api.polymarket.com/v1/accounting/snapshot?user=<wallet>`

The endpoint returns a ZIP containing position/equity CSV data and is useful for reconciling wallet-level PnL against reconstructed fills.

## Market/token mapping

For token IDs or condition IDs recovered directly from Polygon logs, use Gamma market metadata / market-by-token lookups to attach:

- question/title;
- city;
- event date;
- bucket;
- resolver rules;
- neg-risk grouping.

This is the missing step for the July 12 token above.

---

# 6. Full-history reconstruction schema

The useful table is one row per economic fill, not one row per blockchain log.

Fields:

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

Then enrich each fill with weather and market state:

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

# 7. Highest-value tests once more fills are recovered

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
- minutes to climatological/forecast peak.

This identifies certainty-collapse trades.

## Fee-adjusted implied conviction

For each BUY, compare entry probability with the break-even fair probability after actual fee and spread.

The recovered 26–29¢ examples are useful because their fee drag is large enough that only meaningful forecast disagreement can justify repeated execution.

## Exit / capital-recycling policy

For near-1 exits, compute:

- expected minutes/hours until redemption;
- discount to $1;
- exit fee;
- next trade entry time;
- return on redeployed capital.

The Mexico City transaction suggests this can be a genuine PnL component rather than operational housekeeping.

---

# 8. Current evidence grade

## Verified

- exact Milan BUY transaction, timestamp, shares, cash, fee, token and market title;
- exact Mexico City SELL transaction, timestamp, shares, proceeds, fee, token and market title;
- exact July 12 BUY transaction accounting and token/condition IDs;
- public Data API supports wallet trades, positions, closed positions, activity and accounting data.

## Inference

- modal-bucket forecasting appears to be a core wallet behavior;
- T+1 forecast information matters, not only T+0 observations;
- wallet sometimes values immediate execution enough to pay meaningful taker fees;
- near-settlement capital recycling appears intentional.

## Unresolved

- complete wallet fill history;
- exact market mapping of the July 12 token;
- systematic maker/taker mix;
- which forecast source drives T+1 entries;
- whether same-day entries systematically follow observation updates;
- price-controlled realized alpha over the full sample.

The next useful increment is more raw history, not additional qualitative speculation.