# Negative-risk ladder arbitrage — deterministic event-level identities

Snapshot: **2026-08-11**

Purpose: derive the exact multi-outcome arithmetic available in Polymarket temperature ladders before using any meteorological forecast edge.

## Verdict

Daily-temperature events are unusually attractive for **negative-risk relative-value scanning** because the outcomes form a small, exhaustive, mutually exclusive ladder.

For a `K`-outcome event, the assets are not independent binaries. Polymarket's NegRisk Adapter permits a basket of `m` NO tokens to be converted into:

- collateral equal to `m - 1` per unit converted; and
- one YES token in every unselected outcome;
- all outputs reduced by the market-specific conversion fee.

This gives deterministic cross-bucket identities that can be scanned directly from the order books.

The smallest professional implementation should evaluate these identities continuously **before** applying any forecast model. Weather probabilities then improve route selection, residual inventory valuation and maker placement.

Primary sources:

- https://github.com/Polymarket/neg-risk-ctf-adapter/blob/main/docs/NegRiskAdapter.md
- https://raw.githubusercontent.com/Polymarket/neg-risk-ctf-adapter/main/src/NegRiskAdapter.sol
- https://docs.polymarket.com/advanced/neg-risk
- https://github.com/Polymarket/ctf-exchange-v2
- https://raw.githubusercontent.com/Polymarket/ctf-exchange-v2/main/src/adapters/NegRiskCtfCollateralAdapter.sol

---

# 1. Exact conversion identity

Let the event contain `K` mutually exclusive and exhaustive outcomes.

For outcome `i`:

- `Y_i` = one YES share;
- `N_i` = one NO share.

Choose a subset `S` of `m` outcomes whose NO positions will be converted.

Ignoring conversion fees for one moment, the NegRisk Adapter implements:

`sum_{i in S} N_i  <=>  (m - 1) collateral + sum_{j not in S} Y_j`.

This is not just theoretical payoff equivalence; it is an on-chain conversion path supported by the adapter.

Example with three outcomes A/B/C:

`N_A + N_B  ->  $1 + Y_C`.

If A wins, the two NO inputs pay `$1`; output pays `$1`.

If B wins, same.

If C wins, the two NO inputs pay `$2`; output pays `$1 + $1 = $2`.

The adapter generalizes this to arbitrary selected NO subsets.

---

# 2. Current contract fee mechanics

The legacy NegRisk Adapter stores a market-specific `feeBips`.

Current source code computes:

`feeAmount = amount * feeBips / 10_000`

`amountOut = amount - feeAmount`.

For every selected-NO conversion:

- collateral output is multiplied by `amountOut / amount`;
- each complementary YES output is also multiplied by the same factor;
- the deducted collateral and YES-token fee is sent to the configured vault.

The current CTF Exchange V2 `NegRiskCtfCollateralAdapter` reads the same legacy adapter `getFeeBips(marketId)`, calls `convertPositions`, and forwards the fee-adjusted YES/collateral outputs to the caller.

Define:

`f = feeBips / 10_000`

`lambda = 1 - f`.

Then converting one unit of every NO in subset `S` returns:

`lambda * (m - 1)` collateral

plus

`lambda * Y_j` for every `j not in S`.

### Important unresolved current-state field

The conversion fee is **market-specific**. I have not yet verified the live `feeBips` for daily Weather events from an on-chain market ID, so the scanner must read it rather than assume zero.

This parameter can completely determine whether a sub-percent basket discrepancy is executable.

---

# 3. Deterministic full-YES basket

Because exactly one outcome wins:

`Y_1 + Y_2 + ... + Y_K = $1 at settlement`.

Therefore a pure buy-side deterministic opportunity exists when executable all-in YES asks satisfy:

`sum_i ask_yes_i_all_in < 1`.

Gross locked value:

`edge_yes_basket = 1 - sum_i ask_yes_i_all_in`.

This requires no forecast model.

Its main economic drag is capital lock until resolution unless the position can be transformed/recycled earlier.

For a daily Weather market whose resolution is near, the capital-time penalty can be much smaller than for long-duration prediction markets.

A scanner must use **depth-weighted synchronized asks**, not displayed midpoints or independently sampled top-of-book values.

---

# 4. Deterministic full-NO conversion basket

Set `S` equal to all `K` outcomes.

Then there are no complementary YES outputs.

The adapter converts:

`N_1 + N_2 + ... + N_K`

into:

`lambda * (K - 1)` collateral.

Therefore a direct executable buy-and-convert opportunity exists when:

`sum_i ask_no_i_all_in + conversion_gas < lambda * (K - 1)`.

Per-unit gross edge before gas:

`edge_all_no = lambda * (K - 1) - sum_i ask_no_i_all_in`.

