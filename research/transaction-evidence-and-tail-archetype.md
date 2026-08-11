# Transaction evidence: maker/merge + ultra-cheap Weather tails

Snapshot: **2026-08-11**

Purpose: push the specialist reverse-engineering from profile-level inference toward transaction-level mechanisms that can increase net income.

## Verdict

Three distinct Weather monetization archetypes are now empirically visible:

1. **forecast-revision directional trading** — supplied wallet;
2. **buy-heavy maker inventory + merge/recycle** — Poligarch and ColdMath;
3. **ultra-cheap tail YES accumulation** — GbushiCshuo and several high-volume tail collectors.

The first two combine naturally into one production strategy. The third is a separate low-capital/high-convexity overlay that deserves its own calibration test.

The strongest new evidence is an on-chain Poligarch Weather fill proving the account acted as a zero-fee maker inside a daily-temperature neg-risk match.

---

# 1. Direct on-chain proof: Poligarch was a zero-fee Weather maker

Wallet:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

Transaction:

`0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213`

PolygonScan:

https://polygonscan.com/tx/0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213

Timestamp:

`2026-07-21 01:56:10 UTC`

Headline transaction action:

- daily Weather event: **Wellington July 21 — 11°C**;
- taker wallet bought 29.780165 YES shares for about $1.75;
- transaction routed through `Polymarket: Neg Risk CTF Exchange V2`.

The relevant `OrderFilled` log for Poligarch is explicit:

- `maker = 0xB40e89677d59665d5188541aD860450A6e2a7cc9`;
- token id = `101940427571296396096846204867677734529692848694090204797814015788501285652940`;
- `makerAmountFilled = 9.400590 pUSD`;
- `takerAmountFilled = 9.990000 token units`;
- `fee = 0`;
- Poligarch received 9.99 tokens.

Effective token acquisition price:

`9.400590 / 9.990000 = 0.941 = 94.1¢`.

This proves all of the following without inference:

- Poligarch had resting maker liquidity in a daily-temperature event;
- its maker fill paid zero platform trading fee;
- the fill was inside the neg-risk exchange path;
- the account acquired inventory rather than merely selling out a directional position.

### Important limitation

Because the neg-risk adapter creates/transforms related outcome tokens during the same match, the token id above should not be casually labeled the binary's simple UI `NO` token without completing the token/condition mapping.

The economically relevant fact is narrower and firm: **Poligarch provided maker liquidity and acquired a related Weather outcome token at 94.1¢ with fee zero inside the Wellington temperature match.**

This transaction does **not** by itself prove that this exact lot was later paired and merged below $1 total acquisition cost.

---

# 2. Direct pair-capture candidate: Madrid July 6 — 39°C

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-madrid-on-july-6-2026-39c

Indexed snapshot time:

`2026-07-06 10:33 UTC`

The same binary trade table shows:

- age 23m: Poligarch **YES +11.11 @ 55.0¢**, value ~$6.11;
- age 21m: Poligarch **NO +13.34 @ 43.0¢**, value ~$5.74.

If 11.11 shares from those displayed lots were genuinely pairable at those prices:

`combined acquisition price = 0.55 + 0.43 = 0.98`

`gross pair capture/share = 1 - 0.98 = 0.02`

`gross pair capture on 11.11 = $0.2222`.

Gross return on the $0.98 pair cash cost would be about **2.04% for that completed pair cycle** before incentives and any execution/transform cost.

This is a **candidate**, not yet proven realized PnL, because the indexed rows do not expose enough information to establish:

- exact second-level fill timestamps;
- whether both were maker fills;
- whether those exact lots were the lots later merged;
- intervening inventory from earlier fills.

The next decisive reconstruction is chronological fill matching followed by actual merge cashflows.

---

# 3. Why maker pair capture is economically different from directional trading

Official Polymarket mechanics:

https://docs.polymarket.com/trading/ctf/merge

`1 YES + 1 NO -> $1 pUSD`

For paired maker acquisitions at prices `y` and `n`:

`pair_profit = 1 - y - n`

before incentives and operational cost.

Examples:

