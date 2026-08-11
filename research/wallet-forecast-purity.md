# Wallet forecast purity — separate meteorological information from token mechanics

Snapshot: **2026-08-11**

Purpose: prevent the future strategy from treating every profitable WEATHER wallet as a clean weather forecast signal.

The WEATHER leaderboard mixes several economically different activities:

- directional forecast betting;
- full-ladder relative value;
- negative-risk conversion;
- market making / inventory recycling;
- merge/split operations;
- near-certainty settlement trading;
- climate-index trading.

A wallet can be highly profitable in WEATHER without its individual BUY direction being useful as a meteorological prediction feature.

---

# 1. ColdMath is the clearest structural example

Struct profile:

https://explorer.struct.to/traders/0x594edb9112f526fa6a80b8f858a6379c8a2c1c11

Indexed snapshot reports approximately:

- cumulative PnL: **+$132k**;
- volume: **$13.6M**;
- buys: **216,527**;
- sells: **1,287**;
- redeems: **4,857**;
- merges: **6,571**;
- splits: **2**;
- win rate: ~90.2%;
- fees paid: ~$3.88k;
- rebates: ~$530.

The exact counters move with Struct's indexing date, but the shape is unambiguous: **thousands of merge operations and an extreme buy/sell imbalance**.

Its best-weather rows can also show large merge amounts alongside apparent position PnL.

Example Struct rows include weather markets where the displayed “Merge” notional is thousands or tens of thousands of dollars.

## What a merge means

Official Polymarket CTF documentation:

- $1 pUSD can be split into 1 YES + 1 NO;
- equal YES + NO tokens can be **merged back into $1 pUSD collateral**.

Official docs:
https://docs.polymarket.com/trading/ctf/merge
https://docs.polymarket.com/concepts/positions-tokens

Polymarket's market-maker inventory guide explicitly describes merge/split as inventory-management operations used to create quoting inventory, reduce exposure and free collateral.

https://docs.polymarket.com/market-makers/inventory

Therefore a wallet with thousands of merges cannot be interpreted as a simple sequence of “forecast BUYs.”

---

# 2. Negative-risk events make token direction even less intuitive

Temperature ladders are mutually exclusive multi-outcome events and commonly use Polymarket's negative-risk mechanism.

Official docs:
https://docs.polymarket.com/advanced/neg-risk

In a neg-risk event:

- a NO share in one outcome can be converted into YES shares in every other outcome;
- economically equivalent exposure can be expressed through different token operations;
- fills can arise from liquidity/inventory transformations rather than a standalone belief in one binary market.

A raw event such as:

`wallet bought YES on 33°C`

is therefore not always sufficient to infer:

`wallet thinks P(33°C) is high`.

The full transaction and event-level inventory state matter when structural operations are common.

---

# 3. The correct forecast signal is an economic exposure change

For each wallet action, normalize it into **event-level probability exposure**, not UI token direction.

Ideal object:

`Δexposure_{w,e,i}` = change in wallet's payout sensitivity to outcome `i` after the transaction.

For a simple directional BUY YES with no structural operation:

`Δexposure_i > 0`.

For BUY NO in a neg-risk ladder:

its economic effect is distributed across all other outcomes.

For merge/split:

most or all of the token movement can be collateral/inventory transformation rather than new forecast conviction.

The first implementation does not need a full derivatives engine. It can simply **exclude structural transaction types** from the forecast-flow feature until they are normalized correctly.

---

# 4. Simple forecast-purity filter

For wallet `w`, calculate over a weather segment:

`directional_trades = buys + sells`

`structural_actions = merges + splits + converts`.

A crude structural ratio:

`structural_ratio = structural_actions / (directional_trades + structural_actions)`.

Also measure:

- merge notional / total weather notional;
- rebate income / trading PnL;
- fraction of trades near 0/1;
- fraction of positions created through complete-set operations;
- event-level simultaneous opposite-side inventory.

Do not interpret the ratio as “good/bad trader.” It only answers:

> **How cleanly can raw fills be interpreted as forecast opinions?**

ColdMath's thousands of merges make raw copy-flow much less interpretable than a wallet whose activity is mostly ordinary directional fills.

---

# 5. Forecast-purity classes

## Class A — directional forecaster

Typical pattern:

- BUY/SELL dominates;
- few merge/split/convert events;
- position changes map clearly to a bucket view;
- entry/exit timing aligns with weather information;
- realized PnL attributable to directional settlement/markout.

Use raw directional fills as candidate information features.

## Class B — distribution / ladder trader

Pattern:

- multiple YES/NO positions in one event;
- active reductions/rebalancing;
- still mostly ordinary trades;
- PnL depends on the event-level distribution, not one bucket.

Use only after reconstructing net event probability exposure.

`Poligarch` appears closer to this archetype from visible positions.