This is especially important because the conversion returns collateral immediately rather than waiting for weather resolution.

Example for a 10-bucket temperature ladder:

- fee = 0: deterministic output = `$9.00`;
- fee = 10 bps: output = `$8.991`;
- fee = 50 bps: output = `$8.955`.

A 4-cent apparent discrepancy in the sum of NO asks is profitable at zero/10-bp conversion fee but not at 50 bp.

This is why live `feeBips` must be treated as a first-class market parameter.

---

# 5. Arbitrary NO-subset conversion inequalities

For any subset `S` of size `m`, buy its NO tokens and convert.

If the resulting complementary YES tokens are immediately sold, define:

`net_bid_yes_j` = executable YES bid after any applicable sell fee and impact.

Then immediate cash-equivalent proceeds per converted unit are:

`lambda * [(m - 1) + sum_{j not in S} net_bid_yes_j]`.

Let:

`all_in_ask_no_i`

include taker fee/impact for acquiring each selected NO.

A directly executable conversion-and-liquidation opportunity exists when:

`lambda * [(m - 1) + sum_{j not in S} net_bid_yes_j]`

`> sum_{i in S} all_in_ask_no_i + gas_per_unit`.

This family includes the simple one-NO identity as `m = 1`:

`N_i -> lambda * sum_{j != i} Y_j`.

At zero conversion fee:

`N_i = sum_{j != i} Y_j`.

The multi-NO form is more powerful because it can release immediate collateral as `m` increases.

---

# 6. Do not force immediate liquidation of complementary YES

The conversion output does not have to be sold.

If the weather model estimates fair probability vector:

`q = (q_1, ..., q_K)`, with `sum q_i = 1`,

then the model value of the fee-adjusted output is:

`lambda * [(m - 1) + sum_{j not in S} q_j]`.

Since:

`sum_{j not in S} q_j = 1 - sum_{i in S} q_i`,

model value becomes:

`lambda * [m - sum_{i in S} q_i]`.

At zero conversion fee this matches the fair value of the selected NO basket:

`sum_{i in S} (1 - q_i) = m - sum_{i in S} q_i`.

Therefore conversion can be used not only for deterministic arbitrage, but to **transform expensive or unwanted NO inventory into collateral plus the specific YES residuals the forecast model prefers**.

That is particularly natural in temperature ladders where probability mass is concentrated in a few neighboring buckets.

---

# 7. Reverse-direction opportunities require explicit construction costs

The NegRisk Adapter's `convertPositions` operation is one-way:

`NO subset -> collateral + complementary YES`.

Do not assume the reverse transform exists at the same fee/cost.

However, standard binary CTF operations can still construct related portfolios.

For each binary outcome:

`$1 collateral -> Y_i + N_i`

via split.

Therefore a sell-side event-level arbitrage can sometimes be constructed by:

- splitting collateral into YES/NO complete sets;
- selling overpriced legs;
- retaining/transforming the residual inventory.

The exact reverse route must be priced as a separate transaction graph rather than inferred from the forward conversion identity.

This asymmetry matters for scanner design: **use directed edges, not equality assumptions**.

---

# 8. The right abstraction is a tiny asset-transformation graph

For one Weather event, define nodes/assets:

- pUSD collateral;
- `Y_i` for every bucket;
- `N_i` for every bucket.

Available directed transformations include:

### Exchange trades

- pUSD -> YES at executable ask;
- YES -> pUSD at executable bid;
- pUSD -> NO at executable ask;
- NO -> pUSD at executable bid.

Each edge includes actual fee, depth and impact.

### Binary CTF

- 1 pUSD -> 1 YES_i + 1 NO_i via split;
- 1 YES_i + 1 NO_i -> 1 pUSD via merge.

### Negative-risk conversion

For any selected NO subset `S`:

`NO_S -> lambda*(m-1) pUSD + lambda*YES_complement(S)`.

### Resolution

For daily markets close enough to resolution:

- winning YES -> $1;
- losing NO -> $1;
- losing YES / winning NO -> $0.

Resolution paths have capital-time, source-finalization and opportunity-cost terms rather than price uncertainty once physically locked.

The economically clean scanner asks:

> **Does any executable directed cycle begin with pUSD and return more pUSD after all fees, depth, conversion haircuts and gas?**

This can be solved by direct enumeration because Weather ladders are small. No large optimization framework is needed.

---

# 9. Why exact-temperature ladders are unusually suitable

Weather events typically have roughly single-digit to low-double-digit outcome counts.

That means:

- all full-basket checks are trivial;
- every NO subset can be enumerated for `K <= ~12` (`2^K - 1` subsets is only thousands);
- neighboring buckets carry most probability mass;
- tail buckets often have stale or coarse quotes;
- resolution arrives daily, reducing capital duration;
- a coherent meteorological `q` vector already exists for valuing residual output.