| Combined pair cost | Gross capture | Gross return on pair cash |
|---:|---:|---:|
| 99.5¢ | 0.5¢ | ~0.50% |
| 99.0¢ | 1.0¢ | ~1.01% |
| 98.0¢ | 2.0¢ | ~2.04% |
| 97.0¢ | 3.0¢ | ~3.09% |

Do **not** annualize these numbers. The money variable is closure frequency, paired capacity and first-leg exposure time.

The central measurement is:

`net_pair_pnl = merge_proceeds - matched_lot_acquisition_cost + rebate + reward - adverse_selection_loss - operating_cost`

The dangerous state is the period after only one side has filled. Weather information matters precisely because it predicts whether that residual inventory is cheap or toxic.

---

# 4. Poligarch lifecycle strongly supports merge/recycle

Struct trader page:

https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

Aug 10 indexed snapshot approximately shows:

- volume: **$24.5M**;
- fees paid: **$2.29K**;
- buys: **1,612,158**;
- sells: **1,287**;
- redemptions: **40,882**;
- merges: **67,647**;
- splits: **0**;
- converts: **2**;
- cumulative displayed PnL: **$207K**;
- rebates: **$19.3K**;
- liquidity rewards: **$5.52K**.

Operation ratios:

- buys / sells ≈ **1,253:1**;
- merges / sells ≈ **52.6:1**.

Operation counts are not share quantities, but this lifecycle is incompatible with the normal assumption that the account repeatedly buys a forecast view and exits it by selling.

The parsimonious mechanism is:

`acquire inventory -> transform/merge/redeem -> acquire again`,

with direct sells used rarely.

Struct's current open rows also show Poligarch simultaneously holding YES and NO in the same Weather binaries, which is expected from incomplete matching of two-sided maker inventory.

---

# 5. Independent replication: ColdMath

Wallet:

`0x594edb9112f526fa6a80b8f858a6379c8a2c1c11`

Struct:

https://explorer.struct.to/traders/0x594edb9112f526fa6a80b8f858a6379c8a2c1c11

Indexed totals:

- volume: **~$14M**;
- fees: **~$4.02K**;
- buys: **224,892**;
- sells: **1,306**;
- redemptions: **4,999**;
- merges: **6,790**;
- splits: **2**;
- cumulative displayed PnL: **~$132K**.

Ratios:

- buys / sells ≈ **172:1**;
- merges / sells ≈ **5.2:1**.

Polymarket's all-time Weather profit leaderboard crawl places ColdMath at **#3, +$136,377**:

https://polymarket.com/leaderboard/weather/all/profit

This materially reduces the chance that Poligarch's lifecycle is idiosyncratic.

### Even stronger accounting clue

Struct's `Best Wins` for ColdMath contains many Weather rows where:

- displayed entry was around **0.1–1.6¢**;
- current token value is displayed as 0;
- buys may total only tens/hundreds of dollars;
- **merge value is $5K–$15K**;
- displayed PnL is dominated by the merge attribution.

Example:

**Wellington March 28 — 16°C**

- entry 1.2¢;
- buys ~$370 across 907 buy operations;
- sells $0;
- merge ~$14.9K;
- Struct displayed PnL ~$14.6K.

This is not ordinary “buy at 1.2¢ and settle at $1” accounting because the current token is displayed at 0 and the value left through merge.

It is exactly why transformed-inventory strategies must be evaluated with a cashflow ledger rather than position-level PnL.

The underlying paired NO acquisition cost is still needed to know true economic profit.

---

# 6. Weather leaderboard confirms these are not obscure accounts

Polymarket all-time Weather leaderboard crawls (approximately late July 2026 snapshot):

Profit:

https://polymarket.com/leaderboard/weather/all/profit

- ColdMath: **#3, +$136,377**;
- Poligarch: **#6, +$84,711** in the English crawl.

Volume:

https://polymarket.com/leaderboard/weather/all/volume

- Poligarch: **#3, ~$13.856M Weather volume**;
- ColdMath: **#7, ~$10.942M Weather volume**.

These leaderboard figures are Polymarket category metrics, while Struct's totals may include all categories. Do not mix them as if they were identical accounting universes.

The useful conclusion is only that both merge-heavy wallets are independently large and profitable in Weather itself.

---

