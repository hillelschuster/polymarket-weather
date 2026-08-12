# Temporal complete-set capture — a stronger Weather maker mechanism

Snapshot: **2026-08-12**

Purpose: isolate a structural profit mechanism visible in Weather specialist trade tables that is stronger than ordinary spread capture and does **not** depend on the unresolved NegRisk conversion `feeBips`.

## Verdict

A binary Polymarket condition has the exact identity:

`1 YES + 1 NO -> $1 pUSD`.

Therefore a trader does not need to sell a Weather position to realize a profitable round trip. It can acquire one side first, acquire the complementary side later after the market moves, and then merge equal quantities back to collateral whenever the combined all-in basis is below `$1`.

This creates a **temporal complete-set capture** mechanism:

> buy favorable Weather inventory passively; if later price movement lets the complementary token be acquired cheaply enough, lock the pair below $1 and recycle it through ordinary binary CTF merge.

The first leg is directional inventory until the complement arrives. A weather probability engine is valuable because it controls that unpaired-inventory risk and helps cancel/reprice before forecast or observation shocks.

This mechanism is distinct from:

- simultaneous `YES ask + NO ask < $1` taker arbitrage;
- multi-outcome NegRisk NO-subset conversion;
- later selling the original token.

It also fits the observed specialist pattern of enormous BUY counts and very few direct SELLs better than a conventional `buy -> sell` lifecycle.

---

# 1. Official complete-set identity

Polymarket documents that equal YES and NO quantities can be merged back into pUSD:

`100 YES + 100 NO -> $100 pUSD`.

Official sources:

- https://docs.polymarket.com/concepts/positions-tokens
- https://docs.polymarket.com/trading/ctf/merge
- https://docs.polymarket.com/market-makers/inventory

The market-maker inventory documentation explicitly describes merge as a way to reduce exposure and free capital. It also documents gasless inventory operations through the Relayer Client.

For matched quantity `m`:

`merge_value = m`.

If the YES lots used in the pair cost `C_Y` all-in and the NO lots cost `C_N` all-in:

`locked_pair_profit = m - C_Y - C_N`.

No weather outcome is needed after the pair exists.

The unresolved multi-outcome NegRisk `feeBips` is irrelevant to this ordinary binary YES/NO complete-set merge identity.

---

# 2. Strong candidate — Madrid July 5, 39°C

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-madrid-on-july-5-2026-39c

Indexed table snapshot around **2026-07-05 12:18 UTC** shows Poligarch:

- roughly 8 minutes before the snapshot: **NO +4.83 @ 60.0¢**;
- roughly 5 minutes before the snapshot: **YES +21.68 @ 30.0¢**.

Thus the visible chronological sequence is approximately:

`NO 60¢ -> ~3 minutes -> YES 30¢`.

At least `4.83` shares overlap in quantity.

If those acquisitions remained in Poligarch's inventory until the second fill and represent ordinary complementary YES/NO tokens of the same binary condition, their raw paired basis is:

`60¢ + 30¢ = 90¢`.

Raw locked value:

`10¢/share`.

For `4.83` paired shares:

`gross complete-set capture = $0.483`.

### Extreme fee bound

Current Weather taker fee formula:

`fee/share = 0.05 * p * (1-p)`.

Official source:

https://docs.polymarket.com/trading/fees

At 60¢:

`fee = 1.20¢/share`.

At 30¢:

`fee = 1.05¢/share`.

Even under the deliberately pessimistic assumption that **both** acquisitions were taker fills:

`net locked edge = 10¢ - 1.20¢ - 1.05¢ = 7.75¢/share`.

For 4.83 shares:

`~$0.3743` before any fixed operational cost.

If either or both fills were maker, the result is better because makers currently pay zero platform trading fee and eligible fills can receive rebates.

Official maker-rebate source:

https://docs.polymarket.com/market-makers/maker-rebates

### Evidence limit

This is **not yet audited realized PnL**.

The Struct indexed snippet does not prove:

- exact maker/taker role for either Poligarch fill;
- whether Poligarch disposed of or transformed the first NO position in an operation absent from the displayed market-trade rows before the YES acquisition;
- whether/when Poligarch later manually merged the complementary inventory.

The result is therefore a high-value **pair-capture candidate**, not a completed wallet-cashflow proof.

But unlike the earlier 98¢ Madrid July 6 case, the 90¢ basis is wide enough to remain mechanically positive even under a two-taker fee bound.

---

# 3. Second candidate — Madrid July 6, 39°C

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-madrid-on-july-6-2026-39c

Indexed table snapshot around **2026-07-06 10:33 UTC** shows Poligarch:

- **YES +11.11 @ 55.0¢**;
- roughly two minutes later **NO +13.34 @ 43.0¢**.

Minimum overlapping quantity:

`11.11 shares`.

Raw pair basis:

`55¢ + 43¢ = 98¢`.

Gross locked value if the lots remained paired:

`2¢/share`, or about `$0.2222` on 11.11 shares.

Current Weather fee bounds:

- 55¢ taker fee ≈ `1.2375¢/share`;
- 43¢ taker fee ≈ `1.2255¢/share`.

Therefore:

- both maker: `+2.00¢/share` before rebate;
- exactly one taker: roughly `+0.76–0.77¢/share`;
- both taker: roughly `-0.46¢/share`.

This case is therefore specifically useful for recovering maker/taker attribution. It can discriminate a deliberate low-friction maker lifecycle from coincidental directional fills.

---

# 4. Why temporal pairing is economically different from simultaneous arbitrage

Suppose at time `t0` the bot buys YES at `y0`.

It does **not** yet own a riskless set. Expected value depends on its current fair probability `q0`:

`directional_EV_Y = q0 - effective_cost_Y`.

Later, at `t1`, if NO can be acquired at all-in cost `n1` such that:

`effective_cost_Y + n1 < 1`,

then the existing directional inventory can be converted into deterministic value.

Incremental decision at `t1`:

`lock_value_from_buying_NO = 1 - effective_cost_Y - effective_cost_NO`.

Once positive and better than continuing to hold the YES directionally, acquiring NO converts model-dependent value into locked pUSD value.

The same logic works in reverse starting with NO.

This means a Weather maker has two sources of expected profit from the same fill:

1. **directional/fair-value edge while inventory is unpaired**;
2. **complete-set capture if future price movement supplies the opposite leg below the remaining dollar basis**.

The second component is an embedded option created by market volatility.

---

# 5. Why Weather may be unusually favorable for this mechanism

Exact-temperature probabilities move repeatedly as information arrives:

- successive global model cycles;
- regional/high-resolution runs;
- METAR/SPECI observations;
- cloud/wind/radiation changes near the daily peak;
- neighboring bucket mode switches.

A binary bucket can therefore travel, for example:

`YES 40¢ -> 30¢ -> 50¢`

within a single event lifecycle.

A passive specialist that acquired NO cheaply when YES was high can later acquire YES cheaply after the probability moves down. It does not require mean reversion all the way back; it only needs the **sum of its historical acquisition prices** to fall below `$1`.

This is structurally easier than earning a conventional sell-side round trip because the complement has a fixed payoff identity.

The key economic state is not simply current mark-to-market PnL. It is:

`best_locked_pair_basis = cost_of_existing_inventory_side + executable_cost_of_complement`.

---

# 6. Smallest production logic

For every binary Weather bucket maintain:

- unpaired YES quantity and acquisition basis;
- unpaired NO quantity and acquisition basis;
- current calibrated `q`;
- current executable/maker prices;
- maker/taker fee state;
- expected rebate on passive fills.

For existing YES inventory, continuously compute:

`pair_edge_if_buy_NO = 1 - yes_basis - effective_NO_cost`.

For existing NO inventory:

`pair_edge_if_buy_YES = 1 - no_basis - effective_YES_cost`.

If the complement can be acquired passively, use the maker effective cost rather than taker cost but account for fill probability and adverse selection.

When matched inventory exists:

`m = min(Y_qty, N_qty)`.

Merge when releasing `m` pUSD has higher opportunity value than keeping the complete set locked, subject to actual relayer/operation mechanics.

No sophisticated optimizer is needed.

---

# 7. Quote policy implied by the mechanism

Let weather fair YES probability be `q`.

A basic informed-maker pair is:

`YES bid = q - mY`

`NO bid = 1 - q - mN`.

If both bids fill at those prices:

`pair_basis = 1 - mY - mN`.

`pair_capture = mY + mN`.

But the important extension is **asynchronous fill**:

- first fill can remain positive-EV because it was bought below weather fair value;
- the opposite quote can later move with `q` and still create a locked set below $1;
- the bot should cancel stale quotes on information shocks rather than blindly wait for both sides.

Thus weather skill and complete-set capture reinforce each other rather than compete.

---

# 8. Best historical test

For Poligarch, ColdMath and the supplied directional wallet, reconstruct fills by binary condition and track a lot-level state machine:

`unpaired_Y`
`unpaired_N`
`paired_qty`
`paired_basis`
`dedicated_merge_qty`
`redeem_qty`
`cash_delta`.

For every new acquisition ask:

1. Was it below current weather fair value?
2. Did it complement older opposite inventory?
3. What was the resulting complete-set basis after actual fill fee?
4. How long between first and complementary fill?
5. Was matched inventory later merged, held to resolution or transformed by exchange settlement?
6. What percentage of specialist PnL can be explained by locked complete-set capture versus residual directional settlement?

The critical metric is:

`locked_pair_profit / maker_turnover`

and

`locked_pair_profit / inventory_dollar_hour`.

Also measure the distribution of completion lag:

`seconds/minutes from first directional fill -> profitable complementary fill`.

This directly tells us how much capital the mechanism can recycle per day.

---

# 9. Why this raises the maker layer in the priority order

The prior evidence already established:

- major Weather specialists provide passive zero-fee liquidity;
- profitable accounts can have huge BUY counts and tiny direct SELL counts;
- simultaneous YES/NO residual inventory exists;
- Weather maker rebates are real and material;
- target directional specialists sometimes pay taker fees after information changes.

Temporal pair candidates add a concrete route by which buy-heavy activity can realize value **without selling the original position**.

The Madrid July 5 candidate is particularly valuable because the visible raw pair basis is 90¢, leaving a wide edge even under a pessimistic both-taker fee calculation.

The revised priority is therefore:

1. reconstruct temporal complete-set capture at wallet-delta level;
2. measure maker fill markout/adverse selection against weather revisions;
3. combine both into a forecast-aware maker state machine;
4. retain immediate directional taker execution for fresh large information shocks;
5. separately scan NegRisk multi-outcome conversion cycles once `feeBips` is available.

## Bottom line

The most promising structural execution hypothesis is no longer merely “earn the spread.” It is:

> **Use weather fair value to acquire favorable unpaired YES/NO inventory passively, then exploit later probability movement to acquire the complement at a combined basis below $1 and convert uncertain inventory into deterministic complete-set value.**

This is simple, fully compatible with Polymarket's documented CTF mechanics, and now has two concrete Poligarch trade-table candidates—one at 98¢ raw pair basis and a stronger one at 90¢.

The remaining task is transaction-level attribution, not conceptual design.