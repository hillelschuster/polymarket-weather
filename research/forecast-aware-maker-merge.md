# Forecast-aware maker/merge — strongest new structural weather hypothesis

Snapshot: **2026-08-11**

Purpose: identify the smallest reproducible monetization mechanism behind high-frequency profitable Polymarket behavior that can be combined with the existing weather probability engine.

## Verdict

The strongest new evidence is not another forecast model. It is a **different way to monetize the same fair probabilities**:

> **Post passive bids on both complementary YES and NO tokens, acquire inventory below combined collateral value when flow permits, merge matched pairs back into $1 pUSD, collect maker rebates, and let the weather model control quote skew and unpaired-inventory risk. Cross the spread only when a forecast/observation shock is too fast to wait for passive fills.**

This is materially different from a pure directional forecast bettor, but it is complementary to the supplied wallet's apparent forecast-revision behavior.

The most important empirical clue is `Poligarch`.

Wallet:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

Struct's Aug 10 indexed snapshot shows:

- cumulative PnL: **~$207K**;
- volume: **~$24.5M**;
- fees paid: **~$2.29K**;
- buys: **1,612,158**;
- sells: **1,287**;
- redemptions: **40,882**;
- merges: **67,647**;
- splits: **0**;
- converts: **2**;
- rebates: **~$19.3K**;
- liquidity rewards: **~$5.52K**.

Source:
https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

The operation-count shape is extreme: roughly **1,253 buys per sell** and **53 merges per sell**. Counts are operations rather than token quantities, so they do not directly reveal dollars recycled, but they strongly reject a conventional buy-then-sell trading lifecycle.

The parsimonious interpretation is **buy-heavy passive inventory acquisition followed by merge/redemption**, with sells used rarely.

---

# 1. Direct same-market evidence: Poligarch owns both YES and NO

The Aug 10 Struct snapshot shows complementary positions in the same weather binaries.

Examples:

### New York City Aug 10 — 90–91°F

- YES: 126.73 shares, average entry 47.4¢, 24 buys;
- NO: 103.94 shares, average entry 53.5¢, 13 buys.

### New York City Aug 10 — 92–93°F

- YES: 137.29 shares, average entry 19.0¢, 13 buys;
- NO: 235.10 shares, average entry 74.2¢, 29 buys.

### New York City Aug 10 — 88–89°F

- YES: 73.12 shares, average entry 28.1¢, 10 buys;
- NO: 99.90 shares, average entry 71.6¢, 9 buys.

### Houston Aug 10 — 92–93°F

- YES: 21.25 shares, average entry 6.4¢, 3 buys;
- NO: 41.25 shares, average entry 77.8¢, 6 buys.

### Toronto Aug 10 — 28°C

- YES: 90.11 shares, average entry 28.0¢, 5 buys;
- NO: 132.20 shares, average entry 71.5¢, 14 buys.

### London Aug 10 — 26°C

- YES: 190.69 shares, average entry 56.6¢, 22 buys;
- NO: 237.82 shares, average entry 53.3¢, 26 buys;
- Struct also displays merge activity on both rows.

Source:
https://explorer.struct.to/traders/0xb40e89677d59665d5188541ad860450a6e2a7cc9

This is not consistent with interpreting every visible position as an independent directional forecast. A market maker accumulating both complementary tokens can have both positions visible before matched quantity is merged.

Do **not** sum displayed average YES and NO entry prices and treat that as the economics of a matched pair. The averages pool different fill times and residual inventory after prior merges; quantities differ; already-merged lots may no longer appear in the current balance. Chronological fill matching is required.

---

# 2. Why merge is economically powerful

Polymarket's official CTF mechanics are exact:

`1 YES + 1 NO -> $1 pUSD`

For `m` matched shares acquired at cash costs `bY` and `bN` per share:

`pair_cash_cost = m * (bY + bN)`

`merge_proceeds = m`

so before incentives and operational costs:

`locked_pair_pnl = m * (1 - bY - bN)`

If both acquisitions are maker fills and:

`bY + bN < 1`

then the matched pair has positive mechanical PnL independent of the weather outcome.

Official merge docs:
https://docs.polymarket.com/trading/ctf/merge