The full subset enumeration is economically justified here because it is tiny and deterministic, not overengineering.

---

# 10. Execution order matters

A theoretical basket inequality is worthless if the legs cannot be filled together.

For every candidate cycle compute executable depth at common size `x`:

`x <= min(fillable_qty_on_every_required_leg)`.

Then recompute the entire route using VWAP, not top-of-book.

For a taker basket, expected dollars are:

`x * unit_edge(x) - fixed_gas`.

Only the size that maximizes actual net dollars matters.

The scanner should therefore test a small set of breakpoints defined by cumulative order-book depth, because the optimal size changes only when one leg steps to the next price level.

No continuous optimizer is necessary.

---

# 11. Maker accumulation can improve basket economics

The immediate taker inequalities are the conservative baseline.

A forecast-aware maker can instead accumulate one or more required legs passively:

- maker fee = zero in current Weather fee structure;
- potential maker rebates reduce effective acquisition cost;
- incomplete basket inventory is valued using the weather `q` vector;
- once enough legs are held, execute the deterministic conversion/merge route.

This is likely a better use of the Poligarch-style maker evidence than assuming every observed `merge` was manually initiated.

The maker's objective becomes:

`expected basket completion value`

minus

`fill-conditioned adverse selection + residual inventory cost + capital-time`.

Weather forecasting is what lets the bot tolerate incomplete basket fills better than a purely mechanical arbitrageur.

---

# 12. Event-level quote consistency tests

At every synchronized snapshot calculate at least:

### YES simplex

`sum best_ask_yes`

`sum best_bid_yes`.

### NO full basket

`sum best_ask_no`

`sum best_bid_no`.

### Per-outcome neg-risk parity

For each `i`:

`ask_no_i` versus executable cost of acquiring all other YES outcomes and converting/holding appropriately.

### Subset parity

For every subset `S`:

`cost(selected NO)`

versus

`fee-adjusted collateral + executable/fair value of complementary YES`.

### Binary complete-set parity

For every `i`:

`ask_yes_i + ask_no_i` versus `$1` merge value;

and quote construction economics around own fair `q_i`.

All tests must use actual fee side (maker/taker), current tick, conversion `feeBips`, depth and synchronized timestamps.

---

# 13. Forecast model and deterministic arbitrage should share one event object

For each daily temperature event store:

`bucket_ids`
`condition_ids`
`YES token ids`
`NO token ids`
`negRisk market id`
`question indexes`
`conversion feeBips`
`tick sizes`
`taker fee parameters`
`books`
`q vector`
`forecast timestamp`
`resolver state`.

Then each candidate capital action can be ranked in common dollar terms:

1. deterministic full-YES basket;
2. deterministic full-NO conversion basket;
3. subset conversion cycle;
4. binary complete-set acquisition/merge;
5. passive maker quote;
6. directional forecast-revision taker trade;
7. tail acquisition;
8. hold/redeem nearly certain positions.

The bot should fund the highest **expected net dollars per capital-time** route, subject to executable capacity.

---

# 14. Highest-value historical measurement

Before building a full trading system, collect synchronized historical order books for resolved Weather events and replay these inequalities point-in-time.

For every detected violation record:

`event`
`timestamp`
`route`
`subset S`
`feeBips`
`raw top-of-book edge`
`depth-adjusted edge`
`maximum profitable size`
`gas`
`duration violation persisted`
`whether a passive leg could have improved it`
`realized next-tick markout`.

The decisive output is:

`net executable dollars/day`

and

`net executable dollars per $1,000 capital-hour`,

not the count of mathematical violations.

---

# 15. Immediate research priority created by this finding

The next API/on-chain acquisition should retrieve, for every current/historical Weather event:

- `negRiskMarketID`;
- question index for each bucket;
- adapter `getFeeBips(marketId)`;
- YES/NO token ids;
- synchronized multi-book snapshots.

Then run the subset scanner.

This can be implemented in a few hundred lines at most. There is no reason to build a general-purpose optimizer before seeing the empirical distribution of executable edge.

## Bottom line

The project now has a structural alpha layer that is independent of forecast superiority:

> **temperature ladders obey deterministic negative-risk portfolio identities, and Polymarket exposes an on-chain conversion that can immediately release collateral from NO baskets.**

Forecasting is still valuable, but it should sit **on top of** this arithmetic:

- deterministic cycles first;
- maker economics second;
- information-driven directional edge third;
- tails as an overlay.

The single most important unresolved parameter for this layer is the actual Weather-event conversion `feeBips`. Without it, small apparent subset arbitrages cannot be classified as executable.