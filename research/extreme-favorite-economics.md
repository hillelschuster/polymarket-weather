# Extreme-favorite economics — why 99¢ weather bets can lose money with 98%+ win rates

Snapshot: **2026-08-11**

Purpose: quantify one recurring weather-market failure mode using actual trader evidence and the current Weather fee curve.

The result is simple:

> **Very high win probability is not enough. At 99.8–99.9¢, the required hit rate is so extreme that one miss can erase hundreds or more than a thousand ordinary wins.**

This is directly relevant because multiple public weather traders buy far-tail NO outcomes near 99–99.9¢, and Struct exposes examples where rare misses dominate otherwise impressive win rates.

---

# 1. Exact break-even math for a fee-enabled Weather YES/NO token

For a contract bought at price `p`:

`fee = 0.05 * p * (1-p)`

`all_in_cost = p + fee`.

The bought token pays $1 if correct and $0 if wrong.

Therefore the exact break-even true probability is:

`q_break_even = all_in_cost`.

A trader buying a 99.8¢ NO is not profitable merely because the NO outcome wins 99.8% of the time. The fee pushes required accuracy slightly higher.

---

# 2. 99.8¢ NO

Raw price:

`p = 0.998`

Weather fee/share:

`0.05 * .998 * .002 = 0.0000998`

All-in cost:

`c = 0.9980998`.

Profit when correct:

`1 - c = 0.0019002` per share.

Loss when wrong:

`c = 0.9980998` per share.

Break-even win probability:

**99.80998%**.

Equivalent maximum tolerable loss probability:

**0.19002%** — roughly fewer than **1 miss per 526 bets** if opportunities were equal-sized and independent.

One full loss costs approximately:

`0.9980998 / 0.0019002 = 525.3`

ordinary winning profits.

---

# 3. 99.9¢ NO

Raw price:

`p = 0.999`.

Fee/share:

`0.00004995`.

All-in cost:

`0.99904995`.

Profit when correct:

`0.00095005`.

Loss when wrong:

`0.99904995`.

Break-even true probability:

**99.904995%**.

Maximum tolerable failure rate:

**0.095005%** — around fewer than **1 miss per 1,053 bets**.

One loss erases roughly:

**1,052 ordinary wins**.

This is before additional spread/book-walk cost.

---

# 4. Public trader example: 98.6% win rate is nowhere near enough for indiscriminate near-1 buying

Struct profile:

https://explorer.struct.to/traders/0x5637e85e116455e5faef6e44655f4ca9635921f4

Indexed performance snapshot reports:

- **8,948 markets**;
- **7,936 wins**;
- **110 losses**;
- **98.6% win rate**;
- average win **+$2.26**;
- average loss **-$114**;
- worst loss **-$4.12k**;
- worst loss market: **“Will the highest temperature in Wellington be 24°C or higher on February 12?”**.

The account headline at the indexed snapshot was approximately **-$9.77k PnL**.

Regardless of category mix, the payoff geometry is the relevant observation: a spectacular hit rate can coexist with poor PnL when small favorite gains are periodically offset by large binary losses.

At a 98.6% empirical win rate, buying 99.8¢ contracts has a theoretical expected settlement value of only:

`0.986 - 0.9980998 = -0.0120998/share`

or about **-1.21¢ per share**, before spread/depth.

The problem is not variance alone. If 98.6% were the true probability, the trade is massively negative EV.

---

# 5. Direct weather examples of the same geometry

Another weather-focused public account, `Wweather02`, shows visible positions such as:

- San Francisco high 90–91°F NO around **99.8¢**;
- Mexico City 19°C NO around **99.8¢**;
- Amsterdam 33°C NO around **99.8¢**;
- NYC low 60–61°F NO around **99.9¢**;
- Miami low 90–91°F NO around **99.9¢** that went to zero;
- Seattle high 62–63°F NO around **99.9¢** that went to zero.

Profile:

https://explorer.struct.to/traders/0x7f1855bb6885991eddff78412c1433f09f3c1ef3

A visible 99.9¢ Miami-low NO position lost roughly **$71.2**, while many successful 99.8–99.9¢ positions earn only tiny fractions of a percent on committed capital.