Official positions/token mechanics:
https://docs.polymarket.com/concepts/positions-tokens

Polymarket's market-maker inventory docs explicitly describe merging equal YES/NO inventory to free capital and skewing quotes when inventory becomes imbalanced:
https://docs.polymarket.com/market-makers/inventory

This gives a clean capital-recycling loop:

`resting maker bids`

`-> one/both sides fill`

`-> pair min(YES_balance, NO_balance)`

`-> merge paired amount`

`-> pUSD immediately reusable`

`-> keep only residual directional inventory`

The central economic variable is therefore not gross trade volume. It is:

`net_pair_capture = 1 - acquisition_cost_yes - acquisition_cost_no + attributable_rebate + attributable_rewards - residual_inventory_loss - operational_cost`

---

# 3. Weather's current fee structure makes passive acquisition especially attractive

Polymarket's current Weather fee schedule is:

- taker fee rate: **0.05**;
- maker fee rate: **0**;
- maker rebate allocation: **25%** of eligible taker fees.

The fee curve is:

`fee = shares * 0.05 * p * (1-p)`

Official source:
https://docs.polymarket.com/trading/fees

For fee-curve-weighted maker rebates, each maker fill receives a fee-equivalent weight:

`fee_equivalent = shares * 0.05 * p * (1-p)`

and the daily market rebate is allocated as:

`rebate = own_fee_equivalent / total_market_fee_equivalent * rebate_pool`

The exact rebate is therefore competition-dependent. It is **not** correct to assume that a maker automatically gets 25% of the fee-equivalent generated by its own fill.

Maker rebate docs:
https://docs.polymarket.com/market-makers/maker-rebates

Economic implication:

- a taker directional strategy loses roughly 1–1.25 probability points to platform fee near the 30–70¢ region before additional book walking;
- a maker pays zero platform trading fee;
- a successful maker may additionally receive part of the rebate pool.

This makes maker-first execution economically important even if the weather probability model is unchanged.

---

# 4. Liquidity rewards are a separate optional income stream

Polymarket also has per-market liquidity rewards for resting competitive orders. Reward eligibility and economics are **market-specific**, so do not assume every daily-temperature contract carries an active LP reward.

Current configuration can be queried from:

`GET https://clob.polymarket.com/rewards/markets/current`

Official docs:
https://docs.polymarket.com/api-reference/rewards/get-current-active-rewards-configurations

The scoring design explicitly rewards tighter quotes, size and two-sided liquidity; single-sided quoting can score in central probability ranges, while extreme-price markets require two-sided liquidity.

Methodology:
https://docs.polymarket.com/market-makers/liquidity-rewards

For a live weather market the engine should read:

- `rewards_max_spread`;
- `rewards_min_size`;
- daily reward rate;
- current competition / expected share;

and add expected reward only when it is actually configured.

Struct's current rewards page did not surface Weather among the top indexed reward markets inspected on Aug 11, so LP rewards should currently be treated as an opportunistic overlay, not the primary weather thesis.

---

# 5. Poligarch's incentives are economically material but not sufficient to explain PnL

Using Struct's Aug 10 displayed totals only as rough ratios:

- rebates / displayed volume ≈ **7.88 bps**;
- liquidity rewards / displayed volume ≈ **2.25 bps**;
- combined incentives / displayed volume ≈ **10.13 bps**;
- fees paid / displayed volume ≈ **0.93 bps**;
- combined displayed incentives are ≈ **12.0% of displayed cumulative PnL**.

These ratios are descriptive, not audited realized-return attribution. Struct's volume/PnL/merge accounting may use different bases, and some PnL is associated with open inventory.

Still, two facts are useful:

1. **maker incentives are large enough to matter**;
2. **they are not large enough by themselves to explain the displayed $207K PnL**.

The remaining return plausibly comes from some combination of:

- spread/pair capture;
- directional inventory alpha;
- cross-market/neg-risk transformations;
- resolution/redemption economics;
- other non-weather categories.

Therefore the target is not “farm rebates.” The target is a profitable market-making loop whose economics remain positive before uncertain rewards, with rebates as incremental income.

---