# 7. Supplied wallet Milan June 25 exit is now time-bounded

Market:

https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

Struct's market snapshot is timestamped:

`2026-06-25 03:36 UTC`.

The supplied wallet's row shows:

- YES / 10.9¢;
- **-193.78 shares**;
- ~$21.1 value;
- age label **2h**.

This places the reduction in the early UTC hours of June 25, before the local afternoon temperature peak.

### Inference

The timing makes a **forecast-cycle / overnight information reaction more plausible than an exit caused by same-day observed peak temperature**.

This is not yet proof because:

- Struct's `2h` is coarse;
- exact fill timestamp is unavailable;
- preceding acquisition remains unrecovered;
- exact forecast vintage at the sell time still needs reconstruction.

This strengthens, but does not close, the forecast-revision hypothesis.

---

# 8. Third archetype: ultra-cheap tail YES accumulation

A separate trader reveals another potentially profitable Weather mechanism.

Trader:

`GbushiCshuo`

Wallet:

`0xfbb7fc19f80b26152fc5886b5eafa7d437f26f27`

Struct:

https://explorer.struct.to/traders/0xfbb7fc19f80b26152fc5886b5eafa7d437f26f27

Indexed lifecycle:

- volume: roughly **$159K–$165K** depending crawl;
- buys: roughly **152K–156K**;
- sells: only **72–73**;
- redemptions: thousands;
- merges: **0**;
- cumulative PnL: **~$13K**;
- 19,031 Polymarket predictions/markets shown on profile/Struct;
- almost all buy operations in the inspected period were under $10;
- one Struct crawl shows ~100K buys with average trade size only **$0.41**.

Unlike ColdMath, there are zero merges. So the repeated penny Weather winners are not a merge-accounting artifact.

Struct `Best Wins` includes examples such as:

- Paris Apr 6 — 21°C YES: avg entry ~0.2¢, ~$0.80 buys, displayed win ~$399;
- Paris Apr 15 — 22°C YES: ~0.4¢, ~$1.40 buys, ~$399 win;
- Chongqing Mar 28 — 16°C YES: ~0.4¢, ~$1.60 buys, ~$398 win;
- Singapore Apr 1 — 34°C YES: ~0.4¢, ~$1.60 buys, ~$398 win;
- Denver Apr 1 — 52–53°F YES: ~0.5¢, ~$2 buys, ~$398 win;
- numerous 1–2¢ Weather YES outcomes producing ~$390–$400 winning payouts.

A direct market example in old 0.1¢ books:

Munich March 16 — 5°C:

https://explorer.struct.to/markets/highest-temperature-in-munich-on-march-16-2026-5c

shows GbushiCshuo buying **200 YES shares @0.1¢** for ~$0.20 while other traders bought NO at 99.9¢.

Another Paris market shows the same pattern:

https://explorer.struct.to/markets/highest-temperature-in-paris-on-march-2-2026-11corbelow

- large NO buys around 99.8–99.9¢;
- GbushiCshuo YES +199.98 @0.1¢;
- TENETENET and other systematic accounts also accumulating the same penny YES side.

---

# 9. Economics of the penny-tail strategy

At very low prices, absolute probability error becomes enormously valuable in percentage-return terms.

For a YES quote at `p = 0.001`:

- market implies ~0.1%;
- if calibrated fair probability is only 0.2%, gross expected value doubles relative to purchase cost;
- if true probability is 0.5%, the expected return is roughly 4x purchase cost before fee/fill effects.

This is not a reason to buy every penny tail. The expected-value condition remains:

`q_tail > all_in_cost_tail`.

The potentially structural reason Weather is attractive is that generic bettors may round physically unlikely outcomes toward zero much more aggressively than a calibrated forecast-error distribution does.

A one-degree daily-extreme tail can remain a real 0.3–2% event because of:

- model error;
- station/local basis;
- cloud/wind timing errors;
- brief extrema missed by generic city forecasts;
- resolver/display quirks;
- forecast revisions after the market has already left stale penny liquidity.

The eventual full-distribution model automatically produces the correct tail probability. No separate forecasting model is required.

### Fee nuance

Current Weather taker fees follow:

`fee = shares * 0.05 * p * (1-p)`.

