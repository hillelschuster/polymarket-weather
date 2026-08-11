# Daily-temperature specialist archetypes — what profitable traders actually express

Snapshot: **2026-08-11**

Purpose: use public specialist portfolios and trade tables to decide what the eventual probability engine must support.

The main finding is simple:

> Profitable weather traders do **not** share one universal side, price band or holding pattern. The common object is more plausibly an internal fair probability surface over the resolver outcomes.

Therefore the eventual logic should estimate `q_i` for every bucket and choose the best expression at current executable prices rather than encode a trader-specific rule such as “BUY YES under 30¢” or “BUY NO at 80–95¢.”

---

# 1. Supplied wallet — concentrated modal / near-modal buyer

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Current visible portfolio characteristics:

- median entry price ~49.55¢;
- 18/20 visible positions are international whole-degree Celsius exact buckets;
- 8/20 are T+0, 11/20 T+1, one T+2;
- round-dollar sizing tiers around $100/$150/$200/$250/$400/$450;
- can own adjacent buckets in the same event when both appear valuable;
- recovered history includes early T+1 buys, probability-collapse exits and near-$1 capital recycling.

### Apparent expression

**Buy the modal or near-modal exact bucket at intermediate prices when fair probability is materially above ask.**

The wallet often pays the expensive middle of the fee curve, implying forecast conviction large enough to justify immediate acquisition.

### What to copy from the archetype

Not the specific 40–60¢ price band. Copy the underlying decision object:

`calibrated q_i - executable all-in cost_i`.

---

# 2. `badatmath.` — high-frequency lower-price exact-YES specialist

Profile:

https://polymarket.com/profile/0x8fbd7cf5f806f563080864694415829f7229a959

Recent indexed profile snapshots show more than 16k predictions and repeated exact-temperature positions at lower entry probabilities than the supplied wallet.

Examples from July snapshots:

| Market | Expression | Avg entry | Later mark/resolution in snapshot |
|---|---|---:|---:|
| Wuhan Jul 22 — 29°C | YES | 14.8¢ | ~62¢ |
| Helsinki Jul 22 — 18°C | YES | 13.7¢ | ~51¢ |
| Guangzhou Jul 22 — 34°C | YES | 28.7¢ | ~71.5¢ |
| Denver Jul 22 — 94°F+ | YES | 26.4¢ | ~66.5¢ |
| Beijing Jul 26 — 34°C | YES | 23.8¢ | resolved/marked ~100¢ |
| Taipei Jul 26 — 37°C | YES | 17.2¢ | ~99.8¢ |
| Seoul Jul 26 — 31°C | YES | 27.9¢ | large winning position in leaderboard snapshot |

Polymarket's all-time WEATHER volume snapshot lists `badatmath.` at roughly **$7.43M turnover**, and multiple dated weekly/daily leaderboard snapshots place the account near the top of WEATHER PnL.

Sources:

- https://polymarket.com/leaderboard/weather/all/volume
- https://polymarket.com/leaderboard/weather/weekly/profit

### Apparent expression

**Higher-frequency exact YES at 10–30¢ when forecast concentration is much stronger than market price suggests.**

This is economically attractive because a large `q-p` at a low price produces high return on dollars. It also demands better tail/secondary-mode calibration than the supplied wallet's mostly mid-price entries.

### Implication

Do not exclude 10–30¢ buckets. They can be highly profitable when the weather distribution assigns materially greater mass than the market does.

---

# 3. `meteoblue` — professional-weather information expressed across YES and NO

Profile:

https://polymarket.com/profile/@meteoblue

The public profile describes itself as a **meteoblue staff account**.

Indexed positions show successful exact-temperature expressions across multiple cities and prices, including:

- Tokyo 21°C or higher YES around 15.1¢;
- London 19°C YES around 16¢;
- Miami 86–87°F YES around 10.1¢;
- Seoul 19°C YES around 42¢;
- Los Angeles 68–69°F YES around 21.5¢;
- Toronto 10°C YES around 32.8¢;
- Madrid 21°C YES around 33.7¢;
- London / Tokyo / Seoul NO positions in the 64–99¢ range.

A dated WEATHER daily leaderboard snapshot also placed `meteoblue` among the profitable accounts, with one of the largest wins tied to a Wuhan high-temperature market.

### Apparent expression

**Use weather information to trade whichever binary expression is cheap relative to the forecast distribution: modal YES, lower-price YES, or high-confidence NO.**

This is the cleanest empirical argument against a side-specific bot.

---

# 4. `WeatherHK2` — local regional specialist across high and low markets

Profile:

https://polymarket.com/profile/0xdadbf9e1df1b8d7a184a0d6ab9c83b2337b61870

A recent snapshot shows 934 predictions and a biggest win over $6.6k.

Visible weather expressions include:

- Hong Kong lowest 26°C NO at ~51.2¢ that later resolved/marked near 100¢;
- Hong Kong lowest 25°C YES around 93.9¢;
- Guangzhou high 31°C YES around 41.3¢ that later reached 100¢;
- Shenzhen high 29°C NO around 89¢;
- smaller speculative adjacent/outlier YES positions in Hong Kong/Guangzhou/Qingdao.

### Apparent expression

**Region-specific weather knowledge applied across highs, lows, YES and NO, including near-certainty states.**

The presence of daily-low trading reinforces that the reusable mathematical object is a conditional extrema distribution, not a “daily high bot” rule.

---

# 5. Specialist disagreement is information, not a reason to copy blindly

Struct's indexed trade table for **Milan June 25 — 33°C YES** provides a useful micro-case.

Market:

https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

In the same indexed table state:

- supplied wallet: **SELL / reduce 193.78 YES around 10.9¢**, ~$21.1 value;
- `opopv.`: multiple small YES buys around 12¢;
- `Poligarch`: small YES buy around 12¢;
- several other traders bought YES around 11–12¢.

The market ultimately resolved **NO**; the winning Milan bucket was 35°C.

Winning market:

https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-35c

The exact trade timestamps are not fully recovered from the search-indexed relative-age table, so this is not yet a latency event study. But the direction is still informative:

> the supplied wallet materially reduced the losing 33°C bucket while other recognized weather specialists were still adding small YES exposure around the same displayed price regime.

### Implication

Specialist flow should not be copied as a vote count.

A better feature is:

`wallet_signal = side × normalized_size × segment_skill × freshness`

and disagreement can itself be useful.

Large conviction from a historically skilled city/horizon specialist may deserve more weight than several tiny contrary fills.

---

# 6. Observed strategy dimensions that matter

Across these traders, the meaningful axes are:

## Price regime

- penny/small-tail: <10¢;
- secondary mode: ~10–30¢;
- modal/near-modal: ~30–70¢;
- high-confidence favorite/NO: >70¢.

No one band should be excluded before calibration evidence says it is unprofitable.

## Side

- exact YES;
- tail/far-bucket NO;
- near-certainty YES/NO;
- adjacent YES baskets.

## Horizon

- T+0 observation state;
- T+1 forecast revision;
- occasional longer horizon.

## Specialization

- broad international city set;
- regional/local expertise;
- high versus low temperature;
- high-frequency versus larger conviction entries.

## Exit behavior

- hold to resolution;
- reduce after posterior collapse;
- sell locked winners just below $1 to recycle capital.

The eventual model should permit all of these expressions while keeping the calculation identical.

---

# 7. Minimal unified formulation

For event outcomes `i = 1..K`, estimate coherent resolver probabilities:

`q_i >= 0`

`Σ q_i = 1`

For every tradable YES and NO expression, calculate executable all-in value.

YES:

`EV_yes_i = q_i - yes_all_in_ask_i`

NO:

`EV_no_i = (1-q_i) - no_all_in_ask_i`

For adjacent YES basket `S`:

`EV_basket = Σ_{i∈S} q_i - Σ_{i∈S} all_in_ask_i`

Then rank by expected dollar profit at available depth.

That single formulation can reproduce the economically sensible parts of every archetype above.

---

# 8. What specialist flow can add to weather data

The research question is not “which trader should we copy?”

It is whether specialist fills improve the posterior after controlling for weather and market price.

For a candidate bucket:

`q_final = f(weather_state, market_surface, specialist_flow)`

Useful wallet variables:

- signed dollars relative to trader's typical size;
- trader's city-specific historical skill;
- horizon-specific skill;
- trade price;
- time since trade;
- time since forecast/observation release;
- whether multiple independent specialists agree;
- whether the specialist is entering or exiting an existing view.

The Milan case makes **exit flow** especially important. A skilled wallet selling a formerly plausible bucket may carry more information than seeing a fresh small BUY from another trader.

---

# 9. Money-relevant conclusion

Observed profitable specialist behavior argues against hard-coded strategy restrictions.

The simple eventual bot should not be:

- YES-only;
- NO-only;
- one price band;
- one city family;
- one-bucket-only;
- hold-to-resolution-only.

It should be one compact fair-value engine that asks:

> **Which available weather expression has the highest positive expected dollars after current execution costs?**

The specialist data suggests that is broad enough to capture real profitable behavior without adding architectural complexity.