# 6. A second archetype supports basket/liquidity behavior

`automatedAItradingbot` shows a different but related pattern.

Struct indexed roughly:

- 28K buys;
- 10K sells;
- hundreds of merges;
- >$1M volume;
- large weather-market wins.

Publicly indexed Seoul May 30 positions showed many different exact-temperature buckets acquired at approximately the same **9.1¢** entry and **1,000-share** size, including both the eventual winner and multiple losers.

This is much more compatible with a grid/basket/liquidity strategy than a one-bucket point forecast.

The evidence does **not** prove that all ladder buckets filled simultaneously or as maker orders. The useful conclusion is narrower: profitable weather activity includes systematic multi-bucket inventory behavior that a purely directional model would miss.

---

# 7. The correct synthesis: weather model as market-maker control surface

The existing research already argues for a coherent probability vector:

`q = (q_1, ..., q_K)`

for the mutually exclusive resolver ladder.

For each binary bucket `i`:

- fair YES = `q_i`;
- fair NO = `1-q_i`.

A maker should not quote a symmetric fixed spread around the market midpoint. It should quote around its **own resolver probability** and inventory state.

Minimal form:

`bid_yes_i < q_i - required_margin_yes_i`

`bid_no_i < (1-q_i) - required_margin_no_i`

where required margin absorbs:

- expected adverse selection;
- uncertainty in q;
- residual inventory cost;
- opportunity cost of capital;
- expected rebate/reward can reduce the required margin only after measured.

If both sides fill:

`pair_qty_i = min(YES_balance_i, NO_balance_i)`

merge `pair_qty_i` immediately when the released collateral is more valuable than retaining a full pair.

Residual directional inventory:

`net_yes_i = YES_balance_i - NO_balance_i`

A positive value is net YES exposure; a negative value is economically net NO exposure.

Weather probability controls how aggressively the engine tries to acquire the opposite leg versus retaining the residual view.

---

# 8. Forecast revisions define when passive quoting should stop

The supplied wallet remains useful because its recovered Milan behavior suggests directional posterior revision:

- T+1 35°C purchase around 30¢ all-in on Milan Jun 30;
- large reduction of Milan Jun 25 33°C after the bucket deteriorated;
- near-$1 winner sale immediately after local day end in Mexico City.

These behaviors are compatible with an execution router:

## Quiet information state

Forecast distribution changes slowly.

Prefer maker acquisition because:

- zero platform fee;
- spread capture opportunity;
- possible rebate;
- possible LP reward;
- enough time to wait for fill.

## Fresh forecast/observation shock

If `Δq` is large and market response half-life is short:

`EV_cross = q_new - executable_ask - taker_fee - impact`

Cross when immediate expected dollars exceed the passive alternative.

## After deterioration

For an existing YES position at bid `b`:

`net_bid = b - taker_sell_fee`

sell when net realizable value exceeds updated hold value, unless an opposite maker fill/merge route is better.

## Near physical certainty

When the resolver maximum is effectively locked, compare:

- holding to $1;
- selling near $1;
- pairing/merging where possible;
- redeploying collateral into another live edge.

This unifies the supplied wallet's directional behavior with Poligarch's inventory mechanics.

---

# 9. Negative-risk adds a second transformation layer

Daily-temperature events are multi-outcome negative-risk events. In addition to binary YES/NO merge inside an outcome market, Polymarket's neg-risk mechanism creates the identity:

`NO_i ≡ sum(YES_j for j != i)`

Therefore residual inventory should not be valued only against its same-binary opposite side.

At every event snapshot compare:

1. acquire opposite token and merge;
2. keep residual directional exposure;
3. use neg-risk conversion into the other event outcomes;
4. acquire a basket of other YES tokens;
5. sell/cross existing inventory.

The optimal route is the one returning the most pUSD / expected value after actual executable prices and costs.

This is especially attractive in temperature ladders because forecast shocks mostly move mass among neighboring buckets. An engine that knows the entire coherent `q` vector can identify the cheapest way to neutralize or transform unwanted inventory.

---

# 10. Highest-value experiment is now chronological fill -> merge reconstruction

The original highest-value unknown was the entry/revision/exit path of the supplied wallet's Milan positions.