## Class C — structural liquidity/inventory trader

Pattern:

- frequent merges/splits/conversions;
- very high turnover;
- inventory operations comparable to or larger than ordinary sells;
- possible maker/rebate economics.

Do not use raw BUY direction as a weather forecast signal.

ColdMath is the clearest current example.

## Class D — climate/index specialist

Large PnL in GISTEMP/hottest-month/year etc.

Do not transfer its skill prior to airport daily extrema without evidence.

`gopfan2` is a current example of a large climate/index archetype.

---

# 6. Supplied wallet remains useful, but purity is not fully measured yet

The supplied wallet's **observed** behavior is strongly directional:

- recovered T+1 exact-bucket BUY;
- recovered losing-bucket SELL;
- near-settlement winner SELL;
- current exact-bucket positions with regular round-dollar notionals.

Those are clean forecast/revaluation actions.

However, the wallet's complete split/merge/convert counts have not yet been recovered from Struct/Data API in this research environment.

Therefore do **not** assert that it has zero structural activity.

Working classification:

> **directional-forecast candidate with strong observed purity, pending full lifecycle backfill.**

This is sufficient to prioritize its fills but not to ignore transaction-type filtering.

---

# 7. `badatmath.` also shows why one market row can mislead

Struct-indexed weather pages show `badatmath.` in very different expressions:

- 10–30¢ exact YES;
- 0.1–0.5¢ extreme-tail YES;
- SELLs of 99.8–99.9¢ NO / YES near settlement.

Some of these are likely forecast expressions; others can be cheap tails, inventory reductions or capital recycling.

Therefore even for a known specialist, do not build a feature from:

`wallet bought/sold this token`

without contextual fields:

- price;
- size versus wallet baseline;
- horizon;
- entry vs exit;
- existing position;
- structural transaction type;
- information freshness.

---

# 8. Minimal wallet signal after purity filtering

For a clean directional action:

`signal_w = signed_direction * normalized_dollars * skill_weight * freshness_weight * action_type_weight`.

Where:

### `signed_direction`

Economic outcome exposure after neg-risk normalization.

### `normalized_dollars`

`trade_notional / wallet_typical_notional`.

This is crucial because a $200 supplied-wallet exit is more informative than several $1 contrary specialist fills.

### `skill_weight`

Estimated only within matching segment:

- daily high vs daily low;
- city/region;
- T+0/T+1;
- price band.

### `freshness_weight`

Decay from transaction time and from the weather information event that likely caused it.

### `action_type_weight`

- fresh directional entry: high;
- material reduction/exit: high but opposite information;
- tiny tail punt: low;
- merge/split/convert: zero until structurally normalized.

---

# 9. Exits may be more informative than entries

The Milan June 25 case is a strong example.

The supplied wallet sold/reduced **193.78 shares of 33°C YES around 10.9¢** while other recognized specialists made much smaller YES buys around 11–12¢.

The bucket ultimately lost; 35°C won.

A simple wallet-consensus vote would count several bullish 33°C accounts versus one seller and could point the wrong way.

A better interpretation sees:

- large existing-holder exit;
- normalized size much larger than some contrary entries;
- timing near a fresh forecast-cycle window;
- eventual settlement agrees with the exit.

This suggests **posterior revision exits** deserve a dedicated feature rather than being discarded as “not a new position.”

---

# 10. PnL leaderboard should be decomposed before skill weighting

For every top WEATHER account, split PnL into:

1. daily temperature directional PnL;
2. climate/index PnL;
3. structural/merge-related PnL where identifiable;
4. maker rebates;
5. other weather families.

Then estimate directional forecast skill only from class (1).

This prevents a structurally successful market maker or climate bettor from receiving a large weight in a daily airport forecast model.

---

# 11. Smallest useful lifecycle dataset

Per wallet action:

`timestamp`
`wallet`
`event_id`
`condition_id`
`token_id`
`trade_type`
`side`
`price`
`shares`
`notional`
`transaction_hash`

plus event-level position before/after when possible.

Classify transaction type:

- BUY;
- SELL;
- MERGE;
- SPLIT;
- CONVERT;
- REDEEM.

Only BUY/SELL enter the first forecast-flow model.

Then further classify BUY/SELL as:

- new entry;
- add;
- reduction;
- close;
- near-settlement recycle.

That is enough to make wallet information economically interpretable.

---

# Bottom line

Top WEATHER wallets are valuable data, but **leaderboard PnL is not a forecast-quality label**.

ColdMath's thousands of merges prove that structural token/inventory activity can be a major part of a profitable WEATHER footprint. The supplied wallet, by contrast, currently provides unusually interpretable directional examples, but its full lifecycle still needs backfill.

The future wallet factor should therefore learn only from **normalized economic exposure changes**, with merge/split/convert activity excluded until properly normalized.