Official docs also state that fees are rounded to five decimal places and sufficiently tiny fees round to zero.

Therefore micro-orders near the extremes can have a very different friction profile from mid-price directional taker orders.

Source:
https://docs.polymarket.com/market-makers/maker-rebates

This must be modeled using actual current tick size, fee rounding, minimum order constraints and fill mechanics rather than assuming the mid-price fee hurdle.

---

# 10. Tail strategy limitation: capacity is probably the main bottleneck

GbushiCshuo's observed winning trades often risk only cents to single-digit dollars to win roughly $400.

That gives extraordinary percentage returns on successful lots but does not automatically imply high scalable dollar capacity.

The relevant research output is:

`expected net dollars = fillable tail shares * (q_tail - effective_cost)`

summed across all cities/dates/buckets.

Measure:

- number of 0.1–2¢ opportunities/day;
- resting depth available at those prices;
- maker vs taker fill probability;
- hit rate versus calibrated q;
- loss distribution when buying all candidate tails;
- whether winners are explainable by forecast distributions or only ex-post luck;
- net dollars at bankroll scales, not headline ROI.

Because the core full-ladder model already yields `q_i` for every tail, this overlay is cheap to test later.

---

# 11. Updated profitability ordering

Current evidence supports this priority:

## 1. Forecast-aware maker/merge

Why first:

- independently visible in two major profitable Weather accounts;
- direct on-chain maker proof exists;
- avoids Weather taker fees;
- can monetize spread/pair capture even when directional forecast edge is modest;
- weather probability reduces first-leg adverse selection;
- merge releases collateral rapidly.

Main missing measurement:

**actual matched-lot pair PnL distribution and pair-closure latency.**

## 2. Forecast-revision taker layer

Why second:

- supplied wallet pays taker fees for some entries, implying sufficiently large information shocks;
- Milan Jun 25 exit is now plausibly an overnight model-revision response;
- Milan Jun 30 buy aligns with a fresh ECMWF 18Z information window.

Main missing measurement:

**point-in-time forecast vintages immediately before each fill/exit and post-fill market markout.**

## 3. Ultra-cheap tail overlay

Why third:

- direct non-merge profitable examples exist;
- coherent forecast distributions naturally expose mispriced tails;
- potentially exceptional ROI on tiny capital.

Why not first:

- dollar capacity likely much smaller;
- full historical basket of losers is needed to distinguish structural tail underpricing from survivorship-highlighted winners;
- trader is not currently among the top Weather profit leaderboard accounts despite striking individual returns.

---

# 12. The minimal unified economic engine is now clearer

For each Weather event maintain a coherent resolver probability vector:

`q = (q_1,...,q_K)`.

Then expose the same probability vector through three execution modes.

### Maker/merge

Post passive liquidity where:

`fair value - quote > expected adverse selection - expected rebate/reward`.

When complementary inventory accumulates:

`pair_qty = min(YES_balance, NO_balance)`

and merge whenever collateral recycling dominates retaining the pair.

### Directional shock

After a forecast/observation revision:

`EV_cross = q_new - executable_price - taker_fee - impact`.

Cancel stale maker quotes and cross only clear positive-EV depth.

### Tail bids

For very cheap outcomes:

`EV_tail = q_tail - effective_microprice - rounded_fee`.

Post tiny maker bids or take stale asks only where calibrated tail probability materially exceeds cost.

One probability engine; three monetization paths.

---

# Highest-value next measurement

The next research pass should build **one chronological cashflow ledger for a single Poligarch/ColdMath Weather binary** containing both complementary buys and a subsequent merge.

Needed fields:

`timestamp`
`maker/taker`
`YES/NO token`
`price`
`quantity`
`fee`
`rebate`
`inventory after fill`
`merge quantity/time`
`pUSD released`
`unpaired residual`
`markout`

The decisive output is not a wallet win rate. It is the empirical distribution of:

`1 - matched_yes_cost - matched_no_cost`

and how that changes after first-leg adverse selection, rebates, residual inventory and capital-time.

In parallel, the supplied wallet's Milan Jun 25 and Jun 30 events remain the best small sample for proving the forecast-revision alpha that should control the maker's quote skew and taker-on-shock routing.
