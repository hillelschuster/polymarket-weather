# Transaction evidence: passive Weather makers + ultra-cheap tails

Snapshot: **2026-08-11**

Purpose: preserve the transaction-level specialist evidence while correcting an earlier over-attribution of exchange `merge` events to trader-initiated inventory recycling.

## Corrected verdict

Three economically distinct Weather behaviors are visible:

1. **directional taker after information revisions** — supplied wallet;
2. **zero-fee passive maker / two-sided inventory behavior** — Poligarch and likely related specialists;
3. **ultra-cheap tail YES accumulation** — GbushiCshuo and other penny-tail accounts.

A fourth operation — deliberate post-fill YES/NO merge — is a valid Polymarket market-making primitive, but it is **not yet empirically attributable to Poligarch or ColdMath from Struct merge counts alone**.

Reason: the CTF Exchange itself uses MINT/MERGE settlement paths while matching complementary orders. A transaction containing `PositionsMerge` may therefore be exchange plumbing rather than a discretionary trader action.

The detailed correction and maker mathematics are in:

`research/forecast-aware-maker-merge.md`.

---

# 1. Direct zero-fee Weather maker proof

Poligarch wallet:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

Transaction:

`0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213`

PolygonScan:

https://polygonscan.com/tx/0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213

Timestamp:

`2026-07-21 01:56:10 UTC`.

Daily Weather event:

**Wellington July 21 — 11°C**.

Relevant `OrderFilled` fields:

- maker = Poligarch;
- `makerAmountFilled = 9.400590 pUSD`;
- `takerAmountFilled = 9.990000` tokens;
- `fee = 0`.

Effective acquisition price:

`9.400590 / 9.990000 = 94.1¢`.

Direct conclusions:

- Poligarch supplies passive liquidity in Weather;
- maker platform fee is zero on this fill;
- the account acquires inventory through the neg-risk exchange path.

Do not infer exact economic YES/NO direction until the neg-risk token id is mapped to the event condition.

---

# 2. Direct evidence that merge events can be matching-engine plumbing

Transaction:

`0xee8fd0c9e0de9ceb8f42a615188dba0d40aa17f939075fc523fdcb63fcc0b716`

PolygonScan:

https://polygonscan.com/tx/0xee8fd0c9e0de9ceb8f42a615188dba0d40aa17f939075fc523fdcb63fcc0b716

Timestamp:

`2026-05-10 13:17:36 UTC`.

The same Neg Risk CTF Exchange transaction contains:

- multiple pUSD transfers from Poligarch into the exchange;
- zero-fee maker fills;
- a `PositionsMerge` path releasing **33.46** collateral.

The transaction is an exchange matching transaction, not a standalone Poligarch merge call.

Polymarket's official exchange code describes internal settlement modes:

- complementary BUY/SELL -> direct transfer;
- two BUY orders -> MINT;
- two SELL orders -> MERGE.

Source:

https://github.com/Polymarket/ctf-exchange-v2

Legacy matching overview:

https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md

Therefore:

> **Struct's trader-level merge count cannot be treated as proof of deliberate post-fill pair recycling without wallet-level attribution.**

This correction applies equally to ColdMath and any other specialist inferred from aggregate merge counts.

---

# 3. Madrid July 6 pair-capture candidate remains mathematically interesting, but unproven

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-madrid-on-july-6-2026-39c

Indexed snapshot showed Poligarch approximately:

- YES `+11.11 @ 55¢`;
- NO `+13.34 @ 43¢` roughly two minutes later.

If 11.11 shares were genuinely acquired as complementary inventory at those lot prices:

`combined cost = 98¢`

`gross complete-set value = $1`

`candidate pair capture = 2¢/share`

`candidate gross capture = 11.11 * 0.02 = $0.2222`.

This is **not realized-PnL evidence** until all of the following are reconstructed:

- exact order hashes;
- maker/taker role for each lot;
- token ids / condition mapping;
- preceding inventory;
- later wallet deltas;
- whether any merge was user-initiated or exchange-internal.

Use it only as a candidate transaction for a fill-level reconstruction.

---

# 4. ColdMath is still useful independent evidence — with corrected interpretation

ColdMath wallet:

`0x594edb9112f526fa6a80b8f858a6379c8a2c1c11`.

Struct indexed approximately:

- volume: **$14M**;
- buys: **224,892**;
- sells: **1,306**;
- merges: **6,790**;
- cumulative PnL: **$132K**.

Polymarket's indexed all-time Weather leaderboard placed ColdMath around **#3 by Weather profit**.

The useful conclusion is:

> major profitable Weather accounts can have transaction lifecycles very unlike simple `buy forecast -> sell forecast` trading.

Do **not** infer from the merge count alone that ColdMath manually recycled complete sets.

Struct rows where huge value is attributed to `merge` are an accounting warning, not an audited source of trader economic PnL.

---

# 5. Separate archetype: ultra-cheap tail YES accumulation

Trader:

`GbushiCshuo`

Wallet:

`0xfbb7fc19f80b26152fc5886b5eafa7d437f26f27`.

Struct indexed roughly:

- volume: **$159K–$165K** depending crawl time;
- buys: **~152K–156K**;
- sells: only **~72–73**;
- thousands of redemptions;
- merges: **0**;
- cumulative PnL: **~$13K**;
- tens of thousands of predictions/markets;
- extremely small average trade size in inspected periods.