The strategy can still be profitable if its true miss rate is far below the market-implied tail probability, but raw “this almost never happens” reasoning is insufficient.

---

# 6. Exact tail-probability requirement

For a favorite token at all-in cost `c`, let `r = 1-q` be the true probability the favorite loses.

Expected value/share:

`EV = (1-r) - c`

so positive EV requires:

`r < 1-c`.

Examples:

| Raw favorite price | All-in cost | Maximum true miss probability for +EV |
|---:|---:|---:|
| 95¢ | ~95.2375¢ | <4.7625% |
| 97¢ | ~97.1455¢ | <2.8545% |
| 98¢ | ~98.0980¢ | <1.9020% |
| 99¢ | ~99.0495¢ | <0.9505% |
| 99.5¢ | ~99.5249¢ | <0.4751% |
| 99.8¢ | ~99.8100¢ | <0.1900% |
| 99.9¢ | ~99.9050¢ | <0.0950% |

At extreme prices the modeling problem is therefore **tail calibration at basis-point precision**, not ordinary classification accuracy.

---

# 7. Why exact weather tails are difficult

A 99.8¢ NO implies the excluded weather outcome has true probability below roughly 0.19% after fee.

That is demanding because rare daily-extreme failures can come from:

- hidden between-report peaks/troughs;
- wrong resolver station/source;
- 1°C/2°F quantization;
- fronts arriving earlier/later than forecast;
- convection/outflow;
- local sea breeze / foehn / downslope effects;
- model-version bias;
- observation revision;
- forecast error tails much fatter than the center.

A model can be excellent around the mode and still underestimate a 0.2% tail by 5–10×.

That is enough to make a 99.8¢ favorite strongly negative EV.

---

# 8. This does not mean “never buy 99¢”

Near-certainty weather positions can be excellent when the resolver state has become mechanically constrained.

Example structure:

- observed running maximum has already passed the critical boundary;
- local peak is over;
- lower alternative is physically impossible;
- the only residual uncertainty is resolver publication/revision mechanics.

Then true probability may genuinely be 99.99%+.

The correct rule is therefore not a price cap.

It is:

> **Only buy a 99.x¢ favorite if the model can justify a miss probability materially below the fee-adjusted residual payout.**

At 99.9¢, that means demonstrating less than roughly 0.095% failure probability, not merely “very confident.”

---

# 9. Better expression can dominate the near-1 favorite

Suppose a full ladder has:

- favorite NO at 99.8¢;
- a related modal YES at 55¢ with fair value 65%;
- an adjacent YES at 20¢ with fair value 28%.

Even if the favorite is positive EV, the lower-priced expressions can offer much higher return on capital and larger error tolerance.

Rank all expressions by expected dollars at actual depth:

`EV_yes_i = q_i - all_in_yes_cost_i`

`EV_no_i = (1-q_i) - all_in_no_cost_i`.

Do not select the highest nominal probability simply because it feels safest.

---

# 10. Implication for supplied-wallet research

The supplied wallet's visible positions are concentrated around intermediate prices rather than 99.x¢ favorites, with median entry around 49.6¢ and recovered fee-paying buys near 27–30¢.

That regime tolerates several percentage points of probability error and offers substantially larger expected percentage returns per genuine forecasting edge.

This may be economically preferable to farming tiny near-certainty spreads unless the observation state truly collapses uncertainty.

---

# 11. Minimal bot rule

Do not use:

`if probability > 99%: buy`.

Use:

`EV = calibrated_probability - executable_all_in_cost`.

For extreme favorites, require the calibrated tail estimate to be strong enough that:

`estimated_miss_probability < residual_payout_after_fee`.

Because estimation uncertainty matters most in tiny tails, a practical ranking can also compare the **lower confidence bound on fair probability** with all-in cost, but only if that improves historical dollars; no generic safety margin is necessary.

---

# Bottom line

Near-1 weather contracts are not “safe yield.” They are ultra-short-volatility trades.

At 99.8¢, one miss erases about **525 normal wins**.

At 99.9¢, one miss erases about **1,052 wins**.

The public trader evidence confirms the basic danger: **98.6% wins can still coexist with deeply unattractive PnL when average losses dwarf average gains.**

The profitable system should therefore optimize calibrated expected dollars across the ladder, not win rate or nominal certainty.