That remains valuable for directional alpha, but the new structural evidence makes one additional experiment at least as important:

> **Reconstruct one full Poligarch weather day at fill level and determine whether complementary maker buys create positive realized pair capture before rebates.**

For one city/date, collect:

`timestamp`
`condition_id`
`outcome`
`token_id`
`YES/NO`
`BUY/SELL`
`maker/taker`
`shares`
`price`
`fee`
`order_hash`
`tx_hash`
`merge_timestamp`
`merge_quantity`
`rebate allocation`
`LP reward allocation`

Then perform FIFO or lot-aware inventory matching and calculate:

`paired_acquisition_cost`
`merge_proceeds`
`raw_pair_pnl`
`rebate`
`reward`
`unpaired_inventory_markout`
`settlement_pnl`

The decisive questions are:

1. What percentage of acquired shares are eventually merged rather than sold/redeemed?
2. What is the distribution of `1 - bY - bN` for actual paired lots?
3. How long is capital exposed between first-leg and second-leg fill?
4. How much adverse selection occurs on the first filled leg after weather updates?
5. How much of PnL survives with **rebates and LP rewards set to zero**?
6. Does weather-aware skew predict which side fills before the market moves?
7. What is net PnL per $1M maker turnover and per dollar-hour of unpaired inventory?

If pre-incentive paired PnL is positive and repeatable, this is a structural engine worth building immediately.

---

# 11. Accounting warning: Struct position PnL is not sufficient for transformed inventory

Struct is extremely useful for discovery, but its per-position presentation can become misleading when merges/conversions move value between tokens.

Concrete warning signs found in this research:

- some merge-heavy rows display large negative position PnL even though merge value has separately left the position;
- another trader page displayed a “best win” far above its “best day,” indicating that position-level attribution and daily realized accounting are not interchangeable.

Therefore the economic ledger for this strategy must be reconstructed at cashflow/event level:

`pUSD spent on buys`
`+ pUSD received from sells`
`+ pUSD released by merges`
`+ redemption proceeds`
`+ rebates`
`+ rewards`
`- fees`
`+ terminal value of open inventory`

That is the quantity to optimize.

Do not rank strategies from Struct's displayed per-token PnL without reconciling transformation cashflows.

---

# 12. Minimal production strategy implied by current evidence

The current best small professional design is now:

### Probability layer

Maintain coherent exact-resolver probabilities over every bucket using:

- point-in-time model vintages;
- station/horizon residual calibration;
- current resolver observations;
- full-ladder normalization.

### Passive monetization layer

For each binary outcome:

- post maker bids where fair value exceeds quote by enough to cover fill-conditioned adverse selection;
- quote both complementary sides when pair economics are favorable;
- skew based on q and residual inventory;
- merge matched YES/NO immediately to recycle collateral;
- include actual rebate/reward configuration when present.

### Fast directional layer

After meaningful model/observation revisions:

- cancel stale maker quotes immediately;
- cross only the stale depth with clear fee-adjusted EV;
- update all neighboring buckets coherently.

### Capital ranking

Rank each marginal dollar among:

- passive pair-capture opportunity;
- directional taker opportunity;
- residual inventory reduction;
- late-certainty recycling;
- another city/event.

The objective remains:

`maximize expected net dollars / capital-time`

not trade count, rebate amount, win rate or nominal volume.

---

# Bottom line

The earlier research was centered on finding a better weather forecast and copying directional specialists.

The new evidence adds a stronger structural income mechanism:

> **forecast-informed market making with buy-heavy inventory acquisition and aggressive merge-based collateral recycling.**

Poligarch is the clearest evidence: enormous buy count, almost no sells, tens of thousands of merges, material rebates/rewards, and simultaneous YES/NO weather inventory.

The highest-value next measurement is a **single complete weather-day fill/merge ledger** for Poligarch, followed in parallel by the Milan forecast-revision reconstruction for the supplied wallet.

Those two datasets answer complementary questions:

- **where does fair-value alpha come from?** — supplied wallet / forecast revisions;
- **how should we monetize it most efficiently?** — maker fills / paired inventory / merge / incentives.
