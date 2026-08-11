# Weather wallets to reverse-engineer

Snapshot: **2026-08-11**

Public wallets are not a copy-trading list. They are a dataset of revealed decisions. The useful question is: **what information or execution pattern explains their PnL, and does that information remain predictive after controlling for weather forecasts and price?**

## Verified category-level evidence

Polymarket exposes a WEATHER-specific leaderboard. Recent all-time leaderboard snapshots show several large realized category winners, including approximately:

| Account | Wallet shown on leaderboard/profile | Approx. all-time weather PnL in observed snapshot | Why inspect |
|---|---|---:|---|
| `gopfan2` | `0xf2f6af4f27ec2dcf4072095ab804016e14cd5817` | +$349k | largest observed weather-category winner |
| `aenews2` | leaderboard account | +$285k | second large winner; high-value behavior sample |
| `ColdMath` | `0x594edb9112f526fa6a80b8f858a6379c8a2c1c11` | +$136k | high volume + high PnL |
| `gopfan` | leaderboard account | +$118k | possible relationship to `gopfan2` worth investigating, not assuming |
| `Poligarch` | leaderboard account | +$85k | very high observed weather volume |
| `Hans323` | `0x0f37cb80dee49d55b5f6d9e595d52591d6371410` | +$84k | high volume; good execution sample |
| `automatedAItradingbot` | `0xd8f8c13644ea84d62e1ec88c5d1215e436eb0f11` | +$65k | profile identifies meteorology/IT + automated bot testing |
| `WeatherTraderBot` | `0xacc8e9dcabf9d65a5c78e3bec6941ed53a2b7d08` | +$57k | explicitly bot-themed |
| `HighTempTation` | `0x6011655c4afb76f36dd1b08a137a1ba73466b31e` | +$54k | recently strong monthly weather performance in observed snapshots |
| `JoeTheMeteorologist` | `0x1838cca016850ac7185a9b149fe7d0bd2d6629b4` | +$52k | profile self-identifies as former TV weather professional |

Leaderboard values are time-varying; the numbers above are snapshot evidence, not permanent account statistics.

High PnL alone is not enough. We want accounts with enough trades and stable specialty to estimate a policy.

## User-supplied wallet

Profile:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4-1774968947489`

Underlying address observed:

`0xbddc2a7690BF600E347d5eb4A9C28f9F24E55d4f`

Evidence found in public Polymarket/Polygon data includes temperature-market trades such as:

- buying YES on a Milan 35°C daily-temperature bucket;
- selling YES on a Mexico City 25°C bucket;
- selling a Milan 33°C YES position in another event;
- fills through Polymarket's negative-risk exchange contract.

A recent daily WEATHER leaderboard snapshot placed this account in the top ten for that day with roughly +$1.5k. That establishes that it is worth tracking, but **does not establish its all-time profitability or strategy**.

## Other specialist accounts worth watching

### `meteoblue`

Wallet observed: `0xf73f7e9c6bd1f40dc045d2a93bec3dd4248aee53`

Profile bio identifies it as a `meteoblue staff account`; public activity contains many daily-temperature positions. This is potentially unusually informative because meteoblue is itself a professional weather-forecast provider. Treat the bio as self-reported identity, but the trade history is observable.

### `WeatherHK`

Wallet observed: `0x488c725253fc21c7a9ca812030dc2f6343f98c1c`

Recent public activity is heavily weather-focused, including Hong Kong/China-related contracts. Useful for testing whether local-region specialization beats generic global-model signals.

### `opopv.`

Wallet observed: `0x7c63520c2ca9b336af0c205b9ccf68217bb393d4`

Observed profile/activity indicates a very large prediction count and temperature positions across multiple cities. High sample size may make policy inference easier even if per-trade edge is modest.

### `badatmath`

Wallet observed from leaderboard snapshots: `0x8fbd7cf5f806f563080864694415829f7229a959`

Appeared near the top of recent weekly weather PnL and among high all-time weather volume accounts. Worth comparing with the more obviously meteorology-branded accounts.

## What to infer from each wallet

For each historical trade, reconstruct these features **as they existed at execution time**:

### Market state

- event/city/station/date;
- exact bucket;
- side and price;
- best bid/ask and spread;
- depth near trade price;
- time to resolution;
- complete ladder prices;
- fee-enabled status;
- trade size and inferred liquidity-taking/providing behavior where possible.

### Weather state

- latest available forecast run from each model;
- calibrated fair bucket probability;
- ensemble median/spread/skew;
- distance of bucket from forecast median;
- same-day observed maximum;
- current METAR;
- forecast revision since prior run;
- model disagreement;
- hours until likely daily peak.

### Wallet behavior

- first entry time;
- average entry price;
- add/reduce sequence;
- adjacent-bucket hedges;
- YES/NO direction;
- exits before resolution vs hold;
- size as fraction of wallet's recent exposure;
- simultaneous positions in other buckets/events;
- reaction time after model/observation updates.

## Strategy fingerprints to test

1. **Forecast trader:** entries correlate with our forecast-value revisions and settlement outcome.
2. **Nowcaster:** mostly T+0 trades after observations materially constrain the max.
3. **Longshot seller:** repeatedly buys NO / sells YES in low-probability tail buckets.
4. **Central-bucket buyer:** buys forecast-modal bucket before crowd catches up.
5. **Relative-value trader:** holds multiple adjacent buckets / NO-vs-other-YES structures.
6. **Market maker:** many two-sided fills, small inventory, repeated entries/exits, spread capture.
7. **Release sniper:** concentrated activity immediately after model runs or METAR updates.
8. **Climate specialist:** PnL primarily from monthly/global anomaly markets rather than daily highs.

Accounts can of course combine these.

## Incremental-value test

A wallet should only influence our own fair value if its trades predict outcomes or future prices after accounting for the information we already possess.

For example:

`logit(P(outcome)) = weather_probability + current_market_price + wallet_flow + controls`

Or for short-horizon price movement:

`future_price_change = forecast_revision + wallet_signed_flow + spread/depth + controls`

If wallet flow has no out-of-sample incremental value, copying it only creates worse fills behind the original trader.

## PnL decomposition

For each wallet, separate:

- settlement alpha: bought outcomes that ultimately paid more than purchase price;
- mark-to-market alpha: traded ahead of later repricing;
- spread capture: repeated buy-low/sell-high behavior;
- rebates/rewards if inferable;
- concentration: a small number of huge climate bets vs repeatable daily edge.

This distinction is essential. A six-figure leaderboard account built on two giant climate wins is a different research target from a daily-temperature bot compounding small edges.

## API paths to use later

Official Polymarket endpoints expose the necessary public account data:

- profile lookup through Gamma;
- user trades through the Data API;
- activity through the Data API;
- positions through the Data API;
- WEATHER leaderboard by PnL or volume.

The CLOB market APIs provide current/historical price data; for exact contemporaneous depth we will need our own snapshots going forward because historical full books are not guaranteed by the simple price-history endpoint.

## Source policy

- Leaderboard/trades/positions: **verified public platform data**.
- Profile bios: **self-reported**.
- Strategy classification: **inference only until reconstructed quantitatively**.
- Claims about profitability mechanism: **unknown until PnL decomposition is complete**.

## Primary references

- Polymarket Data API leaderboard docs: https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings
- Public trades: https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets
- User activity: https://docs.polymarket.com/api-reference/core/get-user-activity
- User positions: https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user
- Polymarket WEATHER leaderboard: https://polymarket.com/leaderboard/weather/all/profit