The `merges = 0` feature matters: its penny Weather winners cannot be dismissed as merge-accounting artifacts.

Struct highlighted winning examples including:

- Paris Apr 6 — 21°C YES around **0.2¢** entry, under `$1` buys, roughly `$399` displayed win;
- Paris Apr 15 — 22°C YES around **0.4¢**, roughly `$399` win;
- Chongqing Mar 28 — 16°C YES around **0.4¢**, roughly `$398` win;
- Singapore Apr 1 — 34°C YES around **0.4¢**, roughly `$398` win;
- Denver Apr 1 — 52–53°F YES around **0.5¢**, roughly `$398` win;
- numerous 1–2¢ Weather outcomes with very large percentage returns on tiny cash outlay.

Direct market example:

https://explorer.struct.to/markets/highest-temperature-in-munich-on-march-16-2026-5c

showed GbushiCshuo buying roughly **200 YES @ 0.1¢** while other participants bought NO around **99.9¢**.

Another example:

https://explorer.struct.to/markets/highest-temperature-in-paris-on-march-2-2026-11corbelow

showed systematic 0.1¢ YES accumulation against 99.8–99.9¢ NO flow.

---

# 6. Tail economics

For a tail quote `p` and calibrated resolver probability `q`:

`EV/share = q - all_in_price`.

At `p = 0.001`:

- `q = 0.002` already implies roughly 100% gross expected return on purchase cost;
- `q = 0.005` implies roughly 400% gross expected return on purchase cost.

The structural Weather rationale is plausible:

- exact daily extrema are noisy;
- station/model basis error is nonzero;
- brief maxima/minima depend on cloud, wind and local timing;
- one-degree bucket tails can retain genuine probability when humans round them toward zero;
- stale penny liquidity can remain after forecast updates.

But the decisive statistic is not highlighted winners. It is the **full basket**:

`sum(fill_qty_i * (q_i - effective_cost_i))`.

Measure:

- all penny-tail fills, including losers;
- calibrated probability at fill time;
- fillable depth;
- fee rounding / tick size;
- payout distribution;
- net dollars per day;
- capacity at bankroll scales.

The expected capacity is probably much smaller than mainstream mid-price Weather making/taking, so this remains an overlay until the full history proves otherwise.

---

# 7. Current Weather fee nuance helps extreme tails

Current Weather taker fees follow:

`fee = shares * 0.05 * p * (1-p)`.

Polymarket documentation states fees are rounded to five decimal places; sufficiently small fees can round to zero.

Sources:

https://docs.polymarket.com/trading/fees

https://docs.polymarket.com/market-makers/maker-rebates

At extreme prices and tiny order sizes, this can materially lower friction versus mid-price taker trades.

Do not assume zero fee without calculating the actual current order size, price, tick and fee rounding.

---

# 8. Updated profitability ordering

## 1. Information-driven directional layer

Evidence quality:

- target-wallet taker role and fees proven on-chain;
- losing-bucket reduction visible;
- near-$1 winner recycling visible;
- specific forecast/observation catalyst mapping still incomplete.

Highest-value missing measurement:

**point-in-time `Δq` at each fill + post-fill markout.**

## 2. Forecast-aware passive maker layer

Evidence quality:

- direct Weather maker fill proven;
- zero maker fee proven;
- same-market two-sided inventory visible;
- rebates material;
- major profitable Weather specialists exhibit highly nonstandard buy/sell patterns.

Highest-value missing measurement:

**maker fill markout and trader-level inventory/cashflow ledger.**

## 3. Deliberate pair-and-merge recycling

Economics are exact and officially supported, but specialist attribution is currently unproven.

Highest-value missing measurement:

**dedicated trader-initiated merge calls after complementary fills, separated from exchange-internal MINT/MERGE settlement.**

## 4. Penny-tail overlay

Evidence quality:

- direct historical tiny YES fills;
- repeated huge percentage winners;
- zero merge count for the observed specialist.

Highest-value missing measurement:

**full loser-inclusive historical basket and actual dollar capacity.**

---

# 9. Minimal unified engine implied by the evidence

Maintain one coherent exact-resolver probability vector:

`q = (q_1,...,q_K)`.

Use it through three execution modes.

### Passive maker

For binary bucket `i`:

`bid_yes_i = q_i - margin_yes_i`

`bid_no_i = 1 - q_i - margin_no_i`.

Margins should exceed expected fill-conditioned adverse selection and uncertainty.

### Taker after information shock

`EV_cross = q_new - executable_price - taker_fee - impact`.

Cancel stale quotes and cross only clearly positive-EV depth.

### Tail acquisition

`EV_tail = q_tail - effective_microprice - rounded_fee`.

Use small maker/taker orders only where the calibrated nonzero tail probability materially exceeds cost.

Manual pair merge is an inventory operation available whenever complementary balances make it economically superior; do not make it the strategy's assumed source of PnL until live data validates it.

---

# Highest-value next measurement

The research bottleneck is now clearer than before:

1. reconstruct the target wallet's full fill stream to learn **what information shocks justify paying taker fees**;
2. reconstruct one Poligarch Weather market at wallet-delta level to learn **maker markout, inventory path and true spread economics**;
3. explicitly classify each on-chain `MINT/MERGE` as **exchange settlement vs trader-initiated operation**;
4. backtest the full penny-tail basket without survivor selection.

Those measurements are sufficient to decide which execution path deserves capital.